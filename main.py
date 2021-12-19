from itertools import permutations

import numpy as np
import pygad

from Games.TicTacToe import TicTacToe
from Games.TicTacToePlayer import TicTacToePlayer

result_matrix = None


def play_games(ga_instance):
    global result_matrix
    print("\nPlaying games to calculate new fitness values...")
    population_size = ga_instance.pop_size[0]
    all_stars_size = min(len(ga_instance.best_solutions), population_size // 4)
    result_matrix = np.zeros(shape=(population_size + all_stars_size, population_size + all_stars_size))
    games_played = 0
    for player1, player2 in permutations(range(population_size + all_stars_size), r=2):
        if player1 < population_size:
            tictactoe_player1 = TicTacToePlayer(ga_instance.population[player1], 1)
        else:
            tictactoe_player1 = TicTacToePlayer(ga_instance.best_solutions[population_size - player1 - 1], 1)
        if player2 < population_size:
            tictactoe_player2 = TicTacToePlayer(ga_instance.population[player2], -1)
        else:
            tictactoe_player2 = TicTacToePlayer(ga_instance.best_solutions[population_size - player2 - 1], -1)
        tictactoe_game = TicTacToe(tictactoe_player1, tictactoe_player2)
        tictactoe_game.play_game()
        result_matrix.itemset((player1, player2), tictactoe_game.get_winner())
        games_played += 1
    print("{} games were played".format(games_played))


def on_start(ga_instance):
    play_games(ga_instance)


def fitness_func(solution, solution_idx):
    result_size = np.shape(result_matrix)[0]
    total = 0
    for i in range(result_size):
        total += result_matrix.item((solution_idx, i))
        total += result_matrix.item((i, solution_idx))
    total /= 2 * (result_size - 1)
    print(total)
    return total


def on_generation(ga_instance):
    current_best_fitness = np.max(ga_instance.last_generation_fitness)
    prev_best_fitness = np.max(ga_instance.best_solutions_fitness)
    print("Generation {} finished\nFitness: {}\nFitness change: {}".format(ga_instance.generations_completed,
                                                                           current_best_fitness,
                                                                           current_best_fitness - prev_best_fitness))
    if not ga_instance.generations_completed == ga_instance.num_generations:
        play_games(ga_instance)


def main():
    num_generations = 100
    population_size = 50
    num_parents_mating = population_size // 2
    keep_parents = population_size // 8
    mutation_probabilities = 0.25  # (0.5, 0.02)
    num_genes = 9
    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           sol_per_pop=population_size,
                           num_genes=num_genes,
                           fitness_func=fitness_func,
                           on_generation=on_generation,
                           on_start=on_start,
                           mutation_type='random',
                           mutation_probability=mutation_probabilities,
                           parent_selection_type="sss",
                           keep_parents=keep_parents,
                           save_solutions=True,
                           save_best_solutions=True)
    ga_instance.run()

    ga_instance.plot_fitness()
    ga_instance.plot_genes(plot_type="scatter", graph_type="plot", solutions="all")
    ga_instance.plot_new_solution_rate()

    solution, solution_fitness, _ = ga_instance.best_solution(ga_instance.last_generation_fitness)
    print("Parameters of the best solution: {}\nFitness value: {}\n".format(solution, solution_fitness))

    filename = "genetic_solution"
    # ga_instance.save(filename=filename)
    loaded_ga_instance = pygad.load(filename="genetic_solution")
    best_solution = loaded_ga_instance.best_solution(loaded_ga_instance.last_generation_fitness)

    print("Game 1. AI goes first")
    tictactoe_player1 = TicTacToePlayer(best_solution[0], 1, player_type="conv")
    tictactoe_player2 = TicTacToePlayer([], -1, player_type="human")
    tictactoe_game = TicTacToe(tictactoe_player1, tictactoe_player2, print_board=True)
    tictactoe_game.play_game()

    print("Game 2. You go first")
    tictactoe_player1 = TicTacToePlayer(best_solution[0], -1, player_type="conv")
    tictactoe_player2 = TicTacToePlayer([], 1, player_type="human")
    tictactoe_game = TicTacToe(tictactoe_player2, tictactoe_player1, print_board=True)
    tictactoe_game.play_game()


if __name__ == '__main__':
    main()
