import math
import random
from Algorithms.AlgorithmBase import AlgorithmBase, Move


class Node:
    def __init__(self, state: list[int], parent=None, action: tuple[int, int] | None = None):
        self.state: list[int] = state
        self.parent = parent
        self.action: tuple[int, int] | None = action
        self.children: list['Node'] = []
        self.visits: int = 0
        self.wins: int = 0
        self.untried_actions: list[tuple[int, int]] = self.get_possible_actions()
    
    def get_possible_actions(self) -> list[tuple[int, int]]:
        """Return list of possible actions as (stack_index, items_to_remove)"""
        actions = []
        for i, stack_size in enumerate(self.state):
            for items in range(1, stack_size + 1):
                actions.append((i, items))
        return actions
    
    def add_child(self, action: tuple[int, int]) -> 'Node':
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
        return sum(self.state) == 0


class MctsAlgorithm(AlgorithmBase):        
    def get_move(self, stacks: list[int], depth: int) -> Move:
        """Implement the abstract method from AlgorithmBase"""
        non_zero_indices = [i for i, stack in enumerate(stacks) if stack > 0]
        non_zero_stacks = [stacks[i] for i in non_zero_indices]
        
        stack_idx, items = self.nim_misere_mcts(non_zero_stacks, depth)
        return Move(stack_index=non_zero_indices[stack_idx], items_to_remove=items)
    
    def _uses_depth(self) -> bool:
        return True
    
    @classmethod
    def get_name(cls) -> str:
        return "MCTS"
    
    def nim_misere_mcts(self, state: list[int], iterations: int) -> tuple[int, int]:
        root = Node(state)
        
        for _ in range(iterations):
            node = self.select_node(root)
            winner = self.simulate_random_game(node.state)
            self.backpropagate(node, winner)

        if not root.children:
            # If no children (should not happen in a valid game), pick a random move
            possible_actions = root.get_possible_actions()
            if possible_actions:
                return random.choice(possible_actions)
            return (0, 1)  # Fallback
        
        # Find child with highest win rate
        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.action

    def select_node(self, node: Node) -> Node:
        """Select a node to expand using UCB"""
        current = node
        
        # Navigate down the tree until we reach a leaf node or a node with untried actions
        while len(current.untried_actions) == 0 and len(current.children) > 0 and not current.is_terminal():
            # Select child with highest UCB score
            current = max(current.children, key=lambda c: c.ucb_score())
        
        # If we have untried actions, randomly select one and add a child
        if len(current.untried_actions) > 0 and not current.is_terminal():
            action = random.choice(current.untried_actions)
            current = current.add_child(action)
        
        return current

    def simulate_random_game(self, state: list[int]) -> int:
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

    def backpropagate(self, node: Node, winner: int):
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
