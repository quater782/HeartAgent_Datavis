import re
import json
import os

def read_log_file(log_file):
    print("read")
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as file:
        return file.readlines()

def parse_logs(lines, relevant_functions, filepath):
    with open(f"{filepath}.json", 'a', encoding='utf-8') as f:
        f.write('[\n')
    print("parsing")
    entries = []
    current_entry = None
    count_dict = {func: 0 for func in relevant_functions}

    log_levels = ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL', 'SUCCESS']
    entry_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \| (\w+) +\| ([\w\.]+):([\w_]+):(\d+) - (.*)')
    i = 0
    for line in lines:
        if entry_pattern.match(line)!= None:
            # print(i)
            # 处理新的日志条目
            if current_entry:
                # 如果已经有正在记录的条目，则先保存当前条目
                i+=1
                entries.append(current_entry)
                write_entry_to_file(current_entry, filepath, i)
                current_entry = None

            match = entry_pattern.match(line)
            # print(f"match = {match.group(3)}:{match.group(4)}:{match.group(5)}")

            if match!=None:
                function_id = f"{match.group(3)}:{match.group(4)}:{match.group(5)}"
                # print(function_id)
                if function_id in relevant_functions:
                    current_entry = {
                        'datetime': match.group(1),
                        'function_sequence': function_id,
                        'content': match.group(6).strip()
                    }
                    count_dict[function_id] += 1
                    print(f"添加了一条 {function_id} 的记录，当前计数值：{count_dict[function_id]}")
                continue
        elif current_entry:
            # 如果当前记录未完成，继续记录内容
            current_entry['content'] += ' ' + line.strip()
            # print(line.strip())
            # print(f"为 {current_entry['function_sequence']} 添加了content，当前计数值：{count_dict[current_entry['function_sequence']]}")
            # print(current_entry['content'])

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

            print(json_str)
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
def readlogs(path:str):
    log_file = f"logdata/logs/{path}"
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
    lines = read_log_file(log_file)
    logs_json = parse_logs(lines, relevant_functions,path)
    # with open(f"logdata/extractedjson/{path}.json", 'w', encoding='utf-8') as f:
    #     json.dump(logs_json, f, ensure_ascii=False, indent=4)

import os

def list_files_in_directory(directory):
    # 获取目录下所有文件的文件名（包括扩展名）
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files

def main():
    directory = 'logdata/logs'  # 替换为你的目录路径
    files_list = list_files_in_directory(directory)
    for item in files_list:
        print(f"reading{item}")
        readlogs(item)


main()
