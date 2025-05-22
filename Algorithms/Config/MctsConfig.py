from Algorithms.Config.ConfigBase import ConfigBase
from dataclasses import dataclass

class SelectionType:
    """
    Enum for selection types in MCTS.
    """
    UCB1 = "UCB1"
    UCB_TUNED = "UCB_TUNED"
    RAVE = "RAVE"

@dataclass
class MctsConfig(ConfigBase):
    """
    Configuration class for MCTS algorithm.
    """
    hash_states: bool = False
    exploration_constant: float = 1.0
    beta: float = 300.0
    selection_type: SelectionType = SelectionType.UCB1

