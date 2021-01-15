import mysql.connector
mydb= mysql.connector.connect(
    host='localhost',
    passwd='umair123',
    user='root',
    database='newtable'
)
import xlrd
all=[]
try:
    loc=("record.xlsx")
    wb=xlrd.open_workbook(loc)
    sheet= wb.sheet_by_index(0)

    print(sheet.cell_value(1,0))
    for i in range(sheet.nrows):
        value=(sheet.row_values(i))
        #value = (i[0],i[1],i[2])
        all.append(value)
        #print(all)
except:
    print("Error !!!")

print(mydb)
mycursor = mydb.cursor()
#mycursor.execute("create table db2s (name varchar(255), case integer(15),judge varchar(255))") # create table
query = "insert into db2s (name,case,judge) values (%s,%s,%s)"
mycursor.executemany(query,all)
mydb.commit()
#
