from config.constants import GRID_LENGTH, GRID_WIDTH
import random

class GameLogic:
    def __init__(self):
        self._matrix = [[0] * GRID_LENGTH for i in range(GRID_WIDTH)]
        self._score = 0
        
    def random_value(self):
        existing_values = set()
        for i in range(GRID_LENGTH):
            for j in range(GRID_WIDTH):
                if self._matrix[i][j] != 0:
                    existing_values.add(self._matrix[i][j])
    
        if not existing_values:
            return random.choice([2, 4])
        
        return random.choice(list(existing_values))
    
    def print_matrix(self):
        for row in self._matrix:
            print(row)
        print()
    
    def add_to_colomn(self, value, colomn):
        i = 0
        while True:
            if i == GRID_LENGTH:
                print("Colomn is already full")
                break
            
            if self._matrix[i][colomn] == 0:
                self._matrix[i][colomn] = value
                self.merge(i ,colomn)
                break
            else:
                i+=1
        return
    
    def merge(self, row, col):
        value = self._matrix[row][col]
        if value == 0:
            return

        directions = [
            (1, 0),   # down
            (-1, 0),  # up
            (0, 1),   # right
            (0, -1),  # left
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc

            if 0 <= r < GRID_LENGTH and 0 <= c < GRID_WIDTH:
                if self._matrix[r][c] == value:
                    self._matrix[row][col] *= 2
                    self._score += self._matrix[row][col]
                    self._matrix[r][c] = 0
                    return  # merge only once
                
    def get_score(self):
        return self._score