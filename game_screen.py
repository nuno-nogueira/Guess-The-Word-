from tkinter import *
from tkinter import messagebox
import random
import os


class GameScreenApp:
    def __init__(self, window, category):
        self.window = window
        self.category = category
        self.tries = 5
        self.entry_boxes = []
        self.y_position = 20

        self.select_word()
        self.setup_game_screen()
        

    def setup_game_screen(self):
        """
        This function will setup the game screen's UI
        """
        self.game_frame = Frame(self.window, width=1000, height=700, bg="grey")
        self.game_frame.place(x = 0, y = 0)

        self.show_tries_text = StringVar()
        self.show_tries_text.set("Tries Left -> {}".format(self.tries))
        self.show_tries = Label(self.game_frame, bg="grey", textvariable=self.show_tries_text, font=("Arial", 22))
        self.show_tries.place(x = 420, y = 80)

        self.return_btn = Button(self.game_frame, text="Return", width=10, height=2, font=("Halvetica", 12), command=lambda: (self.return_to_title_screen()))
        self.return_btn.place(x = 50, y = 10)

        self.category_chosen = Label(self.game_frame, bg="grey", text="{}".format(self.category), font=("Arial", 20))
        self.category_chosen.place(x = 450, y = 30)


        self.user_input = StringVar()
        self.user_input.set("")
        self.user_entry = Entry(self.game_frame, width=20, textvariable=self.user_input, font=("Halvetica", 12))
        self.user_entry.place(x = 405, y = 380)

        self.input_area = Frame(self.game_frame, width = 1000, height=500, bg="grey")
        self.input_area.place(x = 0, y = 150)


        self.submit_answer = Button(self.game_frame, text = "Submit", width=10, height=2, font=("Halvetica", 18), command=lambda:(self.check_answer()))
        self.submit_answer.place(x = 420, y = 480)

        self.render_new_input()
        print("The chosen word was -> {}".format(self.chosen_word))


    def select_word(self):
        """
        Based on the category chosen by the user, 
        a random word is picked from the chosen category
        """
        #Initialize the "file_name" and "category" variables based on the category chosen
        file_name = ""

        # Get the absolute path of the directory where the script is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        #Check which category the user chose and open the respective word bank
        if self.category == "Animals":
            file_name = "animals.txt" 
        elif self.category == "Fruits":
            file_name = "fruits.txt"
        elif self.category == "Countries":
            file_name = "countries.txt"
        elif self.category == "Jobs":
            file_name = "jobs.txt"

        # Construct the full path to the file
        file_path = os.path.join(base_dir, "Word Bank", file_name)

        # Open the file using the absolute path
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        word_bank = [line.rstrip("\n") for line in lines]
        self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
    

    def render_new_input(self):
        """
        This function will render a row of entry boxes where the user can submit their guess
        This function is first called when the game screen is created as well as everytime the user submits a guess
        """
        
        x_position = self.calculate_center_frame()
        for i in enumerate(self.chosen_word):
            new_entry = Entry(self.input_area, bg = "white", font =("Arial", 28), width=2)
            new_entry.place(x = x_position, y = self.y_position)

            new_entry.bind("<KeyRelease>", self.limit_number_chars)
            new_entry.bind("<FocusIn>", self.on_focus_in)

            self.entry_boxes.append(new_entry)
            x_position += 50

        self.entry_boxes[0].focus_set()


    def check_answer(self):
        """
        Once the user submits their guess, this function will check which
        letters are in the correct position (green bg),
        which are in the wrong position (yellow bg),
        and which aren't in the secret word at all (grey bg)
        """
        x_position = self.calculate_center_frame()
        new_guess = ""
        #Sum all the letters wrote to form the guess word!
        for letter in self.entry_boxes:
            new_guess += letter.get()
        
        #Check if the nª of letters of the user's guess and the secret word are the same!
        if len(new_guess) == len(self.chosen_word):
            #Clear the entry_boxes array for the next guess!
            for letter in self.entry_boxes:
                letter.place_forget()
            self.entry_boxes.clear()
            
            #Check if the letter is in the word
            for i, letter in enumerate(new_guess):
                if letter in self.chosen_word and letter != self.chosen_word[i]:
                    #The letter is in the word, but in the wrong position
                    self.render_result("yellow",x_position, letter)
                elif letter == self.chosen_word[i]:
                    #The letter is in the word as well as in the correct position
                    self.render_result("green",x_position, letter)
                else:
                    #The letter isn't in the word
                    self.render_result("lightgrey", x_position, letter)
                x_position += 50

            if new_guess == self.chosen_word: 
                messagebox.showinfo("CONGRATS!", "YOU GOT IT RIGHT!")
                self.return_to_title_screen()
            else:
                if self.tries > 1:
                    self.tries-=1
                    self.show_tries_text.set("Tries left -> {}".format(self.tries))
                    self.y_position += 60
                    self.render_new_input()
                else: 
                    messagebox.showwarning("You lost!", "You spent all tries! :( \n The answer was -> {}".format(self.chosen_word))
                    self.go_back()
        else:
            messagebox.showinfo("Info","You need to fill all blank spaces!")


    def render_result(self, color, x_position, letter):
        """
        This function will render the result of the user's guess
        """
        if color == "green":
            letter_result = Label(self.input_area, bg="green", font=("Arial", 28), fg="white", text=letter, width= 2)
            letter_result.place(x = x_position, y = self.y_position)
        elif color == "yellow":
            letter_result = Label(self.input_area, bg="yellow", font=("Arial", 28), fg="black",  text=letter, width= 2)
            letter_result.place(x = x_position, y = self.y_position)
        else:
            letter_result = Label(self.input_area, bg="lightgrey", font=("Arial", 28),  text=letter, width= 2)
            letter_result.place(x = x_position, y = self.y_position)


    
    def limit_number_chars(self, event):
        """
        This function has two functionalities:
        -> Prevents the user from typing more than 1 char in a Entry box
        -> Automatically capitalizes every char typed in the Entry box

        """
        entry = event.widget
        current_char = entry.get().upper()
        entry.delete(0, END)
        entry.insert(0, current_char)

        #------

        n_chars = len(entry.get())
        if (n_chars > 1):
            entry.delete(1, END)
            
        #------

        self.shift_entry_focus()
        
    def on_focus_in(self, event):
        """
        This function tracks the current focused entry so the "shift_entry_focus" method can work
        """
        self.entry_widget = event.widget
        self.entry_current_index = self.entry_boxes.index(self.entry_widget)
        
    def shift_entry_focus(self):
        """
        This function will detect which entry box is "focused" and shift onto
        the next one once the user types the letter in a entry box
        """
        if self.entry_widget is not None and len(self.entry_widget.get()) >= 1 and self.entry_current_index < len(self.entry_boxes) - 1:
            next_entry_box = self.entry_boxes[self.entry_current_index + 1]
            next_entry_box.focus_set()


    def calculate_center_frame(self):
        """
        This function center the "game_frame" Frame vertically 
        based on the length of the secret word
        """
        word_length = len(self.chosen_word)
        match word_length:
            case 3: x_position = 420
            case 4: x_position = 400
            case 5: x_position = 380
            case 6: x_position = 350
            case 7: x_position = 330
            case 8: x_position = 310
            case 9: x_position = 290
            case 10: x_position = 270
            case 11: x_position = 250
            case 12: x_position = 230
        return x_position


    def return_to_title_screen(self):
        self.game_frame.place_forget()

        from title_screen import TitleScreenApp
        TitleScreenApp(self.window)

