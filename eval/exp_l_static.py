'''
大实验的描述性数据分析

'''
import sys
# 将父目录添加到系统路径
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# 定义用户数据
phone_numbers = [
    "13050920803",
    "13370792083",
    "13523426691",
    "13662064265",
    "13764851394",
    "13896520229",
    "13916874074",
    "15073142501",
    "15111816459",
    "15178181483",
    "15956956373",
    "17857310325",
    "17859910206",
    "18038829820",
    "18049067425",
    "18120040923",
    "18150061030",
    "18159658021",
    "18208660066",
    "18268155717",
    "18368437211",
    "18372772013",
    "18586127686",
    "18743527817",
    "18931628795",
    "18963809846",
    "19119732512",
    "19527398569",
    "19707045120"
]

# 输出列表
print("# 用户基本信息")
print("有效被试用户手机号：", phone_numbers)
print(f"有效被试用户数量：{len(phone_numbers)} 人" )




from collections import defaultdict
import re
import datetime
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from pymongo import MongoClient

from DB.manage_chat import ChatLogManager
from DB.manage_chatana import ChatAnaManager
from DB.manage_diary import DiaryManager
from DB.manage_todo import TodoManager
from DB.manage_mindfuls import MindfulsManager
from DB.manage_tomato import TomatoesManager
from DB.manage_mood import MoodManager

import colorsys

def hsl_to_rgb(h, s, l):
    """
    将 HSL 颜色值转换为 RGB。
    
    参数：
        h (float): Hue 色调，范围 [0, 360]
        s (float): Saturation 饱和度，范围 [0, 1]
        l (float): Lightness 亮度，范围 [0, 1]
    
    返回：
        tuple: RGB 值，范围 [0, 1]
    """
    h = h / 360  # 将 hue 从 [0, 360] 映射到 [0, 1]
    s = s / 100  # 饱和度百分比转换为小数
    l = l / 100  # 亮度百分比转换为小数
    return colorsys.hls_to_rgb(h, l, s)

class ChatLogManagerWithStats(ChatLogManager):
    
    def get_all_users_chat_stats(self, phone_numbers):
        """
        获取指定用户列表的聊天统计信息。
        
        参数：
            phone_numbers (list): 需要统计的用户ID列表
        
        返回：
            dict: 包含所有用户的整体和个体统计数据
        """
        stats = {
            'total_conversations': 0,
            'total_message_count': 0,
            'total_user_message_count': 0,
            'total_bot_message_count': 0,
            'total_conversation_lengths': [],
            'system_message_count': 0,
            'user_stats': defaultdict(lambda: {
                'conversation_count': 0,
                'total_message_count': 0,
                'total_user_message_count': 0,
                'total_bot_message_count': 0,
                'conversation_lengths': [],
                'system_message_count': 0
            })
        }

        # 遍历所有用户
        for user_id in phone_numbers:
            user_documents = self.collection.find({"user_id": user_id})

            for doc in user_documents:
                chatlog = doc.get("chatlog_raw", [])
                conversation_length = len(chatlog)

                if conversation_length == 0:
                    continue
                
                # 更新整体统计数据
                stats['total_conversations'] += 1
                stats['total_message_count'] += conversation_length
                
                user_message_count = sum(1 for log in chatlog if log.get('user'))
                bot_message_count = sum(1 for log in chatlog if log.get('bot'))
                system_message_count = sum(1 for log in chatlog if re.search(r'系统消息', log.get('bot', '')))

                stats['total_user_message_count'] += user_message_count
                stats['total_bot_message_count'] += bot_message_count
                stats['system_message_count'] += system_message_count
                stats['total_conversation_lengths'].append(conversation_length)

                # 更新用户个人统计数据
                stats['user_stats'][user_id]['conversation_count'] += 1
                stats['user_stats'][user_id]['total_message_count'] += conversation_length
                stats['user_stats'][user_id]['total_user_message_count'] += user_message_count
                stats['user_stats'][user_id]['total_bot_message_count'] += bot_message_count
                stats['user_stats'][user_id]['system_message_count'] += system_message_count
                stats['user_stats'][user_id]['conversation_lengths'].append(conversation_length)
        
        return stats

    def print_stats_summary(self, stats):
        """
        打印统计数据的总结。
        
        参数：
            stats (dict): 从 get_all_users_chat_stats 返回的统计结果
        """
        print("总对话天数:", stats['total_conversations'])
        print("总消息轮数:", stats['total_message_count'])
        print("用户消息数量:", stats['total_user_message_count'])
        print("机器人消息数量:", stats['total_bot_message_count'])
        print("系统消息数量:", stats['system_message_count'], "请注意系统消息不在log中")
        if stats['total_conversation_lengths']:
            avg_length = sum(stats['total_conversation_lengths']) / len(stats['total_conversation_lengths'])
            print("平均对话长度:", avg_length)

        print("\n每个用户的统计数据:")
        for user_id, user_stat in stats['user_stats'].items():
            print(f"用户 {user_id}:")
            print("  对话天数:", user_stat['conversation_count'])
            print("  总消息轮数:", user_stat['total_message_count'])
            print("  用户消息数量:", user_stat['total_user_message_count'])
            print("  机器人消息数量:", user_stat['total_bot_message_count'])
            print("  系统消息数量:", user_stat['system_message_count'])
            if user_stat['conversation_lengths']:
                avg_user_length = sum(user_stat['conversation_lengths']) / len(user_stat['conversation_lengths'])
                print("  平均对话长度:", avg_user_length)

