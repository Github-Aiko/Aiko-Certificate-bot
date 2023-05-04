import subprocess

def check_mysql_installed():
    try:
        subprocess.check_call(['mysql', '--version'])
        return True
    except subprocess.CalledProcessError:
        return False
    
def add_table():
    import mysql.connector

    # Connect to MySQL server
    cnx = mysql.connector.connect(user='user', password='password', host='localhost', database='mysql')

    # Tạo cơ sở dữ liệu
    cursor = cnx.cursor()
    create_database_query = f'CREATE DATABASE {name}'
    cursor.execute(create_database_query)
    cnx.database = name

    # Tạo bảng plan
    create_plan_table_query = 'CREATE TABLE `plan` (`id` int(11) NOT NULL AUTO_INCREMENT, `name` varchar(255) NOT NULL, `price` decimal(10,2) NOT NULL, `status` tinyint(1) NOT NULL DEFAULT \'0\', PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
    cursor.execute(create_plan_table_query)

    # Tạo bảng user
    create_user_table_query = 'CREATE TABLE `user` (`id` int(11) NOT NULL AUTO_INCREMENT, `udid_apple` varchar(50) NOT NULL, `type_of_device` varchar(50) NOT NULL, `telegram_id` varchar(50) DEFAULT NULL, `purchase_date` date DEFAULT NULL, `date_update` date DEFAULT NULL, `wait` date NOT NULL DEFAULT \'1970-01-01\', PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
    cursor.execute(create_user_table_query)

    cursor.close()
    cnx.close()


def create_database(ip='localhost', port='3306', user=None, password=None, name=None):
    # Kiểm tra nếu tên người dùng và mật khẩu được cung cấp
    if not user:
        print("Tên người dùng không được để trống")
        return
    if not password:
        print("Mật khẩu không được để trống")
        return
    if not name:
        print("Tên cơ sở dữ liệu không được để trống")
        return
    
    # Kiểm tra nếu MySQL đã được cài đặt trên hệ thống
    if not check_mysql_installed():
        print("MySQL chưa được cài đặt trên hệ thống. vui lòng cài đặt MySQL trước khi tiếp tục")
        return
    
    # Tạo cơ sở dữ liệu trên máy chủ MySQL
    cmd = f"mysql -h {ip} -P {port} -u {user} -p{password} -e 'CREATE DATABASE {name};'"
    try:
        subprocess.check_call(cmd, shell=True)
        print(f"Đã tạo cơ sở dữ liệu {name} thành công trên MySQL server {ip}:{port}")
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi tạo cơ sở dữ liệu {name}: {e}")

# Nhập thông tin từ người dùng
ip = input("Nhập địa chỉ IP của MySQL server(default : localhost): ")
if ip == '':
    ip = 'localhost'

port = input("Nhập cổng của MySQL server(default: 3306): ")
if port == '':
    port = '3306'

user = input("Nhập tên người dùng MySQL: ")
password = input("Nhập mật khẩu MySQL: ")
name = input("Nhập tên cơ sở dữ liệu mới: ")

# Tạo cơ sở dữ liệu
create_database(ip, port, user, password, name)
add_table()
