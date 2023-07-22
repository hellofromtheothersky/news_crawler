from confluent_kafka import Producer
import socket
import argparse

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--s', type=str, help="website name")
    args = parser.parse_args()
    name=args.s


    with open ('newest_data_'+name+'.json', 'r') as rf:
        data=rf.read()

    data_encoded=data.encode()
    conf = {
        'bootstrap.servers': "localhost:9092",
        'client.id': socket.gethostname()
    }

    producer = Producer(conf)
    producer.produce("newsdata", key="key", value=data_encoded, callback=acked)     
    producer.poll(1)   # Maximum time (1s) to block while waiting for events