from random import sample

import matplotlib.pyplot as plt
import numpy as np


class TicTacToePlayer(object):
    def __init__(self, genes, board_value, player_type="neural_network"):
        self.genes = genes
        self.board_value = board_value
        self.player_type = player_type

    def plot_genes(self):
        if self.player_type == "neural_network":
            reshaped_genes = np.reshape(self.genes, newshape=(10, 9))
            reshaped_genes = np.transpose(reshaped_genes)
            reshaped_genes = reshaped_genes / 10 + 0.5
            fig, axes = plt.subplots(3, 4)
            for i in range(9):
                divided_genes = 1 - reshaped_genes[i][:-1].reshape(3, 3)
                axes[i // 3, i % 3].pcolor(np.flip(divided_genes, axis=0), vmin=0, vmax=1, cmap="bwr")
            biases = 1 - reshaped_genes[:, 9].reshape(3, 3)
            axes[2, 3].pcolor(np.flip(biases, axis=0), vmin=0, vmax=1, cmap="bwr")
            plt.show()

    def make_move(self, board):
        if self.player_type == "neural_network":
            return self.neural_network_move(board)
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

    def neural_network_move(self, board):
        # Gene size = 90
        input_board = np.reshape(board, newshape=(1, 9))
        input_board = np.append(input_board, [[1.0]], axis=1)
        input_board = np.asmatrix(input_board)

        weights = np.reshape(self.genes, newshape=(10, 9))
        weights = np.asmatrix(weights)

        output = input_board * weights

        output = np.squeeze(np.asarray(output))
        choices = np.argsort(-output)
        for _, choice in enumerate(choices):
            value = board.item(choice)
            if value == 0:
                return choice
        return -1

    def conv_move(self, board):
        # Gene size = 9
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
        # Gene size = 3
        cases = np.argsort(self.genes)
        for case in cases:
            choices = []
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