class ChatAnaManagerWithStats(ChatAnaManager):
    
    def get_sdt_analysis_stats(self, phone_numbers):
        """
        获取SDT_analysis中三种状态为'弱'的出现频次，以及总体和每个用户的finish状态和chatlog_rating的统计。
        
        参数：
            phone_numbers (list): 需要统计的用户ID列表
        
        返回：
            dict: 包含SDT_analysis状态、chatlog_rating、finish状态的统计信息
        """
        stats = {
            'total_autonomy_weak': 0,
            'total_competence_weak': 0,
            'total_relatedness_weak': 0,
            'total_chatlog_rating_count': 0,
            'total_chatlog_rating_sum': 0,
            'total_finish_count': 0,
            'total_records': 0,
            'total_records_ana':0,
            'user_stats': defaultdict(lambda: {
                'autonomy_weak': 0,
                'competence_weak': 0,
                'relatedness_weak': 0,
                'chatlog_rating_count': 0,
                'chatlog_rating_sum': 0,
                'finish_count': 0,
                'record_count_ana': 0,
                'record_count': 0
            })
        }

        # 遍历所有用户
        for user_id in phone_numbers:
            user_documents = self.collection.find({"user_id": user_id})

            for doc in user_documents:
                stats['total_records'] += 1
                stats['user_stats'][user_id]['record_count'] += 1

                # 仅当 SDT_analysis 是字典类型时才进行统计
                sdt_analysis = doc.get("SDT_analysis")
                if isinstance(sdt_analysis, dict):
                    stats['total_records_ana'] += 1
                    stats['user_stats'][user_id]['record_count_ana'] += 1
                    if sdt_analysis.get("autonomy_status") == "弱":
                        stats['total_autonomy_weak'] += 1
                        stats['user_stats'][user_id]['autonomy_weak'] += 1
                    if sdt_analysis.get("competence_status") == "弱":
                        stats['total_competence_weak'] += 1
                        stats['user_stats'][user_id]['competence_weak'] += 1
                    if sdt_analysis.get("relatedness_status") == "弱":
                        stats['total_relatedness_weak'] += 1
                        stats['user_stats'][user_id]['relatedness_weak'] += 1
                
                # 统计chatlog_rating
                chatlog_rating = doc.get("chatlog_rating")
                if chatlog_rating is not None:
                    stats['total_chatlog_rating_count'] += 1
                    stats['total_chatlog_rating_sum'] += chatlog_rating
                    stats['user_stats'][user_id]['chatlog_rating_count'] += 1
                    stats['user_stats'][user_id]['chatlog_rating_sum'] += chatlog_rating

                # 统计finish状态
                if doc.get("finish") == True:
                    stats['total_finish_count'] += 1
                    stats['user_stats'][user_id]['finish_count'] += 1

        return stats

    def print_sdt_stats_summary(self, stats):
        """
        打印SDT分析统计数据的总结。
        
        参数：
            stats (dict): 从 get_sdt_analysis_stats 返回的统计结果
        """
        print("SDT_analysis 总共分析数据条数:", stats['total_records'])
        print("SDT_analysis 总共分析次数:", stats['total_records_ana'])
        print("SDT_analysis 中 '弱' 的总计频次:")
        print("  自主感 (autonomy_status) 弱的频次:", stats['total_autonomy_weak'], "占比：", stats['total_autonomy_weak']/stats['total_records_ana'])
        print("  胜任感 (competence_status) 弱的频次:", stats['total_competence_weak'], "占比：", stats['total_competence_weak']/stats['total_records_ana'])
        print("  关联感 (relatedness_status) 弱的频次:", stats['total_relatedness_weak'], "占比：", stats['total_relatedness_weak']/stats['total_records_ana'])
        
        print("\nchatlog_rating 统计:")
        if stats['total_chatlog_rating_count'] > 0:
            avg_rating = stats['total_chatlog_rating_sum'] / stats['total_chatlog_rating_count']
            print("  chatlog_rating 的平均值:", avg_rating)
            print("  chatlog_rating 有分值的占比:", stats['total_chatlog_rating_count'] / stats['total_records'])
        else:
            print("  没有记录评分的chatlog_rating数据。")
        
        print("\n'finish': True 的比例:")
        print("  完成状态 (finish=True) 的比例:", stats['total_finish_count'] / stats['total_records'])
        
        print("\n每个用户的统计数据:")
        for user_id, user_stat in stats['user_stats'].items():
            print(f"用户 {user_id}:")
            print("  自主感 (autonomy_status) 弱的频次:", user_stat['autonomy_weak'])
            print("  胜任感 (competence_status) 弱的频次:", user_stat['competence_weak'])
            print("  关联感 (relatedness_status) 弱的频次:", user_stat['relatedness_weak'])
            if user_stat['chatlog_rating_count'] > 0:
                avg_user_rating = user_stat['chatlog_rating_sum'] / user_stat['chatlog_rating_count']
                print("  chatlog_rating 的平均值:", avg_user_rating)
                print("  chatlog_rating 有分值的占比:", user_stat['chatlog_rating_count'] / user_stat['record_count'])
            else:
                print("  没有记录评分的chatlog_rating数据。")
            print("  完成状态 (finish=True) 的比例:", user_stat['finish_count'] / user_stat['record_count'])


