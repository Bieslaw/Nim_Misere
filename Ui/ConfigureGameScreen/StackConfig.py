from textual.app import ComposeResult
from textual.widgets import Static


class StackConfig(Static):
    DEFAULT_CSS = """
    StackConfig {
        height: 5;
        width: 100%;
        margin: 1;
        padding: 1 3;
        layout: horizontal;
        align-vertical: middle;
        background: #141414;
        border: solid grey;
    }
    """

    def __init__(self, size: int):
        super().__init__()
        self.size = size
        
    def compose(self) -> ComposeResult:
        # TODO: Stack size input, with + and - buttons
        # TODO: Remove  stack button (dock right)
        pass
