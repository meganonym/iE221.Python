import DBConnect
engine = DBConnect.connect()
import pandas as pd
tbl = None

def switch():
    global tbl
    while True:
        print("----- Khoa - Lớp - DML -----")
        print("1. Danh Sách Khoa")
        print("2. Danh Sách Lớp Học Viên")
        print("3. Danh Sách Học Viên 1 Lớp")
        print("4. 35 DQL")
        print("5. 4 DML")
        print("----------------------------")
        try:
            select = int(input("\nChọn tác vụ số: "))
            if select == 1:
                query = f"select * from KHOA"
                print("\nDanh Sách Khoa:")
                output(query)
            elif select == 2:
                query = f"select * from LOP"
                print("\nDanh Sách Lớp Học Viên:")
                output(query)
            elif select == 3:
                hvlist()
            elif select == 4:
                print()
                dql35()
            elif select == 5:
                dml4()
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

def existsLop():
    print("\nNhập 2 chữ số cuối của MALOP:")
    id = f"K{input("K")}"
    query = f"select MALOP from LOP where MALOP='{id}'"
    ans = pd.read_sql(query, engine)
    if ans.empty:
        return False, id
    else:
        return True, id

def hvlist():
    exist, id = existsLop()
    if exist is True:
        print(f"\nDanh sách học viên lớp '{id}':")
        query = f"select * from HOCVIEN where MAHV like '{id}__'"
        output(query)
        query = f"select TRGLOP from LOP where MALOP='{id}'"
        crid = pd.DataFrame(pd.read_sql(query, engine)).at[0, 'TRGLOP']
        print(f"MAHV lớp trưởng lớp '{id}': ", crid, "\n")
        import student
        while True:
            cont = input("Xem dữ liệu học viên? Y/N: ")
            if cont == "Y" or cont == "y":
                student.sview()
            else:
                print()
                break
    else:
        print(f"\n--- không tồn tại MALOP '{id}' trong CSDL ---\n")

