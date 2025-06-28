'''
Jordle.py - An attempt to replicate the game "Wordle"
            in a Python implementation.

Author: Jeff Brelsford

Date: 06/28/2025
'''
#======================
# imports
#======================
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox as msg
import random

######################################
# Constants
######################################
DEFAULT_BG = "#EDEDED"
DARK_GREY = '#878787'
YELLOW_BG = "#FFD572"
GREEN_BG = "#CDD00A"
WHITE_BG = "#FFFFFF"
GRAY_BG = "#C1C1C1"
BLANK_SPACE = "   "
MAX_GUESSES = 6
VERBOSE = False
CHEAT = False
DEBUG = False
GUESS_LABEL = "You have 6 guesses left"

##################################
# Used Letter Dictionary
# The Letter is the key.
# The value is the column and row
# coordinates in the used letter grid.
##################################
used_letter_dict = {
    'Q': (1, 0),
    'W': (2, 0),
    'E': (3, 0),
    'R': (4, 0),
    'T': (5, 0),
    'Y': (6, 0),
    'U': (7, 0),
    'I': (8, 0),
    'O': (9, 0),
    'P': (10, 0),
    'A': (2, 1),
    'S': (3, 1),
    'D': (4, 1),
    'F': (5, 1),
    'G': (6, 1),
    'H': (7, 1),
    'J': (8, 1),
    'K': (9, 1),
    'L': (10, 1),
    'Z': (3, 2),
    'X': (4, 2),
    'C': (5, 2),
    'V': (6, 2),
    'B': (7, 2),
    'N': (8, 2),
    'M': (9, 2)
}

######################################
# Global Variables
######################################
guess_ctr = 0
secret_word = "CHEAT"
play_again = False
secret_words = []
######################################
# Set up Window
######################################
# Create instance
win = tk.Tk()
# Add a title
win.title("Jordle")
win.geometry("410x650")
win.eval('tk::PlaceWindow . center')

######################################
# Initialize Style
######################################
style = ttk.Style()
# Use clam theme
style.theme_use('clam')
# Used TLabelframe for styling labelframe widgets,
# and use red color for border
style.configure("TLabelframe", bordercolor=DARK_GREY, font=("Arial Rounded MT Bold", 15))
#ttk.Style().configure('Font.TLabelframe', font=("Arial Rounded MT 15 Bold" ))


######################################
# Outer Frame
######################################
outer_frame = ttk.LabelFrame(win, text='', borderwidth=10)  # child of win
outer_frame.grid(column=0, row=0, padx=8, pady=4)

######################################
# Display Frame
######################################
display_frame = ttk.LabelFrame(outer_frame, text=GUESS_LABEL)
display_frame.grid(column=1, row=1, padx=10, pady=10)

######################################
# User Input (guess)
######################################
guess_frame = ttk.LabelFrame(outer_frame, text='')
guess_frame.grid(column=1, row=2, padx=10, pady=10, sticky='W')

######################################
# Used Letters
######################################
used_letter_frame = ttk.LabelFrame(outer_frame, text='Used Letter Board')
used_letter_frame.grid(column=0, row=3, sticky='W', columnspan=3)

#############################################################################################
# Logic Functions
#############################################################################################

'''
read_secret_words() - read the words.txt file into a list of secret words
'''


def read_secret_words():
    my_file = open("words.txt", "r")
    test_word = ""
    while True:
        test_word = my_file.readline()
        if test_word == '':
            break
        secret_words.append(test_word)
    my_file.close()


'''
save_secret_words() - save the contents of the secret_words list
                     and write it out to the words.txt file.
'''


def save_secret_words():
    fout = open("words.txt", "w")

    for word in secret_words:
        fout.write(word)

    fout.close()


'''
get_secret_word() - retrieve a randomized secret word from the
                   secret_words list
'''


def get_secret_word():
    secret_word = ""
    random.shuffle(secret_words)
    # Get the first NUM_LETTERS digits in the list for the secret number:
    secret_word = secret_words[0].strip().upper()
    # Now resort the list of secret_words
    secret_words.sort(key=str.lower)
    if DEBUG:
        secret_word = "SCENE"
    if CHEAT:
        print("secret_word : " + secret_word)
    return secret_word


