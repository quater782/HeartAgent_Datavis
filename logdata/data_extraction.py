import re
import json
import os

def read_log_file(log_file):
    # print("read")
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as file:
        return file.readlines()

def parse_logs(lines, relevant_functions, filepath):
    with open(f"logdata\extractedjson\{filepath}.json", 'w', encoding='utf-8') as f:
        f.write('[\n')
    # print("parsing")
    entries = []
    current_entry = None
    count_dict = {func: 0 for func in relevant_functions}

    log_levels = ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL', 'SUCCESS']
    entry_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \| (\w+) +\| ([\w\.]+):([\w_]+):(\d+) - (.*)')
    i = 0
    for line in lines:
        if entry_pattern.match(line)!= None:
            # # print(i)
            # 处理新的日志条目
            if current_entry:
                # 如果已经有正在记录的条目，则先保存当前条目
                i+=1
                entries.append(current_entry)
                write_entry_to_file(current_entry, filepath, i)
                current_entry = None

            match = entry_pattern.match(line)
            # # print(f"match = {match.group(3)}:{match.group(4)}:{match.group(5)}")

            if match!=None:
                function_id = f"{match.group(3)}:{match.group(4)}:{match.group(5)}"
                # # print(function_id)
                if function_id in relevant_functions:
                    current_entry = {
                        'datetime': match.group(1),
                        'function_sequence': function_id,
                        'content': match.group(6).strip()
                    }
                    count_dict[function_id] += 1
                    # print(f"添加了一条 {function_id} 的记录，当前计数值：{count_dict[function_id]}")
                continue
        elif current_entry:
            # 如果当前记录未完成，继续记录内容
            current_entry['content'] += ' ' + line.strip()
            # # print(line.strip())
            # # print(f"为 {current_entry['function_sequence']} 添加了content，当前计数值：{count_dict[current_entry['function_sequence']]}")
            # # print(current_entry['content'])

    if current_entry:
        entries.append(current_entry)
        write_entry_to_file(current_entry, filepath)
    
    with open(f"{filepath}.json", 'a', encoding='utf-8') as f:
        f.write(']\n')

    return entries

def write_entry_to_file(entry, filepath:str, num):
    formatted_data = format_entry(entry)
    with open(f"{filepath}.json", 'a', encoding='utf-8') as f:
        if num !=1:
            f.write(',\n')
        json.dump(formatted_data, f, ensure_ascii=False, indent=4)


def format_entry(entry):
    content = entry['content']
    json_content = None
    
    try:
        # 尝试从字符串中找到 JSON 对象的起始位置

        if "{" and "}" in content:
            start_index = content.find("{")
            end_index = content.find("}")+1
            json_str = content[start_index:end_index]
            

            json_str = json_str.replace("'", '"')
            json_str = json_str.replace("'", '"')
            json_str = json_str.replace(f"\"", '"')

            # print(json_str)
            json_content = json.loads(json_str)
    
    except json.JSONDecodeError:
        pass
    
    formatted_entry = {
        'datetime': entry['datetime'],
        'function_sequence': entry['function_sequence'],
        'extracted_content': json_content if json_content else content
    }
    
    return formatted_entry
# 示例输入
entries = [{
    'datetime': '2024-08-28 12:06:08.310',
    'function_sequence': 'app.services.todo_service:todo_get_greetings:92',
    'content': 'result:{ "user_id": "18392440042", "todo_greetings_title": "午安，朋友！", "todo_greetings_content": "新的一天，新的开始！" }'
}]

relevant_functions = [
    'app.services.chat_service:grow_demand_judgment:319',#判断是不是要干预
    'app.services.chat_service:grow_SDT:362',#干预的js（ = demand_judgement = true）
    'app.universalAPP:request:645',#检测到关键词，但是llm认为不需要干预（这个部分可以不看）
    'app.services.chat_service:determine_completion:196', #判断干预是否已经结束
    'app.services.todo_service:todo_demand_judgment:32',#判断是否要加todo
    'app.services.todo_service:todo_get_greetings:92', #获得greetings
    'app.services.todo_service:todo_get_dailysummary:128',#获得日程每日总结
    'app.services.mood_service:get_mood_trends:41',#获取心情trend记录（bot版本）
    'app.services.diary_service:diary_get_agent_response:52',#获取日记 - agent反馈
    'app.routers.chat:run_reflection:83',#获取反思
    'app.services.chat_service:star_reflection:684'#获取star反思
]

def readlogs(path:str):
    log_file = f"logdata/logs/{path}"

    lines = read_log_file(log_file)
    logs_json = parse_logs(lines, relevant_functions,path)
    # with open(f"logdata/extractedjson/{path}.json", 'w', encoding='utf-8') as f:
    #     json.dump(logs_json, f, ensure_ascii=False, indent=4)