class DiaryManagerWithStats(DiaryManager):
    
    def get_diary_stats(self, phone_numbers):
        """
        获取用户日记的描述性统计数据，包括日记字数统计、总条数、Agent回应字数统计等。
        
        参数：
            phone_numbers (list): 需要统计的用户ID列表
        
        返回：
            dict: 包含日记内容字数统计、日记总条数、Agent回应字数统计等的统计信息
        """
        stats = {
            'total_diaries': 0,
            'total_diary_word_count': 0,
            'total_agent_response_word_count': 0,
            'user_stats': defaultdict(lambda: {
                'diary_count': 0,
                'total_diary_word_count': 0,
                'total_agent_response_word_count': 0
            })
        }

        # 遍历所有用户
        for user_id in phone_numbers:
            user_documents = self.collection.find({"user_id": user_id})

            for doc in user_documents:
                stats['total_diaries'] += 1
                stats['user_stats'][user_id]['diary_count'] += 1

                # 统计日记内容字数
                diary_content = doc.get("diary_content", "")
                diary_word_count = len(diary_content)
                stats['total_diary_word_count'] += diary_word_count
                stats['user_stats'][user_id]['total_diary_word_count'] += diary_word_count

                # 统计Agent回应字数
                diary_agent_response = doc.get("diary_agent_response", "")
                agent_response_word_count = len(diary_agent_response)
                stats['total_agent_response_word_count'] += agent_response_word_count
                stats['user_stats'][user_id]['total_agent_response_word_count'] += agent_response_word_count

        return stats

    def print_diary_stats_summary(self, stats):
        """
        打印日记统计数据的总结。
        
        参数：
            stats (dict): 从 get_diary_stats 返回的统计结果
        """
        print("日记总条数:", stats['total_diaries'])
        
        if stats['total_diaries'] > 0:
            avg_diary_word_count = stats['total_diary_word_count'] / stats['total_diaries']
            print("日记内容的平均字数:", avg_diary_word_count)
            avg_agent_response_word_count = stats['total_agent_response_word_count'] / stats['total_diaries']
            print("Agent 回应的平均字数:", avg_agent_response_word_count)
        else:
            print("没有日记数据。")
        
        print("\n每个用户的统计数据:")
        for user_id, user_stat in stats['user_stats'].items():
            print(f"用户 {user_id}:")
            print("  日记总条数:", user_stat['diary_count'])
            if user_stat['diary_count'] > 0:
                avg_user_diary_word_count = user_stat['total_diary_word_count'] / user_stat['diary_count']
                print("  日记内容的平均字数:", avg_user_diary_word_count)
                avg_user_agent_response_word_count = user_stat['total_agent_response_word_count'] / user_stat['diary_count']
                print("  Agent 回应的平均字数:", avg_user_agent_response_word_count)
            else:
                print("  没有日记数据。")


