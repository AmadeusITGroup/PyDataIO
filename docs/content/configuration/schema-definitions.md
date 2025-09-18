---
title: Schema definitions
layout: default
parent: Configuration
nav_order: 2
---
# Schema Definitions

In some cases (e.g. streaming, reading JSON or CSV inputs), defining a schema is a good practice as it will improve the performances by skipping the schema inference step.

The PyData I/O gives the possibility to call the Spark API's schema() method by specifying a schema when configuring an
input. To do so you have to:

* Create a case class or a variable which represents the schema,
* Specify the `schema` parameter for the `Input` in the configuration file,
* Register your case class in the `SchemaRegistry` in the main function of your program.

## Creating a schema

Creating a schema is done by creating a variable specifying a [spark sql StructType](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.types.StructType.html) which will define the properties of your data. You can use every types supported by Spark SQL.  For more information about supproted types, see the list on [Spark SQL official website](https://spark.apache.org/docs/lqtest/sql-ref-datatypes.html).

For example you can define a simple schema like this:

```python
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
)

myEvents = StructType(
    [
        StructField("id", StringType(), False),
        StructField("name", StringType(), True),
        StructField("value", StringType(), True),
    ]
)
```

You can also define a more complex schema like this:

```python
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    TimestampType
)

myEvents = StructType(
    [
        StructField("id", StringType(), False),
        StructField("name", StringType(), True),
        StructField("value", StringType(), True),
        StructField("from", StructType([
            StructField("origin", StringType(), True),
            StructField("timestamp", TimestampType(), True),            
            ]
            )
        )
    ]
)
```

## Selecting the Schema

To select a schema, you need to add the `schema` field and specify the name of the schema used to register it in the `SchemaRegistry` to the
corresponding input node in your configuration file:

```yaml
Input:
  - name: "my-input"
    type: "pipes.spark.batch.SparkInput"
    path: "/path/my-input"
    schema: "my-event-schema"
```

A same schema can be used by several inputs, but only one schema can be defined for a given input.
{: .info}

## Registering the schema

The schemas must be registered via the `SchemaRegistry`, which centralizes all available schemas for the PyData I/O inputs. To do so,  call the `registerSchema` method within the main function of your application, as shown below:

```python
from pydataio.pipeline import Pipeline

def main():
    (...)
    confPath = ...
    pipeline = Pipeline()
    pipeline.schemaRegistry.registerSchema("my-event-schema", myEvents)
    pipeline.run(confPath)

```

As you can see, registering several schemas is as simple as calling `registerSchema` for each schema you want to be registered.

All the schemas defined in the configuration file must be registered before the call to the run function of your pipeline. If a schema is not found in the registry then the schema is skipped and won't be used.
{: .warning}

