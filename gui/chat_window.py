import customtkinter as ctk

from chatbot import get_response

from memory.memory import (
    load_history,
    save_message,
    export_history,
    clear_history,
    load_profile
)

from voice.speech import speak
from voice.listen import listen
from utilities.task_manager import run_in_background
from config import APP_NAME, VERSION

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ChatWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title(
            "Smart Assistant AI"
        )

        self.geometry(
            "1100x700"
        )

        self.last_response = ""

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_app
        )
        self.create_sidebar()

        self.create_chat_area()

        self.load_previous_messages()



    # -----------------------------
    # SIDEBAR
    # -----------------------------

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=220
        )

        self.sidebar.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )


        title = ctk.CTkLabel(
            self.sidebar,
            text=f"🤖 {APP_NAME}",
            font=("Arial",22)
        )

        version_label = ctk.CTkLabel(
            self.sidebar,
            text=f"Version {VERSION}",
            font=("Arial", 12)
        )

        version_label.pack(
            pady=5
        )

        title.pack(
            pady=20
        )


        self.user_label = ctk.CTkLabel(
            self.sidebar,
            text="",
            font=("Arial",16)
        )

        self.user_label.pack(
            pady=20
        )

        self.status_label = ctk.CTkLabel(
            self.sidebar,
            text="Status: Ready",
            font=("Arial", 14)
        )

        self.status_label.pack(
            pady=10
        )


        self.update_profile_display()



        self.theme_button = ctk.CTkButton(
            self.sidebar,
            text="🌙 Toggle Theme",
            command=self.toggle_theme
        )

        self.theme_button.pack(
            pady=10,
            padx=20
        )


        self.export_button = ctk.CTkButton(
            self.sidebar,
            text="📄 Export Chat",
            command=self.export_chat
        )

        self.export_button.pack(
            pady=10,
            padx=20
        )


        self.clear_button = ctk.CTkButton(
            self.sidebar,
            text="🗑 Clear History",
            command=self.clear_chat
        )

        self.clear_button.pack(
            pady=10,
            padx=20
        )



    # -----------------------------
    # CHAT AREA
    # -----------------------------

    def create_chat_area(self):

        self.chat_frame = ctk.CTkFrame(
            self
        )

        self.chat_frame.pack(
            side="right",
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )


        self.chatbox = ctk.CTkTextbox(
            self.chat_frame,
            wrap="word",
            font=("Arial",15),
            corner_radius=15
        )

        self.chatbox.pack(
            expand=True,
            fill="both",
            padx=15,
            pady=15
        )



        bottom = ctk.CTkFrame(
            self.chat_frame
        )

        bottom.pack(
            fill="x"
        )



        self.entry = ctk.CTkEntry(
            bottom,
            placeholder_text="Ask something..."
        )

        self.entry.pack(
            side="left",
            expand=True,
            fill="x",
            padx=10
        )


        self.entry.bind(
            "<Return>",
            self.send_message
        )



        self.send_button = ctk.CTkButton(
            bottom,
            text="Send",
            command=self.send_message
        )

        self.send_button.pack(
            side="right",
            padx=5
        )



        self.voice_button = ctk.CTkButton(
            bottom,
            text="🎤",
            command=self.voice_input
        )

        self.voice_button.pack(
            side="right",
            padx=5
        )



    # -----------------------------
    # MEMORY DISPLAY
    # -----------------------------

    def load_previous_messages(self):

        history = load_history()


        for item in history:

            self.chatbox.insert(
                "end",
                f"{item['sender']}: {item['message']}\n\n"
            )



    def update_profile_display(self):

        profile = load_profile()

        name = profile.get(
            "name",
            "Guest"
        )


        self.user_label.configure(
            text=f"User:\n{name}"
        )



    # -----------------------------
    # CHAT FUNCTIONS
    # -----------------------------

    def add_message(
            self,
            sender,
            message
    ):

        import datetime

        timestamp = datetime.datetime.now().strftime(
            "%H:%M"
        )

        if sender == "You":

            prefix = f"You  [{timestamp}]"

        else:

            prefix = f"🤖 Smart AI  [{timestamp}]"

        self.chatbox.insert(
            "end",
            f"{prefix}\n"
            f"{message}\n\n"
        )

        self.chatbox.see(
            "end"
        )

        self.chatbox.insert(
            "end",
            f"{sender}: {message}\n\n"
        )


        self.chatbox.see(
            "end"
        )



    def send_message(
            self,
            event=None
    ):

        message = self.entry.get().strip()


        if not message:

            return


        self.entry.delete(
            0,
            "end"
        )


        self.add_message(
            "You",
            message
        )


        save_message(
            "You",
            message
        )

        self.status_label.configure(
            text="Status: Thinking..."
        )

        self.add_message(
            "Bot",
            "Thinking..."
        )


        run_in_background(
            lambda: get_response(message),
            self.display_response
        )



    def display_response(
            self,
            response
    ):

        self.after(
            0,
            lambda: self.finish_response(response)
        )



    def finish_response(
            self,
            response
    ):

        self.chatbox.delete(
            "end-3l",
            "end-2l"
        )


        self.add_message(
            "Bot",
            response
        )


        save_message(
            "Bot",
            response
        )


        self.last_response = response

        self.status_label.configure(
            text="Status: Speaking..."
        )

        speak(response)

        self.status_label.configure(
            text="Status: Ready"
        )


        self.update_profile_display()



    # -----------------------------
    # VOICE
    # -----------------------------

    def voice_input(self):

        text = listen()


        self.entry.insert(
            0,
            text
        )


        self.send_message()



    # -----------------------------
    # BUTTON FUNCTIONS
    # -----------------------------

    def toggle_theme(self):

        current = ctk.get_appearance_mode()


        if current == "Dark":

            ctk.set_appearance_mode(
                "Light"
            )

        else:

            ctk.set_appearance_mode(
                "Dark"
            )



    def export_chat(self):

        export_history()



    def clear_chat(self):

        clear_history()


        self.chatbox.delete(
            "1.0",
            "end"
        )

    def close_app(self):

        print(
            "Smart Assistant shutting down..."
        )
    # -----------------------------
    # CLOSE APPLICATION
    # -----------------------------
    def close_app(self):

        print(
            "Smart Assistant shutting down..."
        )

        self.destroy()


    # -----------------------------
    # START APPLICATION
    # -----------------------------

    def run(self):

        self.mainloop()