import numpy as np
import math
from copy import deepcopy


def makePairs(pop: list[(np.matrix, np.matrix)]) -> list[((np.matrix, np.matrix), (np.matrix, np.matrix))]:
    pairs = []
    for iterator in range(0, len(pop), 2):
        if iterator + 1 < len(pop):
            pairs.append((pop[iterator], pop[iterator + 1]))
        else:
            pairs.append((pop[iterator - 1], pop[iterator]))
    return pairs


def q(cell: tuple[np.matrix, np.matrix]) -> int:
    invalid = 0
    for row in cell[0]:
        invalid += len(row.tolist()[0]) - len(set(row.tolist()[0]))
    for columnIndex in range(cell[0].shape[1]):
        column = cell[0][:, columnIndex]
        invalid += len(column.tolist()[0]) - len(set(column.tolist()[0]))
    rowIndices = (3, 6, 9)
    columnIndices = (3, 6, 9)
    prevRowIndice = 0
    prevColumnIndice = 0
    for rowIndice in rowIndices:
        for columnIndice in columnIndices:
            matrix = cell[0][prevRowIndice:rowIndice, prevColumnIndice:columnIndice]
            matrixValues = list(matrix.flat)
            invalid += len(matrixValues) - len(set(matrixValues))
            prevColumnIndice = columnIndice
        prevRowIndice = rowIndice
    return invalid


def calculateProb(popSize: int, tournamentSize: int, rank: int) -> float:
    return (1 / math.pow(popSize, tournamentSize)) * (math.pow(popSize - rank + 1, tournamentSize) - math.pow(popSize - rank, tournamentSize))


def getProbabilities(pop: list[(np.matrix, np.matrix)], tournamentSize: int = 2, sort: bool = True) -> list[float]:
    if sort:
        sortedPop = sorted(pop, key=q)
    else:
        sortedPop = pop
    calculated = []
    probabilities = []
    rank = 0
    popSize = len(sortedPop)
    for boardTuple in sortedPop:
        if boardTuple[0].tolist() not in calculated:
            rank += 1
            probabilities.append(calculateProb(popSize, tournamentSize, rank))
            calculated.append(boardTuple[0].tolist())
        else:
            probabilities.append(calculateProb(popSize, tournamentSize, rank))
    return probabilities


def tournamentSelection(pop: list[(np.matrix, np.matrix)], tournamentSize: int = 2, seed: int = None) -> list[(np.matrix, np.matrix)]:
    selected = []
    sortedPop = sorted(pop, key=q)
    probs = np.asarray(getProbabilities(sortedPop, tournamentSize, sort=False)).astype("float64")
    probs = probs / np.sum(probs)
    indexList = [index for index in range(len(sortedPop))]
    if seed:
        np.random.seed(seed)
    tournamentIndexes = np.random.choice(indexList, size=len(sortedPop), replace=True, p=probs)
    selected = [sortedPop[index] for index in tournamentIndexes]
    return selected


def crossover(pop: list[(np.matrix, np.matrix)], crossoverProb: float = 0.5, seeds: list[int] = None) -> list[(np.matrix, np.matrix)]:
    pairs = makePairs(pop)
    crossed = []
    if seeds and len(seeds) < len(pairs):
        return []
    for index, pair in enumerate(pairs):
        if seeds:
            boardTuple1, boardTuple2 = singleCrossoverOperation(pair[0], pair[1], crossoverProb, seeds[index])
        else:
            boardTuple1, boardTuple2 = singleCrossoverOperation(pair[0], pair[1], crossoverProb, None)
        crossed.append(boardTuple1)
        crossed.append(boardTuple2)
    if len(pop) % 2 != 0:
        crossed.pop()
    return crossed


