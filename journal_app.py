#!/usr/bin/env python
from entry_db import EntryDB
import urwid
from edit import EditDisplay
from horizontal_menu import horizontal_menu,HorizontalMenu,SubMenu,Choice
from io import StringIO



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
        self.loop = urwid.MainLoop(self.box_menus, HorizontalMenu.palette)
    
    def run(self):
        self.loop.run()
    
    def edit_new(self,caption):
        editor = EditDisplay(StringIO(""))
        self.loop.widget = editor.view
        #handler = SaveHandler(None,editor)
        #loop = urwid.MainLoop(editor.view, editor.palette,
        #    unhandled_input=handler.unhandled_keypress)
        #loop.run()

if __name__ == "__main__":
    app = JournalApp()
    app.run()