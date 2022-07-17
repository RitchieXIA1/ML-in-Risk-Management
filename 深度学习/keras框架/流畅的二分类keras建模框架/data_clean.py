import pandas as pd
import json
from datetime import timedelta, datetime


# 删除部分字段
def del_features(data):
	del_list = ["sid", "ver", "province", "idfamd5", "make", "os", "reqrealip"]
	if data is data2:
		del del_list[0]

	for i in del_list:
		del data[i]

	print("del ok")


# 将nginxtime换算成分钟，并放在新特征time
def nginxtime(data):
	data['datetime'] = pd.to_datetime(data['nginxtime'] / 1000, unit='s') + \
					   timedelta(hours=8)
	data['hour'] = data['datetime'].dt.hour
	data['day'] = data['datetime'].dt.day - data['datetime'].dt.day.min()
	data['minute'] = data['datetime'].dt.minute.astype('uint8')
	data["time"] = data['day'] * 24 * 60 + data['hour'] * 60 + data['minute']

	for i in ["datetime", "hour", "day", "minute"]:
		del data[i]

	print("nginxtime ok")


# 形成新字段像素值，resolution_ratio
def h_w_ppi(data):
	new_h = data["h"] + 0.1
	new_w = data["w"] + 0.1
	new_ppi = data["ppi"] + 0.1
	resolution_ratio = new_h * new_w * new_ppi

	del data["h"]
	del data["w"]
	del data["ppi"]

	data["resolution_ratio"] = resolution_ratio
	print("h_w_ppi ok")


# 将ip地址与城市名称相比较，如果相符则为0,不相符则为1
def ip(data):
	# 从网上爬取的ip对应城市的json文件导入
	with open("data/ip_index.json", "r") as f:
		ip_index = json.load(f)

	new_ip = []
	for n, i in enumerate(data["ip"]):
		try:
			if ip_index[i] in data["city"][n]:
				new_ip.append(0)
			else:
				new_ip.append(1)
		except:
			new_ip.append(1)

	data["ip"] = new_ip
	print("ip ok")


def dvctype(data):
	new_dvctype = []
	for i in data["dvctype"]:
		if i == 3:
			i = 1
		new_dvctype.append(i)

	data["dvctype"] = new_dvctype
	print("dvctype ok")


def orientation(data):
	new_orientation = []
	for i in data["orientation"]:
		if i == 90:
			i = 2
		new_orientation.append(i)

	data["orientation"] = new_orientation
	print("orientation ok")


def apptype(data1, data2):
	global json_dict

	def process(data):
		new_apptype = []
		for i in data["apptype"]:
			try: 
				new_apptype.append(apptype_set.index(i))
			except:
				new_apptype.append(len(apptype_set))
		data["apptype"] = new_apptype

	apptype_set = list(set(data1["apptype"]) & set(data2["apptype"]))
	json_dict["apptype"] = apptype_set

	process(data1)
	process(data2)
	print("apptype ok")


def carrier(data1, data2):
	global json_dict

	def process(data):
		new_carrier = []
		for i in data["carrier"]:
			new_carrier.append(carrier_set.index(i))
		data["carrier"] = new_carrier

	carrier_set = list(set(data1["carrier"]) & set(data2["carrier"]))
	json_dict["carrier"] = carrier_set

	process(data1)
	process(data2)
	print("carrier ok")


def lan(data1, data2):
	global json_dict

	def process_1(data):
		new_lan = []
		for i in data["lan"]:
			try:
				for j in i:
					if j in lan_del_string:
						i = i.replace(j,"")

				i = i.lower()
			except:
				pass
			finally:
				new_lan.append(i)

		return new_lan

	def process_2(data, new_lan):
		for n, i in enumerate(new_lan):
			try:
				new_lan[n] = lan_set.index(i)
			except:
				new_lan[n] = len(lan_set)
		data["lan"] = new_lan

	lan_del_string = ["_", "-"]

	new_lan_1 = process_1(data1)
	new_lan_2 = process_1(data2)

	lan_set = list(set(new_lan_1) & set(new_lan_2))
	json_dict["lan"] = lan_set

	process_2(data1, new_lan_1)
	process_2(data2, new_lan_2)
	print("lan ok")


