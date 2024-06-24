from docx import Document
import json

def extract_questions_from_word(doc_path):
    doc = Document(doc_path)
    questions = {"fill_in_the_blank": [], "single_choice": [], "multiple_choice": [], "true_false": [], "case_analysis": [], "answers": {}}
    section = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if text.startswith("一、填空题"):
            section = "fill_in_the_blank"
        elif text.startswith("二、单选题"):
            section = "single_choice"
        elif text.startswith("三、多选题"):
            section = "multiple_choice"
        elif text.startswith("四、判断题"):
            section = "true_false"
        elif text.startswith("五、案例分析题"):
            section = "case_analysis"
        elif text.startswith("标准答案"):
            section = "answers"
        elif section:
            if section == "answers":
                if text:
                    parts = text.split(' ')
                    question_num = parts[0].rstrip('.')
                    answer = parts[1:]
                    questions[section][question_num] = answer
            else:
                questions[section].append(text)
    
    return questions

doc_path = '0623基础知识学习测试题2.docx'
questions = extract_questions_from_word(doc_path)
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=4)
