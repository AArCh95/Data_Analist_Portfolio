from tkinter import Tk
from ui import DunningLetterUI  # Import the UI class

def main():
    root = Tk()  # Create the Tkinter root window
    app = DunningLetterUI(root)  # Initialize the GUI class
    root.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__":
    main()  # Run the main function
