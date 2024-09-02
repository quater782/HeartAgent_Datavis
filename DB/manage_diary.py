import datetime
from DB.mongo_init import *

class DiaryManager:

    def __init__(self, collection_name='diaries'):
        self.client = client
        self.db = heartDB
        self.collection = self.db[collection_name]

    # 创建日记
    def create_diary(self, user_id, diary_title, diary_content, diary_time=None, diary_agent_response=None, diary_summary=None):
        if diary_time is None:
            diary_time = datetime.datetime.now()
        diary = {
            "user_id": user_id,
            "diary_title": diary_title,
            "diary_content": diary_content,
            "diary_time": diary_time,
            "diary_agent_response": diary_agent_response,
            "diary_summary": diary_summary
        }
        self.collection.insert_one(diary)
        return diary

    # 读取所有日记
    def read_diaries(self, user_id):
        query = {"user_id": user_id}
        return list(self.collection.find(query))

    # 获取特定日记
    def get_diary(self, user_id, diary_time):
        query = {"user_id": user_id, "diary_time": diary_time}
        return self.collection.find_one(query)

    # 更新日记
    def update_diary(self, user_id, diary_time, updated_fields):
        query = {"user_id": user_id, "diary_time": diary_time}
        new_values = {"$set": updated_fields}
        result = self.collection.update_one(query, new_values)
        return result.modified_count

    # 删除日记
    def delete_diary(self, user_id, diary_time):
        query = {"user_id": user_id, "diary_time": diary_time}
        result = self.collection.delete_one(query)
        return result.deleted_count
    
    # 获取某天的所有日记
    def get_diaries_by_day(self, user_id, time_day):
        """返回用户 user_id 在 time_day 这天的所有日记"""
        start_time = time_day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = time_day.replace(hour=23, minute=59, second=59, microsecond=999999)
        query = {
            "user_id": user_id,
            "diary_time": {"$gte": start_time, "$lte": end_time}
        }
        return list(self.collection.find(query))


