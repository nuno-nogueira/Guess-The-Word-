from tkinter import *
from tkinter import messagebox
from game import Game
import os

class ClassicModeSettings:
    def __init__(self, window, difficulty, category):
        self.window = window
        self.difficulty_selected = difficulty
        self.category_selected = category
        self.word_bank_progression()
        self.setup_game_settings_screen()


    def setup_game_settings_screen(self):
        """
        This function has all the game setting's widgets!
        """
        #----> Frames
        self.category_frame = Frame(self.window, width=450, height=400, bg="lightgrey")
        self.category_frame.place(x = 30, y = 50)

        self.difficulty_frame = Frame(self.window, width=450, height=400, bg="lightgrey")
        self.difficulty_frame.place(x = 520, y = 50)

        self.word_bank_frame = Frame(self.window, width=950, height=250, bg="lightgrey")
        self.word_bank_frame.place(x = 25, y = 520)

        self.play_button = Button(self.window, text="Play!",bg="lightgrey", width=16, height=2, border=2, font=("Helvetica", 14), command=lambda:self.start_game())
        self.play_button.place(x = 405, y = 455)

        #----> Category Frame Widgets
        self.category_title = Label(self.category_frame, text="Categories", bg="lightgrey", font=("Arial", 18, "bold"))
        self.category_title.place(x = 160, y = 10)

        self.animal_category = Button(self.category_frame, text="Animals", width=9, height=1, border=2, bg="lightgrey", font=("Helvetica", 16), command=lambda:self.change_category("Animals"))
        self.job_category = Button(self.category_frame, text="Jobs", width=9, height=1, border=2, bg="lightgrey", font=("Helvetica", 16), command=lambda:self.change_category("Jobs"))
        self.colors_category = Button(self.category_frame, text="Colors", width=9, height=1, border=2, bg="lightgrey", font=("Helvetica", 16), command=lambda:self.change_category("Colors"))
        self.fruits_category = Button(self.category_frame, text="Fruits", width=9, height=1, border=2, bg="lightgrey", font=("Helvetica", 16), command=lambda:self.change_category("Fruits"))

        self.animal_category.place(x = 70, y = 100)
        self.job_category.place(x = 270, y = 100)
        self.colors_category.place(x = 70, y = 200)
        self.fruits_category.place(x = 270, y = 200)

        self.show_category = StringVar()
        self.show_category.set("Category selected -> {}".format(self.category_selected))
        self.show_category_lbl = Label(self.category_frame, bg="lightgrey", textvariable=self.show_category, font=("Arial", 16))
        self.show_category_lbl.place( x= 80, y = 310)

        #----> Difficulty Frame widgets
        self.difficulty_title = Label(self.difficulty_frame, text="Difficulties", bg="lightgrey", font=("Arial", 18, "bold"))
        self.difficulty_title.place(x = 160, y = 10)

        self.easy_difficulty = Button(self.difficulty_frame, text="Easy", width=9, height=1, border=2, bg="#84f069", fg="white", font=("Helvetica", 16, "bold"), command=lambda:self.change_difficulty("Easy"))
        self.medium_difficulty = Button(self.difficulty_frame, text="Medium", width=9, height=1, border=2, bg="#e0e342", fg="white", font=("Helvetica", 16, "bold"), command=lambda:self.change_difficulty("Medium"))
        self.hard_difficulty = Button(self.difficulty_frame, text="Hard", width=9, height=1, border=2, bg="#de1c07", fg="white", font=("Helvetica", 16, "bold"), command=lambda:self.change_difficulty("Hard"))
        self.challenge_difficulty = Button(self.difficulty_frame, text="Challenge", width=9, height=1, border=2, bg="#751207", fg="black", font=("Helvetica", 16, "bold"), command=lambda:self.change_difficulty("Challenge"), state="disabled")
        self.random_difficulty = Button(self.difficulty_frame, text="Random", width=9, height=1, border=2, bg="white", fg="black", font=("Helvetica", 16, "bold"), command=lambda:self.change_difficulty("Random"))

        self.easy_difficulty.place(x = 70, y = 60)
        self.medium_difficulty.place(x = 270, y = 60)
        self.hard_difficulty.place(x = 70, y = 160)
        self.challenge_difficulty.place(x = 270, y = 160)
        self.random_difficulty.place(x = 175, y = 240)

        self.show_difficulty = StringVar()
        self.show_difficulty.set("Difficulty selected -> {}".format(self.difficulty_selected))
        self.show_difficulty_lbl = Label(self.difficulty_frame, bg="lightgrey", textvariable=self.show_difficulty, font=("Arial", 16))
        self.show_difficulty_lbl.place( x= 75, y = 310)

        self.coming_soon_lbl1 = Label(self.difficulty_frame, text="Coming Soon!", bg="lightgrey", font=("Arial", 10, "italic"))

        self.coming_soon_lbl1.place(x = 290, y = 135)

        #--->Word Bank Progression Frame widgets
        self.word_bank_frame_title = Label(self.word_bank_frame, text = "Word Bank Progression", font=("Arial", 22,"bold"), bg="lightgrey")
        self.word_bank_frame_title.place(x = 280, y = 10)

        self.total_words_lbl = Label(self.word_bank_frame, text="Total Words \nfound:\n{}/{}".format(self.total_words_found, self.total_words), font=("Arial", 18, "bold"), bg="lightgrey")
        self.total_words_lbl.place(x = 375, y = 62)

        self.easy_words_lbl1 = Label(self.word_bank_frame, text="Easy", font=("Arial", 18, "bold"), fg="white", bg="#84f069")
        self.easy_words_lbl2 = Label(self.word_bank_frame, text="words found:\n{}/{}" .format(self.easy_words_found, self.easy_words), bg="lightgrey", font=("Arial", 16))

        self.easy_words_lbl1.place(x = 40, y = 70)
        self.easy_words_lbl2.place(x = 10, y = 105)

        self.medium_words_lbl1 = Label(self.word_bank_frame, text="Medium", font=("Arial", 18, "bold"), fg = "white", bg="#e0e342")
        self.medium_words_lbl2 = Label(self.word_bank_frame, text="words found:\n{}/{}" .format(self.medium_words_found, self.medium_words), bg="lightgrey", font=("Arial", 16))

        self.medium_words_lbl1.place(x = 190, y = 70)
        self.medium_words_lbl2.place(x = 180, y = 105)

        self.hard_words_lbl1 = Label(self.word_bank_frame, text="Hard", font=("Arial", 18, "bold"), fg="white", bg="#de1c07")
        self.hard_words_lbl2 = Label(self.word_bank_frame, text="words found:\n{}/{}" .format(self.hard_words_found, self.hard_words), bg="lightgrey", font=("Arial", 16))
        
        self.hard_words_lbl1.place(x = 620, y = 70)
        self.hard_words_lbl2.place(x = 590, y = 105)

        self.challenge_lbl1 = Label(self.word_bank_frame, text="Challenge", font=("Arial", 18, "bold"), fg="white", bg="#751207")
        self.challenge_lbl2 = Label(self.word_bank_frame, text="Coming Soon!", bg="lightgrey", font=("Arial", 14, "italic"))

        self.challenge_lbl1.place(x = 770, y = 70)
        self.challenge_lbl2.place(x = 765, y = 110)

        self.reset_word_bank_btn = Button(self.word_bank_frame, text="Reset Word Bank", font=("Arial", 14), border=2 , width=15, height=1, command=lambda: self.reset_word_bank())
        self.reset_word_bank_btn.place(x = 750, y = 10)

    def change_category(self, new_category):
        self.category_selected = new_category
        self.show_category.set("Category selected -> {}".format(self.category_selected))


    def change_difficulty(self, new_difficulty):
        self.difficulty_selected = new_difficulty
        self.show_difficulty.set("Difficulty selected -> {}".format(self.difficulty_selected))


    def word_bank_progression(self):
        """
        This function has several functionalities which mostly tells the user their progression on the game
        It mostly counts the total words the user found and how many words there are still to find for each
        category
        """
        self.words_list = []
        self.total_words = 0
        self.total_words_found = 0
        self.easy_words = 0
        self.easy_words_found = 0
        self.medium_words = 0
        self.medium_words_found = 0
        self.hard_words = 0
        self.hard_words_found = 0
        self.challenge_completed = ""

        base_dir = os.path.dirname(os.path.abspath(__file__))
        list_of_files = ["animals.txt","fruits.txt","colors.txt","jobs.txt"]

        #--> Add all the words to the "self.words_list" array
        for file in list_of_files:
            file_path = os.path.join(base_dir, "Word Bank", file)

            with open(file_path, "r", encoding="utf-8") as f:
                words = f.readlines()

            for word in words:
                self.words_list.append(word)

        self.total_words = len(self.words_list)

        word_length = 0
        #--> Count all the words found by the user!
        for word in self.words_list:
            if ";" in word:
                word_length = len(word[0:word.find(";") - 1])
            else:
                word_length = len(word)
            if ";guessed" in word:
                self.total_words_found += 1
            if word_length <= 5:
                self.easy_words += 1
                if ";guessed" in word:
                    self.easy_words_found += 1
            if word_length >= 6 and word_length <= 9:
                self.medium_words += 1
                if ";guessed" in word:
                    self.medium_words_found += 1
            if word_length >= 10:
                self.hard_words += 1
                if ";guessed" in word:
                    self.hard_words_found += 1      
            


        print("Easy words -> {}".format(self.easy_words))
        print("Easy words found -> {}".format(self.easy_words_found))
        print("Medium words -> {}".format(self.medium_words))
        print("Medium words found -> {}".format(self.medium_words_found))
        print("Hard words -> {}".format(self.hard_words))
        print("Hard words found -> {}".format(self.hard_words_found))


    def reset_word_bank(self):
        """
        This function will let the user reset the "Word Bank"
        By doing so, all words that were previously found will be reset and can be picked again
        to be guessed again
        This basically resets all the progression the user made
        """

        answer = messagebox.askquestion("Reset Word Bank", 
                               "Are you sure? If so, all the progression you've made will be reset and all the words you found can be selected again for you to guess!")


        if answer == "yes":
            self.words_list = []

            base_dir = os.path.dirname(os.path.abspath(__file__))
            list_of_files = ["animals.txt","fruits.txt","colors.txt","jobs.txt"]
            change_files = [] #This array will store the last word of each file so when the word bank is being updated, the words will go to their respective files

            #--> Add all the words to the "self.words_list" array
            for file in list_of_files:
                file_path = os.path.join(base_dir, "Word Bank", file)

                with open(file_path, "r", encoding="utf-8") as f:
                    words = f.readlines()

                for i in range (len(words)):
                    if ";guessed" in words[i]:
                        words[i] = words[i][0:words[i].find(";")]
                        words[i] += "\n"
                    if words[i] == words[len(words) - 1]:
                        change_files.append(words[i])
                    self.words_list.append(words[i])

            print(change_files)

            word_bank = []

            # #Update the word bank
            for file in list_of_files:
                if file == list_of_files[0]:
                    word_bank = self.words_list[0:self.words_list.index(change_files[0]) + 1]
                elif file == list_of_files[1]:
                    word_bank = self.words_list[self.words_list.index(change_files[0]) + 1:self.words_list.index(change_files[1]) + 1]
                elif file == list_of_files[2]:
                    word_bank = self.words_list[self.words_list.index(change_files[1]) + 1:self.words_list.index(change_files[2]) + 1]
                elif file == list_of_files[3]:
                    word_bank = self.words_list[self.words_list.index(change_files[2]) + 1:self.words_list.index(change_files[3]) + 1]

                print(word_bank)
                print(len(word_bank))
                print("\n---------------------------\n")

            
                file_path = os.path.join(base_dir, "Word Bank", file)
                with open(file_path, "w", encoding="utf-8") as f:
                    for word in word_bank:         
                        f.write(word)
                word_bank.clear()

            self.word_bank_frame.place_forget()
            self.word_bank_progression()
            self.setup_game_settings_screen()
            messagebox.showinfo("Word Bank Reset", "The Word Bank has been sucessfully reset!")
        else:
            return

    def start_game(self):
        if self.category_selected == "" or self.difficulty_selected == "":
            messagebox.showwarning("Error","You need to select a category and a difficulty to start the game!")
        else:
            self.category_frame.place_forget()
            self.difficulty_frame.place_forget()
            self.word_bank_frame.place_forget()
            self.play_button.place_forget()
            Game(self.window, self.difficulty_selected, self.category_selected)