import os

def list_files_in_directory(directory):
    # 获取目录下所有文件的文件名（包括扩展名）
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    # print(files)
    return files

def read_save_all_logs():
    directory = 'logdata/logs'  # 替换为你的目录路径
    files_list = list_files_in_directory(directory)
    for item in files_list:
        # print(f"reading{item}")
        readlogs(item)


# main()


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

def macth_user(id:str):
    for item in phone_numbers:
        if id == item:
            return True
    return False

services_to_check = {"app.services.chat_service:grow_demand_judgment:319":{"count":0, "true":0, "f/un":0, "fail":0},#判断是不是要干预
    "app.services.chat_service:grow_SDT:362":{"count" : 0},#干预的js（ = demand_judgement = true）
    "app.universalAPP:request:645":{"count":0},#检测到关键词，但是llm认为不需要干预（这个部分可以不看）
    "app.services.chat_service:determine_completion:196":{"count":0, "true":0, "f/un":0, "fail":0}, #判断干预是否已经结束
    "app.services.todo_service:todo_demand_judgment:32":{"count":0, "true":0, "f/un":0, "fail":0},#判断是否要加todo
    "app.services.todo_service:todo_get_greetings:92":{"count":0,"fail":0, "wordcount":0}, #获得greetings
    "app.services.todo_service:todo_get_dailysummary:128":{"count":0, "fail":0, "wordcount":0},#获得日程每日总结
    "app.services.mood_service:get_mood_trends:41":{"count":0, "fail":0, "wordcount":0},#获取心情trend记录（bot版本）
    "app.services.diary_service:diary_get_agent_response:52":{"count":0, "fail":0, "wordcount":0},#获取日记 - agent反馈
    "app.routers.chat:run_reflection:83":{"count":0},#获取反思
    "app.services.chat_service:star_reflection:684":{"count":0}
    }

