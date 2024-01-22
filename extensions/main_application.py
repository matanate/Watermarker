# Standard library imports

# Third-party library imports
from customtkinter import CTk, set_appearance_mode
from tkinterdnd2 import TkinterDnD

# Local imports
from utils import DARK
from views import MainView


class MainApplication(CTk, TkinterDnD.DnDWrapper):
    """
    MainApplication class represents the main application window.

    This class extends Tk and serves as the main application window. It contains methods for initializing
    the main view, handling the switching of views, and running the main application loop.

    Parameters:
        *args, **kwargs: Additional arguments passed to the Tk constructor.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the MainApplication.

        Parameters:
        *args, **kwargs: Additional arguments passed to the Tk constructor.
        """
        super().__init__(*args, **kwargs)
        self.tk_dnd_version = TkinterDnD._require(self)

        # Initialize the appearance mode to "dark"
        set_appearance_mode("dark")

        self.current_view = None

        # Initialize Window
        self.title("Watermarker")
        self.iconbitmap("resources\images\logo.ico")
        # Calculate the window dimensions to 80% of the screen
        self.window_w = int(self.winfo_screenwidth() * 0.8)
        self.window_h = int(self.winfo_screenheight() * 0.8)
        # Calculate the position of the screen so it will be centered
        self.x = (self.winfo_screenwidth() // 2) - (self.window_w // 2)
        self.y = (self.winfo_screenheight() // 2) - (self.window_h // 2)
        # Set the window geometry
        self.geometry(f"{self.window_w}x{self.window_h}+{self.x}+{self.y}")
        self.configure(bg=DARK)

        self.switch_to_main_view()

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

    def switch_to_main_view(self):
        self.after(50, lambda: self.switch_view(MainView))
