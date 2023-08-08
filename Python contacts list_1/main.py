from tkinter import *
from tkinter import ttk
from  tkinter import messagebox
from db import Database
import re
# from email_validator import validate_email, EmailNotValidError

db = Database("Contactlist1.db")
root = Tk()
root.title("Contacts")
root.geometry('1400x700+83+100')
# root.geometry("1920x1080+0+0")
root.config(bg="#2c3e50")
# root.state("zoomed")

firstname = StringVar()
lastname = StringVar()
email = StringVar()
phonenumber = StringVar()

# regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

# def check(email):
#     if not (re.fullmatch(regex, email)):
#         messagebox.showerror("Error in Input", "Please enter a Valid Email")

# valid email function
def is_valid_email(email):
    # Regular expression to check if the email address is valid
    # This is a simple regular expression, and more complex ones can be used for stricter validation.
    # It's recommended to use a proper email validation library in production code.
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

def validate_email_input():
    if not txtEmail.get():
        return True # Skip validation is the email field is empty
    email_value = txtEmail.get()
    if not is_valid_email(email_value):
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return False
    return True

# valid number and phone format function
def is_valid_phone_number(phone_number):
    # Regular expression to check if the phone number contains only digits and follows the format
    pattern = r"^\d{10}$"  # Assumes 10 digits phone number format (e.g., 1234567890)
    return re.match(pattern, phone_number)

def validate_phone_input():
    phone_value = txtPhoneNumber.get()
    if not phone_value:
        return True  # Skip validation if the phone number field is empty
    phone_digits_only = re.sub(r'\D', '', phone_value)
    if not is_valid_phone_number(phone_digits_only):
        messagebox.showerror("Invalid Phone Number", "Please enter a valid 10-digit phone number.")
        return False
    return True

# change phone number to phone format
def format_phone_number(*args):
    # Get the current phone number value
    phone_value = phonenumber.get()

    # Remove any non-digit characters from the input (e.g., dashes)
    digits_only = re.sub(r'\D', '', phone_value)

    # Check if the phone number is empty or has less than 4 digits
    if not digits_only or len(digits_only) < 4:
        return

    # Format the phone number with dashes
    formatted_phone = '-'.join([digits_only[:3], digits_only[3:6], digits_only[6:]])

    # Update the phone number variable with the formatted value
    phonenumber.set(formatted_phone)

# Set up a trace on the phone number variable to call the format_phone_number function when the variable changes
phonenumber.trace_add('write', format_phone_number)

# Entries Frame
entries_frame = Frame(root, bg="#535c68")
entries_frame.pack(side=TOP, fill=X)
title = Label(entries_frame, text="Contacts", font=("Calibri", 20, "bold"), bg="#535c68", fg="white")
title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

lblFirstName = Label(entries_frame, text="First Name:", font=("Calibri", 16, "bold"), bg="#535c68", fg="white")
lblFirstName.grid(row=1, column=0, padx=10, pady=10, sticky="w")
txtFirstName = Entry(entries_frame, textvariable=firstname, font=("Calibri", 16, "bold"), width=30)
txtFirstName.grid(row=1, column=1, padx=10, pady=10, sticky="w")

lblLastName = Label(entries_frame, text="Last Name:", font=("Calibri", 16, "bold"), bg="#535c68", fg="white")
lblLastName.grid(row=1, column=2, padx=10, pady=10, sticky="w")
txtLastName = Entry(entries_frame, textvariable=lastname, font=("Calibri", 16), width=30)
txtLastName.grid(row=1, column=3, padx=10, pady=10, sticky="w")



lblEmail = Label(entries_frame, text="Email:", font=("Calibri", 16, "bold"), bg="#535c68", fg="white")
lblEmail.grid(row=2, column=0, padx=10, pady=10, sticky="w")
txtEmail = Entry(entries_frame, textvariable=email, font=("Calibri", 16), width=30)  
txtEmail.grid(row=2, column=1, padx=10, pady=10, sticky="w")
txtEmail.config(validate="focusout", validatecommand=validate_email_input)


