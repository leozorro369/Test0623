import json
from flask import Flask, request, render_template, jsonify, send_from_directory
import logging
import os
from waitress import serve

app = Flask(__name__)
app.debug = True  # 启用调试模式

# Logging configuration
logging.basicConfig(filename='server.log', level=logging.DEBUG)

# Load questions from a JSON file
def load_questions():
    file_path = 'questions_corrected.json'
    logging.debug(f"Loading questions from: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            questions = json.load(file)
            logging.debug("Questions successfully loaded")
            return questions
    except FileNotFoundError:
        logging.error(f"{file_path} not found")
        return None
    except Exception as e:
        logging.error(f"Error loading questions: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questions_corrected.json')
def questions():
    return send_from_directory(os.getcwd(), 'questions_corrected.json')

@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.json
    logging.debug(f"User answers: {user_answers}")

    questions = load_questions()
    if not questions:
        return jsonify({"score": 0}), 404

    total_score = 0
    single_choice_score = 0
    multiple_choice_score = 0
    true_false_score = 0
    fill_in_the_blank_score = 0
    case_analysis_score = 0

    # Score fill-in-the-blank questions (2 points each)
    for i, question in enumerate(questions['fill_in_the_blank']):
        for j, correct_answer in enumerate(question['answers']):
            user_answer = user_answers.get(f'fill_in_the_blank_{i}_{j}', '').strip()
            if user_answer == correct_answer:
                if i == 4:  # Special case for question 5 with 3 parts
                    fill_in_the_blank_score += 0.7  # Each part of question 5 is worth 0.7 points
                else:
                    fill_in_the_blank_score += 2
            logging.debug(f"Fill in the blank question {i}_{j}: user_answer='{user_answer}', correct_answer='{correct_answer}', score={fill_in_the_blank_score}")

    logging.debug(f"Fill in the blank score: {fill_in_the_blank_score}")

    # Score single choice questions (2 points each)
    for i, question in enumerate(questions['single_choice']):
        correct_answer = question['answer']
        user_answer = user_answers.get(f'single_choice_{i}', '')
        if user_answer == correct_answer:
            single_choice_score += 2
        logging.debug(f"Single choice question {i}: user_answer='{user_answer}', correct_answer='{correct_answer}', score={single_choice_score}")

    logging.debug(f"Single choice score: {single_choice_score}")

    # Score multiple choice questions (2 points each)
    for i, question in enumerate(questions['multiple_choice']):
        correct_answers = set(question['answer'])
        user_answers_set = set(user_answers.get(f'multiple_choice_{i}', []))
        if user_answers_set == correct_answers:
            multiple_choice_score += 2
        logging.debug(f"Multiple choice question {i}: user_answers_set='{user_answers_set}', correct_answers='{correct_answers}', score={multiple_choice_score}")

    logging.debug(f"Multiple choice score: {multiple_choice_score}")

    # Score true/false questions (1 point each)
    for i, question in enumerate(questions['true_false']):
        correct_answer = question['answer']
        user_answer = user_answers.get(f'true_false_{i}', '')
        if user_answer == correct_answer:
            true_false_score += 1
        logging.debug(f"True/false question {i}: user_answer='{user_answer}', correct_answer='{correct_answer}', score={true_false_score}")

    logging.debug(f"True/false score: {true_false_score}")

    # Score case analysis question (10 points total)
    case_analysis_answer = user_answers.get('case_analysis_0', '').strip()
    key_points = ['确认地址', '使用二维码', '小额测试', '使用官方渠道', '双重确认']
    correct_points = sum(1 for point in key_points if point in case_analysis_answer)
    case_analysis_score = (correct_points / len(key_points)) * 10
    logging.debug(f"Case analysis answer: '{case_analysis_answer}', correct_points={correct_points}, score={case_analysis_score}")

    logging.debug(f"Case analysis score: {case_analysis_score}")

    # Sum total score
    total_score = fill_in_the_blank_score + single_choice_score + multiple_choice_score + true_false_score + case_analysis_score
    total_score = round(total_score, 1)  # Round to 1 decimal place
    logging.debug(f"Total score: {total_score}")

    return jsonify({"score": total_score})

if __name__ == '__main__':
    logging.debug("Starting the server using waitress")
    serve(app, host='0.0.0.0', port=8000)
