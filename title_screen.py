from tkinter import *
from tkinter import ttk
from game_screen import GameScreenApp

class TitleScreenApp:
    def __init__(self, window, difficulty_selected):
        self.window = window
        self.difficulty_selected = difficulty_selected #The difficulty is "Medium" by default
        self.setup_title_screen()
    
    def setup_title_screen(self):
        """
        This function contains all the title screen's GUI configurations
        """
        self.welcome_message = Label(self.window, bg ="grey", fg="white", text="Welcome to \n Guess The Word!", font=("Arial", 20))
        self.welcome_message.place(x = 380, y = 30)

        self.category_frame = PanedWindow(self.window, width=500, height=350, bg="lightgrey")
        self.category_frame.place(x = 200, y = 150)

        self.select_category_lbl = Label(self.category_frame, text = "Select a Category!", bg="lightgrey", font=("Arial", 16))
        self.select_category_lbl.place(x = 210, y = 0)


        self.animal_btn = Button(self.category_frame, text = "Animals", width=10, height=1, border=0, bg="grey", font=("Helvetica", 12), command= lambda:self.start_game("Animals"))
        self.jobs_btn = Button(self.category_frame, text = "Jobs", width=10, height=1, bg="grey",border=0, font=("Helvetica", 12), command= lambda:self.start_game("Jobs"))
        self.countries_btn = Button(self.category_frame, text = "Countries", width=10, height=1,border=0, bg="grey", font=("Helvetica", 12), command= lambda:self.start_game("Countries"))
        self.fruits_btn = Button(self.category_frame, text = "Fruits", width=10, height=1, bg="grey",border=0, font=("Helvetica", 12), command= lambda:self.start_game("Fruits"))
        
        self.animal_btn.grid(row = 0, column= 0, padx=100, pady=50)
        self.jobs_btn.grid(row=0, column=1, padx=100, pady=50)
        self.countries_btn.grid(row=1, column=0, padx=0, pady=40)
        self.fruits_btn.grid(row=1, column=1, padx=0, pady=40)


        self.difficulty_frame = PanedWindow(self.window, width= 602, height= 200, bg="lightgrey")
        self.difficulty_frame.place(x = 200, y = 420)

        self.select_difficulty_lbl = Label(self.difficulty_frame, text = "Select a Difficulty!", bg="lightgrey", font=("Arial", 16))
        self.select_difficulty_lbl.place(x = 210, y = 0)

        self.show_difficulty = StringVar()
        self.show_difficulty.set("Difficulty selected -> {}".format(self.difficulty_selected))
        self.show_difficulty_lbl = Label(self.difficulty_frame, bg="lightgrey", textvariable= self.show_difficulty, font=("Arial", 18))
        self.show_difficulty_lbl.place(x = 150, y = 40)

        self.easy_difficulty_btn = Button(self.difficulty_frame, text = "Easy", fg="white", bg="green", width=10, height= 2, border=0, font=("Helvetica",14), command= lambda:self.change_difficulty("Easy"))
        self.easy_difficulty_btn.place(x = 30, y = 100)

        self.medium_difficulty_btn = Button(self.difficulty_frame, text = "Medium", fg="black", bg="yellow", width=10, height= 2,border=0, font=("Helvetica",14), command= lambda:self.change_difficulty("Medium"))
        self.medium_difficulty_btn.place(x = 240, y = 100)

        self.hard_difficulty_btn = Button(self.difficulty_frame, text = "Hard", fg="black", bg="red", width=10, height= 2,border=0, font=("Helvetica",14), command= lambda:self.change_difficulty("Hard"))
        self.hard_difficulty_btn.place(x = 450, y = 100)

        self.easy_difficulty_info = Label(self.difficulty_frame, text = "(5 letters or less)", bg = "lightgrey", font=("Arial", 12, "italic"))
        self.easy_difficulty_info.place(x = 25, y = 158)

        self.easy_difficulty_info = Label(self.difficulty_frame, text = "(6 - 9 letters)", bg = "lightgrey", font=("Arial", 12, "italic"))
        self.easy_difficulty_info.place(x = 250, y = 158)

        self.easy_difficulty_info = Label(self.difficulty_frame, text = "(10+ letters)", bg = "lightgrey", font=("Arial", 12, "italic"))
        self.easy_difficulty_info.place(x = 460, y = 158)

    def change_difficulty(self, new_difficulty):
        match new_difficulty:
            case "Easy": self.difficulty_selected = "Easy"
            case "Medium": self.difficulty_selected= "Medium"
            case "Hard": self.difficulty_selected = "Hard"

        self.show_difficulty.set("Difficulty selected -> {}".format(self.difficulty_selected))

    def start_game(self, category):
        """
        This function will remove the title screen's GUI and setup
        the game screen's!
        """
        self.welcome_message.place_forget()
        self.category_frame.place_forget()
        self.difficulty_frame.place_forget()

        GameScreenApp(self.window, category, self.difficulty_selected)