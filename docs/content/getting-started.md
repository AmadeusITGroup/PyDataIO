---
title: Getting started
layout: default
nav_order: 2
---
# Getting Started
<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

--- 

## Installation

Using uv:

```sh
uv add pydataio
```

Published releases are available on GitHub Packages, in the PyData I/O repository.
{: .info}

### Dependencies

The `pydataio` project relies on several dependencies to function correctly. Here is a list of the main dependencies and their purposes:

- **Python 3.11**: The programming language used for the project.
- **PyYAML 6.0.2**: A YAML parser and emitter for Python, used to load and parse YAML configuration files.
- **fsspec 2024.10.0**: A filesystem specification library, used to handle various filesystems and file operations.
- **adlfs 2024.7.0**: An implementation of fsspec for Azure Data Lake Storage, used to interact with Azure Blob Storage.
- **pyspark 3.5.2**: The Python API for Apache Spark, used for distributed data processing.

These dependencies are specified in the `pyproject.toml` file and managed using uv.


## Minimal Example

This example presents how to write a rudimentary batch data pipeline: removing the duplicates from a CSV dataset, and saving the result as Parquet.

To make it work, you only need to write three components:

* A data processor, which contains the transformations to operate on the data,
* A configuration file, which contains information about the processor to use, the inputs, outputs, etc.,
* A Pipeline object, which loads the configuration file and runs the data processor with the configuration that you
  defined.

### The Data Transformer

Every transformation made using PyData I/O must be written in a data processor, a class that you create by extending the `Transformer` class.

Data transformations happen in the `featurize` method, which is used by the Pipeline to start the data processing.

```python
from pydataio.transformer import Transformer

class DuplicatesDropper(Transformer):
    def featurize(self, jobConfig: JobConfig, spark: SparkSession, additionalArgs: dict = None):
        data = jobConfig.load(inputName="my-input", spark=spark)
        
        fixed_data = data.dropDuplicates
        
        jobConfig.writer.save(data=fixed_data)
```

### The Configuration File

The configuration file contains the definition of the data processor your application will run, as well as inputs and
outputs. In our case, we only need one input, and one output.

```yaml
Processing:
  type: "getting_started.duplicates_dropper.DuplicatesDropper"

Input:
  - name: "my-input"
    type: "batch.FileSystemInput"
    format: "csv"
    path: "/path/my-input"
    options:
        header: true

Output:
  name: "my-output"
  type: "batch.FileSystemOutput"
  format: "parquet"
  path: "/path/my-output"
```

### The Data Pipeline

Now that we're ready, it's time to create our Pipeline and run the Processor. To do so, we need to set up the main function to load the configuration file, create a `Pipeline` instance, and run the pipeline with the configuration.

```python
import logging
from pydataio.pipeline import Pipeline
from azure.identity import ClientSecretCredential

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Path to the configuration file
    conf_path = 'path/to/your/config.yaml'
    
    # Create a Pipeline instance
    pipeline = Pipeline()
    
    # Run the pipeline
    pipeline.run(confPath=conf_path, credential=None, additionalArgs=None)

if __name__ == "__main__":
    main()
```
