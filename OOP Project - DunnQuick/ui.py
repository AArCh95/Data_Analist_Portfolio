import customtkinter as ctk
import pandas as pd
from PIL import Image, ImageTk  # Use PIL for handling images
from tkinter import messagebox
from letter_generator import DunningLetterGenerator
from agents import collectors  
import os
import sys

mykeys = list(collectors.keys())
mykeys.sort()
collectors = {i: collectors[i] for i in mykeys}

class DunningLetterUI:
    def __init__(self, root):
        # Set up the appearance and style of the CustomTkinter
        ctk.set_appearance_mode("dark")  # "light" or "dark"
        ctk.set_default_color_theme("dark-blue")  # "blue", "green", or "dark-blue"

        self.root = root
        self.root.title("DunnQuick")
        self.root.geometry("685x415")  # Adjust size if needed
        self.root.configure(bg="#203859")  # Blue color (hex code)

        # Lock the window size (set minsize and maxsize)
        self.root.resizable(False, False)

        # Add Logo
        logo_path = self.resource_path("logo.png")
        self.logo_image = Image.open(logo_path)  # Open the image with PIL
        self.logo = ctk.CTkImage(self.logo_image, size=(350, 150))  # Use CTkImage and set the size
        self.logo_label = ctk.CTkLabel(root, image=self.logo, text="")  # Add image to the CTkLabel
        self.logo_label.grid(row=0, column=1, columnspan=3, padx=0, pady=0, sticky="ew")  # Center the logo

        # Labels and entries for user input
        self.name_label = ctk.CTkLabel(root, text="Recipient Name:",
                                       text_color="white",
                                       font=("Arial", 14, "bold"))
        self.name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")  # Align right
        self.name_entry = ctk.CTkEntry(root)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        self.address_label = ctk.CTkLabel(root, text="Recipient Address:",
                                          text_color="white",
                                          font=("Arial", 14, "bold"))
        self.address_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.address_entry = ctk.CTkEntry(root)
        self.address_entry.grid(row=2, column=1, padx=10, pady=10)

        self.account_label = ctk.CTkLabel(root, text="Account Number:",
                                          text_color="white",
                                          font=("Arial", 14, "bold"))
        self.account_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.account_entry = ctk.CTkEntry(root)
        self.account_entry.grid(row=3, column=1, padx=10, pady=10)

        self.total_label = ctk.CTkLabel(root, text="Total Owed:",
                                        text_color="white",
                                        font=("Arial", 14, "bold"))
        self.total_label.grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.total_entry = ctk.CTkEntry(root)
        self.total_entry.grid(row=1, column=3, padx=10, pady=10)

        self.past_due_label = ctk.CTkLabel(root, text="Past Due Amount:",
                                           text_color="white",
                                           font=("Arial", 14, "bold"))
        self.past_due_label.grid(row=2, column=2, padx=10, pady=10, sticky="e")
        self.past_due_entry = ctk.CTkEntry(root)
        self.past_due_entry.grid(row=2, column=3, padx=10, pady=10)

        self.days_to_pay_label = ctk.CTkLabel(root, text="Days to Pay:",
                                              text_color="white",
                                              font=("Arial", 14, "bold"))
        self.days_to_pay_label.grid(row=3, column=2, padx=10, pady=10, sticky="e")
        self.days_to_pay = ctk.CTkEntry(root)
        self.days_to_pay.grid(row=3, column=3, padx=10, pady=10)

        # Dropdown for agent selection
        self.Agent_label = ctk.CTkLabel(root, text="Select Agent:",
                                        text_color="white",
                                        font=("Arial", 14, "bold"))
        self.Agent_label.grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.Agent_var = ctk.StringVar(root)
        self.Agent_var.set(list(collectors.keys())[0])  # Set default value to first collector
        self.Agent_menu = ctk.CTkOptionMenu(root, variable=self.Agent_var, values=list(collectors.keys()))
        self.Agent_menu.grid(row=7, column=1, padx=10, pady=10)


        # Dropdown for letter level selection
        self.level_label = ctk.CTkLabel(root, text="Select Letter Level:",
                                        text_color="white",
                                        font=("Arial", 14, "bold"))
        self.level_label.grid(row=7, column=2, padx=10, pady=10, sticky="e")
        self.level_var = ctk.StringVar(root)
        self.level_var.set("Level 1")  # Default value
        self.level_menu = ctk.CTkOptionMenu(root, variable=self.level_var, values=["Level 1", "Level 2", "Level 3"])
        self.level_menu.grid(row=7, column=3, padx=10, pady=10)

        # Button to generate the letter
        self.generate_button = ctk.CTkButton(root, text="Generate Dunning Letter",
                                             command=self.generate_letter,
                                             text_color="white",
                                             font=("Arial", 14, "bold"))
        self.generate_button.grid(row=9, column=1, columnspan=4, pady=20, sticky="nsew")  # Place button at the bottom

        # Button to clear the fields
        self.clear_button = ctk.CTkButton(root, text="Clear Fields",
                                          font=("Arial", 14, "bold"),
                                          command=self.clear_fields)
        self.clear_button.grid(row=9, column=0, padx=10, pady=20, sticky="e")

    # Function to clear all fields
    def clear_fields(self):
        self.name_entry.delete(0, 'end')  # Clear name entry
        self.address_entry.delete(0, 'end')  # Clear address entry
        self.account_entry.delete(0, 'end')  # Clear account number entry
        self.total_entry.delete(0, 'end')  # Clear total owed entry
        self.past_due_entry.delete(0, 'end')  # Clear past due entry
        self.days_to_pay.delete(0, 'end')  # Clear days to pay entry
        # self.Agent_var.set(list(collectors.keys())[0])  # Reset agent dropdown
        # self.level_var.set("Level 1")  # Reset letter level dropdown

    def generate_letter(self):
        # Get user input
        name = self.name_entry.get()
        address = self.address_entry.get()
        account_number = self.account_entry.get()
        total_owed = self.total_entry.get()
        days_to_due = self.days_to_pay.get()
        past_due = self.past_due_entry.get()
        letter_level = self.level_var.get()
        selected_agent = self.Agent_var.get()  # Get selected agent's name

        # Ensure all fields are filled
        if not all([name, address, account_number, total_owed, past_due, days_to_due]):
            messagebox.showerror("Input Error", "All fields are required!")
            return

        # Ensure valid numbers for total and past due amounts
        try:
            total_owed = float(total_owed)
            past_due = float(past_due)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid amounts!\nOnly numbers allowed!")
            return

        # Get the agent details from the selected agent
        agent_details = collectors[selected_agent]
        agent_name = selected_agent
        agent_email = agent_details['email']
        agent_phone = agent_details['phone']
        agent_location = agent_details['location']

        # Pass the input and agent details to the DunningLetterGenerator class
        letter_gen = DunningLetterGenerator(name, address, account_number, total_owed,
                                            past_due, letter_level, days_to_due,
                                            agent_name, agent_email, agent_phone, agent_location)
        letter_gen.create_pdf()

        # Show success message
        messagebox.showinfo("Success", "Dunning letter generated successfully!")

    def resource_path(self, relative_path):
        """ Get the absolute path to a resource, works for both PyInstaller and development. """
        try:
            # PyInstaller stores data files in _MEIPASS when packaged
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


    def fill_customer_details(self, event):
        selected_name = self.name_entry.get()
        customer_data = self.customers_df[self.customers_df["Customer"] == selected_name]


