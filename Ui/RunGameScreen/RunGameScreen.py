from textual import on, work
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
    
    #whose_turn_label {
        height: 3;
        width: 100%;
        content-align: center middle;
        margin: 1;
        border: solid gray;
        dock: bottom;
        offset-y: -8;
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
        self.limit_input = Input(placeholder="Depth", id="limit_input", validators=Number(minimum=0.01))
        self.change_limit_type_button = Button("Depth", id="limit_type_button", variant="primary")
        self.running_worker = None
    
    def _get_whose_turn_label_text(self) -> str:
        algorithm_name = self.game.first_player.get_name() if self.game.first_player_turn else self.game.second_player.get_name()
        return f"Next move: {'Player 1' if self.game.first_player_turn else 'Player 2'} ({algorithm_name})"
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(*self.stack_labels, id="stacks_container")
        yield Label(self._get_whose_turn_label_text(), id="whose_turn_label")
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
        if not self.limit_input.validate(self.limit_input.value).is_valid:
            if self.change_limit_type_button.label == "Depth":
                self.app.notify("Depth must be a positive integer", severity="error")
                return
            else:
                self.app.notify("Time limit must be a positive real number", severity="error")
                return
        
        self.query_one("#next_move_button").disabled = True
        self.running_worker = self._run_game_step_and_update_ui()
        
    @on(Button.Pressed, "#exit_button")
    def exit(self, event: Button.Pressed) -> None:
        if self.running_worker is not None:
            self.running_worker.cancel()
            self.running_worker = None

        self.dismiss()
        
    @on(Button.Pressed, "#next_move_button")
    def next_move(self, event: Button.Pressed) -> None:
        self._advance_game()
        
    @on(Button.Pressed, "#limit_type_button")
    def toggle_limit_type(self, event: Button.Pressed) -> None:
        self.limit_input.placeholder = "Depth" if self.change_limit_type_button.label == "Depth" else "Time Limit"
        self.change_limit_type_button.label = "Depth" if self.change_limit_type_button.label == "Time Limit" else "Time Limit"
        self.limit_input.value = "" 

    @work(thread=True, exclusive=True)
    def _run_game_step_and_update_ui(self) -> None:
        if self.change_limit_type_button.label == "Depth":
            self.game.step(int(float(self.limit_input.value)))
        else:
            self.game.step_timed(float(self.limit_input.value))
        
        for i, label in enumerate(self.stack_labels):
            label.update(f"Stack {i+1}: {self.game.stacks[i]}")
            if self.game.stacks[i] != self.previous_stacks[i]:
                label.add_class("last_updated")
            else:
                label.remove_class("last_updated")
                
        self.previous_stacks = self.game.stacks.copy()
            
        # TODO: Modal for game over
        
        def do_ui_stuff():
            self.query_one("#next_move_button").disabled = self.game.get_result() is not None
            self.query_one("#whose_turn_label").update(self._get_whose_turn_label_text())
        
        self.app.call_from_thread(do_ui_stuff)
        self.running_worker = None
