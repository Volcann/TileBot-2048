import os
from game_logic.game_logic import GameLogic

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    game_logic = GameLogic()
    game_logic.print_matrix()
    
    while True:
        try:
            value = game_logic.random_value()
            print("Number: ")
            print(value)
            column = int(input(f"Enter column (0-{len(game_logic._matrix[0])-1}): "))
        
            game_logic.add_to_colomn(
                value=value, 
                colomn=column
            )
            clear_terminal()
            game_logic.print_matrix()
            print(f"Score: {game_logic.get_score()}\n")
        
        except (ValueError, IndexError):
            print("Invalid input! Try again.")
