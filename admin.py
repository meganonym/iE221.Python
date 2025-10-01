def adieu():
    while True:
        print("------------ ADMIN ------------")
        print("1. Khoa - Lớp - 35 DQL - 4 DML")
        print("2. Môn Học ")
        print("3. Giáo Viên")
        print("4. Học Viên")
        print("-------------------------------")
        try:
            select = int(input("\nChọn nhánh: "))
            print()
            if select == 1:
                import faculty
                faculty.switch()
            elif select == 2:
                import course
                course.switch()
            elif select == 3:
                import gvidu
                gvidu.switch()
            elif select == 4:
                import hvidu
                hvidu.switch()
            else:
                break
        except ValueError:
            print("\nInvalid input. Please enter a valid integer.\n")