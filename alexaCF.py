from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
from pushbullet import Pushbullet
from datetime import datetime

pb = Pushbullet('o.ecIJUMq4TRVdkrU83tTEeSoXk7cVyppp')

app = Flask(__name__)
ask = Ask(app, "/codeforces_contest")

def get_contest():
	x=""
	response = requests.get('http://codeforces.com/api/contest.list')
	data = response.json()['result']
	for i in range(1,len(data)):
		if(data[i]['phase']=='BEFORE')
			x = x+"#"+str(i)+". "+data[i-1]['name']+"... "
		else:
			break
	return x

def send_me():
	x=""
	response = requests.get('http://codeforces.com/api/contest.list')
	data = response.json()['result']
	for i in range(1,len(data)):
		if(data[i]['phase']=='BEFORE'):
			x = x+"#"+str(i)+". " + data[i]['name'] + '\n' + datetime.utcfromtimestamp(data[i]['startTimeSeconds']).strftime('%H:%M %d-%m-%Y')+'\n'

		if(data[i]['phase']=='FINISHED'):
			break
	push = pb.push_note("Codeforces Contests", x)
	return "I have sent it. You can check it now."

@app.route('/')
def homepage():
	return "Working"

@ask.launch
def start_skill():
	welcome_message = 'What do you want to know in Codeforces?'
	print welcome_message
	return question(welcome_message)

@ask.intent("ContestIntent")
def Contest():
	contest_data=get_contest()
	return statement(contest_data)

@ask.intent("SendIntent")
def Contest():
	sent_confirmation=send_me()
	return statement(sent_confirmation)

@ask.intent("NoIntent")
def no_intent():
	bye_text = "Thank You for wasting my time. Get Lost."
	return statement(bye_text)




if __name__ == '__main__':
	app.run(debug = True)
