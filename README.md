# pyka-cli

### Todo
* Real release process (docker and install)

### Issues
* Avro records with no fields (works but ambiguous result)
* Avro deserializer is quite slow
    * Can use `python-schema-registry-client[faust]==1.2.5` which is a bit faster but less support for some schemas
