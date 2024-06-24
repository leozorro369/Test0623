import json

try:
    with open('questions_corrected.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
        print("JSON文件格式正确！")
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
except Exception as e:
    print(f"其他错误: {e}")
