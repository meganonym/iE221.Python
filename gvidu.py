import DBConnect
engine = DBConnect.connect()
from sqlalchemy import MetaData, Table, delete, update
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
metadata = MetaData()
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

def switch():
    while True:
        print("----- TEACHER MANAGEMENT -----")
        print("1. Xem Danh Sách Giáo Viên")
        print("2. Xem Dữ Liệu 1 Giáo Viên")
        print("3. Sửa Dữ Liệu 1 Giáo Viên")
        print("4. Thêm 1 Giáo Viên Vào CSDL")
        print("5. Xóa Dữ Liệu 1 Giáo Viên")
        print("------------------------------")
        try:
            select = int(input("\nChọn tác vụ số: "))
            if select == 1:
                print("\nDanh Sách Giáo Viên:")
                query = f"select * from GIAOVIEN order by MAKHOA, GIOITINH, MAGV"
                df = pd.DataFrame(pd.read_sql(query, engine))
                print(df)
                try:
                    df.to_excel("admin.xlsx", sheet_name='qlhv', index=False)
                except PermissionError:
                    print("Error: Permission denied. The file 'admin.xlsx' might be open or you lack write permissions.\n")
                except FileNotFoundError:
                    print("Error: The directory for 'admin.xlsx' does not exist.\n")
                except Exception as e:
                    #Catch any other unexpected errors
                    print(f"An unexpected error occurred: {e}")
                print()
            elif select == 2:
                import teacher
                teacher.gview()
            elif select > 2 and select < 6:
                GVaed(select)
            else:
                print()
                break
        except ValueError:
            print("\nInvalid input. Please enter a valid integer.\n")

def existsGV():
    id = f"GV{input("GV")}"
    query = f"select MAGV from GIAOVIEN where MAGV='{id}'"
    ans = pd.read_sql(query, engine)
    if ans.empty:
        return False, id
    else:
        return True, id

def foo(id):
    print(f"\n--- không có MAGV '{id}' trong CSDL ---\n")

def promptGV():
    print("\nHOTEN, HOCVI, HOCHAM, GIOITINH, NGSINH, NGVL, HESO, MUCLUONG, MAKHOA")
    print("Lorem Ipsum, TS, GS, Nu, 2004/2/29, 2004/2/29, 5.00, 9999999, MTT")
    input_string = input("\nNhập dữ liệu GV theo format trên: ")
    i = input_string.split(', ')
    return i

def GVaed(select):
    GVtbl = Table('GIAOVIEN', metadata, autoload_with=engine)
    if select == 3:
        print("Nhập 2 chữ số cuối của MAGV cần update dữ liệu:")
        exist, id = existsGV()
        if exist is True:
            print()
            query = f"select * from GIAOVIEN where MAGV='{id}'"
            ans = pd.read_sql(query, engine)
            print(pd.DataFrame(ans).to_string(index=False))
            i = promptGV()
            stmt = update(GVtbl).where(GVtbl.c.MAGV == id).values(HOTEN=i[0], HOCVI=i[1], HOCHAM=i[2], GIOITINH=i[3], NGSINH=i[4],
                                                                  NGVL=i[5], HESO=i[6], MUCLUONG=i[7], MAKHOA=i[8])
            try:
                with engine.connect() as connection:
                    connection.execute(stmt)
                    connection.commit()
                print(f"\n--- đã update dữ liệu của MAGV '{id}' ---\n")
            except (SQLAlchemyError, DBAPIError) as e:
                print("\n", e, "\n")
        else:
            foo(id)
    elif select == 4:
        print("Nhập 2 chữ số cuối của MAGV cần thêm vào CSDL:")
        exist, id = existsGV()
        if exist is False:
            i = promptGV()
            data = {'MAGV': [id], 'HOTEN': [i[0]], 'HOCVI': [i[1]], 'HOCHAM': [i[2]], 'GIOITINH': [i[3]], 'NGSINH': [i[4]],
                    'NGVL': [i[5]], 'HESO': [i[6]], 'MUCLUONG': [i[7]], 'MAKHOA': [i[8]]}
            df = pd.DataFrame(data)
            try:
                df.to_sql('GIAOVIEN', con=engine, if_exists='append', index=False)
                print(f"\n--- đã thêm MAGV '{id}' vào CSDL ---\n")
            except Exception as e:
                print("\n", e, "\n")
        else:
            print(f"\n--- đã có MAGV '{id}' trong CSDL, hãy nhập MAGV khác ---\n")
    elif select == 5:
        print(("Nhập 2 chữ số cuối của MAGV muốn xóa:"))
        exist, id = existsGV()
        if exist is True:
            stmt = delete(GVtbl).where(GVtbl.c.MAGV == id)
            try:
                with engine.connect() as connection:
                    connection.execute(stmt)
                    connection.commit()
                print(f"\n--- đã xóa MAGV '{id}' khỏi CSDL ---\n")
            except (SQLAlchemyError, DBAPIError) as e:
                print("\n", e, "\n")
        else:
            foo(id)