class TodoManagerWithStats(TodoManager):
    
    def get_todo_stats(self, phone_numbers):
        """
        获取用户日程的描述性统计数据，包括日程总条数与完成情况、日程类型与紧急程度、生成者标识等。
        
        参数：
            phone_numbers (list): 需要统计的用户ID列表
        
        返回：
            dict: 包含日程统计信息
        """
        stats = {
            'total_todos': 0,
            'total_finished_todos': 0,
            'total_urgency_low': 0,
            'total_urgency_medium': 0,
            'total_urgency_high': 0,
            'total_user_created': 0,
            'total_agent_created': 0,
            'user_stats': defaultdict(lambda: {
                'todo_count': 0,
                'finished_todo_count': 0,
                'urgency_low': 0,
                'urgency_medium': 0,
                'urgency_high': 0,
                'user_created': 0,
                'agent_created': 0
            })
        }

        # 遍历所有用户
        for user_id in phone_numbers:
            user_documents = self.collection.find({"user_id": user_id})

            for doc in user_documents:
                stats['total_todos'] += 1
                stats['user_stats'][user_id]['todo_count'] += 1

                # 统计完成情况
                if doc.get("todo_item_status_finish"):
                    stats['total_finished_todos'] += 1
                    stats['user_stats'][user_id]['finished_todo_count'] += 1

                # 统计紧急程度
                urgency = doc.get("todo_item_urgency", 0)
                if urgency == 0:
                    stats['total_urgency_low'] += 1
                    stats['user_stats'][user_id]['urgency_low'] += 1
                elif urgency == 1:
                    stats['total_urgency_medium'] += 1
                    stats['user_stats'][user_id]['urgency_medium'] += 1
                elif urgency == 2:
                    stats['total_urgency_high'] += 1
                    stats['user_stats'][user_id]['urgency_high'] += 1

                # 统计日程生成者标识
                content = doc.get("todo_item_content", "")
                if re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0]', content):
                    stats['total_agent_created'] += 1
                    stats['user_stats'][user_id]['agent_created'] += 1
                else:
                    stats['total_user_created'] += 1
                    stats['user_stats'][user_id]['user_created'] += 1

        return stats

    def print_todo_stats_summary(self, stats):
        """
        打印日程统计数据的总结。
        
        参数：
            stats (dict): 从 get_todo_stats 返回的统计结果
        """
        print("日程总条数:", stats['total_todos'])
        if stats['total_todos'] > 0:
            print("完成的日程总数:", stats['total_finished_todos'])
            print("完成的日程比例:", stats['total_finished_todos'] / stats['total_todos'])

            print("\n日程紧急程度统计:")
            print("  低紧急程度:", stats['total_urgency_low'])
            print("  中紧急程度:", stats['total_urgency_medium'])
            print("  高紧急程度:", stats['total_urgency_high'])

            print("\n日程生成者统计:")
            print("  用户创建的日程:", stats['total_user_created'])
            print("  Agent 创建的日程:", stats['total_agent_created'])
        else:
            print("没有日程数据。")

        print("\n每个用户的统计数据:")
        for user_id, user_stat in stats['user_stats'].items():
            print(f"用户 {user_id}:")
            print("  日程总条数:", user_stat['todo_count'])
            if user_stat['todo_count'] > 0:
                print("  完成的日程:", user_stat['finished_todo_count'])
                print("  完成的日程比例:", user_stat['finished_todo_count'] / user_stat['todo_count'])
                print("  低紧急程度:", user_stat['urgency_low'])
                print("  中紧急程度:", user_stat['urgency_medium'])
                print("  高紧急程度:", user_stat['urgency_high'])
                print("  用户创建的日程:", user_stat['user_created'])
                print("  Agent 创建的日程:", user_stat['agent_created'])
            else:
                print("  没有日程数据。")

