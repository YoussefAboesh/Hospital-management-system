import sqlite3

class Database:
    def __init__(self, data):
        self.con = sqlite3.connect(data)
        self.cur = self.con.cursor()

        
        sql = """
        CREATE TABLE IF NOT EXISTS Patients(
            id INTEGER PRIMARY KEY,
            name text,
            age text,
            gender text,
            blood text,
            chronic_dis text,
            convert_to_dep text,
            phone text,
            address text
        )
        """
        self.cur.execute(sql)
        self.con.commit()

    def insert(self,name,age,gender,blood,chronic_dis,convert_to_dep,phone,address):
        self.cur.execute("INSERT into Patients values(NULL,?,?,?,?,?,?,?,?)",
                        (name,age,gender,blood,chronic_dis,convert_to_dep,phone,address))
        self.con.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM Patients")
        rows = self.cur.fetchall()
        return rows

    def remove(self,id,):
        self.cur.execute("delete from Patients WHERE id=?", (id,))
        self.con.commit()

    def update(self, id, name, age, gender, blood, chronic_dis, convert_to_dep, phone, address):
        self.cur.execute("update Patients set name= ?,age= ?,gender= ?,blood= ?,chronic_dis= ?,convert_to_dep= ?,phone= ?,address= ? where id= ?",
                        (name,age,gender,blood,chronic_dis,convert_to_dep,phone,address,id,))
        self.con.commit()