lblPhoneNumber = Label(entries_frame, text="Phone Number:", font=("Calibri", 16, "bold"), bg="#535c68", fg="white")
lblPhoneNumber.grid(row=2, column=2, padx=10, pady=10, sticky="w")
txtPhoneNumber = Entry(entries_frame, textvariable=phonenumber, font=("Calibri", 16), width=30)
txtPhoneNumber.grid(row=2, column=3, padx=10, pady=10, sticky="w")
txtPhoneNumber.config(validate="key", validatecommand=validate_phone_input)
# txtPhoneNumber.config(validate="focusout", validatecommand=validate_phone_input)


def getData(event):
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    #print(row)
    firstname.set(row[1])
    lastname.set(row[2])
    email.set(row[3])
    phonenumber.set(row[4])
    
   
    

def displayAll():
    tv.delete(*tv.get_children())
    for row in db.fetch():
        tv.insert("", END, values=row)

# is_valid_phone_number(txtPhoneNumber.get())
    

def add_contact():
    if txtFirstName.get() == "" or txtLastName.get() == ""  or txtEmail.get() == ""  or txtPhoneNumber.get() == "":
        messagebox.showerror("Error in Input", "Please Fill All the Details")
        return
    
    # Remove any non-digit characters from the phone number input (e.g., dashes)
    phone_digits_only = re.sub(r'\D', '', txtPhoneNumber.get())

    if not is_valid_phone_number(phone_digits_only):
        messagebox.showerror("Invalid Phone Number", "Please enter a valid 10-digit phone number.")
        return

    # Format the phone number with dashes
    formatted_phone = '-'.join([phone_digits_only[:3], phone_digits_only[3:6], phone_digits_only[6:]])
    
    # Insert the contact with the formatted phone number
    db.insert(txtFirstName.get(), txtLastName.get(), txtEmail.get(), formatted_phone)
    messagebox.showinfo("Success", "Record Inserted")
    
    clearAll()
    displayAll()
 

def update_contact():
    if txtFirstName.get() == "" or txtLastName.get() == ""  or txtEmail.get() == ""  or txtPhoneNumber.get() == "":
        messagebox.showerror("Error in Input", "Please Fill All the Details")
        return
    db.update(row[0], txtFirstName.get(), txtLastName.get(), txtEmail.get(), txtPhoneNumber.get())
    messagebox.showinfo("Success", "Record Update")
    clearAll()
    displayAll()

def delete_contact():
    db.remove(row[0])
    clearAll()
    displayAll()

def clearAll():
    firstname.set("")
    lastname.set("")
    email.set("")
    phonenumber.set("")
    

btn_frame = Frame(entries_frame, bg="#535c68")
btn_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="w")

btnUpdate = Button(entries_frame, text="Update Contact", font=("Calibri", 16), bg="#2980b9", fg="white", command=update_contact)
btnUpdate.grid(row=3, column=1, padx=10, pady=10)

# Create the Delete Contact button
btnDelete = Button(entries_frame, text="Delete Contact", font=("Calibri", 16), bg="#c0392b", fg="white", command=delete_contact)
btnDelete.grid(row=3, column=2, padx=10, pady=10)

# Create the Clear All button
btnClear = Button(entries_frame, text="Clear All", font=("Calibri", 16), bg="#bdc3c7", fg="black", command=clearAll)
btnClear.grid(row=3, column=3, padx=10, pady=10)

# Create the Add Contacts button
btnAdd = Button(entries_frame, text="Add Contacts", font=("Calibri", 16), bg="#16a085", fg="white", command=add_contact)
btnAdd.grid(row=3, column=0, padx=10, pady=10)

# Table Frame
tree_frame = Frame(root, bg="#ecf0f1")
tree_frame.place(x=0, y=240, width=1400, height=520)
# tree_frame.place(x=0, y=480, width=1680, height=520)
style = ttk.Style()
style.theme_use("clam")
style.configure("mystyle.Treeview", font=('Calibri', 18), rowheight=50, background="lightblue", foreground="black") # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 18), background="#93B0C5", foreground="black") # Modify the font of the headings
tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5), style="mystyle.Treeview")
tv.heading("1", text="ID#")
tv.column("1", width=3)
tv.heading("2", text="First Name")
tv.column("2", width=3)
tv.heading("3", text="Last Name")
tv.column("3", width=3)
tv.heading("4", text="Email")
tv.column("4", width=3)
tv.heading("5", text="Phone Number")


tv['show'] = 'headings' 
tv.bind("<ButtonRelease-1>", getData)
tv.pack(fill=X)

displayAll()
root.mainloop()


