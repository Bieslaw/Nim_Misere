from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ConfigBase(ABC):
    """
    Base class for configuration objects.
    This class is intended to be inherited by specific configuration classes.
    """
    pass
