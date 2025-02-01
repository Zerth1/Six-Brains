from enum import Enum, auto
from typing import *
from pyray import *
import os
import json
import math
import random
import user_interface
RESOLUTION_X = 1450
RESOLUTION_Y = 800
SETTINGS = {
    "EnabledCharacterEncodings": {
        "A": False, "B": False, "C": False, "D": False, "E": False, "F": False, "G": False,
        "H": False, "I": False, "J": False, "K": False, "L": False, "M": False, "N": False,
        "O": False, "P": False, "Q": False, "R": False, "S": False, "T": False, "U": False,
        "V": False, "W": False, "X": False, "Y": False, "Z": False,
        "a": False, "b": False, "c": False, "d": False, "e": False, "f": False, "g": False,
        "h": False, "i": False, "j": False, "k": False, "l": False, "m": False, "n": False,
        "o": False, "p": False, "q": False, "r": False, "s": False, "t": False, "u": False,
        "v": False, "w": False, "x": False, "y": False, "z": False,
        "0": True, "1": True, "2": True, "3": True, "4": True, "5": True, "6": True,
        "7": True, "8": True, "9": True
    },
    "Grapheme-Color": {
        "Active": True,
        "N": 2,
    },
    "Chromesthesia": {
        "Active": False,
        "N": 2,
    },
    "TimerDuration": 3,
}
character_color_encodings = {
    "0": Color(0, 0, 255, 255),  # Blue
    "1": Color(255, 0, 0, 255),  # Red
    "2": Color(0, 255, 0, 255),  # Green
    "3": Color(255, 165, 0, 255),  # Orange
    "4": Color(255, 255, 0, 255),  # Yellow
    "5": Color(255, 20, 147, 255),  # Deep Pink
    "6": Color(138, 43, 226, 255),  # Blue Violet
    "7": Color(255, 99, 71, 255),  # Tomato
    "8": Color(255, 255, 255, 255),  # White
    "9": Color(0, 255, 255, 255),  # Cyan

    "A": Color(255, 0, 0, 255),  # Red
    "B": Color(0, 0, 255, 255),  # Blue
    "C": Color(0, 255, 0, 255),  # Green
    "D": Color(255, 255, 0, 255),  # Yellow
    "E": Color(255, 165, 0, 255),  # Orange
    "F": Color(128, 0, 128, 255),  # Purple
    "G": Color(255, 0, 255, 255),  # Magenta
    "H": Color(255, 255, 255, 255),  # White
    "I": Color(0, 0, 0, 255),  # Black
    "J": Color(255, 182, 193, 255),  # Light Pink
    "K": Color(0, 128, 0, 255),  # Dark Green
    "L": Color(255, 69, 0, 255),  # Red-Orange
    "M": Color(139, 69, 19, 255),  # Brown
    "N": Color(0, 255, 255, 255),  # Cyan
    "O": Color(255, 255, 255, 255),  # White
    "P": Color(255, 105, 180, 255),  # Hot Pink
    "Q": Color(128, 128, 0, 255),  # Olive Green
    "R": Color(255, 0, 0, 255),  # Red
    "S": Color(255, 215, 0, 255),  # Gold
    "T": Color(0, 255, 127, 255),  # Spring Green
    "U": Color(0, 255, 255, 255),  # Cyan
    "V": Color(75, 0, 130, 255),  # Indigo
    "W": Color(255, 215, 180, 255),  # Peach
    "X": Color(255, 255, 255, 255),  # White
    "Y": Color(255, 255, 0, 255),  # Yellow
    "Z": Color(0, 0, 128, 255),  # Navy Blue
    "a": Color(255, 182, 193, 255),  # Light Pink
    "b": Color(173, 216, 230, 255),  # Light Blue
    "c": Color(144, 238, 144, 255),  # Light Green
    "d": Color(255, 250, 205, 255),  # Lemon Chiffon
    "e": Color(255, 240, 145, 255),  # Pale Yellow
    "f": Color(221, 160, 221, 255),  # Lavender
    "g": Color(255, 182, 193, 255),  # Light Pink
    "h": Color(245, 245, 245, 255),  # Light Gray
    "i": Color(255, 255, 255, 255),  # White
    "j": Color(255, 160, 122, 255),  # Coral
    "k": Color(34, 139, 34, 255),  # Forest Green
    "l": Color(255, 69, 0, 255),  # Red-Orange
    "m": Color(210, 180, 140, 255),  # Tan
    "n": Color(0, 206, 209, 255),  # Dark Turquoise
    "o": Color(255, 228, 225, 255),  # Misty Rose
    "p": Color(255, 105, 180, 255),  # Hot Pink
    "q": Color(255, 69, 255, 255),  # Fuchsia
    "r": Color(255, 99, 71, 255),  # Tomato Red
    "s": Color(255, 222, 173, 255),  # Peach Puff
    "t": Color(50, 205, 50, 255),  # Lime Green
    "u": Color(173, 216, 230, 255),  # Light Sky Blue
    "v": Color(138, 43, 226, 255),  # Blue Violet
    "w": Color(253, 245, 230, 255),  # Linen
    "x": Color(128, 128, 128, 255),  # Gray
    "y": Color(253, 253, 150, 255),  # Light Yellow
    "z": Color(72, 61, 139, 255),  # Dark Slate Blue
}
character_color_keys = list(character_color_encodings.keys())
character_color_keys.sort()
init_window(RESOLUTION_X, RESOLUTION_Y, "Six-Brains")
set_target_fps(get_monitor_refresh_rate(get_current_monitor()))
if os.path.getsize("settings_data.json") == 0:
    with open("settings_data.json", "w") as settings_file:
        settings_file.write(json.dumps(SETTINGS, indent=4))
