from bs4 import BeautifulSoup
import pprint
import json

# Constants
HTML_FILE_PATH = './data.html'
QUESTION_CLASS = 'qtext'
ANSWER_CLASS = 'answer'
CORRECT_ANSWER_CLASS = 'correct'
ODD_ROW_CLASS = 'r0'
EVEN_ROW_CLASS = 'r1'
JSON_OUTPUT_FILE = 'questions.json'

def read_html(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def extract_questions(soup):
    questions_soup = soup.find_all(class_=QUESTION_CLASS)
    questions = []

    for question in questions_soup:
        text_question = question.find("span")
        questions.append(text_question.text.strip() if text_question else question.text.strip())

    return [" ".join(question.strip().replace("\n", "").split()) for question in questions]

def extract_answers(soup):
    answers_soup = soup.find_all(class_=ANSWER_CLASS)
    all_answers = []
    all_correct_answers = []

    for answer in answers_soup:
        correct_answer = answer.find(class_=CORRECT_ANSWER_CLASS)
        if correct_answer:
            all_correct_answers.append(correct_answer.text.strip())

        q_all_answers = answer.find_all(class_=ODD_ROW_CLASS)
        q_all_answers.extend(answer.find_all(class_=EVEN_ROW_CLASS))

        all_answers.append([q.text.strip().replace("\n", "") for q in q_all_answers])



    return (
        [[answer.strip().replace("\n", "") for answer in answers] for answers in all_answers],
        [answer.strip().replace("\n", "") for answer in all_correct_answers]
    )

def create_question_dict_list(questions, all_answers, all_correct_answers):
    question_dict_list = []

    for i in range(len(questions)):
        question_dict = {
            'question': questions[i],
            'answers': all_answers[i],
            'correct_answer': all_correct_answers[i]
        }
        question_dict_list.append(question_dict)

    return question_dict_list

def export_to_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def main():
    html_content = read_html(HTML_FILE_PATH)
    soup = BeautifulSoup(html_content, 'html.parser')

    questions = extract_questions(soup)
    all_answers, all_correct_answers = extract_answers(soup)

    question_dict_list = create_question_dict_list(questions, all_answers, all_correct_answers)

    pprint.pprint(question_dict_list)

    export_to_json(question_dict_list, JSON_OUTPUT_FILE)
    print(f'Data exported to {JSON_OUTPUT_FILE}')

if __name__ == "__main__":
    main()