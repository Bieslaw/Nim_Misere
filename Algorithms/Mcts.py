import math
import random
from Algorithms.AlgorithmBase import AlgorithmBase, Move
from Algorithms.Config.MctsConfig import MctsConfig, SelectionType

class Node:
    def __init__(self, state: list[int], hash_states: bool, parent=None, action: tuple[int, int] | None = None):
        self.state: list[int] = state
        self.discriminator: tuple | list[int] = Node.make_discriminator(state, hash_states)
        self.hash_states = hash_states
        self.parent = parent
        self.action: tuple[int, int] | None = action  # (stack_size_before, items_to_remove)
        self.children: list['Node'] = []
        self.visits: int = 0
        self.wins: int = 0
        self.untried_actions: list[tuple[int, int]] = self.get_possible_actions()
    
    @classmethod
    def make_discriminator(cls, state: list[int], hash_states: bool) -> tuple | list[int]:
        """Create a discriminator for the node"""
        if hash_states:
            # Create canonical representation by sorting non-zero stacks
            # This ensures [3, 1, 2] and [1, 2, 3] have the same discriminator
            non_zero_stacks = [stack for stack in state if stack > 0]
            return tuple(sorted(non_zero_stacks))
        else:
            # Keep original state for exact matching
            return state.copy()

    def get_possible_actions(self) -> list[tuple[int, int]]:
        """Return list of possible actions as (stack_size, items_to_remove)"""
        actions = []
        # Get unique stack sizes (to avoid duplicate actions)
        unique_stack_sizes = list(set(size for size in self.state if size > 0))
        
        for stack_size in unique_stack_sizes:
            for items in range(1, stack_size + 1):
                actions.append((stack_size, items))
        return actions
    
    def add_child(self, action: tuple[int, int]) -> 'Node':
        """Add a child node with the given action"""
        stack_size_before, items = action
        
        # Find first occurrence of this stack size and apply the action
        new_state = self.state.copy()
        for i, size in enumerate(new_state):
            if size == stack_size_before:
                new_state[i] -= items
                break
        
        # Create child node
        child = Node(new_state, self.hash_states, parent=self, action=action)
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
    
    def rave_score(self, beta_const: float = 300.0) -> float:
        """RAVE-enhanced UCB score"""
        if self.visits == 0:
            return float('inf')

        q = self.wins / self.visits  # standard value
        rave_q = self.rave_wins / self.rave_visits if self.rave_visits > 0 else 0

        beta = self.rave_visits / (self.visits + self.rave_visits + 1e-6)
        score = (1 - beta) * q + beta * rave_q

        exploration = math.sqrt(math.log(self.parent.visits) / self.visits)
        return score + exploration
    
    def uct_tuned_score(self, exploration_weight: float = 1.0) -> float:
        """UCT-Tuned with variance-aware exploration"""
        if self.visits == 0:
            return float('inf')
        
        exploitation = self.wins / self.visits
        
        # Calculate empirical variance
        mean_sq = self.squared_wins / self.visits
        mean = self.wins / self.visits
        variance = mean_sq - mean**2 + 1e-4  # prevent negative values

        exploration = exploration_weight * math.sqrt((math.log(self.parent.visits) / self.visits) * min(0.25, variance))
        
        return exploitation + exploration
    
    def is_terminal(self) -> bool:
        return sum(self.state) == 0


class MctsAlgorithm(AlgorithmBase):        
    def __init__(self):
        self.root: Node | None = None  # persistent root node
        self.config: MctsConfig | None = None  # configuration for the algorithm

    def configure(self, config: MctsConfig):
        self.config = config

    def get_move(self, stacks: list[int], depth: int) -> Move:
        # Filter out zero stacks for MCTS processing
        non_zero_stacks = [stack for stack in stacks if stack > 0]
        
        # Get action in terms of stack sizes
        stack_size_before, items = self.nim_misere_mcts(non_zero_stacks, depth)
        
        # Convert back to original stack index
        for i, stack in enumerate(stacks):
            if stack == stack_size_before:
                return Move(stack_index=i, items_to_remove=items)
        
        # Fallback (shouldn't happen)
        return Move(stack_index=0, items_to_remove=1)

    def _uses_depth(self) -> bool:
        return True

    @classmethod
    def get_name(cls) -> str:
        return "MCTS"

    def nim_misere_mcts(self, state: list[int], iterations: int) -> tuple[int, int]:
        discriminator = Node.make_discriminator(state, self.config.hash_states)
        if self.root is None or self.root.discriminator != discriminator:
            # Try to find the new root among existing children
            if self.root:
                matching_node = self.find_matching_node(self.root, discriminator)
                if matching_node:
                    matching_node.parent = None
                    self.root = matching_node
                else:
                    self.root = Node(state, self.config.hash_states)
            else:
                self.root = Node(state, self.config.hash_states)

        for _ in range(iterations):
            node = self.select_node(self.root)
            winner = self.simulate_random_game(node.state)
            self.backpropagate(node, winner)

        if not self.root.children:
            possible_actions = self.root.get_possible_actions()
            if possible_actions:
                return random.choice(possible_actions)
            else:
                # Fallback - find any non-zero stack
                for stack_size in state:
                    if stack_size > 0:
                        return (stack_size, 1)
                return (1, 1)

        # Pick best move
        best_child = max(self.root.children, key=lambda c: c.visits)
        
        # Update root for next move
        best_child.parent = None
        self.root = best_child
        
        return best_child.action

    def select_node(self, node: Node) -> Node:
        """Select a node to expand using UCB"""
        current = node
        
        selector = {
            SelectionType.UCB1: lambda c: c.ucb_score(self.config.exploration_constant),
            SelectionType.UCB_TUNED: lambda c: c.uct_tuned_score(self.config.exploration_constant),
            SelectionType.RAVE: lambda c: c.rave_score(self.config.beta),
        }

        # Navigate down the tree until we reach a leaf node or a node with untried actions
        while len(current.untried_actions) == 0 and len(current.children) > 0 and not current.is_terminal():
            # Select child with highest UCB score
            current = max(current.children, key=selector[self.config.selection_type])
        
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
            # Get all possible moves (stack_size, items_to_remove)
            possible_moves = []
            unique_stack_sizes = list(set(size for size in state if size > 0))
            
            for stack_size in unique_stack_sizes:
                for items in range(1, stack_size + 1):
                    possible_moves.append((stack_size, items))
                    
            # Make a random move
            stack_size_before, items = random.choice(possible_moves)
            
            # Apply the move to the first stack of that size
            for i, size in enumerate(state):
                if size == stack_size_before:
                    state[i] -= items
                    break
            
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

    def find_matching_node(self, node: Node, discriminator: tuple | list[int]) -> Node | None:
        """Search subtree rooted at `node` for a node matching the discriminator."""
        if node.discriminator == discriminator:
            return node
        for child in node.children:
            if child.discriminator == discriminator:
                return child

        for child in node.children:
            result = self.find_matching_node(child, discriminator)
            if result:
                return result
        return None
