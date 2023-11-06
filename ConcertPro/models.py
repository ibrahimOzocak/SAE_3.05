import mysql.connector

db = mysql.connector.connect(
    host="servinfo-maria",user = "sevellec", password = "sevellec", database = "DBsevellec"
)

cursor = db.cursor()

def test():
    try:
        req1 = "SELECT * FROM Artiste"
        cursor.execute(req1)
        info = cursor.fetchall()
        for i in info:
            print(i)
    except Exception as e:
        print(e.args)
        
if __name__ == "__main__":
    test()