import tkinter as tk
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageColor
from tkinter import filedialog, colorchooser, messagebox
from matplotlib import font_manager
from itertools import product

DARK = "#222831"
GREY = "#393E46"
TURQUOISE = "#00ADB5"
DARK_TURQUOISE = "#00959C"
WHITE = "#EEEEEE"


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
            command=lambda: self.parent.switch_view(MainView),
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
            with Image.open(file_path) as image:
                self.parent.pil_img = image.convert("RGBA")
            self.parent.initiate_text_watermark(False)


class MainView(ctk.CTkFrame):
    def __init__(self, parent, switch_view, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.switch_view = switch_view
        self.parent = parent

        self.screen_w = self.parent.winfo_width()
        self.screen_h = self.parent.winfo_height()

        # Initiate Logo
        with Image.open("img/logo.png") as pil_img:
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


class CanvasView(ctk.CTkFrame):
    def __init__(self, parent, switch_view, image_path=None, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.switch_view = switch_view
        self.parent = parent
        self.image_path = image_path

        self.screen_w = self.parent.winfo_width()
        self.screen_h = self.parent.winfo_height()
        self.font_cache = {}

        # Initiate Canvas
        self.canvas_w = int(self.screen_w * 0.8)
        self.canvas_h = int(self.screen_h * 0.8)

        self.navbar = NavBar(self)
        self.navbar.grid(column=0, row=0)

        self.watermark = None

        # Open the image file with Pillow and convert it to PhotoImage
        with Image.open(self.image_path) as pil_img:
            pil_img_w, pil_img_h = pil_img.size
            new_w, new_h = pil_img.size

            # Check if the image is already contained in the canvas
            if pil_img_w <= self.canvas_w and pil_img_h <= self.canvas_h:
                pass  # Return the original image
            else:
                # Calculate the aspect ratios
                img_aspect_ratio = pil_img_w / pil_img_h
                canvas_aspect_ratio = self.canvas_w / self.canvas_h

                # Calculate the new size to fit within the canvas while maintaining the aspect ratio
                if img_aspect_ratio > canvas_aspect_ratio:
                    new_w = self.canvas_w
                    new_h = int(self.canvas_w / img_aspect_ratio)
                else:
                    new_w = int(self.canvas_h * img_aspect_ratio)
                    new_h = self.canvas_h

            self.bg_pil_img = pil_img
            # Resize the image
            pil_img = pil_img.resize((new_w, new_h), Image.BICUBIC)
            self.bg_img_resize_ratio = pil_img_w / new_w
            self.bg_img = ImageTk.PhotoImage(image=pil_img)

            self.canvas = ctk.CTkCanvas(self, width=new_w, height=new_h, bg=WHITE)
            self.canvas.grid(
                column=0,
                row=1,
                pady=int((self.canvas_h - new_h) / 2),
                padx=int((self.canvas_w - new_w) / 2),
            )

            self.canvas_h = new_h
            self.canvas_w = new_w

            # Create image with anchor set to "NW" and unique tag for identification as background
            self.background_image = self.canvas.create_image(
                self.canvas_w / 2, self.canvas_h / 2, image=self.bg_img
            )

        # Variables to store the offset during dragging
        self.drag_data = {
            "x": int(self.canvas_w / 2),
            "y": int(self.canvas_h / 2),
            "item": None,
        }
        # Bind the text events for the watermark
        self.canvas.tag_bind("watermark", "<Button-1>", self.on_watermark_click)
        self.canvas.tag_bind("watermark", "<B1-Motion>", self.move_watermark)
        self.canvas.tag_bind(
            "watermark", "<ButtonRelease-1>", self.on_watermark_release
        )

    def update_text_image(self):
        # Define the variables
        text = self.properties.text.get()
        color = ImageColor.getcolor(self.properties.color.get(), "RGB")
        opacity = int(self.properties.opacity.get() * 255 / 100)
        rotation = self.properties.rotation.get()
        size = int(self.properties.size.get() * 30)
        font_family = self.properties.font.get()
        font_weight = "bold"

        # Create or reuse the font
        font_key = (font_family, font_weight, size)
        if font_key not in self.font_cache:
            self.font_cache[font_key] = ImageFont.truetype(
                font=font_manager.findfont(
                    font_manager.FontProperties(family=font_family, weight=font_weight)
                ),
                size=size,
            )
        font = self.font_cache[font_key]

        # Get text image size
        text_bbox = font.getbbox(text)
        image_size = (text_bbox[2] - text_bbox[0], (text_bbox[3] - text_bbox[1]) * 2)

        # Create PIL image
        self.pil_img = Image.new("RGBA", image_size, (0, 0, 0, 0))
        # Create ImageDraw object
        draw = ImageDraw.Draw(self.pil_img)

        # Draw the text on the image with the specified opacity
        draw.text(
            (image_size[0] / 2, image_size[1] / 2),
            text,
            font=font,
            fill=color + (opacity,),
            stroke_width=1,
            stroke_fill=color + (opacity,),
            anchor="mm",
            align="center",
        )
        # Get the alpha channel
        alpha = self.pil_img.split()[-1]
        # Calculate the bounding box based on the alpha channel
        bbox = alpha.getbbox()
        self.pil_img = self.pil_img.crop(bbox)

        self.pil_img = self.pil_img.rotate(
            rotation, expand=True, resample=Image.BICUBIC
        )

        if self.properties.tile.get() != "Single":
            if self.properties.tile.get() == "Multiple Square":
                tile_diamond = False
            else:
                tile_diamond = True
            self.pil_img = self.create_img_grid(
                self.pil_img, self.properties.tile_gap.get(), tile_diamond
            )

        self.text_image = ImageTk.PhotoImage(image=self.pil_img)

        if self.watermark:
            self.canvas.itemconfig(
                "watermark",
                image=self.text_image,
            )
        else:
            self.watermark = self.canvas.create_image(
                (self.drag_data["x"], self.drag_data["y"]),
                image=self.text_image,
                tag="watermark",
            )

    def update_image(self):
        # Define the variables
        opacity = int(self.properties.opacity.get() * 255 / 100)
        rotation = self.properties.rotation.get()
        size = int(self.properties.size.get() * 30)
        img_w, img_h = self.pil_img.size
        img_size = (int(size * img_w / img_h), size)

        # set the Image Size
        self.pil_img = self.pil_img.resize(img_size)
        A = self.pil_img.getchannel("A")

        # Make all opaque pixels into semi-opaque
        newA = A.point(lambda i: opacity if i > 0 else 0)

        # set the Image Opacity
        self.pil_img.putalpha(newA)

        # set the Image rotation
        self.pil_img = self.pil_img.rotate(
            rotation, expand=True, resample=Image.BICUBIC
        )

        if self.properties.tile.get() != "Single":
            if self.properties.tile.get() == "Multiple Square":
                is_diamond = False
            else:
                is_diamond = True
            self.pil_img = self.create_img_grid(
                self.pil_img, self.properties.tile_gap.get(), is_diamond
            )

        self.logo_img = ImageTk.PhotoImage(image=self.pil_img)

        if self.watermark:
            self.canvas.itemconfig(
                "watermark",
                image=self.logo_img,
            )
        else:
            self.watermark = self.canvas.create_image(
                (self.drag_data["x"], self.drag_data["y"]),
                image=self.logo_img,
                tag="watermark",
            )

    def initiate_text_watermark(self, is_text):
        self.drag_data["x"] = int(self.canvas_w / 2)
        self.drag_data["y"] = int(self.canvas_h / 2)
        if self.watermark:
            self.remove_watermark()

        self.properties = Properties(self, is_text)
        self.properties.grid(column=1, row=1, pady=20)
        if is_text:
            self.update_text_image()
        else:
            self.update_image()

    def remove_watermark(self):
        self.canvas.delete(self.watermark)
        self.watermark = None
        self.properties.destroy()

    def on_watermark_click(self, event):
        # Store the initial position and the item ID for the watermark text
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["item"] = "watermark"

    def move_watermark(self, event):
        if self.drag_data["item"] == "watermark":
            # Calculate the offset
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]

            # Update the watermark text position with the offset
            self.canvas.move("watermark", dx, dy)

            # Update the drag_data for the next iteration
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_watermark_release(self, event):
        # Reset the drag_data when the mouse button is released
        self.drag_data["item"] = None

    def create_img_grid(self, image, gap, diamond=False):
        # Assuming all images have the same dimensions
        img_width, img_height = image.size
        rows = int(self.canvas_h / (img_height + gap)) + 3
        cols = int(self.canvas_w / (img_width + gap)) + 3

        # Create a blank image
        img_grid = Image.new(
            "RGBA", (cols * (img_width + gap), rows * (img_height + gap)), (0, 0, 0, 0)
        )
        # Paste the same image onto the blank image with the specified gap

        for row, col in product(range(rows), range(cols)):
            x = col * (img_width + gap)
            y = row * (img_height + gap)

            # Add horizontal offset for odd rows
            if diamond and row % 2 == 1:
                x += (img_width + gap) // 2

            img_grid.paste(image, (x, y))

        return img_grid

    def create_output_img(self):
        # Ask the user for the file name and location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        )

        # Check if the user clicked "Cancel"
        if file_path:
            pil_img = self.pil_img.copy()
            w, h = pil_img.size
            pil_img = self.pil_img.resize(
                (int(w * self.bg_img_resize_ratio), int(h * self.bg_img_resize_ratio)),
                resample=Image.Resampling.BICUBIC,
            )
            bg_pil_img = self.bg_pil_img.copy()
            x = int(self.drag_data["x"] * self.bg_img_resize_ratio - w / 2)
            y = int(self.drag_data["y"] * self.bg_img_resize_ratio - h / 2)

            bg_pil_img.paste(pil_img, (x, y), pil_img)
            # Save the image
            bg_pil_img.save(file_path)


class MainApplication(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.current_view = None

        # Initialize Window
        self.parent.title("Watermarker")
        self.parent.iconbitmap("img/logo.ico")
        self.screen_w = int(self.parent.winfo_screenwidth() * 0.8)
        self.screen_h = int(self.parent.winfo_screenheight() * 0.8)
        self.parent.geometry(f"{self.screen_w}x{self.screen_h}")
        self.parent.configure(bg=DARK)
        self.after(50, lambda: self.switch_view(MainView))

    def switch_view(self, view_class, *args, **kwargs):
        new_view = view_class(self.parent, self.switch_view, *args, **kwargs)

        if self.current_view:
            self.current_view.destroy()

        new_view.pack(fill="both", expand=True)
        self.current_view = new_view


class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


def main():
    ctk.set_appearance_mode("dark")
    root = Tk()
    app = MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
