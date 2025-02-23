import numpy as np
import random


def readBoardsStrsFromFile(filename: str) -> list[str]:
    boardsStrs = []
    try:
        with open(filename, "r") as filehandle:
            boardsStrs = filehandle.readlines()
        newBoardStrs = []
        for boardStr in boardsStrs:
            newBoardStrs.append(boardStr.strip())
        return newBoardStrs
    except FileNotFoundError:
        return []


def InitiallFilling(boardStr: str, board: np.matrix, boardMask: np.matrix, rowLength: int) -> None:
    rowIndex = 0
    columnIndex = 0
    for char in boardStr:
        if rowIndex == rowLength:
            rowIndex = 0
            columnIndex += 1
        if char == ".":
            boardMask[rowIndex, columnIndex] = False
        else:
            board[rowIndex, columnIndex] = int(char)
            boardMask[rowIndex, columnIndex] = True
        rowIndex += 1


def makeNumbersToUse(numbersToUse: list, board: np.matrix, rowLength: int) -> None:
    for repetition in range(rowLength):
        for number in range(rowLength):
            numbersToUse.append(number + 1)
    for rowIndex in range(board.shape[0]):
        for columnIndex in range(board.shape[1]):
            if board[rowIndex, columnIndex] in numbersToUse:
                numbersToUse.remove(board[rowIndex, columnIndex])


def FillBoard(board: np.matrix, numbersToUse: list[int], random_state: int) -> None:
    random.seed(random_state)
    for rowIndex in range(board.shape[0]):
        for columnIndex in range(board.shape[1]):
            if board[rowIndex, columnIndex] == 0:
                chosenNumber = random.choice(numbersToUse)
                board[rowIndex, columnIndex] = chosenNumber
                numbersToUse.remove(chosenNumber)
    random.seed(None)


def makeBoardFromFile(boardStr: str, rowLength: int = 9, columnLength: int = 9, random_state: int = 42) -> tuple[np.matrix, np.matrix]:
    board = np.matrix(np.zeros((rowLength, columnLength)), dtype=int)
    boardMask = np.matrix(np.zeros((rowLength, columnLength)), dtype=bool)
    numbersToUse = []
    InitiallFilling(boardStr, board, boardMask, rowLength)
    makeNumbersToUse(numbersToUse, board, rowLength)
    FillBoard(board, numbersToUse, random_state)
    return board, boardMask


def makeBoardsFromFile(
    boardStr: str, rowLength: int = 9, columnLength: int = 9, pop0Size: int = 40, random_state: list[int] or None = None
) -> list[(np.matrix, np.matrix)]:
    boardsMasks = []
    for number in range(pop0Size):
        if random_state:
            board, boardMask = makeBoardFromFile(boardStr, random_state=random_state.pop(0))
        else:
            board, boardMask = makeBoardFromFile(boardStr, random_state=random_state)
        boardsMasks.append((board, boardMask))
    return boardsMasks


def main():
    boardsStrs = readBoardsStrsFromFile("../resources/easy.txt")
    boardsMasks = makeBoardsFromFile(boardsStrs[0], random_state=None)


if __name__ == "__main__":
    main()
