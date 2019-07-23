import tkinter
from threading import Thread
import time
import pika
import sys

def receive():
   	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
   	channel = connection.channel()
   	channel.queue_declare(queue='task_queue2', durable=True)

   	def callback(ch, method, properties, body):
   		print(" [x] Received %r" % body)
   		time.sleep(body.count(b'.'))
   		print(" [x] Done")
   		ch.basic_ack(delivery_tag=method.delivery_tag)

   		msg = str(body)
   		msg = msg[2:len(msg)-1:]

   		msg_list.insert(tkinter.END, 'Somebody: ' + msg)
   		with open('user2.txt', 'r') as data:
   			conteudo = data.readlines() 
   			conteudo.append('Somebody: ' + msg + '\n')
   			with open('user2.txt', 'w') as data2:
   				data2.writelines(conteudo)

   	while True:	
   		channel.basic_qos(prefetch_count=1)
   		channel.basic_consume(queue='task_queue2', on_message_callback=callback)
   		channel.start_consuming()
   		
def sendMessage():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='task_queue2', durable=True)

	message = my_msg.get()
	my_msg.set("")

	token = 'user2'

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
	with open('user2.txt', 'r') as data:
		conteudo = data.readlines() 
		conteudo.append('Me: ' + message + '\n')
		with open('user2.txt', 'w') as data2:
			data2.writelines(conteudo)

top = tkinter.Tk()
top.title("Chatter2")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
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

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()