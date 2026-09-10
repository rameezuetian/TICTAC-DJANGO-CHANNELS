# Tic-Tac-Toe Django Channels Project

A simple Django Channels tic-tac-toe room app with a lobby page and a live play page.

## Features

- Create a room
- Join an existing room
- Play tic-tac-toe through a websocket room
- Room state persisted in Django model storage

## Required packages

```sh
pip install django==6.0.4 channels==4.3.2 daphne==4.2.3
```

## Run locally

From the project root:

```sh
cd e:\django_main\TIC TAC\home
set DJANGO_SETTINGS_MODULE=home.settings
python -m daphne home.asgi:application -b 127.0.0.1 -p 8000
```

Then open:

```text
http://127.0.0.1:8000/
```
