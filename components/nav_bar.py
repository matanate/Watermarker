# Standard library imports
from tkinter import filedialog

# Third-party library imports
import customtkinter as ctk
from PIL import Image


# Local imports
from utils import *


class NavBar(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.configure(bg_color=GREY)
        self.parent = parent

        # Initiate Close app Button
        self.close_app_btn = ctk.CTkButton(
            self,
            height=30,
            width=100,
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

        # Initiate Back Button
        self.back_btn = ctk.CTkButton(
            self,
            height=30,
            width=100,
            fg_color=GREY,
            border_color=WHITE,
            border_width=1,
            hover_color=WHITE,
            text_color=WHITE,
            text="Back",
            command=lambda: self.parent.parent.__init__(),
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

        # Initiate Add Text Button
        self.add_text_btn = ctk.CTkButton(
            self,
            height=30,
            width=100,
            fg_color=GREY,
            border_color=WHITE,
            border_width=1,
            hover_color=WHITE,
            text_color=WHITE,
            text="Add Text",
            command=lambda: self.parent.initiate_text_watermark(True),
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

        # Initiate Add Logo Button
        self.add_logo_btn = ctk.CTkButton(
            self,
            height=30,
            width=100,
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

        # Initiate Remove Button
        self.remove_btn = ctk.CTkButton(
            self,
            height=30,
            width=100,
            fg_color=GREY,
            border_color=WHITE,
            border_width=1,
            hover_color=WHITE,
            text_color=WHITE,
            text="Remove",
            command=self.parent.remove_watermark,
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

        # Initiate Create Button
        self.create_btn = ctk.CTkButton(
            self,
            height=30,
            width=100,
            fg_color=TURQUOISE,
            border_color=WHITE,
            border_width=1,
            hover_color=DARK_TURQUOISE,
            text_color=WHITE,
            text="Create",
            command=self.parent.create_output_img,
        )
        self.create_btn.grid(row=0, column=12)

    def add_logo(self):
        file_path = filedialog.askopenfilename(
            initialdir="/",
            title="Select img",
            filetypes=(
                ("PNG files", "*.png"),
                ("BMP files", "*.bmp"),
                ("JPEG files", "*.jpeg"),
                ("All files", "*.*"),
            ),
        )
        if file_path:
            self.parent.pil_img_path = file_path
            self.parent.initiate_text_watermark(False)
