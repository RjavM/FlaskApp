from flask import Flask, render_template, request, jsonify, redirect, url_for
import openai 
import time
import csv


app = Flask(__name__)

USERS_FILE = "database/data.csv"

# Replace with your OpenAI API key
# openai.api_key = 

# Store chat messages in memory
chat_history = {}
username = ""
password = ""
# @app.route("/logintrial", methods = ["GET", "POST"])
# def logintrial():
#     if request.method == "POST":
#         user_message = request.form['message']
#         return render_template('trail.html', messages = user_message)
    
    # else:
    #     return "<h1>nope</h1>"
    
@app.route("/", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        global username, password
        username = request.form["username"]
        password = request.form["password"]
        with open(USERS_FILE, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and username == row[0] and password == row[1]:
                    if username not in chat_history:
                        chat_history[username] = [] 
                    return redirect(url_for('chat'))
        return render_template("login.html", message="Invalid credentials")
    return render_template("login.html")

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    global username, password
    user = username
    if request.method == "POST":
        username = ""
        password = ""
        return redirect(url_for('login'))
    return render_template("logout.html", message = user)

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if (password1 != password2):
            return render_template("signup.html", message = "Entered passwords don't match up")
        with open(USERS_FILE, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and username == row[0]:
                    return render_template("login.html", message="Username already exists, please login here")
        
        # Write new user to CSV file
        with open(USERS_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password1])

        return redirect(url_for('login'))
    
    return render_template("signup.html")


@app.route("/info", methods=["GET", "POST"])
def index():
    return render_template('info.html')

@app.route("/chat", methods=["GET", "POST"])
def chat():
    global chat_history
    if request.method == "POST":
        user_message = request.form['message']
        chat_history[username].append({'sender': 'user', 'text': user_message})

        try:
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=user_message,
                max_tokens=150
            )
            bot_message = response.choices[0].text.strip()
            chat_history[username].append({'sender': 'bot', 'text': bot_message})
        except Exception as e:
            chat_history[username].append({'sender': 'bot', 'text': str(e)})

    return render_template('bot.html', messages=chat_history[username])

if __name__ == '__main__':
    app.run(debug=True)



# @app.route("/chat", methods=["GET", "POST"])
# def chat():
#     global chat_history
#     if request.method == "POST":
#         user_message = request.form['message']
#         chat_history.append({'sender': 'user', 'text': user_message})

#         try:
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": user_message}
#                 ]
#             )
#             bot_message = response.choices[0].message['content'].strip()
#             chat_history.append({'sender': 'bot', 'text': bot_message})
#         except Exception as e:
#             chat_history.append({'sender': 'bot', 'text': str(e)})

#     return render_template('bot.html', messages=chat_history)

# if __name__ == '__main__':
#     app.run(debug=True)