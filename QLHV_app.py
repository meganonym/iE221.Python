if __name__ == "__main__":
    while True:
        print("--- QUẢN LÝ HỌC VỤ ---")
        print("1. Administrator")
        print("2. Giáo Viên")
        print("3. Học Viên")
        print("----------------------")
        try:
            select = int(input("\nChọn loại user: "))
            if select == 1:
                print()
                import admin
                admin.adieu()
            elif select == 2:
                import teacher
                teacher.gview()
            elif select == 3:
                import student
                student.sview()
            else:
                break
        except ValueError:
            print("\nInvalid input. Please enter a valid integer.\n")