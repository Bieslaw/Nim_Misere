from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from Ui.ConfigureGameScreen.ConfigureGameScreen import ConfigureGameScreen


class NimMisereApp(App):
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    async def on_mount(self) -> None:
        await self.push_screen(ConfigureGameScreen())


if __name__ == "__main__":
    app = NimMisereApp()
    app.run()
