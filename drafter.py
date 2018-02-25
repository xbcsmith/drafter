import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import datetime
import json

app = Flask(__name__, template_folder='/players/templates')

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)

db = client.playersdb

try:
    PLAYERS = json.load(open('/players/players.json'))
except Exception as e:
    raise e

@app.route('/')
def draft():
    _teams = db.teamsdb.find()
    teams = [ team for team in _teams ]
    _items = db.playersdb.find()
    drafted = [item for item in _items]
    drafted = sorted(drafted, key=lambda x: x['round'])
    drafted.reverse()
    players = sorted(PLAYERS)
    items = dict(drafted=drafted,players=players,teams=teams)
    return render_template('draft.html', items=items)

@app.route('/rounds')
def rounds():
    rounds = {}
    items = []
    _items = db.playersdb.find()
    _items = [item for item in _items]
    for info in _items:
        rounds.setdefault(info['round'], []).append(info)
    for _round, players in rounds.items():
        items.append(dict(round=_round,players=players))
    return render_template('rounds.html', items=items)


@app.route('/players')
def players():
    _items = db.playersdb.find()
    items = [item for item in _items]
    items = sorted(items, key=lambda x: x['name'])
    return render_template('players.html', items=items)

@app.route('/list')
def list():
    items = sorted(PLAYERS)
    return render_template('list.html', items=items)

@app.route('/teams')
def teams():
    _items = db.teamsdb.find()
    items = [item for item in _items]
    items = sorted(items, key=lambda x: x['order'])
    return render_template('teams.html', items=items)

@app.route('/addteam', methods=['POST'])
def addteam():
    item_doc = {
        'name': request.form['name'],
        'captain': request.form['captain'],
        'order': request.form['order'],
        'date' : datetime.datetime.utcnow(),
    }
    db.teamsdb.insert_one(item_doc)
    return redirect(url_for('teams'))

@app.route('/removeteam', methods=['POST'])
def removeteam():
    item_doc = {
        'name': request.form['name'],
    }
    db.teamsdb.delete_many(item_doc)
    return redirect(url_for('teams'))

@app.route('/new', methods=['POST'])
def new():
    item_doc = {
        'name': request.form['name'],
        'team': request.form['team'],
        'round': request.form['round'],
        'date' : datetime.datetime.utcnow(),
    }
    db.playersdb.insert_one(item_doc)
    return redirect(url_for('draft'))

@app.route('/remove', methods=['POST'])
def remove():
    item_doc = {
        'name': request.form['name'],
    }
    db.playersdb.delete_many(item_doc)
    return redirect(url_for('draft'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
