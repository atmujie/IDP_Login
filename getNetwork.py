import netifaces as ni
import winreg as wr
import re
import sys

# 获取账号信息
def get_user_info():
    try:
        with open(r"config.txt", "r", encoding="UTF-8") as f:
            r = f.read()
            user_account = re.search(r"user_account='(.*)'", r).group(1)
            user_password = re.search(r"user_password='(.*)'", r).group(1)
            interface_name = re.search(r"interface_name='(.*)'", r).group(1)
            user_info = [user_account, user_password, interface_name]
    except FileNotFoundError:
        print("没有检索到配置文件config.txt,请将配置文件置于LoginIDP.exe同级目录")
        input("按Enter键关闭窗口....\n")
        sys.exit(1)
    return user_info


# 获取指定网卡接口唯一键名对应的IPv4地址
def get_interface_info(key_id):
    ipv4 = ""
    try:
        addresses = ni.ifaddresses(key_id)
        if ni.AF_INET in addresses:
            ipv4 = addresses[ni.AF_INET][0]['addr']
    except:
        print("IPv4地址获取失败")
    return ipv4


# 获取网卡接口唯一键名对应的网卡名映射
def get_key():
    inter_id = ni.interfaces()
    key_name = {}
    try:
        # 建立链接注册表，"HKEY_LOCAL_MACHINE"，None表示本地计算机
        reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
        # 打开网卡所在的key
        reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
    except Exception:
        input("注册表路径出错或者其他问题,按Enter结束程序")
        sys.exit(1)

    for i in inter_id:
        try:
            # 尝试读取每一个网卡键值下对应的Name
            reg_sub_key = wr.OpenKey(reg_key, i + r'\Connection')
            # 如果存在Name，写入key_name字典
            key_name[wr.QueryValueEx(reg_sub_key, 'Name')[0]] = i
        except FileNotFoundError:
            pass
    return key_name
