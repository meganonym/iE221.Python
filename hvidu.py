import DBConnect
engine = DBConnect.connect()
from sqlalchemy import MetaData, Table, delete, update
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
metadata = MetaData()
import pandas as pd

def switch():
    while True:
        print("----- STUDENT MANAGEMENT -----")
        print("1. Xem Dữ Liệu 1 Học Viên")
        print("2. Sửa Dữ Liệu 1 Học Viên")
        print("3. Thêm 1 Học Viên Vào CSDL")
        print("4. Xóa Dữ Liệu 1 Học Viên")
        print("------------------------------")
        try:
            select = int(input("\nChọn tác vụ số: "))
            if select == 1:
                import student
                student.sview()
            elif select > 1 and select < 5:
                HVaed(select)
            else:
                print()
                break
        except ValueError:
            print("\nInvalid input. Please enter a valid integer.\n")

def existsHV():
    id = f"K{input("K")}"
    query = f"select MAHV from HOCVIEN where MAHV='{id}'"
    ans = pd.read_sql(query, engine)
    if ans.empty:
        return False, id
    else:
        return True, id

def foo(id):
    print(f"\n--- không có MAHV '{id}' trong CSDL ---\n")

def promptHV():
    print("\nHO, TEN, NGSINH, GIOITINH, NOISINH, MALOP")
    print("Lorem, Ipsum, 2004/2/29, Nam, Demacia, K13")
    input_string = input("\nNhập dữ liệu HV theo format trên: ")
    i = input_string.split(', ')
    return i

def HVaed(select):
    HVtbl = Table('HOCVIEN', metadata, autoload_with=engine)
    if select == 2:
        print("Nhập 4 chữ số cuối của MAHV cần update dữ liệu:")
        exist, id = existsHV()
        if exist is True:
            print()
            query = f"select * from HOCVIEN where MAHV='{id}'"
            ans = pd.read_sql(query, engine)
            print(pd.DataFrame(ans).to_string(index=False))
            i = promptHV()
            stmt = update(HVtbl).where(HVtbl.c.MAHV == id).values(HO=i[0], TEN=i[1], NGSINH=i[2], GIOITINH=i[3], NOISINH=i[4], MALOP=i[5])
            try:
                with engine.connect() as connection:
                    connection.execute(stmt)
                    connection.commit()
                    print(f"\n--- đã update dữ liệu của MAHV '{id}' ---\n")
            except (SQLAlchemyError, DBAPIError) as e:
                print("\n", e, "\n")
        else:
            foo(id)
    elif select == 3:
        print("Nhập 4 chữ số cuối của MAHV cần thêm vào CSDL:")
        exist, id = existsHV()
        if exist is False:
            i = promptHV()
            data = {'MAHV': [id], 'HO': [i[0]], 'TEN': [i[1]], 'NGSINH': [i[2]], 'GIOITINH': [i[3]], 'NOISINH': [i[4]], 'MALOP': [i[5]]}
            df = pd.DataFrame(data)
            try:
                df.to_sql('HOCVIEN', con=engine, if_exists='append', index=False)
                print(f"\n--- đã thêm MAHV '{id}' vào CSDL ---\n")
            except Exception as e:
                print("\n", e, "\n")
        else:
            print(f"\n--- đã có MAHV '{id}' trong CSDL, hãy nhập MAHV khác ---\n")
    elif select == 4:
        print(("Nhập 4 chữ số cuối của MAHV muốn xóa:"))
        exist, id = existsHV()
        if exist is True:
            stmt = delete(HVtbl).where(HVtbl.c.MAHV == id)
            try:
                with engine.connect() as connection:
                    connection.execute(stmt)
                    connection.commit()
                print(f"\n--- đã xóa MAHV '{id}' khỏi CSDL ---\n")
            except (SQLAlchemyError, DBAPIError) as e:
                print("\n", e, "\n")
        else:
            foo(id)