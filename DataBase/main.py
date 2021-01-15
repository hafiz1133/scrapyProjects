import mysql.connector
mydb = mysql.connector.connect(
    host ="localhost",
    user="root",
    passwd="umair123",
    database="newtable"

        )
print(mydb)
mycursor = mydb.cursor()

# mycursor.execute("show databases")
# mycursor.execute("create table students (id integer(10), name varchar(222))")
# mycursor.execute("show tables")
# for i in mycursor:
#      print(i)
# query="insert into students (id,name) values (%s,%s)"
# st=[
#     (1,"Umair"),
#     (2,"Ali"),
#     (3,"Ahmed"),
#     (4,"Salman")
# ]
# mycursor.executemany(query,st)
# mydb.commit()
# mycursor.execute("select name from students")
# myresult = mycursor.fetchall()
# for j in myresult:
#     print(j)
# mycursor.execute("select * from students where id=1")
# res=mycursor.fetchall()
# for k in res:
#     print(k)
# mycursor.execute("update students set id = 14 where name = 'Umair'")
# mydb.commit()
mycursor.execute("delete from students where name ='Umair'")
mydb.commit()
mycursor.execute("select * from students ")
myresult = mycursor.fetchall()
for j in myresult:
    print(j)