import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from functools import partial
from collections import deque

# ========== Setup main window ==========
root = tk.Tk()
root.title("Cosmic Composers")
root.geometry("800x800")  # Optional: set a window size
root.configure(bg='black')
image_paths = ["galaxy1.jpeg", "galaxy.png", "galaxy2.jpeg", "galaxy3.png"]  # Use your real paths
image_paths = deque(image_paths)  # Use deque for easy rotation

style = ttk.Style(root)
style.configure('TButton',
                foreground='black',  # Changed to white for visibility on black
                background='black',
                font=('Arial', 12),
                relief='raised')
# ========== Configure grid weights ==========
root.grid_columnconfigure(0, weight=3)  # Left column (big)
root.grid_columnconfigure(1, weight=1)  # Right column
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# ========== Left (big) section ==========
left_frame = tk.Frame(root, bg='black', pady=20)
left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
#setup carousel
carousel_frame = tk.Frame(left_frame, bg='black')
carousel_frame.pack(side="top", fill="x")
#setup coordinates label
coord_frame = tk.Frame(left_frame, bg='black')
coord_frame.pack(side="top", fill="x", padx=10, pady=5)
coor_inner = tk.Frame(coord_frame, bg='black')
coor_inner.pack(anchor="center")
# Create a label to display coordinates
coord_label = tk.Label(
    coor_inner,
    text="Click on the image",
    bg='white',
    fg='black',
    font=('Arial', 11),
    relief='solid',
    bd=1
)
coord_label.pack(side="top", fill="x", padx=10, pady=5)
#setup image canvas
imageCanvas = tk.Canvas(left_frame, bg='black', highlightthickness=0)
imageCanvas.pack(fill="both", expand=True)
# Setup carousel
carousel_frame = tk.Frame(left_frame, bg='black')
carousel_frame.pack(side="top", fill="x", pady=(5, 0))

# Inner frame for centering
carousel_inner = tk.Frame(carousel_frame, bg='black')
carousel_inner.pack(anchor="center")

# Create thumbnails
thumbnails = []
for path in image_paths:
    thumb = Image.open(path).copy()
    thumb.thumbnail((60, 60)) 
    thumbnails.append(ImageTk.PhotoImage(thumb))
thumbnails = deque(thumbnails)  # always keep current image at the second position
left_btn = tk.Button(carousel_inner, text="<", width=2, borderwidth=0, highlightthickness=0, command=lambda: update_image(1))
left_btn.pack(side="left", padx=10)

three_thumbnails = []
for i, thumb in enumerate(thumbnails):
    thumbnail_label = tk.Label(carousel_inner, image=thumbnails[i], bg='white', bd=2, relief="ridge")
    thumbnail_label.pack(side="left", padx=10)
    three_thumbnails.append(thumbnail_label)
    if i==2: break

right_btn = tk.Button(carousel_inner, text=">", width=2, bd=0, command=lambda: update_image(-1))
right_btn.pack(side="left", padx=10)

# ===== Carousel functions =====
def update_image(new_index):
    global img, tk_img, three_thumbnails, image_paths, thumbnails
    if new_index < 0:
        thumbnails.rotate(-1)
        image_paths.rotate(-1)
    else:
        thumbnails.rotate(1)
        image_paths.rotate(1)
    for i, thumb in enumerate(three_thumbnails):
        thumb.config(image=thumbnails[i])
    resize_image(imageCanvas)  # Trigger redraw

img = Image.open(image_paths[1])
# === Resize and center image on canvas ===
def resize_image(event=None):
    global tk_img, img_offset, img_size, img
    img = Image.open(image_paths[1])
    if isinstance(event, tk.Event):  # Called from canvas resizing
        canvas = event.widget
    else:
        canvas = imageCanvas  # Manual call

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    img_copy = img.copy()
    img_copy.thumbnail((canvas_width, canvas_height))
    tk_img = ImageTk.PhotoImage(img_copy)

    img_width, img_height = img_copy.size
    x_offset = (canvas_width - img_width) // 2
    y_offset = (canvas_height - img_height) // 2

    img_offset = (x_offset, y_offset)
    img_size = (img_width, img_height)

    canvas.delete("all")
    canvas.create_image(x_offset, y_offset, image=tk_img, anchor="nw")
    canvas.image = tk_img

def on_canvas_click(event):
    global coord_label
    print(f"Canvas clicked at ({event.x}, {event.y})")
    x_click, y_click = event.x, event.y
    x_offset, y_offset = img_offset
    img_width, img_height = img_size

    if x_offset <= x_click <= x_offset + img_width and y_offset <= y_click <= y_offset + img_height: # modify this line to signal out of image click
        x_img = x_click - x_offset
        y_img = y_click - y_offset
        coord_label.config(text=f"Image coordinates: ({x_img}, {y_img})")
    else:
        coord_label.config(text="Click was outside the image.")
# === Bind events ===
imageCanvas.bind("<Configure>", resize_image)
imageCanvas.bind("<Button-1>", on_canvas_click)


# ========== Right upper ==========
# Create the right_top frame
right_top = ttk.Frame(root)  # Use ttk.Frame for themed styling
right_top.grid(row=0, column=1, sticky="nsew")

# Make the right_top frame expand with the window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create the buttons and place them in the grid within right_top
button1 = ttk.Button(right_top, text="Button 1", style='TButton')  # Apply the style
button1.grid(row=0, column=0, sticky="nsew")  # Remove padx, pady from here

button2 = ttk.Button(right_top, text="Button 2", style='TButton')  # Apply the style
button2.grid(row=0, column=1, sticky="nsew")  # Remove padx, pady from here

button3 = ttk.Button(right_top, text="Button 3", style='TButton')  # Apply the style
button3.grid(row=1, column=0, sticky="nsew")  # Remove padx, pady from here

button4 = ttk.Button(right_top, text="Button 4", style='TButton')  # Apply the style
button4.grid(row=1, column=1, sticky="nsew")  # Remove padx, pady from here

# Configure rows and columns of right_top to resize properly
right_top.grid_rowconfigure(0, weight=1)
right_top.grid_rowconfigure(1, weight=1)
right_top.grid_columnconfigure(0, weight=1)
right_top.grid_columnconfigure(1, weight=1)



# ========== Right lower ==========
right_bottom = tk.Frame(root, bg='lightyellow')
right_bottom.grid(row=1, column=1, sticky="nsew")



# ========== Optional: sample widgets ==========
tk.Label(right_bottom, text="Bottom Right").pack(padx=10, pady=10)

root.mainloop()