def singleCrossoverOperation(boardTuple1: (np.matrix, np.matrix), boardTuple2: (np.matrix, np.matrix), crossoverProb: float, seed: int) -> list[(np.matrix, np.matrix), (np.matrix, np.matrix)]:
    if seed:
        np.random.seed(seed)
    if np.random.rand() < crossoverProb:
        newBoard1 = deepcopy(boardTuple1[0])
        newBoardMask1 = deepcopy(boardTuple1[1])
        newBoard2 = deepcopy(boardTuple2[0])
        newBoardMask2 = deepcopy(boardTuple2[1])
        crossoverPoint = np.random.randint(0, newBoard1.shape[0])
        board1Rows = newBoard1[:crossoverPoint, :]
        board1Mask = newBoardMask1[:crossoverPoint, :]
        board2Rows = newBoard2[crossoverPoint:, :]
        board2Mask = newBoardMask2[crossoverPoint:, :]
        newBoard1[crossoverPoint:, :] = board2Rows
        newBoardMask1[crossoverPoint:, :] = board2Mask
        newBoard2[:crossoverPoint, :] = board1Rows
        newBoardMask2[:crossoverPoint, :] = board1Mask
        return [(newBoard1, newBoardMask1), (newBoard2, newBoardMask2)]
    return [boardTuple1, boardTuple2]


def mutation(pop: list[(np.matrix, np.matrix)], mutationProb: float = 0.5, seeds: list[int] = None) -> list[(np.matrix, np.matrix)]:
    mutated = []
    if seeds and len(seeds) < len(pop):
        return []
    for index, boardTuple in enumerate(pop):
        if seeds:
            newBoardTuple = singleMutationOperation(boardTuple[0], boardTuple[1], mutationProb, seeds[index])
        else:
            newBoardTuple = singleMutationOperation(boardTuple[0], boardTuple[1], mutationProb, None)
        mutated.append(newBoardTuple)
    return mutated


def singleMutationOperation(board: np.matrix, boardMask: np.matrix, mutationProb: float, seed: int) -> tuple[np.matrix, np.matrix]:
    mutatedBoard = deepcopy(board)
    mutatedBoardMask = deepcopy(boardMask)
    validIndexes = []
    for row in range(mutatedBoard.shape[0]):
        for column in range(mutatedBoard.shape[1]):
            if not mutatedBoardMask[row, column]:
                validIndexes.append((row, column))
    if len(validIndexes) >= 2:
        indexList = [index for index in range(len(validIndexes))]
        maxMutations = int(len(validIndexes) / 2)
        for mutationNumber in range(maxMutations):
            if seed:
                np.random.seed(seed)
                seed = np.random.randint(1, 100)
            if np.random.rand() < mutationProb:
                index1, index2 = np.random.choice(indexList, size=2, replace=False)
                indexList.remove(index1)
                indexList.remove(index2)
                index1 = validIndexes[index1]
                index2 = validIndexes[index2]
                mutatedBoard[index1[0], index1[1]], mutatedBoard[index2[0], index2[1]] = (
                    mutatedBoard[index2[0], index2[1]],
                    mutatedBoard[index1[0], index1[1]],
                )
    return (mutatedBoard, mutatedBoardMask)


def genethicAlgorithm(
    pop0: list[(np.matrix, np.matrix)],
    maxIter: int = 200,
    tournamentSize: int = 2,
    crossoverProb: float = 0.5,
    mutationProb: float = 0.5,
    maxEvaluations: int = float("inf"),
    selection=tournamentSelection,
    crossover=crossover,
    mutation=mutation,
    optimization=min,
    q=q,
) -> tuple[int, (np.matrix, np.matrix), list[int]]:
    sollutions = []
    bestSollution = optimization(pop0, key=q)
    bestScore = q(optimization(pop0, key=q))
    pop = pop0
    popSize = len(pop)
    evaluations = popSize + 1
    for iteration in range(maxIter):
        if evaluations >= maxEvaluations:
            return bestScore, bestSollution, sollutions, evaluations
        selected = selection(pop, tournamentSize)
        evaluations += popSize
        crossed = crossover(selected, crossoverProb)
        mutated = mutation(crossed, mutationProb)
        currentBest = optimization(mutated, key=q)
        currentBestScore = q(currentBest)
        evaluations += popSize + 1
        sollutions.append(currentBestScore)
        bestScore = optimization(bestScore, currentBestScore)
        if bestScore == currentBestScore:
            bestSollution = currentBest
        if bestScore == 0:
            return bestScore, bestSollution, sollutions, evaluations
        pop = mutated
    return bestScore, bestSollution, sollutions, evaluations
