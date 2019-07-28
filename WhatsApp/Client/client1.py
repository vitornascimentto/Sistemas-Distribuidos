import tkinter
from threading import Thread
import time
import pika
import sys
from cryptography.fernet import Fernet

def desencriptarMensagem(key, mensagem):
	key = key.encode('utf-8')
	mensagem = mensagem.encode('utf-8')
	
	f = Fernet(key)
	return f.decrypt(mensagem).decode('utf-8')

def encriptarMensagem(key, mensagem):
	mensagem = mensagem.encode('utf-8')	
	key = key.encode('utf-8')

	f = Fernet(key)
	token = f.encrypt(b'%s'%mensagem)
	
	return token.decode('utf-8')

def atualizar():

	with open('key.txt', 'r') as arq:
		key = arq.read()

	with open('user1.txt', 'r') as arq:
		text = arq.readlines()
		for linha in text:
			linha = desencriptarMensagem(key, linha)
			msg_list.insert(tkinter.END, linha[:len(linha):])

def receive():
   	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
   	channel = connection.channel()
   	channel.queue_declare(queue='task_queue1', durable=True)

   	def callback(ch, method, properties, body):
   		print(" [x] Received %r" % body)
   		time.sleep(body.count(b'.'))
   		print(" [x] Done")
   		ch.basic_ack(delivery_tag=method.delivery_tag)

   		msg = str(body)
   		msg = msg[2:len(msg)-1:]

   		msg_list.insert(tkinter.END, 'Somebody: ' + msg)

   		msg = 'Somebody: ' + msg

   		with open('key.txt', 'r') as arq:
   			key = arq.read()

   		msg = encriptarMensagem(key, msg)

   		with open('user1.txt', 'r') as data:
   			conteudo = data.readlines() 
   			conteudo.append(msg + '\n')
   			with open('user1.txt', 'w') as data2:
   				data2.writelines(conteudo)

   	while True:	
   		channel.basic_qos(prefetch_count=1)
   		channel.basic_consume(queue='task_queue1', on_message_callback=callback)
   		channel.start_consuming()

def sendMessage():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='task_queue1', durable=True)

	message = my_msg.get()
	my_msg.set("")

	token = 'user1'

	channel.basic_publish(
	    exchange='',
	    routing_key='task_queue',
	    body=token + message,
	    properties=pika.BasicProperties(
	        delivery_mode=2,  # make message persistent
	    ))
	print(" [x] Sent %r" % message)
	connection.close()	

	msg_list.insert(tkinter.END, 'Me: ' + message)

	msg = 'Me: ' + message

	with open('key.txt', 'r') as arq:
		key = arq.read()

	message = encriptarMensagem(key, msg)

	with open('user1.txt', 'r') as data:
		conteudo = data.readlines() 
		conteudo.append(message + '\n')
		with open('user1.txt', 'w') as data2:
			data2.writelines(conteudo)

top = tkinter.Tk()
top.title("Chatter1")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", sendMessage)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=sendMessage)
send_button.pack()

atualizar()

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()