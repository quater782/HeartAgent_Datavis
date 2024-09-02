import sys
# 将父目录添加到系统路径
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.manager.mongo_init import *
from datetime import datetime


# 创建数据库
db = client['heartDB']

# # 创建集合 仅运行一次
collections = ['users', 'diaries', 'todos', 'moods', 'chatlogs', 'mindfuls', 'tomatoes']
for collection_name in collections:
    db.create_collection(collection_name)
# 打印数据库中所有集合的名称，验证创建是否成功
print("Collections in 'heartDB' database:")
print(db.list_collection_names())

# 示例用法：向某个集合中插入一个文档
example_diary = {
    "user_id": "default",
    "diary_title": "今日总结",
    "diary_content": "今天发生了很多有趣的事情...",
    "diary_time": datetime.now(), # 2024-07-28T14:34:37.680+00:00
    "diary_agent_response": "这是AI的回应...",
    "diary_summary": "今日主要内容总结..."
}

db['diaries'].insert_one(example_diary)
print("Inserted a document into 'diaries' collection.")
