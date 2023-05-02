import subprocess

# import infomation of MySQL server
ip = input("Nhập địa chỉ IP của MySQL server(default : localhost): ")
if ip == '':
    ip = 'localhost'
port = input("Nhập cổng của MySQL server(default: 3306): ")
if port == '':
    port = '3306'
user = input("Nhập tên người dùng MySQL: ")
if user == '':
    print("Tên người dùng không được để trống")
    exit(0)
    
password = input("Nhập mật khẩu MySQL: ")
if password == '':
    print("Mật khẩu không được để trống")
    exit(0)
    
name = input("Nhập tên cơ sở dữ liệu mới: ")
if name == '':
    print("Tên cơ sở dữ liệu không được để trống")
    exit(0)

try:
    result = subprocess.run(['mysql', '--version'], capture_output=True, text=True)
    print(result.stdout)
except FileNotFoundError:
    print("MySQL chưa được cài đặt trên hệ thống. vui lòng cài đặt MySQL trước khi tiếp tục")

# Create database on MySQL server
cmd = f"mysql -h {ip} -P {port} -u {user} -p{password} -e 'CREATE DATABASE {name};'"
subprocess.run(cmd, shell=True)
