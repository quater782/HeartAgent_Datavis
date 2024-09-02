from manage_diary import *
from manage_todo import *
from manage_mood import *
from manage_chat import *
from manage_mindfuls import *
from manage_tomato import *
from manage_user import *
from datetime import datetime


''' 日记后端测试 ok'''

# manager = DiaryManager()

# # 创建日记
# manager.create_diary("default", "1今日总结", "今天发生了很多有趣的事情...")

# # 读取所有日记
# print(manager.read_diaries("default"))

# # 获取特定日记
# manager.create_diary("default", "另一篇日记", "这是另一篇日记...")
# print(manager.get_diary("default", datetime.now()))

# # 更新日记
# manager.update_diary("default", datetime.now(), {"diary_content": "更新后的日记内容..."})
# print(manager.get_diary("default", datetime.now()))

# # 删除日记
# manager.delete_diary("default", diary_time)


''' todo 测试 ok'''
# manager = TodoManager()

# # # 创建日程
# # manager.create_todo("default", "完成项目报告", todo_item_urgency=2, todo_item_date_start=datetime(2024, 7, 28, 9, 0), todo_item_date_end=datetime(2024, 7, 28, 17, 0))

# # # 读取所有日程
# # print(manager.read_todos("default"))

# # # 获取特定日程
# # specific_start_time = datetime(2024, 7, 28, 9, 0)
# # print(manager.get_todo("default", specific_start_time))

# # # 更新日程
# # manager.update_todo("default", specific_start_time, {"todo_item_content": "更新后的项目报告内容"})

# # 删除日程
# manager.delete_todo("default", datetime(2024, 7, 28, 9, 0))


''' 心情测试 ok '''

# manager = MoodManager()

# # # 创建心情记录
# # manager.create_mood("default", mood_indicator=0.8, mood_keywords=["开心", "兴奋"], mood_factors=["工作", "健康"])

# # # 读取所有心情记录
# # print(manager.read_moods("default"))

# # # 获取特定心情记录
# # specific_time = datetime(2024, 7, 28, 9, 0)
# # manager.create_mood("default", mood_indicator=0.5, mood_keywords=["难过"], mood_factors=["家庭"], mood_time_logged=specific_time)
# # print(manager.get_mood("default", specific_time))

# # # 更新心情记录
# # manager.update_mood("default", specific_time, {"mood_indicator": 0.9, "mood_keywords": ["开心", "满足"]})

# # 删除心情记录
# manager.delete_mood("default", datetime(2024, 7, 28, 9, 0))


''' 对话测试 ok'''

# manager = ChatManager()

# # 创建对话记录
# manager.create_chatlog(
#     user_id="default",
#     chatlog_raw=[{"time": datetime(2024, 7, 28, 9, 0), "user": "你好", "bot": "你好，有什么我能帮忙的吗？"}],
#     chatlog_tags=["动机", "心理韧性"],
#     chatlog_tags_state=[1, -1],
#     chatlog_star_s="用户感到压力",
#     chatlog_star_t="帮助用户放松",
#     chatlog_star_a="提供深呼吸练习指导",
#     chatlog_star_r="用户感到放松",
#     chatlog_summary="通过提供深呼吸练习帮助用户放松",
#     chatlog_rating=5
# )

# # 读取所有对话记录
# print(manager.read_chatlogs("default"))

# # 获取特定对话记录
# specific_time = datetime(2024, 7, 28, 16, 0)
# manager.create_chatlog(
#     user_id="default",
#     chatlog_raw=[{"time": specific_time, "user": "你好", "bot": "你好，有什么我能帮忙的吗？"}],
#     chatlog_time=specific_time
# )
# print(manager.get_chatlog("default", specific_time))

# # 更新对话记录
# manager.update_chatlog("default", specific_time, {"chatlog_summary": "更新后的总结"})
# # 更新对话记录
# manager.update_chatlog("default", (2024, 7, 28, 9, 0), {"chatlog_summary": "更新后的总结——好"})

# # 删除对话记录
# manager.delete_chatlog("default", specific_time)


'''冥想测试 ok '''

# manager = MindfulsManager()

# # # 创建冥想记录
# # manager.create_mindful(
# #     user_id="default",
# #     mindful_duration=30
# # )

# # # 读取所有冥想记录
# # print(manager.read_mindfuls("default"))

# # # 获取特定冥想记录
# specific_time = datetime(2024, 7, 28, 9, 0)
# # manager.create_mindful(
# #     user_id="default",
# #     mindful_duration=20,
# #     mindful_time=specific_time
# # )
# # print(manager.get_mindful("default", specific_time))

# # # 更新冥想记录
# # manager.update_mindful("default", specific_time, {"mindful_status": False})

# # 删除冥想记录
# manager.delete_mindful("default", specific_time)

'''番茄测试 ok'''

# manager = TomatoesManager()

# # 创建番茄钟记录
# manager.create_tomato(
#     user_id="default",
#     tomato_duration=25
# )

# # 读取所有番茄钟记录
# print(manager.read_tomatoes("default"))

# # 获取特定番茄钟记录
# specific_time = datetime(2024, 7, 28, 9, 0)
# manager.create_tomato(
#     user_id="default",
#     tomato_duration=25,
#     tomato_time=specific_time
# )
# print(manager.get_tomato("default", specific_time))

# # 更新番茄钟记录
# manager.update_tomato("default", specific_time, {"tomato_status": False})

# # # 删除番茄钟记录
# # manager.delete_tomato("default", specific_time)

'''用户个人信息测试 ok'''

# manager = UserInfoManager()

# # 创建用户信息
# manager.create_user_info(
#     user_id="1234567890",
#     name="John Doe",
#     info="Student",
#     city="New York",
#     age=25
# )

# # 读取用户信息
# print(manager.read_user_info("1234567890"))

# # 更新用户信息
# manager.update_user_info("1234567890", {"city": "Los Angeles", "age": 26})

# # # 删除用户信息
# # manager.delete_user_info("1234567890")

# # 读取所有用户信息
# print(manager.read_all_users())