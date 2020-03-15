#!/usr/bin/env python
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
        menu_top = SubMenu(u'Main Menu', [
            Choice(u'New Entry',self.edit_new),
            SubMenu(u'Browse', [
                Choice(u'Entry Placeholder')
            ]),
        ])
        self.box_menus = horizontal_menu(menu_top)
        self.db = EntryDB("entries.db")
        self.loop = urwid.MainLoop(self.box_menus, HorizontalMenu.palette + editor_palette,unhandled_input=self.unhandled_keypress)# EditDisplay.palette)
        self.current_entry = None
        self.editor = None
    
    def run(self):
        self.loop.run()
    
    def edit_new(self,caption):
        self.editor = EditDisplay(StringIO(""))
        self.loop.widget = self.editor.view

    def unhandled_keypress(self,k):
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