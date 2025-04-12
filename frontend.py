import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Cosmic Composers")
root.geometry("800x800")  # Optional: set a window size
root.configure(bg='black')

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
left_frame = tk.Frame(root, bg='lightblue')
left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
image_path = "galaxy.png"
coord_label = tk.Label(
    left_frame,
    text="Click on the image",
    bg='white',
    fg='black',
    font=('Arial', 11),
    relief='solid',
    bd=1
)
coord_label.pack(side="bottom", fill="x", padx=10, pady=5)
imageCanvas = tk.Canvas(left_frame, bg='white')
imageCanvas.pack(fill="both", expand=True)
img = Image.open(image_path)
# === Resize and center image on canvas ===
def resize_image(event):
    global tk_img, img_offset, img_size

    canvas_width = event.width
    canvas_height = event.height

    img_copy = img.copy()
    img_copy.thumbnail((canvas_width, canvas_height))  # Maintain aspect ratio
    tk_img = ImageTk.PhotoImage(img_copy)

    img_width, img_height = img_copy.size
    x_offset = (canvas_width - img_width) // 2
    y_offset = (canvas_height - img_height) // 2

    img_offset = (x_offset, y_offset)
    img_size = (img_width, img_height)

    imageCanvas.delete("all")
    imageCanvas.create_image(x_offset, y_offset, image=tk_img, anchor="nw")
    imageCanvas.image = tk_img

def on_canvas_click(event):
    global coord_label
    print('clicked')
    print(f"Canvas clicked at ({event.x}, {event.y})")
    x_click, y_click = event.x, event.y
    x_offset, y_offset = img_offset
    img_width, img_height = img_size

    if x_offset <= x_click <= x_offset + img_width and y_offset <= y_click <= y_offset + img_height:
        x_img = x_click - x_offset
        y_img = y_click - y_offset
        coord_label.config(text=f"Image coordinates: ({x_img}, {y_img})")
    else:
        coord_label.config(text="Click was outside the image.")
# === Bind resize event ===
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
