class Task:
    result = []

    def __init__(self, QueryTaskDB) -> None:
        self.status = QueryTaskDB.status
        self.obj = QueryTaskDB.obj
        if QueryTaskDB.postive is not None:
            self.postive == ''.join(QueryTaskDB.postive)
        if QueryTaskDB.negative is not None:
            self.postive == ''.join(QueryTaskDB.negative)
    
    def set_result(self, result):
        self.result = result