with open("settings_data.json", "r") as file:
    settings_data = json.load(file)
game_image = load_image("game_screen.png")
settings_image = load_image("settings.jpeg")
game_texture = load_texture_from_image(game_image)
settings_texture = load_texture_from_image(settings_image)
unload_image(game_image)
unload_image(settings_image)

door_right = load_image("door_right.png")
door_left = load_image("door_left.png")
door_right_texture = load_texture_from_image(door_right)
door_left_texture = load_texture_from_image(door_left)
unload_image(door_right)
unload_image(door_left)
in_transition = False
delta_time = 0.0
def transition_room():
    global in_transition
    global delta_time
    delta_time += get_frame_time()
    if delta_time > 0.5:
        in_transition = False
        delta_time = 0.0
    else:
        draw_texture(door_left_texture, int(0 - ((RESOLUTION_X / 2) * min((delta_time * 2), 1.0))), 0, GRAY)
        draw_texture(door_right_texture, int((RESOLUTION_X / 2) + ((RESOLUTION_X / 2) * min((delta_time * 2), 1.0))), 0, GRAY)
deep_settings = False
is_settings = False
settings_buttons = {}
settings_buttons["grapheme_active"] = user_interface.Button("Active:", 25, Rectangle(50 + measure_text("Active:", 25) + 10, 75, 25, 25))
settings_buttons["grapheme_active"]._on = settings_data["Grapheme-Color"]["Active"]
settings_buttons["grapheme_n"] = user_interface.InputButton("N:", 25, Rectangle(50 + measure_text("N:", 25) + 10, 125, measure_text("00", 25), 25))
settings_buttons["grapheme_n"].text = str(settings_data["Grapheme-Color"]["N"])
settings_buttons["chromo_active"] = user_interface.Button("Active:", 25, Rectangle(50 + measure_text("Active:", 25) + 10, 75, 25, 25))
settings_buttons["chromo_active"]._on = settings_data["Chromesthesia"]["Active"]
settings_buttons["chromo_n"] = user_interface.InputButton("N:", 25, Rectangle(50 + measure_text("N:", 25) + 10, 125, measure_text("00", 25), 25))
settings_buttons["chromo_n"].text = str(settings_data["Chromesthesia"]["N"])

