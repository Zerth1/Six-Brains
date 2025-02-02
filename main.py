from enum import Enum, auto
from typing import *
from pyray import *
from music21 import *
import os
import json
import math
import random
import threading
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
    "EnabledSoundEncodings": {},
    "TimerDuration": 3,
}
def map_ranges(a: float, b: float, c: float, d: float, v: float):
    return c + (((v - a) / (b - a)) * (d - c))
def play_midi_in_thread(stream_obj):
    sp = midi.realtime.StreamPlayer(stream_obj)
    sp.play()
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
note_frequencies = {
    "C0": 16.35, "C#0": 17.32, "D0": 18.35, "D#0": 19.45, "E0": 20.60, "F0": 21.83, "F#0": 23.12, "G0": 24.50, "G#0": 25.96, "A0": 27.50, "A#0": 29.14, "B0": 30.87,
    "C1": 32.70, "C#1": 34.65, "D1": 36.71, "D#1": 38.89, "E1": 41.20, "F1": 43.65, "F#1": 46.25, "G1": 49.00, "G#1": 51.91, "A1": 55.00, "A#1": 58.27, "B1": 61.74,
    "C2": 65.41, "C#2": 69.30, "D2": 73.42, "D#2": 77.78, "E2": 82.41, "F2": 87.31, "F#2": 92.50, "G2": 98.00, "G#2": 103.83, "A2": 110.00, "A#2": 116.54, "B2": 123.47,
    "C3": 130.81, "C#3": 138.59, "D3": 146.83, "D#3": 155.56, "E3": 164.81, "F3": 174.61, "F#3": 185.00, "G3": 196.00, "G#3": 207.65, "A3": 220.00, "A#3": 233.08, "B3": 246.94,
    "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13, "E4": 329.63, "F4": 349.23, "F#4": 369.99, "G4": 392.00, "G#4": 415.30, "A4": 440.00, "A#4": 466.16, "B4": 493.88,
    "C5": 523.25, "C#5": 554.37, "D5": 587.33, "D#5": 622.25, "E5": 659.26, "F5": 698.46, "F#5": 739.99, "G5": 783.99, "G#5": 830.61, "A5": 880.00, "A#5": 932.33, "B5": 987.77,
    "C6": 1046.50, "C#6": 1108.73, "D6": 1174.66, "D#6": 1244.51, "E6": 1318.51, "F6": 1396.91, "F#6": 1479.98, "G6": 1567.98, "G#6": 1661.22, "A6": 1760.00, "A#6": 1864.66, "B6": 1975.53,
    "C7": 2093.00, "C#7": 2217.46, "D7": 2349.32, "D#7": 2489.02, "E7": 2637.02, "F7": 2793.83, "F#7": 2959.96, "G7": 3135.96, "G#7": 3322.44, "A7": 3520.00, "A#7": 3729.31, "B7": 3951.07,
    "C8": 4186.01
}
note_ranges = {
    'C0': (16.35, 17.32),
    'C#0': (17.32, 18.35),
    'D0': (18.35, 19.45),
    'D#0': (19.45, 20.6),
    'E0': (20.6, 21.83),
    'F0': (21.83, 23.12),
    'F#0': (23.12, 24.5),
    'G0': (24.5, 25.96),
    'G#0': (25.96, 27.5),
    'A0': (27.5, 29.14),
    'A#0': (29.14, 30.87),
    'B0': (30.87, 32.7),
    'C1': (32.7, 34.65),
    'C#1': (34.65, 36.71),
    'D1': (36.71, 38.89),
    'D#1': (38.89, 41.2),
    'E1': (41.2, 43.65),
    'F1': (43.65, 46.25),
    'F#1': (46.25, 49.0),
    'G1': (49.0, 51.91),
    'G#1': (51.91, 55.0),
    'A1': (55.0, 58.27),
    'A#1': (58.27, 61.74),
    'B1': (61.74, 65.41),
    'C2': (65.41, 69.3),
    'C#2': (69.3, 73.42),
    'D2': (73.42, 77.78),
    'D#2': (77.78, 82.41),
    'E2': (82.41, 87.31),
    'F2': (87.31, 92.5),
    'F#2': (92.5, 98.0),
    'G2': (98.0, 103.83),
    'G#2': (103.83, 110.0),
    'A2': (110.0, 116.54),
    'A#2': (116.54, 123.47),
    'B2': (123.47, 130.81),
    'C3': (130.81, 138.59),
    'C#3': (138.59, 146.83),
    'D3': (146.83, 155.56),
    'D#3': (155.56, 164.81),
    'E3': (164.81, 174.61),
    'F3': (174.61, 185.0),
    'F#3': (185.0, 196.0),
    'G3': (196.0, 207.65),
    'G#3': (207.65, 220.0),
    'A3': (220.0, 233.08),
    'A#3': (233.08, 246.94),
    'B3': (246.94, 261.63),
    'C4': (261.63, 277.18),
    'C#4': (277.18, 293.66),
    'D4': (293.66, 311.13),
    'D#4': (311.13, 329.63),
    'E4': (329.63, 349.23),
    'F4': (349.23, 369.99),
    'F#4': (369.99, 392.0),
    'G4': (392.0, 415.3),
    'G#4': (415.3, 440.0),
    'A4': (440.0, 466.16),
    'A#4': (466.16, 493.88),
    'B4': (493.88, 523.25),
    'C5': (523.25, 554.37),
    'C#5': (554.37, 587.33),
    'D5': (587.33, 622.25),
    'D#5': (622.25, 659.25),
    'E5': (659.25, 698.46),
    'F5': (698.46, 739.99),
    'F#5': (739.99, 783.99),
    'G5': (783.99, 830.61),
    'G#5': (830.61, 880.0),
    'A5': (880.0, 932.33),
    'A#5': (932.33, 987.77),
    'B5': (987.77, 1046.5),
    'C6': (1046.5, 1108.73),
    'C#6': (1108.73, 1174.66),
    'D6': (1174.66, 1244.51),
    'D#6': (1244.51, 1318.51),
    'E6': (1318.51, 1396.91),
    'F6': (1396.91, 1479.98),
    'F#6': (1479.98, 1567.98),
    'G6': (1567.98, 1661.22),
    'G#6': (1661.22, 1760.0),
    'A6': (1760.0, 1864.66),
    'A#6': (1864.66, 1975.53),
    'B6': (1975.53, 2093.0),
    'C7': (2093.0, 2217.46),
    'C#7': (2217.46, 2349.32),
    'D7': (2349.32, 2489.02),
    'D#7': (2489.02, 2637.02),
    'E7': (2637.02, 2793.83),
    'F7': (2793.83, 2959.96),
    'F#7': (2959.96, 3135.96),
    'G7': (3135.96, 3322.44),
    'G#7': (3322.44, 3520.0),
    'A7': (3520.0, 3729.31),
    'A#7': (3729.31, 3951.07),
    'B7': (3951.07, 4186.01),
    'C8': (4186.01, 4434.92)
}
chromatic_scale_sharps = ["C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C"]
pitches = []
for octave in range(8):
    if octave == 0 or octave == 7:
        continue
    for note_x in chromatic_scale_sharps:
        pitches.append(note_x + str(octave))
