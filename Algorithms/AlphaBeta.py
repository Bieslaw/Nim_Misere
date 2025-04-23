import math
from Algorithms.AlgorithmBase import AlgorithmBase, Move


class AlphaBetaAlgorithm(AlgorithmBase):        
    def get_move(self, stacks: list[int], depth: int) -> Move:
        non_zero_indices = [i for i, stack in enumerate(stacks) if stack > 0]
        non_zero_stacks = [stacks[i] for i in non_zero_indices]

        chosen_move = self.alphabeta_move(non_zero_stacks, depth)
        return Move(stack_index=non_zero_indices[chosen_move.stack_index], items_to_remove=chosen_move.items_to_remove)
    
    def _uses_depth(self) -> bool:
        return True

    def alphabeta_move(self, stacks: list[int], depth: int) -> Move:
        best_value = -math.inf
        chosen_move = Move(stack_index=0, items_to_remove=1)
                
        for stack in range(len(stacks)):
            for i in range(1, stacks[stack]+1):  
                stacks[stack] = stacks[stack] - i
                value = self.alphabeta_search(stacks, depth, -math.inf, math.inf, -1)
                stacks[stack] = stacks[stack] + i
                
                if best_value <= value:
                    best_value = value
                    chosen_move = Move(stack_index=stack, items_to_remove=i)
                    
        return chosen_move
        
    def alphabeta_search(self, stacks: list[int], depth: int, alpha: int, beta: int, our_turn: bool) -> int:
        if len(stacks) == 0:
            return 1 if our_turn else -1

        if depth == 0:
            return 0

        if not our_turn:
            for stack in range(len(stacks)):
                for i in range(1, stacks[stack]+1):  
                    stacks[stack] = stacks[stack] - i
                    beta = min(beta, self.alphabeta_search(stacks, depth-1, alpha, beta, 1))
                    stacks[stack] = stacks[stack] + i
                    
                    if alpha >= beta or alpha == 1:
                        break
                    
                if alpha >= beta or alpha == 1:
                        break
            return beta
        else:
            for stack in range(len(stacks)):
                for i in range(1, stacks[stack]+1):  
                    stacks[stack] = stacks[stack] - i
                    alpha = max(alpha, self.alphabeta_search(stacks, depth-1, alpha, beta, -1))
                    stacks[stack] = stacks[stack] + i
                    
                    if alpha >= beta or beta == -1:
                        break
                    
                if alpha >= beta or beta == -1:
                        break
            return alpha
