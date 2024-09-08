from tkinter import *
from tkinter import messagebox
from game import Game

class ClassicModeSettings:
    def __init__(self, window):
        self.window = window
        self.difficulty_selected = ""
        self.category_selected = ""
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

        self.guessed_words_frame = Frame(self.window, width=900, height=200, bg="lightgrey")
        self.guessed_words_frame.place(x = 50, y = 580)

        self.play_button = Button(self.window, text="Play!",bg="lightgrey", width=16, height=2, border=2, font=("Helvetica", 14), command=lambda:self.start_game())
        self.play_button.place(x = 405, y = 480)

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
        self.random_difficulty = Button(self.difficulty_frame, text="Random", width=9, height=1, border=2, bg="white", fg="black", font=("Helvetica", 16, "bold"), command=lambda:self.change_difficulty("Random"), state="disabled")

        self.easy_difficulty.place(x = 70, y = 60)
        self.medium_difficulty.place(x = 270, y = 60)
        self.hard_difficulty.place(x = 70, y = 160)
        self.challenge_difficulty.place(x = 270, y = 160)
        self.random_difficulty.place(x = 175, y = 240)

        self.show_difficulty = StringVar()
        self.show_difficulty.set("Difficulty selected -> {}".format(self.category_selected))
        self.show_difficulty_lbl = Label(self.difficulty_frame, bg="lightgrey", textvariable=self.show_difficulty, font=("Arial", 16))
        self.show_difficulty_lbl.place( x= 75, y = 310)

        self.coming_soon_lbl1 = Label(self.difficulty_frame, text="Coming Soon!", bg="lightgrey", font=("Arial", 10, "italic"))
        self.coming_soon_lbl2 = Label(self.difficulty_frame, text="Coming Soon!", bg="lightgrey", font=("Arial", 10, "italic"))
        self.coming_soon_lbl3 = Label(self.guessed_words_frame, text="Coming Soon!", bg="lightgrey", font=("Arial", 22, "bold"))

        self.coming_soon_lbl1.place(x = 290, y = 135)
        self.coming_soon_lbl2.place(x = 195, y = 215)
        self.coming_soon_lbl3.place(x = 350, y = 40)


    def change_category(self, new_category):
        self.category_selected = new_category
        self.show_category.set("Category selected -> {}".format(self.category_selected))


    def change_difficulty(self, new_difficulty):
        self.difficulty_selected = new_difficulty
        self.show_difficulty.set("Difficulty selected -> {}".format(self.difficulty_selected))

    
    def start_game(self):
        if self.category_selected == "" or self.difficulty_selected == "":
            messagebox.showwarning("Error","You need to select a category and a difficulty to start the game!")
        else:
            self.category_frame.place_forget()
            self.difficulty_frame.place_forget()
            self.guessed_words_frame.place_forget()
            self.play_button.place_forget()
            Game(self.window, self.difficulty_selected, self.category_selected)