def count_services_in_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # 遍历 JSON 中的每个条目
        for entry in data:
            if relevant_functions[0] in entry["function_sequence"]:
                # print("添加了干预起始判断一条")
                services_to_check[relevant_functions[0]]["count"]+=1
                content = entry["extracted_content"]
                if "true" in content or "True" in content:
                    services_to_check[relevant_functions[0]]["true"]+=1
                elif "false" in content or "unclear" in content or "False" in content or "Unclear" in content:
                    services_to_check[relevant_functions[0]]["f/un"]+=1
                else:
                    # print(f"{content}\n")
                    services_to_check[relevant_functions[0]]["fail"]+=1

            elif relevant_functions[1] in entry["function_sequence"]:
                # print("添加了开始干预痕迹，1条")
                services_to_check[relevant_functions[1]]["count"]+=1

            elif relevant_functions[2] in entry["function_sequence"]:
                # print("添加了触发关键词但不干预，1条")
                services_to_check[relevant_functions[2]]["count"]+=1

            elif relevant_functions[3] in entry["function_sequence"]:
                services_to_check[relevant_functions[3]]["count"]+=1
                # print("添加了干预结束判断一条")
                content = entry["extracted_content"]
                if "true" in content or "True" in content:
                    services_to_check[relevant_functions[3]]["true"]+=1
                elif "false" in content or "unclear" in content or "False" in content or "Unclear" in content:
                    services_to_check[relevant_functions[3]]["f/un"]+=1
                else:
                    services_to_check[relevant_functions[3]]["fail"]+=1
                    
            elif relevant_functions[4] in entry["function_sequence"]:
                services_to_check[relevant_functions[4]]["count"]+=1
                # print("添加了添加日程判断一条")
                content = entry["extracted_content"]
                if "true" in content or "True" in content:
                    services_to_check[relevant_functions[4]]["true"]+=1
                elif "false" in content or "unclear" in content or "False" in content or "Unclear" in content:
                    services_to_check[relevant_functions[4]]["f/un"]+=1
                else:
                    services_to_check[relevant_functions[4]]["fail"]+=1

            elif relevant_functions[5] in entry["function_sequence"]:
                services_to_check[relevant_functions[5]]["count"]+=1
                # print("添加了todo日程greetings一条")
                content = {}
                content = entry["extracted_content"]
                sum=""
                result1 = content.get('todo_greetings_title', 'notfound')
                result2 = content.get('todo_greetings_content', 'notfound')
                if result1!="notfound":
                    sum = f"{sum}{result1}"
                if result2!="notfound":
                    sum = f"{sum}{result2}"
                lenth = len(sum)
                if lenth<1:
                    # print("添加了todo日程greetings - fail record 一条")
                    services_to_check[relevant_functions[5]]["fail"]+=1
                else:
                    services_to_check[relevant_functions[5]]["wordcount"]+=lenth

            elif relevant_functions[6] in entry["function_sequence"]:
                services_to_check[relevant_functions[6]]["count"]+=1
                # print("添加了todo日程每日总结一条")
                content = {}
                try:
                    content = entry["extracted_content"]
                    userid = content["user_id"]
                    if macth_user(userid):
                        sum=""
                        result1 = content.get('dailysummary', 'notfound')
                        if result1!="notfound":
                            sum = f"{sum}{result1}"
                        lenth = len(sum)
                        if lenth<1:
                            # print("添加了todo日程每日总结 - fail record 一条")
                            services_to_check[relevant_functions[6]]["fail"]+=1
                        else:
                            services_to_check[relevant_functions[6]]["wordcount"]+=lenth
                    else:
                        services_to_check[relevant_functions[6]]["count"]-=1
                except Exception as e:
                    # print("不符合格式规范，扣打分")
                    services_to_check[relevant_functions[7]]["fail"]+=1  
            
            elif relevant_functions[7] in entry["function_sequence"]:
                services_to_check[relevant_functions[7]]["count"]+=1
                # print(entry["extracted_content"])
                # print("添加了moodtrends一条")
                content = {}
                try:
                    content = entry["extracted_content"]
                    userid = content["user_id"]
                    if macth_user(userid):
                        sum=""
                        result1 = content.get('trends', 'notfound')
                        if result1!="notfound":
                            sum = f"{sum}{result1}"
                        lenth = len(sum)
                        if lenth<1:
                            # print("添加了moodtrends - fail record 一条")
                            services_to_check[relevant_functions[7]]["fail"]+=1
                        else:
                            services_to_check[relevant_functions[7]]["wordcount"]+=lenth
                    else:
                        services_to_check[relevant_functions[7]]["count"]-=1
                except Exception as e:
                    # print("不符合格式规范，扣打分")
                    services_to_check[relevant_functions[7]]["fail"]+=1


            
            elif relevant_functions[8] in entry["function_sequence"]:
                services_to_check[relevant_functions[8]]["count"]+=1
                # print("添加了日记回应一条")
                content = {}
                try:
                    content = entry["extracted_content"]
                    userid = content["user_id"]
                    if macth_user(userid):
                        sum=""
                        result1 = content.get('diary_agent_response', 'notfound')
                        if result1!="notfound":
                            sum = f"{sum}{result1}"
                        lenth = len(sum)
                        if lenth<1:
                            # print("添加了日记回应 - fail record 一条")
                            services_to_check[relevant_functions[8]]["fail"]+=1
                        else:
                            services_to_check[relevant_functions[8]]["wordcount"]+=lenth
                    else:
                        services_to_check[relevant_functions[8]]["count"]-=1
                except Exception as e:
                    # print("不符合格式规范，扣打分")
                    services_to_check[relevant_functions[7]]["fail"]+=1                      

    except FileNotFoundError:
        print("文件未找到，请检查文件路径是否正确。")
    except json.JSONDecodeError:
        print("JSON文件格式有误，请检查文件内容。")



def read_a_json(path:str):
    json_file = f"logdata\extractedjson\{path}"
    count_services_in_json(json_file)
    # with open(f"logdata/extractedjson/{path}.json", 'w', encoding='utf-8') as f:
    #     json.dump(logs_json, f, ensure_ascii=False, indent=4)

def read_all_json():
    jslist = list_files_in_directory("logdata\extractedjson")
    for jsonfile in jslist:
        print(f"readingfile: {jsonfile}")
        read_a_json(jsonfile)
    
    filename = f'contreasult.json'

    # 使用 'with' 语句打开文件，确保正确关闭文件
    with open(filename, 'w', encoding='utf-8') as file:
        # 使用 json.dump 将数据写入文件，确保使用utf-8编码
        json.dump(services_to_check, file, ensure_ascii=False,indent=4)

read_all_json()



def calculate_statistics(services):
    for key, stats in services.items():
        if 'count' in stats:
            print(f"{key} - Total Number: {stats['count']}")
        if 'fail' in stats:
            fail_rate = stats['fail'] / stats['count'] * 100
            print(f"{key} - Fail Rate: {fail_rate:.2f}%")
        
        if 'true' in stats:
            true_rate = stats['true'] / stats['count'] * 100
            f_un_rate = stats['f/un'] / stats['count'] * 100
            print(f"{key} - True Rate: {true_rate:.2f}%, F/UN Rate: {f_un_rate:.2f}%")

        if 'wordcount' in stats:
            if 'true' in stats and stats['true'] > 0:
                avg_words_per_true = stats['wordcount'] / stats['true']
                print(f"{key} - Average Words per True: {avg_words_per_true:.2f}")
            else:
                avg_words = stats['wordcount'] / stats['count']
                print(f"{key} - Average Words: {avg_words:.2f}")
        print(f"\n")