'''
get_letter_occurrences_count() - return the count for the number
                               of times a specific letter occurs
                               within a test_word.
'''


def get_letter_occurrences_count(letter, test_word):
    ctr = 0
    for i in range(len(test_word)):
        if test_word[i] == letter:
            ctr = ctr + 1
    return ctr


'''
all_letters_guessed() - returns True if all of the letters within
                       the secret word have been guessed and 
                       False otherwise.
'''


def all_letters_guessed(letter, guess, secret_word):
    secret_ltr_count = get_letter_occurrences_count(letter, secret_word)
    guessLtrCount = get_letter_occurrences_count(letter, guess)
    if secret_ltr_count < 1:
        return True
    elif guessLtrCount > secret_ltr_count:
        return True
    else:
        ctr = 0
        for i in range(len(secret_word)):
            if secret_word[i] == guess[i] and guess[i] == letter:
                ctr = ctr + 1
        if ctr == secret_ltr_count:
            return True
        else:
            return False


'''
focus_guess_entered() - clear the guess_entered text entry and force
                       the cursor into the text entry box
'''


def focus_guess_entered():
    guess_entered.delete(0, 99)
    guess_entered.focus_force()
    display_frame.update_idletasks()  # Update the display before getting back to main loop


'''
show_guess() - update the guess puzzle board with which letters are
               correct in the guess.
'''


def show_guess():
    global guess_ctr

    if VERBOSE:
        print("Guess was " + guess_str.get())
        print("guess_ctr: " + str(guess_ctr))

    guess_str_upper = guess_str.get().upper()

    if guess_ctr > MAX_GUESSES:
        show_failure()
        return

    else:
        bg_color = WHITE_BG
        for col in range(len(guess_str_upper)):
            used_letter_key = guess_str_upper[col]
            used_letter_col = used_letter_dict[used_letter_key][0]
            used_letter_row = used_letter_dict[used_letter_key][1]
            if guess_str_upper[col] == secret_word[col]:
                # A correct letter is in the correct place.
                bg_color = GREEN_BG
                used_letter_color = GREEN_BG
            elif guess_str_upper[col] in secret_word:
                # A correct letter is in the incorrect place
                if all_letters_guessed(guess_str_upper[col], guess_str_upper, secret_word):
                    bg_color = WHITE_BG
                    used_letter_color = GRAY_BG
                else:
                    bg_color = YELLOW_BG
                    used_letter_color = YELLOW_BG

            else:
                # letter is not in the secret word
                bg_color = WHITE_BG
                used_letter_color = GRAY_BG

            lbl_text_guess = guess_str_upper[col:col + 1]
            letter_labelGuess = ttk.Label(display_frame, text=lbl_text_guess, background=bg_color,
                                          font=("Arial Rounded MT Bold", 14))
            letter_labelGuess.grid(row=guess_ctr, column=col)
            used_letter_label = ttk.Label(used_letter_frame, text=used_letter_key, background=used_letter_color)
            used_letter_label.grid(row=used_letter_row, column=used_letter_col)

        focus_guess_entered()
        guess_ctr = guess_ctr + 1
        guesses_left = MAX_GUESSES - guess_ctr
        if guesses_left == 1:
            guesses_left_msg = 'You have ' + str(guesses_left) + ' guess left'
        else:
            guesses_left_msg = 'You have ' + str(guesses_left) + ' guesses left'

        display_frame.config(text=guesses_left_msg)
        display_frame.update_idletasks()  # Update the display before getting back to main loop

        play_again = False
        if (guess_str_upper == secret_word):
            play_again = show_success()
            if play_again == False:
                quit()
            else:
                reset()
        elif (guess_ctr >= MAX_GUESSES):
            play_again = show_failure()
            if play_again == False:
                quit()
            else:
                reset()


'''
do_guess() - process the player's guess to determine if the user entered
             valid input, and then show the results of the guess to the
             player.
'''


