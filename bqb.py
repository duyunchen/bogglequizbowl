#!/usr/bin/env python

#  This file is part of Boggle Quiz Bowl.
# 
#     Boggle Quiz Bowl is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Foobar is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
    
# Import flask
from flask import Flask, render_template
from flask import request, session, redirect, url_for, flash
app = Flask(__name__)

app.secret_key = "0\x9f\xfe\xfd.Q\x90X\xf4\xaf\x9e[\xf6\xcb\x9e\xba\x18\xc3\xe0\xdd\xd0f\xeb\xda"

# Add the bin folder to PYTHONPATH
import os, sys
sys.path.append(os.path.abspath("./bin"))

# Import all our modules
from Player import Player
from Board import Board
import PlayerService
import LoginService
import BoardService
import SolverService
import QuestionService
import JsonService
import FileService
import SQLiteDB as db

# This initializes the application, DB, etc
def init():
    db.init_db()

# This handles the game screen after authentication
@app.route("/", methods=["GET"])
def home():
    username = session.get("username")
    player = PlayerService.get_player(username)
    return render_template("home.html", player=player)

@app.route("/getTemplate", methods=["GET"])
def get_template():
    return render_template(request.args.get("filename", ""))

# This checks if the user is already logged in
@app.route("/isLoggedIn", methods=["GET"])
def is_logged_in():
    if "username" in session:
        username = session.get("username").strip()
        player = PlayerService.get_player(username)
        
        if not player: 
            PlayerService.insert_player(username)
            player = PlayerService.get_player(username)
        
        return JsonService.jsonify(player)
    else:
        return JsonService.jsonify({})

# This lists all the players in the DB (excluding guest and debug players)
@app.route("/list", methods=["GET"])
def list_players():
    players = PlayerService.list()
    return JsonService.jsonify(players)
    
# This checks user authentication info
@app.route("/login", methods=["POST"])
def checkLogin():
    username = request.form["username"].strip().lower()
    valid = LoginService.check_auth(username,
                       request.form["password"])
    if valid:
        session["username"] = username
        return JsonService.jsonify({valid : True})
    else:
        return JsonService.jsonify({valid : False})

@app.route("/updateHighscore", methods=["POST"])
def updateHighscore():
    username = request.form["username"].strip().lower()
    highscore = request.form["highscore"]
    
    player = PlayerService.get_player(username)
    if player and highscore > player.highscore:
        player.highscore = highscore
        PlayerService.update_player(player)
    
    return JsonService.jsonify({})
    
@app.route("/getQuestion", methods=["GET"])
def getQuestion():
    question = QuestionService.generate_question()
    return JsonService.jsonify(question)
    
# This gets a randomly generated board
@app.route("/getBoard", methods=["GET"])
def getBoard():
    board = BoardService.generate_board()
    return board.letters.upper()

# This gets a randomly generated board
@app.route("/solveBoard", methods=["GET"])
def solveBoard():
    letters = request.args.get("board", None).strip()
    print type(letters)
    print len(letters) 
    if letters is None or type(letters) is not unicode or len(letters) is not 16: 
        return "Please specific board as a 16 letter GET parameter \"board\""
    solutions = SolverService.find_words(Board(letters=letters.lower()))
    wordlist = [solution.word for solution in solutions]
    wordset = set(wordlist)
    finallist = "".join(word.upper() + "<br />" for word in wordset)
    return finallist

# This gets the dictionary
@app.route("/getDict", methods=["GET"])
def getDictionary():
    return JsonService.jsonify(FileService.read_dictionary())

# This logs the user out
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop("username", None)
    return redirect(url_for("home"))

@app.errorhandler(500)
def internal_error(exception):
    return render_template('500.html', exception = exception), 500

if __name__ == "__main__":
    from Config import DEBUG
    app.run(debug = DEBUG)
