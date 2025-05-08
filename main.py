import json
from flask import Flask, render_template, request,session
from flask_session import Session

# Configure application
app = Flask(__name__)
# Enable session for tracking user score
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
#style options
style_options = ["light", "dark", "disco"]

@app.route("/", methods=["GET", "POST"])
def index():
	#load questions from JSON file
	with open("questions.json") as file:
		data = json.load(file)
		
	# count the number of questions
	session["question_count"] = len(data["questions"])
			
	if request.method == "GET": # this is the initial load of the site
		session["question"] = 0
		session["correct"] = 0
		session["answer_given"] = "None"
		session["correct_answer"] = ""
		if session.get("style_choice") == None:
			session["style_choice"] = style_options[0]
	elif request.method == "POST":
		#get answer
		session["answer_given"] = request.form.get("answer")
		#get style
		session["style_choice"] = request.form.get("style_choice")
		
		# get correct answer for current question being submitted
		session["correct_answer"] = data["questions"][session["question"]]["answer"]
		
		# if answer matches the answer in JSON file then increment score
		if(session["correct_answer"] == session["answer_given"]):
			session["correct"] = session["correct"] + 1

		# move to next question
		session["question"] = session["question"] + 1
	
	# load next question (if there are more left)
	if session["question"] < session["question_count"]:
		next_q = data["questions"][session["question"]]
		return render_template("index.html", question=next_q, options=style_options)
	# redirect to end page 
	else:
		return render_template("final.html", questions=data["questions"])

# test page for streetview, go to the URL /test on your app to load this page
@app.route("/test")
def test():
	#load questions from JSON file
	with open("questions.json") as file:
		data = json.load(file)
	return render_template("test.html", questions=data["questions"])
	
app.run(host='0.0.0.0', port=8080)