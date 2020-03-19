import arrow
import os.path
from os import path
import json
import journal_entry
 
class EntryDB():
    def __init__(self,filename):
        self.file_name = filename
        try:
            with open(self.file_name,"r") as dbfile:
                self.entries_list = []
                json_text = dbfile.read()
                self.entries_list = json.loads(json_text,cls=journal_entry.JournalEntry.JSONDecoder)
        except FileNotFoundError:
            self.entries_list = [] #no file exists yet

    def add_entry(self,entry):
        self.entries_list.insert(0,entry)

    def get_all_entries(self):
      return self.entries_list

    def flush_to_disk(self):
        json_text = json.dumps(self.entries_list,cls=journal_entry.JournalEntry.JSONEncoder)
        with open(self.file_name,"w") as dbfile:
            dbfile.write(json_text)

    def search(self,term):
        return [i for i in self.entries_list if term in i.content()]

    def search_date(self,start,end):
        return [i for i in self.entries_list if start < i.creation_date() and end > i.creation_date()]