def do_guess(event=None):  # Note the event=None - This had to be added to bind the <Return> key to this function
    if len(guess_str.get()) < 5 or len(guess_str.get()) > 5:
        show_enter_five_letters()
        return

    if VERBOSE:
        print("do_guess - Guess was " + guess_str.get())

    check_list = list(map(str, secret_words))
    x = " ".join(check_list)
    if x.find(guess_str.get()) != -1:
        if VERBOSE:
            print(guess_str.get() + " in secret_words")
        show_guess()
    else:
        if VERBOSE:
            print(guess_str.get() + " NOT in secret_words")
        answer = msg.askyesnocancel('Is That a Word?',
                                    'Is "' + guess_str.get().upper() + '" an actual word?\n If you answer Yes, I will add it to my dictionary.',
                                    parent=win)
        if answer == True:
            secret_words.append(guess_str.get() + '\n')
            show_guess()
        else:
            focus_guess_entered()


######################################
# User Input (guess)
######################################
# guess label
guess_label = ttk.Label(guess_frame, text="Enter your guess")
guess_label.grid(row=0, column=0, sticky='W')
# Adding a Textbox Entry widget
guess_str = tk.StringVar()
guess_entered = ttk.Entry(guess_frame, width=12, textvariable=guess_str, font=('Courier New', 14, 'bold'))
guess_entered.grid(row=1, column=0, sticky='W')

# guess button
guess_btn = ttk.Button(guess_frame, text="Guess Word", command=do_guess)
guess_btn.grid(row=1, column=1, sticky='W', padx=4)
win.bind('<Return>', do_guess)

######################################
# Menu Bar
######################################
'''
quit() - save the secret_words list to the words.txt file
          and close the application.
'''


def quit():
    save_secret_words()
    win.quit()
    win.destroy()
    exit()


'''
set_used_letter_label() - set the letter in the used letter board
                        with the letter, column and row position
'''


def set_used_letter_label(lbl_text, cl, rw):
    used_letter_label = ttk.Label(used_letter_frame, text=lbl_text, relief=tk.RIDGE, borderwidth=9,
                                  background=WHITE_BG)
    used_letter_label.grid(column=cl, row=rw, padx=1, pady=1)


'''
render_used_letters() - populate the used letter board at the 
                       beginning of the game.
'''


def render_used_letters():
    set_used_letter_label(BLANK_SPACE, 0, 0)
    set_used_letter_label('Q', 1, 0)
    set_used_letter_label('W', 2, 0)
    set_used_letter_label('E', 3, 0)
    set_used_letter_label('R', 4, 0)
    set_used_letter_label('T', 5, 0)
    set_used_letter_label('Y', 6, 0)
    set_used_letter_label('U', 7, 0)
    set_used_letter_label('I', 8, 0)
    set_used_letter_label('O', 9, 0)
    set_used_letter_label('P', 10, 0)
    set_used_letter_label(BLANK_SPACE, 11, 0)
    set_used_letter_label(BLANK_SPACE, 0, 1)
    set_used_letter_label(BLANK_SPACE, 1, 1)
    set_used_letter_label('A', 2, 1)
    set_used_letter_label('S', 3, 1)
    set_used_letter_label('D', 4, 1)
    set_used_letter_label('F', 5, 1)
    set_used_letter_label('G', 6, 1)
    set_used_letter_label('H', 7, 1)
    set_used_letter_label('J', 8, 1)
    set_used_letter_label('K', 9, 1)
    set_used_letter_label('L', 10, 1)
    set_used_letter_label(BLANK_SPACE, 11, 1)
    set_used_letter_label(BLANK_SPACE, 0, 2)
    set_used_letter_label(BLANK_SPACE, 1, 2)
    set_used_letter_label(BLANK_SPACE, 2, 2)
    set_used_letter_label('Z', 3, 2)
    set_used_letter_label('X', 4, 2)
    set_used_letter_label('C', 5, 2)
    set_used_letter_label('V', 6, 2)
    set_used_letter_label('B', 7, 2)
    set_used_letter_label('N', 8, 2)
    set_used_letter_label('M', 9, 2)
    set_used_letter_label(BLANK_SPACE, 10, 2)
    set_used_letter_label(BLANK_SPACE, 11, 2)


