import tkinter as tk
from tkinter import messagebox

def calculate_sum():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
        
        result = a + b + c

        result_label.config(text=f"{a} + {b} + {c} = {result}")
        
        result_line_number = len(result_label["text"])

        # Calculate the required window height based on content
        window_height = int(300 + (result_line_number ))   # Adjust padding as needed
        app.geometry(f"250x{window_height}")

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")




# Create the main application window
app = tk.Tk()
app.title("API_Tester")
app.geometry("250x300")

center_frame = tk.Frame(app)
center_frame.grid(row=0, column=0, padx=65, pady=45)

# Create input fields and labels
label_a = tk.Label(center_frame, text="Input1:", bg="lightblue", width="17")
label_a.grid(row=0, column=0)
entry_a = tk.Entry(center_frame)
entry_a.grid(row=1, column=0)

# Create an empty row
empty_row_1 = tk.Frame(center_frame, height=10)
empty_row_1.grid(row=2)

label_b = tk.Label(center_frame, text="Input2:", bg="lightblue", width="17")
label_b.grid(row=3, column=0)
entry_b = tk.Entry(center_frame)
entry_b.grid(row=4, column=0)

# Create an empty row
empty_row_2 = tk.Frame(center_frame, height=10)
empty_row_2.grid(row=5)

label_c = tk.Label(center_frame, text="Input3:", bg="lightblue", width="17")
label_c.grid(row=6, column=0)
entry_c = tk.Entry(center_frame)
entry_c.grid(row=7, column=0)

# Bind the Enter key to the calculate_sum function
entry_a.bind("<Return>", lambda event: calculate_sum())
entry_b.bind("<Return>", lambda event: calculate_sum())
entry_c.bind("<Return>", lambda event: calculate_sum())

# Create an empty row
empty_row_3 = tk.Frame(center_frame, height=10)
empty_row_3.grid(row=8)

# Button to calculate the sum
calculate_button = tk.Button(center_frame, text="Compute", command=calculate_sum)
calculate_button.grid(row=9, column=0, columnspan=2)

# Create an empty row
empty_row_4 = tk.Frame(center_frame, height=10)
empty_row_4.grid(row=10)

#Label for the label of the result
label_r = tk.Label(center_frame, text="Result:", bg="lightblue", width="17")
label_r.grid(row=11, column=0)

# Label to display the result
result_label = tk.Label(center_frame, text="", bg="lightblue", width="17", wraplength="100")
result_label.grid(row=12, column=0, columnspan=2)

# Center the frame in the window
center_frame.grid_configure(sticky="nsew")

# Start the main event loop
app.mainloop()