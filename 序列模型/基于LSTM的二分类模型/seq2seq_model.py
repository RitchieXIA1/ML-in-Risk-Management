# ==============================================================================
# -*- coding: utf-8 -*-
# @Time    : 2020-03-08 PM 2:00
# @Author  : deymm
# @Email   : deymm671@126.com
# ==============================================================================

"""encoder2predict model for text classification.
"""
from collections import namedtuple

import numpy as np
import tensorflow as tf
import parameter_config

HParams = namedtuple('HParams',
                     'mode, batch_size, enc_timesteps, emb_dim, min_input_len, '
                     'num_hidden, enc_layers, min_lr, lr, max_grad_norm')


class Seq2SeqModel(object):
    """Wrapper for Tensorflow model graph for text sum vectors."""

    def __init__(self, hps, vocab, num_gpus=0):
        self._hps = hps
        self._vocab = vocab
        self._num_gpus = num_gpus
        self._cur_gpu = 0

    def run_train_step(self, sess, target_batch, enc_batch, enc_input_lens, nn_keep_prob, emb_keep_prob):
        to_return = [self._loss, self.global_step, self._train_op]
        return sess.run(to_return,
                        feed_dict={self._input: enc_batch,
                                   self._targets: target_batch,
                                   self._input_lens: enc_input_lens,
                                   self._nn_keep_prob: nn_keep_prob,
                                   self._emb_keep_prob: emb_keep_prob})

    def run_eval_step(self, sess, target_batch, enc_batch, enc_input_lens, nn_keep_prob, emb_keep_prob):
        to_return = [self._loss, self._predict, self.global_step]
        return sess.run(to_return,
                        feed_dict={self._input: enc_batch,
                                   self._targets: target_batch,
                                   self._input_lens: enc_input_lens,
                                   self._nn_keep_prob: nn_keep_prob,
                                   self._emb_keep_prob: emb_keep_prob})

    def run_decode_step(self, sess, target_batch, enc_batch, enc_input_lens, nn_keep_prob, emb_keep_prob):
        to_return = [self._logits, self._predict, self.global_step]
        return sess.run(to_return,
                        feed_dict={self._input: enc_batch,
                                   self._targets: target_batch,
                                   self._input_lens: enc_input_lens,
                                   self._nn_keep_prob: nn_keep_prob,
                                   self._emb_keep_prob: emb_keep_prob})

    def _next_device(self):
        """Round robin the gpu device. (Reserve last gpu for expensive op)."""
        if self._num_gpus == 0:
            return ''
        dev = '/gpu:%d' % self._cur_gpu
        if self._num_gpus > 1:
            self._cur_gpu = (self._cur_gpu + 1) % (self._num_gpus - 1)
        return dev

    def _get_gpu(self, gpu_id):
        if self._num_gpus <= 0 or gpu_id >= self._num_gpus:
            return ''
        return '/gpu:%d' % gpu_id

    def _add_placeholders(self):
        """Inputs to be fed to the graph."""
        hps = self._hps
        self._input = tf.placeholder(tf.int32, [hps.batch_size, hps.enc_timesteps],name='input')
        self._targets = tf.placeholder(tf.float32, [hps.batch_size, 1], name='targets')
        self._input_lens = tf.placeholder(tf.int32, [hps.batch_size], name='input_lens')
        self._nn_keep_prob = tf.placeholder(tf.float32)
        self._emb_keep_prob = tf.placeholder(tf.float32)

    def _add_seq2seq(self):
        hps = self._hps
        vsize = self._vocab.NumIds()

        with tf.variable_scope('seq2seq'):
            # ????????????
            encoder_inputs = self._input
            targets = self._targets
            input_lens = self._input_lens

            # ?????????????????????embedding
            with tf.variable_scope('embedding'), tf.device('/cpu:0'):
                embedding = tf.get_variable('embedding', [vsize, hps.emb_dim], dtype=tf.float32)
                emb_encoder_inputs = tf.nn.embedding_lookup(embedding, encoder_inputs)

            # ???embedding????????????????????????encoder
            with tf.variable_scope('encoder'), tf.device(self._next_device()):
                # ??????dropout???LSTM
                lstm_cell = [tf.nn.rnn_cell.DropoutWrapper(tf.nn.rnn_cell.LSTMCell(hps.num_hidden), 
                    self._nn_keep_prob) for _ in range(hps.enc_layers)]
                cell = tf.nn.rnn_cell.MultiRNNCell(lstm_cell)

                # ???????????????dropout??????
                dropout_emb_encoder_inputs = tf.nn.dropout(emb_encoder_inputs, self._emb_keep_prob)
                # ??????rnn??????
                outputs, last_states = tf.nn.dynamic_rnn(cell, dropout_emb_encoder_inputs, 
                    sequence_length = input_lens, dtype=tf.float32)
                ## last_output = outputs[:,-1,:]
                # ??????????????????????????????????????????encoder??????????????????
                last_output = last_states[-1].h

            # ???encoder????????????????????????NN???????????????sigmoid????????????????????????LR???
            with tf.variable_scope('predict'), tf.device(self._next_device()):
                # ?????????????????????
                weights = tf.get_variable('weights', [hps.num_hidden, 1], dtype=tf.float32, 
                    initializer=tf.truncated_normal_initializer(stddev=0.5))
                bias = tf.get_variable('bias', [1], dtype=tf.float32,
                    initializer=tf.truncated_normal_initializer(stddev=0.5))
                # ??????????????????
                logits = tf.matmul(last_output, weights) + bias
                self._logits = logits
                # ???????????????????????????sigmoid
                self._predict = tf.nn.sigmoid(self._logits)

            # ??????loss??????logits??????sigmoid????????????????????????????????????????????????
            with tf.variable_scope('loss'), tf.device(self._next_device()):
                loss = tf.nn.sigmoid_cross_entropy_with_logits(logits=logits, labels=targets)
                self._loss = tf.reduce_mean(loss)

    def _add_train_op(self):
        """??????????????????????????????self._train_op."""
        hps = self._hps

        self._lr_rate = tf.maximum(
            hps.min_lr,  # min_lr_rate.
            tf.train.exponential_decay(hps.lr, self.global_step, 
                parameter_config.LR_DECAY_STEP, parameter_config.LR_DECAY))

        tvars = tf.trainable_variables()
        # SGD ??????????????????????????????0.1??????
        # with tf.device(self._get_gpu(self._num_gpus - 1)):
        #     # ??????????????????????????????
        #     grads, global_norm = tf.clip_by_global_norm(
        #         tf.gradients(self._loss, tvars), hps.max_grad_norm)
        # optimizer = tf.train.GradientDescentOptimizer(self._lr_rate)
        # self._train_op = optimizer.apply_gradients(
        #     zip(grads, tvars), global_step=self.global_step, name='train_step')

        # Adam ??????
        optimizer_op = tf.train.AdamOptimizer(self._lr_rate).minimize(self._loss, global_step=self.global_step)
        # ??????????????????
        ema = tf.train.ExponentialMovingAverage(parameter_config.EMA_RATE, self.global_step)
        variables_averages_op = ema.apply(tvars)

        with tf.control_dependencies([optimizer_op, variables_averages_op]):
            self._train_op = tf.no_op('train')

    def build_graph(self):
        self._add_placeholders()
        self._add_seq2seq()
        self.global_step = tf.Variable(0, name='global_step', trainable=False)
        if self._hps.mode == 'train':
            self._add_train_op()
