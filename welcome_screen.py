from tkinter import *
from tkinter import ttk
from gamemode_screen import GamemodeScreenApp
from PIL import Image, ImageTk
import os

class WelcomeScreenApp:
    def __init__(self, window):
        self.window = window
        self.setup_welcome_screen()

    def setup_welcome_screen(self):
        """
        Contains all widgets in the Welcome Screen!
        """
        self.background_canvas = Canvas(self.window, width= 1000, height=700)
        self.background_canvas.place(x = 0, y = 0)

        background_img_path = os.path.join("images","main_screen_background.jpg")
        open_img = Image.open(background_img_path)
        resized_bg_image = open_img.resize((1000, 700))
        self.background_img = ImageTk.PhotoImage(resized_bg_image)
        self.background_canvas.create_image(500, 350, anchor=CENTER, image=self.background_img)
        
        self.welcome_frame = Frame(self.window, width=400, height=1000, bg="lightgrey")
        self.welcome_frame.place(x = 300, y = 0)

        self.welcome_message = Label(self.window, bg="lightgrey", fg="black", text = "Welcome to \n Guess The Word!", font=("Arial", 26))
        self.welcome_message.pack(pady=100)

        self.play_btn = Button(self.window, text = "Play!", width=14, height=2, border=2, bg = "lightgrey", font=("Helvetica", 14), command=lambda:self.choose_gamemode())
        self.play_btn.pack(pady=30)

        self.intructions_btn = Button(self.window, text = "How to Play?", width=14, height=2, border=2, bg = "lightgrey", font=("Helvetica", 14), command=lambda:self.setup_instructions_screen())
        self.intructions_btn.pack(pady=30)

    def choose_gamemode(self):
        """
        This function will remove all the Welcome Screen's widgets
        and setup all widgets from the "Choose the Gamemode" window
        """
        self.welcome_message.pack_forget()
        self.play_btn.pack_forget()
        self.intructions_btn.pack_forget()
        self.welcome_frame.place_forget()

        GamemodeScreenApp(self.window)


    def setup_instructions_screen(self):
        self.instructions_window = Toplevel()
        self.instructions_window.title("How to Play?")
        self.instructions_window.geometry("900x700")
        self.instructions_window.resizable(False, False)
        self.instructions_window.config(background="lightgrey")
        from main import AppConfig
        AppConfig.center_window(self.instructions_window, 900, 700)

        #-------> Instruction 1
        self.step1_lbl = Label(self.instructions_window, text="1.", font=("Arial", 24), bg="lightgrey")
        self.step1_lbl.place(x = 50, y = 30)

        img1_path = os.path.join("images","instruction1_img.png")
        img1 = Image.open(img1_path)
        img1 = img1.resize((230, 130))
        open_new_img = ImageTk.PhotoImage(img1)
        self.instruction1_img = Label(self.instructions_window, image=open_new_img)
        self.instruction1_img.image = open_new_img
        self.instruction1_img.place(x = 100, y = 30)

        self.instruction1_lbl = Label(self.instructions_window, 
        text="You have to guess the secret word by \ntypping out the letters! \nBe careful, you only have 5 tries!", font=("Arial", 14), bg="lightgrey")
        self.instruction1_lbl.place(x = 60, y = 165)

        arrow1_path = os.path.join("images","arrow1.png")
        arrow1 = Image.open(arrow1_path)
        arrow1 = arrow1.resize((80, 60))
        open_new_img = ImageTk.PhotoImage(arrow1)
        self.arrow1_img = Label(self.instructions_window, bg="lightgrey", image= open_new_img)
        self.arrow1_img.image = open_new_img
        self.arrow1_img.place(x = 400, y = 115)

        #-------> Instruction 2
        self.step2_lbl = Label(self.instructions_window, text="2.", font=("Arial", 24), bg="lightgrey")
        self.step2_lbl.place(x = 500, y = 30)

        img2_path = os.path.join("images","instruction2_img.png")
        img2 = Image.open(img2_path)
        img2 = img2.resize((230, 230))
        open_new_img = ImageTk.PhotoImage(img2)
        self.instruction2_img = Label(self.instructions_window, image=open_new_img)
        self.instruction2_img.image = open_new_img
        self.instruction2_img.place(x = 550, y = 30)

        self.instruction2_lbl = Label(self.instructions_window, 
        text="When you are sure about your guess,\n click on the 'Submit' button!", font=("Arial", 14), bg="lightgrey")
        self.instruction2_lbl.place(x = 500, y = 270)

        arrow2_path = os.path.join("images","arrow2.png")
        arrow2 = Image.open(arrow2_path)
        arrow2 = arrow2.resize((60, 80))
        open_new_img = ImageTk.PhotoImage(arrow2)
        self.arrow2_img = Label(self.instructions_window, bg="lightgrey", image= open_new_img)
        self.arrow2_img.image = open_new_img
        self.arrow2_img.place(x = 530, y = 330)

        #-------> Instruction 3
        self.step3 = Label(self.instructions_window, text="3.", font=("Arial", 24), bg = "lightgrey")
        self.step3.place(x = 500, y = 420)

        img3_1_path = os.path.join("images","green_box.png")
        img3_1 = Image.open(img3_1_path)
        img3_1 = img3_1.resize((50, 50))
        open_new_img = ImageTk.PhotoImage(img3_1)
        self.instruction3_1_img = Label(self.instructions_window, image=open_new_img, bg = "lightgrey")
        self.instruction3_1_img.image = open_new_img
        self.instruction3_1_img.place(x = 550, y = 450)

        self.instruction3_1_lbl = Label(self.instructions_window, 
        text="You got the letter and \n its position correct!", font=("Arial", 14), bg="lightgrey")
        self.instruction3_1_lbl.place(x = 610, y = 453)

        img3_2_path = os.path.join("images","yellow_box.png")
        img3_2 = Image.open(img3_2_path)
        img3_2 = img3_2.resize((50, 50))
        open_new_img = ImageTk.PhotoImage(img3_2)
        self.instruction3_2_img = Label(self.instructions_window, image=open_new_img, bg = "lightgrey")
        self.instruction3_2_img.image = open_new_img
        self.instruction3_2_img.place(x = 550, y = 520)

        self.instruction3_2_lbl = Label(self.instructions_window, 
        text="You got the letter right but \n it's in the wrong position!", font=("Arial", 14), bg="lightgrey")
        self.instruction3_2_lbl.place(x = 610, y = 523)

        img3_3_path = os.path.join("images","grey_box.png")
        img3_3 = Image.open(img3_3_path)
        img3_3 = img3_3.resize((50, 50))
        open_new_img = ImageTk.PhotoImage(img3_3)
        self.instruction3_3_img = Label(self.instructions_window, image=open_new_img, bg="lightgrey")
        self.instruction3_3_img.image = open_new_img
        self.instruction3_3_img.place(x = 550, y = 590)

        self.instruction_3_3_lbl = Label(self.instructions_window, 
        text="The letter isn't included in \n the secret word!", font=("Arial", 14), bg="lightgrey")
        self.instruction_3_3_lbl.place(x = 610, y = 593)

        arrow3_path = os.path.join("images","arrow3.png")
        arrow3 = Image.open(arrow3_path)
        arrow3 = arrow3.resize((80, 60))
        open_new_img = ImageTk.PhotoImage(arrow3)
        self.arrow3_img = Label(self.instructions_window, bg="lightgrey", image= open_new_img)
        self.arrow3_img.image = open_new_img
        self.arrow3_img.place(x = 400, y = 520)


        #-------> Instruction 4
        self.step4_lbl = Label(self.instructions_window, text="4.", font=("Arial", 24), bg = "lightgrey")
        self.step4_lbl.place(x = 50, y = 300)

        self.instruction4_lbl = Label(self.instructions_window, text="Try to guess ALL the words in the game \n HAVE FUN! :-)",
        font=("Arial",14), bg="lightgrey")
        self.instruction4_lbl.place(x = 50, y = 530)