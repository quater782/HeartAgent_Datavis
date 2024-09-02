import sys
# 将父目录添加到系统路径
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DB.mongo_init import *
from datetime import datetime
from bson.objectid import ObjectId

class ProactiveMessageManager:
    def __init__(self, collection_name='autoMessage'):
        self.client = client
        self.db = heartDB
        self.collection = self.db[collection_name]

    def create_message(self, user_id: str, send_time: datetime, content: str, send_day: datetime):
        """创建一个新的主动发送消息的记录"""
        # 将 send_day 仅保留年月日部分
        send_day = send_day.replace(hour=0, minute=0, second=0, microsecond=0)
        
        message = {
            "user_id": user_id,
            "send_time": send_time,
            "content": content,
            "send_day": send_day
        }
        return self.collection.insert_one(message).inserted_id

    def get_message(self, message_id: str):
        """根据ID获取消息记录"""
        return self.collection.find_one({"_id": ObjectId(message_id)})

    def update_message(self, message_id: str, updated_fields: dict):
        """更新消息记录，支持部分字段更新"""
        if "send_day" in updated_fields:
            updated_fields["send_day"] = updated_fields["send_day"].replace(hour=0, minute=0, second=0, microsecond=0)
        
        query = {"_id": ObjectId(message_id)}
        update = {"$set": updated_fields}
        return self.collection.update_one(query, update).modified_count

    def delete_message(self, message_id: str):
        """删除指定ID的消息记录"""
        return self.collection.delete_one({"_id": ObjectId(message_id)}).deleted_count

    def find_messages_by_user(self, user_id: str):
        """根据用户ID查找所有消息记录"""
        return list(self.collection.find({"user_id": user_id}))

    def find_messages_by_date(self, send_day: datetime):
        """根据发送日期查找所有消息记录，仅匹配年月日"""
        send_day = send_day.replace(hour=0, minute=0, second=0, microsecond=0)
        return list(self.collection.find({"send_day": send_day}))

    def list_all_messages(self):
        """列出所有消息记录"""
        return list(self.collection.find())
    
    def mark_message_as_sent(self, message_id: str):
        """标记消息为已发送"""
        query = {"_id": ObjectId(message_id)}
        update = {"$set": {"sent": True}}
        return self.collection.update_one(query, update).modified_count

# # 示例使用

# manager = ProactiveMessageManager()

# # 创建消息
# message_id = manager.create_message(
#     user_id="cyx1555",
#     send_time=datetime(2024, 8, 20, 14, 30, 0),
#     content="Hello, this is a scheduled message!",
#     send_day=datetime(2024, 8, 20)
# )
# print(f"Message created with ID: {message_id}")


# # 创建消息
# message_id = manager.create_message(
#     user_id="cyx1555",
#     send_time=datetime(2024, 8, 16, 16, 0, 0),
#     content="Hello, this is a scheduled message!",
#     send_day=datetime(2024, 8, 16)
# )
# print(f"Message created with ID: {message_id}")

# # 创建消息
# message_id = manager.create_message(
#     user_id="cyx1555",
#     send_time=datetime(2024, 8, 16, 16, 5, 0),
#     content="Hello, this is a scheduled message!",
#     send_day=datetime(2024, 8, 16)
# )
# print(f"Message created with ID: {message_id}")

# # 创建消息
# message_id = manager.create_message(
#     user_id="cyx1555",
#     send_time=datetime(2024, 8, 16, 16, 6, 0),
#     content="Hello, this is a scheduled message!",
#     send_day=datetime(2024, 8, 16)
# )
# print(f"Message created with ID: {message_id}")
# # 创建消息
# message_id = manager.create_message(
#     user_id="cyx1555",
#     send_time=datetime(2024, 8, 16, 16, 3, 0),
#     content="Hello, this is a scheduled message!",
#     send_day=datetime(2024, 8, 16)
# )
# print(f"Message created with ID: {message_id}")

# # 创建消息
# message_id = manager.create_message(
#     user_id="cyx1555",
#     send_time=datetime(2024, 8, 16, 16, 2, 0),
#     content="Hello, this is a scheduled message!",
#     send_day=datetime(2024, 8, 16)
# )
# print(f"Message created with ID: {message_id}")

# # 获取消息
# message = manager.get_message(message_id)
# print(f"Retrieved Message: {message}")

# # 更新消息
# update_count = manager.update_message(message_id, {"content": "Updated message content"})
# print(f"Number of documents updated: {update_count}")

# # 查找特定用户的消息
# user_messages = manager.find_messages_by_user("cyx1555")
# print(f"Messages for cyx1555: {user_messages}")

# # 根据日期查找消息
# day_messages = manager.find_messages_by_date(datetime(2024, 8, 20))
# print(f"Messages for 2024-08-20: {day_messages}")

# # 删除消息
# delete_count = manager.delete_message(message_id)
# print(f"Number of documents deleted: {delete_count}")