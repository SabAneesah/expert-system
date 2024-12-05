import tkinter as tk
from tkinter import messagebox, BooleanVar, Checkbutton
from knowledge_base import DiabetesExpertSystemKB

def collect_user_input():
    # List of questions and corresponding input types
    questions = [
        {"question": "What is your age? (Years):", "type": "int", "key": "age"},
        {"question": "What is your gender? (Male/Female/Other):", "type": "option", "key": "gender", "options": ["Male", "Female", "Other"]},
        {"question": "What is your weight? (kg):", "type": "float", "key": "weight"},
        {"question": "What is your height? (cm):", "type": "float", "key": "height"},
        {"question": "Do you have a family history of diabetes? (Yes/No):", "type": "option", "key": "family_history_diabetes", "options": ["Yes", "No"]},
        {"question": "Have you been diagnosed with diabetes before? (Yes/No):", "type": "option", "key": "diagnosed_diabetes", "options": ["Yes", "No"]},
        {"question": "Select any symptoms you are experiencing:", "type": "multiple_choice", "key": "symptoms", "options": ["Frequent urination", "Increased thirst", "Unexplained weight loss", "Fatigue", "Blurred vision"]},
        {"question": "What is your fasting blood sugar level? (mg/dL):", "type": "float", "key": "fasting_blood_sugar"},
        {"question": "What is your HbA1c level? (%):", "type": "float", "key": "hba1c"},
        {"question": "Do you take any medication for diabetes? (Yes/No):", "type": "option", "key": "medication", "options": ["Yes", "No"]},
        {"question": "How often do you exercise? (Daily/Weekly/Rarely/Never):", "type": "option", "key": "exercise_frequency", "options": ["Daily", "Weekly", "Rarely", "Never"]},
    ]

    # Store responses
    responses = {}

    # Function to display next question
    def next_question():
        nonlocal current_question_index

        # Collect and validate user input
        if current_question_index > 0:
            question_type = questions[current_question_index - 1]["type"]
            key = questions[current_question_index - 1]["key"]
            if question_type == "int":
                try:
                    responses[key] = int(entry.get())
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid number.")
                    return
            elif question_type == "float":
                try:
                    responses[key] = float(entry.get())
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid number.")
                    return
            elif question_type == "text":
                responses[key] = entry.get().strip()
            elif question_type == "option":
                responses[key] = option_var.get()
            elif question_type == "multiple_choice":
                responses[key] = [option for var, option in zip(check_vars, questions[current_question_index - 1]["options"]) if var.get()]

        # Check if there are more questions
        if current_question_index < len(questions):
            # Display next question
            question_label.config(text=questions[current_question_index]["question"])
            question_type = questions[current_question_index]["type"]

            # Clear previous input
            entry.grid_remove()
            option_menu.grid_remove()
            for checkbox in checkboxes:
                checkbox.grid_remove()

            if question_type == "text" or question_type in ["int", "float"]:
                entry.grid(row=1, column=0, pady=10)
                entry.delete(0, tk.END)
            elif question_type == "option":
                options = questions[current_question_index]["options"]
                option_var.set(options[0])
                option_menu['menu'].delete(0, 'end')
                for option in options:
                    option_menu['menu'].add_command(label=option, command=tk._setit(option_var, option))
                option_menu.grid(row=1, column=0, pady=10)
            elif question_type == "multiple_choice":
                options = questions[current_question_index]["options"]
                for i, option in enumerate(options):
                    check_vars[i].set(False)  # Reset checkboxes
                    checkboxes[i].config(text=option)
                    checkboxes[i].grid(row=1 + i, column=0, sticky="w")

            current_question_index += 1
        else:
            # Submit responses to the knowledge base
            kb = DiabetesExpertSystemKB()
            for key, value in responses.items():
                kb.add_fact(key, value)

            # Run inference engine and display results
            results = kb.run_inference_engine()
            result_text = "\n".join([f"{key}: {value}" for key, value in results.items()])
            messagebox.showinfo("Diabetes Risk Assessment", result_text)
            root.destroy()

    # Initialize Tkinter window
    root = tk.Tk()
    root.title("Diabetes Risk Assessment")
    root.geometry("900x500")

    # Question Label
    question_label = tk.Label(root, text="", font=("Arial", 12), wraplength=400)
    question_label.grid(row=0, column=0, pady=10)

    # Entry widget for text/numeric input
    entry = tk.Entry(root)

    # OptionMenu for dropdown input
    option_var = tk.StringVar()
    option_menu = tk.OptionMenu(root, option_var, "")

    # Checkboxes for multiple choice
    check_vars = [BooleanVar() for _ in range(10)]  # Max 10 options
    checkboxes = [Checkbutton(root, variable=var, font=("Arial", 10)) for var in check_vars]

    # Next Button
    next_button = tk.Button(root, text="Next", command=next_question)
    next_button.grid(row=15, column=0, pady=20)

    # Start with the first question
    current_question_index = 0
    next_question()

    root.mainloop()

if __name__ == "__main__":
    collect_user_input()
