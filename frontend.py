import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from collections import deque
import math
from tkmacosx import Button


# ========== Setup main window ==========
root = tk.Tk()
root.title("Cosmic Composers")
root.geometry("1000x800")  # Optional: set a window size
IMG_WIDTH = 500
IMG_HEIGHT = 500
root.configure(bg='black')
image_paths = ["galaxy1.jpeg", "galaxy.png", "galaxy2.jpeg", "galaxy3.png"]  # Use your real paths
image_paths = deque(image_paths)  # Use deque for easy rotation
animation_running = False
animation_step = 0
animation_id = None
animation_speed = 100  # Milliseconds between frames

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

#setup coordinates label
coord_frame = tk.Frame(left_frame, bg='black')
coord_frame.pack(side="top", fill="x", padx=10, pady=5)
coor_inner = tk.Frame(coord_frame, bg='black')
coor_inner.pack(anchor="center")
# Create a label to display coordinates
coord_label = tk.Label(
    coor_inner,
    text="Select a Spaxel!",
    bg='black',
    fg='white',
    font=('Arial', 30, 'bold'),  # Increased font size and made it bold
    # relief='groove',  # Changed relief style
    # bd=2,
    padx=10,  # Added horizontal padding
    pady=5     # Added vertical padding
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
    if i==2: break #only three thumbnails

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
        thumb.config(image=thumbnails[i]) #update the thumbnail images
    resize_image(imageCanvas)  # update the main image

img = Image.open(image_paths[1]).convert("RGBA")
img = img.resize((IMG_WIDTH, IMG_HEIGHT))
# === Resize and center image on canvas ===
def resize_image(event=None):
    global tk_img, img_offset, img_size, img
    img = Image.open(image_paths[1])
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
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

#get image coordinates on click
def on_canvas_click(event):
    global coord_label
    print(f"Canvas clicked at ({event.x}, {event.y})")
    x_click, y_click = event.x, event.y
    x_offset, y_offset = img_offset
    img_width, img_height = img_size

    if x_offset <= x_click <= x_offset + img_width and y_offset <= y_click <= y_offset + img_height: # modify this line to signal out of image click
        x_img = x_click - x_offset
        y_img = y_click - y_offset
        coord_label.config(text=f"Selected Spaxel: ({x_img}, {y_img})")
    else:
        coord_label.config(text="Click was outside the image.")

# === Bind events ===
imageCanvas.bind("<Configure>", resize_image)
imageCanvas.bind("<Button-1>", on_canvas_click)

# ========== Right upper ==========
# Create the right_top frame
right_top = tk.Frame(root, width=40, bg='black')
right_top.grid(row=0, column=1, sticky="nsew", pady=20, padx=20) 
# Make the right_top frame expand with the window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

play_type = None
# Create the buttons and place them in the grid within right_top
right = Button(right_top, text="Right", height=5, width=8, bg="black", 
               borderless=1, fg="white", command=lambda: draw_cursor(1))  # Apply the style
right.grid(row=0, column=0, sticky="nsew", padx=5, pady=5) 

down = Button(right_top, text="Down", height=5, width=8,  bg="black", borderless=1, fg="white", command=lambda: draw_cursor(0))  # Apply the style
down.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)  

clockwise = Button(right_top,height=5, width=8,  bg="black", borderless=1, fg="white", text="Clockwise",  command=lambda: draw_cursor(2))  # Apply the style
clockwise.grid(row=1, column=0, sticky="nsew", padx=5, pady=5) 

out = Button(right_top,height=5, width=8,  bg="black", borderless=1, fg="white", text="Out",  command=lambda: draw_cursor(3))  # Apply the style
out.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)  

play = Button(right_top, text="Play", bg= "black", fg="white", borderless=1, command=lambda: play_animation(4))  # Apply the style
play.grid(row=2, column=0, columnspan=2, sticky="nsew")  # Span both columns
# Configure rows and columns of right_top to resize properly
right_top.grid_rowconfigure(0, weight=1)
right_top.grid_rowconfigure(1, weight=1)
right_top.grid_columnconfigure(0, weight=1)
right_top.grid_columnconfigure(1, weight=1)


