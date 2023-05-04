# hàm lấy ngày hôm nay
from datetime import datetime

def getToday():
    return datetime.today().strftime('%Y-%m-%d')

print(getToday())