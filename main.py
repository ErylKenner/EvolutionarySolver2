from itertools import permutations

import numpy as np
from pygad import cnn, gacnn, GA, load

from Games.TicTacToe import TicTacToe
from Games.TicTacToePlayer import TicTacToePlayer

result_matrix = None
GACNN_instance = None


def play_games(ga_instance):
    global result_matrix
    global GACNN_instance
    print("\nPlaying games to calculate new fitness values...")
    population_size = ga_instance.pop_size[0]
    result_matrix = np.zeros(shape=(population_size, population_size))
    games_played = 0
    for player1, player2 in permutations(range(population_size), r=2):
        tictactoe_player1 = TicTacToePlayer(GACNN_instance.population_networks[player1], 1)
        tictactoe_player2 = TicTacToePlayer(GACNN_instance.population_networks[player2], -1)
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
    global GACNN_instance
    population_matrices = gacnn.population_as_matrices(population_networks=GACNN_instance.population_networks,
                                                       population_vectors=ga_instance.population)
    GACNN_instance.update_population_trained_weights(population_trained_weights=population_matrices)

    current_best_fitness = np.max(ga_instance.last_generation_fitness)
    prev_best_fitness = np.max(ga_instance.best_solutions_fitness)
    print("Generation {} finished\nFitness: {}\nFitness change: {}".format(ga_instance.generations_completed,
                                                                           current_best_fitness,
                                                                           current_best_fitness - prev_best_fitness))
    if not ga_instance.generations_completed == ga_instance.num_generations:
        play_games(ga_instance)


def main():
    input_layer = cnn.Input2D(input_shape=(3, 3))
    conv_layer = cnn.Conv2D(num_filters=1,
                            kernel_size=3,
                            previous_layer=input_layer,
                            activation_function="relu")
    average_pooling_layer = cnn.AveragePooling2D(pool_size=5,
                                                 previous_layer=conv_layer,
                                                 stride=3)
    flatten_layer = cnn.Flatten(previous_layer=average_pooling_layer)
    dense_layer = cnn.Dense(num_neurons=9,
                            previous_layer=flatten_layer,
                            activation_function="softmax")
    model = cnn.Model(last_layer=dense_layer,
                      epochs=5,
                      learning_rate=0.01)
    model.summary()
    global GACNN_instance
    GACNN_instance = gacnn.GACNN(model=model,
                                 num_solutions=4)
    population_vectors = gacnn.population_as_vectors(population_networks=GACNN_instance.population_networks)
    print(population_vectors)
    initial_population = population_vectors.copy()

    num_generations = 10
    population_size = 8
    num_parents_mating = population_size // 2
    keep_parents = population_size // 8
    mutation_probabilities = 0.25  # (0.5, 0.02)
    num_genes = 3
    ga_instance = GA(num_generations=num_generations,
                     num_parents_mating=num_parents_mating,
                     initial_population=initial_population,
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
    ga_instance.save(filename=filename)
    loaded_ga_instance = load(filename="genetic_solution")
    print(loaded_ga_instance.population)


if __name__ == '__main__':
    main()
