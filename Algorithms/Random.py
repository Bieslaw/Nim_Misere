import random

from Algorithms.AlgorithmBase import AlgorithmBase, Move


class Random(AlgorithmBase):
    def get_move(self, stacks: list[int], depth: int) -> Move:
        non_zero_indices = [i for i, stack in enumerate(stacks) if stack > 0]
        non_zero_stacks = [stacks[i] for i in non_zero_indices]
        
        stack_index = random.randint(0, len(non_zero_stacks) - 1)
        items_to_remove = random.randint(1, non_zero_stacks[stack_index])
        return Move(stack_index=non_zero_indices[stack_index], items_to_remove=items_to_remove)
    
    @classmethod
    def get_name(cls) -> str:
        return "Random"
    
    def _uses_depth(self) -> bool:
        return False
