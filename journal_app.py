from entry_db import EntryDB
import urwid
from edit import EditDisplay

menu_top = SubMenu(u'Main Menu', [
    Choice(u'New Entry'),
    SubMenu(u'Browse', [
        Choice(u'Entry Placeholder')
    ]),
])


class JournalApp:

    def __init__(self):
        self.box_menus = HorizontalBoxes()
        self.box_menus.open_box(menu_top.menu)
        self.db = EntryDB("entries.db")
        self.loop = urwid.MainLoop(urwid.Filler(top, 'middle', 10), palette)
    
    def run(self):
        self.loop.start()
    
    def edit_new(self):
        self.loop.stop()
        editor = EditDisplay(StringIO(""))
        handler = SaveHandler(None,editor)
        loop = urwid.MainLoop(editor.view, editor.palette,
            unhandled_input=handler.unhandled_keypress)
        loop.run()