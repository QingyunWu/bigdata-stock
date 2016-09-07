# read from a kafka topic
# publish data to redis PUB
import argparse
import atexit
import logging
from kafka import KafkaConsumer
import redis

topic = ''
kafka_broker = ''
redis_channel = ''
redis_host = ''
redis_port = ''

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('topic', help='the kafka tipic to consume from')
	parser.add_argument('kafka_broker', help='location of kafka broker')
	parser.add_argument('redis_channel', help='the redis channel(topic)')
	parser.add_argument('redis_host', help='the ip of the redis_host')
	parser.add_argument('redis_port', help='the port of redis')
	# the arguments of address and port are seperate in redis
	args = parser.parse_args()
	topic = args.topic
	kafka_broker = args.kafka_broker
	redis_channel = args.redis_channel
	redis_host = args.redis_host
	redis_port = args.redis_port

	# setup kafka consumer
	KafkaConsumer = KafkaConsumer(topic, bootstrap_servers=kafka_broker)

	# setup redis client
	redis_client = redis.StrictRedis(host=redis_host, port = redis_port)

	for msg in kafka_consumer:
		logger.info('Received new data from kafka %s' % str(msg))
		redis_client.publish(redis_channel, msg.value)
		 

