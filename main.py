import random
from typing import Optional

players = ['WHITE', 'BLACK']

initial_board = {
    'A': ['R', 'P', None, None, None, None, 'p', 'r'],
    'B': ['N', 'P', None, None, None, None, 'p', 'n'],
    'C': ['B', 'P', None, None, None, None, 'p', 'b'],
    'D': ['Q', 'P', None, None, None, None, 'p', 'q'],
    'E': ['K', 'P', None, None, None, None, 'p', 'k'],
    'F': ['B', 'P', None, None, None, None, 'p', 'b'],
    'G': ['N', 'P', None, None, None, None, 'p', 'n'],
    'H': ['R', 'P', None, None, None, None, 'p', 'r']
}



COLORS = [WHITE, BLACK] = [True, False]
COLOR_NAMES = ["black", "white"]

PieceType = int
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(1, 7)
PIECE_SYMBOLS = [None, "p", "n", "b", "r", "q", "k"]
PIECE_NAMES = [None, "pawn", "knight", "bishop", "rook", "queen", "king"]

Square = int
SQUARES = [
    A1, B1, C1, D1, E1, F1, G1, H1,
    A2, B2, C2, D2, E2, F2, G2, H2,
    A3, B3, C3, D3, E3, F3, G3, H3,
    A4, B4, C4, D4, E4, F4, G4, H4,
    A5, B5, C5, D5, E5, F5, G5, H5,
    A6, B6, C6, D6, E6, F6, G6, H6,
    A7, B7, C7, D7, E7, F7, G7, H7,
    A8, B8, C8, D8, E8, F8, G8, H8,
] = range(64)

UNICODE_PIECES = {
    'K': '♚', 'k': '♔',
    'Q': '♛', 'q': '♕',
    'R': '♜', 'r': '♖',
    'B': '♝', 'b': '♗',
    'N': '♞', 'n': '♘',
    'P': '♟︎', 'p': '♙'  
}

UNICODE_SQUARES = {
    WHITE: '◼',
    BLACK: '◻'
}

def invert_player_color(player_color):
    if player_color == WHITE:
        return BLACK
    if player_color == BLACK:
        return WHITE
    return None


    
class Piece:
    def __init__(self, color, piece_id: str, allowed_directions) -> None:
        self.color = color
        self.allowed_directions = allowed_directions
        self.no_of_moves = 0
        self.piece_id = piece_id.upper() if color == WHITE else piece_id.lower()

    def piece_has_been_moved(self) -> bool:
        return self.no_of_moves > 0
    
    def update_after_move(self):
        self.no_of_moves += 1

    def get_max_no_of_steps(self):
        return 1
    
    def __str__(self) -> str:
        return UNICODE_PIECES[self.piece_id]
    
    def __repr__(self):
        return self.__str__()

class MultiStepPiece(Piece):
    def __init__(self, color, piece_id, allowed_directions) -> None:
        super().__init__(color,piece_id,  allowed_directions)

    def get_max_no_of_steps(self):
        return 8
    
