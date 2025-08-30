# app.py
import customtkinter as ctk
from tkinter import messagebox
import pyperclip  # To copy password to clipboard

from database import Database
from password_generator import generate_password


# --- Main Application Class ---
class PasswordManagerApp(ctk.CTk):
    def __init__(self, db: Database):
        super().__init__()

        self.db = db
        self.generated_password = ""

        # --- Window Configuration ---
        self.title("MyPwdManagiah")
        self.geometry("650x300")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("red_theme.json")

        # --- Main Tab View ---
        self.tab_view = ctk.CTkTabview(self, width=550)
        self.tab_view.pack(padx=20, pady=20, fill="both", expand=True)

        self.generator_tab = self.tab_view.add("Generator")
        self.retriever_tab = self.tab_view.add("Retriever")

        self._create_generator_widgets()
        self._create_retriever_widgets()

    def _create_generator_widgets(self):
        """Creates widgets for the password generator tab."""
        frame = self.generator_tab

        # --- Website URL ---
        ctk.CTkLabel(frame, text="Website URL:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.gen_url_entry = ctk.CTkEntry(frame, width=400)
        self.gen_url_entry.grid(row=0, column=1, padx=10, pady=10)

        # --- Username / Email ---
        ctk.CTkLabel(frame, text="Username or Email:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.gen_username_entry = ctk.CTkEntry(frame, width=400)
        self.gen_username_entry.grid(row=1, column=1, padx=10, pady=10)

        # --- Generated Password Display ---
        ctk.CTkLabel(frame, text="Generated Password:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.password_display = ctk.CTkEntry(frame, width=400, state="readonly")
        self.password_display.grid(row=2, column=1, padx=10, pady=10)

        # --- Buttons ---
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        self.generate_button = ctk.CTkButton(button_frame, text="Generate Password", command=self._on_generate)
        self.generate_button.pack(side="left", padx=10)

        self.save_button = ctk.CTkButton(button_frame, text="Save Credentials", state="disabled", command=self._on_save)
        self.save_button.pack(side="left", padx=10)

    def _create_retriever_widgets(self):
        """Creates widgets for the password retriever tab."""
        frame = self.retriever_tab

        # --- Search URL ---
        ctk.CTkLabel(frame, text="Website URL:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.search_url_entry = ctk.CTkEntry(frame, width=300, placeholder_text="e.g., google.com")
        self.search_url_entry.grid(row=0, column=1, padx=10, pady=10)

        self.search_button = ctk.CTkButton(frame, text="Search", command=self._on_search)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        # --- Results Display ---
        results_frame = ctk.CTkFrame(frame)
        results_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=20, sticky="ew")

        ctk.CTkLabel(results_frame, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.result_username_label = ctk.CTkLabel(results_frame, text="", font=("Arial", 12, "bold"))
        self.result_username_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(results_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.result_password_label = ctk.CTkLabel(results_frame, text="", font=("Arial", 12, "bold"))
        self.result_password_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.copy_button = ctk.CTkButton(results_frame, text="Copy Password", state="disabled", command=self._on_copy)
        self.copy_button.grid(row=2, column=1, pady=10, sticky="e")

    # --- Callback Functions ---
    def _on_generate(self):
        self.generated_password = generate_password()
        self.password_display.configure(state="normal")
        self.password_display.delete(0, "end")
        self.password_display.insert(0, self.generated_password)
        self.password_display.configure(state="readonly")
        self.save_button.configure(state="normal")

    def _on_save(self):
        url = self.gen_url_entry.get()
        username = self.gen_username_entry.get()

        if not all([url, username, self.generated_password]):
            messagebox.showerror("Error", "All fields must be filled before saving.")
            return

        self.db.save_password(url, username, self.generated_password)
        messagebox.showinfo("Success", f"Credentials for {url} saved successfully!")

        # Clear fields after saving
        self.gen_url_entry.delete(0, "end")
        self.gen_username_entry.delete(0, "end")
        self.password_display.configure(state="normal")
        self.password_display.delete(0, "end")
        self.password_display.configure(state="readonly")
        self.generated_password = ""
        self.save_button.configure(state="disabled")

    def _on_search(self):
        url = self.search_url_entry.get()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL to search.")
            return

        credentials = self.db.get_password(url)

        if credentials:
            self.result_username_label.configure(text=credentials["username"])
            self.result_password_label.configure(text=credentials["password"])
            self.copy_button.configure(state="normal")
        else:
            self.result_username_label.configure(text="Not Found")
            self.result_password_label.configure(text="Not Found")
            self.copy_button.configure(state="disabled")
            messagebox.showinfo("Not Found", f"No credentials found for {url}.")

    def _on_copy(self):
        password = self.result_password_label.cget("text")
        if password and password != "Not Found":
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")


# --- Main Execution ---
if __name__ == "__main__":
    db_connection = Database()
    if db_connection.client:
        app = PasswordManagerApp(db=db_connection)
        app.mainloop()