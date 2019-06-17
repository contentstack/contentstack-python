
class EntryModel:
    
    def __init__(self, result):
        self.result = result
        self.entry_uid = None
        self.owner_email_id = None
        self.owner_uid = None
        self.title = None
        self.url = None
        self.tags = []
        self.owner_map = dict
        self._metadata = dict
        self.tags = dict


    def get_uid(self):
        if self.result != None :
            if 'uid' in self.result :
                self.result['uid'] = 'uid'

