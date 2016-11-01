# PGet

pget offers a simple yet functional API that enables you to save large files from bandwidth limited servers.

Basically, Downloader operates asynchronously and creates multithreads that connect to specified url from different ranges.

Simple use case can be found in bin module of the library. This module also creates an executable that can be used as

```
pget <url> <filename> <connection_number>
```