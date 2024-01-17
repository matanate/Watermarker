from tkinter import *
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
from tkinter import simpledialog, filedialog


class WatermarkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermarker")
        self.screen_w = int(self.root.winfo_screenwidth() * 0.8)
        self.screen_h = int(self.root.winfo_screenheight() * 0.8)
        self.root.geometry(f"{self.screen_w}x{self.screen_h}")
        self.root.configure(bg="white")

        self.canvas_w = int(self.screen_w * 0.8)
        self.canvas_h = int(self.screen_h * 0.8)

        self.my_canvas = Canvas(
            root, width=self.canvas_w, height=self.canvas_h, bg="#EEEEEE"
        )
        self.my_canvas.pack(pady=20)

        pil_img = Image.open("img/logo.png")
        pil_img.resize(
            ((int((self.canvas_w / 2) * 0.8)), int((self.canvas_h / 2) * 0.8))
        )
        self.logo = ImageTk.PhotoImage(pil_img)
        self.logo_img = self.my_canvas.create_image(
            self.canvas_w / 2,
            self.canvas_h / 4,
            image=self.logo,
            tags="logo-img",
        )
        self.my_canvas.create_text(
            self.canvas_w / 2,
            self.canvas_h / 2,
            text="Add Watermark",
            font=("Arial", 30),
        )

        self.img = None
        self.img_h = 0
        self.img_w = 0
        self.x = self.canvas_w / 2
        self.y = self.canvas_h / 2
        self.background_image = None
        self.watermark_text = None
        self.watermark_img = None

        # Variables to store the offset during dragging
        self.drag_data = {"x": 0, "y": 0, "item": None}

        # Bind the drag and drop events
        self.my_canvas.drop_target_register(DND_FILES)
        self.my_canvas.dnd_bind("<<Drop>>", self.load_image)

        # Bind the text events for the watermark
        self.my_canvas.tag_bind(
            "watermark-text", "<Button-1>", self.on_watermark_text_click
        )
        self.my_canvas.tag_bind(
            "watermark-text", "<B1-Motion>", self.move_watermark_text
        )
        self.my_canvas.tag_bind(
            "watermark-text", "<ButtonRelease-1>", self.on_watermark_text_release
        )

        # Menu for adding watermark text
        menu = Menu(root)
        root.config(menu=menu)
        watermark_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Watermark", menu=watermark_menu)
        watermark_menu.add_command(label="Add Text", command=self.add_watermark_text)
        watermark_menu.add_command(label="Add Image", command=self.add_watermark_img)

    def load_image(self, event):
        # Load the dropped image file
        file_path = event.data
        try:
            # Remove curly braces and handle paths with spaces
            file_path = file_path.strip("{}").replace("\n", "")
            if file_path.startswith('"') and file_path.endswith('"'):
                file_path = file_path[1:-1]

            # Open the image file with Pillow and convert it to PhotoImage
            pil_img = Image.open(file_path)
            pil_img_w, pil_img_h = pil_img.size
            if pil_img_h / pil_img_w > self.canvas_h / self.canvas_w:
                new_img_h = self.canvas_h
                new_img_w = int(pil_img_w * (self.canvas_h / pil_img_h))
            else:
                new_img_h = int(pil_img_h * (self.canvas_w / pil_img_w))
                new_img_w = self.canvas_w
            pil_img = pil_img.resize((new_img_w, new_img_h))
            self.img = ImageTk.PhotoImage(pil_img)
            self.img_w = self.img.width()
            self.img_h = self.img.height()

            # Create image with anchor set to "NW" and unique tag for identification as background
            self.background_image = self.my_canvas.create_image(
                self.canvas_w / 2,
                self.canvas_h / 2,
                image=self.img,
                tags="background",
            )
            self.my_canvas.tag_lower("background")

        except Exception as e:
            print(f"Error loading image: {e}")

    def on_watermark_img_click(self, event):
        # Check if the click is within the bounding box of the image
        item_id = self.my_canvas.find_withtag("watermark-img")
        if item_id and item_id[0] == self.watermark_img:
            # Store the initial position and the item ID
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            self.drag_data["item"] = "watermark-img"

    def move_watermark_img(self, event):
        if self.drag_data["item"] == "watermark-img":
            # Calculate the offset
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]

            # Update the canvas position with the offset
            self.my_canvas.move(self.background_image, dx, dy)

            # Update the drag_data for the next iteration
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_watermark_img_release(self, event):
        # Reset the drag_data when the mouse button is released
        self.drag_data["item"] = None

    def add_watermark_img(self):
        img_path = filedialog.askopenfilename(
            initialdir="/",
            title="Select img",
            filetypes=(
                ("PNG files", "*.png"),
                ("BMP files", "*.bmp"),
                ("JPEG files", "*.jpeg"),
                ("All files", "*.*"),
            ),
        )
        if img_path:
            # Delete previous watermarks if it exists
            if self.watermark_text:
                self.my_canvas.delete(self.watermark_text)
            if self.watermark_img:
                self.my_canvas.delete(self.watermark_img)

            # Calculate the center of the canvas
            canvas_center_x = self.my_canvas.winfo_reqwidth() / 2
            canvas_center_y = self.my_canvas.winfo_reqheight() / 2

            # Add new watermark text to the canvas at the center
            pil_img = Image.open(img_path)
            self.img = ImageTk.PhotoImage(pil_img)

            # Create image with anchor set to "NW" and unique tag for identification as background
            self.watermark_img = self.my_canvas.create_image(
                0, 0, anchor=NW, image=self.img, tags="watermark-img"
            )

    def add_watermark_text(self):
        # Prompt user for text input
        text = simpledialog.askstring("Watermark Text", "Enter text for watermark:")
        if text:
            # Delete previous watermarks if it exists
            if self.watermark_text:
                self.my_canvas.delete(self.watermark_text)
            if self.watermark_img:
                self.my_canvas.delete(self.watermark_img)

            # Calculate the center of the canvas
            canvas_center_x = self.my_canvas.winfo_reqwidth() / 2
            canvas_center_y = self.my_canvas.winfo_reqheight() / 2

            # Add new watermark text to the canvas at the center
            self.watermark_text = self.my_canvas.create_text(
                canvas_center_x,
                canvas_center_y,
                text=text,
                font=("Helvetica", 12),
                fill="red",
                tags="watermark-text",
            )

    def on_watermark_text_click(self, event):
        # Store the initial position and the item ID for the watermark text
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["item"] = "watermark-text"

    def move_watermark_text(self, event):
        if self.drag_data["item"] == "watermark-text":
            # Calculate the offset
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]

            # Update the watermark text position with the offset
            self.my_canvas.move("watermark-text", dx, dy)

            # Update the drag_data for the next iteration
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_watermark_text_release(self, event):
        # Reset the drag_data when the mouse button is released
        self.drag_data["item"] = None


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = WatermarkerApp(root)
    root.mainloop()
