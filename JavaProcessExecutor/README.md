# Java Process Executor #
This example shows how to run a Java Application and how to pass custom configuration paramaters using a `Process Executor Operator`.

The Process Executor Operator starts the Java Application as a process and provides given contiguous streams to it. The operator finishes when the forked Java process terminates.

The functionality was tested with Data Hub version 2.4.

![Graph](./graph.png "Graph")

## Requirements

Before you start using the example, please make sure that:

- You are familiar with the basic concepts of SAP Data Hub Modeling such Pipelines (Graphs), Operators and Dockerfiles.  For more information, you may refer to the Modeling Guide for SAP Data Hub that is available on the SAP Help Portal (https://help.sap.com/viewer/p/SAP_DATA_HUB).
- You are familiar with the basic concepts of Docker (https://docs.docker.com/get-started/) and Kubernetes (https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).

## Build

The [solution/JavaProcessExecutor.tgz](solution/JavaProcessExecutor.tgz) already includes all required artifacts to run this example. However, when you want to build the solution from your local computer, you can use the following commands:

### Build example JavaApplication using Maven (https://maven.apache.org/)

```
$ mvn clean package -f src/JavaApplication/pom.xml
```

### Build SAP Data Hub Solution

```
$ tar -cvz --exclude='./JavaApplication' -f solution/JavaProcessExecutor.tgz -C src .
```

## Content  
**1. Dockerfile** [src/vrep/vflow/dockerfiles/examples/JavaProcessExecutor/Dockerfile](src/vrep/vflow/dockerfiles/examples/JavaProcessExecutor/Dockerfile)
  - Specifies the Docker Image that is used by the ProcessExecutor
  - The used Base Image provides the Java Runtime Environment required by the ProcessExecutor
  - provides the image tag `java` with version `11`

**2. Java Application**  [src/JavaApplication/src/main/java/com/sap/javaapplication](src/JavaApplication/src/main/java/com/sap/javaapplication)
  - Example Java Application that shows how to read from stdin and how to write to stdout/stderr
  
**2. Custom Operator**  [src/vrep/vflow/operators/examples/JavaProcessExecutor/](src/vrep/vflow/operators/examples/JavaProcessExecutor/)
  - Derived from 'ProcessExecutor'
  - Uses the image tag `java` with version `11`
  - Has one parameter `mode`
  - Runs the command `java -jar /vrep/vflow/operators/examples/JavaProcessExecutor/JavaApplication.jar ${mode}` 
 
**3. Sample Graph** [src/vrep/vflow/graphs/examples/JavaProcessExecutor/](src/vrep/vflow/graphs/examples/JavaProcessExecutor/)
  - Demonstrates how to use the custom Process Executor to run a Java Application

## How to run
  - Import [solution/JavaProcessExecutor.tgz](solution/JavaProcessExecutor.tgz) via `SAP Data Hub System Management` -> `Files` -> `Import Solution`
  - Run the `Graph` -> `examples.JavaProcessExecutor`
