from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Input, Select, Label
from textual.containers import Container

from Algorithms.AlgorithmBase import AlgorithmBase
from Algorithms.Random import Random
from Algorithms.Mcts import MctsAlgorithm
from Algorithms.AlphaBeta import AlphaBetaAlgorithm
from Algorithms.Optimal import Optimal

from Ui.RunGameScreen.RunGameScreen import RunGameScreen

class ConfigureGameScreen(Screen):
    BINDINGS = []
    TITLE = "Configure Game"
    CSS = """
    ConfigureGameScreen {
        layout: vertical;
        layers: default above;
    }
    
    #algorithm_label_container {
        layout: horizontal;
        width: 100%;
        height: 3;
    }
    
    #algorithm_select_container {
        layout: horizontal;
        width: 100%;
        height: 3;
    }
    
    .algorithm_label {
        height: 3;
        width: 50%;
        content-align: center middle;
    }
    
    .algorithm_select {
        height: 3;
        width: 50%;
    }
    
    #stack_sizes_label {
        height: 3;
        width: 100%;
        content-align: center middle;
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
    
    def __init__(self):
        super().__init__()
        self.select_1 = Select(options=[
            ("Random", Random),
            ("MCTS", MctsAlgorithm),
            ("AlphaBeta", AlphaBetaAlgorithm),
            ("Optimal", Optimal)], classes="algorithm_select")
        self.select_2 = Select(options=[
            ("Random", Random),
            ("MCTS", MctsAlgorithm),
            ("AlphaBeta", AlphaBetaAlgorithm),
            ("Optimal", Optimal)], classes="algorithm_select")
        self.stack_sizes_input = Input(placeholder="Stack size", id="stack_size_input")
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("Choose first algorithm", classes="algorithm_label"),
            Label("Choose second algorithm", classes="algorithm_label"),
            id="algorithm_label_container")
        
        yield Container(
            self.select_1, 
            self.select_2, 
            id="algorithm_select_container")
        
        yield Label("Choose stack sizes (as comma separated values)", id="stack_sizes_label")
        yield self.stack_sizes_input
        yield Button("Start", id="start_button", variant="success")
        yield Footer()
        
    @on(Button.Pressed, "#start_button")
    def start_game(self, event: Button.Pressed) -> None:
        self.app.push_screen(RunGameScreen())
