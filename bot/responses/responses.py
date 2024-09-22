import json


def load_responses(file_path):
    with open(file_path, encoding='utf-8') as file:
        responses = json.load(file)
    return responses


responses = load_responses('bot/responses/public_responses.json')
