'''
This is a script used to play songs for runthroughs.  You can specify a list of types of songs
to play (WTVFQ, CRSPJ, WTAFAV for smooth), and it will randomly play songs from your collection.
This script has strict dependencies on the sox and afplay command line programs.
'''

import os
import time
import random

# Get lists of songs
standard_smooth_folder = "Standard-Smooth"
latin_folder = "Latin"

names = {
    "W": "Waltz",
    "T": "Tango",
    "F": "Slow Foxtrot",
    "Q": "Quickstep",
    "V": "Viennese Waltz",
    "AF": "American Foxtrot",
    "AV": "American Viennese Waltz",
    "C": "Cha-Cha",
    "S": "Samba",
    "R": "Rumba",
    "J": "Jive",
    "P": "Paso Doble"
}

rates = {
    "AF": 1.04,
    "AV": 0.93
}

set_lengths = {
    "P": {
        "length": 83.5,
        "fadeout": 0
    },
    "V": {
        "length": 75,
        "fadeout": 3
    }
}

paths = {
    "W": os.path.join(standard_smooth_folder, "Waltz"),
    "T": os.path.join(standard_smooth_folder, "Tango"),
    "F": os.path.join(standard_smooth_folder, "Slow Foxtrot"),
    "AF": os.path.join(standard_smooth_folder, "Slow Foxtrot"),
    "Q": os.path.join(standard_smooth_folder, "Quickstep"),
    "V": os.path.join(standard_smooth_folder, "VWaltz"),
    "AV": os.path.join(standard_smooth_folder, "VWaltz"),
    "C": os.path.join(latin_folder, "Cha"),
    "S": os.path.join(latin_folder, "Samba"),
    "R": os.path.join(latin_folder, "Rumba"),
    "J": os.path.join(latin_folder, "Jive"),
    "P": os.path.join(latin_folder, "Paso")
}

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

songs = {}
played = {}

for key in paths.keys():
    song_list = os.listdir(paths[key])
    songs[key] = [os.path.join(paths[key], song) for song in song_list if song[0] != '.']
    played[key] = []

def play_song(song, length, speed=1, fadeout=3):
    print color.BOLD + 'Curently playing: ' + color.RED + song + color.END + color.END
    base_sox_command = 'sox "{0}" current_song.wav '.format(song)
    fade_command = 'fade h 0 {0} {1} '.format(length, fadeout)
    speed_command = 'speed {0} '.format(speed)
    # volume_command = '-v 1.2 '
    os.system(base_sox_command + fade_command + speed_command)
    os.system('afplay -v 1.5 current_song.wav')

def play_round(song_keys, length, break_time):
    for index, song_key in enumerate(song_keys):
        time.sleep(break_time)

        song_list = songs[song_key]
        played_list = played[song_key]
        valid_list = [song for song in song_list if song not in played_list]


        if len(valid_list) == 0:
            valid_list = song_list
            played[song_key] = []

        song = random.choice(valid_list)

        speed = 1
        if song_key in rates:
            speed = rates[song_key]

        fadeout = 3
        if song_key in set_lengths:
            length = set_lengths[song_key]["length"]
            fadeout = set_lengths[song_key]["fadeout"]

        played[song_key].append(song)
        play_song(song, length, speed, fadeout)

while True:
    choice = raw_input(color.CYAN + 'R to play a round, T to set a timer, Q to quit: ').lower()
    if (choice == 'r'):
        print('Type in songs in format WTVFQ, CRSPJ, etc')
        print('For American Foxtrot or V Waltz, type AF or AV like WTAFAV')
        songs_to_play = raw_input('Songs to play: ').upper()
        length = input('How many seconds should each song be played for? ')
        break_time = input('How many seconds break before each dance? ')

        print(color.END)
        
        song_keys = []
        american_style = False
        for key in songs_to_play:
            if key in names.keys():
                song_keys.append(('A' if american_style else '') + key)
                american_style = False
            elif key == 'A':
                american_style = True

        play_round(song_keys, length, break_time)

    if (choice == 't'):
        timer_length = input('How many seconds total? ')
        warning = 'n'
        if timer_length > 60:
            warning = raw_input('Give a one-minute warning (Y/N)? ').lower()
        
        print(color.END)

        if warning == 'y' :
            first_timer = timer_length - 60
            time.sleep(first_timer)
            os.system('say "One minute warning"')
            time.sleep(60)
        else:
            time.sleep(timer_length)
        os.system('say "The timer is going off"')
    if (choice == 'q'):
        print(color.END)
        
        os.system('rm current_song.wav')
        break