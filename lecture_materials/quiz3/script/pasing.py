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

def clean_text(text):
    """Remove new lines and extra spaces from the text."""
    return " ".join(text.strip().replace("\n", "").split())

def read_html(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def extract_questions(soup):
    questions_soup = soup.find_all(class_=QUESTION_CLASS)
    questions = []

    for question in questions_soup:
        text_question = question.find("span")
        questions.append(text_question if text_question else question)
    
    # Remove new lines and extra spaces
    questions = [clean_text(question.text) for question in questions]

    return questions

def extract_choices(soup):
    choices_soup = soup.find_all(class_=ANSWER_CLASS)

    all_questions_choices = []

    for choices in choices_soup:
        choice_elements = choices.find_all(class_=ODD_ROW_CLASS) + choices.find_all(class_=EVEN_ROW_CLASS)
        formatted_choices = [clean_text(choice.text) for choice in choice_elements]
        all_questions_choices.append(formatted_choices)

    return [[clean_text(answer) for answer in answers] for answers in all_questions_choices]

def extract_correct_choices(soup):
    choices_soup = soup.find_all(class_=ANSWER_CLASS)
    all_questions_correct_choice = []

    for choices in choices_soup:
        correct_answer = choices.find(class_=CORRECT_ANSWER_CLASS)
        if correct_answer:
            all_questions_correct_choice.append(correct_answer.text)

    return [clean_text(answer) for answer in all_questions_correct_choice]

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
    all_answers = extract_choices(soup)
    all_correct_answers = extract_correct_choices(soup)

    question_dict_list = create_question_dict_list(questions, all_answers, all_correct_answers)

    pprint.pprint(question_dict_list)

    export_to_json(question_dict_list, JSON_OUTPUT_FILE)
    print(f'Data exported to {JSON_OUTPUT_FILE}')

if __name__ == "__main__":
    main()