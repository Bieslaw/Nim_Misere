from textual.app import ComposeResult
from textual.widgets import Static, Button
from textual import on
from textual.containers import Vertical, Container, ScrollableContainer

from Ui.ConfigureGameScreen.StackConfig import StackConfig


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
    
    #stacks_container {
        width: 100%;
        height: auto;
        layout: vertical;
        align: center middle;
    }
    
    #add_stack_button {
        width: 100%;
        height: 3;
        margin-bottom: 2;
    }
    """

    def __init__(self):
        super().__init__()
        self.stacks: list[StackConfig] = [StackConfig(1)]
    
    def compose(self) -> ComposeResult:
        yield self._make_stacks_container()
            
    def _make_stacks_container(self) -> ScrollableContainer:
        return ScrollableContainer(
            *[stack_config for stack_config in self.stacks],
            Button("Add Stack", id="add_stack_button"),
            Static(id="bottom_spacer"),
            id="stacks_container"
        )
    
    @on(Button.Pressed, "#add_stack_button")
    async def add_stack(self) -> None:
        stack_config = StackConfig(1)
        self.stacks.append(stack_config)
        await self.query_one("#stacks_container").remove()
        self.mount(self._make_stacks_container())
