from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer


class RunGameScreen(Screen):
    BINDINGS = []
    TITLE = "Run Game"
    CSS = """
    RunGameScreen {
        layout: vertical;
    }
    
    #end_game_button {
        height: 3;
        width: 50%;
        margin: 2;
        dock: bottom;
        align-horizontal: center;
        content-align-horizontal: center;
        offset-y: -1;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header()
        # TODO
        yield Button("End Game", id="end_game_button", variant="error")
        yield Footer()
        
    @on(Button.Pressed, "#end_game_button")
    def end_game(self, event: Button.Pressed) -> None:
        self.dismiss()