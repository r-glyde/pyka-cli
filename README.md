# pyka-cli

A CLI tool to consume from kafka topics

### Todo
* Real release process (docker and install)

### Issues
* Avro records with no fields (works but ambiguous result)
* Avro deserializer is quite slow
    * Can use `python-schema-registry-client[faust]==1.2.5` which is a bit faster but less support for some schemas
    
### Use it
```
usage: pyka [-h] -t  [-o] [-k] [-v] [-r] [-X   KEY=VALUE] brokers

Consume from a kafka topic

positional arguments:
  brokers               list of kafka brokers

optional arguments:
  -h, --help            show this help message and exit
  -t , --topic          topic to consume from
  -o , --offset         starting offset: earliest (default) or +/- from beginning/end of partition
  -k , --key-decoder    decoder for message keys: string (default) or avro
  -v , --val-decoder    decoder for message values: string (default) or avro
  -r , --registry-url   schema-registry-url for avro deserialization (with protocol!)
  -X   KEY=VALUE        additional properties as defined at https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md

```
