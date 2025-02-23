from Solver import Solver
from argparse import ArgumentParser
from utils import get_boards_from_file


def main():
    parser = ArgumentParser(description="Sudoku Solver with Hyperparameters")
    parser.add_argument("difficulty", help="Difficulty of the sudoku board")
    parser.add_argument("-antsNum", "--antsNum", type=int, default=100, help="Number of ants")
    parser.add_argument("-gloPherUp", "--globalPherUpdate", type=float, default=0.9, help="Global pheromone update")
    parser.add_argument("-locPherUp", "--localPherUpdate", type=float, default=0.1, help="Local pheromone update")
    parser.add_argument("-greed", "--greediness", type=float, default=0.9, help="Greediness")
    parser.add_argument("-evapPar", "--evaporationParam", type=float, default=0.005, help="Best value evaporation parameter")
    parser.add_argument("-iter", "--iterations", type=int, default=200, help="Number of iterations")
    parser.add_argument("-nboard", "--boardNumber", type=int, default=0, help="Number of board")

    args = parser.parse_args()
    try:
        board = get_boards_from_file(f"../resources/{args.difficulty}.txt")[args.boardNumber]
    except FileNotFoundError:
        board = get_boards_from_file(f"./resources/{args.difficulty}.txt")[args.boardNumber]
    print(board.print())
    print("Solving...")
    solver = Solver(args.antsNum, args.globalPherUpdate, args.localPherUpdate, args.greediness, args.evaporationParam, args.iterations)
    returned = solver.solve(board, print_step=True)
    print(returned[1].print())


if __name__ == "__main__":
    main()
