# Standard library imports
from itertools import product
from tkinter import filedialog, Canvas
from threading import Thread

# Third-party library imports
from customtkinter import CTkFrame
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageColor
from matplotlib import font_manager

# Local imports
from utils import *
from components import NavBar, Properties, SaveProgressDialog


class CanvasView(CTkFrame):
    """
    CanvasView class represents the canvas view where users can manipulate and add watermarks to images.

    This class extends CTkFrame and provides functionalities for adding text or image watermarks to the
    selected background image. It includes methods for updating the watermark, handling dragging events,
    and creating the final output image with the watermark applied.

    Parameters:
        parent (Tk): The parent Tkinter window.
        switch_view (function): Function to switch views.
        bg_image_path (str): Path to the background image file.
        *args, **kwargs: Additional arguments passed to the CTkFrame constructor.
    """

    def __init__(self, parent, switch_view, bg_image_path=None, *args, **kwargs):
        """
        Initialize the CanvasView.

        Args:
            parent (Tk): The parent Tkinter widget.
            switch_view (callable): Function to switch views.
            bg_image_path (str): Path to the background image file.
            *args, **kwargs: Additional arguments passed to the CTkFrame constructor.
        """
        CTkFrame.__init__(self, parent, *args, **kwargs)
        self.switch_view = switch_view
        self.parent = parent
        self.bg_image_path = bg_image_path

        # Get window Size
        self.window_w = self.parent.winfo_width()
        self.window_h = self.parent.winfo_height()

        # Set Canvas frame size
        self.canvas_frame_w = int(self.window_w * 0.9)
        self.canvas_frame_h = int(self.window_h * 0.9)

        # Variables Initiation
        self.font_cache = {}
        self.watermark = None

        # Initiate Navigation Bar
        self.navbar = NavBar(self)
        self.navbar.pack()

        # Open the image file with Pillow and convert it to PhotoImage
        self.get_bg_image()

        # Initiate Canvas
        self.initiate_canvas()

        # Variables to store the offset during dragging
        self.drag_data = {
            "x": int(self.canvas_w / 2),
            "y": int(self.canvas_h / 2),
            "item": None,
        }

        # Create background image on the canvas
        self.background_image = self.canvas.create_image(
            0, 0, anchor="nw", image=self.bg_img
        )

        # Bind the events for the watermark dragging
        self.canvas.tag_bind(WATERMARK_TAG, "<Button-1>", self.on_watermark_click)
        self.canvas.tag_bind(WATERMARK_TAG, "<B1-Motion>", self.move_watermark)
        self.canvas.tag_bind(
            WATERMARK_TAG, "<ButtonRelease-1>", self.on_watermark_release
        )

    def get_bg_image(self):
        """
        Load and preprocess the background image.
        """
        # Open the image file with Pillow and convert it to PhotoImage
        with Image.open(self.bg_image_path) as pil_img:
            self.org_bg_img = pil_img.copy()
            pil_img_w, pil_img_h = pil_img.size
            self.canvas_w, self.canvas_h = pil_img.size

            # Check if the image is already contained in the canvas
            if pil_img_w <= self.canvas_frame_w and pil_img_h <= self.canvas_frame_h:
                pass  # Return the original image
            else:
                # Calculate the aspect ratios
                img_aspect_ratio = pil_img_w / pil_img_h
                canvas_aspect_ratio = self.canvas_frame_w / self.canvas_frame_h

                # Calculate the new size to fit within the canvas while maintaining the aspect ratio
                if img_aspect_ratio > canvas_aspect_ratio:
                    self.canvas_w = self.canvas_frame_w
                    self.canvas_h = int(self.canvas_frame_w / img_aspect_ratio)
                else:
                    self.canvas_w = int(self.canvas_frame_h * img_aspect_ratio)
                    self.canvas_h = self.canvas_frame_h

            # Resize the image
            pil_img = pil_img.resize((self.canvas_w, self.canvas_h))
            self.bg_img_resize_ratio = pil_img_w / self.canvas_w

            # Create TkImage object of bg image
            self.bg_img = ImageTk.PhotoImage(
                image=pil_img, height=self.canvas_h, width=self.canvas_w
            )

    def initiate_canvas(self):
        """
        Initialize the Canvas widget.
        """
        self.canvas = Canvas(
            self,
            width=self.canvas_w,
            height=self.canvas_h,
            bg=WHITE,
            borderwidth=0,
            highlightthickness=0,
        )
        self.canvas.pack(pady=self.window_h * 0.04)

    def insert_watermark_to_canvas(self):
        """
        Insert the watermark into the Canvas widget.
        """
        # Create Tk Image from the PIL Image
        self.text_watermark_image = ImageTk.PhotoImage(image=self.watermark_pil_img)

        # Change the watermark object image if exists or create a new one if not
        if self.watermark:
            self.canvas.itemconfig(
                WATERMARK_TAG,
                image=self.text_watermark_image,
            )
            1
        else:
            self.watermark = self.canvas.create_image(
                (self.drag_data["x"], self.drag_data["y"]),
                image=self.text_watermark_image,
                tag=WATERMARK_TAG,
            )
            1

    def update_text_watermark(self):
        """
        Update the watermark image with text properties.
        """
        # Set properties variables
        text = self.properties.text.get()
        color = ImageColor.getcolor(self.properties.color.get(), "RGB")  # RGB color
        opacity = int(self.properties.opacity.get() * 255 / 100)
        rotation = self.properties.rotation.get()
        size = int(self.properties.size.get() * BASE_SIZE)
        font_family = self.properties.font.get()
        tile = self.properties.tile.get()
        tile_gap = self.properties.tile_gap.get()
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

        # Get text image size (hight set to double because of inaccuracy of getbbox method)
        text_bbox = font.getbbox(text)
        text_image_size = (
            text_bbox[2] - text_bbox[0],
            (text_bbox[3] - text_bbox[1]) * 2,
        )

        # Create PIL image
        self.watermark_pil_img = Image.new("RGBA", text_image_size, (0, 0, 0, 0))

        # Create ImageDraw object
        draw = ImageDraw.Draw(self.watermark_pil_img)

        # Draw the text on the image with the given parameters
        draw.text(
            (text_image_size[0] / 2, text_image_size[1] / 2),
            text,
            font=font,
            fill=color + (opacity,),
            stroke_width=1,
            stroke_fill=color + (opacity,),
            anchor="mm",
            align="center",
        )
        # Get the alpha channel
        alpha = self.watermark_pil_img.split()[-1]

        # Calculate the bounding box based on the alpha channel
        bbox = alpha.getbbox()
        self.watermark_pil_img = self.watermark_pil_img.crop(bbox)

        # Rotate the Text based on the rotation property
        self.watermark_pil_img = self.watermark_pil_img.rotate(
            rotation, expand=True, resample=RESAMPLE_METHOD
        )

        # Check Tile property and initiate the proper Tile configuration
        if tile != "Single":
            if tile == "Multiple Square":
                tile_diamond = False
            else:
                tile_diamond = True
            self.watermark_pil_img = self.create_img_grid(
                self.watermark_pil_img, tile_gap, tile_diamond
            )

        # Insert the watermark into the canvas
        self.insert_watermark_to_canvas()

    def update_image_watermark(self):
        """
        Update the watermark image with image properties.
        """
        # Create a copy of the original image
        self.watermark_pil_img = self.org_watermark_pil_img.copy()

        # Set properties variables
        opacity = int(self.properties.opacity.get() * 255 / 100)
        rotation = self.properties.rotation.get()
        size = int(self.properties.size.get() * BASE_SIZE)
        tile = self.properties.tile.get()
        tile_gap = self.properties.tile_gap.get()

        # Get image size, as set the hight to the size property
        img_w, img_h = self.watermark_pil_img.size
        img_size = (int(size * img_w / img_h), size)

        # resize the image to the selected size
        self.watermark_pil_img = self.watermark_pil_img.resize(img_size)

        # Make all opaque pixels into semi-opaque based on opacity property
        A = self.watermark_pil_img.getchannel("A")
        newA = A.point(lambda i: opacity if i > 0 else 0)

        # set the Image Opacity
        self.watermark_pil_img.putalpha(newA)

        # set the Image rotation
        self.watermark_pil_img = self.watermark_pil_img.rotate(
            rotation, expand=True, resample=RESAMPLE_METHOD
        )

        # Check Tile property and initiate the proper Tile configuration
        if tile != "Single":
            if tile == "Multiple Square":
                is_diamond = False
            else:
                is_diamond = True
            self.watermark_pil_img = self.create_img_grid(
                self.watermark_pil_img, tile_gap, is_diamond
            )

        # Insert the watermark into the canvas
        self.insert_watermark_to_canvas()

    def initiate_watermark(self, is_text):
        """
        Initialize the text or image watermark based on the user's choice.

        Args:
            is_text (bool): True for text watermark, False for image watermark.
        """
        # Reset the drag date to the center of the canvas
        self.drag_data["x"] = int(self.canvas_w / 2)
        self.drag_data["y"] = int(self.canvas_h / 2)

        # Check if a watermark exists, if so remove it
        if self.watermark:
            self.remove_watermark()

        # Initiate new properties object
        self.properties = Properties(self, is_text)

        # Initiate the proper watermark Text/Image
        if is_text:
            self.update_text_watermark()
        else:
            with Image.open(self.watermark_img_path) as image:
                self.org_watermark_pil_img = image.convert("RGBA")
            self.update_image_watermark()

    def remove_watermark(self):
        """
        Remove the current watermark from the canvas.
        """
        self.canvas.delete(self.watermark)
        self.watermark = None
        self.properties.destroy()

    def on_watermark_click(self, event):
        """
        Handle the event when the user clicks on the watermark.
        """
        # Store the initial position and the item ID for the watermark text
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["item"] = WATERMARK_TAG

    def move_watermark(self, event):
        """
        Handle the event when the user moves the watermark.
        """
        if self.drag_data["item"] == WATERMARK_TAG:
            # Calculate the offset
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]

            # Update the watermark text position with the offset
            self.canvas.move(WATERMARK_TAG, dx, dy)

            # Update the drag_data for the next iteration
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_watermark_release(self, event):
        """
        Handle the event when the user releases the mouse button after moving the watermark.
        """
        # Reset the drag_data when the mouse button is released
        self.drag_data["item"] = None

    def create_img_grid(self, image, gap, diamond=False):
        """
        Create a grid of images with a specified gap between them.

        Args:
            image (Image): The PIL Image to create a grid from.
            gap (int): The gap between images in pixels.
            diamond (bool): True if the grid should have a diamond pattern.

        Returns:
            Image: The resulting PIL Image grid.
        """
        # Get image size and calculate rows and columns number
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

            # Add horizontal offset for odd rows if set to diamond
            if diamond and row % 2 == 1:
                x += (img_width + gap) // 2

            img_grid.paste(image, (x, y))

        return img_grid

    def create_output_img(self, file_path):
        """
        Create the final output image by combining the background and watermark images.
        """

        pil_img = self.watermark_pil_img.copy()
        w, h = pil_img.size

        # Resize the watermark image to fit the original background image
        pil_img = self.watermark_pil_img.resize(
            (int(w * self.bg_img_resize_ratio), int(h * self.bg_img_resize_ratio)),
            resample=RESAMPLE_METHOD,
        )
        w_new, h_new = pil_img.size
        bg_pil_img = self.org_bg_img.copy()

        # Set the coordinates to pate the watermark
        img_cord = self.canvas.coords(WATERMARK_TAG)
        x = int(img_cord[0] * self.bg_img_resize_ratio - w_new / 2)
        y = int(img_cord[1] * self.bg_img_resize_ratio - h_new / 2)

        # Paste the watermark into the background
        bg_pil_img.paste(pil_img, (x, y), pil_img)

        # Save the image
        bg_pil_img.save(file_path)
        self.progress_dialog.stop()

    def save_img(self):
        # Ask the user for the file name and location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=FILE_TYPES
        )

        # Check if the user clicked "Cancel" do nothing
        if file_path:
            # Create and start the progress bar
            self.progress_dialog = SaveProgressDialog(self.parent)
            self.progress_dialog.start()

            # Run the save process in a thread
            save_thread = Thread(target=self.create_output_img, args=(file_path,))
            save_thread.start()
