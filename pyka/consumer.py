from confluent_kafka import Consumer, KafkaError, KafkaException, TopicPartition, OFFSET_BEGINNING
from confluent_kafka.avro import CachedSchemaRegistryClient
from confluent_kafka.avro import MessageSerializer
from json.decoder import JSONDecodeError
import json

from .utils import eprint


class ConsoleConsumer:
    def __init__(self, brokers, topic, offset, key_decoder, value_decoder, registry_url, additional_properties):
        config = {'bootstrap.servers': brokers,
                  'enable.partition.eof': 'true',
                  'group.id': 'not-used',
                  'auto.offset.reset': 'earliest',
                  'enable.auto.commit': 'false'}
        self.consumer = Consumer({**additional_properties, **config})
        self.topic = topic
        self.offset = offset.lower()
        self.key_decoder = key_decoder.lower()
        self.value_decoder = value_decoder.lower()
        self.avro_serializer = None
        if registry_url:
            client = CachedSchemaRegistryClient(registry_url)
            self.avro_serializer = MessageSerializer(client)

    def run(self):
        try:
            partition_ends = 0
            total_parts, partitions = self._partitions()
            self.consumer.assign(partitions)
            while True:
                msg = self.consumer.poll(timeout=0.5)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        eprint(f'{msg.topic()} reached end of partition [{msg.partition()}] at offset {msg.offset()}')
                        partition_ends += 1
                        if partition_ends == total_parts:
                            break
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    record = {'key': self._decode(self.key_decoder, msg.key()),
                              'payload': self._decode(self.value_decoder, msg.value()),
                              'topic': msg.topic(),
                              'partition': msg.partition(),
                              'offset': msg.offset(),
                              'timestamp': msg.timestamp()[1]}
                    print(json.dumps(record))
        finally:
            self.consumer.close()

    def _partitions(self):
        parts = []
        topic_data = self.consumer.list_topics(topic=self.topic)
        total_parts = len(topic_data.topics[self.topic].partitions)
        for i in range(0, total_parts):
            partition = TopicPartition(self.topic, i, offset=OFFSET_BEGINNING)
            if self.offset == 'earliest':
                parts.append(partition)
            else:
                try:
                    start, end = self.consumer.get_watermark_offsets(partition, timeout=0.5)
                    real_offset = int(self.offset)
                    ass_offset = (end + real_offset) if (real_offset < 0) else (start + real_offset)
                    parts.append(TopicPartition(self.topic, i, offset=ass_offset))
                except ValueError:
                    eprint(f"Could not parse offset: {self.offset}")
                    exit(1)
        return total_parts, parts

    def _decode(self, data_type, payload):
        if data_type == "avro":
            return self.avro_serializer.decode_message(payload)
        payload_str = payload.decode('utf-8')
        try:
            return json.loads(payload_str)
        except (JSONDecodeError, TypeError):
            return payload_str
