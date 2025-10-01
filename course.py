import DBConnect
engine = DBConnect.connect()
from sqlalchemy import MetaData, Table, delete, update
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
metadata = MetaData()
import pandas as pd
tbl = None

def switch():
    while True:
        print("----- COURSE MANAGEMENT -----")
        print("1. Xem danh sách môn học")
        print("2. Xem danh sách lớp môn học")
        print("3. Xem bảng điểm 1 môn học")
        print("4. Xem dữ liệu 1 môn học")
        print("5. Sửa dữ liệu 1 môn học")
        print("6. Thêm 1 môn học vào CSDL")
        print("7. Xóa dữ liệu 1 môn học")
        print("------------------------------")
        try:
            select = int(input("\nChọn tác vụ số: "))
            if select == 1:
                print("\nDanh sách môn học:")
                query = f"select * from MONHOC"
                output(query)
            elif select == 2:
                clist()
            elif select == 3:
                gradebook()
            elif select == 4:
                cview()
            elif select > 4 and select < 8:
                MHaed(select)
            else:
                print()
                break
        except ValueError:
            print("\nInvalid input. Please enter a valid integer.\n")
    if not tbl is None:
        try:
            tbl.to_excel("admin.xlsx", sheet_name='qlhv', index=False)
        except PermissionError:
            print("Error: Permission denied. The file 'admin.xlsx' might be open or you lack write permissions.\n")
        except FileNotFoundError:
            print("Error: The directory for 'admin.xlsx' does not exist.\n")
        except Exception as e:
            #Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")

def output(query):
    global tbl
    ans = pd.read_sql(query, engine)
    if ans.empty:
        print("\n--- không có dữ liệu ---\n")
    else:
        df = pd.DataFrame(ans)
        tbl = pd.concat([tbl, df], axis=0)
        print(df)
        print()

def existsMH():
    id = input("MAMH: ")
    query = f"select MAMH from MONHOC where MAMH='{id}'"
    ans = pd.read_sql(query, engine)
    if ans.empty:
        return False, id
    else:
        return True, id

def foo(id):
    print(f"\n--- không có MAMH '{id}' trong CSDL ---\n")

def clist():
    print("\nDanh sách lớp môn học:")
    query = f"select * from GIANGDAY order by MAMH, NAM, HOCKY"
    output(query)

def gradebook():
    exist, id = existsMH()
    if exist is True:
        print(f"\nBảng điểm MAMH '{id}':")
        query = f"select * from KETQUATHI where MAMH='{id}' order by MAHV, NGTHI"
        output(query)
    else:
        foo(id)

def cview():
    global tbl
    id = input("MAMH: ")
    query = f"select * from MONHOC where MAMH='{id}'"
    df = pd.DataFrame(pd.read_sql(query, engine))
    if not df.empty:
        tbl = pd.concat([tbl, df], axis=0)
        print(df)
        print()
    else:
        foo(id)

def promptMH():
    print("\nTENMH, TCLT, TCTH, MAKHOA")
    print("Lorem Ipsum, 3, 1, HTTT\n")
    input_string = input("Nhập dữ liệu môn học theo format trên: ")
    i = input_string.split(', ')
    return i

def MHaed(select):
    MHtbl = Table('MONHOC', metadata, autoload_with=engine)
    if select == 5:
        print("Nhập MAMH cần update dữ liệu:")
        exist, id = existsMH()
        if exist is True:
            print()
            query = f"select * from MONHOC where MAMH='{id}'"
            ans = pd.read_sql(query, engine)
            print(pd.DataFrame(ans).to_string(index=False))
            i = promptMH()
            stmt = update(MHtbl).where(MHtbl.c.MAMH == id).values(TENMH=i[0], TCLT=i[1], TCTH=i[2], MAKHOA=i[3])
            try:
                with engine.connect() as connection:
                    connection.execute(stmt)
                    connection.commit()
                print(f"\n--- đã update dữ liệu của MAMH '{id}' ---\n")
            except (SQLAlchemyError, DBAPIError) as e:
                print("\n", e, "\n")
        else:
            foo(id)
    elif select == 6:
        print("Nhập MAMH cần thêm vào CSDL:")
        exist, id = existsMH()
        if exist is False:
            i = promptMH()
            data = {'MAMH': [id], 'TENMH': [i[0]], 'TCLT': [i[1]], 'TCTH': [i[2]], 'MAKHOA': [i[3]]}
            df = pd.DataFrame(data)
            try:
                df.to_sql('MONHOC', con=engine, if_exists='append', index=False)
                print(f"\n--- đã thêm MAMH '{id}' vào CSDL ---\n")
            except Exception as e:
                print("\n", e, "\n")
        else:
            print(f"\n--- đã có MAMH '{id}' trong CSDL, hãy nhập MAMH khác ---\n")
    elif select == 7:
        print(("Nhập MAMH của môn học muốn xóa:"))
        exist, id = existsMH()
        if exist is True:
            stmt = delete(MHtbl).where(MHtbl.c.MAMH == id)
            try:
                with engine.connect() as connection:
                    connection.execute(stmt)
                    connection.commit()
                print(f"\n--- đã xóa MAMH '{id}' khỏi CSDL ---\n")
            except (SQLAlchemyError, DBAPIError) as e:
                print("\n", e, "\n")
        else:
            foo(id)