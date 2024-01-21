# Standard library imports
from tkinter import filedialog, messagebox

# Third-party library imports
import customtkinter as ctk
from PIL import Image
from tkinterdnd2 import DND_FILES

# Local imports
from utils import *
from views import CanvasView


class MainView(ctk.CTkFrame):
    def __init__(self, parent, switch_view, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.switch_view = switch_view
        self.parent = parent

        self.screen_w = self.parent.winfo_width()
        self.screen_h = self.parent.winfo_height()

        # Initiate Logo
        with Image.open("resources\images\logo.ico") as pil_img:
            img_dim = int((self.screen_h / 2) * 0.8)
            pil_img.resize((img_dim, img_dim))
            self.logo_img = ctk.CTkImage(
                light_image=pil_img, dark_image=pil_img, size=(img_dim, img_dim)
            )
        self.logo = ctk.CTkLabel(self, image=self.logo_img, text=None)
        self.logo.pack(pady=((self.screen_h / 2) - img_dim) / 2)

        # Initiate Text
        self.text_label = ctk.CTkLabel(
            self,
            text="Add Watermark",
            font=("Open Sans", 30),
            text_color=WHITE,
        )
        self.text_label.pack(pady=20)

        # Initialize Button
        self.button = ctk.CTkButton(
            self,
            fg_color=TURQUOISE,
            hover_color=DARK_TURQUOISE,
            text="Add File",
            font=("Open Sans", 25, "bold"),
            width=150,
            height=50,
            command=self.get_button_img,
        )
        self.button.pack()

        # Initiate Text
        self.text_label1 = ctk.CTkLabel(
            self,
            text="or drag file here",
            font=("Open Sans", 15),
            text_color=WHITE,
        )
        self.text_label1.pack()

        # Bind the drag and drop events
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.get_dragged_img)

    def get_dragged_img(self, event):
        # Load the dropped image file
        file_path = event.data
        self.process_img_url(file_path)

    def get_button_img(self):
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
            self.process_img_url(file_path)

    def process_img_url(self, file_path):
        try:
            # Remove curly braces and handle paths with spaces
            file_path = file_path.strip("{}").replace("\n", "")
            if file_path.startswith('"') and file_path.endswith('"'):
                file_path = file_path[1:-1]

            # Switch view to CanvasView
            self.switch_view(CanvasView, image_path=file_path)

        except Exception as e:
            messagebox.showerror(title="Error loading image", message=e)
