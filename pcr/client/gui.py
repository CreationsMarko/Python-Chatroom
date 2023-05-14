from ..client import Client
from tkinter import scrolledtext, Tk, Frame, Label, Entry, Button, Text
from threading import Thread
from tkinter import *
from PIL import Image, ImageTk


class ClientGUI(Client):

    def start(self):

        self.root = Tk()

        self.background_image = ImageTk.PhotoImage(Image.open("assets/texture.png"))
        bg_label = Label(self.root, image=self.background_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.root.geometry('420x280')
        self.root.title('Chatroom Login')

        init_frame = self.init_window()
        init_frame.pack(side = "top", fill = "both", expand = True)

        self.root.protocol("WM_DELETE_WINDOW", self.leave)
        self.root.mainloop()

    def init_window(self):

        window = Frame(self.root)

        bg_label = Label(window, image=self.background_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        usernameLabel = Label(window, text="Enter Your name")
        username_input = Entry(window)

        submitButton = Button(window, text="Submit", command=lambda: self.process_init(username_input, window))

        usernameLabel.place(relx=0.5, rely=0.3, anchor="center")
        username_input.place(relx=0.5, rely=0.6, anchor="center")
        submitButton.place(relx=0.5, rely=0.9, anchor="center")

        return window

    def main_window(self):

        window = Frame(self.root)

        bg_label = Label(window, image=self.background_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        chat_label = Label(window, text="Chat: ", bg="lightgray")
        chat_label.config(font=("Arial", 12))
        chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(window)
        self.text_area.pack(padx=20, pady=5)

        msg_label = Label(window, text="Message: ", bg="lightgray")
        msg_label.config(font=("Arial", 12))
        msg_label.pack(padx=20, pady=5)

        self.input_area = Text(window, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.root.bind('<Return>', self.write_message)
        send_button = Button(window, text="Send", command=lambda: self.write_message())
        send_button.config(font=("Arial", 12))
        send_button.pack(padx=20, pady=5)

        return window


    def clear_frame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def process_init(self, username_input, old_frame):

        username = username_input.get()
        self.set_username(username)

        self.root.geometry("520x600")
        self.root.title('Chatroom')

        self.clear_frame(old_frame)
        main_frame = self.main_window()
        main_frame.pack(side = "top", fill = "both", expand = True)

        main_frame.tkraise()


    def process_message(self, username: str, message: str):
        self.print_message(f"{username}: {message}")

    def join_message(self, username: str):
        self.print_message(f"{username} joined the chatroom.")

    def leave_message(self, username: str):
        self.print_message(f"{username} left the chatroom.")

    def print_message(self, message: str):
        self.text_area.insert(END, message.strip().rstrip()+'\n')

    def write_message(self, *_):
        raw_message = self.input_area.get("1.0", "end")
        message = str(raw_message).strip().rstrip()
        self.send_message(message)
        self.input_area.delete("1.0", "end")
    
    def leave(self):
        super().leave()
        self.root.destroy()
