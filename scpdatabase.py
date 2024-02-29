import tkinter as tk
from tkinter import messagebox
import openai

class SCPDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title('SCP Foundation Secure Database Terminal')
        self.command_history = []
        self.command_history_index = -1
        self.chat_history = []  # Initialize chat history for maintaining context

        # Main frame with dark background
        self.main_frame = tk.Frame(root, padx=10, pady=10, bg='#1c1c1c')
        self.main_frame.pack(expand=True, fill='both')

        # SCP-themed text display setup with dark background and bright green text
        self.text = tk.Text(self.main_frame, height=20, width=100, wrap='word', bg='#1c1c1c', fg='#00ff00', insertbackground='white')
        self.text.pack(expand=True, fill='both', pady=(0, 10))
        self.display_data("Welcome, Operator. You've accessed the secure terminal of the SCP Foundation's database. "
                          "Your inquiries into our catalog of anomalies are paramount. "
                          "Proceed with caution. What information do you seek today?")

        # User input area with thematic adjustments
        self.message_entry = tk.Entry(self.main_frame, width=100, bg='#2d2d2d', fg='#00ff00', insertbackground='white')
        self.message_entry.pack(fill='x', pady=(0, 10))
        self.message_entry.bind("<Return>", self.send_message_event)
        self.message_entry.bind("<Up>", self.prev_command)
        self.message_entry.bind("<Down>", self.next_command)

        # Thematic button for message sending
        self.send_message_button = tk.Button(self.main_frame, text="Send Query", command=self.send_message, bg='#333333', fg='#00ff00')
        self.send_message_button.pack()

        # API key input area styled to match the theme
        self.api_key_frame = tk.Frame(root, padx=10, pady=10, bg='#1c1c1c')
        self.api_key_frame.pack(side=tk.BOTTOM, fill='x')
        self.api_key_entry = tk.Entry(self.api_key_frame, width=100, show="*", bg='#2d2d2d', fg='#00ff00', insertbackground='white')
        self.api_key_entry.pack(side=tk.LEFT, expand=True, fill='x')
        self.set_api_key_button = tk.Button(self.api_key_frame, text="Authorize", command=self.set_api_key, bg='#333333', fg='#00ff00')
        self.set_api_key_button.pack(side=tk.RIGHT)

        self.send_message_button.config(state=tk.DISABLED)

    def send_message_event(self, event=None):
        self.send_message()

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            self.command_history.append(message)
            self.command_history_index = len(self.command_history)
            response = self.get_scp_response(message)
            self.display_data(f"Operator Inquiry: {message}\nDatabase Response: {response}")
            self.message_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Transmission Error", "Input is void. Please articulate your inquiry.")

    def prev_command(self, event):
        if self.command_history and self.command_history_index > 0:
            self.command_history_index -= 1
            self.message_entry.delete(0, tk.END)
            self.message_entry.insert(0, self.command_history[self.command_history_index])

    def next_command(self, event):
        if self.command_history_index < len(self.command_history) - 1:
            self.command_history_index += 1
            self.message_entry.delete(0, tk.END)
            self.message_entry.insert(0, self.command_history[self.command_history_index])
        elif self.command_history_index == len(self.command_history) - 1:
            self.command_history_index += 1
            self.message_entry.delete(0, tk.END)

    def set_api_key(self):
        self.api_key = self.api_key_entry.get().strip()
        if self.api_key:
            self.api_key_entry.config(state='disabled', bg='#3c3c3c')
            self.set_api_key_button.config(state='disabled', bg='#3c3c3c')
            self.send_message_button.config(state=tk.NORMAL)
            self.display_data("Authorization Confirmed. Secure channel established. You may now interface with the database.")
        else:
            messagebox.showerror("Authorization Failure", "Invalid credentials. Please provide a valid Authorization Key.")

    def get_scp_response(self, message: str):
        if not self.api_key:
            return "System Alert: Authorization Key is not set. Please enter your Authorization Key to access the database."
        # Prepend a character-driven context modifier for the SCP universe
        character_modifier = "You are an AI created by the SCP Foundation to assist with inquiries about anomalies. All information provided should be consistent with the SCP Foundation's records and the understanding that the SCP universe is real."
        if not self.chat_history:  # Only add the character modifier if the chat history is empty
            self.chat_history.append({"role": "system", "content": character_modifier})
        self.chat_history.append({"role": "user", "content": message})
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=self.chat_history,
                api_key=self.api_key
            )
            response_content = response['choices'][0]['message']['content']
            self.chat_history.append({"role": "assistant", "content": response_content})  # Add AI response to history
            return response_content
        except openai.error.OpenAIError as e:
            return f"System Error: {e}. Please report this issue to your Site Administrator."

    def display_data(self, data):
        self.text.insert(tk.END, data + "\n\n")
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)  # Prevent user from editing the text display
        self.text.after(1000, lambda: self.text.config(state=tk.NORMAL))  # Re-enable text widget after short delay for continuous updates

# Running the application with thematic enhancements
if __name__ == "__main__":
    root = tk.Tk()
    app = SCPDatabaseApp(root)
    root.mainloop()
