from sqlite3 import connect
from tkinter import Toplevel, Button, RIGHT, Tk, LEFT

from kapcsolatkezelo.model import Contact
from kapcsolatkezelo.view import ContactForm, ContactList


class NewContactForm(Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.contact = None
        self.form = ContactForm(self)
        self.button = Button(self, text='OK', command=self.ok)
        self.form.pack(padx=10, pady=10)
        self.button.pack(padx=10, pady=10)
        self.resizable(False, False)

    def ok(self):
        self.contact = self.form.get_contact_data()
        if self.contact:
            self.destroy()

    def get_contact(self):
        self.grab_set()
        self.wait_window()
        return self.contact


class UpdateContactForm(ContactForm):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # noinspection SpellCheckingInspection
        self.btn_save = Button(self, text='Mentes')
        # noinspection SpellCheckingInspection
        self.btn_delete = Button(self, text='Torol')
        self.btn_save.pack(side=RIGHT, padx=5, pady=5)
        self.btn_delete.pack(side=RIGHT, padx=5, pady=5)

    def bind_save(self, fn):
        self.btn_save.config(command=fn)

    def bind_delete(self, fn):
        self.btn_delete.config(command=fn)


class App(Tk):

    def __init__(self, connection):
        super().__init__()
        # noinspection SpellCheckingInspection
        self.title('TKinter kapcsolat app')
        self.resizable(False, False)
        self.conn = connection
        self.selected_index = None
        self.list = ContactList(self, height=20)
        self.form = UpdateContactForm(self)
        # noinspection SpellCheckingInspection
        self.btn_new = Button(self, text='Uj kapcsolat felvetele', command=self.new_contact)
        self.contacts = self.get_contacts_from_db()
        for contact in self.contacts:
            self.list.insert(contact)
        self.list.pack(side=LEFT, padx=10, pady=10)
        self.form.pack(padx=10, pady=10)
        self.list.double_click(self.one_contact_show)
        self.form.bind_save(self.contact_update)
        self.form.bind_delete(self.contact_delete)
        self.btn_new.pack(padx=10, pady=10)

    def get_contacts_from_db(self) -> list:
        contacts = []
        for record in self.conn.execute('SELECT * FROM contacts'):
            try:
                contact = Contact(*record[1:])
            except ValueError:
                pass
            else:
                contact.id = record[0]
                contacts.append(contact)
        return contacts

    def one_contact_show(self, index):
        self.selected_index = index
        contact = self.contacts[index]
        self.form.contact_details_inserting(contact)

    def new_contact(self):
        new_contact = NewContactForm(self)
        contact = new_contact.get_contact()
        if not contact:
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute("""INSERT INTO contacts(
            first_name,
            last_name,
            email,
            phone)
            VALUES (?, ?, ?, ?)""",
                           contact.get_contact_details_in_tuple())
            self.conn.commit()
            contact.id = cursor.lastrowid
            self.contacts.append(contact)
            self.list.insert(contact)
        except ValueError:
            pass

    def contact_update(self):
        if self.selected_index is None:
            return
        contact_id = self.contacts[self.selected_index].id
        contact = self.form.get_contact_data()
        if contact:
            with self.conn as connection:
                connection.execute("""UPDATE contacts SET
                 first_name=?,
                 last_name=?,
                 email=?,
                 phone=?
                 WHERE id=?""",
                                   contact.get_contact_details_in_tuple() + (contact_id,))
            contact.id = contact_id
            self.contacts[self.selected_index] = contact
            self.list.edit(contact, self.selected_index)

    def contact_delete(self):
        if self.selected_index is None:
            return
        contact_id = self.contacts[self.selected_index].id
        with self.conn as c:
            c.execute('DELETE FROM contacts WHERE id=?', (contact_id,))
        self.form.delete()
        self.list.delete(self.selected_index)
        self.selected_index = None


with connect('contacts.db') as conn:
    app = App(conn)
    app.mainloop()
