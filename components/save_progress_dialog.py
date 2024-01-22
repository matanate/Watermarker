# Standard library imports

# Third-party library imports
from customtkinter import CTkToplevel, CTkLabel, CTkProgressBar


# Local imports


class SaveProgressDialog(CTkToplevel):
    """
    SaveProgressDialog class represents a dialog window for displaying saving progress.

    This class extends CTkToplevel and provides a simple dialog with a progress bar
    to indicate the progress of a saving operation.

    Parameters:
        parent (Tk): The parent Tkinter window.
        *args, **kwargs: Additional arguments passed to the CTkToplevel constructor.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initialize the SaveProgressDialog.

        Args:
            parent (Tk): The parent Tkinter widget.
            *args, **kwargs: Additional arguments passed to the CTkToplevel constructor.
        """
        CTkToplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.attributes("-topmost", "true")
        self.title("Saving...")

        # Set the size and position of the window
        self.window_w = 300
        self.window_h = 100
        self.x = (self.parent.winfo_screenwidth() // 2) - (self.window_w // 2)
        self.y = (self.parent.winfo_screenheight() // 2) - (self.window_h // 2)
        self.geometry(f"{self.window_w}x{self.window_h}+{self.x}+{self.y}")

        # Create and pack widgets
        self.progress_label = CTkLabel(self, text="Saving in progress...")
        self.progress_label.pack(pady=10)

        self.progress_bar = CTkProgressBar(self)
        self.progress_bar.pack(pady=10)

    def start(self):
        """
        Start the progress bar to indicate the beginning of the saving process.
        """
        self.progress_bar.start()

    def stop(self):
        """
        Stop the progress bar, set it to 100% and update the progress label to indicate completion.
        """
        self.progress_bar.stop()
        self.progress_bar.set(100)
        self.progress_label.configure(text="Save Complete!")
