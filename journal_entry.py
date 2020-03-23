import arrow
import json

class JournalEntry():
    def __init__(self,content,creation_date=None):
        """Create JournalEntry object using a content string and an optional date. If date is None then it is set to the current time."""
        utc = arrow.utcnow()
        local = utc.to('US/Pacific')
        self._content = content
        if creation_date==None:
            self._creation_date = local
        else:
            self._creation_date = creation_date

    def creation_date(self):
        return self._creation_date

    def content(self):
        return self._content

    def set_content(self,content):
        self._content = content

    class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            return {"_type": "journalentry", "entry_date":o._creation_date.format('YYYY-MM-DD HH:mm:ss'),"content":o._content}

    class JSONDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

        def object_hook(self, obj):
            if '_type' not in obj:
                return obj
            type = obj['_type']
            if type == 'journalentry':
              return JournalEntry(obj['content'], arrow.get(obj['entry_date']).replace(tzinfo='US/Pacific'))
            return obj
