from DB.mongo_init import *
from datetime import datetime

class MindfulsManager:
    def __init__(self, collection_name='mindfuls'):
        self.client = client
        self.db = heartDB
        self.collection = self.db[collection_name]

    # 创建冥想记录
    def create_mindful(self, user_id, mindful_duration, mindful_time=None, mindful_status=True):
        if mindful_time is None:
            mindful_time = datetime.now()
        mindful = {
            "user_id": user_id,
            "mindful_duration": mindful_duration,
            "mindful_time": mindful_time,
            "mindful_status": mindful_status
        }
        self.collection.insert_one(mindful)
        return mindful

    # 读取冥想记录
    def read_mindfuls(self, user_id):
        query = {"user_id": user_id}
        return list(self.collection.find(query))

    # 获取特定冥想记录
    def get_mindful(self, user_id, mindful_time):
        query = {"user_id": user_id, "mindful_time": mindful_time}
        return self.collection.find_one(query)

    # 更新冥想记录
    def update_mindful(self, user_id, mindful_time, updated_fields):
        query = {"user_id": user_id, "mindful_time": mindful_time}
        new_values = {"$set": updated_fields}
        result = self.collection.update_one(query, new_values)
        return result.modified_count

    # 删除冥想记录
    def delete_mindful(self, user_id, mindful_time):
        query = {"user_id": user_id, "mindful_time": mindful_time}
        result = self.collection.delete_one(query)
        return result.deleted_count
    
    # 获取某天的所有冥想
    def get_mindful_by_day(self, user_id, time_day):
        """返回用户 user_id 在 time_day 这天的所有冥想"""
        start_time = time_day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = time_day.replace(hour=23, minute=59, second=59, microsecond=999999)
        query = {
            "user_id": user_id,
            "mindful_time": {"$gte": start_time, "$lte": end_time}
        }
        return list(self.collection.find(query))

