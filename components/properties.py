# Standard library imports
import tkinter as tk
from tkinter import colorchooser

# Third-party library imports
import customtkinter as ctk

# Local imports
from utils import *


class Properties(ctk.CTkFrame):
    def __init__(self, parent, is_text=None, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.configure(bg_color=GREY)
        self.parent = parent
        self.is_text = is_text
        # Initialize Title
        self.properties_title = ctk.CTkLabel(
            self, text="Properties:", font=("Open Sans", 15, "bold")
        )
        self.properties_title.grid(row=0)
        row_number = 1
        if self.is_text:
            self.update_function = self.parent.update_text_image

            # Initialize Text input
            row_number += 1
            # Text input Frame
            self.text_input_frame = ctk.CTkFrame(self, bg_color=DARK)
            self.text_input_frame.grid(row=row_number)
            # Text input Label
            self.text_input_label = ctk.CTkLabel(
                self.text_input_frame, text="Text:", font=("Open Sans", 15)
            )
            self.text_input_label.grid(column=0, row=0)

            # Text input Entry
            self.text = tk.StringVar()
            self.text.set("Text")
            self.text_input_entry = ctk.CTkEntry(
                self.text_input_frame, font=("Open Sans", 15), textvariable=self.text
            )
            self.text_input_entry.grid(column=1, row=0)

            self.text.trace_add("write", self.text_callbacks)

            # Initialize Fonts Combobox
            row_number += 1
            # Font Frame
            self.font_frame = ctk.CTkFrame(self, bg_color=DARK)
            self.font_frame.grid(row=row_number)

            # Font Label
            self.font_label = ctk.CTkLabel(
                self.font_frame, text="Font:", font=("Open Sans", 15)
            )
            self.font_label.grid(column=0, row=0)

            # Font Combobox
            self.font = tk.StringVar()
            self.font_combobox = ctk.CTkComboBox(
                self.font_frame,
                state="readonly",
                values=[
                    "Arial",
                    "Courier New",
                    "Times New Roman",
                    "Calibri",
                    "David",
                    "Segoe UI",
                    "DejaVu Serif",
                    "Modern No. 20",
                ],
                variable=self.font,
                bg_color=DARK,
            )
            self.font_combobox.set("Arial")
            self.font_combobox.grid(column=1, row=0)

            self.font.trace_add("write", self.text_callbacks)

            # Initialize color selector
            row_number += 1
            # Color Frame
            self.color_frame = ctk.CTkFrame(self, bg_color=DARK)
            self.color_frame.grid(row=row_number)

            # Color Label
            self.color_label = ctk.CTkLabel(
                self.color_frame, text="Color:", font=("Open Sans", 15)
            )
            self.color_label.grid(column=0, row=0)

            # Color Selector
            self.color = tk.StringVar(value="#000000")
            self.color_selector = ctk.CTkButton(
                self.color_frame,
                text=None,
                command=self.choose_color,
                fg_color=self.color.get(),
                hover_color=self.color.get(),
            )
            self.color_selector.grid(column=1, row=0)

            self.color.trace_add("write", self.text_callbacks)
        else:
            self.update_function = self.parent.update_image
        # initiate size selector
        row_number += 1
        # Size Frame
        self.size_frame = ctk.CTkFrame(self, bg_color=DARK)
        self.size_frame.grid(row=row_number)

        # Size Label
        self.size_selector_label = ctk.CTkLabel(
            self.size_frame, text="Size:", font=("Open Sans", 15)
        )
        self.size_selector_label.grid(column=0, row=0)

        # Size Selector
        self.size = tk.DoubleVar()
        self.size_selector = ctk.CTkSlider(
            self.size_frame,
            from_=0.2,
            to=8.0,
            number_of_steps=78,
            orientation="horizontal",
            variable=self.size,
        )
        self.size_selector.grid(column=1, row=0)
        self.size_selector.set(1.0)

        # Size Value Label
        self.size_value_var = tk.StringVar()
        self.size_value_var.set("{:.2f}".format(self.size.get()))
        self.size_value_label = ctk.CTkLabel(
            self.size_frame, textvariable=self.size_value_var, font=("Open Sans", 15)
        )
        self.size_value_label.grid(column=2, row=0)

        self.size.trace_add("write", self.text_callbacks)

        # Initiate Opacity Selector
        row_number += 1
        # Opacity Frame
        self.opacity_frame = ctk.CTkFrame(self, bg_color=DARK)
        self.opacity_frame.grid(row=row_number)

        # Opacity Label
        self.opacity_label = ctk.CTkLabel(
            self.opacity_frame, text="Opacity:", font=("Open Sans", 15)
        )
        self.opacity_label.grid(column=0, row=0)

        # Opacity Selector
        self.opacity = tk.IntVar()
        self.opacity_selector = ctk.CTkSlider(
            self.opacity_frame,
            from_=1,
            to=100,
            number_of_steps=100,
            orientation="horizontal",
            variable=self.opacity,
        )
        self.opacity_selector.grid(column=1, row=0)
        self.opacity_selector.set(100)

        # Opacity Value Label
        self.opacity_value_label = ctk.CTkLabel(
            self.opacity_frame, textvariable=self.opacity, font=("Open Sans", 15)
        )
        self.opacity_value_label.grid(column=2, row=0)

        self.opacity.trace_add("write", self.text_callbacks)

        # Initiate Rotation
        row_number += 1
        # Rotation Frame
        self.rotation_frame = ctk.CTkFrame(self, bg_color=DARK)
        self.rotation_frame.grid(row=row_number)

        # Rotation Label
        self.rotation_label = ctk.CTkLabel(
            self.rotation_frame, text="Rotation:", font=("Open Sans", 15)
        )
        self.rotation_label.grid(column=0, row=0)

        # Rotation Selector
        self.rotation = tk.IntVar()
        self.rotation_selector = ctk.CTkSlider(
            self.rotation_frame,
            from_=-180,
            to=180,
            number_of_steps=361,
            orientation="horizontal",
            variable=self.rotation,
        )
        self.rotation_selector.grid(column=1, row=0)
        self.rotation_selector.set(0)

        # Rotation Value Label
        self.rotation_value_label = ctk.CTkLabel(
            self.rotation_frame, textvariable=self.rotation, font=("Open Sans", 15)
        )
        self.rotation_value_label.grid(column=2, row=0)

        self.rotation.trace_add("write", self.text_callbacks)

        # Initiate Tile
        row_number += 1
        # Tile Frame
        self.tile_frame = ctk.CTkFrame(self, bg_color=DARK)
        self.tile_frame.grid(row=row_number)

        # Tile Label
        self.tile_selector_label = ctk.CTkLabel(
            self.tile_frame, text="Tile:", font=("Open Sans", 15)
        )
        self.tile_selector_label.grid(column=0, row=0)

        # Tile Selector
        self.tile = tk.StringVar()
        self.tile_selector = ctk.CTkSegmentedButton(
            self.tile_frame,
            values=["Single", "Multiple Square", "Multiple Diamond"],
            variable=self.tile,
        )
        self.tile.set("Single")
        self.tile_selector.grid(column=1, row=0)

        self.tile.trace_add("write", self.tile_callbacks)

        # initiate tile gap
        # Tile Gap Label
        self.tile_gap_label = ctk.CTkLabel(
            self.tile_frame, text="Gap:", font=("Open Sans", 15)
        )

        # Tile Gap Selector
        self.tile_gap = tk.IntVar()
        self.tile_gap_selector = ctk.CTkSlider(
            self.tile_frame,
            from_=0,
            to=200,
            number_of_steps=21,
            orientation="horizontal",
            variable=self.tile_gap,
        )
        self.tile_gap_selector.set(20)

        # Tile Gap Value Label
        self.tile_gap_value_label = ctk.CTkLabel(
            self.tile_frame, textvariable=self.tile_gap, font=("Open Sans", 15)
        )

    def choose_color(self):
        # variable to store hexadecimal code of color
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code[1] is not None:
            self.color.set(color_code[1])
            self.color_selector.configure(
                fg_color=self.color.get(), hover_color=self.color.get()
            )

    def text_callbacks(self, var, index, mode):
        self.size_value_var.set("{:.2f}".format(self.size.get()))
        self.update_function()

    def tile_callbacks(self, var, index, mode):
        self.update_function()
        if self.tile.get() != "Single":
            self.tile_gap_label.grid(column=0, row=1)
            self.tile_gap_selector.grid(column=1, row=1)
            self.tile_gap_value_label.grid(column=2, row=1)
            self.tile_gap.trace_add("write", self.text_callbacks)
        else:
            self.tile_gap_label.grid_forget()
            self.tile_gap_selector.grid_forget()
            self.tile_gap_value_label.grid_forget()
