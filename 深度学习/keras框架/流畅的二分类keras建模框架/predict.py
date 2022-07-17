import numpy as np
import pandas as pd
from data_process import data_process

# 模型以及参数位置
MODEL_NAME = "captcha_adam_binary_crossentropy_bs_2048_epochs_450.h5"
MODEL_PATH = 'model/92.09/'

import sys
sys.path.append(MODEL_PATH)
from pre_model import model


# 参数以及模型对应的超参数
OPT = 'adam'
LOSS = 'binary_crossentropy'
dropout_ALPHA = 0.5


# 加载模型和参数
def load_model():
	pre_model = model(LOSS, OPT, dropout_ALPHA)
	pre_model.load_weights(MODEL_PATH + MODEL_NAME)

	return pre_model


# 预测
def predict(test, pre_model):
	predict_result = pre_model.predict(test)
	predict_result = list(predict_result.reshape(len(predict_result),))

	# 根据赛题要求，不是0就是1
	# result=[]
	# for i in predict_result:
	# 	if i < 0.5:
	# 		i = 0
	# 	else:
	# 		i = 1
	# 	result.append(i)

	return predict_result


# 保存为csv
def save_csv(sid, result):
	result_table = pd.DataFrame({"sid": sid, "label": result})
	result_table.to_csv("predict.csv", index=False)


if __name__ == "__main__":
	pre_model = load_model()
	input1, input2, sid = data_process(train=False)
	result = predict([input1, input2], pre_model)
	save_csv(sid, result)
