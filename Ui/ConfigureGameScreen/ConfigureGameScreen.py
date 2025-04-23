from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer

from Ui.RunGameScreen.RunGameScreen import RunGameScreen
from Ui.ConfigureGameScreen.StackConfigList import StackConfigList

class ConfigureGameScreen(Screen):
    BINDINGS = []
    TITLE = "Configure Game"
    CSS = """
    ConfigureGameScreen {
        layout: vertical;
        layers: default above;
    }
    
    #start_button {
        height: 3;
        width: 100%;
        margin: 2;
        dock: bottom;
        align-horizontal: center;
        content-align-horizontal: center;
        offset-y: -1;
        layer: above;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header()
        # TODO: Algorithm selection
        yield StackConfigList()
        yield Button("Start", id="start_button", variant="success")
        yield Footer()
        
    @on(Button.Pressed, "#start_button")
    def start_game(self, event: Button.Pressed) -> None:
        self.app.push_screen(RunGameScreen())
