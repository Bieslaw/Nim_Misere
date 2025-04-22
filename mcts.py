import math
import random
from typing import List, Tuple, Dict, Optional
import copy
import sys

class Node:
    def __init__(self, state: List[int], parent=None, action: Optional[Tuple[int, int]] = None):
        self.state = state
        self.parent = parent
        self.action = action  # (which_stack, how_many_to_take)
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_actions = self.get_possible_actions()
    
    def get_possible_actions(self) -> List[Tuple[int, int]]:
        """Return list of possible actions as (stack_index, items_to_remove)"""
        actions = []
        for i, stack_size in enumerate(self.state):
            for items in range(1, stack_size + 1):
                actions.append((i, items))
        return actions
    
    def add_child(self, action: Tuple[int, int]) -> 'Node':
        """Add a child node with the given action"""
        # Create new state by applying action
        new_state = self.state.copy()
        stack_idx, items = action
        new_state[stack_idx] -= items
        
        # Create child node
        child = Node(new_state, parent=self, action=action)
        self.untried_actions.remove(action)
        self.children.append(child)
        return child
    
    def ucb_score(self, exploration_weight: float = 1.0) -> float:
        """Calculate UCB score for node selection"""
        if self.visits == 0:
            return float('inf')
        
        # Exploitation component
        exploitation = self.wins / self.visits
        
        # Exploration component
        exploration = exploration_weight * math.sqrt(math.log(self.parent.visits) / self.visits)
        
        return exploitation + exploration
    
    def is_terminal(self) -> bool:
        """Check if the state is terminal (all stacks are empty)"""
        return sum(self.state) == 0


def nim_misere_mcts(state: List[int], iterations: int = 1000) -> Tuple[int, int]:
    """
    Use Monte Carlo Tree Search to find the best move in Nim's Misère game
    
    Args:
        state: List of integers representing the number of items in each stack
        iterations: Number of MCTS iterations to run
        
    Returns:
        Tuple of (which_stack, how_many_to_take)
    """
    # Create root node
    root = Node(state)
    
    # Run MCTS iterations
    for _ in range(iterations):
        # Selection and Expansion
        node = select_node(root)
        
        # Simulation
        winner = simulate_random_game(node.state)
        
        # Backpropagation
        backpropagate(node, winner)
    
    # Choose best child based on win rate
    if not root.children:
        # If no children (should not happen in a valid game), pick a random move
        possible_actions = root.get_possible_actions()
        if possible_actions:
            return random.choice(possible_actions)
        return (0, 1)  # Fallback
    
    # Find child with highest win rate
    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.action


def select_node(node: Node) -> Node:
    """Select a node to expand using UCB"""
    current = node
    
    # Navigate down the tree until we reach a leaf node or a node with untried actions
    while current.untried_actions == [] and current.children and not current.is_terminal():
        # Select child with highest UCB score
        current = max(current.children, key=lambda c: c.ucb_score())
    
    # If we have untried actions, randomly select one and add a child
    if current.untried_actions and not current.is_terminal():
        action = random.choice(current.untried_actions)
        current = current.add_child(action)
    
    return current


def simulate_random_game(state: List[int]) -> int:
    """
    Simulate a random game from the given state and return the winner
    
    Returns:
        1 if first player wins, 0 if second player wins
    """
    # In Misère Nim, the player who takes the last item loses
    state = state.copy()
    current_player = 0  # 0 for first player, 1 for second player
    
    while sum(state) > 0:
        # Get all possible moves
        possible_moves = []
        for i, stack_size in enumerate(state):
            for items in range(1, stack_size + 1):
                possible_moves.append((i, items))
                
        # Make a random move
        stack_idx, items = random.choice(possible_moves)
        state[stack_idx] -= items
        
        # Switch player
        current_player = 1 - current_player
    
    # In Misère Nim, the player who takes the last item loses
    # So the winner is the current player
    # The one who just moved took last item, but then we switched current player
    winner = current_player
    return winner


def backpropagate(node: Node, winner: int):
    """Backpropagate the result up the tree"""
    current = node
    player = 1  # Start with player who just moved (opposite of the node's player)
    
    while current:
        current.visits += 1
        # If this node's player is the winner, increment wins
        if player == winner:
            current.wins += 1
            
        # Switch players as we move up the tree
        player = 1 - player
        current = current.parent


def optimal_nim_move(state: List[int]) -> Tuple[int, int]:
    """
    Calculate the optimal move for Misère Nim using nim-sum strategy
    This function works for the special case where there are no heaps of size 1
    
    Args:
        state: List of integers representing the number of items in each stack
        
    Returns:
        Tuple of (which_stack, how_many_to_take)
    """
    # Calculate nim-sum of all stacks
    nim_sum = 0
    for stack in state:
        nim_sum ^= stack
        
    # Count stacks of size 1
    ones_count = state.count(1)
    
    # Check if we're in an endgame situation (only stacks of size 1 remain)
    non_ones = [s for s in state if s > 1]
    if not non_ones:
        # In endgame with only 1s, we want odd number of 1s to win
        if ones_count % 2 == 1:
            # Take the last one if odd number of 1s
            idx = state.index(1)
            return (idx, 1)
        else:
            # Take the last one if even number of 1s
            idx = state.index(1)
            return (idx, 1)
    
    # Normal play
    for i, stack in enumerate(state):
        if stack > 1:  # Skip stacks of size 1 in regular play
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
                            return (i, take)
                    else:
                        return (i, take)
    
    # If no winning move, just take 1 from the largest stack
    max_stack_idx = state.index(max(state))
    return (max_stack_idx, 1)


def mcts_move(state: List[int]) -> Tuple[int, int]:
    """
    Get the best move for the current state of Nim Misère
    This function combines MCTS with the optimal strategy when possible
    
    Args:
        state: List of integers representing the number of items in each stack
        
    Returns:
        Tuple of (which_stack, how_many_to_take)
    """
    # Use MCTS with more iterations for complex positions
    if sum(state) > 20 or len(state) > 3:
        return nim_misere_mcts(state, iterations=2000)
    else:
        # Use MCTS with fewer iterations for simpler positions
        return nim_misere_mcts(state, iterations=1000)