def dql35():
    while True:
        print("---------- 35 Câu Truy Vấn Chi Tiết ----------")
        select = int(input("\nChọn câu truy vấn số: "))

        if select == 1:
            query = f"SELECT hv.MAHV, (HO+' '+TEN) AS fullName, hv.NGSINH, l.MALOP FROM LOP l, HOCVIEN hv WHERE l.TRGLOP = hv.MAHV"
            print("\nDanh sách (mã học viên, họ tên, ngày sinh, mã lớp) lớp trưởng của các lớp:")
        elif select == 2:
            query = (f"SELECT hv.MAHV, (HO+' '+TEN) AS fullName, kq.LANTHI, kq.DIEM FROM KETQUATHI kq, HOCVIEN hv"
                     + f" WHERE hv.MAHV = kq.MAHV AND MALOP = 'K12' AND MAMH = 'CTRR' ORDER BY TEN, HO")
            print("\nBảng điểm thi (mã học viên, họ tên , lần thi, điểm số) môn CTRR của lớp “K12”, sắp xếp theo tên, họ học viên:")
        elif select == 3:
            query = (f"SELECT hv.MAHV, (HO+' '+TEN) AS fullName, kq.MAMH FROM KETQUATHI kq, HOCVIEN hv"
                     + f" WHERE hv.MAHV = kq.MAHV AND LANTHI = 1 AND KQUA = 'Dat' ORDER BY fullName")
            print("\nDanh sách những học viên (mã học viên, họ tên) và những môn học mà học viên đó thi lần thứ nhất đã đạt:")
        elif select == 4:
            query = (f"SELECT hv.MAHV, (HO+' '+TEN) AS fullName FROM KETQUATHI kq, HOCVIEN hv"
                     + f" WHERE hv.MAHV = kq.MAHV AND MALOP='K11' AND MAMH = 'CTRR' AND LANTHI = 1 AND KQUA = 'Khong Dat' ORDER BY hv.MAHV")
            print("\nDanh sách học viên (mã học viên, họ tên) của lớp “K11” thi môn CTRR không đạt (ở lần thi 1):")
        elif select == 5:
            query = (f"SELECT DISTINCT hv.MAHV, (HO+' '+TEN) AS fullName FROM KETQUATHI kq, HOCVIEN hv"
                     + f" WHERE hv.MAHV = kq.MAHV AND MALOP LIKE 'K%' AND MAMH = 'CTRR'"
                     + f" AND NOT EXISTS(SELECT * FROM KETQUATHI WHERE MAHV = hv.MAHV AND MAMH='CTRR' AND KQUA='Dat') ORDER BY hv.MAHV")
            print("\nDanh sách học viên (mã học viên, họ tên) của lớp “K” thi môn CTRR không đạt (ở tất cả các lần thi):")
        elif select == 6:
            query = f"SELECT DISTINCT MAMH FROM GIANGDAY gd, GIAOVIEN gv WHERE gd.MAGV = gv.MAGV AND HOTEN = 'Tran Tam Thanh' AND HOCKY = 1 AND NAM = 2006"
            print("\nTên những môn học mà giáo viên có tên “Tran Tam Thanh” dạy trong học kỳ 1 năm 2006:")
        elif select == 7:
            query = f"SELECT MAMH FROM GIANGDAY gd, GIAOVIEN gv, LOP l WHERE gd.MAGV = gv.MAGV AND HOCKY = 1 AND NAM = 2006 AND gv.MAGV = l.MAGVCN AND l.MALOP = 'K11'"
            print("\nTên những môn học (mã môn học, tên môn học) mà giáo viên chủ nhiệm lớp “K11” dạy trong học kỳ 1 năm 2006:")
        elif select == 8:
            query = (f"SELECT MAHV, (HO+' '+TEN) AS fullName FROM GIANGDAY gd, GIAOVIEN gv, MONHOC mh, LOP l, HOCVIEN hv"
                     + f" WHERE gd.MAGV = gv.MAGV AND HOTEN = 'Nguyen To Lan' AND gd.MAMH = mh.MAMH AND TENMH = 'Co So Du Lieu' AND gd.MALOP = l.MALOP AND l.TRGLOP = hv.MAHV")
            print("\nHọ tên lớp trưởng của các lớp mà giáo viên có tên “Nguyen To Lan” dạy môn “Co So Du Lieu”:")
        elif select == 9:
            query = f"SELECT M2.MAMH, M2.TENMH FROM DIEUKIEN dk, MONHOC M1, MONHOC M2 WHERE dk.MAMH = M1.MAMH AND M1.TENMH = 'Co So Du Lieu' AND dk.MAMH_TRUOC = M2.MAMH"
            print("\nDanh sách các môn học (mã môn học, tên môn học) phải học liền trước môn “Co So Du Lieu”:")
        elif select == 10:
            query = f"SELECT M2.MAMH, M2.TENMH FROM DIEUKIEN dk, MONHOC M1, MONHOC M2 WHERE dk.MAMH_TRUOC = M1.MAMH AND M1.TENMH = 'Cau Truc Roi Rac' AND dk.MAMH = M2.MAMH"
            print("\nMôn “Cau Truc Roi Rac” là môn bắt buộc phải học liền trước những môn học (mã môn học, tên môn học):")
        elif select == 11:
            query = (f"SELECT HOTEN FROM GIANGDAY gd, GIAOVIEN gv"
                     + f" WHERE gd.MAGV = gv.MAGV AND MAMH = 'CTRR' AND MALOP = 'K11' AND HOCKY = 1 AND NAM = 2006"
                     + f" INTERSECT"
                     + f" SELECT HOTEN FROM GIANGDAY gd, GIAOVIEN gv WHERE gd.MAGV = gv.MAGV AND MAMH = 'CTRR' AND MALOP = 'K12' AND HOCKY = 1 AND NAM = 2006")
            print("\nHọ tên giáo viên dạy môn CTRR cho cả hai lớp “K11” và “K12” trong cùng học kỳ 1 năm 2006:")
        elif select == 12:
            query = (f"SELECT hv.MAHV, (HO+' '+TEN) AS fullName FROM KETQUATHI K1, HOCVIEN hv"
                     + f" WHERE K1.MAHV = hv.MAHV AND MAMH = 'CSDL' AND LANTHI = 1 AND KQUA = 'Khong Dat'"
                     + f" AND K1.MAHV NOT IN (SELECT MAHV FROM KETQUATHI K2 WHERE K2.LANTHI > 1)")
            print("\nDanh sách học viên (mã học viên, họ tên) thi không đạt môn CSDL ở lần thi thứ 1 nhưng chưa thi lại môn này:")
        elif select == 13:
            query = f"SELECT MAGV, HOTEN FROM GIAOVIEN WHERE MAGV NOT IN (SELECT MAGV FROM GIANGDAY)"
            print("\nDanh sách giáo viên (mã giáo viên, họ tên) không được phân công giảng dạy bất kỳ môn học nào:")
        elif select == 14:
            query = (f"SELECT MAGV, HOTEN FROM GIAOVIEN WHERE MAGV NOT IN"
                     + f" (SELECT gd.MAGV 	FROM GIANGDAY gd, MONHOC mh, GIAOVIEN gv"
                     + f" WHERE gd.MAGV = gv.MAGV AND gd.MAMH = mh.MAMH AND gv.MAKHOA = mh.MAKHOA)")
            print("\nDanh sách giáo viên (mã giáo viên, họ tên) không được phân công giảng dạy bất kỳ môn học nào thuộc khoa giáo viên đó phụ trách:")
        elif select == 15:
            query = (f"SELECT MAHV, (HO+' '+TEN) AS fullName FROM HOCVIEN WHERE MALOP = 'K11'"
                     + f" AND MAHV IN (SELECT kq.MAHV FROM KETQUATHI kq, HOCVIEN hv"
                     + f" WHERE kq.MAHV = hv.MAHV AND MAMH = 'CTRR' AND LANTHI = 2 AND DIEM = 5 )"
                     + f" UNION"
                     + f" SELECT DISTINCT hv.MAHV, (HO+' '+TEN) AS fullName"
                     + f" FROM HOCVIEN hv"
                     + f" WHERE MALOP = 'K11' AND hv.MAHV IN"
                     + f" (SELECT MAHV	FROM KETQUATHI WHERE KQUA = 'Khong Dat'	GROUP BY MAHV, MAMH	HAVING COUNT(*) >= 3)")
            print("\nHọ tên các học viên thuộc lớp “K11” thi một môn bất kỳ quá 3 lần vẫn “Khong dat” hoặc thi lần thứ 2 môn CTRR được 5 điểm:")
        elif select == 16:
            query = (f"SELECT gv.MAGV, HOTEN FROM GIANGDAY gd, GIAOVIEN gv WHERE gd.MAGV = gv.MAGV AND MAMH = 'CTRR'"
                     + f" GROUP BY gv.MAGV, HOTEN, NAM, HOCKY HAVING COUNT(*) >= 2")
            print("\nHọ tên các giáo viên dạy môn CTRR cho ít nhất hai lớp trong cùng một học kỳ của một năm học:")
        elif select == 17:
            query = (f"SELECT hv.* FROM KETQUATHI kq, HOCVIEN hv WHERE kq.MAHV = hv.MAHV AND MAMH = 'CSDL'"
                     + f" AND LANTHI = (SELECT MAX(LANTHI) FROM KETQUATHI WHERE MAHV = hv.MAHV AND MAMH = 'CSDL' GROUP BY MAHV)")
            print("\nDanh sách học viên và điểm thi môn CSDL (chỉ lấy điểm của lần thi sau cùng):")
        elif select == 18:
            query = (f"SELECT hv.*, DIEM FROM KETQUATHI kq, HOCVIEN hv, MONHOC mh"
                     + f" WHERE kq.MAHV = hv.MAHV AND kq.MAMH = mh.MAMH AND TENMH = 'Co So Du Lieu'"
                     + f" AND DIEM = (SELECT MAX(DIEM) FROM KETQUATHI WHERE MAHV = hv.MAHV AND MAMH = 'CSDL' GROUP BY MAHV)")
            print("\nDanh sách học viên và điểm thi môn “Co So Du Lieu” (chỉ lấy điểm cao nhất của các lần thi):")
        elif select == 19:
            query = (f"SELECT MAKHOA, TENKHOA FROM KHOA WHERE NGTLAP = (SELECT MIN(NGTLAP) FROM KHOA)")
            print("\nKhoa (mã khoa, tên khoa) được thành lập sớm nhất:")
        elif select == 20:
            query = (f"SELECT COUNT(*) AS 'số lượng”' FROM GIAOVIEN WHERE HOCHAM IN ('GS', 'PGS')")
            print("\nSố giáo viên có học hàm là “GS” hoặc “PGS”:")
        elif select == 21:
            query = (f"SELECT MAKHOA, COUNT(*) FROM GIAOVIEN WHERE HOCVI IN ('CN', 'KS', 'ThS', 'TS', 'PTS') GROUP BY MAKHOA")
            print("\nSố giáo viên có học vị là “CN”, “KS”, “Ths”, “TS”, “PTS” trong mỗi khoa:")
        elif select == 22:
            query = (f"SELECT MAMH, KQUA, COUNT(*) AS 'số học viên' FROM KETQUATHI GROUP BY MAMH, KQUA ORDER BY MAMH")
            print("\nSố lượng học viên theo kết quả (đạt và không đạt) mỗi môn học:")
        elif select == 23:
            query = (f"SELECT DISTINCT gv.MAGV, HOTEN FROM GIAOVIEN gv, LOP l, GIANGDAY gd"
                     + f" WHERE gv.MAGV = l.MAGVCN AND gv.MAGV = gd.MAGV AND l.MALOP = gd.MALOP")
            print("\nDanh sách giáo viên (mã giáo viên, họ tên) là giáo viên chủ nhiệm của một lớp, đồng thời dạy cho lớp đó ít nhất một môn học:")
        elif select == 24:
            query = (f"SELECT MAHV, (HO+' '+TEN) AS fullName FROM HOCVIEN hv, LOP l WHERE hv.MAHV = l.TRGLOP AND SISO = (SELECT MAX(SISO) FROM LOP)")
            print("\nHọ tên lớp trưởng của lớp có sỉ số cao nhất:")
        elif select == 25:
            query = (f"SELECT (HO+' '+TEN) AS fullName FROM HOCVIEN hv, LOP l, KETQUATHI kq"
                     + f" WHERE hv.MAHV = l.TRGLOP AND hv.MAHV = kq.MAHV AND KQUA = 'Khong Dat'"
                     + f" GROUP BY hv.MAHV, HO, TEN HAVING COUNT(*) >= 3")
            print("\nHọ tên những LOPTRG thi không đạt quá 3 môn (mỗi môn đều thi không đạt ở tất cả các lần thi):")
        elif select == 26:
            query = (f"SELECT TOP 1 WITH TIES hv.MAHV, (HO+' '+TEN) AS fullName FROM HOCVIEN hv, KETQUATHI kq"
                     + f" WHERE hv.MAHV = kq.MAHV AND DIEM >= 9 GROUP BY hv.MAHV, HO, TEN ORDER BY COUNT(*) DESC")
            print("\nDanh sách học viên (mã học viên, họ tên) có số môn đạt điểm 9,10 nhiều nhất:")
        elif select == 27:
            query = (f"SELECT TOP 1 WITH TIES hv.MALOP, hv.MAHV, (HO+' '+TEN) AS fullName FROM HOCVIEN hv, KETQUATHI kq"
                     + f" WHERE hv.MAHV = kq.MAHV AND DIEM >= 9 GROUP BY hv.MALOP, hv.MAHV, HO, TEN ORDER BY COUNT(*) DESC")
            print("\nDanh sách học viên (mã học viên, họ tên) có số môn đạt điểm 9,10 nhiều nhất trong từng lớp:")
        elif select == 28:
            query = (f"SELECT MAGV, COUNT(DISTINCT MAMH) AS 'số môn', COUNT(DISTINCT MALOP) AS 'số lớp' FROM GIANGDAY GROUP BY MAGV")
            print("\nSố môn học, số lớp mỗi giáo viên được phân công dạy trong từng học kỳ của từng năm:")
        elif select == 29:
            query = (f"SELECT TOP 1 WITH TIES NAM, HOCKY, MAGV FROM GIANGDAY GROUP BY NAM, HOCKY, MAGV ORDER BY COUNT(*) DESC")
            print("\nDanh sách giáo viên (mã giáo viên, họ tên) giảng dạy nhiều nhất trong từng học kỳ của từng năm:")
        elif select == 30:
            query = (f"SELECT TOP 1 WITH TIES mh.MAMH, TENMH FROM KETQUATHI kq, MONHOC mh"
                     + f" WHERE kq.MAMH = mh.MAMH AND LANTHI = 1 AND KQUA = 'Khong Dat' GROUP BY mh.MAMH, TENMH ORDER BY COUNT(*) DESC")
            print("\nDanh sách môn học (mã môn học, tên môn học) có nhiều học viên thi không đạt (ở lần thi thứ 1) nhất:")
        elif select == 31:
            query = (f"SELECT DISTINCT hv.MAHV, (HO+' '+TEN) AS fullName FROM HOCVIEN hv, KETQUATHI K1"
                     + f" WHERE hv.MAHV = K1.MAHV AND KQUA = 'Dat'"
                     + f" AND hv.MAHV NOT IN"
                     + f" (SELECT MAHV	FROM KETQUATHI K2	WHERE K2.MAHV = hv.MAHV AND LANTHI = 1 AND KQUA = 'Khong Dat')")
            print("\nDanh sách học viên (mã học viên, họ tên) thi môn nào cũng đạt (chỉ xét lần thi thứ 1):")
        elif select == 32:
            query = (f"SELECT DISTINCT hv.MAHV, (HO+' '+TEN) AS fullName FROM HOCVIEN hv, KETQUATHI K1"
                     + f" WHERE hv.MAHV = K1.MAHV AND KQUA = 'Dat'"
                     + f" AND K1.MAMH NOT IN"
                     + f" (SELECT MAMH	FROM KETQUATHI K2 WHERE MAHV = hv.MAHV AND KQUA = 'Khong Dat'"
                     + f" AND LANTHI = (SELECT MAX(LANTHI) FROM KETQUATHI K2 WHERE MAHV = hv.MAHV AND MAMH = K1.MAMH GROUP BY MAHV))")
            print("\nDanh sách học viên (mã học viên, họ tên) thi môn nào cũng đạt (chỉ xét lần thi thứ 1):")
        elif select == 33:
            query = (f"SELECT hv.MAHV, (HO+' '+TEN) AS fullName FROM HOCVIEN hv"
                     + f" WHERE NOT EXISTS"
                     + f" (SELECT MAMH	FROM MONHOC mh	WHERE MAMH NOT IN"
                     + f" (SELECT MAMH FROM KETQUATHI kq WHERE kq.MAHV = hv.MAHV AND KQUA = 'Dat' AND LANTHI = 1))")
            print("\nDanh sách học viên (mã học viên, họ tên) đã thi tất cả các môn đều đạt (chỉ xét lần thi thứ 1):")
        elif select == 34:
            query = (f"SELECT hv.MAHV, (HO+' '+TEN) AS fullName FROM HOCVIEN hv"
                     + f" WHERE NOT EXISTS"
                     + f" (SELECT MAMH FROM MONHOC mh	WHERE MAMH NOT IN"
                     + f" (SELECT MAMH FROM KETQUATHI kq WHERE kq.MAHV = hv.MAHV AND KQUA = 'Dat'"
                     + f" AND LANTHI = (SELECT MAX(LANTHI) FROM KETQUATHI WHERE MAHV = hv.MAHV AND MAMH = mh.MAMH GROUP BY MAHV)))")
            print("\nDanh sách học viên (mã học viên, họ tên) đã thi tất cả các môn đều đạt (chỉ xét lần thi sau cùng):")
        elif select == 35:
            query = (f"SELECT kq.MAMH, hv.MAHV, (HO + '  ' + TEN) AS fullName, DIEM FROM KETQUATHI kq, HOCVIEN hv,"
                     + f" (SELECT MAMH, MAX(DIEM) AS maxGrade FROM"
                     + f" (SELECT K2.MAMH, K2.MAHV, K2.DIEM "
                     + f" FROM KETQUATHI K2, (SELECT MAMH, MAHV, MAX(LANTHI) AS lanThiCuoi FROM KETQUATHI K1 GROUP BY MAMH, MAHV)  AS lastTry"
                     + f" WHERE K2.MAMH = lastTry.MAMH AND K2.MAHV = lastTry.MAHV AND K2.LANTHI = lastTry.lanThiCuoi"
                     + f" GROUP BY K2.MAMH, K2.MAHV, K2.DIEM) AS A"
                     + f" GROUP BY MAMH) AS B WHERE kq.MAHV = hv.MAHV AND kq.MAMH = B.MAMH AND DIEM = B.maxGrade"
                     + f" AND kq.LANTHI = (SELECT MAX(LANTHI) FROM KETQUATHI WHERE MAHV = hv.MAHV AND MAMH = kq.MAMH GROUP BY MAHV) ORDER BY MAMH, hv.MAHV")
            print("\nDanh sách học viên (mã học viên, họ tên) có điểm thi cao nhất trong từng môn (lấy điểm ở lần thi sau cùng):")
        else:
            print()
            break
        output(query)

