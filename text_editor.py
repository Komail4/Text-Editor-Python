import tkinter
from tkinter import ttk, messagebox
import tkinter.filedialog

class HomePage(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller  = controller
        self.label_welcome = ttk.Label(self, text="Welcome to Komail's Text Editor", font=("Arial", 24))
        self.label_welcome.pack(pady=100)

class TextEditPage(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.current_file = None
    
        scrollbar = tkinter.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")

        self.text = tkinter.Text(self, height=30, width=100, yscrollcommand=scrollbar.set)
        self.text.pack(side="left", fill="both", expand=True, pady=10, padx=10)

        scrollbar.config(command=self.text.yview)
    
    def open_file(self):
        file_path = tkinter.filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.current_file = file_path
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text.delete("1.0", "end")
                self.text.insert("1.0", content)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as file:
                content = self.text.get("1.0", "end-1c",)
                file.write(content)
        else:
            file_path = tkinter.filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            
            if file_path:
                self.current_file = file_path
                with open(file_path, "w", encoding="utf-8") as file:
                    content = self.text.get("1.0", "end-1c")
                    file.write(content)
                messagebox.showinfo("Success", "File saved successfully.")
            else:
                messagebox.showwarning("Warning", "File not saved. Please choose a file name.")
    
    def new(self):
        if self.current_file:
            with open(self.current_file, "r", encoding="utf-8") as file:
                content = file.read()
                
            current = self.text.get("1.0", "end-1c")
            if current != content:
                choice = messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Do you want to save them?")
                if choice:
                    self.save_file()
                else:
                    self.current_file = None
                    self.text.delete("1.0", "end")

        elif not self.current_file and self.text.get("1.0", "end-1c").strip():
            choice = messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Do you want to save them?")
            if choice:
                self.save_file()
            else:
                self.text.delete("1.0", "end")
        # self.text.delete("1.0", "end")
        # self.current_file = None
            
# Main App
class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Text Editor (Text Document)")
        self.geometry("1000x600")

        # Container to hold all frames
        self.container = tkinter.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}  # Store page instances here

        # Initialize all frames once
        for F in (HomePage, TextEditPage):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        self.create_menu()
        self.show_frame("TextEditPage")

    def create_menu(self):
        menubar = tkinter.Menu(self)

        file_menu = tkinter.Menu(menubar, tearoff=0)
        
        file_menu.add_command(label="New", command=self.frames["TextEditPage"].new)
        file_menu.add_command(label="Open", command=self.frames["TextEditPage"].open_file)
        file_menu.add_command(label= "Save", command = self.frames["TextEditPage"].save_file)
        file_menu.add_command(label="Exit", command=self.quit)

        menubar.add_cascade(label="File", menu=file_menu)

        main_menu = tkinter.Menu(menubar, tearoff=0)

        main_menu.add_command(label="Home Page", command=lambda: self.show_frame("HomePage"))

        menubar.add_cascade(label="Menu", menu=main_menu)
        
        self.config(menu=menubar)

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()