import sqlite3

class Database:
    def __init__(self,db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS contactslist(
            id Integer Primary Key,
            firstname text,
            lastname text,
            email text,
            phonenumber text
        )
        """ 
        self.cur.execute(sql)
        self.con.commit()

    #Insert Function
    def insert(self, firstname, lastname, email, phonenumber):
        self.cur.execute("insert into contactslist values (NULL,?,?,?,?)",
                         (firstname, lastname, email, phonenumber))
        self.con.commit()

    # Fetch All Data from DB
    def fetch(self):
        self.cur.execute("SELECT * from contactslist")
        rows = self.cur.fetchall()
        # print(rows)
        return rows
    
    # Delete a Record in DB
    def remove(self, id):
        self.cur.execute("delete from contactslist where id=?", (id,))
        self.con.commit()

    #Update a Record in DB
    def update(self, id, firstname, lastname, email, phonenumber):
        self.cur.execute(
            "update contactslist set firstname=?, lastname=?, email=?, phonenumber=? where id=?",
            (firstname, lastname, email, phonenumber, id))
        self.con.commit()