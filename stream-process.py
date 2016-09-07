# read from kafka
# do average
# save data back
import sys
import logging
import time
import json
# to create a new topic to kafka from spark  
from kafka import KafkaProducer
# from kafka.errors import KafkaError
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('stream-processing')
logger.setLevel(logging.INFO)

kafka_broker = '192.168.99.101:9092'
kafka_topic = 'stock-analyzer'
new_topic = 'test'

# RDD is an abstraction of data by spark, can not be changed but derives new RDD 
def process(timeobj, rdd):
	num_of_records = rdd.count()
	if num_of_records == 0:
		return
	# sum up all the price in this rdd
	# for each rdd record, do sth ( take out the lastTradePrice, json) -> map
	# for all the rdd record, sum up -> reduce
	# record is a list, the 0 position is json value, convert json to python obj, the 0 pos is the map
	price_sum = rdd \
	        .map(lambda record: float(json.loads(record[1].decode('utf-8'))[0].get('LastTradePrice'))) \
	        .reduce(lambda a, b: a + b) 
	average = price_sum / num_of_records
	logger.info('received records from kafka, average price is %f' % average)
	current_time = time.time()
	data = json.dumps({'timestamp':current_time, 'average': average})
	# write the spark results back to Kafka
	# need to handle exception
	kafka_producer.send(new_topic, value = data)
if __name__ == '__main__':
	if (len(sys.argv) != 4):
		# first arguments is the func itself  
		print("not enough arguments [kafka broker location], [kafka topic]")
		exit(1)
	# SparkContext runs on local, name it stockAveragePrice
	sc = SparkContext("local[2]", "StockAveragePrice")
	# DEBUG INFO WARNING ERROR
	sc.setLogLevel('ERROR') 
	ssc = StreamingContext(sc, 5) 

	kafka_broker, kafka_topic, new_topic = sys.argv[1:]

	# setup a kafka stream
	
	directKafkaStream = KafkaUtils.createDirectStream(ssc, [kafka_topic], {'metadata.broker.list': kafka_broker})
	# one RDD created every 5 secs
	directKafkaStream.foreachRDD(process)
	kafka_producer = KafkaProducer(bootstrap_servers=kafka_broker)

	# shutdown hook

	ssc.start()
	ssc.awaitTermination()



