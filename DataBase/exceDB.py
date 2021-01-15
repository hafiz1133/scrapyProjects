import mysql.connector
mydb= mysql.connector.connect(
    host='localhost',
    passwd='umair123',
    user='root',
    database='newtable'

)
mycursor= mydb.cursor()
#mycursor.execute("create table excels (name varchar(255), caseNumber integer(10),judgeName varchar(255))")
import xlrd
all=[]
try:
    loc=("Book1.xlsx")
    wb=xlrd.open_workbook(loc)
    sheet= wb.sheet_by_index(0)

    print(sheet.cell_value(1,0))
    for i in range(sheet.nrows):
        val=(sheet.row_values(i))
        all.append(val)
except:
    print("Error !!!")
query = "insert into excels (name,caseNumber,judgeName) values (%s,%s,%s)"
mycursor.executemany(query,all)
mydb.commit()