# 对model进行初步处理
def model(data):
	model_del_string = [" ", "_", ",", "+", "/", "-", "%", "(", ")", "."]
	special_type = {'PACM00': "OPPO R15", 'PBAM00': "OPPO A5", \
					'PBEM00': "OPPO R17", 'PADM00': "OPPO A3", \
					'PBBM00': "OPPO A7", 'PAAM00': "OPPO R15_1", \
					'PACT00': "OPPO R15_2", 'PABT00': "OPPO A5_1", \
					'PBCM10': "OPPO R15x"}
	new_model = []

	# 把一些定制手机的型号转换成一般形式
	for i in special_type:
		data['model'].replace(i, special_type[i], inplace=True)

	for i in data["model"]:
		try:
			for j in i:
				if j in model_del_string:
					i = i.replace(j,"")

			i = i.lower()
			if "huaweihuawei" in i:
				i = i.replace("huaweihuawei","huawei")
			if "xiaomixiaomi" in i:
				i = i.replace("xiaomixiaomi","xiaomi")
		except:
			pass
		finally:
			new_model.append(i)

	data["model"] = new_model
	print("model ok")


# 对osv进行初步处理
def osv(data):
	new_osv = []
	for i in data["osv"]:
		try:
			if "," in i:
				i = i.replace(",", ".")
			if " 十核2.0G_HD" in i:
				i = i.replace(" 十核2.0G_HD", "")

			process = i.split(".")
			while process[-1] == "0":
				del process[-1]
			i = ".".join(process)
		except:
			pass
		finally:
			new_osv.append(i)

	data["osv"] = new_osv
	print("osv ok")


# embedding特征构建索引
def embedding(data1, data2):
	global json_dict

	def build_index(n, data, feature):
		new_feature = []
		for i in data[feature]:
			try:
				new_feature.append(embedding_set.index(i))
			except:
				new_feature.append(len(embedding_set) + n)

		return new_feature

	embedding_index = ["pkgname", "adunitshowid", "mediashowid", "city", \
					   "adidmd5", "imeimd5","openudidmd5", "macmd5", \
					   "model", "osv"]
	embedding_set = []

	for i in embedding_index:
		embedding_set += list(set(data1[i]) & set(data2[i]))

	embedding_set = list(set(embedding_set))
	json_dict["embedding"] = embedding_set

	for n, i in enumerate(embedding_index):
		data1[i] = build_index(n, data1, i)
		data2[i] = build_index(n, data2, i)
		print("{} is ok".format(i))

	print("embedding ok")


# 将连续值特征，需要one-hot的特征，需要embedding的特征分开排放
def change_col_index(data):
	col_index = ["label", "time", "ip", "resolution_ratio", "apptype", \
				"dvctype", "ntt", "carrier", "orientation", "lan", "pkgname", \
				"adunitshowid", "mediashowid", "city", "adidmd5", \
				"imeimd5","openudidmd5", "macmd5", "model", "osv"]
	if data is data2:
		col_index[0] = "sid"

	return data[col_index]


# 数据清洗
def data_clean(data1, data2):
	apptype(data1, data2)
	carrier(data1, data2)
	lan(data1, data2)

	for i in [data1, data2]:
		del_features(i)
		nginxtime(i)
		dvctype(i)
		orientation(i)
		h_w_ppi(i)
		ip(i)
		model(i)
		osv(i)

	embedding(data1, data2)


# index_json.json中存储所有需要one-hot及embedding特征的索引，不要轻易改动
if __name__ == "__main__":
	data1_path = "data/train.csv"
	data2_path = "data/test.csv"
	data1_to_csv_path = "data/train_clean.csv"
	data2_to_csv_path = "data/test_clean.csv"
	json_path = "data/index_json.json"

	data1 = pd.read_csv(data1_path)
	data2 = pd.read_csv(data2_path)
	json_dict = {}

	data_clean(data1, data2)
	data1 = change_col_index(data1)
	data2 = change_col_index(data2)

	data1.to_csv(data1_to_csv_path, index=False)
	data2.to_csv(data2_to_csv_path, index=False)
	with open(json_path,"w") as f:
		json.dump(json_dict, f)
