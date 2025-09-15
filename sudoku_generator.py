import math, random

class SudokuGenerator:

    def __init__(self, removed_cells, row_length = 9):
        #just initialising the variables 
        self.box_length = int(math.sqrt(row_length))
        self.row_length = row_length
        # Ensure board size is a perfect square
        if int(math.sqrt(row_length)) ** 2 != row_length:
            raise ValueError("Row length must be a perfect square (e.g., 9 for a 9x9 Sudoku board)")
        self.removed_cells = int(removed_cells)
        self.board = [[0 for _ in range(self.row_length)] for _ in range(self.row_length)] #made the board an array of 0s 

    def get_board(self):
        return self.board #literally just the same thing that was set to self.board in line 11

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) if num != 0 else '-' for num in row)) #this is just a print function to print the board in a readable format


    def valid_in_row(self, row, num):
        return num not in self.board[row] #checks if the number is in the row or not

    def valid_in_col(self, col, num):
        return all(self.board[row][col] != num for row in range(self.row_length)) #checks if the number is in the column or not

    def valid_in_box(self, row_start, col_start, num):
        for i in range(row_start, row_start + self.box_length): 
            for j in range(col_start, col_start + self.box_length): #checks if the number is in the box or not
                if self.board[i][j] == num: #if the number is in the box, return false
                    return False
        return True

    def is_valid(self, row, col, num):
        # Temporarily clear current cell value for accurate validation
        current = self.board[row][col]
        self.board[row][col] = 0
        valid = (self.valid_in_row(row, num) and
                 self.valid_in_col(col, num) and
                 self.valid_in_box(row - row % self.box_length, col - col % self.box_length, num))
        self.board[row][col] = current  # Restore value
        return valid #checks if the number is valid or not by checking if it is in the row, column and box

    def fill_box(self, row_start, col_start):
        nums = list(range(1, self.row_length + 1)) #creates a list of numbers from 1 to 9
        random.shuffle(nums)    #shuffles the numbers randomly
        for i in range(row_start, row_start + self.box_length): #fills the box with the numbers
            for j in range(col_start, col_start + self.box_length): 
                self.board[i][j] = nums.pop() #pops the number from the list and fills the box with it

    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):    
            self.fill_box(i, i) #fills the diagonal boxes with the numbers

    def fill_remaining(self, row, col): 
        if col >= self.row_length and row < self.row_length - 1:
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        for num in range(1, self.row_length + 1): 
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, 0)

    def remove_cells(self): 
        cells_removed = 0  
        while cells_removed < self.removed_cells:
            i = random.randint(0, self.row_length - 1) 
            j = random.randint(0, self.row_length - 1)
            if self.board[i][j] != 0:
                self.board[i][j] = 0
                cells_removed += 1 
    
    def is_board_complete(self):
        for row in range(self.row_length):
            for col in range(self.row_length):
                if self.board[row][col] == 0 or not self.is_valid(row, col, self.board[row][col]):
                    return False
        return True
    
    def set_value(self, row, col, value):
        if self.board[row][col] == 0 and self.is_valid(row, col, value):
            self.board[row][col] = value
            return True
        return False
    
def generate_sudoku(removed):
    sudoku = SudokuGenerator(removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

# def generate_sudoku_and_solutions(removed):
#     sudoku = SudokuGenerator(removed)
#     sudoku.fill_values()
#     solution=sudoku.board
#     sudoku.remove_cells()
#     board = sudoku.board
#     return board,solution
#same thing as last but also gets solution for sudoku
