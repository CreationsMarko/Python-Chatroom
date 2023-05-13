from ..client import Client
from tkinter import *
from tkinter import scrolledtext
from functools import partial
from PIL import Image, ImageTk

class ClientGUI(Client):
    # def __init__(self, host, port):
    #     self.host = "localhost"
    #     self.port = 7077
    #     self.client = ClientGUI("localhost",7077)

    # def connect(self):
    #     self.client.connect("localhost", 7077)
    
    def printDetails(self, usernameEntry, tkWindow):
        usernameText = usernameEntry.get()
        self.set_username(usernameText)
        self.openNewWindow(tkWindow)

    def openNewWindow(self, tkWindow):
        newWindow = Toplevel(tkWindow)
        newWindow.geometry("800x800")
        newWindow.title('Chatroom')

        image = Image.open("design/Bg-chatroom.png")
        photo = ImageTk.PhotoImage(image)
        bg_label = Label(newWindow, image=photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        newWindow.configure(bg="lightgrey")

        chat_label = Label(newWindow, text="Chat: ", bg="lightgray")
        chat_label.config(font=("Arial", 12))
        chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(newWindow)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        msg_label = Label(newWindow, text="Message: ", bg="lightgray")
        msg_label.config(font=("Arial", 12))
        msg_label.pack(padx=20, pady=5)

        input_area = Text(newWindow, height=3)
        input_area.pack(padx=20, pady=5)

        send_button = Button(newWindow, text="Send", command=lambda: self.write(input_area))
        send_button.config(font=("Arial", 12))
        send_button.pack(padx=20, pady=5)

        tkWindow.withdraw()

        newWindow.mainloop()

        tkWindow.destroy()

    def write(self, input_area):
        message = str(input_area.get("1.0", "end"))
        self.send_message(message)
        input_area.delete("1.0", END)

    def start(self):
        print('W.I.P.')
        tkWindow = Tk()
        tkWindow.geometry('420x420')
        tkWindow.title('Chatroom Login')

        image = Image.open("design/tekstura.png")
        photo = ImageTk.PhotoImage(image)
        bg_label = Label(tkWindow, image=photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        usernameLabel = Label(tkWindow, text="Enter Your name")
        usernameEntry = Entry(tkWindow)

        printDetailsCallable = partial(self.printDetails, usernameEntry, tkWindow)

        submitButton = Button(tkWindow, text="Submit", command=printDetailsCallable)

        usernameLabel.place(relx=0.5, rely=0.3, anchor="center")
        usernameEntry.place(relx=0.5, rely=0.6, anchor="center")
        submitButton.place(relx=0.5, rely=0.9, anchor="center")

        tkWindow.mainloop()

    def process_message(self, username: str, message: str):
        self.text_area.config(state="normal")
        self.text_area.insert(END, f"{username}: {message}\n")
        self.text_area.config(state="disabled")
        self.update_display()

    def join_message(self, username: str):
        self.text_area.config(state="normal")
        self.text_area.insert(END, f"{username} has joined the chatroom.\n")
        self.text_area.config(state="disabled")
        self.update_display()

    def leave_message(self, username: str):
        self.text_area.config(state="normal")
        self.text_area.insert(END, f"{username} has left the chatroom.\n")
        self.text_area.config(state="disabled")
        self.update_display()

    def send_message(self, message: str):
        try:
            self.socket.send(bytes(message, "utf8"))
        except ConnectionResetError:
            print("Disconnected from the server.")


# from ..client import Client
# from tkinter import *
# from tkinter import scrolledtext
# from functools import partial
# from PIL import Image, ImageTk

# class ClientGUI(Client):
    
#     def printDetails(self, usernameEntry, tkWindow):
#         usernameText = usernameEntry.get()
#         self.set_username(usernameText)
#         self.openNewWindow(tkWindow)

#     def openNewWindow(self, tkWindow):
#         newWindow = Toplevel(tkWindow)
#         newWindow.geometry("800x800")
#         newWindow.title('Chatroom')

#         image = Image.open("design/Bg-chatroom.png")
#         photo = ImageTk.PhotoImage(image)
#         bg_label = Label(newWindow, image=photo)
#         bg_label.place(x=0, y=0, relwidth=1, relheight=1)

#         newWindow.configure(bg="lightgrey")

#         chat_label = Label(newWindow, text="Chat: ", bg="lightgray")
#         chat_label.config(font=("Arial", 12))
#         chat_label.pack(padx=20, pady=5)

#         self.text_area = scrolledtext.ScrolledText(newWindow)
#         self.text_area.pack(padx=20, pady=5)
#         self.text_area.config(state="disabled")

#         msg_label = Label(newWindow, text="Message: ", bg="lightgray")
#         msg_label.config(font=("Arial", 12))
#         msg_label.pack(padx=20, pady=5)

#         input_area = Text(newWindow, height=3)
#         input_area.pack(padx=20, pady=5)

# #        send_button = Button(newWindow, text="Send", command=lambda: self.write(input_area))
#         send_button = Button(newWindow, text="Send", command=lambda: self.write(input_area, self.text_area))
#         send_button.config(font=("Arial", 12))
#         send_button.pack(padx=20, pady=5)

#         tkWindow.withdraw()

#         newWindow.mainloop()

#         tkWindow.destroy()

#     def write( self, input_area, text_area):
#         message = str(input_area.get("1.0", "end"))
#         self.send_message(message)
#         input_area.delete("1.0", END)
#         # self.text_area.config(state="normal")
#         # self.text_area.insert(END, message)
#         # self.text_area.config(state="disabled")

#     def start(self):
#         print('W.I.P.')
#         tkWindow = Tk()
#         tkWindow.geometry('420x420')
#         tkWindow.title('Chatroom Login')

#         image = Image.open("design/tekstura.png")
#         photo = ImageTk.PhotoImage(image)
#         bg_label = Label(tkWindow, image=photo)
#         bg_label.place(x=0, y=0, relwidth=1, relheight=1)

#         usernameLabel = Label(tkWindow, text="Enter Your name")
#         usernameEntry = Entry(tkWindow)

#         printDetailsCallable = partial(self.printDetails, usernameEntry, tkWindow)

#         submitButton = Button(tkWindow, text="Submit", command=printDetailsCallable)

#         usernameLabel.place(relx=0.5, rely=0.3, anchor="center")
#         usernameEntry.place(relx=0.5, rely=0.6, anchor="center")
#         submitButton.place(relx=0.5, rely=0.9, anchor="center")

#         tkWindow.mainloop()

#     def process_message(self, message: str):
#         print(message)
#         self.text_area.config(state="normal")
#         self.text_area.insert(END, message)
#         self.text_area.config(state="disabled")
