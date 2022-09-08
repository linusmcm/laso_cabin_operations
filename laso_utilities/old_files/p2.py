import time 
import json 
import random 
from datetime import datetime
from sts.old_files.data_generator import generate_message
from kafka import KafkaProducer

# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')

# Kafka Producer
producer = KafkaProducer(bootstrap_servers=['10.1.1.191:9094'], value_serializer=serializer)

if __name__ == '__main__':
    # Infinite loop - runs until you kill the program
    while True:
        # Generate a message
        dummy_message = generate_message()
        
        # Send it to our 'messages' topic
        print(f'Producing message @ {datetime.now()} | Message = {str(dummy_message)}')
        producer.send('test2', dummy_message)
        producer.send('test', dummy_message)
        
        # Sleep for a random number of seconds
        time_to_sleep = random.randint(1, 11)
        time.sleep(time_to_sleep)
