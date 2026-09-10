import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Game


class GameRoom(WebsocketConsumer):
    def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'room_{self.room_code}'

        if self.channel_layer:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name,
            )

        self.accept()

    def disconnect(self, code):
        if self.channel_layer:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name,
            )

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'move':
            room_code = self.room_code
            game = Game.objects.filter(room_code=room_code).first()
            if not game:
                return

            username = data.get('username', '')
            row = int(data.get('row'))
            col = int(data.get('col'))
            mark = 'X' if username == game.game_creator else 'O'

            index = row * 3 + col
            board = list(game.board)
            if board[index] != '-':
                self.send(text_data=json.dumps({'event': 'invalid_move'}))
                return

            board[index] = mark
            game.board = ''.join(board)
            game.current_turn = game.game_opponent if username == game.game_creator else game.game_creator
            game.winner = self.calculate_winner(game.board)
            game.is_over = bool(game.winner)
            game.save()

            payload = {
                'event': 'game_state',
                'room_code': room_code,
                'board': game.board,
                'current_turn': game.current_turn,
                'winner': game.winner,
                'is_over': game.is_over,
                'username': username,
                'row': row,
                'col': col,
            }

            if self.channel_layer:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'run_game',
                        'payload': json.dumps(payload),
                    },
                )

    def run_game(self, event):
        payload = event.get('payload')
        self.send(text_data=payload)

    def calculate_winner(self, board):
        lines = [
            board[0:3], board[3:6], board[6:9],
            board[0] + board[3] + board[6],
            board[1] + board[4] + board[7],
            board[2] + board[5] + board[8],
            board[0] + board[4] + board[8],
            board[2] + board[4] + board[6],
        ]

        for line in lines:
            if line == 'XXX':
                return 'X'
            if line == 'OOO':
                return 'O'

        if '-' not in board:
            return 'draw'

        return ''
