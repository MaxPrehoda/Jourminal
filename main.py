import arrow
import os.path
from os import path
import json
import entry_db
import journal_entry

db = entry_db.EntryDB("entries.db")

def greeting():
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

def menu():
    print(greeting())
    while True:
        print("1. Make Entry\n2. Browse\n3. Quit")
        select = input()
        if select == "1":
            input_text = multi_input("How are you feeling today?")
            entry = journal_entry.JournalEntry(input_text)
            db.add_entry(entry)
            db.flush_to_disk()
        elif select == "2":
            browse_menu()
            break
        elif select == "3":
            return quit()

def browse_menu():
    while True:
        print("What entries would you like to view?")
        browse_select = input("1. Browse all\n2. Search \n4. Back")
        if browse_select == "1":
            display_entries(db.get_all_entries())
        elif browse_select == "2":
            display_entries(search())
        elif browse_select == "3":
            menu()

def display_entries(entries):
    for entry in entries:
        if entry.creation_date().day == arrow.now().day:
            print(f"{entry.creation_date().humanize()} {entry.content()}")
        else:
            print(f"{entry.creation_date().format('YYYY-MM-DD HH:mm:ss')} {entry.content()}")

def search():
    term = input("Search:")
    return db.search(term)

def multi_input(prompt=None):
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


menu()

