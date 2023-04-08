import sqlite3


class DataBase:
    def __init__(self):
        self.count = 0;
        self.db_name = "data" + str(self.count) + ".db"



    def make_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS data(h REAR,v REAR)")
        conn.commit()
        conn.close()

    def insert_data(self, h, v):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO data VALUES(?,?)", (h, v))
        conn.commit()
        conn.close()

    def make_db2(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS data2(h REAR)")
        conn.commit()
        conn.close()

    def insert_data2(self, h):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO data2 VALUES(?)", (h))
        conn.commit()
        conn.close()

    def make_db3(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS data3(v REAR)")
        conn.commit()
        conn.close()

    def insert_data3(self, v):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO data3 VALUES(?)", (v,))
        conn.commit()
        conn.close()


    def make_db4(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS data4(v REAR)")
        conn.commit()
        conn.close()

    def insert_data4(self, v):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO data4 VALUES(?)", (v,))
        conn.commit()
        conn.close()

    def make_db5(self):# Taking Picture 부분
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS data5(v REAR)")
        conn.commit()
        conn.close()


    def insert_data5(self, v):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO data5 VALUES(?)", (v,))
        conn.commit()
        conn.close()

    def make_db6(self):# 샘플수 부분
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS data6(v REAR)")
        conn.commit()
        conn.close()

    def insert_data6(self, v):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO data6 VALUES(?)", (v,))
        conn.commit()
        conn.close()

    # select w only and return list
    # def select_w(self):
    #     w = []
    #     conn = sqlite3.connect(self.db_name)
    #     c = conn.cursor()
    #     c.execute("SELECT w FROM data")
    #     data = c.fetchall()
    #     for i in range(len(data)):
    #         w.append(data[i][0])
    #     conn.close()
    #     return w

    # select w only and return list
    # def select_h(self):
    #     h = []
    #     conn = sqlite3.connect(self.db_name)
    #     c = conn.cursor()
    #     c.execute("SELECT h FROM data")
    #     data = c.fetchall()
    #     for i in range(len(data)):
    #         h.append(data[i][0])
    #     conn.close()
    #     return h
    #
    def select_data(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM data")
        data = c.fetchall()
        conn.close()
        return data

    def select_data2(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM data2")
        data = c.fetchall()
        conn.close()
        return data

    def select_data3(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM data3")
        data = c.fetchall()
        conn.close()
        return data

    def select_data4(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM data4")
        data = c.fetchall()
        conn.close()
        return data

    def select_data5(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM data5")
        data = c.fetchall()
        conn.close()
        return data

    def select_data6(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM data6")
        data = c.fetchall()
        conn.close()
        return data
    #
    def delete_data(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM data")
        conn.commit()
        conn.close()

    def delete_data2(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM data2")
        conn.commit()
        conn.close()

    def delete_data3(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM data3")
        conn.commit()
        conn.close()

    def delete_data4(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM data4")
        conn.commit()
        conn.close()

    def delete_data5(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM data5")
        conn.commit()
        conn.close()

    def delete_data6(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM data6")
        conn.commit()
        conn.close()

    #
    # # get how many data in db
    # def get_data_count(self):
    #     conn = sqlite3.connect(self.db_name)
    #     c = conn.cursor()
    #     c.execute("SELECT * FROM data")
    #     data = c.fetchall()
    #     conn.close()
    #     return len(data)


d = DataBase()
d.make_db()
d.make_db2()
d.make_db3()
d.make_db4()
d.make_db5()
d.make_db6()