from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label
from textual.containers import ScrollableContainer, Container

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
    
    #button_container {
        layout: horizontal;
        width: 100%;
        height: 3;
        dock: bottom;
        offset-y: -1;
    }
    
    #end_game_button {
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
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(*self.stack_labels, id="stacks_container")
        # TODO: Choose depth/time limit
        yield Container(
            Button("End Game", id="end_game_button", variant="error"),
            Button("Next Move", id="next_move_button", variant="primary"),
            id="button_container"
        )
        yield Footer()
        
    def _advance_game(self) -> None:
        self.game.step(100)
        
        # TODO: Modal for game over
        
        for i, label in enumerate(self.stack_labels):
            label.update(f"Stack {i+1}: {self.game.stacks[i]}")
            if self.game.stacks[i] != self.previous_stacks[i]:
                label.add_class("last_updated")
            else:
                label.remove_class("last_updated")
            
        self.previous_stacks = self.game.stacks.copy()
        
    @on(Button.Pressed, "#end_game_button")
    def end_game(self, event: Button.Pressed) -> None:
        self.dismiss()
        
    @on(Button.Pressed, "#next_move_button")
    def next_move(self, event: Button.Pressed) -> None:
        self._advance_game()
        