from DrissionPage import ChromiumPage, ChromiumOptions
import time
import requests
import subprocess


ueername='' #natfrp登录用户名
password='' #natfrp登录密码
remark=''   #隧道备注
link_password='' #SakuraFrp客户端密码
access_password=''#SakuraFrp隧道密码
ip_port=''  #访问地址 域名:端口 可在隧道列表页点击端口号复制 示例 frp.top:1111

RDP_command = [
    'mstsc',
    '/v:'+ip_port,  # 指定服务器和端口
    '/admin'
]
def switch_tunnel_state(switch):
 
    try:
        options=ChromiumOptions()
        options.headless()
        options.set_user('NatFRP')
        page = ChromiumPage(options)
        page.get('https://www.natfrp.com/remote/v2')

        if (page.url !='https://www.natfrp.com/remote/v2'):
            page.quit()
            options.clear_arguments()
            options.set_argument('--window-size', '800,600')
            options.set_user('NatFRP')
            page = ChromiumPage(options)
            page.get('https://www.natfrp.com/remote/v2')
            time.sleep(1)
    
        if (page.url == "https://openid.13a.com/login"):
            for i in range(3):
                page.ele('#username').clear()
                page.ele('#password').clear()
                page.ele('#username').input(ueername)
                page.ele('#password').input(password)
                page.ele('#login').click()
                page.wait.load_start()
                if (page.url != 'https://openid.13a.com/login'):
                    time.sleep(1)
                    page.get('https://www.natfrp.com/remote/v2')
                    break

        if (page.ele('.adult-check', timeout=0.1)):
            page.ele('.yes').click()

        if (page.ele('tag:a@text():关闭', timeout=0.1)):
            print(page.eles('tag:a@text()=关闭')[1].click(by_js=None))            

        if (page.url == "https://www.natfrp.com/remote/v2"):
            page.ele('.n-input__input-el').input(link_password)
            time.sleep(1)
            page.ele('.n-base-wave').click()
            enable_area = page.eles('.tunnel-grid')[0]
            disable_area = page.eles('.tunnel-grid')[1]
            tunnel = page.ele('tag:span@text():'+remark).parent(6)
            if switch:
                tunnel.drag_to(enable_area)
            else:
                tunnel.drag_to(disable_area)
            time.sleep(1)

    finally:
        page.quit()
def auth():
    url = 'https://'+ip_port+'/'

    data = {
        'pw': access_password,
        'csrf': '0000000000000000',
        'persist_auth': 'on'
    }

    response = requests.post(url,  data=data, verify=False)
    if (response.status_code==200 and '认证成功' in response.text):
        print("认证成功")
        return True
    else:
        print("认证失败")
        return False
    
def RDP():
    RDP_link = subprocess.Popen(RDP_command)
    RDP_link.wait()
try:
    switch_tunnel_state(True)
    auth()

    RDP()
finally:
    print("即将断开隧道")
    switch_tunnel_state(False)
    print("隧道断开成功")
