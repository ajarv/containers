import os

amqp_username = os.environ.get('AMQP_USERNAME', 'guest')
amqp_passwd = os.environ.get('AMQP_PASSWORD', 'guest')
amqp_host = os.environ.get('AMQP_HOST', 'libra')
amqp_port = os.environ.get('AMQP_PORT', '5672')

broker_url = f"pyamqp://{amqp_username}:{amqp_passwd}@{amqp_host}:{amqp_port}//"