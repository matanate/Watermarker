# Standard library imports
from tkinter import filedialog, messagebox
import os

# Third-party library imports
from customtkinter import CTkFrame, CTkImage, CTkLabel, CTkButton
from PIL import Image
from tkinterdnd2 import DND_FILES

# Local imports
from utils import *
from views import CanvasView


class MainView(CTkFrame):
    """
    MainView class represents the main graphical user interface of the application.

    This class extends CTkFrame and serves as the entry point for the application. It contains
    methods to initialize various UI elements such as the logo, "Add Watermark" text label,
    buttons, and handles events related to image selection and drag-and-drop.

    Parameters:
        parent (Tk): The parent Tkinter window.
        switch_view (function): The function to switch between different views.
    """

    def __init__(self, parent, switch_view, *args, **kwargs):
        """
        Initialize the MainView.

        Parameters:
            parent (Tk): The parent Tkinter window.
            switch_view (function): The function to switch between different views.
        """

        CTkFrame.__init__(self, parent, *args, **kwargs)
        self.switch_view = switch_view
        self.parent = parent

        # Get the screen dimensions
        self.screen_w = self.parent.winfo_width()
        self.screen_h = self.parent.winfo_height()

        # Initiate Logo
        self.initiate_logo()

        # Initiate "Add Watermark" Text
        self.initiate_add_watermark_text()

        # Initialize "Add File" Button
        self.initiate_button()

        # Initiate "drag File" Text
        self.initiate_drag_text()

        # Bind the drag and drop events
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.get_dragged_img)

    def get_dragged_img(self, event):
        """
        Event handler for the drop event. Load the dropped image file.

        Parameters:
            event (tkinter.Event): The drop event.
        """
        # Load the dropped image file
        file_path = event.data
        self.process_img_url(file_path)

    def get_button_img(self):
        """
        Open a file dialog to select an image file and process the selected image.
        """
        file_path = filedialog.askopenfilename(title="Select img", filetypes=FILE_TYPES)
        if file_path:
            self.process_img_url(file_path)

    def process_img_url(self, file_path):
        """
        Process the image file and switch to the CanvasView.

        Parameters:
            file_path (str): The path of the image file.
        """
        try:
            # Remove curly braces and handle paths with spaces
            file_path = file_path.strip("{}").replace("\n", "")
            if file_path.startswith('"') and file_path.endswith('"'):
                file_path = file_path[1:-1]

            # Switch view to CanvasView
            self.switch_view(CanvasView, bg_image_path=file_path)

        except Exception as e:
            messagebox.showerror(title="Error loading image", message=e)

    def initiate_logo(self):
        """
        Initialize the logo image.
        """
        logo_path = os.path.join("resources", "images", "logo.ico")
        with Image.open(logo_path) as pil_img:
            img_dim = int((self.screen_h / 2) * 0.8)
            pil_img = pil_img.resize((img_dim, img_dim))
            self.logo_img = CTkImage(
                light_image=pil_img, dark_image=pil_img, size=(img_dim, img_dim)
            )
        self.logo = CTkLabel(self, image=self.logo_img, text=None)
        self.logo.pack(pady=((self.screen_h / 2) - img_dim) / 2)

    def initiate_add_watermark_text(self):
        """
        Initialize the "Add Watermark" text label.
        """
        self.text_label = CTkLabel(
            self,
            text="Add Watermark",
            font=("Open Sans", 30),
            text_color=WHITE,
        )
        self.text_label.pack(pady=20)

    def initiate_button(self):
        """
        Initialize the button to add a file.
        """
        self.button = CTkButton(
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

    def initiate_drag_text(self):
        """
        Initialize the drag-and-drop text label.
        """
        self.drag_text = CTkLabel(
            self,
            text="or drag file here",
            font=("Open Sans", 15),
            text_color=WHITE,
        )
        self.drag_text.pack()
