import pymysql

# Thiết lập các thông số kết nối đến database
host = 'your_host'
port = 3306 # default port for MySQL
user = 'your_username'
password = 'your_password'
database = 'your_database_name'

# Tạo kết nối đến database
conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)

# Tạo bảng mới trong database vừa tạo hoặc sử dụng một bảng đã tồn tại
with conn.cursor() as cursor:
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INT(11) PRIMARY KEY,
                      name VARCHAR(255) NOT NULL,
                      email VARCHAR(255) NOT NULL,
                      age INT(11))''')

# Lưu các thay đổi và đóng kết nối
conn.commit()
conn.close()
