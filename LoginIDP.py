import requests
import urllib
import getNetwork
import sys

if __name__ == "__main__":
    # 获取用户名和密码
    try:
        user_info = getNetwork.get_user_info()
    except:
        sys.exit(1)
    user_account = user_info[0]
    user_password = urllib.parse.quote(user_info[1])
    interface_name = user_info[2]
    print("读取到你的信息如下:")
    print("账号：{} 密码：{} 无线网卡：{}\n".format(user_account, user_info[1], interface_name))
    print("开始请求192.168.138.2, 请忽略弹出的警告\n")

    # 获取WLAN网卡IP地址
    key_name = getNetwork.get_key()
    try:
        wlan_user_ip = getNetwork.get_interface_info(key_name[interface_name])
    except KeyError:
        input("请检查输入的网卡名称,按Enter关闭程序")
        sys.exit(1)

    # 请求登录
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Referer": "https://192.168.138.2/"
    }
    url = "https://192.168.138.2:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account={0}&user_password={1}&wlan_user_ip={2}".format(user_account, user_password, wlan_user_ip)

    # 检查结果
    res = ""
    try:
        res = requests.get(url=url, headers=header, verify=False).text
    except Exception:
        print("还没有从IDP获取到IP地址，无法进行身份认证,请稍后再试")
        input("按Enter键关闭窗口....\n")
        sys.exit(1)
    if '"result":"1"' in res:
        print("脚本执行完毕,IDP登录认证完成")
    elif '"result":"0","msg":"","ret_code":2' in res:
        print("脚本执行完毕,登录失败,可能原因如下：")
        print("你已经登录了IDP")
    else:
        print("脚本执行完毕,登录失败,可能原因如下：")
        print("配置文件中的用户信息写入错误[账号|密码|无线网卡名称]，请按初始格式正确填写")
    input("按Enter键关闭窗口....\n")


