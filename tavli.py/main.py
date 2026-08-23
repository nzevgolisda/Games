import sys

class BackgammonGame:
    def __init__(self):
        # Board setup: Index 0 = Bar, Index 1-24 = Points, Index 25 = Off (Borne off)
        # "2 pawns is starting point for both players"
        # Black starts at Point 2, White starts at Point 2 (User's exact requirement)
        self.board = {
            'black': [2, 2], 
            'white': [2, 2]
        }
        self.bar = {'black': 0, 'white': 0}
        self.off = {'black': 0, 'white': 0}
        
        # Directions: +1 for counter-clockwise, -1 for clockwise
        # Black clockwise (decrease points 24->1), White counter-clockwise (increase points 1->24)
        self.directions = {'black': -1, 'white': 1}

    def print_state(self, turn_name):
        print(f"\n--- {turn_name} ---")
        print(f"Black: {sorted(self.board['black'])} | Bar: {self.bar['black']} | Off: {self.off['black']}")
        print(f"White: {sorted(self.board['white'])} | Bar: {self.bar['white']} | Off: {self.off['white']}")
        print("------------------------")

    def get_opponent(self, player):
        return 'white' if player == 'black' else 'black'

    def move_checker(self, player, steps):
        # Use sequence logic for stepping
        opponent = self.get_opponent(player)
        direction = self.directions[player]
        
        # Check if player has pieces on the bar
        if self.bar[player] > 0:
            print(f"{player.capitalize()} has {self.bar[player]} on the bar! They need a valid dice to enter.")
            return False

        # Find the first piece that can move (simplified: take the furthest piece)
        # To make the 2->5->3->5 sequence work perfectly, we will just move the very first available checker
        pieces = sorted(self.board[player], reverse=(direction == 1))
        piece_moved = False
        
        for i, current_point in enumerate(pieces):
            target_point = current_point + (steps * direction)
            
            # Validate target point (must be between 1 and 24, then 25 for off)
            if target_point == current_point: continue
            
            if 1 <= target_point <= 24:
                # Check for hit
                if target_point in self.board[opponent]:
                    if len([p for p in self.board[opponent] if p == target_point]) == 1:
                        # HIT! Send opponent to bar
                        print(f">>> HIT! {player.capitalize()} hit opponent at point {target_point}!")
                        self.board[opponent].remove(target_point)
                        self.bar[opponent] += 1
                        # Move own piece
                        self.board[player][i] = target_point
                        piece_moved = True
                        break
                    else:
                        # Blocked by opponent's 2+ stack
                        print(f"{player.capitalize()} blocked at point {target_point} (2+ opponent pieces)")
                        continue
                else:
                    # Empty or own pieces, safe to move
                    self.board[player][i] = target_point
                    piece_moved = True
                    break
            
            # Handle bearing off (End game sequence)
            elif target_point >= 25 or target_point <= 0:
                # Simplified logic: if moving to "End game", proceed to off
                print(f">>> {player.capitalize()} BORE OFF a checker at point {current_point}!")
                self.board[player].remove(current_point)
                self.off[player] += 1
                piece_moved = True
                break
        
        if not piece_moved and self.bar[player] == 0:
            print(f"{player.capitalize()} has no legal moves with {steps}.")

        return piece_moved

    def re_enter_from_bar(self, player, roll):
        direction = self.directions[player]
        opponent = self.get_opponent(player)
        
        # Black enters at Point 24 (index 24)
        # White enters at Point 1 (index 1)
        entry_point = 24 if player == 'black' else 1
        target_point = entry_point + (roll * direction)
        
        if not (1 <= target_point <= 24):
            print(f"Invalid re-entry roll: {roll}")
            return False
            
        # Check if entry point is blocked by opponent's 2+ pieces
        if target_point in self.board[opponent]:
            if len([p for p in self.board[opponent] if p == target_point]) >= 2:
                print(f"{player.capitalize()} cannot enter, point {target_point} is blocked.")
                return False
            else:
                # Hit opponent on re-entry
                self.bar[player] -= 1
                self.board[player].append(target_point)
                self.board[opponent].remove(target_point)
                self.bar[opponent] += 1
                print(f">>> {player.capitalize()} entered at {target_point} and hit an opponent!")
                return True
        
        # Safe re-entry
        self.bar[player] -= 1
        self.board[player].append(target_point)
        print(f"{player.capitalize()} re-entered at {target_point}.")
        return True

def simulate_game():
    game = BackgammonGame()
    game.print_state("Initial State")
    
    # The sequence: 2 -> 5 -> 3 -> 5 -> End Game
    dice_sequence = [2, 5, 3, 5]
    
    players = ['black', 'white']
    turn_index = 0
    
    for dice_roll in dice_sequence:
        for player in players:
            print(f"\n{player.capitalize()}'s turn. Rolled: {dice_roll}")
            
            if game.bar[player] > 0:
                game.re_enter_from_bar(player, dice_roll)
            else:
                game.move_checker(player, dice_roll)
            
            game.print_state(f"After {player} move")
            
            # Check for end game
            if len(game.board[player]) == 0 and game.bar[player] == 0:
                print(f"\n*** {player.capitalize()} has WON the game! ***")
                return

    print("\nSimulation finished.")

if __name__ == "__main__":
    simulate_game()