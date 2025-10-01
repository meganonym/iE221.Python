import DBConnect
engine = DBConnect.connect()
from sqlalchemy import MetaData, Table, delete, update
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
metadata = MetaData()
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
id = None
tbl = None

def gview():
    global id, tbl
    touch = False
    groom = False
    menu = 0
    print("\nNhập 2 chữ số cuối của MAGV:")
    id = f"GV{input("GV")}"
    query = f"select * from GIAOVIEN where MAGV='{id}'"
    ans = read(query)
    if ans.empty:
        print(f"\n--- không có MAGV '{id}' trong CSDL ---\n")
    else:
        df1 = pd.DataFrame(ans)
        tbl = pd.concat([tbl, df1], axis=0)
        query = f"select TRGKHOA, MAKHOA, TENKHOA from KHOA"
        df2 = pd.DataFrame(pd.read_sql(query, engine))
        found = False
        for i in range(df2.shape[0]):
            if id == df2.at[i, "TRGKHOA"]:
                found = True
                facid = df2.at[i, "MAKHOA"]
                facname = df2.at[i, "TENKHOA"]
                if not df1.at[0, "MAKHOA"] == facid:
                    print("\n", df1)
                    print(f"\ntable GIAOVIEN:\tMAGV = '{id}'; MAKHOA = {df1.at[0, 'MAKHOA']}")
                    print(f"table LOP:\tMAGV = '{id}'; MAKHOA = {facid}")
                    df1.at[0, "MAKHOA"] = facid
                    GVtbl = Table('GIAOVIEN', metadata, autoload_with=engine)
                    stmt = update(GVtbl).where(GVtbl.c.MAGV == id).values(MAKHOA=facid)
                    try:
                        with engine.connect() as connection:
                            connection.execute(stmt)
                            connection.commit()
                        print(f"\n--- đã update MAKHOA của MAGV '{id}' ---")
                    except (SQLAlchemyError, DBAPIError) as e:
                        print("\n", e, "\n")
                break
        if found is True:
            title = "trưởng"
        else:
            title = "giáo viên"
            query = f"select TENKHOA from KHOA where MAKHOA='{df1.at[0, "MAKHOA"]}'"
            df2 = pd.read_sql(query, engine)
            facname = df2.at[0, "TENKHOA"]
        print(f"\nChức danh: {title} khoa '{facname}'")
        print(df1.to_string(index=False))
        print()

        query = f"select * from GIANGDAY where MAGV='{id}' ORDER BY NAM, HOCKY"
        ans = read(query)
        if not(ans.empty):
            touch = True
            menu += 1
            print("Các môn đã dạy:")
            df2 = output(ans)

        query = f"select * from LOP where MAGVCN='{id}'"
        ans = read(query)
        if not(ans.empty):
            groom = True
            menu += 1
            print("Các lớp đã chủ nhiệm:")
            df3 = output(ans)

        if menu > 0 or (title == "trưởng"):
            while True:
                if menu > 0:
                    print("---- Giảng Dạy & Chủ Nhiệm ----")
                    if touch is True:
                        print("1. Xem bảng điểm môn đã dạy")
                    if groom is True:
                        print("2. Xem dữ liệu lớp chủ nhiệm")
                    print("-------------------------------")
                if title == "trưởng":
                    print("----- FACULTY MANAGEMENT -----")
                    print("3. Xem danh sách giáo viên")
                    print("4. Xem danh sách môn học")
                    print("5. Xem danh sách lớp môn học")
                    print("6. Xem bảng điểm 1 môn học")
                    print("------------------------------")
                try:
                    select = int(input("\nChọn tác vụ số: "))
                    if select == 1 and touch is True:
                        print("\nCác môn đã dạy:")
                        print(df2)
                        print()
                        taught(df2)
                    elif select == 2 and groom is True:
                        print("\nCác lớp đã chủ nhiệm:")
                        print(df3)
                        print()
                        homeroom(df3)
                    elif select > 2 and select < 7:
                        dean(select, facid)
                    else:
                        print()
                        break
                except ValueError:
                    print("\nInvalid input. Please enter a valid integer.\n")
    if not tbl is None:
        try:
            tbl.to_excel("teacher.xlsx", sheet_name=f"{id}", index=False)
        except PermissionError:
            print("Error: Permission denied. The file 'teacher.xlsx' might be open or you lack write permissions.\n")
        except FileNotFoundError:
            print("Error: The directory for 'teacher.xlsx' does not exist.\n")
        except Exception as e:
            #Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")