class MindfulsManagerWithStats(MindfulsManager):
    
    def get_mindful_stats(self, phone_numbers):
        """
        获取用户冥想功能的描述性统计数据，包括使用频率、实际完成时长及完成率等。
        
        参数：
            phone_numbers (list): 需要统计的用户ID列表
        
        返回：
            dict: 包含冥想统计信息
        """
        stats = {
            'total_sessions': 0,
            'total_duration': 0,
            'total_completed_sessions': 0,
            'user_stats': defaultdict(lambda: {
                'session_count': 0,
                'total_duration': 0,
                'completed_sessions': 0
            })
        }

        # 遍历所有用户
        for user_id in phone_numbers:
            user_documents = self.collection.find({"user_id": user_id})

            for doc in user_documents:
                stats['total_sessions'] += 1
                stats['user_stats'][user_id]['session_count'] += 1

                # 统计冥想的总时长
                duration = doc.get("mindful_duration", 0)
                stats['total_duration'] += duration
                stats['user_stats'][user_id]['total_duration'] += duration

                # 统计完成的冥想次数
                if doc.get("mindful_status"):
                    stats['total_completed_sessions'] += 1
                    stats['user_stats'][user_id]['completed_sessions'] += 1

        return stats

    def print_mindful_stats_summary(self, stats):
        """
        打印冥想统计数据的总结。
        
        参数：
            stats (dict): 从 get_mindful_stats 返回的统计结果
        """
        print("冥想功能使用总次数:", stats['total_sessions'])
        print("冥想总时长:", stats['total_duration'])
        if stats['total_sessions'] > 0:
            print("平均每次冥想时长:", stats['total_duration'] / stats['total_sessions'])
            print("完成的冥想次数:", stats['total_completed_sessions'])
            print("冥想完成率:", stats['total_completed_sessions'] / stats['total_sessions'])
        else:
            print("没有冥想数据。")

        print("\n每个用户的统计数据:")
        for user_id, user_stat in stats['user_stats'].items():
            print(f"用户 {user_id}:")
            print("  冥想使用次数:", user_stat['session_count'])
            print("  总冥想时长:", user_stat['total_duration'])
            if user_stat['session_count'] > 0:
                print("  平均每次冥想时长:", user_stat['total_duration'] / user_stat['session_count'])
                print("  完成的冥想次数:", user_stat['completed_sessions'])
                print("  冥想完成率:", user_stat['completed_sessions'] / user_stat['session_count'])
            else:
                print("  没有冥想数据。")

