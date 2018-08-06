import random
from datetime import datetime


def get_ticket():
    # 生成session id的随机数
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    ticket = ''
    for i in range(50):
        ticket += random.choice(s)
    return ticket


# 获得随机订单号的时间戳
def get_order_num():
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    num = ''
    for i in range(50):
        num += random.choice(s)
    order_time = datetime.now().strftime('%Y%m%d%H%M%S')

    return order_time + num
