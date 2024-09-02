from datetime import datetime
from DB.mongo_init import *

class TodoManager:
    def __init__(self, collection_name='todos'):
        self.client = client
        self.db = heartDB
        self.collection = self.db[collection_name]

    # 创建日程
    def create_todo(self, user_id, todo_item_content, 
                    todo_item_urgency=0, todo_item_time_start=None, 
                    todo_item_time_end=None, todo_item_time_repeat=0, todo_item_status_finish=False, 
                    todo_item_notification_type=2):
        if todo_item_time_start is None:
            todo_item_time_start = datetime.now()
        if todo_item_time_end is None:
            todo_item_time_end = datetime.now()
        todo = {
            "user_id": user_id,
            "todo_item_content": todo_item_content,
            "todo_item_urgency": todo_item_urgency,
            "todo_item_time_start": todo_item_time_start,
            "todo_item_time_end": todo_item_time_end,
            "todo_item_time_repeat": todo_item_time_repeat,
            "todo_item_status_finish": todo_item_status_finish,
            "todo_item_notification_type": todo_item_notification_type
        }
        self.collection.insert_one(todo)
        return todo

    # 读取用户所有日程
    def read_todos(self, user_id):
        query = {"user_id": user_id}
        return list(self.collection.find(query))

    # 获取特定日程
    # TODO 这里的查询条件可能需要根据实际情况修改
    def get_todo(self, user_id, todo_item_time_start):
        query = {"user_id": user_id, "todo_item_time_start": todo_item_time_start}
        return self.collection.find_one(query)

    # 更新日程
    def update_todo(self, user_id, todo_item_time_start, updated_fields):
        query = {"user_id": user_id, "todo_item_time_start": todo_item_time_start}
        new_values = {"$set": updated_fields}
        result = self.collection.update_one(query, new_values)
        # 根本没有这个value
        print (result)
        return result.modified_count
    
    # 更新日程
    def update_todo_con(self, user_id, content, updated_fields):
        query = {"user_id": user_id, "todo_item_content": content}
        new_values = {"$set": updated_fields}
        result = self.collection.update_one(query, new_values)
        print (result)
        # print (result.dict())
        return result.modified_count

    # 删除日程
    def delete_todo(self, user_id, todo_item_time_start):
        query = {"user_id": user_id, "todo_item_time_start": todo_item_time_start}
        result = self.collection.delete_one(query)
        return result.deleted_count

