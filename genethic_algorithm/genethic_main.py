from board import readBoardsStrsFromFile, makeBoardsFromFile
from argparse import ArgumentParser
from genethic_algorithm import genethicAlgorithm

def main():
    parser = ArgumentParser(description="Sudoku Solver with Hyperparameters")
    parser.add_argument("difficulty", help="Difficulty of the sudoku board")
    parser.add_argument("-nboard", "--boardNumber", type=int, default=0, help="Number of board")

    args = parser.parse_args()
    try:
        boardsStr = readBoardsStrsFromFile(f"../resources/{args.difficulty}.txt")[args.boardNumber]
    except FileNotFoundError:
        boardsStr = readBoardsStrsFromFile(f"./resources/{args.difficulty}.txt")[args.boardNumber]
    pop0 = makeBoardsFromFile(boardsStr, pop0Size=100, random_state=[index for index in range(800)])
    print("Solving...")
    bestScore, bestSollution, sollutions, evaluations = genethicAlgorithm(pop0, maxIter=200, tournamentSize=50, crossoverProb=0.1, mutationProb=0.2)
    print(bestScore)
    print(bestSollution)
    print(min(sollutions))



if __name__ == "__main__":
    main()
