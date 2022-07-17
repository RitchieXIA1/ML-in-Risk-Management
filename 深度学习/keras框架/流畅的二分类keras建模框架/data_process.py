import pandas as pd
import numpy as np
import json
from keras.utils import np_utils


# 连续值特征数据处理
def continuous_features(data):
	# 数值归一化
	def normalize_feature(df):
		return df.apply(lambda column: (column - column.mean()) / column.std())

	continuous_train = data[["time", "resolution_ratio"]]
	continuous_train = normalize_feature(continuous_train)

	# ip字段就只有0和1，不需要归一化
	continuous_train["ip"] = data["ip"]

	continuous_train = np.array(continuous_train)

	return continuous_train


# one-hot特征数据处理
def one_hot_features(data):
	# 构建one-hot向量
	def make_one_hot(feature, one_hot_data):
		# 有几个特征本身已经做好了索引，故并没有放在json文件当中
		try:
			n = len(index_json[feature])
		except:
			n = int(data[feature].max())

		return np_utils.to_categorical(one_hot_data, n + 1)

	# 导入json文件
	with open("data/index_json.json", "r") as f:
		index_json = json.load(f)

	one_hot_set = {}
	for i in ["apptype", "dvctype", "ntt", "carrier", "orientation", "lan"]:
		one_hot_set[i] = make_one_hot(i, np.uint8(data[i].values.reshape(len(data[i]), 1)))

	one_hot_train = np.hstack(tuple(one_hot_set.values()))

	return one_hot_train


# embedding特征数据处理
def embedding_features(data):
	embedding_train = data[["pkgname", "adunitshowid", "mediashowid", "city", \
					"adidmd5", "imeimd5","openudidmd5", "macmd5", \
					"model", "osv"]]
	embedding_train = np.array(embedding_train)

	return embedding_train


# 数据处理
def data_process(train=True):
	if train == True:
		data = pd.read_csv("data/train_clean.csv")
	else:
		data = pd.read_csv("data/test_clean.csv")
		sid = pd.read_csv("data/test.csv")
		sid = list(sid["sid"])

	continuous_train = continuous_features(data)
	one_hot_train = one_hot_features(data)
	embedding_train = embedding_features(data)

	# 合并不是embedding的数据
	unembedding_train = np.hstack((continuous_train, one_hot_train))

	# 对train数据和test数据分开return
	if train == True:
		return unembedding_train, \
			   embedding_train, \
			   np.array(data["label"]).reshape(len(data["label"]), 1)
	else:
		return unembedding_train, \
			   embedding_train, \
			   sid