'''
reset() - reset the game to be played for the first 
           time or again.
'''


def reset():
    global secret_word
    global guess_ctr

    guess_ctr = 0
    secret_word = get_secret_word()
    for rw in range(6):
        for col in range(5):
            # lbl_text = str(rw) + ', ' + str(col)
            lbl_text = BLANK_SPACE
            letter_label = ttk.Label(display_frame, text=lbl_text, relief=tk.RIDGE, borderwidth=9, background=WHITE_BG)
            letter_label.grid(row=rw, column=col, padx=8, pady=8)
    display_frame.config(text=GUESS_LABEL)
    render_used_letters()
    focus_guess_entered()


'''
show_about() - show the About Dialog
'''


def show_about():
    msg.showinfo('Jordle', 'Jordle: A take on the game Wordle implemented in Python 3.9.\nAuthor: Jeff Brelsford',
                 parent=win)


'''
show_rules_popup() - show the How To Play Dialog
'''


def show_rules_popup():
    popup = Toplevel()
    popup.geometry("460x400")
    popup.title("How To Play Jordle")
    pop_x_pos = win.winfo_x()
    pop_y_pos = win.winfo_y()
    popup.geometry("+%d+%d" % (pop_x_pos - 20, pop_y_pos + 150))

    def close_rules():
        popup.destroy()

    rules_str = '''
    In Jordle, you have 6 chances to guess a 5-letter word.
    The puzzle board will show you each guess you make.
    
    If a letter in the puzzle board has a GREEN background
    it means that the letter is in the puzzle AND is in 
    the CORRECT position.
    
    If a letter in the puzzle board has a YELLOW background
    it means that the letter is in the puzzle but is in 
    the INCORRECT position.
    
    Your guessed letters will appear on the Used Letter Board.
    A GRAY background means the guessed letter was not 
    in the puzzle.
    
    The game is over when you either guess the puzzle
    correctly or exhaust your 6 chances.
    '''
    spacer1_label = ttk.Label(popup, text=BLANK_SPACE, background=WHITE_BG, borderwidth=3).pack()
    popup_label = ttk.Label(popup, text=rules_str, relief=tk.RIDGE, borderwidth=9).pack()
    spacer2_label = ttk.Label(popup, text=BLANK_SPACE, background=WHITE_BG, borderwidth=3).pack()

    close_button = tk.Button(popup, text="Got It!", command=close_rules, relief=tk.RAISED, background=DEFAULT_BG, width=10, borderwidth=13).pack()

    popup.mainloop()


'''
show_success() - show the Success Dialog - The player won.
'''


def show_success():
    msg.showinfo('Jordle', 'You guessed the Secret Word in ' + str(guess_ctr) + ' guesses!\n' + secret_word, parent=win)
    answer = msg.askyesnocancel('Congrats!', 'Want to Play Again?', parent=win)
    if VERBOSE:
        print("show_success answer = " + str(answer))
    return answer


'''
show_failure() - show the failure dialog. The player lost.
'''


def show_failure():
    msg.showinfo('Jordle', 'You did not guess the Secret Word in ' + str(guess_ctr) + ' guesses:\n' + secret_word,
                 parent=win)
    answer = msg.askyesnocancel('Boo!', 'Want to Try Again?', parent=win)
    if VERBOSE:
        print("show_failure answer = " + str(answer))
    return answer


'''
show_enter_five_letters() - show the dialog for the player to enter a 5-letter word.
'''


def show_enter_five_letters():
    msg.showwarning('Jordle', 'You need to enter a 5 letter word.', parent=win)
    focus_guess_entered()


'''
show_welcome_message() - show a welcome message box
'''


def show_welcome_message():
    msg.showinfo('Jordle', 'Let''s Play Some Jordle!', parent=win)
    focus_guess_entered()


menu_bar = Menu(win)
win.config(menu=menu_bar)

# Add menu items
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add another Menu to the Menu Bar and an item
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
help_menu.add_command(label="How to Play", command=show_rules_popup)
menu_bar.add_cascade(label="Help", menu=help_menu)

read_secret_words()

reset()

#show_welcome_message()

#======================
# Start GUI
#======================
win.mainloop()
