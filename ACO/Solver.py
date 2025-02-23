try:
    from Board import Board, BOARD_SIZE
except ModuleNotFoundError:
    from ACO.Board import Board, BOARD_SIZE
import copy
import random
import numpy as np


class Ant:
    def __init__(self, board: Board, pheromone_matrix: list[list[dict[int, float]]], local_pher_update: float, greedines: float) -> None:
        self.local_pher_update = local_pher_update
        self.greedines = greedines
        self.initial_pheromone_value = 1 / BOARD_SIZE**2
        self.board = board
        self.pheromone_matrix = pheromone_matrix
        self.row = random.randint(0, BOARD_SIZE - 1)
        self.column = random.randint(0, BOARD_SIZE - 1)

    def step(self) -> None:
        if not self.board.is_cell_fixed((self.row, self.column)) and not self.board.is_cell_failed((self.row, self.column)):
            self._update_cell()

    def _update_cell(self) -> None:
        value = self._select_value()
        self.board.set_cell_fixed_value((self.row, self.column), value)  # type: ignore
        self.board.propagate_constraints((self.row, self.column))
        self.board.propagate_constraints_all()
        pher_value_to_update = self.pheromone_matrix[self.row][self.column][value]
        self.pheromone_matrix[self.row][self.column][value] = (
            1 - self.local_pher_update
        ) * pher_value_to_update + self.local_pher_update * self.initial_pheromone_value
        self.row, self.column = (self.row, self.column + 1) if self.column < BOARD_SIZE - 1 else ((self.row + 1) % 9, 0)

    def _select_value(self) -> int:
        pheromone = self.pheromone_matrix[self.row][self.column]
        possible_values = self.board.get_cell((self.row, self.column))

        if random.random() > self.greedines:
            best_value = max(possible_values, key=lambda value: pheromone[value], default=0)
        else:
            total_pheromone = np.cumsum([pheromone[value] for value in possible_values])
            spin_value = total_pheromone[-1] * random.random()
            best_value = possible_values[np.searchsorted(total_pheromone, spin_value)]
        return best_value


class Solver:
    def __init__(
        self,
        ants_number: int,
        global_pher_update: float,
        local_pher_update: float,
        greedines: float,
        evaporation_parameter: float,
        max_iterations: int,
        max_evaluations: int = None,
    ) -> tuple[int, Board, list[int], int]:
        self.ants_number = ants_number
        self.global_pher_update = global_pher_update
        self.local_pher_update = local_pher_update
        self.greedines = greedines
        self.evaporation_parameter = evaporation_parameter
        self.best_pheromone_to_add = 0
        self.max_iterations = max_iterations
        self.max_evaluations = max_evaluations

    def solve(self, board: Board, print_step: bool = False) -> Board:
        self.board_to_solve = board
        self._initialize_global_pheromone()
        self._initialize_ants()
        self.best_solution = board
        solutions = []
        evaluations = 0
        for iter in range(self.max_iterations):
            self._initialize_ants()
            for _ in range(BOARD_SIZE**2):
                for ant in self.ants:
                    ant.step()
            best_ant = None
            for ant in self.ants:
                if len(solutions)==0 or BOARD_SIZE**2 - ant.board.get_cell_fixed_count() < solutions[-1]:
                    best_ant = ant
                    solutions.append(BOARD_SIZE**2 - ant.board.get_cell_fixed_count())
                else:
                    solutions.append(solutions[-1])
                evaluations += 1
            if best_ant:
                self.best_solution = (
                    best_ant.board if best_ant.board.get_cell_fixed_count() > self.best_solution.get_cell_fixed_count() else self.best_solution
                )
                for _ in range(2):
                    solutions.append(solutions[-1])
                    evaluations += 1
            if self.max_evaluations and evaluations >= self.max_evaluations:
                return BOARD_SIZE**2 - self.best_solution.get_cell_fixed_count(), self.best_solution, solutions, evaluations, iter+1
            if print_step:
                print(
                    f"Fixed {round(self.best_solution.get_cell_fixed_count()/BOARD_SIZE**2 * 100 , 2)} % of the cells, iteration: {iter}/{self.max_iterations}",
                    end="\r"
                )
            if self.best_solution.all_cells_fixed():
                return 0, self.best_solution, solutions, evaluations, iter+1
            self._update_pheromone_matrix(self.best_solution)
        return BOARD_SIZE**2 - self.best_solution.get_cell_fixed_count(), self.best_solution, solutions, evaluations, iter+1

    def _initialize_global_pheromone(self) -> None:
        self.global_pher_matrix = [
            [{num: 1 / BOARD_SIZE**2 for num in range(1, BOARD_SIZE + 1)} for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        ]

    def _initialize_ants(self) -> None:
        self.ants: list[Ant] = []
        for _ in range(self.ants_number):
            ant = Ant(copy.deepcopy(self.board_to_solve), self.global_pher_matrix, self.local_pher_update, self.greedines)
            self.ants.append(ant)

    def _update_pheromone_matrix(self, best_ant_board: Board) -> None:
        pheromone_to_add = BOARD_SIZE**2 / (BOARD_SIZE**2 - best_ant_board.get_cell_fixed_count())

        if pheromone_to_add > self.best_pheromone_to_add:
            self.solution = best_ant_board
            self.best_pheromone_to_add = pheromone_to_add

        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if not best_ant_board.is_cell_failed((row, column)):
                    value = best_ant_board.get_cell_value((row, column))
                    self.global_pher_matrix[row][column][value] = self.global_pher_matrix[row][column][value] * (1 - self.global_pher_update) + self.global_pher_update * self.best_pheromone_to_add  # type: ignore
        self.best_pheromone_to_add *= 1 - self.evaporation_parameter
