from typing import List, Literal

TetrominGrid = List[List[Literal[0, 1]]]


class Tetromino:
    def __init__(self, grid_rotations: List[TetrominGrid], color: str, x=0, y=0):
        self.grid_rotations = grid_rotations
        self.rotation = 0
        self.color = color
        self.x = x
        self.y = y
        self.x = x
        self.y = y

    def width(self) -> int:
        return len(self.current_grid()[0])

    def height(self) -> int:
        return len(self.current_grid())

    def defined_rotations(self) -> int:
        return len(self.grid_rotations)

    def current_rotation_i(self) -> int:
        return self.rotation % len(self.grid_rotations)

    def current_grid(self) -> TetrominGrid:
        return self.grid_rotations[self.rotation % len(self.grid_rotations)]

    def peek_next_grid(self, backward=False) -> TetrominGrid:
        self.rotate(backward)
        next_grid = self.current_grid()
        self.rotate(not backward)
        return next_grid

    def rotate(self, backward=False) -> None:
        self.rotation += 1 if not backward else -1

    def debug_print(self) -> None:
        for row in self.current_grid():
            print(row)


class TetrominoI(Tetromino):
    def __init__(self, x=0, y=0):
        super().__init__([
            [
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0]
            ],
            [
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]
            ]
        ], 'cyan3', x, y)


class TetrominoJ(Tetromino):
    def __init__(self, x=0, y=0):
        super().__init__([
            [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 1],
                [0, 1, 0],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 0, 1]
            ],
            [
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 0]
            ]
        ], 'DodgerBlue3', x, y)


class TetrominoL(Tetromino):
    def __init__(self, x=0, y=0):
        super().__init__([
            [
                [0, 0, 1],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 1]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [1, 0, 0]
            ],
            [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 0]
            ]
        ], 'orange', x, y)


class TetrominoO(Tetromino):
    def __init__(self, x=0, y=0):
        super().__init__([
            [
                [1, 1],
                [1, 1]
            ]
        ], 'yellow2', x, y)


class TetrominoS(Tetromino):
    def __init__(self, x=0, y=0):
        super().__init__([
            [
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 0, 1]
            ],
            [
                [0, 0, 0],
                [0, 1, 1],
                [1, 1, 0]
            ],
            [
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
        ], 'green', x, y)


class TetrominoT(Tetromino):
    def __init__(self, x=0, y=0):
        super().__init__([
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 1, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
        ], 'purple', x, y)


class TetrominoZ(Tetromino):
    def __init__(self, x=0, y=0):
        super().__init__([
            [
                [1, 1, 0],
                [0, 1, 1],
                [0, 0, 0]
            ],
            [
                [0, 0, 1],
                [0, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 0],
                [0, 1, 1]
            ],
            [
                [0, 1, 0],
                [1, 1, 0],
                [1, 0, 0]
            ]
        ], 'red4', x, y)


tetromin_list = [
    TetrominoI,
    TetrominoO,
    TetrominoT,
    TetrominoJ,
    TetrominoL,
    TetrominoS,
    TetrominoZ
]