settings_buttons["timer_duration"] = user_interface.InputButton("Timer Duration:", 25, Rectangle(50 + measure_text("Timer Duration:", 25) + 10, 280, measure_text("000", 25), 25))
settings_buttons["timer_duration"].text = str(settings_data["TimerDuration"])
def redirect_settings():
    global deep_settings
    draw_text("Grapheme-Color Mode", 50, 80, 25, WHITE)
    draw_text("Chromesthesia Mode", 50, 130, 25, WHITE)
    if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
        current_position = get_mouse_position()
        if check_collision_point_rec(current_position, Rectangle(50, 80, measure_text("Grapheme-Color Mode", 25), 25)):
            deep_settings = True
            settings_buttons["grapheme_active"].toggle()
            settings_buttons["grapheme_n"].toggle()
        elif check_collision_point_rec(current_position, Rectangle(50, 130, measure_text("Chromesthesia Mode", 25), 25)):
            deep_settings = True
            settings_buttons["chromo_active"].toggle()
            settings_buttons["chromo_n"].toggle()
is_generating = False
is_playing = False
looking_at_encodings = False
chosen_gamemode = ""
blacklist_toggle = []

grapheme_objects = []
symbol_objects = []
trial_match = []
match_color = WHITE
def reset_game():
    global grapheme_objects
    global trial_match
    global symbol_objects
    global current_trial
    global is_playing
    global match_color
    grapheme_objects = []
    trial_match = []
    symbol_objects = []
    current_trial = 1
    is_playing = False
    match_color = WHITE
