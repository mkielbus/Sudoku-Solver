try:
    from Board import Board, BOARD_SIZE
except ModuleNotFoundError:
    from ACO.Board import Board, BOARD_SIZE


def get_boards_from_file(file_path: str) -> list[Board]:
    demo_boards = []
    with open(file_path, "r") as f:
        demo_boards = f.readlines()
    boards = []
    for demo_board in demo_boards:
        board = create_board_from_str(demo_board)
        boards.append(board)
    return boards

def create_board_from_str(board_str: str) -> Board:
    board = []
    for col in range(BOARD_SIZE):
        board.append([])
        for row in range(BOARD_SIZE):
            char = board_str[col * BOARD_SIZE + row]
            if char == ".":
                board[col].append(0)
            else:
                board[col].append(int(char))
    board = Board(board)
    return board