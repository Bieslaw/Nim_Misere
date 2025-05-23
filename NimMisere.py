from Algorithms.AlgorithmBase import AlgorithmBase, Move


class NimMisere:
    def __init__(self, stacks: list[int], first_player: AlgorithmBase, second_player: AlgorithmBase):
        self.stacks: list[int] = stacks
        self.first_player: AlgorithmBase = first_player
        self.second_player: AlgorithmBase = second_player
        
        self.first_player_turn: bool = True
        
    def get_result(self) -> bool | None:
        """
        Returns True if the first player wins, False if the second player wins, and None if the game is still in progress.
        """
        if all(stack == 0 for stack in self.stacks):
            return self.first_player_turn
        return None
    
    def get_winner_name(self) -> str | None:
        if self.get_result() is None:
            return None
        
        return self.first_player.get_name() if self.get_result() else self.second_player.get_name()
    
    def get_current_player_name(self) -> str:
        return self.first_player.get_name() if self.first_player_turn else self.second_player.get_name()
    
    def step(self, depth: int) -> Move:
        if self.get_result() is not None:
            return
        
        if self.first_player_turn:
            move = self.first_player.get_move(self.stacks, depth)
        else:
            move = self.second_player.get_move(self.stacks, depth)

        self.stacks[move.stack_index] -= move.items_to_remove
        self.first_player_turn = not self.first_player_turn

        return move
        
    def step_timed(self, time_in_seconds: float) -> Move:
        if self.get_result() is not None:
            return
        
        if self.first_player_turn:
            move = self.first_player.get_move_timed(self.stacks, time_in_seconds)
        else:
            move = self.second_player.get_move_timed(self.stacks, time_in_seconds)

        self.stacks[move.stack_index] -= move.items_to_remove
        self.first_player_turn = not self.first_player_turn

        return move
