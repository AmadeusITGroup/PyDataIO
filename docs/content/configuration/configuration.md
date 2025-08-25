---
title: Configuration
layout: default
has_children: true
nav_order: 6
---
# Configuration

At the heart of PyData I/O is a configuration file that defines the inputs and outputs available for your application. The
configuration file provides a structured way to specify the components of your ETL pipeline.

It consists of different root notes:

- **Processing**: This node defines the transformation step and specifies the fully qualified name of the class
  responsible for transforming the data.
- **Input**: The input node defines the data sources for your pipeline. It can be a single object or an array of
  objects, each representing an input configuration. Each specifies the fully qualified name of the class that reads the
  data, along with any required parameters.
- **Output**: The output node defines the destinations where the transformed data will be written, it is a single object. It specifies the fully qualified name of the class
  responsible for writing the data, along with the necessary parameters.

In each of these nodes, the Type field is mandatory, representing the fully qualified name of the corresponding class.
The `name` field must be specified to provide a unique identifier for the object, making it easily accessible
from JobConfig in the code.
{: .important}

Here is an example of configuration file: 

```yaml
Processing:
  type: "gettingstarted.DuplicatesDropper"

Input:
  - name: "my-input"
    type: "pipes.spark.batch.SparkInput"
    format: "json"
    path: "/path/my-input"

Output:
  name: "my-output"
  type: "pipes.spark.batch.SparkOutput"
  format: "noop"
  mode: "append"
  path: "/path/my-output"
  options:
    failOnDataLoss: false

```
