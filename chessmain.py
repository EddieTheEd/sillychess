import chess
import chess.svg
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,   100,   1100,   1100)
        
        layout = QVBoxLayout(self)
        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10,   10,   1080,   1080)
        layout.addWidget(self.widgetSvg)
        
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
            size=1080
        ).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            square_size =  1080 //  8
            local_pos = event.pos() - self.widgetSvg.geometry().topLeft()
            x_offset =  0
            y_offset =  30
            file = ((local_pos.x() + x_offset) // square_size)
            rank =  7 - ((local_pos.y() + y_offset) // square_size)
            square = rank *  8 + file
            if self.selected_piece:
                move = chess.Move(self.selected_square, square)
                if move in self.chessboard.legal_moves:
                    self.chessboard.push(move)
                    self.print_fen()
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
    while True:
        nextmove = input("Next move:\n")
        try:
            window.chessboard.push_san(nextmove)
            window.print_fen()  # Call the FEN printing function here
            window.update_board()
            window.outcome_check()
        except ValueError:
            print("Incorrect move.")
    app.exec_()
