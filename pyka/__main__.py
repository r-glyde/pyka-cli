import argparse
from argparse import RawTextHelpFormatter
from .consumer import ConsoleConsumer
from.utils import eprint


def main():
    parser = argparse.ArgumentParser(description='Consume from a kafka topic', formatter_class=RawTextHelpFormatter)
    parser.add_argument('brokers', help='list of kafka brokers', metavar='brokers')
    parser.add_argument('-t', '--topic', help='topic to consume from', metavar='', required=True)
    parser.add_argument('-o',
                        '--offset',
                        help='starting offset: earliest (default) or +/- from beginning/end of partition',
                        default='earliest',
                        metavar='')
    parser.add_argument('-k',
                        '--key-decoder',
                        choices=['string', 'avro'],
                        help='decoder for message keys: string (default) or avro',
                        default="string",
                        metavar='')
    parser.add_argument('-v',
                        '--val-decoder',
                        choices=['string', 'avro'],
                        help='decoder for message values: string (default) or avro',
                        default="string",
                        metavar='')
    parser.add_argument('-r',
                        '--registry-url',
                        help='schema-registry-url for avro deserialization (with protocol!)',
                        metavar='')
    librdkafka_config = 'https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md'
    parser.add_argument('-X',
                        help=f'additional properties as defined at {librdkafka_config}',
                        metavar='  KEY=VALUE',
                        action='append')

    args = parser.parse_args()

    key_deserializer = args.key_decoder
    value_deserializer = args.val_decoder
    registry_url = args.registry_url

    additional_properties = {}
    if args.X:
        for prop in args.X:
            try:
                key, value = prop.split('=', maxsplit=1)
                additional_properties[key] = value
            except ValueError:
                eprint(f'Ignoring {prop}: did not match expected input for -X key=value')
                continue

    if (key_deserializer == 'avro' or value_deserializer == 'avro') and not registry_url:
        eprint("Schema registry URL must be configured with -r to use avro deserialisers")
        parser.print_help()
        exit(1)
    consumer = ConsoleConsumer(args.brokers,
                               args.topic,
                               args.offset,
                               key_deserializer,
                               value_deserializer,
                               registry_url,
                               additional_properties)
    consumer.run()


if __name__ == '__main__':
    main()