pitch_map = {}
pitch_i = 0
for note_x in pitches:
    pitch_map[note_x] = pitch.Pitch(note_x)
    if pitch_i < 3:
        SETTINGS["EnabledSoundEncodings"][note_x] = True
    else:
        SETTINGS["EnabledSoundEncodings"][note_x] = False
    pitch_i += 1
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
deep_encodings = False
viewing_grapheme_encodings = False
viewing_chromo_encodings = False
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
looking_at_chromo_wheel = False
chosen_gamemode = ""
blacklist_toggle = []

grapheme_objects = []
chromo_objects = []
symbol_objects = []
sound_objects = []
trial_match = []
match_color = WHITE
played_sound = False
def reset_game():
    global grapheme_objects
    global chromo_objects
    global trial_match
    global symbol_objects
    global sound_objects
    global current_trial
    global is_playing
    global match_color
    global played_sound
    grapheme_objects = []
    chromo_objects = []
    trial_match = []
    symbol_objects = []
    sound_objects = []
    current_trial = 1
    is_playing = False
    match_color = WHITE
    played_sound = False
trial_clock = 0
current_trial = 1
trials = 0
valid_key_copies = []
chromo_wheel_divisions = 12
radial_divisions = 7

distance = 0.0
frequency = 0.0
theta = 0.0
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
        elif chosen_gamemode == "Chromesthesia":
            trials = max(20, settings_data[chosen_gamemode]["N"] * 10)
            valid_key_copies = pitches.copy()
            for key in valid_key_copies.copy():
                if not settings_data["EnabledSoundEncodings"][key]:
                    valid_key_copies.remove(key)
            for i in range(trials):
                if i < settings_data[chosen_gamemode]["N"]:
                    chromo_objects.append(random.choice(valid_key_copies))
                else:                
                    if random.random() < 0.4:
                        trial_match.append(True)
                        sound_objects.append(chromo_objects[i - settings_data["Chromesthesia"]["N"]])
                    else:
                        trial_match.append(False)
                        key_copies = valid_key_copies.copy()
                        key_copies.remove(chromo_objects[i - settings_data["Chromesthesia"]["N"]])
                        sound_objects.append(random.choice(key_copies))
                    chromo_objects.append(random.choice(valid_key_copies))               
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
            if deep_encodings:
                current_position = get_mouse_position()
                if viewing_grapheme_encodings:
                    x_offset_index = -1
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
                    x_offset_index = -1
                    for i, encoding in enumerate(pitches):
                        if i % 20 == 0:
                            x_offset_index += 1
                        draw_text(encoding + ":", 100 + (x_offset_index * 200), 50 + ((i % 20) * 25), 12, WHITE)
                        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT): 
                            if check_collision_point_rec(current_position, Rectangle(100 + (x_offset_index * 200) + 25 + measure_text(encoding + ":", 25), 50 + ((i % 20) * 25), 12, 12)):
                                settings_data["EnabledSoundEncodings"][encoding] = not settings_data["EnabledSoundEncodings"][encoding]
                        if settings_data["EnabledSoundEncodings"][encoding]:
                            draw_rectangle(100 + (x_offset_index * 200) + 25 + measure_text(encoding + ":", 25), 50 + ((i % 20) * 25), 12, 12, GREEN)
                        else:
                            draw_rectangle(100 + (x_offset_index * 200) + 25 + measure_text(encoding + ":", 25), 50 + ((i % 20) * 25), 12, 12, RED)
                    pass    
            else:
                draw_text("Grapheme-Color", 50, 30, 25, WHITE)
                draw_text("Chromesthesia", 50, 80, 25, WHITE)
                current_position = get_mouse_position()
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    if check_collision_point_rec(current_position, Rectangle(50, 30, measure_text("Grapheme-Color", 25), 25)):
                        deep_encodings = True
                        viewing_grapheme_encodings = True
                    elif check_collision_point_rec(current_position, Rectangle(50, 80, measure_text("Chromesthesia", 25), 25)):
                        deep_encodings = True
                        viewing_chromo_encodings = True
        elif looking_at_chromo_wheel:
            reset_game()
            old_angle = 0
            for i in range(chromo_wheel_divisions):
                for j in range(radial_divisions):
                    middle_angle = old_angle + ((360 / chromo_wheel_divisions) / 2)
                    draw_circle_sector(Vector2(int(RESOLUTION_X / 2), int(RESOLUTION_Y / 2)), (radial_divisions - j) * (300 / radial_divisions), old_angle, middle_angle + ((360 / chromo_wheel_divisions) / 2), 50, color_from_hsv(middle_angle, 1.0, map_ranges(32.70, 4186.01, 0.0, 1.0, 32.70 + ((radial_divisions - j) / radial_divisions) * (4186.01 - 32.70))))
                old_angle += (360 / chromo_wheel_divisions)
            old_angle = 0
            for i in range(chromo_wheel_divisions):
                draw_circle_sector_lines(Vector2(int(RESOLUTION_X / 2), int(RESOLUTION_Y / 2)), 300, old_angle, old_angle + (360 / chromo_wheel_divisions), 50, WHITE)
                old_angle += (360 / chromo_wheel_divisions)
            for i in range(radial_divisions):
                draw_circle_lines(int(RESOLUTION_X / 2), int(RESOLUTION_Y / 2), (radial_divisions - i) * (300 / radial_divisions), WHITE)
            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                current_position = get_mouse_position()
                if check_collision_point_circle(current_position, Vector2(int(RESOLUTION_X / 2), int(RESOLUTION_Y / 2)), 300):
                    distance = vector2_distance(current_position, Vector2(int(RESOLUTION_X / 2), int(RESOLUTION_Y / 2)))
                    clicked_radial = int(math.ceil((distance / 300) * radial_divisions))
                    theta = math.degrees(vector2_angle(vector2_subtract(current_position, Vector2(int(RESOLUTION_X / 2), int(RESOLUTION_Y / 2))), Vector2(1, 0)) % (2 * math.pi))
                    frequency = map_ranges(0.0, 1.0, note_ranges[chromatic_scale_sharps[::-1][int(theta / (360 / len(chromatic_scale_sharps)))] + str(clicked_radial)][0], note_ranges[chromatic_scale_sharps[::-1][int(theta / (360 / len(chromatic_scale_sharps)))] + str(clicked_radial)][1], ((((clicked_radial) / radial_divisions) * 300) - distance) / ((1 / radial_divisions) * 300))
                    clicked_note = note.Note(chromatic_scale_sharps[::-1][int(theta / (360 / len(chromatic_scale_sharps)))] + str(clicked_radial), quarterLength=1.0) 
                    clicked_note.pitch.frequency = frequency
                    new_stream = stream.Stream([clicked_note])
                    thread = threading.Thread(target=play_midi_in_thread, args=(new_stream,))
                    thread.start()
            draw_text("Distance: " + str(distance) + " | " + "Frequency: " + str(frequency) + " | " + "Theta: " + str(theta), int(RESOLUTION_X / 2) - 500, int(0.95 * RESOLUTION_Y), 25, WHITE)
        else:
            if settings_buttons["timer_duration"]._enabled:
                settings_buttons["timer_duration"].toggle()
            draw_texture(game_texture, 0, 0, Color(255, 255, 255, 60))
            draw_text("[S] Settings", 50, 30, 25, WHITE)
            draw_text("[E] Encodings", RESOLUTION_X - 50 - measure_text("[E] Encodings", 25), 30, 25, WHITE)
            draw_text("[C] Chromo Wheel", RESOLUTION_X - 50 - measure_text("[C] Chromo Wheel", 25), 80, 25, WHITE)
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
                    key_copies = valid_key_copies.copy()
                    draw_rectangle(int(RESOLUTION_X / 2) - int(RESOLUTION_Y / 4), int(RESOLUTION_Y / 4), int(RESOLUTION_Y / 2), int(RESOLUTION_Y / 2), color_from_hsv(chromatic_scale_sharps[::-1].index(chromo_objects[current_trial - 1][:-1]) * (360 / chromo_wheel_divisions), 1.0, int(chromo_objects[current_trial - 1][-1]) / radial_divisions))
                    draw_text("Trial: " + str(current_trial) + " / " + str(trials), int(RESOLUTION_X / 2) - int(RESOLUTION_Y / 4), int(RESOLUTION_Y / 4) - 75, 50, WHITE)
                    if current_trial > settings_data["Chromesthesia"]["N"]:
                        if is_key_pressed(KeyboardKey.KEY_A):
                            if trial_match[current_trial - settings_data["Chromesthesia"]["N"] - 1]:
                                match_color = GREEN
                            else:
                                match_color = RED
                        draw_text(sound_objects[current_trial - settings_data["Chromesthesia"]["N"] - 1], int(RESOLUTION_X / 2) + int(RESOLUTION_Y / 4) + 100, int(RESOLUTION_Y / 2), 100, RED)
                        draw_text("[A] Match", int(RESOLUTION_X / 2) + int(RESOLUTION_Y / 4) + 100, int(RESOLUTION_Y / 2) + 100, 50, match_color)
                        if not played_sound:
                            played_sound = True
                            clicked_note = note.Note(chromo_objects[current_trial - 1][:-1] + chromo_objects[current_trial - 1][-1], quarterLength=1.0) 
                            new_stream = stream.Stream([clicked_note])
                            thread = threading.Thread(target=play_midi_in_thread, args=(new_stream,))
                            thread.start()
                    if get_time() > trial_clock:
                        trial_clock += settings_data["TimerDuration"]
                        current_trial += 1
                        match_color = WHITE
                        played_sound = False
                        if current_trial == trials:
                            reset_game()                           
            if is_key_pressed(KeyboardKey.KEY_SPACE):
                if not is_playing:
                    is_generating = True
                    reset_game()
                is_playing = not is_playing
        if not looking_at_chromo_wheel and is_key_pressed(KeyboardKey.KEY_E):
            if deep_encodings:
                deep_encodings = not deep_encodings
                viewing_grapheme_encodings = False
                viewing_chromo_encodings = False
            else:
                looking_at_encodings = not looking_at_encodings
        elif not looking_at_encodings and is_key_pressed(KeyboardKey.KEY_C):
            looking_at_chromo_wheel = not looking_at_chromo_wheel
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
