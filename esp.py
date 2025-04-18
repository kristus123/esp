import keyboard
import pyperclip
import json
from time import sleep

from GlobalValue import GlobalValue as G

with open('config.json', 'r') as file:
    shortcuts = json.load(file)


def replace_shortcut(shortcut, replacement, key):

    #print(f"replacing {shortcut} with {replacement}")

    for _ in range(len(shortcut) + 1): # +1 to accompany for the extra space
        sleep(0.05)  # Short delay between backspaces
        keyboard.press_and_release('backspace')
        
    pyperclip.copy(replacement)
    keyboard.press_and_release('ctrl+v')
    
    sleep(0.1)
    if key == " ":
        keyboard.press_and_release("space")
    elif key == ".":
        keyboard.press_and_release(".")

def on_key_event(event):

    if event.event_type == keyboard.KEY_DOWN:
        key = event.name
        

        if key in ["ctrl", "enter", "alt", "tab"]:
            G.reset()
        elif key == "backspace":
            G.typed_keys = G.typed_keys[:-1]
            G.idle_time = 0
        elif len(key) == 1:  # single character
            G.typed_keys += key
            G.idle_time = 0
        elif key == "space":
            G.typed_keys += " "

        if key == "space":
            key = " "
        if key == " " or key == ".":
            #print('checking if' + " '" + G.typed_keys + "' " + 'matches anything')
            for shortcut, replacement in shortcuts.items():
                if G.typed_keys == shortcut + key:
                    #print("Found match")
                    replace_shortcut(shortcut, replacement, key)
                    break
            G.reset()

keyboard.hook(on_key_event)

#print("Text Expander running... Press Ctrl+C to exit.")
try:
    while True:
        G.idle_time += 1
        sleep(1)

        if G.idle_time >= 4:
            print("idle")
            G.typed_keys = ""
            G.idle_time = 0
except:
    print("Exiting...")
finally:
    keyboard.unhook_all()  # Unhooks all keyboard listeners before the program exits.
