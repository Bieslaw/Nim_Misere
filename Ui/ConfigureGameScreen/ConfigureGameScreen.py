from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Input, Select, Label, Checkbox
from textual.containers import Container, Horizontal, Vertical

from Algorithms.AlgorithmBase import AlgorithmBase
from Algorithms.Random import Random
from Algorithms.Mcts import MctsAlgorithm
from Algorithms.AlphaBeta import AlphaBetaAlgorithm
from Algorithms.Optimal import Optimal
from Algorithms.Config.ConfigBase import ConfigBase
from Algorithms.Config.MctsConfig import MctsConfig, SelectionType

from NimMisere import NimMisere
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
    
    .algorithm_select_row {
        height: 3;
        width: 50%;
        layout: horizontal;
    }
    
    .algorithm_select {
        height: 3;
        width: 1fr;
    }
    
    .config_gear {
        width: 3;
        height: 3;
        min-width: 3;
        content-align: center middle;
        display: none;
    }
    
    .config_gear.visible {
        display: block;
    }
    
    .mcts_config_container {
        layout: vertical;
        width: 50%;
        height: auto;
        margin: 1 0;
        padding: 1;
        border: solid $primary;
        display: none;
    }
    
    .mcts_config_container.visible {
        display: block;
    }
    
    .config_label {
        height: 1;
        content-align: center middle;
        text-style: bold;
    }
    
    .config_input {
        height: 3;
        margin: 1 0;
    }
    
    #config_containers {
        layout: horizontal;
        width: 100%;
        height: auto;
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
            (Random.get_name(), Random),
            (MctsAlgorithm.get_name(), MctsAlgorithm),
            (AlphaBetaAlgorithm.get_name(), AlphaBetaAlgorithm),
            (Optimal.get_name(), Optimal)], 
            classes="algorithm_select", 
            value=Optimal)
        self.select_2 = Select(options=[
            (Random.get_name(), Random),
            (MctsAlgorithm.get_name(), MctsAlgorithm),
            (AlphaBetaAlgorithm.get_name(), AlphaBetaAlgorithm),
            (Optimal.get_name(), Optimal)], 
            classes="algorithm_select", 
            value=Random)
        
        self.gear_1 = Button("⚙", classes="config_gear", id="gear_1")
        self.gear_2 = Button("⚙", classes="config_gear", id="gear_2")
        
        self.config_1 = self.get_config_widget("config_1")
        self.config_2 = self.get_config_widget("config_2")
        
        self.config_1_visible = False
        self.config_2_visible = False

        self.stack_sizes_input = Input(value="1,2,3,4", placeholder="Stack size", id="stack_size_input")
    
    @staticmethod
    def get_config_widget(config_id):
        # For now, only MCTS has configuration options
        return Container(
            Label("MCTS Configuration", classes="config_label"),
            Checkbox("Use hash states", id=f"{config_id}_hash_states_input", classes="config_input"),
            Label("Exploration constant", classes="config_label", id=f"{config_id}_param_label"),
            Input(value="1.0", placeholder="Exploration constant", id=f"{config_id}_param_input", classes="config_input"),
            Label("Selection type", classes="config_label"),
            Select(options=[
                (SelectionType.UCB1, SelectionType.UCB1),
                (SelectionType.UCB_TUNED, SelectionType.UCB_TUNED),
                (SelectionType.RAVE, SelectionType.RAVE)
                ],
                id=f"{config_id}_selection_type_input",
                classes="config_input",
                value=SelectionType.UCB1),
            classes="mcts_config_container",
            id=config_id,
        )

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("Choose first algorithm", classes="algorithm_label"),
            Label("Choose second algorithm", classes="algorithm_label"),
            id="algorithm_label_container")
        
        yield Container(
            Horizontal(
                self.select_1,
                self.gear_1,
                classes="algorithm_select_row"
            ),
            Horizontal(
                self.select_2, 
                self.gear_2,
                classes="algorithm_select_row"
            ),
            id="algorithm_select_container")
        
        yield Container(
            self.config_1,
            self.config_2,
            id="config_containers"
        )
        
        yield Label("Choose stack sizes (as comma separated values)", id="stack_sizes_label")
        yield self.stack_sizes_input
        yield Button("Start", id="start_button", variant="success")
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when the screen is mounted"""
        self.update_config_visibility(self.select_1, self.gear_1, self.config_1)
        self.update_config_visibility(self.select_2, self.gear_2, self.config_2)
        # Initialize parameter labels for both configs
        self.update_parameter_display("config_1")
        self.update_parameter_display("config_2")
    
    @on(Select.Changed)
    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle select changes"""
        if event.select == self.select_1:
            self.config_1_visible = False
            self.config_1.remove_class("visible")
            self.update_config_visibility(self.select_1, self.gear_1, self.config_1)
        elif event.select == self.select_2:
            self.config_2_visible = False
            self.config_2.remove_class("visible")
            self.update_config_visibility(self.select_2, self.gear_2, self.config_2)
        # Handle selection type changes within config containers
        elif event.select.id and event.select.id.endswith("_selection_type_input"):
            config_id = event.select.id.replace("_selection_type_input", "")
            self.update_parameter_display(config_id)
    
    def update_parameter_display(self, config_id):
        """Update parameter label and input based on selection type"""
        try:
            selection_type_select = self.query_one(f"#{config_id}_selection_type_input")
            param_label = self.query_one(f"#{config_id}_param_label")
            param_input = self.query_one(f"#{config_id}_param_input")
            
            if selection_type_select.value == SelectionType.RAVE:
                param_label.update("Beta value")
                param_input.placeholder = "Beta value"
                # Update input value to a suitable default for beta if it's still the exploration constant default
                if param_input.value == "1.0":
                    param_input.value = "0.5"
            else:
                param_label.update("Exploration constant")
                param_input.placeholder = "Exploration constant"
                # Update input value to exploration constant default if it's still the beta default
                if param_input.value == "0.5":
                    param_input.value = "1.0"
        except Exception:
            # Silently handle case where widgets don't exist yet
            pass
    
    @on(Button.Pressed, "#gear_1")
    def toggle_config_1(self, event: Button.Pressed) -> None:
        """Toggle configuration visibility for first algorithm"""
        self.config_1_visible = not self.config_1_visible
        if self.config_1_visible:
            self.config_1.add_class("visible")
        else:
            self.config_1.remove_class("visible")
    
    @on(Button.Pressed, "#gear_2")
    def toggle_config_2(self, event: Button.Pressed) -> None:
        """Toggle configuration visibility for second algorithm"""
        self.config_2_visible = not self.config_2_visible
        if self.config_2_visible:
            self.config_2.add_class("visible")
        else:
            self.config_2.remove_class("visible")

    def update_config_visibility(self, select_widget, gear_button, config_container):
        """Show/hide gear button based on selected algorithm"""
        if select_widget.value == MctsAlgorithm:
            gear_button.add_class("visible")
        else:
            gear_button.remove_class("visible")
            config_container.remove_class("visible")
        
    @on(Button.Pressed, "#start_button")
    def start_game(self, event: Button.Pressed) -> None:
        if not self.stack_sizes_input.value.strip():
            self.app.notify("Stack sizes cannot be empty", severity="error")
            return
            
        try:
            stack_sizes = [int(size.strip()) for size in self.stack_sizes_input.value.split(",") if size.strip()]
            
            if not stack_sizes:
                self.app.notify("No valid stack sizes provided", severity="error")
                return
                
            if any(size <= 0 for size in stack_sizes):
                self.app.notify("All stack sizes must be positive integers", severity="error")
                return
                
        except ValueError:
            self.app.notify("Invalid stack sizes. Please enter comma-separated integers", severity="error")
            return
        
        if self.select_1.value == Select.BLANK:
            self.app.notify("First algorithm is not chosen", severity="error")
            return
        
        if self.select_2.value == Select.BLANK:
            self.app.notify("Second algorithm is not chosen", severity="error")
            return
        
        player_1 = self.select_1.value()
        player_2 = self.select_2.value()

        config_1 = self.build_config(player_1, self.config_1, "config_1")
        config_2 = self.build_config(player_2, self.config_2, "config_2")
        player_1.configure(config_1)
        player_2.configure(config_2)

        game = NimMisere(stack_sizes, player_1, player_2)
        self.app.push_screen(RunGameScreen(game))

    def build_config(self, player, config_container, config_id) -> ConfigBase:
        if type(player) == MctsAlgorithm:
            try:
                hash_states = config_container.query_one(f"#{config_id}_hash_states_input").value
                param_value = float(config_container.query_one(f"#{config_id}_param_input").value)
                selection_type = config_container.query_one(f"#{config_id}_selection_type_input").value
                if selection_type not in SelectionType:
                    raise ValueError("Invalid selection type")
                
                # Pass the parameter value as either exploration_constant or beta depending on selection type
                if selection_type == SelectionType.RAVE:
                    return MctsConfig(hash_states, selection_type=selection_type, beta=param_value)
                else:
                    return MctsConfig(hash_states, exploration_constant=param_value, selection_type=selection_type)
            except (ValueError, TypeError):
                # Use default values if parsing fails
                return MctsConfig()
        
        return ConfigBase()
