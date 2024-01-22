# Standard library imports
from tkinter import StringVar, DoubleVar, IntVar, colorchooser
from threading import Thread
import time

# Third-party library imports
from customtkinter import (
    CTkToplevel,
    CTkFrame,
    CTkLabel,
    CTkEntry,
    CTkComboBox,
    CTkButton,
    CTkSlider,
    CTkSegmentedButton,
)

# Local imports
from utils import *

# Constants
FONT = ("Open Sans", 15, "bold")
LABEL_WIDTH = 80
FRAME_PADX = 10
FRAME_PADY = 2
DEBOUNCE_SEC = 0.5


class Properties(CTkToplevel):
    """
    Properties class represents the Watermark Properties window.

    This class extends CTkToplevel and provides a graphical interface for users to configure
    various properties of a watermark, including text, font, color, size, opacity, rotation, and tiling.

    Parameters:
        parent (Tk): The parent Tkinter window.
        is_text (bool): Indicates whether the watermark is text or image.
        *args, **kwargs: Additional arguments passed to the CTkToplevel constructor.
    """

    def __init__(self, parent, is_text=None, *args, **kwargs):
        """
        Initialize the Properties window.

        Args:
            parent (Tk): The parent Tkinter widget.
            is_text (bool): Indicates whether the watermark is text or image.
            *args, **kwargs: Additional arguments passed to the CTkToplevel constructor.
        """
        CTkToplevel.__init__(self, parent, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.configure(bg_color=GREY)
        self.parent = parent
        self.is_text = is_text
        self.thread_is_running = False
        self.last_execution_time = 0

        self.attributes("-topmost", "true")
        self.title("Watermark Properties")

        # Initialize Title
        self.initiate_title()

        # Initialize the row count
        self.row_number = 0

        # Check if the watermark is Text or Image
        if self.is_text:
            # Set the update function to update_text_watermark
            self.update_function = self.parent.update_text_watermark

            # Initialize Text Entry
            self.initiate_text()

            # Initialize Fonts Combobox
            self.initiate_font()

            # Initialize color selector
            self.initiate_color()

        else:
            # Set the update function to update_image_watermark
            self.update_function = self.parent.update_image_watermark

        # Initiate Size Selector
        self.initiate_size()

        # Initiate Opacity Selector
        self.initiate_opacity()

        # Initiate Rotation Selector
        self.initiate_rotation()

        # Initiate Tile Selector
        self.initiate_tile()

    def initiate_title(self):
        """Initialize the title label."""
        self.properties_title = CTkLabel(self, text="Properties:", font=FONT)
        self.properties_title.grid(row=0)

    def initiate_text(self):
        """Initialize Text-related elements."""
        self.row_number += 1

        # Text Frame
        self.text_frame = CTkFrame(self, fg_color=DARK)
        self.text_frame.grid(
            row=self.row_number, sticky=("e", "w"), padx=FRAME_PADX, pady=FRAME_PADY
        )

        # Text Label
        self.text_label = CTkLabel(
            self.text_frame, text="Text:", font=FONT, width=LABEL_WIDTH
        )
        self.text_label.grid(column=0, row=0)

        # Text  Entry
        self.text = StringVar()
        self.text.set("Text")
        self.text_entry = CTkEntry(self.text_frame, font=FONT, textvariable=self.text)
        self.text_entry.grid(column=1, row=0, columnspan=2)

        self.text.trace_add("write", self.watermark_callbacks)

    def initiate_font(self):
        """Initialize Font-related elements."""
        self.row_number += 1

        # Font Frame
        self.font_frame = CTkFrame(self, fg_color=DARK)
        self.font_frame.grid(
            row=self.row_number, sticky=("e", "w"), padx=FRAME_PADX, pady=FRAME_PADY
        )

        # Font Label
        self.font_label = CTkLabel(
            self.font_frame, text="Font:", font=FONT, width=LABEL_WIDTH
        )
        self.font_label.grid(column=0, row=0)

        # Font Combobox
        self.font = StringVar()
        self.font_combobox = CTkComboBox(
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
        )
        self.font_combobox.set("Arial")
        self.font_combobox.grid(column=1, row=0, columnspan=2)

        self.font.trace_add("write", self.watermark_callbacks)

    def initiate_color(self):
        """Initialize Color-related elements."""
        self.row_number += 1
        # Color Frame
        self.color_frame = CTkFrame(self, fg_color=DARK)
        self.color_frame.grid(
            row=self.row_number, sticky=("e", "w"), padx=FRAME_PADX, pady=FRAME_PADY
        )

        # Color Label
        self.color_label = CTkLabel(
            self.color_frame, text="Color:", font=FONT, width=LABEL_WIDTH
        )
        self.color_label.grid(column=0, row=0)

        # Color Selector
        self.color = StringVar(value="#000000")
        self.color_selector = CTkButton(
            self.color_frame,
            text=None,
            command=self.choose_color,
            fg_color=self.color.get(),
            hover_color=self.color.get(),
        )
        self.color_selector.grid(column=1, row=0, columnspan=2)

        self.color.trace_add("write", self.watermark_callbacks)

    def initiate_size(self):
        """Initialize Size-related elements."""
        self.row_number += 1

        # Size Frame
        self.size_frame = CTkFrame(self, fg_color=DARK)
        self.size_frame.grid(
            row=self.row_number, sticky=("e", "w"), padx=FRAME_PADX, pady=FRAME_PADY
        )

        # Color Label
        self.size_label = CTkLabel(
            self.size_frame, text="Size:", font=FONT, width=LABEL_WIDTH
        )
        self.size_label.grid(column=0, row=0)

        # Size Selector
        self.size = DoubleVar()
        self.size_selector = CTkSlider(
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
        self.size_value_var = StringVar()
        self.size_value_var.set("{:.2f}".format(self.size.get()))
        self.size_value_label = CTkLabel(
            self.size_frame, textvariable=self.size_value_var, font=FONT
        )
        self.size_value_label.grid(column=2, row=0)

        # Size 'x' Label
        self.size_x_label = CTkLabel(self.size_frame, text="x", font=FONT)
        self.size_x_label.grid(column=3, row=0)

        self.size.trace_add("write", self.watermark_callbacks)

    def initiate_opacity(self):
        """Initialize Opacity-related elements."""
        self.row_number += 1

        # Opacity Frame
        self.opacity_frame = CTkFrame(self, fg_color=DARK)
        self.opacity_frame.grid(
            row=self.row_number, sticky=("e", "w"), padx=FRAME_PADX, pady=FRAME_PADY
        )

        # Opacity Label
        self.opacity_label = CTkLabel(
            self.opacity_frame,
            text="Opacity:",
            font=FONT,
            width=LABEL_WIDTH,
        )
        self.opacity_label.grid(column=0, row=0)

        # Opacity Selector
        self.opacity = IntVar()
        self.opacity_selector = CTkSlider(
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
        self.opacity_value_label = CTkLabel(
            self.opacity_frame, textvariable=self.opacity, font=FONT
        )
        self.opacity_value_label.grid(column=2, row=0)

        # Opacity '%' Label
        self.opacity_pct_label = CTkLabel(self.opacity_frame, text="%", font=FONT)
        self.opacity_pct_label.grid(column=3, row=0)

        self.opacity.trace_add("write", self.watermark_callbacks)

    def initiate_rotation(self):
        """Initialize Rotation-related elements."""
        self.row_number += 1

        # Rotation Frame
        self.rotation_frame = CTkFrame(self, fg_color=DARK)
        self.rotation_frame.grid(
            row=self.row_number, sticky=("e", "w"), padx=FRAME_PADX, pady=FRAME_PADY
        )

        # Rotation Label
        self.rotation_label = CTkLabel(
            self.rotation_frame,
            text="Rotation:",
            font=FONT,
            width=LABEL_WIDTH,
        )
        self.rotation_label.grid(column=0, row=0)

        # Rotation Selector
        self.rotation = IntVar()
        self.rotation_selector = CTkSlider(
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
        self.rotation_value_label = CTkLabel(
            self.rotation_frame, textvariable=self.rotation, font=FONT
        )
        self.rotation_value_label.grid(column=2, row=0)

        # Rotation '°' Label
        self.opacity_deg_label = CTkLabel(self.rotation_frame, text="°", font=FONT)
        self.opacity_deg_label.grid(column=3, row=0)

        self.rotation.trace_add("write", self.watermark_callbacks)

    def initiate_tile(self):
        """Initialize Tile-related elements."""
        self.row_number += 1
        # Tile Frame
        self.tile_frame = CTkFrame(self, fg_color=DARK)
        self.tile_frame.grid(
            row=self.row_number, sticky=("e", "w"), padx=FRAME_PADX, pady=FRAME_PADY
        )

        # Tile Label
        self.tile_selector_label = CTkLabel(
            self.tile_frame, text="Tile:", font=FONT, width=LABEL_WIDTH
        )
        self.tile_selector_label.grid(column=0, row=0)

        # Tile Selector
        self.tile = StringVar()
        self.tile_selector = CTkSegmentedButton(
            self.tile_frame,
            values=["Single", "Multiple Square", "Multiple Diamond"],
            variable=self.tile,
        )
        self.tile.set("Single")
        self.tile_selector.grid(column=1, row=0, columnspan=2)

        self.tile.trace_add("write", self.tile_callbacks)

        # Tile Gap Label
        self.tile_gap_label = CTkLabel(
            self.tile_frame, text="Gap:", font=FONT, width=LABEL_WIDTH
        )

        # Tile Gap Selector
        self.tile_gap = IntVar()
        self.tile_gap_selector = CTkSlider(
            self.tile_frame,
            from_=0,
            to=200,
            number_of_steps=21,
            orientation="horizontal",
            variable=self.tile_gap,
        )
        self.tile_gap_selector.set(50)

        # Tile Gap Value Label
        self.tile_gap_value_label = CTkLabel(
            self.tile_frame, textvariable=self.tile_gap, font=FONT
        )

    def choose_color(self):
        """Open color chooser dialog and set the chosen color."""
        # variable to store hexadecimal code of color
        chosen_color = colorchooser.askcolor(title="Choose color")
        if chosen_color[1] is not None:
            self.color.set(chosen_color[1])
            self.color_selector.configure(
                fg_color=self.color.get(), hover_color=self.color.get()
            )

    def watermark_callbacks(self, var, index, mode):
        """Callback function for various watermark-related elements."""
        current_time = time.time()
        # Run the update function in a thread
        if (
            not self.thread_is_running
            and (current_time - self.last_execution_time) > DEBOUNCE_SEC
        ):
            self.size_value_var.set("{:.2f}".format(self.size.get()))
            # Update the last execution time
            self.last_execution_time = current_time
            # Run the update function in a thread
            new_thread = Thread(target=self.threaded_update_function)
            new_thread.start()

    def tile_callbacks(self, var, index, mode):
        """Callback function for tile-related elements."""
        self.watermark_callbacks(var, index, mode)

        if self.tile.get() != "Single":
            self.tile_gap_label.grid(column=0, row=1)
            self.tile_gap_selector.grid(column=1, row=1)
            self.tile_gap_value_label.grid(column=2, row=1)
            self.tile_gap.trace_add("write", self.watermark_callbacks)
        else:
            self.tile_gap_label.grid_forget()
            self.tile_gap_selector.grid_forget()
            self.tile_gap_value_label.grid_forget()

    def threaded_update_function(self):
        """Run the update function with indication of a thread being running"""
        self.thread_is_running = True
        self.update_function()
        self.thread_is_running = False
