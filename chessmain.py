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

    def print_fen(self):
        fen = self.chessboard.fen()
        print(f"Current FEN: {fen}")


    def update_board(self, move_squares=None):
        fill_map = {}
        if move_squares:
            for square in move_squares:
                fill_map[square] = '#ff0000'  # Red color for highlighting
        self.chessboardSvg = chess.svg.board(
            self.chessboard,
            fill=fill_map,
            size=1080
        ).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

# Modify the mousePressEvent method to pass the squares of possible moves
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            square_size =  1080 //  8
            local_pos = event.pos() - self.widgetSvg.geometry().topLeft()
            x_offset =  0
            y_offset =  30
            file = ((local_pos.x() + x_offset) // square_size)
            rank =  7 - ((local_pos.y() + y_offset) // square_size)
            piece = self.chessboard.piece_at(rank *  8 + file)
            if piece:
                algebraic_notation = chess.square_name(rank *  8 + file)
                legal_moves = [move for move in self.chessboard.legal_moves if move.from_square == rank *  8 + file]
                print(f"Possible moves for {algebraic_notation}: {', '.join(str(move) for move in legal_moves)}")
                # Highlight the squares of the possible moves
                self.update_board(move_squares=[move.to_square for move in legal_moves])
            else:
                print("No piece found at the clicked position.")
                # Clear the highlighted squares
                self.update_board()


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
        except ValueError:
            print("Incorrect move.")
    app.exec_()
