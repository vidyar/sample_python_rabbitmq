import pika

class Rabbit():

    global message

    def sendMessage(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body='Hello World!')
        connection.close()

    def readMessage(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='hello')

        def callback(ch, method, properties, body):
            self.message = body
            channel.stop_consuming()

        channel.basic_consume(callback,
                              queue='hello',
                              no_ack=True)
        channel.start_consuming()

    def relayMessage(self):
        self.readMessage()
        return self.message

if __name__ == "__main__":
    rabbit = Rabbit()
    rabbit.sendMessage()
    print(rabbit.readMessage())
