class Task:
    result = []

    def __init__(self, QueryTaskDB) -> None:
        self.status = QueryTaskDB.status
        self.obj = QueryTaskDB.obj
        if QueryTaskDB.positive is not None:
            self.positive = ''.join(QueryTaskDB.positive)
        if QueryTaskDB.negative is not None:
            self.neagtive = ''.join(QueryTaskDB.negative)
    
    def set_result(self, result):
        self.result = result