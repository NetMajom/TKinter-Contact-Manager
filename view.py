from tkinter import Frame, Listbox, Scrollbar, RIGHT, Y, LEFT, BOTH, END, LabelFrame, Label, Entry
from tkinter.messagebox import showerror

from kapcsolatkezelo.model import Contact


class ContactList(Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.lb = Listbox(self)
        scroll = Scrollbar(self, command=self.lb.yview)
        self.lb.config(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        self.lb.pack(side=LEFT, fill=BOTH)

    def insert(self, contact, index=END):
        self.lb.insert(index, "{} {}".format(contact.first_name, contact.last_name))

    def delete(self, index):
        self.lb.delete(index)

    def edit(self, contact, index):
        self.delete(index)
        self.insert(contact, index)

    def double_click(self, fn):
        self.lb.bind('<Double-Button-1>', lambda _: fn(self.lb.curselection()[0]))


class ContactForm(LabelFrame):
    # noinspection SpellCheckingInspection
    form_fields = ('Vezeteknev', 'Keresztnev', 'Email', 'Telefon')

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.frame = Frame(self)
        self.input_fields = list(map(self.create_fields, enumerate(self.form_fields)))
        self.frame.pack()

    def create_fields(self, field):
        position, title = field
        label = Label(self.frame, text=title)
        input_field = Entry(self.frame, width=30)
        label.grid(row=position, column=0, pady=5)
        input_field.grid(row=position, column=1, pady=5, padx=5)
        return input_field

    def contact_details_inserting(self, contact):
        details = (contact.first_name, contact.last_name, contact.email, contact.phone)
        for input_field, value in zip(self.input_fields, details):
            input_field.delete(0, END)
            input_field.insert(0, value)

    def get_contact_data(self):
        values = [i.get() for i in self.input_fields]
        try:
            return Contact(*values)
        except ValueError as ex:
            # noinspection SpellCheckingInspection
            showerror('Validacios hiba!', ex, parent=self)

    def delete(self):
        for input_field in self.input_fields:
            input_field.delete(0, END)
