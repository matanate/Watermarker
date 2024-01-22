# Standard library imports
from tkinter import filedialog

# Third-party library imports
from customtkinter import CTkFrame, CTkButton
from PIL import Image


# Local imports
from utils import *


class NavBar(CTkFrame):
    """
    NavBar represents the navigation bar in the application.

    This class provides buttons for various actions such as closing the app,
    going back, adding text, adding a logo, removing the watermark, and creating the final image.

    Parameters:
        parent: The parent widget.
        *args, **kwargs: Additional arguments passed to the CTkFrame constructor.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initialize the NavBar.

        Args:
            parent (Tk): The parent Tkinter widget.
            *args, **kwargs: Additional arguments passed to the CTkFrame constructor.
        """
        CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Initiate Close App Button
        self.initiate_close_btn()

        # Initiate Back Button
        self.initiate_back_btn()

        # Initiate Add Text Button
        self.initiate_add_text_btn()

        # Initiate Add Logo Button
        self.initiate_add_logo_btn()

        # Initiate Remove Button
        self.initiate_remove_btn()

        # Initiate Create Button
        self.initiate_create_btn()

    def initiate_close_btn(self):
        """
        Initialize the Close App button.

        This button closes the application.

        """
        self.close_app_btn = CTkButton(
            self,
            fg_color=GREY,
            border_color=WHITE,
            border_width=1,
            hover_color=WHITE,
            text_color=WHITE,
            text="Close App",
            command=self.parent.parent.destroy,
        )
        self.close_app_btn.grid(row=0, column=0)
        self.close_app_btn.bind(
            "<Enter>",
            lambda event: self.close_app_btn.configure(text_color=DARK, fg_color=WHITE),
        )
        self.close_app_btn.bind(
            "<Leave>",
            lambda event: self.close_app_btn.configure(text_color=WHITE, fg_color=GREY),
        )

    def initiate_back_btn(self):
        """
        Initialize the Back button.

        This button allows the user to go back to the main view.

        """
        self.back_btn = CTkButton(
            self,
            fg_color=GREY,
            border_color=WHITE,
            border_width=1,
            hover_color=WHITE,
            text_color=WHITE,
            text="Back",
            command=self.parent.parent.switch_to_main_view,
        )
        self.back_btn.grid(row=0, column=1)
        self.back_btn.bind(
            "<Enter>",
            lambda event: self.back_btn.configure(text_color=DARK, fg_color=WHITE),
        )
        self.back_btn.bind(
            "<Leave>",
            lambda event: self.back_btn.configure(text_color=WHITE, fg_color=GREY),
        )

    def initiate_add_text_btn(self):
        """
        Initialize the Add Text button.

        This button allows the user to add text as a watermark.

        """
        self.add_text_btn = CTkButton(
            self,
            fg_color=GREY,
            border_color=WHITE,
            border_width=1,
            hover_color=WHITE,
            text_color=WHITE,
            text="Add Text",
            command=lambda: self.parent.initiate_watermark(True),
        )
        self.add_text_btn.grid(row=0, column=5)
        self.add_text_btn.bind(
            "<Enter>",
            lambda event: self.add_text_btn.configure(text_color=DARK, fg_color=WHITE),
        )
        self.add_text_btn.bind(
            "<Leave>",
            lambda event: self.add_text_btn.configure(text_color=WHITE, fg_color=GREY),
        )

    def initiate_add_logo_btn(self):
        """
        Initialize the Add Logo button.

        This button allows the user to add a logo as a watermark.

        """
        self.add_logo_btn = CTkButton(
            self,
            fg_color=GREY,
            border_color=WHITE,
            border_width=1,
            hover_color=WHITE,
            text_color=WHITE,
            text="Add Logo",
            command=self.add_logo,
        )
        self.add_logo_btn.grid(row=0, column=6, columnspan=2)
        self.add_logo_btn.bind(
            "<Enter>",
            lambda event: self.add_logo_btn.configure(text_color=DARK, fg_color=WHITE),
        )
        self.add_logo_btn.bind(
            "<Leave>",
            lambda event: self.add_logo_btn.configure(text_color=WHITE, fg_color=GREY),
        )

    def initiate_remove_btn(self):
        """
        Initialize the Remove button.

        This button removes the current watermark.

        """
        self.remove_btn = CTkButton(
            self,
            fg_color=GREY,
            border_color=WHITE,
            border_width=1,
            hover_color=WHITE,
            text_color=WHITE,
            text="Remove",
            command=self.remove_btn_command,
        )
        self.remove_btn.grid(row=0, column=8)
        self.remove_btn.bind(
            "<Enter>",
            lambda event: self.remove_btn.configure(text_color=DARK, fg_color=WHITE),
        )
        self.remove_btn.bind(
            "<Leave>",
            lambda event: self.remove_btn.configure(text_color=WHITE, fg_color=GREY),
        )

    def initiate_create_btn(self):
        """
        Initialize the Create button.

        This button creates the final output image.

        """
        self.create_btn = CTkButton(
            self,
            fg_color=TURQUOISE,
            border_color=WHITE,
            border_width=1,
            hover_color=DARK_TURQUOISE,
            text_color=WHITE,
            text="Create",
            command=self.parent.save_img,
        )
        self.create_btn.grid(row=0, column=12)

    def add_logo(self):
        """
        Open a file dialog to add a logo image.
        """
        file_path = filedialog.askopenfilename(title="Select img", filetypes=FILE_TYPES)
        if file_path:
            self.parent.watermark_img_path = file_path
            self.parent.initiate_watermark(False)

    def remove_btn_command(self):
        if self.parent.watermark:
            self.parent.remove_watermark()