def read(query):
    return pd.read_sql(query, engine)

def output(ans):
    global tbl
    if ans.empty:
        foo()
    else:
        df = pd.DataFrame(ans)
        tbl = pd.concat([tbl, df], axis=0)
        print(df)
        print()
        return df

def foo():
    print("\n--- không có dữ liệu ---\n")

def taught(df2):
    global id, tbl
    while True:
        while True:
            row = int(input("Chọn hàng số: "))
            if row in range(0, df2.shape[0]):
                print(f"\nBảng điểm MAMH '{df2.at[row, 'MAMH']}':")
                break
        query = (f"select * from KETQUATHI where MAHV LIKE '{df2.at[row, 'MALOP']}__' AND MAMH='{df2.at[row, 'MAMH']}'"
                 + f" AND DATEDIFF(day, '{df2.at[row, 'DENNGAY']}', NGTHI) < 30")
        output(read(query))
        cont = input("Tiếp tục xem bảng điểm môn đã dạy? Y/N: ")
        if cont == "N" or cont == "n":
            break
        print("\nCác môn đã dạy:")
        print(df2)
        print()
    print()

def homeroom(df3):
    global id, tbl
    while True:
        while True:
            row = int(input("Chọn hàng số: "))
            if row in range(0, df3.shape[0]):
                clsid = df3.at[row, 'MALOP']
                print(f"\nDanh sách học viên MALOP '{clsid}':")
                break
        query = f"select * from HOCVIEN where MALOP='{clsid}'"
        df4 = output(pd.DataFrame(pd.read_sql(query, engine)))
        tbl = pd.concat([tbl, df4], axis=0)
        print(f"MAHV lớp trưởng lớp '{clsid}': " + f"'{df3.at[row, 'TRGLOP']}'" + "\n")
        select = input("Xem dữ liệu học viên? Y/N: ")
        if select == "Y" or select == "y":
            while True:
                hvid = f"K{input("\nNhập 4 chữ số cuối của MAHV: K")}"
                found = False
                for i in range(df4.shape[0]):
                    if hvid == df4.at[i, 'MAHV']:
                        found = True
                        print()
                        break
                if found == True:
                    import student
                    student.output(hvid)
                    cont = input("Tiếp tục xem dữ liệu học viên? Y/N: ")
                    if cont == "N" or cont == "n":
                        break
        cont = input("Tiếp tục xem dữ liệu lớp chủ nhiệm? Y/N: ")
        if cont == "N" or cont == "n":
            break
        print("\nCác lớp đã chủ nhiệm:")
        print(df3)
    print()

def dean(select, facid):
    global tbl
    query = f"select * from MONHOC where MAKHOA='{facid}'"
    df5 = pd.DataFrame(read(query))
    if select == 3:
        print("\nDanh sách giáo viên:")
        query = f"select * from GIAOVIEN where MAKHOA='{facid}'"
        output(read(query))
    elif select == 4:
        print("\nDanh sách môn học:")
        if not df5.empty:
            tbl = pd.concat([tbl, df5], axis=0)
            print(df5)
            print()
        else:
            foo()
    elif select == 5:
        print("\nDanh sách lớp môn học:")
        query = f"select g.*, m.MAKHOA from GIANGDAY g, MONHOC m where g.MAMH = m.MAMH and m.MAKHOA='{facid}' order by MAMH, NAM, HOCKY"
        output(read(query))
    elif select == 6:
        cid = input("MAMH: ")
        found = False
        for i in range(df5.shape[0]):
            if cid == df5.at[i, 'MAMH']:
                found = True
                break
        if found is True:
            print(f"\nBảng điểm MAMH '{cid}':")
            query = f"select * from KETQUATHI k where k.MAMH = '{cid}' order by MAHV, NGTHI"
            output(read(query))
        else:
            print(f"\nMAKHOA '{facid}' không quản lý MAMH '{cid}'\n")