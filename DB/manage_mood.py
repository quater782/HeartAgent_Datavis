from datetime import datetime
from DB.mongo_init import *

class MoodManager:
    def __init__(self, collection_name='moods'):
        self.client = client
        self.db = heartDB
        self.collection = self.db[collection_name]

    # 创建心情记录
    # p.s. 这里没有做可选项的约束，感觉可以做到前端
    def create_mood(self, user_id, mood_indicator=1.0, mood_keywords=None, mood_factors=None, mood_time_logged=None):
        if mood_keywords is None:
            mood_keywords = []
        if mood_factors is None:
            mood_factors = []
        if mood_time_logged is None:
            mood_time_logged = datetime.now()
        mood = {
            "user_id": user_id,
            "mood_indicator": mood_indicator,
            "mood_keywords": mood_keywords,
            "mood_factors": mood_factors,
            "mood_time_logged": mood_time_logged
        }
        self.collection.insert_one(mood)
        return mood

    # 读取心情记录
    def read_moods(self, user_id):
        query = {"user_id": user_id}
        return list(self.collection.find(query))

    # 获取特定心情记录
    def get_mood(self, user_id, mood_time_logged):
        query = {"user_id": user_id, "mood_time_logged": mood_time_logged}
        return self.collection.find_one(query)

    # 更新心情记录
    def update_mood(self, user_id, mood_time_logged, updated_fields):
        query = {"user_id": user_id, "mood_time_logged": mood_time_logged}
        new_values = {"$set": updated_fields}
        result = self.collection.update_one(query, new_values)
        return result.modified_count

    # 删除心情记录
    def delete_mood(self, user_id, mood_time_logged):
        query = {"user_id": user_id, "mood_time_logged": mood_time_logged}
        result = self.collection.delete_one(query)
        return result.deleted_count

    # 获取某天的所有心情
    def get_moods_by_day(self, user_id, time_day):
        """返回用户 user_id 在 time_day 这天的所有心情"""
        start_time = time_day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = time_day.replace(hour=23, minute=59, second=59, microsecond=999999)
        query = {
            "user_id": user_id,
            "mood_time_logged": {"$gte": start_time, "$lte": end_time}
        }
        return list(self.collection.find(query))
