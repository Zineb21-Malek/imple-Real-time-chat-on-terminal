"""
Created on Sat Dec  3 08:08:09 2022

@author: DELL
"""

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Initialize connection
nickname = ""
clt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clt.connect(('127.0.0.1', 55555))

# GUI class
class ChatGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat Client")

        self.chat_label = tk.Label(self.root, text="Chat:")
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(self.root)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state=tk.DISABLED)

        self.msg_label = tk.Label(self.root, text="Message:")
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tk.Text(self.root, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tk.Button(self.root, text="Send", command=self.write)
        self.send_button.pack(padx=20, pady=5)

        self.nickname_label = tk.Label(self.root, text="Enter your nickname:")
        self.nickname_label.pack(padx=20, pady=5)

        self.nickname_entry = tk.Entry(self.root)
        self.nickname_entry.pack(padx=20, pady=5)

        self.set_nickname_button = tk.Button(self.root, text="Set Nickname", command=self.set_nickname)
        self.set_nickname_button.pack(padx=20, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def set_nickname(self):
        global nickname
        nickname = self.nickname_entry.get()
        if nickname:
            self.nickname_label.pack_forget()
            self.nickname_entry.pack_forget()
            self.set_nickname_button.pack_forget()
            self.receive_thread = threading.Thread(target=self.receive)
            self.receive_thread.daemon = True
            self.receive_thread.start()
        else:
            messagebox.showerror("Error", "Please enter a nickname")

    def receive(self):
        while True:
            try:
                msg = clt.recv(1024).decode('ascii')
                if msg == 'nickname':
                    clt.send(nickname.encode('ascii'))
                else:
                    self.text_area.config(state=tk.NORMAL)
                    self.text_area.insert('end', msg + '\n')
                    self.text_area.yview('end')
                    self.text_area.config(state=tk.DISABLED)
            except:
                messagebox.showerror("Error", "An error occurred!")
                clt.close()
                break

    def write(self):
        msg = self.input_area.get("1.0", 'end').strip()
        self.input_area.delete("1.0", 'end')
        if msg:
            full_msg = f'{nickname}: {msg}'
            clt.send(full_msg.encode('ascii'))
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert('end', full_msg + '\n')
            self.text_area.yview('end')
            self.text_area.config(state=tk.DISABLED)

    def on_closing(self):
        clt.close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

# Start GUI in the main thread
if __name__ == "__main__":
    chat_gui = ChatGUI()
    chat_gui.run()