trial_clock = 0
current_trial = 1
trials = 0
valid_key_copies = []
while not window_should_close():
    begin_drawing()
    clear_background(BLACK)
    if is_generating:
        gamemode_options = []
        if settings_data["Grapheme-Color"]["Active"]:
            gamemode_options.append("Grapheme-Color")
        if settings_data["Chromesthesia"]["Active"]:
            gamemode_options.append("Chromesthesia")
        chosen_gamemode = random.choice(gamemode_options)
        is_generating = False
        if chosen_gamemode == "Grapheme-Color":
            trials = max(20, settings_data[chosen_gamemode]["N"] * 10)
            valid_key_copies = character_color_keys.copy()
            for key in valid_key_copies.copy():
                if not settings_data["EnabledCharacterEncodings"][key]:
                    valid_key_copies.remove(key)
            for i in range(trials):
                if i < settings_data[chosen_gamemode]["N"]:
                    grapheme_objects.append(random.choice(valid_key_copies))
                else:                
                    if random.random() < 0.4:
                        trial_match.append(True)
                        symbol_objects.append(grapheme_objects[i - settings_data["Grapheme-Color"]["N"]])
                    else:
                        trial_match.append(False)
                        key_copies = valid_key_copies.copy()
                        key_copies.remove(grapheme_objects[i - settings_data["Grapheme-Color"]["N"]])
                        symbol_objects.append(random.choice(key_copies))
                    grapheme_objects.append(random.choice(valid_key_copies))
            print(trial_match)
        elif chosen_gamemode == "Chromesthesia":
            trials = max(20, settings_data[chosen_gamemode]["N"] * 10)
        trial_clock = get_time() + settings_data["TimerDuration"]
    if is_settings:
        draw_texture(settings_texture, 0, 0, GRAY)
        if deep_settings:
            if settings_buttons["timer_duration"]._enabled:
                settings_buttons["timer_duration"].toggle() 
        else:
            time_elapsed_since_generation = 0
            if not settings_buttons["timer_duration"]._enabled:
                settings_buttons["timer_duration"].toggle()
            redirect_settings()
    else:
        if looking_at_encodings:
            reset_game()
            x_offset_index = -1
            current_position = get_mouse_position()
            for i, encoding in enumerate(character_color_keys):
                if i % 10 == 0:
                    x_offset_index += 1
                draw_text(encoding + ":", 100 + (x_offset_index * 200), 50 + ((i % 10) * 50), 25, WHITE)
                draw_rectangle(100 + (x_offset_index * 200) + 25, 50 + ((i % 10) * 50), 25, 25, character_color_encodings[encoding])
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT): 
                    if check_collision_point_rec(current_position, Rectangle(100 + (x_offset_index * 200) + 100, 50 + ((i % 10) * 50), 25, 25)):
                        settings_data["EnabledCharacterEncodings"][encoding] = not settings_data["EnabledCharacterEncodings"][encoding]
                if settings_data["EnabledCharacterEncodings"][encoding]:
                    draw_rectangle(100 + (x_offset_index * 200) + 100, 50 + ((i % 10) * 50), 25, 25, GREEN)
                else:
                    draw_rectangle(100 + (x_offset_index * 200) + 100, 50 + ((i % 10) * 50), 25, 25, RED)
        else:
            if settings_buttons["timer_duration"]._enabled:
                settings_buttons["timer_duration"].toggle()
            draw_texture(game_texture, 0, 0, Color(255, 255, 255, 60))
            draw_text("[S] Settings", 50, 30, 25, WHITE)
            draw_text("[E] Encodings", RESOLUTION_X - 50 - measure_text("[E] Encodings", 25), 30, 25, WHITE)
            draw_text("[Space] Start/Stop", int((RESOLUTION_X / 2) - measure_text("[Space] Start/Stop", 50) / 2), int(0.875 * RESOLUTION_Y), 50, WHITE)
            if is_playing:
                if chosen_gamemode == "Grapheme-Color":
                    key_copies = valid_key_copies.copy()
                    draw_rectangle(int(RESOLUTION_X / 2) - int(RESOLUTION_Y / 4), int(RESOLUTION_Y / 4), int(RESOLUTION_Y / 2), int(RESOLUTION_Y / 2), character_color_encodings[grapheme_objects[current_trial - 1]])
                    draw_text("Trial: " + str(current_trial) + " / " + str(trials), int(RESOLUTION_X / 2) - int(RESOLUTION_Y / 4), int(RESOLUTION_Y / 4) - 75, 50, WHITE)
                    if current_trial > settings_data["Grapheme-Color"]["N"]:
                        if is_key_pressed(KeyboardKey.KEY_A):
                            if trial_match[current_trial - settings_data["Grapheme-Color"]["N"] - 1]:
                                match_color = GREEN
                            else:
                                match_color = RED
                        draw_text(symbol_objects[current_trial - settings_data["Grapheme-Color"]["N"] - 1], int(RESOLUTION_X / 2) + int(RESOLUTION_Y / 4) + 100, int(RESOLUTION_Y / 2), 100, RED)
                        draw_text("[A] Match", int(RESOLUTION_X / 2) + int(RESOLUTION_Y / 4) + 100, int(RESOLUTION_Y / 2) + 100, 50, match_color)
                    if get_time() > trial_clock:
                        trial_clock += settings_data["TimerDuration"]
                        current_trial += 1
                        match_color = WHITE
                        if current_trial == trials:
                            reset_game()
                elif chosen_gamemode == "Chromesthesia":
                    pass
            if is_key_pressed(KeyboardKey.KEY_SPACE):
                if not is_playing:
                    is_generating = True
                    reset_game()
                is_playing = not is_playing
        if is_key_pressed(KeyboardKey.KEY_E):
            looking_at_encodings = not looking_at_encodings
    if not looking_at_encodings and is_key_pressed(KeyboardKey.KEY_S):
        reset_game()
        in_transition = True
        if deep_settings:
            deep_settings = False
            for key, settings_object in settings_buttons.items():
                if settings_object._enabled:
                    blacklist_toggle.append(key)    
                    settings_object.toggle()
                else:
                    if key in blacklist_toggle:
                        blacklist_toggle.remove(key)
        else:
            is_settings = not is_settings      
        settings_data["Grapheme-Color"]["Active"] = settings_buttons["grapheme_active"]._on
        settings_data["Chromesthesia"]["Active"] = settings_buttons["chromo_active"]._on
        settings_data["Grapheme-Color"]["N"] = max(int(settings_buttons["grapheme_n"].text), 1)
        settings_data["Chromesthesia"]["N"] = max(int(settings_buttons["chromo_n"].text), 1)
        settings_data["TimerDuration"] = int(settings_buttons["timer_duration"].text)
        with open("settings_data.json", "w") as file:
            json.dump(settings_data, file)
    for settings_object in settings_buttons.values():
        settings_object.update()
    if in_transition:
        transition_room()
    end_drawing()
close_window()