class TomatoesManagerWithStats(TomatoesManager):
    
    def get_tomato_stats(self, phone_numbers):
        """
        获取用户番茄钟功能的描述性统计数据，包括使用频率、时长、实际完成率等。
        
        参数：
            phone_numbers (list): 需要统计的用户ID列表
        
        返回：
            dict: 包含番茄钟统计信息
        """
        stats = {
            'total_sessions': 0,
            'total_duration': 0,
            'total_completed_sessions': 0,
            'user_stats': defaultdict(lambda: {
                'session_count': 0,
                'total_duration': 0,
                'completed_sessions': 0
            })
        }

        # 遍历所有用户
        for user_id in phone_numbers:
            user_documents = self.collection.find({"user_id": user_id})

            for doc in user_documents:
                stats['total_sessions'] += 1
                stats['user_stats'][user_id]['session_count'] += 1

                # 统计番茄钟的总时长
                duration = doc.get("tomato_duration", 0)
                stats['total_duration'] += duration
                stats['user_stats'][user_id]['total_duration'] += duration

                # 统计完成的番茄钟次数
                if doc.get("tomato_status"):
                    stats['total_completed_sessions'] += 1
                    stats['user_stats'][user_id]['completed_sessions'] += 1

        return stats

    def print_tomato_stats_summary(self, stats):
        """
        打印番茄钟统计数据的总结。
        
        参数：
            stats (dict): 从 get_tomato_stats 返回的统计结果
        """
        print("番茄钟使用总次数:", stats['total_sessions'])
        print("番茄钟总时长:", stats['total_duration'])
        if stats['total_sessions'] > 0:
            print("平均每次番茄钟时长:", stats['total_duration'] / stats['total_sessions'])
            print("完成的番茄钟次数:", stats['total_completed_sessions'])
            print("番茄钟完成率:", stats['total_completed_sessions'] / stats['total_sessions'])
        else:
            print("没有番茄钟数据。")

        print("\n每个用户的统计数据:")
        for user_id, user_stat in stats['user_stats'].items():
            print(f"用户 {user_id}:")
            print("  番茄钟使用次数:", user_stat['session_count'])
            print("  总番茄钟时长:", user_stat['total_duration'])
            if user_stat['session_count'] > 0:
                print("  平均每次番茄钟时长:", user_stat['total_duration'] / user_stat['session_count'])
                print("  完成的番茄钟次数:", user_stat['completed_sessions'])
                print("  番茄钟完成率:", user_stat['completed_sessions'] / user_stat['session_count'])
            else:
                print("  没有番茄钟数据。")


