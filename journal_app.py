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
    ('head', 'dark cyan', 'dark blue', 'bold'),
    ]


class JournalApp:

    footer_text = ('foot', [
        "PyJournal    ",
        ('key', "F5"), " save  ",
        ('key', "F8"), " back",
    ])

    def __init__(self):
        self.db = EntryDB("entries.db")
        self.box_menus = self.make_menus()
        self.loop = urwid.MainLoop(self.box_menus, HorizontalMenu.palette + editor_palette,unhandled_input=self.unhandled_keypress)# EditDisplay.palette)
        self.current_entry = None
        self.editor = None
    
    def make_menus(self):
        browse_line_length = 39
        entries_list = self.db.get_all_entries()
        choice_list = []
        for entry in entries_list:
            if entry.creation_date().day == arrow.now().day:
                date_string = entry.creation_date().humanize()
            else:
                date_string = entry.creation_date().format('YYYY-MM-DD HH:mm:ss')
            ellipsis = '...' if len(entry.content()) > browse_line_length-len(date_string) else ''
            choice_list.append(SubMenu(f"{date_string} {entry.content()}"[:browse_line_length]+ellipsis,[Choice("Edit Entry",self.edit,entry),Choice("Delete Entry",self.delete,entry)]))
        menu_top = SubMenu(u'Main Menu', [
            Choice(u'New Entry',self.edit),
            SubMenu(u'Browse', choice_list),
            Choice('Exit', self.exit_app)
        ])
        return horizontal_menu(menu_top)

    def greeting(self):
        entries = self.db.get_all_entries()
        if entries:
            time_humanized = entries[0].creation_date().replace(tzinfo='US/Pacific').humanize()
            current = arrow.now()
            if current.hour < 12:
                date = 'morning'
            elif current.hour > 18:
                date = 'evening'
            else:
                date = 'afternoon'
        return ("head", [
            f"Good {date}, you last made an entry {time_humanized}"
        ])

    def delete(self,caption,entry):
        self.db.delete_entry(entry)
        self.db.flush_to_disk()
        self.box_menus = self.make_menus()
        self.loop.widget = self.box_menus

    def run(self):
        self.loop.run()
    
    def exit_app(self,caption,entry):
        self.loop.stop()
        quit()
    
    def edit(self,caption,entry):
        if entry == None:
            content = ""
            self.current_entry = None
            header = self.greeting()
        else:
            header = None
            content = entry.content()
            self.current_entry = entry
        self.editor = EditDisplay(StringIO(content),header,JournalApp.footer_text)
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
                self.box_menus = self.make_menus()
                self.loop.widget = self.box_menus
            else:
                self.editor.unhandled_keypress(k)

if __name__ == "__main__":
    app = JournalApp()
    app.run()
