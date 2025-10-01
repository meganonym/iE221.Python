def connect():
    try:
        from sqlalchemy.engine import URL, create_engine
        connection_string = "Trusted_Connection={Yes};DRIVER={ODBC Driver 13 for SQL Server};SERVER={LAPTOP-O53V65GC\\SQLEXPRESS};DATABASE={QuanLyGiaoVu}"
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        return create_engine(connection_url)
    except Exception as e:
        print("error in connection", e)