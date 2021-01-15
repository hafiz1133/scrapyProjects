import mysql.connector
import csv
mydb= mysql.connector.connect(
    host='localhost',
    passwd='umair123',
    user='root',
    database='newtable'
)
print(mydb)
mycursor = mydb.cursor()
#mycursor.execute("create table db1s (name varchar(255), age integer(12),area varchar(255))") # create table
with open('book1.csv','r') as file:
    reader = csv.reader(file )
    all=[]
    for i in reader:
        value = (i[0],i[1],i[2])
        all.append(value)
# mycursor.execute("show tables")
# print(all)
# query = "insert into db1s (name,age,area) values (%s,%s,%s)"
# mycursor.execute(query)
# mydb.commit()

mycursor.execute("select * from db1s")
myresult = mycursor.fetchall()
for j in myresult:
    print(j)