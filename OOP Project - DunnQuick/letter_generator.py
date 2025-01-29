from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime, timedelta
import os
import sys


class DunningLetterGenerator:
    def __init__(self, recipient_name, recipient_address, account_number, total_owed, past_due,
                 letter_level, days_to_due, agent_name, agent_email, agent_phone, agent_location):
        self.recipient_name = recipient_name
        self.recipient_address = recipient_address
        self.account_number = account_number
        self.total_owed = total_owed
        self.past_due = past_due
        self.days_to_due = days_to_due
        self.letter_level = letter_level
        self.agent_name = agent_name
        self.agent_email = agent_email
        self.agent_phone = agent_phone
        self.agent_location = agent_location

    def resource_path(self, relative_path):
        """Get the absolute path to a resource (assets/templates), compatible with PyInstaller packaging."""
        try:
            # PyInstaller stores data files in a temporary directory named _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def create_pdf(self):

        # Load the appropriate template
        template_path = self.resource_path(f"templates/{self.letter_level.lower()}.txt")
        with open(template_path, 'r', encoding='cp1252') as template_file:
            letter_content = template_file.read()

        # Get today's date and calculate the future due dates
        today = datetime.today().strftime('%A, %B %d, %Y')
        future_date = self.calculate_due_date(self.days_to_due)
        in_10_days = datetime.today() + timedelta(days=10)
        in_30_days = datetime.today() + timedelta(days=30)

        # Replace placeholders in the template
        letter_content = letter_content.replace("[LOCATION]", self.agent_location)
        letter_content = letter_content.replace("[NUMBER OF DAYS]", self.days_to_due)
        letter_content = letter_content.replace("[COLLECTOR PHONE NUMBER]", self.agent_phone)
        letter_content = letter_content.replace('[COLLECTOR EMAIL]', self.agent_email)
        letter_content = letter_content.replace("[COLLECTOR NAME]", self.agent_name)
        letter_content = letter_content.replace("[DATE]", today)
        letter_content = letter_content.replace("[CUSTOMER NAME]", self.recipient_name)
        letter_content = letter_content.replace("[ADDRESS]", self.recipient_address)
        letter_content = letter_content.replace("[ACCOUNT NUMBER]", self.account_number)
        letter_content = letter_content.replace("[AMOUNT]", f"${self.total_owed:,.2f}")
        letter_content = letter_content.replace("[PAST DUE AMOUNT]", f"${self.past_due:,.2f}")
        letter_content = letter_content.replace("[DATE TO BE PAID BY]", future_date)
        letter_content = letter_content.replace("[DATE + 10]", in_10_days.strftime('%A, %B %d, %Y'))
        letter_content = letter_content.replace("[DATE + 30]", in_30_days.strftime('%A, %B %d, %Y'))

        # Generate the PDF
        documents_folder = os.path.expanduser("~/Documents")  # Get the user's Documents folder
        file_name = f"{documents_folder}/Dunning letter - {self.recipient_name} - {self.letter_level}.pdf"
        c = canvas.Canvas(file_name, pagesize=A4)
        c.setFont("Helvetica", 11)  # Using Helvetica instead of Arial
        width, height = A4

        # Draw the logo on the top left of the PDF
        logo_path = self.resource_path('assets/logo.png')
        logo_width = 2.1 * inch  # Set the desired width for the logo
        logo_height = 0.93 * inch  # Set the desired height for the logo
        c.drawImage(logo_path, 250, 750, width=logo_width, height=logo_height)

        # Draw the address on the top right of the PDF
        address_path = self.resource_path('assets/address.PNG')
        address_width = 3 * inch  # Set the desired width for the logo
        address_height = 0.75 * inch  # Set the desired height for the logo
        c.drawImage(address_path, 190, 20, width=address_width, height=address_height)

        # Set the margins
        left_margin = 50
        right_margin = 550  # Adjust this value for your right limit (A4 width is 595.27 points)
        text_width = right_margin - left_margin

        # Create a text object
        text_object = c.beginText(left_margin, height - 100)
        text_object.setFont("Helvetica", 11)

        # Wrap text manually while preserving paragraphs and line breaks
        lines = letter_content.splitlines()

        for line in lines:
            if line.strip() == "":  # If the line is a blank line, add it as-is (paragraph space)
                text_object.textLine("")
            else:
                # Manually wrap the text using canvas.stringWidth()
                wrapped_lines = self.wrap_text(line, text_width, c)
                for wrapped_line in wrapped_lines:
                    text_object.textLine(wrapped_line)

        c.drawText(text_object)

        # Save the PDF
        c.save()
        print(f"Dunning letter saved as {file_name}")

        # Open the generated PDF automatically
        os.startfile(file_name)  # This will open the file automatically on Windows

    def wrap_text(self, text, max_width, canvas):
        """Manually wrap text based on the width available."""
        words = text.split(' ')
        wrapped_lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            # Check if adding the next word exceeds the max_width
            if canvas.stringWidth(test_line, "Helvetica", 11) <= max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line.strip())
                current_line = word + " "

        # Append the last line
        if current_line:
            wrapped_lines.append(current_line.strip())

        return wrapped_lines

    def calculate_due_date(self, days_to_due):
        """Calculate the future due date based on the days to due."""
        today_date = datetime.today()
        days_to_due = int(days_to_due)
        future_date = today_date + timedelta(days=days_to_due)
        return future_date.strftime('%A, %B %d, %Y')