directions = {
    'STRAIGHT': [(0, 1), (0, -1), (1, 0), (-1, 0)],
    'DIAGONAL': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
    'KNIGHT': [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
}

class pawn(Piece):
    def __init__(self, color) -> None:
        super().__init__(color, 'P', [(0, 1)] if color == WHITE else [(0, -1)])

    def get_max_no_of_steps(self):
        return 1 if self.piece_has_been_moved() else 2
    def __str__(self) -> str:
        return UNICODE_PIECES[self.piece_id]
    
class rook(MultiStepPiece):
    def __init__(self, color) -> None:
        super().__init__(color, 'R', directions['STRAIGHT'])

class bishop(MultiStepPiece):
    def __init__(self, color) -> None:
        super().__init__(color, 'B', directions['DIAGONAL'])
    
class knight(Piece):
    def __init__(self, color) -> None:
        super().__init__(color, 'N', directions['KNIGHT'])

class queen(MultiStepPiece):
    def __init__(self, color) -> None:
        super().__init__(color, 'Q', directions['STRAIGHT'] + directions['DIAGONAL'])

class king(Piece):
    def __init__(self, color) -> None:
        super().__init__(color, 'K', directions['STRAIGHT'] + directions['DIAGONAL'])

class Board:

    COLUMN_INDICES = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    BOARD_COLUMNS = list(COLUMN_INDICES.keys())

    def __init__(self) -> None:
        self.state = Board.get_initial_state()
        self.active_pieces = self.get_active_pieces()
        self.kings = {
            WHITE: self.state['E'][0],
            BLACK: self.state['E'][7]
        }
        self.last_moved_piece = None
        self.previous_square = None
        self.last_piece_taken = None
        self.last_pawn_exchanged = None

    def get_initial_state():
        return {
            'A': [rook(WHITE),   pawn(WHITE), None, None, None, None, pawn(BLACK), rook(BLACK)],
            'B': [knight(WHITE), pawn(WHITE), None, None, None, None, pawn(BLACK), knight(BLACK)],
            'C': [bishop(WHITE), pawn(WHITE), None, None, None, None, pawn(BLACK), bishop(BLACK)],
            'D': [queen(WHITE),  pawn(WHITE), None, None, None, None, pawn(BLACK), queen(BLACK)],
            'E': [king(WHITE),   pawn(WHITE), None, None, None, None, pawn(BLACK), king(BLACK)],
            'F': [bishop(WHITE), pawn(WHITE), None, None, None, None, pawn(BLACK), bishop(BLACK)],
            'G': [knight(WHITE), pawn(WHITE), None, None, None, None, pawn(BLACK), knight(BLACK)],
            'H': [rook(WHITE),   pawn(WHITE), None, None, None, None, pawn(BLACK), rook(BLACK)]
        }
    
    def get_active_pieces(self):
        active_pieces = {
            WHITE: {}, 
            BLACK: {}
        }
        for col_key, col in self.state.items():
            for row_index, piece in enumerate(col):
                if piece != None:
                    active_pieces[piece.color][piece] = (col_key, row_index)
        return active_pieces
    
    def get_piece_position(self, piece: Piece):
        return self.active_pieces[piece.color][piece]
    
    def undo_last_move(self):
        current_pos = self.get_piece_position(self.last_moved_piece)
        if self.last_piece_taken != None:
            self.state[current_pos[0]][current_pos[1]] = self.last_piece_taken
            self.active_pieces[self.last_piece_taken.color][self.last_piece_taken] = current_pos
        else:
            self.state[current_pos[0]][current_pos[1]] = None
        if self.last_pawn_exchanged != None:
            self.state[self.previous_square[0]][self.previous_square[1]] = self.last_pawn_exchanged
            self.active_pieces[self.last_pawn_exchanged.color][self.last_pawn_exchanged] = self.previous_square
        else:    
            self.state[self.previous_square[0]][self.previous_square[1]] = self.last_moved_piece
            self.active_pieces[self.last_moved_piece.color][self.last_moved_piece] = self.previous_square

    def execute_move(self, piece: Piece, target_square):
        def position_is_opposite_end(color, row_index):
            return (color == WHITE and row_index == 7) or (color == BLACK and row_index == 0)

        dead_piece = self.state[target_square[0]][target_square[1]]
        if dead_piece != None:
            self.active_pieces[dead_piece.color].pop(dead_piece, None)

        old_square = self.get_piece_position(piece)
        self.state[old_square[0]][old_square[1]] = None

        self.last_moved_piece = piece
        self.previous_square = old_square
        self.last_piece_taken = dead_piece
        self.last_pawn_exchanged = None

        # check if a pawn reached the end
        if isinstance(piece, pawn) and position_is_opposite_end(piece.color, target_square[1]):
            self.active_pieces[piece.color].pop(piece, None)
            self.last_pawn_exchanged = piece
            piece = queen(piece.color)
            self.last_moved_piece = piece

        self.state[target_square[0]][target_square[1]] = piece
        self.active_pieces[piece.color][piece] = target_square

    def move_is_within_bounds(col_index: int, row_index: int) -> bool:
        # check if col & row is legal
        if 0 <= col_index < 8 and 0 <= row_index < 8:
            return True
        return False
    
    def get_possible_moves(self, piece: Piece, test_in_check = True):
        # get position of piece
        (col_key, row_index) = self.get_piece_position(piece)

        if piece == None: 
            return []
        col_index = self.COLUMN_INDICES[col_key]
        possible_moves = []
        for direction in piece.allowed_directions:
            move_row = row_index
            move_col = col_index
            for _ in range(piece.get_max_no_of_steps()):
                move_row += direction[1]
                move_col += direction[0]

                if not Board.move_is_within_bounds(move_col, move_row):
                    break

                move_col_name = Board.BOARD_COLUMNS[move_col]

                target_piece: Piece = self.state[move_col_name][move_row]
                if target_piece != None and target_piece.color == piece.color:
                    break

                if test_in_check and self.is_in_check_after_move(piece, (move_col_name, move_row)):
                    break
                
                possible_moves.append((move_col_name, move_row))

                if target_piece != None and target_piece.color != piece.color: # square is owned by enemy (move takes)
                    break

        return possible_moves
    

    def is_in_check(self, player_color):
        opponent_pieces = self.active_pieces[invert_player_color(player_color)]
        for opp_piece in opponent_pieces:
            for move in self.get_possible_moves(opp_piece, False):
                if move == self.active_pieces[player_color][self.kings[player_color]]: # move attacks players king
                    return True
        return False
    
    def is_in_check_after_move(self, piece, move):
        self.execute_move(piece, move)
        in_check = self.is_in_check(piece.color)
        self.undo_last_move()
        return in_check

    def is_check_mate(self, player_color):
        if not self.is_in_check(player_color):
            return False
        
        king_moves = self.get_possible_moves(self.kings[player_color])
        if any(not self.is_in_check_after_move(self.kings[player_color], move) for move in king_moves):
            return False
        
        return True

    def __str__(self) -> str:
        column_strings = []
        for col_key, col in self.state.items():
            col_index = Board.COLUMN_INDICES[col_key]
            row_strings = []
            for i, piece in enumerate(col):
                if piece == None:
                    row_strings.append(UNICODE_SQUARES[BLACK] if (col_index + i) % 2 == 0 else UNICODE_SQUARES[WHITE])
                else:
                    row_strings.append(str(piece))
            column_strings.append(' '.join(row_strings))

        return '\n'.join(column_strings) 
    
class Chess:
    def __init__(self) -> None:
        self.board = Board()
        self.players = {
            WHITE: RandomPlayer(WHITE),
            BLACK: RandomPlayer(BLACK)
        }
        self.player_to_act = WHITE

    def switch_player(self):
        self.player_to_act = invert_player_color(self.player_to_act)

    def is_draw(self):
        return len(self.board.active_pieces[WHITE]) <= 1 and len(self.board.active_pieces[BLACK]) <= 1

    def run(self):
        i = 0
        print(self.board)
        print(f'iterations: {i}')
        while not self.board.is_check_mate(self.player_to_act):
            
            print(f'{self.player_to_act} is next to act...')
            piece, move = self.players[self.player_to_act].get_next_move(self.board)
            if piece == None:
                print("could not find any more random moves!")
                break
            self.board.execute_move(piece, move)
            self.switch_player()
            print(self.board)
            i += 1
            print(f'iterations: {i}')

            if self.is_draw():
                print("Draw!")
                break
            

class Player:
    def __init__(self, color) -> None:
        self.color = color

    def get_next_move(self, board) -> tuple[Piece, tuple]:
        pass

class HumanPlayer(Player):
    def __init__(self, color) -> None:
        super().__init__(color)

class ComputerPlayer(Player):
    def __init__(self, color) -> None:
        super().__init__(color)

class RandomPlayer(Player):
    def __init__(self, color) -> None:
        super().__init__(color)

    def get_next_move(self, board: Board) -> tuple[Piece, tuple]:
        no_of_pieces = len(board.active_pieces[self.color])
        for i in range(no_of_pieces):
            random_piece_index = random.randint(0, no_of_pieces-1)
            random_piece = list(board.active_pieces[self.color].keys())[random_piece_index]
            moves = board.get_possible_moves(random_piece)
            if len(moves) == 0:
                continue
            random_move_index = random.randint(0, len(moves)-1)
            return random_piece, moves[random_move_index]
        return None, None

CHECKMATE = 20000
DRAW = 0
class MiniMaxPlayer(ComputerPlayer):
    def __init__(self, color) -> None:
        super().__init__(color)
        self.max_depth = 10

    def evaluate_score(self, board):
        return 0
    
    def get_next_move(self, board: Board, depth, alpha, beta) -> tuple[Piece, tuple]:
        pass
    
chess_game = Chess()
chess_game.run()





