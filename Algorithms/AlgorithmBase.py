import time

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Move:
    stack_index: int
    items_to_remove: int


class AlgorithmBase(ABC):
    @abstractmethod
    def get_move(self, stacks: list[int], depth: int) -> Move:
        """
        Get next move for the current state of Nim Misère
        
        Args:
            state: List of integers representing the number of items in each stack
            depth: Search depth for algorithms that use it - ignored otherwise
        """
        pass
    
    @abstractmethod
    def _uses_depth(self) -> bool:
        pass
    
    def get_move_timed(self, stacks: list[int], time_for_move: float) -> Move:
        """
        Get next move for the current state of Nim Misère with a time limit.
        While there is time left, bigger depth will be tried.
        
        Args:
            stacks: List of integers representing the number of items in each stack
            time_for_move: Time limit for the move
        """
        if not self._uses_depth():
            return self.get_move(stacks, 0)
        
        start_time = time.time()
        
        depth = 1
        while time.time() - start_time < time_for_move:
            move = self.get_move(stacks, depth)
            depth += 1

        return move
