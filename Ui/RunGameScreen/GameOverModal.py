from textual import on
from textual.widgets import Label, Button
from textual.app import ComposeResult
from textual.screen import ModalScreen

from NimMisere import NimMisere


class GameOverModal(ModalScreen):
    CSS = """
    GameOverModal {
        layout: vertical;
        align: center middle;
        width: 50%;
    }
    
    #game_over_label {
        width: 50%;
        height: 3;
        align: center middle;
        content-align: center middle;
        border: solid gray;
    }
    
    #play_again_button {
        width: 50%;
    }
    """
    
    def __init__(self, game: NimMisere):
        super().__init__()
        self.game = game
        
        if game.get_result() is None:
            raise ValueError("Game is not over")

    def compose(self) -> ComposeResult:
        algorithm_name = self.game.first_player.get_name() if self.game.first_player_turn else self.game.second_player.get_name()
        label_text = f"{'Player 1' if self.game.get_result() == 1 else 'Player 2'} ({algorithm_name}) wins!"
        yield Label(label_text, id="game_over_label")
        yield Button("Play again", id="play_again_button", variant="success")

    @on(Button.Pressed, "#play_again_button")
    def play_again(self) -> None:
        self.dismiss()

