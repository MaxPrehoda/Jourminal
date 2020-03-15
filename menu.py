import urwid
from entry_db import EntryDB
from edit import EditDisplay
from io import StringIO

class MenuButton(urwid.Button):
    def __init__(self, caption, callback):
        super(MenuButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'  \N{BULLET} ', caption], 2), None, 'selected')

class SubMenu(urwid.WidgetWrap):
    def __init__(self, caption, choices):
        super(SubMenu, self).__init__(MenuButton(
            [caption, u"\N{HORIZONTAL ELLIPSIS}"], self.open_menu))
        line = urwid.Divider(u'\N{LOWER ONE QUARTER BLOCK}')
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.AttrMap(urwid.Text([u"\n  ", caption]), 'heading'),
            urwid.AttrMap(line, 'line'),
            urwid.Divider()] + choices + [urwid.Divider()]))
        self.menu = urwid.AttrMap(listbox, 'options')

    def open_menu(self, button):
        top.open_box(self.menu)

class Choice(urwid.WidgetWrap):
    def __init__(self, caption,handler):
        super(Choice, self).__init__(
            MenuButton(caption, self.item_chosen))
        self.caption = caption
        self.handler = handler

    def item_chosen(self, button):
        self.handler()

def exit_program(key):
    raise urwid.ExitMainLoop()

class HorizontalBoxes(urwid.Columns):
    def __init__(self):
        super(HorizontalBoxes, self).__init__([], dividechars=1)

    def open_box(self, box):
        if self.contents:
            del self.contents[self.focus_position + 1:]
        self.contents.append((urwid.AttrMap(box, 'options', focus_map),
            self.options('given', 24)))
        self.focus_position = len(self.contents) - 1

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
    top.open_box(menu_top.menu)
    urwid.MainLoop(urwid.Filler(top, 'middle', 10), palette).run()
    db = EntryDB("entries.db")
    entry = db.get_all_entries()[0]
    editor = EditDisplay(StringIO(entry.content()))
    handler = SaveHandler(entry,editor)
    loop = urwid.MainLoop(editor.view, editor.palette,
        unhandled_input=handler.unhandled_keypress)
    loop.run()
    db.flush_to_disk()

if __name__ == "__main__":
    main()