class MoodManagerWithStats(MoodManager):

    def extract_mood_data(self, phone_numbers):
        """
        提取每个用户每天的心情值和情绪关联词条的正向度
        
        参数：
            phone_numbers (list): 需要提取数据的用户ID列表
        
        返回：
            dict: 包含用户每天心情值和正向度的信息
        """
        mood_data = defaultdict(lambda: defaultdict(list))  # 用户 -> 日期 -> [心情值, 关键词正向度]
        
        for user_id in phone_numbers:
            user_moods = self.collection.find({"user_id": user_id})
            
            for mood in user_moods:
                # 提取日期信息（只保留日期部分）
                mood_time = mood["mood_time_logged"].date()
                
                # 将心情值重新映射到 [-100, 100] 的范围
                mood_indicator = 100 - mood["mood_indicator"] * 200

                # 计算正向度（所有关键词共享心情值）
                mood_keywords = mood.get("mood_keywords", [])
                positive_degree = mood_indicator / 100 if mood_keywords else 0

                # 存储心情值和正向度
                mood_data[user_id][mood_time].append((mood_indicator, positive_degree, mood_keywords))

        return mood_data

    def generate_mood_statistics(self, mood_data):
        """
        生成心情数据的描述性统计报告。
        
        参数：
            mood_data (dict): 提取的用户心情数据
        
        返回：
            dict: 包含统计信息的报告
        """
        report = defaultdict(lambda: {
            'mood_summary': {},  # 心情值统计
            'keyword_frequency': {},  # 关键词频率
            'positive_degree_summary': {},  # 关键词正向度统计
        })
        
        # 遍历所有用户的心情数据
        for user_id, daily_data in mood_data.items():
            all_mood_values = []
            all_keywords = []
            all_positive_degrees = []

            for date, mood_entries in daily_data.items():
                # 提取心情值和正向度
                mood_values = [mood_value for mood_value, _, _ in mood_entries]
                positive_degrees = [positive_degree for _, positive_degree, _ in mood_entries]
                keywords = [kw for _, _, kws in mood_entries for kw in kws]

                all_mood_values.extend(mood_values)
                all_positive_degrees.extend(positive_degrees)
                all_keywords.extend(keywords)

            # 计算心情值的统计信息
            mood_mean = np.mean(all_mood_values)
            mood_std = np.std(all_mood_values)
            mood_min = np.min(all_mood_values)
            mood_max = np.max(all_mood_values)

            # 关键词频率统计
            keyword_counter = Counter(all_keywords)
            total_keywords = sum(keyword_counter.values())
            keyword_freq = {k: v / total_keywords for k, v in keyword_counter.items()}

            # 关键词正向度统计
            positive_degree_mean = np.mean(all_positive_degrees)
            positive_degree_std = np.std(all_positive_degrees)

            # 填充报告
            report[user_id]['mood_summary'] = {
                'mean': mood_mean,
                'std_dev': mood_std,
                'min': mood_min,
                'max': mood_max,
                'total_entries': len(all_mood_values)
            }
            report[user_id]['keyword_frequency'] = keyword_freq
            report[user_id]['positive_degree_summary'] = {
                'mean': positive_degree_mean,
                'std_dev': positive_degree_std
            }

        return report

    def print_mood_statistics_report(self, report):
        """
        打印心情数据的描述性统计报告。
        
        参数：
            report (dict): 从 generate_mood_statistics 返回的统计结果
        """
        for user_id, stats in report.items():
            print(f"\n### 用户 {user_id} 的心情统计报告：")
            
            # 打印心情值统计
            mood_summary = stats['mood_summary']
            print(f"心情值统计：")
            print(f"  平均值: {mood_summary['mean']:.2f}")
            print(f"  标准差: {mood_summary['std_dev']:.2f}")
            print(f"  最小值: {mood_summary['min']:.2f}")
            print(f"  最大值: {mood_summary['max']:.2f}")
            print(f"  总记录数: {mood_summary['total_entries']}")

            # 打印关键词频率
            print(f"\n情绪关键词频率：")
            for keyword, freq in stats['keyword_frequency'].items():
                print(f"  {keyword}: {freq * 100:.2f}%")

            # 打印关键词正向度统计
            positive_degree_summary = stats['positive_degree_summary']
            print(f"\n关键词正向度统计：")
            print(f"  平均正向度: {positive_degree_summary['mean']:.2f}")
            print(f"  正向度标准差: {positive_degree_summary['std_dev']:.2f}")
            
    def plot_mood_scatter(self, mood_data):
        """
        绘制情绪散点图，颜色从紫色到绿色到红色，表示心情程度。
        
        参数：
            mood_data (dict): 每个用户每天的心情数据
        """
        plt.figure(figsize=(10, 6))
        
        for user_id, daily_data in mood_data.items():
            for date, mood_values in daily_data.items():
                for mood_indicator, _, _ in mood_values:
                    # 使用 HSL 映射心情值到颜色
                    value = abs((mood_indicator + 100) / 200 - 1)  # 映射到 [0, 1] 范围
                    hue = (1 - value) * 23 + value * 273  # HSL 中的 hue 值
                    rgb_color = hsl_to_rgb(hue, 80, 50)  # 将 HSL 转换为 RGB
                    
                    # 绘制散点
                    plt.scatter(date, mood_indicator, color=rgb_color, label=user_id)
        
        plt.title("Emotional scatter chart")
        plt.xlabel("Date")
        plt.ylabel("moods index [-100, 100]")
        plt.grid(True)
        plt.savefig('exp_l_static_mood_1.jpg')
        plt.show()

    def plot_mood_factor_trend(self,mood_data):
        """
        绘制情绪-因素影响关联度变化图。
        
        参数：
            mood_data (dict): 每个用户每天的心情数据
        """
        plt.figure(figsize=(10, 6))

        for user_id, daily_data in mood_data.items():
            dates = []
            positive_degrees = []
            
            for date, mood_values in daily_data.items():
                total_positive_degree = sum(positive_degree for _, positive_degree, _ in mood_values)
                dates.append(date)
                positive_degrees.append(total_positive_degree)

            # 绘制趋势图
            plt.plot(dates, positive_degrees, label=f"{user_id} Positive degree change")
        
        plt.title("Emotion-factors influence the change of correlation degree")
        plt.xlabel("Date")
        plt.ylabel("Positive dimension")
        plt.grid(True)
        # 移动图例到图的外侧
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1, fontsize='small')  # 将图例移到右侧

        plt.tight_layout(rect=[0, 0, 0.85, 1])  # 调整图的布局，避免图例遮挡图像
        plt.savefig('exp_l_static_mood_2.jpg')
        plt.show()



