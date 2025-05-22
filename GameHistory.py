from Algorithms.AlgorithmBase import Move
from NimMisere import NimMisere


class GameHistory:
    def __init__(self, game: NimMisere):
        self.game: NimMisere = game
        self.history: list[Move] = []
        self.behind_by: int = 0

    def step(self, depth: int) -> None:
        if self.behind_by > 0:
            self.behind_by -= 1
            return
        
        move = self.game.step(depth)
        self.history.append(move)

    def step_timed(self, time_in_seconds: float) -> None:
        if self.behind_by > 0:
            self.behind_by -= 1
            return
        
        move = self.game.step_timed(time_in_seconds)
        self.history.append(move)

    def get_stacks(self) -> list[int]:
        stacks = self.game.stacks.copy()
        for move in list(reversed(self.history))[:self.behind_by]:
            stacks = self._revert_move(stacks, move)
            
        return stacks
    
    def step_back(self) -> None:
        if self.behind_by >= len(self.history):
            return
        
        self.behind_by += 1
    
    @staticmethod
    def _revert_move(stacks: list[int], move: Move) -> list[int]:
        stacks[move.stack_index] += move.items_to_remove
        return stacks
