import mysql.connector
import mysql
import csv
mydb= mysql.connector.connect(
    host='localhost',
    passwd='umair123',
    user='root',
    database='newtable'
)
print(mydb)
mycursor = mydb.cursor()
# This is USED To create table in Databse whose name mentioned above
# mycursor.execute("Create table temp(id int(11) NOT NULL AUTO_INCREMENT, name varchar(255) DEFAULT NULL, email varchar(255) DEFAULT NULL, phone varchar(255) DEFAULT NULL, phone2 varchar(255) DEFAULT NULL, company varchar(255) DEFAULT NULL, city varchar(255) DEFAULT NULL, country varchar(255) DEFAULT NULL, link varchar(255) DEFAULT NULL, designation varchar(255) DEFAULT NULL, industry varchar(255) DEFAULT NULL,  PRIMARY KEY (id), UNIQUE KEY data_unique (name,email,city) )")
# mycursor.execute("show tables")
# for i in mycursor:
#     print(i)
# with open('data-2020-10-26 14-19-46.csv','r' ,encoding="utf8") as file:
#     reader = csv.reader(file )
#     all=[]
#     for i in reader:
#         value = (i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9])
#         all.append(value)
#
# query = "insert ignore into temp (name,email,phone,phone2,company,city,country,link,designation,industry) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
# mycursor.executemany(query,all)
# mydb.commit()
mycursor.execute("select * from temp")
myresult = mycursor.fetchall()
for j in myresult:
    print(j)