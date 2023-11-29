#!/usr/bin/env python
# coding: utf-8

from lib.good_stuff import call_cool_function
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, QuestionAnsweringPipeline
from lib.qautilities import answer_df, answer_from_text
import json
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt

# Example template
call_cool_function("this is a dumb function ....")

# Pre-trained model
tokenizer = AutoTokenizer.from_pretrained("ktrapeznikov/biobert_v1.1_pubmed_squad_v2")
model = AutoModelForQuestionAnswering.from_pretrained("ktrapeznikov/biobert_v1.1_pubmed_squad_v2")
nlp = QuestionAnsweringPipeline(model=model, tokenizer=tokenizer)

# Read Json
with open('all-papers.json', "r") as f:
    all_papers = json.load(f)

# title_dict and text_data
title_list_02 = []
text_data_02 = []

for paper in all_papers:
    complete_title = ''
    complete_abstract = ''
    paper_id = paper['id']
    
    for ps in paper['passages']:
        try:
            if ps['infons']['section_type'] == 'TITLE':
                complete_title += ' '
                complete_title += ps['text']
            elif ps['infons']['type'] == 'abstract':
                complete_abstract += ' '
                complete_abstract += ps['text']
        except:
            pass
    
    title_dict[paper_id] = complete_title
    passage_dict_title = {'paper_id': paper_id, 'title': complete_title}
    passage_dict_text = {'paper_id': paper_id, 'passage_text': complete_abstract}
    
    title_list_02.append(passage_dict_title)
    text_data_02.append(passage_dict_text)

# Answer from text
for question in ['Which group developed a clinical practice guideline?',
                 'Which type of breast-cancer is most affected?',
                 'What recommendation do you give to stage 1 versus stage 2 cancer patients?',
                 'How does a survivorship plan look like for a stage 3 cancer patient?',
                 'How is the patient engagement rated in the cancer survivorship plans?']:
    result_answer = answer_from_text(question, text_data_02, title_dict, tokenizer, model)
    df = answer_df(result_answer)
    display(df.head())
    plt.figure()
    df['score'].plot.hist()

# Follow-up question
result_answer = answer_from_text('Why is the elderly population most susceptible to breast cancer?', text_data_02, title_dict, tokenizer, model)
df = answer_df(result_answer)
display(df.head())
plt.figure()
df['score'].plot.hist()
