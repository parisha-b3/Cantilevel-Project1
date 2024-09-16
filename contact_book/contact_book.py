import tkinter as tk
from tkinter import messagebox

class Contact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __str__(self):
        return f"{self.name}, {self.phone}"

def load_contacts(filename="contacts.txt"):
    contacts = []
    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(", ")
                if len(parts) == 2:
                    name, phone = parts
                    contacts.append(Contact(name, phone))
                else:
                    print(f"Skipping incorrectly formatted line: {line.strip()}")
    except FileNotFoundError:
        pass  # If the file doesn't exist, return an empty list
    return contacts


def save_contacts(contacts, filename="contacts.txt"):
    with open(filename, "w") as file:
        for contact in contacts:
            file.write(f"{contact.name}, {contact.phone}\n")

# Tkinter GUI implementation
contacts = []

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")

        # UI Elements
        self.name_label = tk.Label(root, text="Name:")
        self.name_entry = tk.Entry(root)

        self.phone_label = tk.Label(root, text="Phone:")
        self.phone_entry = tk.Entry(root)

        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact)
        self.update_button = tk.Button(root, text="Update Contact", command=self.update_contact)
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_entries)
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_form)
        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact)

        self.listbox = tk.Listbox(root)
        self.listbox.bind('<<ListboxSelect>>', self.load_selected_contact)

        # Layout
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.phone_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.add_button.grid(row=2, column=0, padx=5, pady=5)
        self.update_button.grid(row=2, column=1, padx=5, pady=5)
        self.clear_button.grid(row=3, column=0, padx=5, pady=5)
        self.reset_button.grid(row=3, column=1, padx=5, pady=5)
        self.delete_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Place the listbox in the same row but different column (side by side)
        self.listbox.grid(row=0, column=2, rowspan=5, padx=10, pady=5, sticky="nsew")

        # Configure the column and row weights to make the listbox expand properly
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(5, weight=1)

        self.update_listbox()

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()

        if name and phone:
            contacts.append(Contact(name, phone))
            self.update_listbox()
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Please fill out both fields.")

    def update_contact(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            if name and phone:
                contacts[index].name = name
                contacts[index].phone = phone
                self.update_listbox()
                self.clear_entries()
            else:
                messagebox.showwarning("Input Error", "Please fill out both fields.")
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to update.")

    def delete_contact(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del contacts[index]
            self.update_listbox()
            self.clear_entries()
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    def reset_form(self):
        self.clear_entries()
        self.listbox.selection_clear(0, tk.END)

    def load_selected_contact(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            selected_contact = contacts[index]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(tk.END, selected_contact.name)
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(tk.END, selected_contact.phone)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for contact in contacts:
            self.listbox.insert(tk.END, str(contact))

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()