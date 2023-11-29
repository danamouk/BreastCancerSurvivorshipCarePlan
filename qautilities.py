import requests
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, QuestionAnsweringPipeline
import torch
import torch.nn.functional as F
import pandas as pd

#######################################################################################################

def cool_function(x):
    """
    Print a message and the specified argument.

    Parameters:
    - x (any): The input argument.
    """
    print("Hey, this is a cool function")
    print(f"Here's the argument you specified: {x}")

def call_cool_function(x):
    """
    Call the cool_function with the specified argument.

    Parameters:
    - x (any): The input argument.
    """
    cool_function(x)

def requests_something(x):
    """
    Make a GET request to 'http://python.org'.

    Parameters:
    - x (any): Placeholder argument (not used).

    Returns:
    - requests.Response: The response object from the GET request.
    """
    response = requests.get('http://python.org')
    return response

#######################################################################################################


def get_answer(question, passage_dict, title_dict, tokenizer, model):
    """
    Get the answer to a question from a passage.

    Parameters:
    - question (str): The question.
    - passage_dict (dict): Dictionary with 'paper_id' and 'passage_text'.
    - title_dict (dict): Dictionary with paper_id as keys and paper titles as values.
    - tokenizer (transformers.AutoTokenizer): Tokenizer for encoding inputs.
    - model (transformers.AutoModelForQuestionAnswering): Question answering model.

    Returns:
    - dict: A dictionary containing answer-related information.
    """
    text = passage_dict['passage_text'][:1000]
    paper_id = passage_dict['paper_id']

    inputs = tokenizer.encode_plus(question, text, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]

    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    answer_start_scores, answer_end_scores = model(**inputs)

    answer_start = torch.argmax(answer_start_scores)
    answer_end = torch.argmax(answer_end_scores) + 1

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

    start_confidence = F.softmax(torch.tensor(answer_start_scores), dim=1).cpu().detach().numpy()[0].max()
    end_confidence = F.softmax(torch.tensor(answer_end_scores), dim=1).cpu().detach().numpy()[0].max()
    score = (start_confidence + end_confidence) / 2

    if (answer.startswith('[CLS]')) or (answer == ''):
        score = 0

    output = {
        'paper_id': passage_dict['paper_id'],
        'paper_title': title_dict[paper_id],
        'question': question,
        'answer': answer,
        'score': score,
        'passage': text
    }

    return output

def answer_df(question_answers):
    """
    Create a DataFrame from a list of question-answering results.

    Parameters:
    - question_answers (list): List of dictionaries containing question-answering results.

    Returns:
    - pd.DataFrame: A DataFrame sorted by score in descending order.
    """
    df = pd.DataFrame(question_answers).sort_values(by='score', ascending=False)
    return df

def answer_from_text(question, text_data, title_dict, tokenizer, model):
    """
    Get answers to a question from a list of passages.

    Parameters:
    - question (str): The question.
    - text_data (list): List of passage dictionaries.
    - title_dict (dict): Dictionary with paper_id as keys and paper titles as values.
    - tokenizer (transformers.AutoTokenizer): Tokenizer for encoding inputs.
    - model (transformers.AutoModelForQuestionAnswering): Question answering model.

    Returns:
    - list: List of dictionaries containing answer-related information.
    """
    answer_outputs = []
    for passage_dict in text_data:
        result = get_answer(question, passage_dict, title_dict, tokenizer, model)
        answer_outputs.append(result)
    return answer_outputs
