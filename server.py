from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os

def gelen_baglantilari_kabul_et():
    """Gelen istemcilerin işlenmesini ayarlar."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s bağlandı." % client_address)
        client.send(bytes("Sohbet uygulamasına hoş geldin, başlamak için lütfen kullanıcı adını gir.", "utf8"))
        addresses[client] = client_address
        Thread(target=client_handle, args=(client,)).start()

def client_handle(client):
    """Tek bir istemci bağlantısını işler."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome_message = 'Merhaba %s! Sohbetten ayrılmak için, metin kısmına {quit} komutunu yazabilirsin.' % name
    client.send(bytes(welcome_message, "utf8"))
    message = "%s sohbete katıldı!" % name
    broadcast(bytes(message, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            if msg.startswith(b"dosya_bilgisi"):
                file_info = msg.decode("utf8").split(" ")
                file_name, file_size = file_info[1], int(file_info[2])
                receive_file(client, file_name, file_size)
                distribute_file(client, file_name, file_size)
            else:
                broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s sohbetten ayrıldı." % name, "utf8"))
            break
    
def broadcast(msg, prefix=""):
    """Tüm istemcilere bir mesajı yayınlar."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

def distribute_file(client, file_name, file_size):
    for sock in clients:
        if sock == client:
            continue
        sock.send(bytes("dosya_bilgisi {} {}".format(file_name, file_size), "utf8"))
        with open(file_name, "rb") as file:
            file_data = file.read()  # Dosya içeriğini oku
            sock.sendall(file_data)
    
def receive_file(client, file_name, file_size):
    # Dosya verilerini al ve dosyaya yaz
    received_size = 0
    with open(file_name, "wb") as file:
        while received_size < file_size:
            data = client.recv(BUFSIZ)
            file.write(data)
            received_size += len(data)

    # İstemciye onay mesajı gönder
    client.send(bytes("Dosya {} alındı.".format(file_name), "utf8"))


clients = {}
addresses = {}

HOST = ''
PORT = 3300
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Bağlantı bekleniyor...")
    ACCEPT_THREAD = Thread(target=gelen_baglantilari_kabul_et)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
