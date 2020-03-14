import arrow
import os.path
from os import path
import json
import entry_db
import journal_entry
from edit import EditDisplay
from io import StringIO
import urwid


def greeting(self,db):
    entries=db.get_all_entries()
    if entries:
        time_humanized=entries[0].creation_date().humanize()
        current=arrow.now()
        if current.hour < 12:
            date = 'morning'
        elif current.hour > 12:
            date = 'afternoon'
        elif current.hour > 6:
            date = 'evening'
        return f"Good {date}, you last made an entry {time_humanized}"

def menu(self):
    db = entry_db.EntryDB("entries.db")
    print(greeting(db))
    while True:
        print("1. Make Entry\n2. Browse\n3. Quit")
        select = input()
        if select == "1":
            input_text = multi_input("How are you feeling today?")
            entry = journal_entry.JournalEntry(input_text)
            db.add_entry(entry)
            db.flush_to_disk()
        elif select == "2":
            browse_menu(db)
            break
        elif select == "3":
            return quit()

def browse_menu(self,db):
    while True:
        print("What entries would you like to view?")
        browse_select = input("1. Browse all\n2. Text Search \n3. Date Search\n4. Back")
        if browse_select == "1":
            display_entries(db.get_all_entries())
        elif browse_select == "2":
            display_entries(search(db))
        elif browse_select == "3":
            display_entries(search_date(db))
        elif browse_select == "4":
            menu()

def display_entries(self,entries):
    for entry in entries:
        if entry.creation_date().day == arrow.now().day:
            print(f"{entry.creation_date().humanize()} {entry.content()}")
        else:
            print(f"{entry.creation_date().format('YYYY-MM-DD HH:mm:ss')} {entry.content()}")

def search_date(self,db):
    usr_date = input("Enter day (MM-DD-YY):")
    usr_date = arrow.get(usr_date, 'MM-DD-YY')
    return db.search_date(usr_date.floor('day'),usr_date.ceil('day'))

def search(self,db):
    term = input("Search:")
    return db.search(term)

def multi_input(self,prompt=None):
    #custom input function for multi-line entries
    if prompt:
        print(prompt)
    content = []
    while True:
        try:
            line = input()
            content.append(line)
        except EOFError:
            return "/n".join(content)

class SaveHandler():
    def __init__(self,entry,editor):
        self.entry = entry
        self.editor = editor
    def unhandled_keypress(self,k):
        if k == "f5":
            self.entry.set_content(self.editor.get_text())
        else:
            self.editor.unhandled_keypress(k)
def main():
    db = entry_db.EntryDB("entries.db")
    entry = db.get_all_entries()[0]
    editor = EditDisplay(StringIO(entry.content()))
    handler = SaveHandler(entry,editor)
    loop = urwid.MainLoop(editor.view, editor.palette,
        unhandled_input=handler.unhandled_keypress)
    loop.run()
    db.flush_to_disk()


main()
