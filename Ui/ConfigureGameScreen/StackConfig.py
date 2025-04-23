from textual.app import ComposeResult
from textual.widgets import Static, Button, Label, Input
from textual import on
from textual.validation import Number


class StackConfig(Static):
    DEFAULT_CSS = """
    StackConfig {
        height: 7;
        width: 100%;
        margin: 1;
        padding: 1 3;
        layout: horizontal;
        align-vertical: middle;
        background: #141414;
        border: solid grey;
    }
    
    #size_label {
        width: auto;
        content-align-vertical: middle;
        margin-right: 2;
    }
    
    .change_button {
        width: 3;
        height: 3;
        margin: 0 1;
        content-align: center middle;
    }
    
    #size_display {
        width: 1fr;
        content-align: center middle;
        margin: 0 2;
    }
    
    #remove_stack_button {
        dock: right;
        width: 15;
        height: 3;
        margin-left: 2;
    }
    """

    def __init__(self, stack_size: int) -> None:
        super().__init__()
        self.stack_size_input = Input(value=str(stack_size), id="size_display", validators=[Number(minimum=1)])
        
    def compose(self) -> ComposeResult:
        yield Label("Stack size:", id="size_label")
        yield Button("-", classes="change_button", id="decrease_button")
        yield self.stack_size_input
        yield Button("+", classes="change_button", id="increase_button")
        yield Button("Remove Stack", id="remove_stack_button")

    @on(Button.Pressed, "#decrease_button")
    def decrease_size(self) -> None:
        if int(self.stack_size_input.value) > 1:
            self.stack_size_input.value = str(int(self.stack_size_input.value) - 1)

    @on(Button.Pressed, "#increase_button")
    def increase_size(self) -> None:
        self.stack_size_input.value = str(int(self.stack_size_input.value) + 1)

    @on(Button.Pressed, "#remove_stack_button")
    def remove_stack(self) -> None:
        self.remove()
