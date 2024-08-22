import socket
import threading
import tkinter
from tkinter import filedialog
import os

def receive():
    """Gelen mesajları işler."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ)
            if msg.startswith(b"dosya_bilgisi"):
                # Dosya bilgileri işlenir
                dosya_bilgisi = msg.decode("utf8").split(" ")
                dosya_adi, dosya_boyutu = dosya_bilgisi[1], int(dosya_bilgisi[2])
                download_file(dosya_adi, dosya_boyutu)
            else:
                msg_list.insert(tkinter.END, msg.decode("utf8"))
        except OSError:
            break

def download_file(dosya_adi, dosya_boyutu):
    # Kullanıcıya dosyayı kaydetmek istediği konum sorulur
    file_path = filedialog.asksaveasfilename(initialdir=os.path.expanduser("~/Desktop"), title="Dosyayı kaydet", initialfile=dosya_adi, filetypes=(("All files", "*.*"),))
    if file_path:
        with open(file_path, "wb") as file:
            received_size = 0
            while received_size < dosya_boyutu:
                data = client_socket.recv(BUFSIZ)
                if not data:
                    break
                file.write(data)
                received_size += len(data)
            msg_list.insert(tkinter.END, "Dosya {} kaydedildi.".format(dosya_adi))

def send_file(file_path):
    with open(file_path, "rb") as file:
        while True:
            file_data = file.read(BUFSIZ)
            if not file_data:
                break
            client_socket.sendall(file_data)
        print(f"{file_path} dosyası gönderildi.")

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    if msg.startswith("dosya_gonder"):
        file_path = msg.split(" ", 1)[1]  
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            client_socket.send(bytes(f"dosya_bilgisi {file_name} {file_size}", "utf8"))
            send_file(file_path)
        else:
            msg_list.insert(tkinter.END, "Dosya bulunamadı: {}".format(file_path))
    else:
        client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_send_file_button_click():
    file_path = filedialog.askopenfilename()
    if file_path and os.path.isfile(file_path):
        my_msg.set("dosya_gonder " + file_path)
        send()
    else:
        msg_list.insert(tkinter.END, "Geçerli bir dosya seçilmedi.")

def on_closing(event=None):
    """Sohbet penceresi kapatıldığında çağrılır."""
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Sohbet Uygulaması")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # Gönderilecek string mesajlar.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # Geçmiş mesajları gezmede kullanılır.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()

send_button_frame = tkinter.Frame(top)
send_button_frame.pack()
send_button = tkinter.Button(send_button_frame, text="Gönder", command=send)
send_button.pack(side=tkinter.LEFT)

send_file_button = tkinter.Button(send_button_frame, text="Dosya Gönder", command=on_send_file_button_click)
send_file_button.pack(side=tkinter.LEFT)

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = input('Sunucu adresini girin: ')  
PORT = 3300
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(ADDR)
    print("Sunucuya başarıyla bağlanıldı.")
except Exception as e:
    print("Sunucuya bağlanılamadı:", e)
    exit()

receive_thread = threading.Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # GUI başlatılır.
