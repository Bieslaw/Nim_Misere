from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, Input
from textual.containers import ScrollableContainer, Container
from textual.validation import Number

from NimMisere import NimMisere


class RunGameScreen(Screen):
    BINDINGS = []
    TITLE = "Run Game"
    CSS = """
    RunGameScreen {
        layout: vertical;
    }
    
    #stacks_container {
        width: 100%;
    }
    
    .stack_label {
        height: 3;
        width: 1fr;
        content-align: center middle;
        margin: 1;
        border: solid gray;
    }
    
    .last_updated {
        background: green;
    }
    
    #params_container {
        layout: horizontal;
        width: 100%;
        height: 3;
        dock: bottom;
        offset-y: -5;
    }
    
    #limit_input {
        width: 3fr;
    }
    
    #limit_type_button {
        width: 1fr;
    }
    
    #button_container {
        layout: horizontal;
        width: 100%;
        height: 3;
        dock: bottom;
        offset-y: -1;
    }
    
    #exit_button {
        height: 3;
        width: 1fr;
    }
    
    #next_move_button {
        height: 3;
        width: 1fr;
    }
    """
    
    def __init__(self, game: NimMisere):
        super().__init__()
        self.game = game
        self.previous_stacks = game.stacks.copy()
        self.stack_labels = [Label(f"Stack {i+1}: {size}", classes="stack_label") 
                             for i, size in enumerate(self.game.stacks)]
        self.limit_input = Input(placeholder="Time Limit", id="limit_input", validators=Number(minimum=0.01))
        self.change_limit_type_button = Button("Depth", id="limit_type_button", variant="primary")
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(*self.stack_labels, id="stacks_container")
        # TODO: Choose depth/time limit
        yield Container(
            self.change_limit_type_button,
            self.limit_input,
            id="params_container"
        )
        yield Container(
            Button("Exit", id="exit_button", variant="error"),
            Button("Next Move", id="next_move_button", variant="primary"),
            id="button_container"
        )
        yield Footer()
        
    def _advance_game(self) -> None:
        if not self.limit_input.is_valid:
            if self.limit_input.placeholder == "Depth":
                self.app.notify("Depth must be a positive integer", severity="error")
            else:
                self.app.notify("Time limit must be a positive real number", severity="error")
            return
        
        if self.limit_input.placeholder == "Depth":
            self.game.step(int(float(self.limit_input.value)))
        else:
            self.game.step_timed(float(self.limit_input.value))
                
        # TODO: Modal for game over
        
        for i, label in enumerate(self.stack_labels):
            label.update(f"Stack {i+1}: {self.game.stacks[i]}")
            if self.game.stacks[i] != self.previous_stacks[i]:
                label.add_class("last_updated")
            else:
                label.remove_class("last_updated")
            
        self.previous_stacks = self.game.stacks.copy()
        
    @on(Button.Pressed, "#exit_button")
    def exit(self, event: Button.Pressed) -> None:
        self.dismiss()
        
    @on(Button.Pressed, "#next_move_button")
    def next_move(self, event: Button.Pressed) -> None:
        self._advance_game()
        
    @on(Button.Pressed, "#limit_type_button")
    def toggle_limit_type(self, event: Button.Pressed) -> None:
        self.limit_input.placeholder = "Depth" if self.limit_input.placeholder == "Time Limit" else "Time Limit"
        self.change_limit_type_button.label = "Depth" if self.limit_input.placeholder == "Depth" else "Time Limit"
        self.limit_input.value = ""            
            