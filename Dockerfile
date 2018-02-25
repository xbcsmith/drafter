FROM python:2.7
COPY requirements.txt /players/requirements.txt
COPY drafter.py  /players/drafter.py
COPY players.json  /players/players.json
COPY ./templates/players.html /players/templates/players.html
COPY ./templates/draft.html /players/templates/draft.html
COPY ./templates/list.html /players/templates/list.html
COPY ./templates/rounds.html /players/templates/rounds.html
COPY ./templates/teams.html /players/templates/teams.html
WORKDIR /players
RUN pip install -r requirements.txt
