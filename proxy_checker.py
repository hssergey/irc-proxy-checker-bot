
import requests, sys
import socket
import traceback
import settings

tor_ips = []

def check_dnsbl(ip):
    # API, через который происходит проверка
    url = 'http://www.ip-score.com/ajax_handler/get_bls'
    # Список серверов с блек-листами
    blacklist = [
#     'block.dnsbl.sorbs.net', 
      'dnsbl.dronebl.org',
#     'dnsbl.sorbs.net', 
#     'dul.dnsbl.sorbs.net', 
#     'escalations.dnsbl.sorbs.net',
#     'http.dnsbl.sorbs.net', 
#     'misc.dnsbl.sorbs.net', 'new.dnsbl.sorbs.net',
#     'old.dnsbl.sorbs.net',
#     'recent.dnsbl.sorbs.net',
#     'smtp.dnsbl.sorbs.net', 'socks.dnsbl.sorbs.net',
#     'web.dnsbl.sorbs.net', 'zombie.dnsbl.sorbs.net',
    ]
   
    for server in blacklist:
        try:
            # данные, передаваемые через POST
            data = {'ip': ip, 'server': server}
      
            # полученный ответ, timeout 3 секунды (некоторые серверы могут не отвечать)
            response = requests.post(url, data=data, timeout=3)
      
            # проверяем, что код ответа 200
            if response.status_code != 200:
                raise ValueError('Expected 200 OK')
      
            data = response.json()
#             print(data)
            # JSON приходит в формате {"сервер": "пусто или IP адрес"}
            # поэтому берем первое значение первого ключа
            rating = data[server]
            # если значение не пустое, то IP в блек листе
            if rating != "":
                print("found in %s" % server)
                return server
        except Exception as e:
#             traceback.print_exc()
            # тут обрабатываются различные ошибки, сообщение выводится в STDERR
            sys.stderr.write ("Skip server: " + server + "\n")
    return None


def check_http_proxy(ip, port):
    try:
        http_proxy  = "http://%s:%s" % (ip, port)
        https_proxy = "https://%s:%s" % (ip, port)
        proxyDict = { 
          "http"  : http_proxy, 
          "https" : https_proxy, 
        }
        response = requests.get('http://www.google.com', proxies=proxyDict, timeout=3)  
        data = response.text
        print("status = %s" % response.status_code)
        if not response.status_code == 200:
            return False       
    except Exception as e:
#         traceback.print_exc()
        return False
    return True



def is_socks4(ip, port):
    try:
        proxy  = "socks4://%s:%s" % (ip, port)
        proxyDict = { 
          "http"  : proxy, 
          "https" : proxy, 
        }
        response = requests.get('http://www.google.com', proxies=proxyDict, timeout=3)  
        data = response.text      
    except Exception as e:
        return False
    return True
    
    
def is_socks5(ip, port):
    try:
        proxy  = "socks5://%s:%s" % (ip, port)
        proxyDict = { 
          "http"  : proxy, 
          "https" : proxy, 
        }
        response = requests.get('http://www.google.com', proxies=proxyDict, timeout=3)  
        data = response.text      
    except Exception as e:
#         traceback.print_exc()
        return False
    return True


def get_socks_version(host, port):
    if(is_socks4(host, port)):
        return 5
    elif(is_socks5(host, port)):
        return 4
    else:
        return 0



def load_tor_ips():
    data = ""
    try:
        response = requests.get('https://check.torproject.org/exit-addresses', timeout=15)  
        data = response.text
    except Exception as e:
        print("can't connect to tor site, loading local list...")
        f = open("tor-exit-nodes.txt", "r")
        data = f.read()
    lines = data.split("\n")
    for line in lines:
        if "ExitAddress" in line:
            values = line.split(" ")
            address =  values[1].strip()     
            tor_ips.append(address)
    print("Loaded %s tor exit nodes" % len(tor_ips))


#main

def check_bad_host(host):
    socks_ports = [
        1080,
        1081,
#         9999,
    ]
    http_ports = [
        3128,
        8080,
    ]
    try:
        if host in settings.proxy_check_excluded_hosts:
            return (False, None)
        ip = socket.gethostbyname(host)
        print("Checking host %s ip %s" % (host, ip));
        if ip in tor_ips:
            return(True, "Host %s is TOR exit node!" % host)
        if check_dnsbl(ip):
            return(True, "Host %s is in dnsbl!" % host)
        for port in socks_ports:
            socks_version = get_socks_version(ip, port)
            if socks_version:
                return(True, "Socks%s proxy detected at port %s!" % (socks_version, port));
        for port in http_ports:
            if check_http_proxy(ip, port):
                return(True, "HTTP proxy detected!");
                sys.exit()
        print("host %s is clear" % host);                
    except Exception as e:
        traceback.print_exc()
    return (False, None)