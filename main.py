from datetime import datetime
import os.path
from os import path
import json
from dateutil import parser

class JournalEntry():
    def __init__(self,content,creation_date=None):
        self._content = content
        if creation_date==None:
            self._creation_date = datetime.now()
        else:
            self._creation_date = creation_date

    def creation_date(self):
        return self._creation_date
   
    def content(self):
        return self._content
   
    class JSONEncoder(json.JSONEncoder):
        DATE_FORMAT = "%Y-%m-%d"
        TIME_FORMAT = "%H:%M:%S"
        def default(self, o):
            return {"_type": "journalentry", "entry_date":o._creation_date.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                )),"content":o._content}
       
    class JSONDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

        def object_hook(self, obj):
            if '_type' not in obj:
                return obj
            type = obj['_type']
            if type == 'journalentry':
              return JournalEntry(obj['content'], parser.parse(obj['entry_date']))
            return obj
       
class EntryDB():
    def __init__(self,filename):
        self.file_name = filename
        try:
            
            with open(self.file_name,"r") as dbfile:
                self.entries_list = []
                json_text = dbfile.read()
                self.entries_list = json.loads(json_text,cls=JournalEntry.JSONDecoder)
        except FileNotFoundError:
            self.entries_list = [] #no file exists yet
           
    def add_entry(self,entry):
        self.entries_list.insert(0,entry)
      
    def get_all_entries(self):
      return self.entries_list
   
    def flush_to_disk(self):
        json_text = json.dumps(self.entries_list,cls=JournalEntry.JSONEncoder)
        with open(self.file_name,"w") as dbfile:
            dbfile.write(json_text)   

db = EntryDB("entries.db")

def menu():
    while True:
        print("1. Make Entry\n2. Browse\n3. Quit")
        select = input()
        if select == "1":
            input_text = input("How are you feeling today?")
            entry = JournalEntry(input_text)
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
          browse_select = input("1. All entries\n2. Most recent entry")
          if browse_select == "1":
            for entry in db.get_all_entries():
              print(f"{entry.creation_date().strftime('%a,%d,%B,%Y')} {entry.content()}")
          elif browse_select == "2":
            pass
           # for entry in db.get_recent_entry():
           #   print(f"{entry.creation_date()} {entry.content()}")

   

menu()

