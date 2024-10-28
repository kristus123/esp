import tkinter as tk
import keyboard
from ctypes import windll

# Example apps dictionary with abbreviations
apps = {
    "Calculator": {
        "abbreviations": ["cl", "ca"],
        "action": lambda: print("Opening Calculator...")
    },
    "Text Editor": {
        "abbreviations": ["te", "txt"],
        "action": lambda: print("Opening Text Editor...")
    },
    "Browser": {
        "abbreviations": ["br", "bw"],
        "action": lambda: print("Opening Browser...")
    },
    "Terminal": {
        "abbreviations": ["trm", "term"],
        "action": lambda: print("Opening Terminal...")
    },
    "Music Player": {
        "abbreviations": ["mp", "music"],
        "action": lambda: print("Opening Music Player...")
    },
}

# Flag to keep track of window visibility
is_visible = False

# Currently selected button (for highlighting)
current_selected_button = None

# Function to center the window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to make the window click-through
def make_click_through(window_id):
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x00080000
    WS_EX_TRANSPARENT = 0x00000020

    # Get the window handle (HWND)
    hwnd = windll.user32.GetParent(window_id)

    # Get the current window style
    styles = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)

    # Add WS_EX_LAYERED and WS_EX_TRANSPARENT to the current style
    windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, styles | WS_EX_LAYERED | WS_EX_TRANSPARENT)

# Function to restore interactivity (disable click-through)
def disable_click_through(window_id):
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x00080000

    # Get the window handle (HWND)
    hwnd = windll.user32.GetParent(window_id)

    # Get the current window style
    styles = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)

    # Remove WS_EX_TRANSPARENT to make the window interactive
    windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, styles | WS_EX_LAYERED)

# Function to handle search action (updates list as user types)
def search_apps(event=None):
    search_term = search_entry.get().lower()
    print(f"Searching for apps: {search_term}")
    update_app_list(search_term)

# Function to show or hide the overlay (Alt+Z toggle)
def toggle_overlay():
    global is_visible
    if is_visible:
        hide_overlay()
    else:
        show_overlay()

# Function to show the overlay
def show_overlay():
    global is_visible
    root.deiconify()  # Show the overlay window
    root.attributes("-topmost", True)  # Ensure it's always on top
    disable_click_through(root.winfo_id())  # Make it interactive
    search_entry.delete(0, tk.END)  # Clear any previous input
    search_entry.focus_force()  # Force focus on the search entry
    update_app_list("")  # Show all apps initially
    is_visible = True

# Function to hide the overlay
def hide_overlay():
    global is_visible
    root.withdraw()  # Hide the window
    make_click_through(root.winfo_id())  # Restore click-through for next time
    is_visible = False

# Function to trigger app logic when an app is selected
def run_app(app_name):
    if app_name in apps:
        apps[app_name]["action"]()  # Call the app action function
    hide_overlay()  # Hide the overlay after app launch

# Function to update the list of apps based on search input
def update_app_list(search_term):
    # Clear the current list
    for widget in app_frame.winfo_children():
        widget.destroy()

    # Filter and display matching apps
    filtered_apps = []
    for app_name, app_data in apps.items():
        # Check if the search term matches the full name or any abbreviation
        if search_term in app_name.lower() or any(abbr in search_term for abbr in app_data["abbreviations"]):
            filtered_apps.append(app_name)

    # Create app buttons and enable tab navigation
    last_button = None
    global app_buttons
    global current_selected_button
    app_buttons = []  # List to keep track of app buttons
    current_selected_button = None  # Reset current selected button
    for app_name in filtered_apps:
        app_button = tk.Button(
            app_frame, 
            text=app_name, 
            font=("Arial", 14), 
            command=lambda a=app_name: run_app(a),
            bg="#333333",  # Dark background color
            fg="#FFFFFF",  # Light text color
            relief="flat",  # Flat button, can also use 'groove' or 'raised'
            bd=0,  # Remove border
            padx=10,
            pady=5,
            highlightthickness=0,  # Remove highlight when clicked
            activebackground="#555555",  # Darker when clicked
            activeforeground="#FFFFFF"  # Keep text white when clicked
        )
        app_button.pack(fill=tk.X, pady=2, padx=10)
        
        # Add to the app_buttons list
        app_buttons.append(app_button)

        if last_button:
            last_button.bind("<Tab>", lambda e, btn=app_button: highlight_button(btn))
        
        # Bind Enter key to select the focused app
        app_button.bind("<Return>", lambda e, a=app_name: run_app(a))

        last_button = app_button

    # Ensure tabbing wraps around
    if last_button:
        last_button.bind("<Tab>", lambda e: highlight_button(search_entry))

    # Highlight the first button by default
    if app_buttons:
        highlight_button(app_buttons[0])

# Function to select the top app when Enter is pressed
def select_top_app(event=None):
    if app_buttons:  # If there are any apps in the list
        # Trigger the action of the top app (first one in the list)
        app_buttons[0].invoke()  # Simulate a click on the first app
    else:
        print("No apps found for the given search term.")

# Function to highlight the currently selected button
def highlight_button(button):
    global current_selected_button
    # Reset background of the previously selected button
    if current_selected_button:
        current_selected_button.config(bg="#333333")  # Reset to default color

    # Set new button's background to highlighted color
    button.config(bg="#555555")  # Highlighted color
    current_selected_button = button

# Set up global hotkey binding for Alt + Z (toggle)
keyboard.add_hotkey('alt+z', toggle_overlay)

# Create the main window
root = tk.Tk()

# Hide the window initially
root.withdraw()

# Make the window borderless and set transparency
root.overrideredirect(True)
root.attributes("-alpha", 0.9)  # Set transparency (0.9 is semi-transparent)

# Set window size and position it in the center
window_width = 400
window_height = 300
center_window(root, window_width, window_height)

# Add a search bar (text field) at the top
search_entry = tk.Entry(
    root, 
    font=("Arial", 14),
    bg="#222222",  # Dark background color for the entry field
    fg="#FFFFFF",   # Light text color
    bd=0,           # Remove border
    relief="flat",   # Flat relief to match button style
    highlightthickness=0  # Remove highlight when clicked
)
search_entry.pack(pady=10, padx=10, fill=tk.X)

# Bind KeyRelease event to trigger search as the user types
search_entry.bind("<KeyRelease>", search_apps)

# Bind Enter key to select the top app
search_entry.bind("<Return>", select_top_app)

# Add a frame to hold the list of apps
app_frame = tk.Frame(root)
app_frame.pack(fill=tk.BOTH, expand=True)

# Bind "Escape" key to hide the window
root.bind('<Escape>', lambda e: hide_overlay())

# Start the main loop
root.mainloop()