import sys
# 将父目录添加到系统路径
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from DB.mongo_init import *
from datetime import datetime, date, time

# 数据格式参考
# {
#     "_id": ObjectId,
#     "user_id": "string",   // 用户标识
#     "date": Date,          // 日期（不包含时间，表示某一天）
#     "chatlog_raw": [
#         {
#             "time": DateTime, // 完整的时间戳
#             "user": "string", // 用户发送的消息
#             "bot": "string"   // 机器人回复的消息
#         },
#         // ... 其他聊天记录
#     ]
# }



class ChatLogManager:
    def __init__(self, collection_name='chatlogs'):
        self.client = client
        self.db = heartDB
        self.collection = self.db[collection_name]

    def _get_date_only(self, dt):
        """
        将输入的日期或时间标准化为仅包含日期部分，时间设为 00:00:00
        """
        if isinstance(dt, datetime):
            return datetime.combine(dt.date(), time.min)
        elif isinstance(dt, date):
            return datetime.combine(dt, time.min)
        elif isinstance(dt, str):
            # 假设输入字符串格式为 'YYYY-MM-DD'
            return datetime.combine(datetime.strptime(dt, '%Y-%m-%d').date(), time.min)
        else:
            raise ValueError('Invalid date format')

    def add_chatlog_entry(self, user_id, log_datetime, user_message, bot_message):
        """
        向指定用户和日期的文档中添加新的聊天记录。
        如果文档不存在，则创建新文档。一个用户的一天内的聊天都会存在一个document中
        
        参数：
            user_id (str): 用户标识
            log_datetime (datetime): 聊天消息的时间戳
            user_message (str): 用户发送的消息
            bot_message (str): 机器人回复的消息
        """
        # 标准化日期
        log_date = self._get_date_only(log_datetime)
        
        # 新的聊天记录
        new_log_entry = {
            "time": log_datetime,
            "user": user_message,
            "bot": bot_message
        }
        
        # 使用 upsert，如果文档存在则追加记录，否则创建新文档
        result = self.collection.update_one(
            {"user_id": user_id, "date": log_date},
            {"$push": {"chatlog_raw": new_log_entry}},
            upsert=True
        )
        return result

    def get_chatlogs(self, user_id, log_date):
        """
        获取指定用户在特定日期的所有聊天记录。
        
        参数：
            user_id (str): 用户标识
            log_date (date/datetime/str): 需要获取聊天记录的日期
        
        返回：
            dict: 包含聊天记录的文档，如果不存在则返回 None
        """
        # 标准化日期
        log_date = self._get_date_only(log_date)
        
        document = self.collection.find_one({"user_id": user_id, "date": log_date})
        return document

    def delete_chatlogs(self, user_id, log_date):
        """
        删除指定用户在特定日期的聊天记录文档。
        
        参数：
            user_id (str): 用户标识
            log_date (date/datetime/str): 需要删除聊天记录的日期
        
        返回：
            DeleteResult: 删除操作的结果
        """
        # 标准化日期
        log_date = self._get_date_only(log_date)
        
        result = self.collection.delete_one({"user_id": user_id, "date": log_date})
        return result
    
    # 不建议使用
    def update_chatlog_entry(self, user_id, log_date, entry_time, updated_entry):
        """
        更新特定聊天记录项（通过时间戳定位，但是尽量不要使用，不建议修改聊天）。
        
        参数：
            user_id (str): 用户标识
            log_date (date/datetime/str): 聊天记录的日期
            entry_time (datetime): 需要更新的聊天记录的时间戳
            updated_entry (dict): 更新后的聊天记录，例如：{"user": "...", "bot": "..."}
        
        返回：
            UpdateResult: 更新操作的结果
        """
        # 标准化日期
        log_date = self._get_date_only(log_date)
        
        # 构建查询条件，定位具体的聊天记录项
        query = {
            "user_id": user_id,
            "date": log_date,
            "chatlog_raw.time": entry_time
        }
        
        # 构建更新内容
        update_fields = {}
        for key in ['user', 'bot']:
            if key in updated_entry:
                update_fields[f'chatlog_raw.$.{key}'] = updated_entry[key]
        
        if not update_fields:
            raise ValueError("No valid fields to update.")
        
        result = self.collection.update_one(query, {"$set": update_fields})
        return result
    
    # 不建议使用
    def delete_chatlog_entry(self, user_id, log_date, entry_time):
        """
        删除特定的聊天记录项（通过时间戳定位，不建议使用，不建议修改聊天）。
        
        参数：
            user_id (str): 用户标识
            log_date (date/datetime/str): 聊天记录的日期
            entry_time (datetime): 需要删除的聊天记录的时间戳
        
        返回：
            UpdateResult: 删除操作的结果
        """
        # 标准化日期
        log_date = self._get_date_only(log_date)
        
        # 使用 $pull 操作符删除特定的聊天记录项
        result = self.collection.update_one(
            {"user_id": user_id, "date": log_date},
            {"$pull": {"chatlog_raw": {"time": entry_time}}}
        )
        return result
    
    def find_chatlogs_in_range(self, user_id, start_time, end_time):
        """
        查找指定用户在特定时间范围内的聊天记录。

        参数：
            user_id (str): 用户标识
            start_time (datetime): 开始时间
            end_time (datetime): 结束时间

        返回：
            list: 聊天记录的列表，按时间排序
        """
        query = {
            "user_id": user_id,
            "chatlog_raw.time": {
                "$gte": start_time,
                "$lte": end_time
            }
        }
        
        # 查找符合条件的文档
        documents = self.collection.find(query, {"chatlog_raw": 1}).sort("chatlog_raw.time", 1)
        
        # 提取并过滤聊天记录
        chatlogs = []
        for document in documents:
            # 过滤符合时间范围的聊天记录
            filtered_logs = [
                log for log in document.get("chatlog_raw", [])
                if start_time <= log["time"] <= end_time
            ]
            chatlogs.extend(filtered_logs)
        
        # 按时间排序
        chatlogs.sort(key=lambda log: log["time"])
        
        return chatlogs


