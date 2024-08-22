from tkinter import *
from tkinter import ttk
from game_screen import GameScreenApp

class TitleScreenApp:
    def __init__(self, window):
        self.window = window
        self.setup_title_screen()
    
    def setup_title_screen(self):
        """
        This function contains all the title screen's GUI configurations
        """
        self.welcome_message = Label(self.window, bg ="grey", fg="white", text="Welcome to \n Guess The Word!", font=("Arial", 20))
        self.welcome_message.place(x = 380, y = 50)

        self.category_frame = PanedWindow(self.window, width=500, height=300, bg="lightgrey")
        self.category_frame.place(x = 200, y = 150)

        self.animal_btn = Button(self.category_frame, text = "Animals", width=10, height=1, bg="grey", font=("Helvetica", 12), command= lambda:self.start_game("Animals"))
        self.jobs_btn = Button(self.category_frame, text = "Jobs", width=10, height=1, bg="grey", font=("Helvetica", 12), command= lambda:self.start_game("Jobs"))
        self.countries_btn = Button(self.category_frame, text = "Countries", width=10, height=1, bg="grey", font=("Helvetica", 12), command= lambda:self.start_game("Countries"))
        self.fruits_btn = Button(self.category_frame, text = "Fruits", width=10, height=1, bg="grey", font=("Helvetica", 12), command= lambda:self.start_game("Fruits"))
        
        self.animal_btn.grid(row = 0, column= 0, padx=100, pady=40)
        self.jobs_btn.grid(row=0, column=1, padx=100, pady=40)
        self.countries_btn.grid(row=1, column=0, padx=0, pady=40)
        self.fruits_btn.grid(row=1, column=1, padx=0, pady=40)

    def start_game(self, category):
        """
        This function will remove the title screen's GUI and setup
        the game screen's!
        """
        self.welcome_message.place_forget()
        self.category_frame.place_forget()

        GameScreenApp(self.window, category)