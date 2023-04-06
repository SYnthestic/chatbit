import random
import os
import json
import pickle
import numpy as np
import sys


# Email
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.message import EmailMessage


import nltk
from nltk.stem import WordNetLemmatizer

import pandas as pd

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
# intents = json.loads(open(r'intents.json').read())
intents = json.loads(open(r'C:\Users\sam75\OneDrive - Singapore Polytechnic\SP\Y3\Intern\Work\Chatbox\chatbit\application\intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
# model = load_model("chatbot_model.h5")
model = load_model(r"C:\Users\sam75\OneDrive - Singapore Polytechnic\SP\Y3\Intern\Work\Chatbox\chatbit\chatbot_model.h5")


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res)]
    
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json, message):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
        # if (tag == 'send feedback' or tag == 'positive feedback' or tag == 'complain'):
        #     entry = False
        #     while entry != True:
        #         nameEntry = False
        #         emailEntry = False
        #         issueEntry = False
        #         while nameEntry == False:
        #             name = input("Input your name: ")
        #             if name.isnumeric() == True:
        #                 print("Error! Names cannot have numbers in them")
        #             elif name == ' ' or name == '' or name == None:
        #                 print("Error! Names cannot be null")
        #             else:
        #                 nameEntry = True
        #         while emailEntry == False:
        #             email = input("Input your email: ")
        #             if '@' not in email:
        #                 print("Error! Emails must have @")
        #             elif email == ' ' or email == '' or email == None:
        #                 print("Error! Names cannot be null")
        #             elif '.com' not in email:
        #                 print("Error! Emails must end with .com[.xxx]")
        #             else:
        #                 emailEntry = True
        #         while issueEntry == False:
        #             issue = input("Input your issue: ")
        #             if issue == ' ' or issue == '' or issue == None:
        #                 print("Error! Issues cannot be null")
        #             else:
        #                 issueEntry = True
        #         entry = True
        #     # Get user feedback and email address
        #     EMAILADR = os.environ.get('EMAIL_USER')
        #     EMAILPW = os.environ.get('EMAIL_PASS')
        #     # EMAILADR = 'samuelyam953@gmail.com'
        #     # EMAILPW = 'TIB1108A'
        #     feedback = issue
        #     receiver = email

        #     # # Create email message
        #     msg = EmailMessage()
        #     msg['Subject'] = "Feedback on our service"
        #     msg['From'] = EMAILADR
        #     msg['To'] = receiver
        #     msg.set_content(feedback)
            
        #     # context = ssl.create_default_context()
            
        #     # Connect to SMTP server and send email
        #     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        #         print(EMAILADR)
        #         print(EMAILPW)
                
        #         # smtp.ehlo()
        #         # smtp.starttls()
        #         # smtp.ehlo()
                
        #         smtp.login(EMAILADR, EMAILPW)
                
                
        #         subject = 'Feedback at QueueCut'
        #         body = issue
        #         msg = (f'Subject: {subject}\n\n{body}')
                
        #         smtp.send_message(msg)
                
        #         smtp.sendmail(EMAILADR, receiver, msg.as_string())
            
            
            
                
                
                
    return result
print("QueueCutBot is running!")
a = None
# def generate_reply(input_text):
#     if 'hello' in input_text:
#         return 'Hi, how can I help you?'
#     elif 'goodbye' in input_text:
#         return 'Goodbye!'
#     else:
#         return 'Sorry, I did not understand your question.'

while True:
    message = input("Input: ")
    ints = predict_class(message)
    res = get_response(ints, intents, message)
    print(res)
    