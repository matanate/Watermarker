# Standard library imports

# Third-party library imports
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD

# Local imports
from utils import DARK, switch_view
from views import MainView


class MainApplication(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

        # Initialize the appearance mode to "dark"
        ctk.set_appearance_mode("dark")

        self.current_view = None

        # Initialize Window
        self.title("Watermarker")
        self.iconbitmap("resources\images\logo.ico")
        self.screen_w = int(self.winfo_screenwidth() * 0.8)
        self.screen_h = int(self.winfo_screenheight() * 0.8)
        self.geometry(f"{self.screen_w}x{self.screen_h}")
        self.configure(bg=DARK)

        self.after(50, lambda: self.switch_view(MainView))

    def switch_view(self, view_class, *args, **kwargs):
        """Switches to a new view and destroys the current one.

        Args:
            view_class (class): The class of the view to switch to.
            *args: Additional positional arguments for the new view.
            **kwargs: Additional keyword arguments for the new view.
        """
        selected_view = view_class(self, self.switch_view, *args, **kwargs)

        if self.current_view:
            self.current_view.destroy()

        selected_view.pack(fill="both", expand=True)
        self.current_view = selected_view
