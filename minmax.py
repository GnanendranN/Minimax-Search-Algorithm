import time

class Game:

    def __init__(self):
        self.initialize_game()

    # Initialize the game
    def initialize_game(self):
        self.current_state = [
            ['.', '.', '.'],
            ['.', '.', '.'],
            ['.', '.', '.']
        ]

        
        self.player_turn = 'X'                                      # Player X always plays first

    # Display the board
    def draw_board(self):
        for i in range(0, 3):
            for j in range(0, 3):
                print('{}|'.format(self.current_state[i][j]), end=" ")
            print()
        print()

    # Check whether the given position is valid
    def is_valid(self, px, py):
        if px < 0 or px > 2 or py < 0 or py > 2:
            return False

        elif self.current_state[px][py] != '.':
            return False

        else:
            return True

    # Check whether the game has ended
    def is_end(self):

        # Vertical win
        for i in range(0, 3):
            if (self.current_state[0][i] != '.' and
                    self.current_state[0][i] == self.current_state[1][i] and
                    self.current_state[1][i] == self.current_state[2][i]):

                return self.current_state[0][i]

        # Horizontal win
        for i in range(0, 3):

            if self.current_state[i] == ['X', 'X', 'X']:
                return 'X'

            elif self.current_state[i] == ['O', 'O', 'O']:
                return 'O'

        # Main diagonal
        if (self.current_state[0][0] != '.' and
                self.current_state[0][0] == self.current_state[1][1] and
                self.current_state[0][0] == self.current_state[2][2]):

            return self.current_state[0][0]

        # Second diagonal
        if (self.current_state[0][2] != '.' and
                self.current_state[0][2] == self.current_state[1][1] and
                self.current_state[0][2] == self.current_state[2][0]):

            return self.current_state[0][2]

        # Check whether the board is full
        for i in range(0, 3):
            for j in range(0, 3):

                if self.current_state[i][j] == '.':
                    return None

        # Board is full and nobody wins
        return '.'

    # MAX function
    # O is the maximizing player
    def max(self):

        # -1 = X wins
        #  0 = Tie
        #  1 = O wins

        maxv = -2

        px = None
        py = None

        result = self.is_end()

        # If the game has ended
        if result == 'X':
            return (-1, 0, 0)

        elif result == 'O':
            return (1, 0, 0)

        elif result == '.':
            return (0, 0, 0)

        # Try every possible move
        for i in range(0, 3):
            for j in range(0, 3):

                # Check whether the cell is empty
                if self.current_state[i][j] == '.':

                    # O makes a temporary move
                    self.current_state[i][j] = 'O'

                    # Call MIN to simulate X's response
                    (m, min_i, min_j) = self.min()

                    # O wants the maximum value
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j

                    # Undo the temporary move
                    self.current_state[i][j] = '.'

        return (maxv, px, py)

    # MIN function
    # X is the minimizing player
    def min(self):

        # -1 = X wins
        #  0 = Tie
        #  1 = O wins

        minv = 2

        qx = None
        qy = None

        result = self.is_end()

        # If the game has ended
        if result == 'X':
            return (-1, 0, 0)

        elif result == 'O':
            return (1, 0, 0)

        elif result == '.':
            return (0, 0, 0)

        # Try every possible move
        for i in range(0, 3):
            for j in range(0, 3):

                # Check whether the cell is empty
                if self.current_state[i][j] == '.':

                    # X makes a temporary move
                    self.current_state[i][j] = 'X'

                    # Call MAX to simulate O's response
                    (m, max_i, max_j) = self.max()

                    # X wants the minimum value
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j

                    # Undo the temporary move
                    self.current_state[i][j] = '.'

        return (minv, qx, qy)

    # Main game function
    def play(self):

        while True:

            # Display board
            self.draw_board()

            # Check game status
            self.result = self.is_end()

            # If game has ended
            if self.result != None:

                if self.result == 'X':
                    print('The winner is X!')

                elif self.result == 'O':
                    print('The winner is O!')

                elif self.result == '.':
                    print("It's a tie!")

                # Reset the game
                self.initialize_game()
                return

            # Human player's turn
            if self.player_turn == 'X':

                while True:

                    # Calculate recommended move using MINIMAX
                    start = time.time()

                    (m, qx, qy) = self.min()

                    end = time.time()

                    print(
                        'Evaluation time: {}s'.format(
                            round(end - start, 7)
                        )
                    )

                    print(
                        'Recommended move: X = {}, Y = {}'.format(
                            qx, qy
                        )
                    )

                    # Get human player's move
                    try:
                        px = int(input('Insert the X coordinate: '))
                        py = int(input('Insert the Y coordinate: '))
                    except ValueError:
                        print('Please enter numbers between 0 and 2.')
                        continue

                    # Check whether move is valid
                    if self.is_valid(px, py):

                        # Place X
                        self.current_state[px][py] = 'X'

                        # Change turn to O
                        self.player_turn = 'O'

                        break

                    else:
                        print('The move is not valid! Try again.')

            # AI player's turn
            else:

                print("AI (O) is thinking...")

                start = time.time()

                # MAX chooses the best move for O
                (m, px, py) = self.max()

                end = time.time()

                print(
                    'AI evaluation time: {}s'.format(
                        round(end - start, 7)
                    )
                )

                print(
                    'AI chooses: X = {}, Y = {}'.format(
                        px, py
                    )
                )

                # Place O
                self.current_state[px][py] = 'O'

                # Change turn to X
                self.player_turn = 'X'


# Main function
def main():

    g = Game()
    g.play()


# Start the program
if __name__ == "__main__":
    main()