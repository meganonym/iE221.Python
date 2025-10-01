import DBConnect
engine = DBConnect.connect()
import pandas as pd

def sview():
    print("\nNhập 4 chữ số cuối của MAHV:")
    id = f"K{input("K")}"

    query = f"select * from HOCVIEN where MAHV='{id}'"
    ans = pd.read_sql(query, engine)
    if ans.empty:
        print(f"\n--- không có MAHV '{id}' trong CSDL ---\n")
    else:
        print()
        output(id)

def output(id):
    query = f"SELECT * FROM HOCVIEN WHERE MAHV='{id}'"
    df1 = pd.DataFrame(pd.read_sql(query, engine))
    df = df1
    print(df1.to_string(index=False))
    query = f"select * from KETQUATHI where MAHV='{id}' ORDER BY NGTHI"
    ans = pd.read_sql(query, engine)
    if not ans.empty:
        fullName = df1.at[0, 'HO'] + ' ' + df1.at[0, 'TEN']
        print("\nBảng Điểm Học Viên - ", fullName, "- MAHV:", id)
        df2 = pd.DataFrame(ans)
        print(df2)
        df = pd.concat([df1, df2], axis=0)
    print()
    try:
        df.to_excel("student.xlsx", sheet_name=f"{id}", index=False)
    except PermissionError:
        print("Error: Permission denied. The file 'student.xlsx' might be open or you lack write permissions.\n")
    except FileNotFoundError:
        print("Error: The directory for 'student.xlsx' does not exist.\n")
    except Exception as e:
        #Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")