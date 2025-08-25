---
title: Custom transformer classes
layout: default
parent: Advanced
nav_order: 1
---
# Custom transformer classes

Apart from the provided `Transformer` abstract class, you can define your own custom class that extend `Transformer` to match your specific use cases. This allows you to encapsulate common data transformation patterns or reusable logic into custom classes, making your code even more modular and maintainable.

For example, if your organization regularly needs to join data from two different datasets, you could create a `JoinTransformer` class, such as:

```python
from abc import abstractmethod

from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame

from pydataio.transformer import Transformer
from pydataio.job_config import JobConfig

class JoinTransformer(Transformer):
    
    job_config: JobConfig
    spark: SparkSession
    
    def featurize(self, jobConfig: JobConfig, spark: SparkSession, additionalArgs: dict = None):
        if len(jobConfig.reader) < 2:
            raise ValueError("Can not run a JoinTransformer without two inputs configurations.") 
                
        self.job_config = jobConfig
        self.spark = spark
        
        events1 = jobConfig.load(inputName="events1", spark=spark)
        events2 = jobConfig.load(inputName="events2", spark=spark)
        
        self.transform(events1, events2)
        
    @abstractmethod
    def transform(self, input_data1: DataFrame, input_data2: DataFrame) -> DataFrame:
        pass

```

Since the class extends `Transformer`, it is compatible with PyData I/O and can be used in the configuration file.