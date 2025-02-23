import math

BOARD_SIZE = 9


class Board:
    def __init__(self, board: list[list[int]]):
        positionsible_values_def = [i for i in range(1, BOARD_SIZE + 1)]
        self.board = [[positionsible_values_def.copy() for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if board[row][column] != 0:
                    self.set_cell_fixed_value((row, column), board[row][column])
                    self.propagate_constraints((row, column))

    def is_cell_fixed(self, position: tuple[int, int]) -> bool:
        return len(self.get_cell(position)) == 1

    def is_cell_failed(self, position: tuple[int, int]) -> bool:
        return len(self.get_cell(position)) == 0

    def get_cell(self, position: tuple[int, int]) -> list[int]:
        return self.board[position[0]][position[1]]

    def get_cell_value(self, position: tuple[int, int]) -> int | None:
        return self.get_cell(position)[0] if not self.is_cell_failed(position) else None

    def _delete_cell_value(self, position: tuple[int, int], val: int) -> None:
        self.board[position[0]][position[1]].remove(val) if val in self.board[position[0]][position[1]] else None

    def set_cell_fixed_value(self, position: tuple[int, int], val: int) -> None:
        self.board[position[0]][position[1]] = [val]

    def _can_cell_contain(self, position: tuple[int, int], val: int) -> bool:
        return val in self.get_cell(position)

    def all_cells_fixed(self) -> bool:
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if not self.is_cell_fixed((row, column)):
                    return False
        return True

    def get_cell_fixed_count(self) -> int:
        fixed_cnt = 0
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if self.is_cell_fixed((row, column)):
                    fixed_cnt += 1
        return fixed_cnt

    def not_solvable(self) -> bool:
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if self.is_cell_failed((row, column)):
                    return True
        return False

    def propagate_constraints_all(self) -> None:
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if self.is_cell_fixed((row, column)):
                    self.propagate_constraints((row, column))

    def propagate_constraints(self, position: tuple[int, int]) -> None:
        self._propagate_constraints_row(position)
        self._propagate_constraints_column(position)
        self._propagate_constraints_square(position)

    def _propagate_constraints_row(self, position: tuple[int, int]) -> None:
        for column in range(BOARD_SIZE):
            if self.is_cell_failed(position):
                return

            if column is not position[1]:
                cell_coordintaes = (position[0], column)
                self._propagate_constraints_cell(cell_coordintaes, position)

    def _propagate_constraints_column(self, position: tuple[int, int]) -> None:
        for row in range(BOARD_SIZE):
            if self.is_cell_failed(position):
                return

            if row is not position[0]:
                cell_coordintaes = (row, position[1])
                self._propagate_constraints_cell(cell_coordintaes, position)

    def _propagate_constraints_square(self, position: tuple[int, int]) -> None:
        square_size = int(math.sqrt(BOARD_SIZE))
        square_start_row = position[0] // square_size * square_size
        square_start_column = position[1] // square_size * square_size

        for row in range(square_start_row, square_start_row + square_size):
            for column in range(square_start_column, square_start_column + square_size):
                if self.is_cell_failed(position):
                    return

                if row != position[0] or column != position[1]:
                    cell_coordintaes = (row, column)
                    self._propagate_constraints_cell(cell_coordintaes, position)

    def _propagate_constraints_cell(self, cell_coordintaes: tuple[int, int], position: tuple[int, int]) -> None:
        if not self.is_cell_failed(cell_coordintaes):
            if self.is_cell_fixed(cell_coordintaes) and self.get_cell_value(position):
                self._delete_cell_value(cell_coordintaes, self.get_cell_value(position))  # type: ignore

            elif self.get_cell_value(position):
                self._delete_cell_value(cell_coordintaes, self.get_cell_value(position))  # type: ignore

                if self.is_cell_fixed(cell_coordintaes):
                    self.propagate_constraints(cell_coordintaes)

    def print(self) -> None:
        print("")
        for row in range(BOARD_SIZE):
            if row % math.sqrt(BOARD_SIZE) == 0:
                print("-------------------------")

            for column in range(BOARD_SIZE):
                if column % math.sqrt(BOARD_SIZE) == 0:
                    print("|", end=" ")

                if self.is_cell_fixed((row, column)):
                    print(self.get_cell_value((row, column)), end=" ")
                else:
                    print("-", end=" ")

            print("|")

        print("-------------------------")
