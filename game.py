from tkinter import *
from tkinter import messagebox
import os
import random

class Game:
    def __init__(self, window, difficulty, category):
        self.window = window
        self.difficulty = difficulty
        self.category = category
        self.entry_boxes = []
        self.popup = None
        self.x_position = 0
        self.y_position = 40
        self.tries = 5
        self.input_area = ""
        self.chosen_word = ""
        self.label_color = ""

        self.select_word()

    #-------> Game Widgets!
    def game_screen_setup(self):
        """
        This function has all the game screen's widgets!
        """
        
        self.game_frame = Frame(self.window, width=900, height=680, bg="lightgrey")
        self.game_frame.place(x = 50, y = 10)

        self.show_tries_text = StringVar()
        self.show_tries_text.set("Tries Left -> {}".format(self.tries))
        self.show_tries = Label(self.game_frame, bg="lightgrey", textvariable=self.show_tries_text, font=("Arial", 22))
        self.show_tries.place(x = 360, y = 50)

        self.return_btn = Button(self.game_frame, text="Return", width=10, height=2, font=("Halvetica", 12), command=lambda: (self.return_to_title_screen()))
        self.return_btn.place(x = 10, y = 10)

        self.category_chosen = Label(self.game_frame, bg="lightgrey", text="{}".format(self.category), font=("Arial", 20))
        self.category_chosen.place(x = 410, y = 10)

        self.difficulty_chosen = Label(self.game_frame, bg= self.label_color, text="{}".format(self.difficulty), fg="white", font=("Arial", 20, "bold"))
        self.difficulty_chosen.place(x = 410, y = 110)

        self.user_input = StringVar()
        self.user_input.set("")
        self.user_entry = Entry(self.game_frame, width=20, textvariable=self.user_input, font=("Halvetica", 12))
        self.user_entry.place(x = 455, y = 380)

        self.input_area = Frame(self.game_frame, width = 1000, height=500, bg="lightgrey")
        self.input_area.place(x = 0, y = 150)

        self.submit_answer = Button(self.game_frame, text = "Submit", width=10, height=2, font=("Halvetica", 18), command=lambda:(self.check_answer()))
        self.submit_answer.place(x = 380, y = 500)


        self.window.bind("<Return>", lambda event: self.check_answer())
        self.render_new_input()

    #-------> Game Management
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
        elif self.category == "Colors":
            file_name = "colors.txt"
        elif self.category == "Jobs":
            file_name = "jobs.txt"

        # Construct the full path to the file
        self.file_path = os.path.join(base_dir, "Word Bank", file_name)

        # Open the file using the absolute path
        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        word_bank = [line.rstrip("\n") for line in lines]

        #Already guesses words will not be picked again!
        for word in word_bank:
            if ";guessed" in word:
                word_bank.remove(word)

        print(word_bank)
        self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
        
        #Pick a word that has the parameters of the selected difficulty
        if self.difficulty == "Easy":
            self.label_color = "#84f069"
            while len(self.chosen_word) > 5:
                self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
                
        elif self.difficulty == "Medium":
            self.label_color = "#e0e342"
            while len(self.chosen_word) < 6 or len(self.chosen_word) > 9:
                self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
        else:
            self.label_color = "#de1c07"
            while len(self.chosen_word) < 9:
                self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
        
        print("The chosen word's length -> {}".format(len(self.chosen_word)))
        print("The chosen word is -> {}".format(self.chosen_word))
        self.game_screen_setup()


    def render_new_input(self):
        """
        This function will render a row of entry boxes where the user can submit their guess
        This function is first called when the game screen is created as well as everytime the user submits a guess
        """
        
        self.calculate_center_frame()

        for i, char in enumerate(self.chosen_word):
            if char != " ":
                new_entry = Entry(self.input_area, bg = "white", font =("Arial", 28), width=2)
                new_entry.place(x = self.x_position, y = self.y_position)

                new_entry.bind("<KeyRelease>", self.limit_number_chars)
                new_entry.bind("<FocusIn>", self.on_focus_in)
                new_entry.bind("<Left>", self.shift_focus_left)
                new_entry.bind("<Right>", self.shift_focus_right)

                self.entry_boxes.append(new_entry)
            self.x_position += 50
        self.entry_boxes[0].focus_set()

    
    #----> Input Functionalities
    def limit_number_chars(self, event):
        """
        This function prevents the user from typing more than 1 char in a Entry box

        """
        entry = event.widget
        current_char = entry.get().upper()
        entry.delete(0, END)
        entry.insert(0, current_char)

        #------

        n_chars = len(entry.get())
        if (n_chars > 1):
            entry.delete(1, END)
            

    def on_focus_in(self, event):
        """
        This function tracks the current focused entry so the "shift_entry_focus" method can work
        """
        self.entry_widget = event.widget
        if self.entry_widget in self.entry_boxes:
            self.entry_current_index = self.entry_boxes.index(self.entry_widget)
        else:
            self.entry_current_index = -1 


    def shift_focus_right(self, event):
        """
        This function will move the Entry focus to the entry on the right of the previous Entry
        """
        self.entry_widget = event.widget
        self.entry_current_index = self.entry_boxes.index(self.entry_widget)

        if len(self.entry_widget.get()) >= 0 and self.entry_current_index < len(self.entry_boxes) - 1:
            next_entry_box = self.entry_boxes[self.entry_current_index + 1]
            next_entry_box.focus_set()
        else:
            next_entry_box = self.entry_boxes[0]
            next_entry_box.focus_set()
        

    def shift_focus_left(self, event):
        """
        This function will move the Entry focus to the entry on the left of the previous Entry
        """
        self.entry_widget = event.widget
        self.entry_current_index = self.entry_boxes.index(self.entry_widget)

        if self.entry_current_index > 0:
            previous_entry_box = self.entry_boxes[self.entry_current_index - 1]
            previous_entry_box.focus_set()
        else:
            previous_entry_box = self.entry_boxes[len(self.entry_boxes) - 1]
            previous_entry_box.focus_set()


    def calculate_center_frame(self):
        """
        This function center the "game_frame" Frame vertically 
        based on the length of the secret word
        """
        word_length = len(self.chosen_word)
        match word_length:
            case 3: self.x_position = 370
            case 4: self.x_position = 350
            case 5: self.x_position = 330
            case 6: self.x_position = 300
            case 7: self.x_position = 280
            case 8: self.x_position = 260
            case 9: self.x_position = 240
            case 10: self.x_position = 220
            case 11: self.x_position = 200
            case 12: self.x_position = 180
            case 13: self.x_position = 140
            case 14: self.x_position = 120
            case 15: self.x_position = 100
    

    #----> Check user's answer
    def check_answer(self):
        """
        Once the user submits their guess, this function will check which
        letters are in the correct position (green bg),
        which are in the wrong position (yellow bg),
        and which aren't in the secret word at all (grey bg)
        """
        self.calculate_center_frame()
        new_guess = ""
        #Sum all the letters wrote to form the guess word!
        for letter in self.entry_boxes:
            new_guess += letter.get()
        
        secret_word = self.chosen_word.replace(" ","") #Remove a space when there is one so the lengtho of the secret word is not interfered by the space 

        #Check if the nª of letters of the user's guess and the secret word are the same!
        if len(new_guess) == len(secret_word):
            #Clear the entry_boxes array for the next guess!
            for letter in self.entry_boxes:
                letter.place_forget()
            self.entry_boxes.clear()
            
            n_spaces = 0 #To increment with "i" if there is a space in the secret word
            #Check if the letter is in the word
            for i, letter in enumerate(new_guess):
                if self.chosen_word[i] == " ":
                    n_spaces += 1
                    self.x_position += 50
                if letter in self.chosen_word and letter != self.chosen_word[i + n_spaces]:
                    #The letter is in the word, but in the wrong position
                    self.render_result("yellow", letter)
                elif letter == self.chosen_word[i + n_spaces]:
                    #The letter is in the word as well as in the correct position
                    self.render_result("green", letter)
                else:
                    #The letter isn't in the word
                    self.render_result("lightgrey", letter)
                self.x_position += 50

            if new_guess == secret_word: 
                messagebox.showinfo("CONGRATS!", "YOU GOT IT RIGHT!")
                self.update_word_bank()
                self.play_again()
            else:
                if self.tries > 1:
                    self.tries-=1
                    self.show_tries_text.set("Tries left -> {}".format(self.tries))
                    self.y_position += 60
                    self.render_new_input()
                else: 
                    self.losing_popup()
                    
        else:
            messagebox.showinfo("Info","You need to fill all blank spaces!")

    
    def render_result(self, color, letter):
        """
        This function will render the result of the user's guess
        """
        if color == "green":
            letter_result = Label(self.input_area, bg="#77d442", font=("Arial", 28), fg="white", text=letter, width= 2)
            letter_result.place(x = self.x_position, y = self.y_position)
        elif color == "yellow":
            letter_result = Label(self.input_area, bg="#ebf739", font=("Arial", 28), fg="white",  text=letter, width= 2)
            letter_result.place(x = self.x_position, y = self.y_position)
        else:
            letter_result = Label(self.input_area, bg="lightgrey", font=("Arial", 28),  text=letter, width= 2)
            letter_result.place(x = self.x_position, y = self.y_position)


    #----> After game ending
    def update_word_bank(self):
        """
        By guessing a word, that word will not appear anymore as long as the user doesn't reset the word bank
        So the word won't appear more times
        """

        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        word_bank = [line.rstrip("\n") for line in lines]
        
        #Iterate the word bank to update the secret word so it doesn't get chosen again
        for i in range(len(word_bank)):
            if word_bank[i].upper() == self.chosen_word:
                word_bank[i] += ";guessed"  
                
        
        with open(self.file_path, "w", encoding="utf-8") as f:
            for word in word_bank:
                if not word_bank[len(word_bank) - 1] == word:
                    f.write(word + "\n")
                else:
                    f.write(word)

    
    def return_to_title_screen(self):
        if self.popup is not None:
            self.popup.destroy()

        self.game_frame.place_forget()

        from game_settings_screen import ClassicModeSettings
        ClassicModeSettings(self.window)


    def play_again(self):
        """
        Keep playing the game (same category and difficulty chosen!).
        """
        if self.popup is not None:
            self.popup.destroy()

        self.game_frame.place_forget()
        Game(self.window, self.difficulty, self.category)
    

    def losing_popup(self):
        """
        This function will display a "popup" showing the user that they spent
        all tries as well as the correct answer
        It also gives the user the possibility to go back to the title screen
        or keep playing!
        """
        self.popup = Toplevel()
        self.popup.title("You lost! :(")
        self.popup.geometry("500x300")
        self.popup.resizable(False, False)
        self.popup.config(background="lightgrey")
        from main import AppConfig
        AppConfig.center_window(self.popup, 500, 300)

        losing_message_lbl = Label(self.popup, text="You lost! :(", font = ("Arial", 18), bg="lightgrey")
        losing_message_lbl.place(x = 190, y = 20)

        correct_answer_lbl = Label(self.popup, text="The correct answer was -> {}".format(self.chosen_word), font=("Arial", 14), bg="lightgrey")
        correct_answer_lbl.place(x = 90, y = 80)

        go_back_btn = Button(self.popup, text = "Return to \n Title Screen!",width= 12, height=3, font=("Arial", 12), command=lambda:self.return_to_title_screen())
        go_back_btn.place(x = 100, y = 150)

        play_again_btn = Button(self.popup, text="Play again!",width= 12, height=3, font=("Arial", 12), command=lambda:self.play_again())
        play_again_btn.place(x = 300, y = 150)
        