# # 初始化管理类
# manager = ChatLogManager()

# # 示例用户和时间
# user_id = 'user123'
# chat_datetime = datetime(2023, 5, 7, 15, 30)  # 2023年5月7日 15:30

# # 添加一条聊天记录
# manager.add_chatlog_entry(
#     user_id=user_id,
#     log_datetime=chat_datetime,
#     user_message='你好',
#     bot_message='你好！有什么我可以帮助您的吗？'
# )

# # 获取用户在2023年5月7日的聊天记录
# chatlogs = manager.get_chatlogs(user_id, '2023-05-07')
# print("聊天记录：", chatlogs)

# # 更新特定的聊天记录项
# manager.add_chatlog_entry(
#     user_id=user_id,
#     log_datetime=chat_datetime,
#     user_message='你好',
#     bot_message='你好！有什么我可以帮助您的吗？'
# )

# class TestChatLogManager(unittest.TestCase):
    
#     @classmethod
#     def setUpClass(cls):
#         # 连接到 MongoDB，并创建测试数据库和集合
#         cls.client = client
#         cls.db = heartDB
#         cls.collection = 'test_chatlogs'
#         cls.manager = ChatLogManager(collection_name=cls.collection_name)
        
#         # 插入一些测试数据
#         cls.manager.collection.insert_many([
#             {
#                 "user_id": "user1",
#                 "date": datetime(2024, 8, 16),
#                 "chatlog_raw": [
#                     {"time": datetime(2024, 8, 16, 10, 0), "user": "Hi", "bot": "Hello"},
#                     {"time": datetime(2024, 8, 16, 11, 0), "user": "How are you?", "bot": "I'm good"}
#                 ]
#             },
#             {
#                 "user_id": "user1",
#                 "date": datetime(2024, 8, 17),
#                 "chatlog_raw": [
#                     {"time": datetime(2024, 8, 17, 9, 0), "user": "Good morning", "bot": "Good morning!"},
#                     {"time": datetime(2024, 8, 17, 10, 0), "user": "What's up?", "bot": "Not much"}
#                 ]
#             }
#         ])

#     @classmethod
#     def tearDownClass(cls):
#         # 清理测试数据库
#         cls.manager.collection.drop()
#         cls.client.close()

#     def test_find_chatlogs_in_range(self):
#         start_time = datetime(2024, 8, 16, 9, 0)
#         end_time = datetime(2024, 8, 16, 12, 0)
        
#         expected_result = [
#             {"time": datetime(2024, 8, 16, 10, 0), "user": "Hi", "bot": "Hello"},
#             {"time": datetime(2024, 8, 16, 11, 0), "user": "How are you?", "bot": "I'm good"}
#         ]
        
#         result = self.manager.find_chatlogs_in_range("user1", start_time, end_time)
#         self.assertEqual(result, expected_result)

# if __name__ == '__main__':
#     unittest.main()