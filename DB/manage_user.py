
from DB.mongo_init import *

class UserInfoManager:
    def __init__(self,collection_name='users'):
        self.client = client
        self.db = heartDB
        self.collection = self.db[collection_name]

    # 创建用户信息
    def create_user_info(self, user_id, name=None, info=None, city=None, age=18):
        user_info = {
            "user_id": user_id,
            "name": name,
            "info": info,
            "city": city,
            "age": age
        }
        self.collection.insert_one(user_info)
        return user_info

    # 读取用户信息
    def read_user_info(self, user_id):
        query = {"user_id": user_id}
        return self.collection.find_one(query)

    # 获取所有用户信息
    def read_all_users(self):
        return list(self.collection.find({}))

    # 更新用户信息
    def update_user_info(self, user_id, updated_fields):
        query = {"user_id": user_id}
        new_values = {"$set": updated_fields}
        result = self.collection.update_one(query, new_values)
        return result.modified_count

    # 删除用户信息
    def delete_user_info(self, user_id):
        query = {"user_id": user_id}
        result = self.collection.delete_one(query)
        return result.deleted_count


