import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from analysis import load_data, get_statistics, save_statistics, add_row, update_row, delete_row


class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Analysis Application")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.data = None
        self.file_path = None

        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons and text
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.load_button = ctk.CTkButton(self.frame, text="Load Data", command=self.load_data)
        self.load_button.pack(pady=10)

        self.stats_text = ScrolledText(self.frame, width=60, height=20)
        self.stats_text.pack(pady=10)

        self.plot_button = ctk.CTkButton(self.frame, text="Show Plot", command=self.show_plot)
        self.plot_button.pack(pady=10)

        self.save_button = ctk.CTkButton(self.frame, text="Save Statistics", command=self.save_stats)
        self.save_button.pack(pady=10)

        self.add_button = ctk.CTkButton(self.frame, text="Add Row", command=self.add_row)
        self.add_button.pack(pady=10)

        self.update_button = ctk.CTkButton(self.frame, text="Update Row", command=self.update_row)
        self.update_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(self.frame, text="Delete Row", command=self.delete_row)
        self.delete_button.pack(pady=10)

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_path = file_path
            self.data = load_data(file_path)
            stats = get_statistics(self.data)
            self.display_statistics(stats)

    def display_statistics(self, stats):
        self.stats_text.delete(1.0, 'end')
        for key, value in stats.items():
            self.stats_text.insert('end', f"{key}:\n{value}\n\n")

    def show_plot(self):
        if self.data is not None:
            # Create a new window for the plot
            plot_window = ctk.CTkToplevel(self.root)
            plot_window.title("Data Plot")

            fig, ax = plt.subplots()
            self.data.plot(ax=ax)

            # Create a canvas and pack it into the new window
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
        else:
            messagebox.showerror("Error", "No data to display")

    def save_stats(self):
        if self.data is not None:
            stats = get_statistics(self.data)
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                save_statistics(stats, file_path)
                messagebox.showinfo("Info", "Statistics saved successfully")
        else:
            messagebox.showerror("Error", "No data to save")

    def add_row(self):
        if self.data is not None:
            new_row = self.get_row_input("Add Row")
            if new_row:
                self.data = add_row(self.data, new_row)
                self.save_data()
                messagebox.showinfo("Info", "Row added successfully")
        else:
            messagebox.showerror("Error", "No data loaded")

    def update_row(self):
        if self.data is not None:
            index = simpledialog.askinteger("Update Row", "Enter the index of the row to update:")
            if index is not None and 0 <= index < len(self.data):
                updated_row = self.get_row_input("Update Row")
                if updated_row:
                    self.data = update_row(self.data, index, updated_row)
                    self.save_data()
                    messagebox.showinfo("Info", "Row updated successfully")
            else:
                messagebox.showerror("Error", "Invalid row index")
        else:
            messagebox.showerror("Error", "No data loaded")

    def delete_row(self):
        if self.data is not None:
            index = simpledialog.askinteger("Delete Row", "Enter the index of the row to delete:")
            if index is not None and 0 <= index < len(self.data):
                self.data = delete_row(self.data, index)
                self.save_data()
                messagebox.showinfo("Info", "Row deleted successfully")
            else:
                messagebox.showerror("Error", "Invalid row index")
        else:
            messagebox.showerror("Error", "No data loaded")

    def get_row_input(self, title):
        row_str = simpledialog.askstring(title,
                                         "Enter the new row values separated by commas (e.g., value1,value2,value3):")
        if row_str:
            values = row_str.split(',')
            if len(values) == len(self.data.columns):
                return pd.Series(values, index=self.data.columns)
            else:
                messagebox.showerror("Error", "The number of values does not match the number of columns")
                return None
        return None

    def save_data(self):
        if self.file_path:
            self.data.to_csv(self.file_path, index=False)
        else:
            messagebox.showerror("Error", "No file path to save data")


if __name__ == "__main__":
    root = ctk.CTk()
    app = DataAnalysisApp(root)
    root.mainloop()