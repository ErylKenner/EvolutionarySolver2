import numpy as np


class TicTacToePlayer(object):
    def __init__(self, genes, board_value):
        self.genes = genes
        self.board_value = board_value

    def make_move(self, board):
        # Do some logic based on genes
        # Return the move to make
        # prepared_board = np.expand_dims(prepared_board, axis=0)
        prepared_board = np.zeros(shape=(1, 3, 3, 1))
        for i in range(3):
            for j in range(3):
                value = board.item((i, j))
                # value = np.matrix(value)
                prepared_board.itemset((0, i, j, 0), value)
        # print(prepared_board)
        ret = self.genes.predict(prepared_board)
        # print(self.genes)
        print(ret)

        # return ret
        """
        # Make all valid moves equal to 1 and all invalid moves equal to 0
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
        """
        # For now, return the first nonzero move
        for row in range(3):
            for col in range(3):
                if board.item((row, col)) == 0:
                    return row, col
        return -1, -1
