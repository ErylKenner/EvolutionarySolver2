import numpy as np


class TicTacToe(object):
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = np.zeros(shape=(3, 3))
        self.winner = 0

    def play_game(self):
        player = self.player1
        while True:
            player_board = self.board_to_player_perspective(player.board_value)
            move = player.make_move(player_board)
            self.make_move(player.board_value, move)
            if self.has_won(player.board_value):
                self.winner = player.board_value
                return
            if self.has_tied():
                return
            if player.board_value == self.player1.board_value:
                player = self.player2
            else:
                player = self.player1

    def get_winner(self):
        return self.winner

    def board_to_player_perspective(self, player):
        return self.board * player

    def has_won(self, player):
        # Horizontal
        if self.board.item(0) == player and self.board.item(1) == player and self.board.item(2) == player:
            return True
        if self.board.item(3) == player and self.board.item(4) == player and self.board.item(5) == player:
            return True
        if self.board.item(6) == player and self.board.item(7) == player and self.board.item(8) == player:
            return True
        # Vertical
        if self.board.item(0) == player and self.board.item(3) == player and self.board.item(6) == player:
            return True
        if self.board.item(1) == player and self.board.item(4) == player and self.board.item(7) == player:
            return True
        if self.board.item(2) == player and self.board.item(5) == player and self.board.item(8) == player:
            return True
        # Diagonal
        if self.board.item(0) == player and self.board.item(4) == player and self.board.item(8) == player:
            return True
        if self.board.item(2) == player and self.board.item(4) == player and self.board.item(6) == player:
            return True
        return False

    def has_tied(self):
        return np.count_nonzero(self.board) == 9

    def make_move(self, player, move):
        cur_value = self.board.item(move)
        if cur_value != 0:
            raise ValueError("Player {} tried to set board position {}, which already had value {}".format(player,
                                                                                                           move,
                                                                                                           cur_value))
        self.board.itemset(move, player)
