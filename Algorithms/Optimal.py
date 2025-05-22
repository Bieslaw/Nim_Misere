from Algorithms.AlgorithmBase import AlgorithmBase, Move
from Algorithms.Config.ConfigBase import ConfigBase


class Optimal(AlgorithmBase):
    def get_move(self, stacks: list[int], depth: int) -> Move:
        non_zero_indices = [i for i, stack in enumerate(stacks) if stack > 0]
        non_zero_stacks = [stacks[i] for i in non_zero_indices]
        
        move = self.optimal_nim_move(non_zero_stacks)
        return Move(stack_index=non_zero_indices[move.stack_index], items_to_remove=move.items_to_remove)
    
    def configure(self, config: ConfigBase):
        pass

    def _uses_depth(self) -> bool:
        return False

    @classmethod
    def get_name(cls) -> str:
        return "Optimal"
    
    @staticmethod
    def optimal_nim_move(state: list[int]) -> Move:
        """
        Calculate the optimal move for Misère Nim using nim-sum strategy
        
        Args:
            state: stack sizes (excluding empty stacks)
            
        Returns:
            Move object with stack index and items to take
        """
        if all(s == 1 for s in state):
            # In endgame with only 1s, all moves are equivalent
            return Move(stack_index=0, items_to_remove=1)
        
        # If there is only one stack with more than 1 item, 
        # we need to ensure that after the move we have an odd number of 1s
        if sum(1 for s in state if s > 1) == 1:
            max_stack_idx = state.index(max(state))
            items_to_remove = state[max_stack_idx] - 1 if len(state) % 2 == 1 else state[max_stack_idx]
            return Move(stack_index=max_stack_idx, items_to_remove=items_to_remove)

        nim_sum = 0
        for stack in state:
            nim_sum ^= stack
        
        if nim_sum == 0:
            # If nim-sum is 0, we lose with optimal play - do whatever
            max_stack_idx = state.index(max(state))
            return Move(stack_index=max_stack_idx, items_to_remove=1)
        
        for i, stack in enumerate(state):
            if stack == 1:
                continue

            # Calculate how many to take to get the best nim-sum
            for take in range(1, stack + 1):
                new_stack = stack - take
                new_nim_sum = nim_sum ^ stack ^ new_stack
                
                if new_nim_sum == 0:
                    # This is good unless it leaves only 1s
                    new_state = state.copy()
                    new_state[i] = new_stack
                    if sum(1 for s in new_state if s > 1) == 0:
                        # If this leaves only 1s, ensure odd count for misère win
                        ones_in_new = sum(1 for s in new_state if s == 1)
                        if ones_in_new % 2 == 0:
                            return Move(stack_index=i, items_to_remove=take)
                    else:
                        return Move(stack_index=i, items_to_remove=take)
        
        # this should never happen
        print(f"No winning move found for nim-sum = {nim_sum} ({state})")
        return Move(stack_index=0, items_to_remove=1)
