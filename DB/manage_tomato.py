from DB.mongo_init import *
from datetime import datetime

class TomatoesManager:
    def __init__(self, collection_name='tomatoes'):
        self.client = client
        self.db = heartDB
        self.collection = self.db[collection_name]

    # 创建番茄钟记录
    def create_tomato(self, user_id, tomato_duration, tomato_time=None, tomato_status=True):
        if tomato_time is None:
            tomato_time = datetime.now()
        tomato = {
            "user_id": user_id,
            "tomato_duration": tomato_duration,
            "tomato_time": tomato_time,
            "tomato_status": tomato_status
        }
        self.collection.insert_one(tomato)
        return tomato

    # 读取番茄钟记录
    def read_tomatoes(self, user_id):
        query = {"user_id": user_id}
        return list(self.collection.find(query))

    # 获取特定番茄钟记录
    def get_tomato(self, user_id, tomato_time):
        query = {"user_id": user_id, "tomato_time": tomato_time}
        return self.collection.find_one(query)

    # 更新番茄钟记录
    def update_tomato(self, user_id, tomato_time, updated_fields):
        query = {"user_id": user_id, "tomato_time": tomato_time}
        new_values = {"$set": updated_fields}
        result = self.collection.update_one(query, new_values)
        return result.modified_count

    # 删除番茄钟记录
    def delete_tomato(self, user_id, tomato_time):
        query = {"user_id": user_id, "tomato_time": tomato_time}
        result = self.collection.delete_one(query)
        return result.deleted_count

    # 获取某天的所有番茄
    def get_tomato_by_day(self, user_id, time_day):
        """返回用户 user_id 在 time_day 这天的所有tomato"""
        start_time = time_day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = time_day.replace(hour=23, minute=59, second=59, microsecond=999999)
        query = {
            "user_id": user_id,
            "tomato_time": {"$gte": start_time, "$lte": end_time}
        }
        return list(self.collection.find(query))