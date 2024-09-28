from tkinter import *
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import random
    
class Game:
    def __init__(self, window, difficulty, category, gamemode):
        self.window = window
        self.difficulty = difficulty
        self.category = category
        self.gamemode = gamemode
        self.entry_boxes = []
        self.popup = None
        self.x_position = 0
        self.y_position = 40
        self.tries = 5
        self.input_area = ""
        self.chosen_word = ""
        self.label_color = ""
        #---> Challenge-related variables
        self.challenge_words = [] #--> To store all chosen words for the challenge
        self.word_counter = 1 #--> To count the amount of words the user guessed
        #Timer variables
        self.minutes_timer = 5
        self.seconds_timer = 1
    
        if self.gamemode == "Classic":
            self.save_user_info()
            self.select_word()
        elif self.gamemode == "Flag":
            self.select_country()

    #-------> Game Screen Widgets!
    def classic_mode_screen_setup(self, chosen_difficulty, minutes_timer, seconds_timer):
        """
        This function has all the game screen's widgets!
        """
        
        self.minutes_timer = minutes_timer
        self.seconds_timer = seconds_timer

        self.game_frame = Frame(self.window, width=950, height=680, bg="lightgrey")
        self.game_frame.place(x = 25, y = 10)

        self.show_tries_text = StringVar()
        self.show_tries_text.set("Tries Left -> {}".format(self.tries))
        self.show_tries = Label(self.game_frame, bg="lightgrey", textvariable=self.show_tries_text, font=("Arial", 22))
        self.show_tries.place(x = 360, y = 50)

        self.category_chosen = Label(self.game_frame, bg="lightgrey", text="{}".format(self.category), font=("Arial", 20))
        self.category_chosen.place(x = self.category_label_x_pos, y = 10)

        self.difficulty_chosen = Label(self.game_frame, bg= self.label_color, text="{}".format(chosen_difficulty), fg="white", font=("Arial", 20, "bold"))
        self.difficulty_chosen.place(x = self.difficulty_label_x_pos, y = 90)


        self.user_input = StringVar()
        self.user_input.set("")
        self.user_entry = Entry(self.game_frame, width=20, textvariable=self.user_input, font=("Halvetica", 12))
        self.user_entry.place(x = 455, y = 380)

        self.input_area = Frame(self.game_frame, width = 1000, height=500, bg="lightgrey")
        self.input_area.place(x = 0, y = 150)

        self.submit_answer = Button(self.game_frame, text = "Submit", width=10, height=1, font=("Halvetica", 18, "bold"), command=lambda:(self.check_answer()))
        self.submit_answer.place(x = 375, y = 500)


        if self.difficulty == "Challenge":
            self.timer = Label(self.game_frame, bg="lightgrey", text="{}:{}".format(self.minutes_timer, self.seconds_timer), font=("Arial", 22, "bold"))
            self.timer.place(x = 420, y = 140)
            self.set_timer(self.minutes_timer, self.seconds_timer)

        #--> Go back button
        icon_path = os.path.join("images","go_back_icon.png")
        icon = Image.open(icon_path)
        icon = icon.resize((56, 56))
        open_new_icon = ImageTk.PhotoImage(icon)
        self.go_back_button = Button(self.game_frame, image=open_new_icon, bg="lightgrey", command=lambda: (self.return_to_title_screen()))
        self.go_back_button.image = open_new_icon
        self.go_back_button.place(x = 820, y = 10)

        self.window.bind("<Return>", lambda event: self.check_answer())
        self.render_new_input()


    def flag_mode_screen_setup(self):
        """
        This function contains all the game screen's widgets for
        the "Flag Mode"
        """

        self.game_frame = Frame(self.window, width=950, height=680, bg="lightgrey")
        self.game_frame.place(x = 25, y = 10)

        self.show_tries_text = StringVar()
        self.show_tries_text.set("Tries Left -> {}".format(self.tries))
        self.show_tries = Label(self.game_frame, bg="lightgrey", textvariable=self.show_tries_text, font=("Arial", 22))
        self.show_tries.place(x = 380, y = 50)

        self.category_chosen = Label(self.game_frame, bg=self.category_label_color, text="{}".format(self.category), font=("Arial", 20, "bold"))
        self.category_chosen.place(x = self.category_label_x_pos, y = 10)

        flag_path = os.path.join(self.folder_path, self.chosen_country_flag)
        flag = Image.open(flag_path)
        flag = flag.resize((130, 90))
        open_flag = ImageTk.PhotoImage(flag)
        self.flag_image = Label(self.game_frame, image = open_flag, bg = "lightgrey")
        self.flag_image.image = open_flag
        self.flag_image.place(x = 400, y = 110)

        # --> Place the current directory path 4 folders back
        os.chdir('..\\..')
        os.chdir('..\\..')

        self.user_input = StringVar()
        self.user_input.set("")
        self.user_entry = Entry(self.game_frame, width=20, textvariable=self.user_input, font=("Halvetica", 12))
        self.user_entry.place(x = 455, y = 500)

        self.input_area = Frame(self.game_frame, width = 1000, height=500, bg="lightgrey")
        self.input_area.place(x = 0, y = 200)

        self.submit_answer = Button(self.game_frame, text = "Submit", width=10, height=1, font=("Halvetica", 18, "bold"), command=lambda:(self.check_answer()))
        self.submit_answer.place(x = 410, y = 600)


        #--> Go back button
        icon_path = os.path.join("images","go_back_icon.png")
        icon = Image.open(icon_path)
        icon = icon.resize((56, 56))
        open_new_icon = ImageTk.PhotoImage(icon)
        self.go_back_button = Button(self.game_frame, image=open_new_icon, bg="lightgrey", command=lambda: (self.return_to_title_screen()))
        self.go_back_button.image = open_new_icon
        self.go_back_button.place(x = 850, y = 10)

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
            self.category_label_x_pos = 400
        elif self.category == "Fruits":
            file_name = "fruits.txt"
            self.category_label_x_pos = 415
        elif self.category == "Colors":
            file_name = "colors.txt"
            self.category_label_x_pos = 410
        elif self.category == "Jobs":
            file_name = "jobs.txt"
            self.category_label_x_pos = 420

        # Construct the full path to the file
        self.file_path = os.path.join(base_dir, "Word Bank", file_name)

        # Open the file using the absolute path
        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        word_bank = []

        #Already guessed words won't be picked again! (Unless the user resets the Word Bank)
        for line in lines:
            line = line.rstrip("\n")
            if ";guessed" not in line:
                word_bank.append(line)

            if self.difficulty == "Challenge":
                word_bank.append(line[:-8])
           
                    

        # So the "Challenge complete" line is not counted as a word
        del word_bank[len(word_bank) - 1]

        self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
    
        chosen_difficulty = self.difficulty

        if chosen_difficulty == "Random":
            difficulties = ["Easy","Medium","Hard"]
            chosen_difficulty = difficulties[random.randint(-1, 2)]

        #Check if there are words within the difficulty & category chosen
        if chosen_difficulty != "Challenge":
            words_available = False
            for word in word_bank:
                if chosen_difficulty == "Easy":
                    if len(word) <= 5:
                        words_available = True
                elif chosen_difficulty == "Medium":
                    if len(word) >= 6 and len(word) <= 9:
                        words_available = True
                elif chosen_difficulty == "Hard":
                    if len(word) >= 10:
                        words_available = True

            if words_available == False:
                messagebox.showinfo("All words found!","All words were found for the {} difficulty in the {} category!\n Try to choose a different category and/or difficulty!" .format(chosen_difficulty, self.category))
                from game_settings_screen import ClassicModeSettings
                ClassicModeSettings(self.window)
                return

        #Pick a word that has the parameters of the selected difficulty
        if chosen_difficulty == "Easy":
            self.label_color = "#84f069"
            self.difficulty_label_x_pos = 420
            while len(self.chosen_word) > 5:
                self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
        elif chosen_difficulty == "Medium":
            self.label_color = "#e0e342"
            self.difficulty_label_x_pos = 400
            while len(self.chosen_word) < 6 or len(self.chosen_word) > 9:
                self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
        elif chosen_difficulty == "Hard":
            self.label_color = "#de1c07"
            self.difficulty_label_x_pos = 420
            while len(self.chosen_word) < 10:
                self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
        elif chosen_difficulty == "Challenge":
            self.label_color = "#751207"
            self.difficulty_label_x_pos = 380
            for i in range (5):
                while len(self.chosen_word) < 10 or self.chosen_word in self.challenge_words:
                        self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
                self.challenge_words.append(self.chosen_word)
                self.chosen_word = self.challenge_words[0]
        print("The chosen word is -> {}\n".format(self.chosen_word))
        print("Challenge words -> {}".format(self.challenge_words))
        self.classic_mode_screen_setup(chosen_difficulty, self.minutes_timer, self.seconds_timer)


    def select_country(self):
        """
        Based on the continent chosen by the user, 
        a random word is picked from that chosen continent
        """

        folder_name = "" # --> This variable will contain the folder's name depending on which continent the player chose!

        base_dir = os.path.dirname(os.path.abspath(__file__)) # --> Absolute path for the script directory

        if self.category == "Europe":
            folder_name = "europe"
            self.category_label_x_pos = 425
            self.category_label_color = "#bcf6f0"

        elif self.category == "America":
            folder_name = "america"
            self.category_label_x_pos = 410
            self.category_label_color = "#f8cb76"

        elif self.category == "Asia":
            folder_name = "asia"
            self.category_label_x_pos = 440
            self.category_label_color = "#f77070"

        elif self.category == "Africa":
            folder_name = "africa"
            self.category_label_x_pos = 430
            self.category_label_color = "#a7f770"

        elif self.category == "Oceania":
            folder_name = "oceania"
            self.category_label_x_pos = 420
            self.category_label_color = "#70f7c4"

        # --> Construct the full path to the wanted folder
        self.folder_path = os.path.join(base_dir, "images", "flag_gamemode", "country_icons", folder_name)

        # --> To position in the continent folder containing all flag images
        os.chdir(self.folder_path)

        # --> This array will contain all flag images
        countries_image_list = os.listdir()
        
        # --> Add the file name for the chosen continent
        self.file_path = os.path.join(base_dir, "Word Bank", "flag_gamemode", folder_name)
        self.file_path = self.file_path + ".txt"

        with open(self.file_path, "r", encoding = "utf-8") as f:
            lines = f.readlines()


        country_bank = []

        #Already guessed words won't be picked again! (Unless the user resets the Word Bank)
        for line in lines:
            line = line.rstrip("\n")
            if ";guessed" not in line:
                country_bank.append(line)
            else:
                
                line = line[:-8]
                line = line.lower()
                if line.find(" "):
                    line = line.replace(" ", "-")
                countries_image_list.remove(line + ".png")

        if len(country_bank) == 0:
            messagebox.showinfo("All words found!","All countries were found for {}!" .format(self.category))
            from game_settings_screen import FlagModeSettings
            os.chdir('..\\..')
            os.chdir('..\\..')
            FlagModeSettings(self.window)
            return

        random_index = random.randint(0, len(country_bank) - 1)
        self.chosen_country = country_bank[random_index].upper()
        self.chosen_country_flag = countries_image_list[random_index]

        print("The chosen country is -> {}\n" .format(self.chosen_country))
        print(self.chosen_country_flag)

        self.flag_mode_screen_setup()
            

    def render_new_input(self):
        """
        This function will render a row of entry boxes where the user can submit their guess
        This function is first called when the game screen is created as well as everytime the user submits a guess
        """
        
        self.calculate_center_frame()

        if self.gamemode == "Classic":
            secret_word = self.chosen_word
        else:
            secret_word = self.chosen_country

        for i, char in enumerate(secret_word):
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

    
    def set_timer(self, minutes_timer, seconds_timer):
        self.minutes_timer = minutes_timer
        self.seconds_timer = seconds_timer

        self.seconds_timer -= 1
        if self.seconds_timer == 0:
            if self.minutes_timer == 0:
                messagebox.showwarning("Game's over","Time's up! :(")
                self.return_to_title_screen()
                return
            self.seconds_timer = 59
            self.minutes_timer -= 1
        
        if self.seconds_timer < 10:
            self.timer.config(text = "{}:0{}".format(self.minutes_timer, self.seconds_timer))
        else:
            self.timer.config(text = "{}:{}".format(self.minutes_timer, self.seconds_timer))

        self.timer_id = self.window.after(1000, lambda: self.set_timer(self.minutes_timer, self.seconds_timer))


    def stop_timer(self):
        """
        This function will stop the set_timer() function once the user guesses a word
        If this function wasn't here, there would be for example 2 timers running in the 
        2nd mysterious word
        """
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

    #----> Input Functionalities
    def limit_number_chars(self, event):
        """
        This function prevents the user from typing more than 1 char in a Entry box

        """
        entry = event.widget
        current_char = entry.get().upper()

        # Only 1 char per entry box
        entry.delete(0, END)
        entry.insert(0, current_char)

        # Get the current index of the entry
        current_index = self.entry_boxes.index(entry)

        # Check if the pressed key isn't an arrow key so it allows the user to shift focus manually
        if event.keysym not in ["Left","Right"]:
            # Automatically moves the focus to the next entry if 1 char is in the entry box
            if len(current_char) == 1 and current_index < len(self.entry_boxes) - 1:
                next_entry = self.entry_boxes[current_index + 1]
                next_entry.focus_set()

        # Delete the extra chars 
        n_chars = len(entry.get())
        if (n_chars > 1):
            entry.delete(1, END)
            

    def on_focus_in(self, event):
        """
        Tracks the current focused entry so the "shift_entry_focus" method can work
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
        #If the focus is on the last entry box, it will cycle back to the 1st entry box
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
        #If the focus is on the first entry box, it will cycle back to the last entry box
        else:
            previous_entry_box = self.entry_boxes[len(self.entry_boxes) - 1]
            previous_entry_box.focus_set()


    def calculate_center_frame(self):
        """
        This function center the "game_frame" Frame vertically 
        based on the length of the secret word
        """
        if self.gamemode == "Classic":
            word_length = len(self.chosen_word)
        else:
            word_length = len(self.chosen_country)

        match word_length:
            case 2: self.x_position = 390
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
            case 16: self.x_position = 80
            case 17: self.x_position = 60
            case 18: self.x_position = 40
    

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

        #Sum all the letters wrote to form the user's guess!
        for letter in self.entry_boxes:
            new_guess += letter.get()

        #Remove a space when there is one so the secret word's length isn't interfered by the space 
        if self.gamemode == "Classic":
            secret_word = self.chosen_word.replace(" ","") 
        else:
            secret_word = self.chosen_country.replace(" ","") 

        #Check if the nª of letters of the user's guess and the secret word are the same!
        if len(new_guess) == len(secret_word):
            #Clear the entry_boxes array for the next guess!
            for letter in self.entry_boxes:
                letter.place_forget()
            self.entry_boxes.clear()
            
            n_spaces = 0 #To increment with "i" if there is a space in the secret word
            #Check if the letter is in the word
            for i, letter in enumerate(new_guess):
                if self.gamemode == "Classic":
                    if self.chosen_word[i] == " ":
                        n_spaces += 1
                        self.x_position += 50
                    if letter in self.chosen_word and letter != self.chosen_word[i + n_spaces]:
                        #If the letter is correct and the position where that letter is supposed to be already has that letter
                        for j in range (len(self.chosen_word)):
                            if new_guess[j] == new_guess[i] and new_guess[j] == self.chosen_word[j + n_spaces]:
                                self.render_result("lightgrey", letter)
                                break
                            if j == (len(self.chosen_word) - 1):
                                #The letter is in the word, but in the wrong position
                                self.render_result("yellow", letter)
                    elif letter == self.chosen_word[i + n_spaces]:
                        #The letter is in the word as well as in the correct position
                        self.render_result("green", letter)
                    else:
                        #The letter isn't in the word
                        self.render_result("lightgrey", letter)
                    self.x_position += 50
                else:
                    if self.chosen_country[i] == " ":
                        n_spaces += 1
                        self.x_position += 50
                    if letter in self.chosen_country and letter != self.chosen_country[i + n_spaces]:
                        #If the letter is correct and the position where that letter is supposed to be already has that letter
                        for j in range (len(self.chosen_country)):
                            if new_guess[j] == new_guess[i] and new_guess[j] == self.chosen_country[j + n_spaces]:
                                self.render_result("lightgrey", letter)
                                break
                            if j == (len(self.chosen_country) - 1):
                                #The letter is in the word, but in the wrong position
                                self.render_result("yellow", letter)
                    elif letter == self.chosen_country[i + n_spaces]:
                        #The letter is in the word as well as in the correct position
                        self.render_result("green", letter)
                    else:
                        #The letter isn't in the word
                        self.render_result("lightgrey", letter)
                    self.x_position += 50

            if new_guess == secret_word: 
                if self.difficulty == "Challenge":
                    if self.word_counter == 5:
                        messagebox.showinfo("WOOO","CONGRATS, YOU DID IT! :D")
                        self.update_word_bank()
                        self.save_user_info()
                        self.return_to_title_screen()
                        return
                    else:
                        messagebox.showinfo("Good job!","{} word(s) found! Way to go! :D".format(self.word_counter))
                        self.word_counter += 1
                        self.stop_timer()
                    self.chosen_word = self.challenge_words[self.word_counter - 1]
                    self.game_frame.place_forget()
                    self.game_screen_setup(self.difficulty, self.minutes_timer, self.seconds_timer)
                    self.render_new_input()
                else:
                    messagebox.showinfo("CONGRATS!", "YOU GOT IT RIGHT!")

                    if self.gamemode == "Classic":
                        self.update_word_bank()
                        self.save_user_info()
                        self.play_again()
                    else:
                        self.update_country_bank()
                        self.play_again()
            else:
                if self.tries > 1:
                    self.tries-=1
                    self.show_tries_text.set("Tries left -> {}".format(self.tries))
                    self.y_position += 60
                    self.render_new_input()
                else: 
                    self.losing_popup()
                    return
                    
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

        del word_bank[len(word_bank) - 1] #Delete the last line which is the "Challenge complete?" line

        #Iterate the word bank to update the secret word so it doesn't get chosen again
        for i in range(len(word_bank)):
            if word_bank[i].upper() == self.chosen_word:
                word_bank[i] += ";guessed"  
                
        
        with open(self.file_path, "w", encoding="utf-8") as f:
            for word in word_bank:
                f.write(word + "\n")
            if self.word_counter == 5:
                f.write("Challenge complete? Yes")
            else:
                f.write("Challenge complete? No")
                

    def update_country_bank(self):
        with open(self.file_path, "r", encoding = "utf-8") as f:
            lines = f.readlines()

        country_bank = [line.rstrip("\n") for line in lines]

        #Iterate the country bank to update it
        for i in range(len(country_bank)):
            if country_bank[i].upper() == self.chosen_country:
                country_bank[i] += ";guessed"

        with open(self.file_path, "w", encoding = "utf-8") as f:
            for country in country_bank:
                if country == country_bank[len(country_bank) - 1]:
                    f.write(country)
                else:
                    f.write(country + "\n")
                

    def save_user_info(self):
        """
        This function will update the user's info (what category & difficulty they chose, and nº of hints they have)
        in the "user.txt"
        """

        # Get the absolute path of the directory where the script is located & csonstruct the full path to the file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "user.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Category:{}\n" .format(self.category))
            f.write("Difficulty:{}".format(self.difficulty))


    def return_to_title_screen(self):
        if self.popup is not None:
            self.popup.destroy()

        self.game_frame.place_forget()
        self.save_user_info()

        if self.gamemode == "Classic":
            from game_settings_screen import ClassicModeSettings
            ClassicModeSettings(self.window)
        else:
            from game_settings_screen import FlagModeSettings
            FlagModeSettings(self.window)


    def play_again(self):
        """
        Keep playing the game (same category and difficulty chosen!).
        """
        if self.popup is not None:
            self.popup.destroy()

        self.game_frame.place_forget()
        Game(self.window, self.difficulty, self.category, self.gamemode)
    

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

        go_back_btn = Button(self.popup, text = "Return to \n Title Screen!",width= 12, height=3, font=("Arial", 12), command=lambda:self.return_to_title_screen())
        go_back_btn.place(x = 100, y = 150)

        play_again_btn = Button(self.popup, text="Play again!",width= 12, height=3, font=("Arial", 12), command=lambda:self.play_again())
        play_again_btn.place(x = 300, y = 150)
        