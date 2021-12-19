from random import sample

import numpy as np


class TicTacToePlayer(object):
    def __init__(self, genes, board_value, player_type="conv"):
        self.genes = genes
        self.board_value = board_value
        self.player_type = player_type

    def make_move(self, board):
        if self.player_type == "conv":
            return self.conv_move(board)
        if self.player_type == "simple":
            return self.simple_move(board)
        if self.player_type == "random":
            return self.random_move(board)
        if self.player_type == "human":
            return self.human_move(board)

    def human_move(self, board):
        move = input("Move: ")
        return int(move)

    def conv_move(self, board):
        padded_board = np.zeros(shape=(5, 5))
        for i in range(3):
            for j in range(3):
                board_value = board.item((i, j))
                padded_board.itemset((i + 1, j + 1), board_value)

        conv_filter = np.zeros(shape=(3, 3))
        for i in range(9):
            conv_filter.itemset(i, self.genes.item(i))

        output = np.zeros(shape=9)
        for i in range(3):
            for j in range(3):
                value = 0
                for row in range(3):
                    for col in range(3):
                        value += conv_filter.item((row, col)) * padded_board.item((i + row, j + col))
                output.itemset(3 * i + j, value)

        choices = (-output).argsort()
        for choice in choices:
            if board.item(choice) == 0:
                return choice

        return -1

    def random_move(self, board):
        for row in range(3):
            for col in range(3):
                if board.item((row, col)) == 0:
                    return row, col
        return -1, -1

    def simple_move(self, board):
        cases = np.argsort(self.genes)
        for case in cases:
            if case == 0:
                choices = sample([0, 2, 6, 8], 4)
            elif case == 1:
                choices = sample([1, 3, 5, 7], 4)
            elif case == 2:
                choices = [4]
            for choice in choices:
                if board.item(choice) == 0:
                    return choice
        return -1
