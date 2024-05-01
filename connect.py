import pymysql

class db:
    host = '211.101.239.27'
    port = 3306
    user = 'mrfz'
    password ='	y6JFE3bwEXnxsrj4'
    database ='mrfz'
    debug = 0

    data = None
    cursor = None

    def __init__(self) -> None:
        self.data = pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.password,database=self.database)
        self.cursor = self.data.cursor()

    def __del__(self) -> None:
        self.data.commit()
        self.cursor.close()
        self.data.close()

    def execute(self,query):
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        self.data.commit()
        return res
    

if __name__ == '__main__':
    a = db()
    print(type(a.execute(query='select uid,password from account')))