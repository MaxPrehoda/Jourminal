#!/usr/bin/env python
import arrow
from entry_db import EntryDB
from journal_entry import JournalEntry
import urwid
from edit import EditDisplay
from horizontal_menu import horizontal_menu,HorizontalMenu,SubMenu,Choice
from io import StringIO

editor_palette = [
    ('body','black','light cyan'),
    ('foot','dark cyan', 'dark blue', 'bold'),
    ('key','light cyan', 'dark blue', 'underline'),
    ]


class JournalApp:

    def __init__(self):
        self.db = EntryDB("entries.db")
        entries_list = self.db.get_all_entries()
        choice_list = []
        for entry in entries_list:
            ellipsis = '...' if len(entry.content()) > 5 else ''
            choice_list.append(Choice(f"{entry.creation_date().format('YYYY-MM-DD HH:mm:ss')} {entry.content()}"[:25]+ellipsis, self.edit))
           #if entry.creation_date().day == arrow.now().day:
                #choice_list.append(Choice(f"{entry.creation_date().humanize(arrow.now())} {entry.content()}", self.edit_old))
            #else:
                #choice_list.append(Choice(f"{entry.creation_date().format('YYYY-MM-DD HH:mm:ss')} {entry.content()}"[:25], self.edit_old))
        menu_top = SubMenu(u'Main Menu', [
            Choice(u'New Entry',self.edit),
            SubMenu(u'Browse', choice_list),
        ])
        self.box_menus = horizontal_menu(menu_top)
        self.loop = urwid.MainLoop(self.box_menus, HorizontalMenu.palette + editor_palette,unhandled_input=self.unhandled_keypress)# EditDisplay.palette)
        self.current_entry = None
        self.editor = None
    
    def run(self):
        self.loop.run()
    
    def edit(self,caption):
        if caption == "New Entry":
            content = ""
            self.current_entry = None
        else:
            d = arrow.get(caption[:19],'YYYY-MM-DD HH:mm:ss').replace(tzinfo='US/Pacific')
            for i in self.db.get_all_entries():
                if i.creation_date() == d:
                    content = i.content()
                    break
        self.editor = EditDisplay(StringIO(content))
        self.loop.widget = self.editor.view

    def unhandled_keypress(self,k):
        if not self.loop.widget is self.box_menus:
            if k == "f5":
                if self.current_entry == None:
                    new_entry = JournalEntry(self.editor.get_text())
                    self.current_entry = new_entry
                    self.db.add_entry(new_entry)
                    self.db.flush_to_disk()
                else:
                    self.current_entry.set_content(self.editor.get_text())
                    self.db.flush_to_disk()
            elif k == "f8":
                self.loop.widget = self.box_menus
            else:
                self.editor.unhandled_keypress(k)

if __name__ == "__main__":
    app = JournalApp()
    app.run()