from django.db import models


class Game(models.Model):
    room_code = models.CharField(max_length=100, unique=True)
    game_creator = models.CharField(max_length=100)
    game_opponent = models.CharField(max_length=100, blank=True, null=True)
    board = models.CharField(max_length=9, default='---------')
    current_turn = models.CharField(max_length=100, default='')
    winner = models.CharField(max_length=100, blank=True, null=True)
    is_over = models.BooleanField(default=False)

    def get_board_list(self):
        return list(self.board)

    def set_board_list(self, values):
        self.board = ''.join(values)

    def __str__(self):
        return self.room_code
