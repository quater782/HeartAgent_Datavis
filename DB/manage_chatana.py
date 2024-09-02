import sys
# 将父目录添加到系统路径
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DB.mongo_init import *
from datetime import datetime
from bson.objectid import ObjectId

class ChatAnaManager:
    def __init__(self, collection_name='chatlogsAna'):
        self.client = client
        self.db = heartDB
        self.collection = self.db[collection_name]

    def create_chatana(self, user_id, sdt_analysis, star_analysis, finish, chatlog_raw, chatlog_summary, chatlog_rating):
        chatana = {
            "user_id": user_id,
            "time": datetime.now(),
            "SDT_analysis": sdt_analysis,
            "STAR_analysis": star_analysis,
            "finish": finish,
            "chatlog_raw": chatlog_raw,
            "chatlog_summary": chatlog_summary,
            "chatlog_rating": chatlog_rating #默认是-1，-1=没评分
        }
        result = self.collection.insert_one(chatana)
        return result.inserted_id

    def read_chatana(self, user_id):
        # 返回该用户的所有ChatAna记录
        return list(self.collection.find({"user_id": user_id}))

    def update_chatana(self, chatana_id, updates):
        # 使用chatana_id来指定更新的记录
        return self.collection.update_one({"_id": ObjectId(chatana_id)}, {"$set": updates})

    def delete_chatana(self, chatana_id):
        # 使用chatana_id来指定删除的记录
        return self.collection.delete_one({"_id": ObjectId(chatana_id)})

    def read_all_chatana(self):
        return list(self.collection.find())
    
    def add_chatlog_entry(self, chatana_id, new_log_entry):
        # 使用$push操作符追加新日志条目
        return self.collection.update_one(
            {"_id": ObjectId(chatana_id)},
            {"$push": {"chatlog_raw": new_log_entry}}
        )
    
    def find_incomplete_chatana(self, user_id):
        query = {
            "user_id": user_id,
            "finish": False,
            "$expr": {"$lt": [{"$size": "$chatlog_raw"}, 29]}
        }
        return list(self.collection.find(query))
    
    def mark_as_finished(self, _id):
        result = self.collection.update_one(
            {"_id": ObjectId(_id)},
            {"$set": {"finish": True}}
        )
        return result.modified_count
    
    def get_chatana_list_by_time_range(self, start_time: datetime, end_time: datetime):
        """
        获取指定时间范围内的所有 ChatAna 记录。
        
        :param start_time: 开始时间 (datetime 对象)
        :param end_time: 结束时间 (datetime 对象)
        :return: 在指定时间范围内的 ChatAna 记录列表
        """
        query = {
            "time": {
                "$gte": start_time,
                "$lte": end_time
            }
        }
        return list(self.collection.find(query))
    
''' 数据格式可参考这个 '''
# # Example usage:
# print("1")
# manager = ChatAnaManager()
# result = manager.create_chatana(
#     user_id="123456789",
#     sdt_analysis={
#         "autonomy_status": "强",
#         "autonomy_reason": "用户表现出高度的决策自主性。",
#         "competence_status": "无",
#         "competence_reason": "用户未表现出能力或成就相关的特征。",
#         "relatedness_status": "弱",
#         "relatedness_reason": "用户在此上下文中表达的与他人的联系较弱。"
#     },
#     star_analysis={
#         "situation": "用户遇到了问题，需要干预。",
#         "situationSDT": "用户心理需求较弱。",
#         "task": "提升用户的自主感。",
#         "action": "计划与用户沟通，提高自主感。",
#         "result": "用户感受到自主感的提升。",
#         "reflection": "干预成功，用户表现积极。"
#     },
#     finish=True,
#     chatlog_raw=[
#         {"time": datetime.now(), "user": "你好", "bot": "你好，有什么我可以帮助的吗？"},
#     ],
#     chatlog_summary="用户对话情感积极，干预成功。",
#     chatlog_rating=5
# )

# # Example usage:
# # manager = ChatAnaManager()
# new_log_entry = {"time": datetime.now(), "user": "谢谢", "bot": "不客气！"}
# manager.add_chatlog_entry(result.inserted_id, new_log_entry)

# a = manager.find_incomplete_chatana("123456789")
# print(a)
# print(len(a)) # 1