def count_sent_documents(collection_name):
    # 连接 MongoDB 数据库
    client = MongoClient("mongodb://localhost:27017/")  # 修改为你的 MongoDB 连接 URI
    db = client['heartDBEval']  # 修改为你的数据库名
    collection = db[collection_name]

    # 查询 sent = true 的文档数量
    sent_count = collection.count_documents({"sent": True})

    return sent_count

# 使用示例
collection_name = "autoMessage"  # 修改为你的集合名
sent_count = count_sent_documents(collection_name)
print("# 用户主动发消息(autoMessage)的描述性统计")
print(f"Sent 为 true 的文档数量: {sent_count}")


print("\n\n")
print("# 用户聊天数据(chatlog)的描述性统计")
manager_chatlog_sta = ChatLogManagerWithStats()
sta = manager_chatlog_sta.get_all_users_chat_stats(phone_numbers=phone_numbers)
manager_chatlog_sta.print_stats_summary(stats=sta)

print("\n\n")
print("# 用户SDT、STAR数据(chatana)的描述性统计")
manager_chatana_sta = ChatAnaManagerWithStats()
sta = manager_chatana_sta.get_sdt_analysis_stats(phone_numbers=phone_numbers)
manager_chatana_sta.print_sdt_stats_summary(stats=sta)

print("\n\n")
print("# 用户日记数据(diary)的描述性统计")
manager_diary_sta = DiaryManagerWithStats()
sta = manager_diary_sta.get_diary_stats(phone_numbers=phone_numbers)
manager_diary_sta.print_diary_stats_summary(stats=sta)

print("\n\n")
print("# 用户日程数据(todo)的描述性统计")
manager_todo_sta = TodoManagerWithStats()
sta = manager_todo_sta.get_todo_stats(phone_numbers=phone_numbers)
manager_todo_sta.print_todo_stats_summary(stats=sta)

print("\n\n")
print("# 用户冥想数据(mindful)的描述性统计")
manager_mind_sta = MindfulsManagerWithStats()
sta = manager_mind_sta.get_mindful_stats(phone_numbers=phone_numbers)
manager_mind_sta.print_mindful_stats_summary(stats=sta)

print("\n\n")
print("# 用户番茄数据(tomato)的描述性统计")
manager_tomato_sta = TomatoesManagerWithStats()
sta = manager_tomato_sta.get_tomato_stats(phone_numbers=phone_numbers)
manager_tomato_sta.print_tomato_stats_summary(stats=sta)


print("\n\n")
print("# 用户心情数据(mood)的描述性统计")
mood_manager_sta = MoodManagerWithStats()
# 提取心情数据
mood_data = mood_manager_sta.extract_mood_data(phone_numbers)
# 绘制情绪散点图
mood_manager_sta.plot_mood_scatter(mood_data)
# 绘制情绪-因素关联度变化趋势图
mood_manager_sta.plot_mood_factor_trend(mood_data)
# 描述性统计
sta = mood_manager_sta.generate_mood_statistics(mood_data)
mood_manager_sta.print_mood_statistics_report(sta)