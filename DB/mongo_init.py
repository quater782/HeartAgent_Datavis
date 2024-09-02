
from pymongo import MongoClient
import datetime


# 男主名字和数据库名称的对应，为了浓缩下面的代码
db_name_to_db = {
    # 光夜
    '00': '00DB',
    '11': '11DB',
    '55': '55DB',
    '66': '66DB',
    '77': '77DB',
    # 深空
    'ls': 'LS_DB',
    'qy': 'QY_DB',
    'sxh': 'SXH_DB',
    'xyz':'XYZ_DB',
    'qc': 'QC_DB',
    # heart APP 
    'cyxTest': 'TestDB',
    'heartDBTest': 'heartDB',
    'cyxheartDBEval': 'heartDBEval', # cyx 本地实验地址
    'heartDB':'heartDB', 
    'hqTest':'heartDB' # 本地数据库名称
}

bot_paths = {
    '11': 'C:\\gaungye_bot\\ChatailoverBot11',
    '66': 'C:\\gaungye_bot\\ChatailoverBot66',
    # '陆沉': 'C:\\gaungye_bot\\ChatailoverBot66',
    '77': 'C:\\gaungye_bot\\ChatailoverBot77',
    '55': 'C:\\gaungye_bot\\ChatailoverBot55',
    '00': 'C:\\gaungye_bot\\ChatailoverBot00',
    'ls': 'C:\\0-shenkong_bot\\ls',
    'qy': 'C:\\0-shenkong_bot\\qy',
    'sxh': 'C:\\0-shenkong_bot\\sxh',
    'xyz': 'C:\\0-shenkong_bot\\xyz',
    'qc': 'C:\\0-shenkong_bot\\qc',
    'cyxTest': 'D:\\AILover\\code\\loveBot1.2', # cyx bot本地测试路径
    'heartDBTest':'D:\\MyCode\\chi2024\\heartDB', # cyx app本地测试路径
    'cyxheartDBEval':'D:\\MyCode\\chi2024\\HeartAgent_Datavis', # cyx 实验地址
    'hqTest': '/Users/yuwen/Desktop/HeartAgentDB/heartAgentDB/', # hq app本地测试路径
    'heartDB':'E:\\heartAgentDB'  # 服务器app路径
}


# 向xxDB的Limit表里插入新数据：按需自定义待插入的数据库
def newInfo(client, user_qq, db_name, info_data):
    
    # 连接男主数据库
    database = client[db_name_to_db[db_name]]
    info_collection = database['user_info']


    # 设置user_info表插入值
    if info_data == None:
        info_data = {
            "id": user_qq,    #用户
            "name": "你的女朋友",   #默认姓名
            "info": "一名女性", #默认设定
            "city": None,   #默认城市无
            "city_code": 0,  #默认城市id无
            "age": 18,  #默认18sui
            "auto_message_on": 1,   #默认开启主动发消息
            "custom_identity_on": 1,    #默认开启自定义身份
            "custom_action_on": 1,  #默认开启动描
            "voice_on": 1,  #后面的还没做
            "sing_on": 1,
            "meme_on": 1,
            "img_rec_on": 1,
            "custom_sched_on": 1,
            "menstrual_on": 1,
            "custom_sleep_on": 1,
            "auto_weather_on": 1,
            "group_on": 1,
            "game_on": 1,
            "version": "buy1",   #默认付费版1
            "nanzhu": "66", # 0811新增 默认66
            "intervene": "" # 0814 新增 默认啥也没有，不干预
        }
    else:
        info_data = info_data

    info_collection.insert_one(info_data)
    
    print("new data inserted in userLimit.")  # 新数据插入成功

    return info_data


# 向xxDB的Limit表里插入新数据：按需自定义待插入的数据库
def newLimit(client, user_qq= "ceshi", type = "\u597d\u53cb", db_name = '11', limit_data = None):
    '''
    db_name: default=='00'。可选值见db_name_to_db定义。
    limit_data: 需要被插入的新数据，none则插入测试数据。
    '''
    # 连接男主数据库
    database = client[db_name_to_db[db_name]]
    limit_collection = database['user_limit']


    # 设置user_limit表插入值
    if limit_data == None:
        limit_data = {
            "id": user_qq,
            "type": type,
            # 科研原因，默认8000条
            "rate": 8000,
            "date": str(datetime.date.today()),
            "days": 31,
            "count": 0,
            "free_rate": 400, # 0629 新添加的，代表免费版用户拥有的额度
            "free_count":0, # 0629 新添加的，代表免费版用户已经使用的额度
            "wd_key": 'wd_key', # 0629 新添加的，代表用户最近一次购买信息验证的券码
            "auto_message": 0,
            "custom_identity":1,
            "custom_action":0,
            "voice":0,
            "sing":0,
            "meme":0,
            "img_rec":0,
            "custom_sched":0,
            "menstrual":1,
            "custom_sleep":0,
            "auto_weather":0,
            "group":0,
            "game":1,
            "custom":0 # 0628 新添加的，代表用户是否是定制版用户/是否购买了定制版
        }
    else:
        limit_data = limit_data

    limit_collection.insert_one(limit_data)
    
    print("new data inserted in userLimit.")  # 新数据插入成功

    return limit_data


# 这个男主是根据bot代码运行路径来判断是在服务器上还是在测试
def connect_to_mongo(nanzhu):
    # 连接到MongoDB

    username = "rootUser"
    password = "ChatAILover"
    auth_db = "admin"

    # TODO 测试路径，开发者请将本地测试路径名称在这里配置好
    if nanzhu in ['cyxTest', 'heartDBTest', 'hqTest', 'cyxheartDBEval']:
        # print('yes')
        client = MongoClient('mongodb://localhost:27017/')
    # 要是有其他姐妹的测试路径也可以写在这里
    # 服务器上男主的情况
    else:
        # client = MongoClient(f"mongodb://{username}:{password}@localhost:27017/{auth_db}")
        client = MongoClient(f"mongodb://{username}:{password}@localhost:27017/")
    return client

# 根据程序路径判断男主、数据库
current_file_path = __file__

for key in bot_paths:
    value = bot_paths.get(key)
    if value in current_file_path:
        nanzhu = key
        break
if nanzhu == None:
    raise Exception(f'info manage 中 self.nanzhu参数错误, 请检查mongo_init.py 中男主路径是否和目前代码运行的路径不相符')

client = connect_to_mongo(nanzhu)
print('当前男主：', nanzhu)
# 数据库
heartDB = client['heartDBEval']