def dml4():
    while True:
        print("\n---------- 4 DML queries, ngôn ngữ thao tác dữ liệu ----------")
        select = int(input("\nChọn câu truy vấn số: "))

        if select == 1:
            print("\nTăng hệ số lương thêm 0.2 cho những giáo viên là trưởng khoa")
            query = f"UPDATE GIAOVIEN SET HESO = HESO + 0.2 WHERE MAGV IN (SELECT TRGKHOA FROM KHOA)"
        elif select == 2:
            print("\nCập nhật điểm trung bình tất cả môn học (DIEMTB) của mỗi học viên (tất cả các môn đều có hệ số 1 và nếu hv thi 1 môn nhiều lần, chỉ lấy điểm lần thi sau cùng)")
            query = (f"UPDATE HOCVIEN SET DIEMTB ="
                     + f" (	SELECT AVG(DIEM) 	FROM KETQUATHI K1 	WHERE LANTHI ="
                       + f" (SELECT MAX(LANTHI) FROM KETQUATHI K2 WHERE K1.MAHV = K2.MAHV AND K1.MAMH = K2.MAMH GROUP BY MAHV, MAMH)"
                         + f"	GROUP BY MAHV HAVING MAHV = HOCVIEN.MAHV)")
        elif select == 3:
            print("\nCập nhật giá trị cho cột GHICHU là “Cam thi” đối với trường hợp: học viên có một môn bất kỳ thi lần thứ 3 dưới 5 điểm")
            query = (f"UPDATE HOCVIEN SET GHICHU = 'Cam thi'"
                     + f" WHERE MAHV IN("
                       + f"	SELECT MAHV	FROM KETQUATHI k WHERE k.MAHV = HOCVIEN.MAHV AND LANTHI = 3 AND DIEM < 5)")
        elif select == 4:
            print("\nCập nhật giá trị cho cột XEPLOAI trong quan hệ HOCVIEN như sau:")
            print("-- o Nếu DIEMTB ≥ 9 thì XEPLOAI =”XS”")
            print("-- o Nếu 8 ≤ DIEMTB < 9 thì XEPLOAI = “G”")
            print("-- o Nếu 6.5 ≤ DIEMTB < 8 thì XEPLOAI = “K”")
            print("-- o Nếu 5 ≤ DIEMTB < 6.5 thì XEPLOAI = “TB”")
            print("-- o Nếu DIEMTB < 5 thì XEPLOAI = ”Y”")
            query = (f"SELECT hv.MAHV, (HO+' '+TEN) AS fullName FROM KETQUATHI kq, HOCVIEN hv"
                     + f" WHERE hv.MAHV = kq.MAHV AND MALOP='K11' AND MAMH = 'CTRR' AND LANTHI = 1 AND KQUA = 'Khong Dat' ORDER BY hv.MAHV")
        else:
            print()
            break
        print("\n--- not yet implemented ---")