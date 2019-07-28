import tkinter
from threading import Thread
import time
import pika
import sys

class User:

	def __init__(self, arquivo, fila, token, nome):
		self.arquivo = arquivo
		self.fila = fila
		self.token = token
		self.nome = nome

		top = tkinter.Tk()
		top.title(self.nome)

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
		entry_field.bind("<Return>", self.sendMessage)
		entry_field.pack()
		send_button = tkinter.Button(top, text="Send", command=self.sendMessage)
		send_button.pack()

		self.atualizar()

		receive_thread = Thread(target=self.receive)
		receive_thread.start()
		tkinter.mainloop()

	def interface(self):
		return 0

	def atualizar(self):
		with open('{}.txt'.format(self.arquivo), 'r') as arq:
			text = arq.readlines()
			for linha in text:
				msg_list.insert(tkinter.END, linha[:len(linha)-1:])

	def receive(self):
	   	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	   	channel = connection.channel()
	   	channel.queue_declare(queue=self.fila, durable=True)

	   	def callback(ch, method, properties, body):
	   		print(" [x] Received %r" % body)
	   		time.sleep(body.count(b'.'))
	   		print(" [x] Done")
	   		ch.basic_ack(delivery_tag=method.delivery_tag)

	   		msg = str(body)
	   		msg = msg[2:len(msg)-1:]

	   		msg_list.insert(tkinter.END, 'Somebody: ' + msg)
	   		with open('{}.txt'.format(self.arquivo), 'r') as data:
	   			conteudo = data.readlines() 
	   			conteudo.append('Somebody: ' + msg + '\n')
	   			with open('{}.txt'.format(self.arquivo), 'w') as data2:
	   				data2.writelines(conteudo)

	   	while True:	
	   		channel.basic_qos(prefetch_count=1)
	   		channel.basic_consume(queue=self.fila, on_message_callback=callback)
	   		channel.start_consuming()
   		
	def sendMessage(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		channel = connection.channel()
		channel.queue_declare(queue=self.fila, durable=True)

		message = my_msg.get()
		my_msg.set("")

		token = self.token

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
		with open('{}.txt'.format(self.arquivo), 'r') as data:
			conteudo = data.readlines() 
			conteudo.append('Me: ' + message + '\n')
			with open('{}.txt'.format(self.arquivo), 'w') as data2:
				data2.writelines(conteudo)

	

if __name__ == '__main__':
	obj = User('user1', 'task_queue1', 'user1', 'chat1')
	obj.interface()