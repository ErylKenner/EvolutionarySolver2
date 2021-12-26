from itertools import combinations

import numpy as np
import pygad

from Games.TicTacToe import TicTacToe
from Games.TicTacToePlayer import TicTacToePlayer

fitness_values = []
opponent = None


def play_self_games(ga_instance):
    global fitness_values
    # print("\nPlaying games to calculate new fitness values...")
    population_size = ga_instance.pop_size[0]
    all_stars_size = min(len(ga_instance.best_solutions), population_size // 4)
    result_matrix = np.zeros(shape=(population_size + all_stars_size, population_size + all_stars_size))
    games_played = 0
    for player1, player2 in combinations(range(population_size + all_stars_size), r=2):
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
        fitness = tictactoe_game.get_winner()
        result_matrix.itemset((player1, player2), fitness)
        result_matrix.itemset((player2, player1), -fitness)
        games_played += 1
    # print("{} games were played".format(games_played))

    fitness_values = []
    for solution_idx in range(population_size):
        total = 0
        for i in range(population_size + all_stars_size):
            total += result_matrix.item((solution_idx, i))
            # total += result_matrix.item((i, solution_idx))
        total /= (population_size + all_stars_size - 1)
        fitness_values.append(total)
    ga_instance.last_generation_fitness = np.array(fitness_values)


def play_coevolution_games(ga_instance):
    global fitness_values
    global opponent
    # print("\nPlaying coevolution games to calculate new fitness values...")
    population_size = ga_instance.pop_size[0]
    fitness_values = np.zeros(shape=population_size)
    for player in range(population_size):
        opponent_size = opponent.shape[0]
        for opponent_player in range(opponent_size):
            # You go first
            tictactoe_player = TicTacToePlayer(ga_instance.population[player], 1)
            tictactoe_opponent = TicTacToePlayer(opponent[opponent_player], -1)
            tictactoe_game = TicTacToe(tictactoe_player, tictactoe_opponent)
            tictactoe_game.play_game()
            fitness = tictactoe_game.get_winner()
            fitness_values[player] += fitness

            # Opponent goes first
            tictactoe_opponent.board_value = 1
            tictactoe_player.board_value = -1
            tictactoe_game = TicTacToe(tictactoe_opponent, tictactoe_player)
            tictactoe_game.play_game()
            fitness = tictactoe_game.get_winner()
            fitness_values[player] -= fitness

    fitness_values = fitness_values / (2 * population_size)


def on_start_self(ga_instance):
    play_self_games(ga_instance)


def on_start_coevolution(ga_instance):
    play_coevolution_games(ga_instance)


def fitness_func(solution, solution_idx):
    # print(fitness_values[solution_idx])
    return fitness_values[solution_idx]


def on_generation_self(ga_instance):
    current_best_fitness = np.max(ga_instance.last_generation_fitness)
    print(
        "Self-play generation {} finished.  Fitness: {:.3f}".format(ga_instance.generations_completed,
                                                                    current_best_fitness))
    if not ga_instance.generations_completed == ga_instance.num_generations:
        play_self_games(ga_instance)


def on_generation_coevolution(ga_instance):
    current_best_fitness = np.max(ga_instance.last_generation_fitness)
    print("Coevolution generation {} finished.  Fitness: {:.3f}".format(ga_instance.generations_completed,
                                                                        current_best_fitness))
    if not ga_instance.generations_completed == ga_instance.num_generations:
        play_coevolution_games(ga_instance)


def mutation_func(offspring, ga_instance):
    for chromosome_idx in range(offspring.shape[0]):
        if fitness_func([], chromosome_idx) >= 0.85:
            num_genes = 2
            magnitude = 0.5
        elif fitness_func([], chromosome_idx) >= 0.75:
            num_genes = 2
            magnitude = 1
        elif fitness_func([], chromosome_idx) >= 0.6:
            num_genes = 3
            magnitude = 1
        elif fitness_func([], chromosome_idx) >= 0.5:
            num_genes = 3
            magnitude = 2.5
        else:
            num_genes = 3
            magnitude = 3
        choices = np.random.choice(range(offspring.shape[1]), size=num_genes)
        for choice in choices:
            offspring[chromosome_idx, choice] += np.random.random() * magnitude * np.random.choice([-1, 1])
    return offspring


def main():
    filename = "genetic_solution_coevolution"
    np.set_printoptions(edgeitems=30, linewidth=100000, formatter=dict(float=lambda x: "{:>6.3f}".format(x)))

    num_generations = 200
    population_size = 50
    num_parents_mating = population_size // 2
    keep_parents = population_size // 4
    mutation_probabilities = 0.25  # (0.5, 0.02)
    num_genes = 90

    # ga_instance_a = pygad.load(filename="genetic_solution_coevolution_2")
    # ga_instance_b = pygad.load(filename="genetic_solution_coevolution_2")
    # population_a = ga_instance_a.population
    # population_b = ga_instance_b.population

    ga_instance_a = None
    ga_instance_b = None
    population_a = np.asarray(np.random.uniform(low=-4, high=4, size=(population_size, num_genes)))
    population_b = np.asarray(np.random.uniform(low=-4, high=4, size=(population_size, num_genes)))

    global_iterations = 100
    for global_iteration in range(global_iterations):
        print("\n\n\nGlobal iteration {}\n".format(global_iteration))
        ga_instance_a = pygad.GA(num_generations=num_generations,
                                 num_parents_mating=num_parents_mating,
                                 initial_population=population_a,
                                 fitness_func=fitness_func,
                                 on_generation=on_generation_self,
                                 on_start=on_start_self,
                                 mutation_type=mutation_func,
                                 parent_selection_type="sss",
                                 keep_parents=keep_parents)
        ga_instance_a.run()
        population_a = ga_instance_a.population
        # ga_instance_a.plot_fitness()

        ga_instance_b = pygad.GA(num_generations=num_generations,
                                 num_parents_mating=num_parents_mating,
                                 initial_population=population_b,
                                 fitness_func=fitness_func,
                                 on_generation=on_generation_self,
                                 on_start=on_start_self,
                                 mutation_type=mutation_func,
                                 parent_selection_type="sss",
                                 keep_parents=keep_parents)
        ga_instance_b.run()
        population_b = ga_instance_b.population
        # ga_instance_b.plot_fitness()

        global opponent
        iterations = 5
        for iteration in range(iterations):
            # Instance B trains. Instance A is stagnant
            opponent = population_a
            ga_instance_b = pygad.GA(num_generations=20,
                                     num_parents_mating=num_parents_mating,
                                     initial_population=population_b,
                                     fitness_func=fitness_func,
                                     on_generation=on_generation_coevolution,
                                     on_start=on_start_coevolution,
                                     mutation_type=mutation_func,
                                     parent_selection_type="sss",
                                     keep_parents=keep_parents)
            ga_instance_b.run()
            population_b = ga_instance_b.population
            # ga_instance_b.plot_fitness()
            # Instance A trains. Instance B is stagnant
            opponent = population_b
            ga_instance_a = pygad.GA(num_generations=20,
                                     num_parents_mating=num_parents_mating,
                                     initial_population=population_a,
                                     fitness_func=fitness_func,
                                     on_generation=on_generation_coevolution,
                                     on_start=on_start_coevolution,
                                     mutation_type=mutation_func,
                                     parent_selection_type="sss",
                                     keep_parents=keep_parents)
            ga_instance_a.run()
            population_a = ga_instance_a.population
            # ga_instance_a.plot_fitness()
        ga_instance_a.save(filename="{}_{}".format(filename, str(global_iteration)))

    solution, solution_fitness, _ = ga_instance_a.best_solution(ga_instance_a.last_generation_fitness)
    print(
        "Parameters of the best solution: \n{}\nFitness value: {:.5f}\n".format(solution.reshape(10, 9),
                                                                                solution_fitness))

    loaded_ga_instance = pygad.load(filename="{}_{}".format(filename, global_iterations - 1))
    best_solution, _, _ = loaded_ga_instance.best_solution(loaded_ga_instance.last_generation_fitness)
    best_player = TicTacToePlayer(best_solution, 1)
    best_player.plot_genes()

    print("Game 1. AI goes first")
    human_player = TicTacToePlayer([], -1, player_type="human")
    tictactoe_game = TicTacToe(best_player, human_player, print_board=True)
    tictactoe_game.play_game()

    print("Game 2. You go first")
    human_player.board_value = 1
    best_player.board_value = -1
    tictactoe_game = TicTacToe(human_player, best_player, print_board=True)
    tictactoe_game.play_game()


if __name__ == '__main__':
    main()