# ========== Animation Functions ==========
def draw_cursor(type, event=None):
    global img, imageCanvas, play_type, animation_step
    resize_image()  # Ensure the image is resized before drawing
    animation_step = 0
    # Get the image dimensions
    width, height = img.size
    draw = ImageDraw.Draw(img)
    play_type = type
    if type == 0:  # Horizontal line
        line_start = (0, 0)
        line_end = (width, 0)
        draw.line([line_start, line_end], fill=(255, 255, 255, 255), width=3)
    elif type == 1:  # Vertical line
        line_start = (0, 0)
        line_end = (0, height)
        draw.line([line_start, line_end], fill=(255, 255, 255, 255), width=3)
    elif type == 2: #clock line
        line_start = (width//2, height//2)
        line_end = (width, height)
        draw.line([line_start, line_end], fill=(255, 255, 255, 255), width=3)
    elif type == 3: #single point in center
        center_x = width // 2
        center_y = height // 2
        radius = 2
        x1 = center_x - radius
        y1 = center_y - radius
        x2 = center_x + radius
        y2 = center_y + radius
        draw.ellipse([(x1, y1), (x2, y2)], outline="white", width=3)
    # Convert the modified PIL image to Tkinter PhotoImage
    tk_img = ImageTk.PhotoImage(img)
    # Update the image on the canvas
    imageCanvas.delete("all")
    canvas_width = imageCanvas.winfo_width()
    canvas_height = imageCanvas.winfo_height()
    img_width, img_height = img.size
    x_offset = (canvas_width - img_width) // 2
    y_offset = (canvas_height - img_height) // 2
    imageCanvas.create_image(x_offset, y_offset, image=tk_img, anchor="nw")
    imageCanvas.image = tk_img  # Keep a reference!

def update_canvas():
    global img, imageCanvas, tk_img
    try:
        tk_img = ImageTk.PhotoImage(img)
        imageCanvas.delete("all")
        canvas_width = imageCanvas.winfo_width()
        canvas_height = imageCanvas.winfo_height()
        img_width, img_height = img.size
        x_offset = (canvas_width - img_width) // 2
        y_offset = (canvas_height - img_height) // 2
        imageCanvas.create_image(x_offset, y_offset, image=tk_img, anchor="nw")
        imageCanvas.image = tk_img
    except Exception as e:
        print(f"Error updating canvas: {e}")

def play_animation(event=None):
    global play_type, animation_running, animation_step, animation_id, img
    if play_type is None or animation_running:
        return

    animation_running = True
    animation_step = 0

    def animate_frame():
        global animation_step, animation_id, animation_running, img, image_paths
        if not animation_running:
            return

        try:
            # Open the original image for each frame
            img = Image.open(image_paths[1]).convert("RGBA")
            img = img.resize((IMG_WIDTH, IMG_HEIGHT))
            width, height = img.size
            draw = ImageDraw.Draw(img)

            if play_type == 0:  # Moving horizontal line
                y_position = (animation_step * 5)  # Move down 
                if y_position > height: 
                    stop_animation()
                    return
                draw.line([(0, y_position), (width, y_position)], fill="white", width=3)
            elif play_type == 1:  # Moving vertical line
                x_position = (animation_step * 5) # Move right 
                if x_position > width:
                    stop_animation()
                    return
                draw.line([(x_position, 0), (x_position, height)], fill="white", width=3)
            elif play_type == 2:  # Rotating clock hand
                center_x, center_y = width // 2, height // 2
                angle = (animation_step * 10) # Rotate 10 degrees per frame
                if angle >360:
                    stop_animation()
                    return
                end_x = int(center_x + (width // 2 - 10) * math.cos(math.radians(angle)))
                end_y = int(center_y + (height // 2 - 10) * math.sin(math.radians(angle)))
                draw.line([(center_x, center_y), (end_x, end_y)], fill="white", width=3)
            elif play_type == 3:  # Pulsating point
                center_x, center_y = width // 2, height // 2
                max_radius = width // 2  # Maximum possible radius to cover the image
                # Make the radius grow and reset
                radius = (animation_step * 10) % (max_radius * 2)
                if radius > max_radius:
                    stop_animation()
                else:
                    current_radius = radius

                # You might want to control the visibility with alpha (transparency)
                alpha = int(255 * (1 - current_radius / max_radius))

                # Draw the expanding/shrinking circle
                draw.ellipse([(center_x - current_radius, center_y - current_radius),
                              (center_x + current_radius, center_y + current_radius)],
                             outline="white")

            update_canvas()
            animation_step += 1
            animation_id = root.after(animation_speed, animate_frame)

        except FileNotFoundError:
            print(f"Error: Image not found during animation.")
            stop_animation()
        except Exception as e:
            print(f"Error during animation frame: {e}")
            stop_animation()

    animate_frame()

def stop_animation():
    global animation_running, animation_id
    animation_running = False
    if animation_id:
        root.after_cancel(animation_id)
        animation_id = None

# ========== Right lower ==========
right_bottom = tk.Frame(root, bg='black')
right_bottom.grid(row=1, column=1, sticky="nsew")



# ========== Optional: sample widgets ==========
tk.Label(right_bottom, text="Spaxel Spectrum", bg="black", fg="white").pack(padx=10, pady=10)

root.mainloop()
