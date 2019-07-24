import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def send(verificar, body):
	if verificar == "b'user1'":
		key = 'task_queue2' 
	if verificar == "b'user2'":
		key = 'task_queue1'

	channel.basic_publish(
		exchange='',
		routing_key=key,
		body=body,
		properties=pika.BasicProperties(
		    delivery_mode=2,  # make message persistent
		))

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

    verificar = str(body[:5:])
    body = body[5::]

    send(verificar, body)
    
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()