'''
大实验的描述性数据分析

'''
import sys
# 将父目录添加到系统路径
import os
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
from DB.manage_chat import ChatLogManager
from DB.manage_chatana import ChatAnaManager

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
            'user_stats': defaultdict(lambda: {
                'autonomy_weak': 0,
                'competence_weak': 0,
                'relatedness_weak': 0,
                'chatlog_rating_count': 0,
                'chatlog_rating_sum': 0,
                'finish_count': 0,
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
        print("SDT_analysis 中 '弱' 的总计频次:")
        print("  自主感 (autonomy_status) 弱的频次:", stats['total_autonomy_weak'])
        print("  胜任感 (competence_status) 弱的频次:", stats['total_competence_weak'])
        print("  关联感 (relatedness_status) 弱的频次:", stats['total_relatedness_weak'])
        
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
print("# 用户日程数据(todo)的描述性统计")

print("\n\n")
print("# 用户日记数据(diary)的描述性统计")

print("\n\n")
print("# 用户番茄数据(tomato)的描述性统计")

print("\n\n")
print("# 用户冥想数据(mindful)的描述性统计")

print("\n\n")
print("# 用户心情数据(mood)的描述性统计")