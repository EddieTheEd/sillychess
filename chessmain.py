import chess
import chess.svg
import datetime
from chess.pgn import Game
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,   100,   1100,   1100)

        self.firstmove = True

        self.game = Game()
        self.game.headers["Event"] = "Custom Event"
        self.game.headers["White"] = "Player  1"
        self.game.headers["Black"] = "Player  2"
        self.game.headers["Date"] = datetime.datetime.now().isoformat()
        self.game.headers["Result"] = "*"
        
        layout = QVBoxLayout(self)
        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10,   10,   1080,   1080)
        layout.addWidget(self.widgetSvg)

        self.setWindowFlags(Qt.Window)
        
        self.chessboard = chess.Board()
        self.update_board()

        self.selected_piece = None
        self.selected_square = None
        self.fen = None

    def outcome_check(self):
        outcome = self.chessboard.outcome()
        if outcome:
            if outcome.termination == chess.Termination.CHECKMATE:
                winner = 'White' if outcome.winner == chess.WHITE else 'Black'
                print(f"{winner} wins by checkmate!")
            elif outcome.termination == chess.Termination.STALEMATE:
                print("The game ended in a stalemate.")
            else:
                print(f"Game over: {outcome.termination}")
            self.game.headers["Result"] = str(self.chessboard.result())
            print(str(self.game))
        return outcome

    def print_fen(self):
        self.fen = self.chessboard.fen()
        print(f"Current FEN: {self.fen}")

    def update_board(self, move_squares=None):
        fill_map = {}
        if move_squares:
            for square in move_squares:
                fill_map[square] = '#003153'
        self.chessboardSvg = chess.svg.board(
            self.chessboard,
            fill=fill_map,
            size=1100,
            coordinates=False
        ).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            square_size =  1100 //  8
            local_pos = event.pos() - self.widgetSvg.geometry().topLeft()
            x_offset =  0
            y_offset =  0
            file = ((local_pos.x() + x_offset) // square_size)
            rank =  7 - ((local_pos.y() + y_offset) // square_size)
            square = rank *  8 + file
            if self.selected_piece:
                move = chess.Move(self.selected_square, square)
                if self.chessboard.piece_at(self.selected_square).piece_type == chess.PAWN and \
                   ((self.chessboard.turn == chess.WHITE and rank ==  7) or \
                    (self.chessboard.turn == chess.BLACK and rank ==  0)):
                    move.promotion = chess.QUEEN  # Promote to queen
                if move in self.chessboard.legal_moves:
                    self.chessboard.push(move)
                    
                    # we send this move!
                    #self.print_fen()
                    if self.firstmove:
                        self.node = self.game.add_variation(move)
                        self.firstmove = False
                    else:
                        self.node = self.node.add_variation(move)
                    window.outcome_check()
                    self.update_board()
                    self.selected_piece = None
                    self.selected_square = None
                else:
                    self.update_board()
                    self.selected_piece = None
                    self.selected_square = None
            if self.chessboard.piece_at(square):
                self.selected_piece = self.chessboard.piece_at(square)
                self.selected_square = square
                legal_moves = [move for move in self.chessboard.legal_moves if move.from_square == square]
                self.update_board(move_squares=[move.to_square for move in legal_moves])

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
