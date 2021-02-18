import os
import re
import socket
import ssl
import threading
import time

sem = threading.Semaphore(2)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
    mysocket.connect(("utm.md", 443))
    mysocket = ssl.wrap_socket(mysocket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE,
                               ssl_version=ssl.PROTOCOL_SSLv23)
    mysocket.sendall(b"GET / HTTP/1.1\r\nHost: utm.md\r\n\r\n")

    print(str(mysocket.recv(52), 'utf-8'))


def get_url_images_in_text(source):
    # Finds image's urls
    urls = []
    results = re.findall(r'\/wp-content\/[^\"]*(?:png|jpg)', source)

    for x in results:
        if 'https://' not in x:
            x = 'https://utm.md' + x
        urls.append(x)
    urls = list(set(urls))
    print('Links of images detected: ' + str(len(urls)))
    return urls


def get_images_from_url(url):
    domain = url.split("//")[-1].replace("/", "")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
        mysocket = ssl.wrap_socket(mysocket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE,
                                   ssl_version=ssl.PROTOCOL_SSLv23)
        mysocket.connect((socket.gethostbyname(domain), 443))
        mysocket.sendall(b"GET / HTTP/1.1\r\nHost: utm.md\r\n\r\n")
        mysocket.sendall("GET / HTTP/1.1\r\nHost: {0}\r\nConnection: close\r\n\r\n".format(domain).encode("latin1"))
        list_links = ""

        while True:
            data = mysocket.recv(1024)
            if len(data) == 0:
                break
            list_links += data.decode("latin1")

        return get_url_images_in_text(list_links)



def download_images(path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
        mysocket.connect(("utm.md", 443))
        mysocket = ssl.wrap_socket(mysocket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE,
                                   ssl_version=ssl.PROTOCOL_SSLv23)
        mysocket.sendall("GET {0} HTTP/1.1\r\nHost: utm.md\r\nConnection: close\r\n\r\n".format(path).encode("latin1"))

        images = b''

        while True:
            sem.acquire()
            data = mysocket.recv(1024)
            if not data:
                images = images.split(b"\r\n\r\n")
                if "200" not in images[0].decode("latin1"):
                    print(path)
                image_path = os.path.join(os.getcwd(), "UtmImages", path.rpartition("/")[-1])
                with open(image_path, "wb") as fcont:
                    fcont.write(images[-1])
                break

            images += data
        sem.release()



img_list = get_images_from_url("utm.md")

newlist = img_list

array1 = [newlist[i] for i in range(len(newlist)) if i % 2 == 0]
array2 = [newlist[i] for i in range(len(newlist)) if i % 2 == 1]

print(array1)
print(array2)

thread_list = []
for i in range(2):
    print("Start download")
    t1 = threading.Thread(target=download_images, args=(array1,))
    thread_list.append(t1)
    t1.start()
    t2 = threading.Thread(target=download_images, args=(array2,))
    thread_list.append(t2)
    t2.start()

print("Download Done")



