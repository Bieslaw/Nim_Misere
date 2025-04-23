
from textual.app import ComposeResult
from textual.widgets import Static


class StackConfigList(Static):
    DEFAULT_CSS = """
    StackConfigList {
        height: 100%;
        width: 100%;
        layout: vertical;
        align: center middle;
    }
    
    #bottom_spacer {
        height: 6;
        width: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        # TODO: StackConfig for each stack
        # TODO: Add stack button (at the bottom, dock right, same width as Remove Stack button in StackConfig)
        yield Static(id="bottom_spacer")
