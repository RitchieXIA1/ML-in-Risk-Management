from data_process import data_process
from model import model
import os
import tensorflow.gfile as gfile
import pickle

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


# 超参数
OPT = 'adam'
LOSS = 'binary_crossentropy'
dropout_ALPHA = 0.5
BATCH_SIZE = 2048
EPOCHS = 450

# 参数
DATA_PATH = "data/"
MODEL_DIR = './model/first/'
MODEL_FORMAT = '.h5'
HISTORY_DIR = './history/first/'
HISTORY_FORMAT = '.history'
filename_str = "{}captcha_{}_{}_bs_{}_epochs_{}{}"
MODEL_FILE = filename_str.format(MODEL_DIR, OPT, LOSS, \
				str(BATCH_SIZE), str(EPOCHS), MODEL_FORMAT)
HISTORY_FILE = filename_str.format(HISTORY_DIR, OPT, LOSS, \
				str(BATCH_SIZE), str(EPOCHS), HISTORY_FORMAT)


# 保存模型和历史记录
def save_model(model, history):
	if not gfile.Exists(MODEL_DIR):
		gfile.MakeDirs(MODEL_DIR)

	model.save(MODEL_FILE)

	if gfile.Exists(HISTORY_DIR) == False:
		gfile.MakeDirs(HISTORY_DIR)

	with open(HISTORY_FILE, 'wb') as f:
		pickle.dump(history.history, f)


if __name__ == "__main__":
	# input1为unembedding数据，input2为embedding数据
	input1, input2, Y_train = data_process()
	model = model(LOSS, OPT, dropout_ALPHA)

	history = model.fit([input1, input2],
						Y_train,
						batch_size=BATCH_SIZE,
						epochs=EPOCHS,
						verbose=2,
						validation_split=0.01)

	save_model(model, history)
