from pyautogui import prompt
import json
import pyperclip
import os

os.system(f'git pull')

config_file = r'C:\Users\mulig\Documents\git\meta-repo\repos\espanso-config\config.json'

with open(config_file, 'r') as file:
    data = json.load(file)

word = prompt(text='word', default=pyperclip.paste())

while True:
    t = prompt(text='trigger (shortcut)', default='')
    if t:
        data[t + " "] = word + " "
    else:
        break

# Sort the data by the length of keys (in descending order)
sorted_data = {k: data[k] for k in sorted(data, key=len, reverse=True)}

with open(config_file, 'w') as file:
    json.dump(sorted_data, file, indent=4)


os.system(f'git add . & git commit -m "added {word}" & git push')
