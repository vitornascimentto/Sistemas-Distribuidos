import pika
import sys
#import interface

def sendMessage(message):
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='task_queue1', durable=True)

	#message = ' '.join(sys.argv[1:]) or "Hello World!"

	#message = input('Message: ')

	
    #my_msg.set("")

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