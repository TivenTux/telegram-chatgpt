import os
from os import environ
import requests
import re
import json
import telebot
import openai

## configuration ##
#use number 1 for openAI or 2 for custom api
if environ.get('aiselection') is not None:
    aiselection = os.environ['aiselection']
else:
    aiselection = 1

#ChatGPT / openAI settings
if environ.get('openaikey') is not None:
    openaikey = os.environ['openaikey']
else:
    openaikey = ''

#locally hosted LLM settings - ignore this section if you are using ChatGPT / OpenAI
#aihost = '127.0.0.1:5000'
if environ.get('aihost') is not None:
    aihost = os.environ['aihost']
else:
    aihost = '127.0.0.1:5000'
aiurl = f'http://{aihost}/api/v1/generate'

#telegram settings
if environ.get('telegram_bot_token') is not None:
    telegram_bot_token = os.environ['telegram_bot_token']
else:
    telegram_bot_token = ''

if environ.get('bot_nickname') is not None:
    bot_nickname = os.environ['bot_nickname']
else:
    bot_nickname = 'yyyy'

if environ.get('bot_keyword') is not None:
    bot_keyword = os.environ['bot_keyword']
else:
    bot_keyword = ''

#Option to give the user's first name to the bot. Enable with 1, disable with 0.
#Default enabled.
if environ.get('pass_author') is not None:
    pass_author = os.environ['pass_author']
else:
    pass_author = 1

#initiate some vars
totalaierrors = 0
bot = telebot.TeleBot(telegram_bot_token)
keywordlen = len(bot_keyword)

#remove any special characters from user name
def cleanupname(datainput):
    cleanedupname=re.sub("[^A-Za-z]","",datainput)
    cleanedupname = cleanedupname[0].upper() + cleanedupname[1:]
    return (cleanedupname)

#pass and process all messages through here
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    messagelen = len(message.text)
    #check for keyword and for total message length over 11 chars
    if (message.text).upper().startswith(bot_keyword.upper()) and messagelen > 11:
        #finding user's first name, because not every user sets a username
        try:
            usern = message.from_user.first_name
        except Exception as e:
            print(e)
            usern = 'User'
        aiquestion = message.text[keywordlen:]
        #check for option in conf
        if int(pass_author) == 1:
            finprompt1 = "Below is a conversation between a user named " + usern + " and an AI assistant named " + bot_nickname + ".\n" + bot_nickname + " was made by Tiven and provides helpful answers.\n" + usern + ": "
        elif int(pass_author) == 0:
            finprompt1 = "Below is a conversation between a user and an AI assistant named " + bot_nickname + ".\n" + bot_nickname + " was made by Tiven and provides helpful answers.\n" + "User: "
        aifinal_question = finprompt1 + aiquestion + "\n" + bot_nickname + ":"
        #send prompt to AI depending on ai selection option
        if int(aiselection) == 1:
            finalresponse = aiprocess1(aifinal_question)
        elif int(aiselection) == 2:
            finalresponse = aiprocess2(aifinal_question, message)
        bot.reply_to(message, finalresponse)

    return

#chatGPT/openAI - default option
def aiprocess1(aifinal_question):
    try:
        openai.api_key = openaikey
        response = openai.Completion.create(
            model="text-davinci-003", #available models here: https://platform.openai.com/docs/models/overview
            prompt=aifinal_question,
            temperature=0.5,
            max_tokens=485,
            top_p=0.4,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            stop=[" \n"]
            )

        json_data2 = json.dumps(response.choices)
        aianswer = json.loads(json_data2)
        print(aianswer[0]["text"])
    except Exception as e:
        print(e)
        print("error aiprocess1")
        return "nope"
    return aianswer[0]["text"]

#locally hosted LLM
def aiprocess2(aifinal_question, aifinal_questionoriginal):
    global totalaierrors
    request = {
        'prompt': aifinal_question,
        'max_new_tokens': 540,
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.5,
        'top_p': 0.5,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'repetition_penalty_range': 0,
        'top_k': 20,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }
    try:
        response = requests.post(aiurl, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            print(aifinal_question)
            print(result)
    except Exception as e:
        print(e)
        print("error aiprocess2")
        totalaierrors += 1
        return "nope"
    return result

#keeps the process running until stopped
bot.infinity_polling()