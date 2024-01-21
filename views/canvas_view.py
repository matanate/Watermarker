# Standard library imports
from itertools import product
from tkinter import filedialog

# Third-party library imports
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageColor
from matplotlib import font_manager

# Local imports
from utils import *
from components import NavBar, Properties


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
        with Image.open(self.pil_img_path) as image:
            self.pil_img = image.convert("RGBA")
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
