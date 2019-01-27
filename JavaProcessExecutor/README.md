# Java Process Executor #
This example shows how to run a Java Application using a Process Executor Operator

The functionality was tested with Data Hub version 2.4.

![Graph](graph.png "Graph")

# Build

### Build example JavaApplication using Maven (https://maven.apache.org/)

```
$ mvn clean package -f src/JavaApplication/pom.xml
```

### Build SAP Data Hub Solution

```
$ tar -cvz --exclude='./JavaApplication' -f solution/JavaProcessExecutor.tgz -C src .
```
