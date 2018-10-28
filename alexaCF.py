from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
from pushbullet import Pushbullet

pb = Pushbullet('o.ecIJUMq4TRVdkrU83tTEeSoXk7cVyppp')

app = Flask(__name__)
ask = Ask(app, "/codeforces_contest")

def get_contest():
	x=""
	response = requests.get('http://codeforces.com/api/contest.list')
	data = response.json()['result']
	for i in range(1,6):
		x = x+"#"+str(i)+". "+data[i-1]['name']+"... "
	return x

def send_me():
	x=""
	response = requests.get('http://codeforces.com/api/contest.list')
	data = response.json()['result']
	for i in range(1,6):
		x = x+"#"+str(i)+". "+data[i-1]['name']+'\n'
	push = pb.push_note("Codeforces Contests", x)
	return "I have sent it. You can check it now."

@app.route('/')
def homepage():
	return "Working"

@ask.launch
def start_skill():
	welcome_message = 'What do you want to know in Codeforces'
	print welcome_message
	return question(welcome_message)

@ask.intent("ContestIntent")
def Contest():
	contest_data=get_contest()
	return statement(contest_data)

@ask.intent("SendIntent")
def Contest():
	contest_data=send_me()
	return statement(contest_data)

@ask.intent("NoIntent")
def no_intent():
	bye_text = "Get lost, why did you even wake me up"
	return statement(bye_text)




if __name__ == '__main__':
	app.run(debug = True)