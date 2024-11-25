# Created by prisca olose on 10/16/23.

import json
import openai

# Read key from a text file
def read_text_key(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

api_key = read_text_key('text.txt')
openai.api_key = api_key

# Load knowledge base from a JSON file
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
        return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str or None:
    for question in questions:
        if question.lower() == user_question.lower():
            return question
    return None

def get_answer_for_question(question: str, knowledge_base: dict) -> str or None:
    for q in knowledge_base["questions"]:
        if q["question"].lower() == question.lower():
            return q["answer"]
    return None

def get_ChatGPT_answer(question):
    response = openai.Completion.create(
        engine="davinci-002",
        prompt=f"Q: {question}\nA:",
        max_tokens=200,  # to limit the response length
        stop=["\n"] # stop sequence to end the response at the first newline
    )
    answer = response.choices[0].text.strip()
    return answer

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        best_match: str = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            answer = get_ChatGPT_answer(user_input)
            print(f'Bot: {answer}')
            knowledge_base["questions"].append({"question": user_input, "answer": answer})
            save_knowledge_base('knowledge_base.json', knowledge_base)
            print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    chat_bot()
