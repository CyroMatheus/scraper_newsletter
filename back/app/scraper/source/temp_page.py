import os, json

class tempPage():
    def __init__(self, model):
        super(tempPage, self).__init__()
        self.model = model
        self.path = f"source/temp/{self.model}.json"

    def page(self):
        try:
            page = json.load(open(self.path))
            page = list(page.keys())
            return int(page[0])
        except Exception as e:
            return 1
    
    def save(self, list):
        with open(self.path, "w") as arquivo:
            json.dump(list, arquivo, indent=4)
