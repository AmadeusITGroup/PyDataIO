---
title: Writing your transformers
layout: default
nav_order: 4
---
# Writing Your Transformers
<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

--- 

Data transformer play a crucial role in the PyData I/O framework, allowing you to implement custom data transformation logic within your pipelines. This page will guide you through the process of creating your own data transformer using the PyData I/O framework.

## Overview
Data transformer encapsulate the specific data processing steps required for your ETL pipelines. Each PyData I/O application requires a transformer that is responsible for manipulating the data according to your business requirements.

### Transformer abstract class

The `Transformer` abstract class is the base class for creating custom transformer. It provides the structure and functionality required to define your data transformation logic. By extending the `Transformer` class, you can create your own custom processors and implement the `featurize` method with your specific transformation steps.

Here's an example of a custom transformer that extends the `Transformer` trait:

```python
from pyspark.sql import DataFrame, SparkSession

from pydataio.job_config import JobConfig
from pydataio.transformer import Transformer

class MyDataTransformer(Transformer):
    def featurize(self, jobConfig: JobConfig, spark: SparkSession, additionalArgs: dict = None):
        # Access input data
        data = jobConfig.load(inputName="my-input", spark=spark)
        
        # Perform data transformation
        transformed_data = self.transformData(data)
        
        # Write transformed data to output
        jobConfig.writer.save(data=fixed_data)
        
    def transformData(self, inputData: DataFrame):
        # Your custom data transformation logic here
        # Example: Perform data cleansing, filtering, or aggregations
        # Return the transformed DataFrame
        ...
```

### Streaming  and for each batch sink
The `SinkProcessor` abstract class can be used to specify a dedicated sink function when using a [for each batch sink](https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.DataStreamWriter.foreachBatch.html).

Here's an example of a custom sink that extends the `SinkProcessor` class:

```python
from pydataio.io.abstract_io import SinkProcessor
from pyspark.sql import DataFrame

class MySinkProcessor(SinkProcessor):

    def process(self, data: DataFrame):
        # apply transformation in batch context
        ....
        
        # return the transformed dataset so that it can be written to the output
        return data
```

--- 

You can also define your own processor abstract class by extending the `Transformer` class. For more information on that, please visit the [advanced section](advanced/custom-transformer-classes.html).

## Custom Configuration

You can access custom configuration options directly within your transformer code. The custom configuration options
defined under the `Processing` configuration node can be accessed through the `parameters` member variable of the JobConfig class.

Here's an example of how to access custom configuration values within your processor:

```python
from pyspark.sql import DataFrame, SparkSession

from pydataio.job_config import JobConfig
from pydataio.transformer import Transformer

class MyDataTransformer(Transformer):
    def featurize(self, jobConfig: JobConfig, spark: SparkSession, additionalArgs: dict = None):
        # Access input data
        data = jobConfig.load(inputName="my-input", spark=spark)
        
        # Access custom configuration values
        custom_value1 = jobConfig.parameters["custom_value_1"]
        custom_value2 = jobConfig.parameters["custom_value_2"]
        
        # Perform data transformation
        transformed_data = self.transformData(data)
        
        # Write transformed data to output
        jobConfig.writer.save(data=fixed_data)

```

In the above example, `custom_value_1` and `custom_value_2` are custom configuration values defined under
the `Processing` configuration node in your configuration file:

```yaml
Processing:
  type: com.mycompany.MyDataProcessor
  parameters:
    custom_value_1: = "june"
    custom_value_2: = "2023"

```

By directly accessing the config member variable in your processor, you can leverage custom configuration options to parameterize and customize the behavior of your processors.

It is also possible to access additional command lines parameters using the `additionalArgs` dictionary injected in the `featurize` function.