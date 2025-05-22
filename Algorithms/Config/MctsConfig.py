from Algorithms.Config.ConfigBase import ConfigBase
from dataclasses import dataclass

@dataclass
class MctsConfig(ConfigBase):
    """
    Configuration class for MCTS algorithm.
    """
    hash_states: bool = False
