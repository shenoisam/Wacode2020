from .db import DB_Connection


class Controller:
    def __init__(self):
        self.db = DB_Connection()

    def validate_user(self,username, password):
        rmStr = "username = \"%s\" AND password = \"%s\"" % (username, password)
        print(rmStr)
        res = self.db.query("ID", "user", rmStr)
        if res is not None:
            res = None
        print(res)
        return res