# 调用函数计算统计数据
calculate_statistics(services_to_check)

'''
app.services.chat_service:grow_demand_judgment:319 - Total Number: 422
app.services.chat_service:grow_demand_judgment:319 - Fail Rate: 5.21%
app.services.chat_service:grow_demand_judgment:319 - True Rate: 27.96%, F/UN Rate: 66.82%


app.services.chat_service:grow_SDT:362 - Total Number: 112


app.universalAPP:request:645 - Total Number: 277


app.services.chat_service:determine_completion:196 - Total Number: 454
app.services.chat_service:determine_completion:196 - Fail Rate: 0.00%
app.services.chat_service:determine_completion:196 - True Rate: 22.69%, F/UN Rate: 77.31%


app.services.todo_service:todo_demand_judgment:32 - Total Number: 946
app.services.todo_service:todo_demand_judgment:32 - Fail Rate: 0.74%
app.services.todo_service:todo_demand_judgment:32 - True Rate: 29.28%, F/UN Rate: 69.98%


app.services.todo_service:todo_get_greetings:92 - Total Number: 753
app.services.todo_service:todo_get_greetings:92 - Fail Rate: 10.76%
app.services.todo_service:todo_get_greetings:92 - Average Words: 12.79


app.services.todo_service:todo_get_dailysummary:128 - Total Number: 652
app.services.todo_service:todo_get_dailysummary:128 - Fail Rate: 0.92%
app.services.todo_service:todo_get_dailysummary:128 - Average Words: 23.20


app.services.mood_service:get_mood_trends:41 - Total Number: 667
app.services.mood_service:get_mood_trends:41 - Fail Rate: 28.94%
app.services.mood_service:get_mood_trends:41 - Average Words: 18.01
app.services.mood_service:get_mood_trends:41 - Average Words: 18.01



app.services.diary_service:diary_get_agent_response:52 - Total Number: 245

app.services.diary_service:diary_get_agent_response:52 - Total Number: 245
app.services.diary_service:diary_get_agent_response:52 - Total Number: 245
app.services.diary_service:diary_get_agent_response:52 - Fail Rate: 0.00%
app.services.diary_service:diary_get_agent_response:52 - Average Words: 147.03


app.routers.chat:run_reflection:83 - Total Number: 0


app.services.chat_service:star_reflection:684 - Total Number: 0

'''







'''
app.services.chat_service:grow_demand_judgment:319 - Total Number: 422
app.services.chat_service:grow_demand_judgment:319 - Fail Rate: 5.21%
app.services.chat_service:grow_demand_judgment:319 - True Rate: 27.96%, F/UN Rate: 66.82%


app.services.chat_service:grow_SDT:362 - Total Number: 112


app.universalAPP:request:645 - Total Number: 277


app.services.chat_service:determine_completion:196 - Total Number: 454
app.services.chat_service:determine_completion:196 - Fail Rate: 0.00%
app.services.chat_service:determine_completion:196 - True Rate: 22.69%, F/UN Rate: 77.31%


app.services.todo_service:todo_demand_judgment:32 - Total Number: 946
app.services.todo_service:todo_demand_judgment:32 - Fail Rate: 0.74%
app.services.todo_service:todo_demand_judgment:32 - True Rate: 29.28%, F/UN Rate: 69.98%


app.services.todo_service:todo_get_greetings:92 - Total Number: 753
app.services.todo_service:todo_get_greetings:92 - Fail Rate: 10.76%
app.services.todo_service:todo_get_greetings:92 - Average Words: 12.79


app.services.todo_service:todo_get_dailysummary:128 - Total Number: 743
app.services.todo_service:todo_get_dailysummary:128 - Fail Rate: 5.52%
app.services.todo_service:todo_get_dailysummary:128 - Average Words: 23.40


app.services.mood_service:get_mood_trends:41 - Total Number: 707
app.services.mood_service:get_mood_trends:41 - Fail Rate: 11.03%
app.services.mood_service:get_mood_trends:41 - Average Words: 19.88


app.services.diary_service:diary_get_agent_response:52 - Total Number: 268
app.services.diary_service:diary_get_agent_response:52 - Fail Rate: 0.00%
app.services.diary_service:diary_get_agent_response:52 - Average Words: 163.64


app.routers.chat:run_reflection:83 - Total Number: 0


app.services.chat_service:star_reflection:684 - Total Number: 0
'''