from pydataio.config_handler import buildInput
from pydataio.config_handler import buildOutput
from pydataio.io.pipes.spark.batch.inputs import SparkInput as BatchInput
from pydataio.io.pipes.spark.batch.outputs import SparkOutput as BatchOutput
from pydataio.io.pipes.spark.streaming.inputs import SparkInput as StreamingInput
from pydataio.io.pipes.spark.streaming.outputs import SparkOutput as StreamingOutput
from pydataio.io.utils.triggers import AvailableNowTrigger
from pydataio.schema_registry import SchemaRegistry
from tests.dummies import dummyEventSchema


def test_buildInput_single_batch():
    conf: list[dict] = [
        {
            "name": "events",
            "type": "pipes.spark.batch.SparkInput",
            "format": "json",
            "path": "tests/resources/data/events",
            "schema": "dummyEventSchema",
            "options": {"header": "true"},
        }
    ]

    registry = SchemaRegistry().registerSchema("dummyEventSchema", dummyEventSchema)
    reader = buildInput(conf, registry)

    assert isinstance(reader["events"], BatchInput)
    assert reader["events"].format == "json"
    assert reader["events"].path == "tests/resources/data/events"
    assert reader["events"].schema == dummyEventSchema
    assert reader["events"].options == {"header": "true"}


def test_buildInput_single_streaming():
    conf: list[dict] = [
        {
            "name": "events",
            "type": "pipes.spark.streaming.SparkInput",
            "format": "json",
            "path": "tests/data/streaming",
            "schema": "dummyEventSchema",
            "options": {"header": "true"},
        }
    ]

    registry = SchemaRegistry().registerSchema("dummyEventSchema", dummyEventSchema)
    reader = buildInput(conf, registry)

    assert isinstance(reader["events"], StreamingInput)
    assert reader["events"].format == "json"
    assert reader["events"].path == "tests/data/streaming"
    assert reader["events"].schema == dummyEventSchema
    assert reader["events"].options == {"header": "true"}


def test_buildInput_mix():
    conf: list[dict] = [
        {
            "name": "events",
            "type": "pipes.spark.batch.SparkInput",
            "format": "json",
            "path": "tests/resources/data/events",
            "schema": "dummyEventSchema",
            "options": {"header": "true"},
        },
        {
            "name": "rules",
            "type": "pipes.spark.streaming.SparkInput",
            "format": "parquet",
            "path": "tests/data/rules",
            "schema": "dummyEventSchema",
            "options": {"header": "true"},
        },
    ]

    registry = SchemaRegistry().registerSchema("dummyEventSchema", dummyEventSchema)
    reader = buildInput(conf, registry)

    assert isinstance(reader["events"], BatchInput)
    assert reader["events"].format == "json"
    assert reader["events"].path == "tests/resources/data/events"
    assert reader["events"].schema == dummyEventSchema
    assert reader["events"].options == {"header": "true"}

    assert isinstance(reader["rules"], StreamingInput)
    assert reader["rules"].format == "parquet"
    assert reader["rules"].path == "tests/data/rules"
    assert reader["rules"].schema == dummyEventSchema
    assert reader["rules"].options == {"header": "true"}


def test_buildInput_mix_not_optional():
    conf: list[dict] = [
        {
            "name": "events",
            "type": "pipes.spark.batch.SparkInput",
            "format": "json",
            "path": "tests/resources/data/events",
        },
        {
            "name": "rules",
            "type": "pipes.spark.streaming.SparkInput",
            "format": "parquet",
            "path": "tests/data/rules",
        },
    ]

    registry = SchemaRegistry().registerSchema("selAggregatedEvent", dummyEventSchema)
    reader = buildInput(conf, registry)

    assert isinstance(reader["events"], BatchInput)
    assert reader["events"].format == "json"
    assert reader["events"].path == "tests/resources/data/events"
    assert reader["events"].schema is None
    assert reader["events"].options == {}

    assert isinstance(reader["rules"], StreamingInput)
    assert reader["rules"].format == "parquet"
    assert reader["rules"].path == "tests/data/rules"
    assert reader["rules"].schema is None
    assert reader["rules"].options == {}


def test_buildInput_none():
    conf = None

    registry = SchemaRegistry().registerSchema("selAggregatedEvent", dummyEventSchema)
    reader = buildInput(conf, registry)

    assert reader is None


def test_buildSparkOutput_batch():
    conf: dict = {
        "type": "pipes.spark.batch.SparkOutput",
        "format": "json",
        "path": "tests/data/output",
        "mode": "overwrite",
        "partitionColumn": "date",
        "options": {"header": "true"},
    }

    writer = buildOutput(conf)

    assert isinstance(writer, BatchOutput)
    assert writer.format == "json"
    assert writer.path == "tests/data/output"
    assert writer.mode == "overwrite"
    assert writer.partitionColumn == "date"
    assert writer.options == {"header": "true"}


def test_buildSparkOutput_batch_not_optional():
    conf: dict = {
        "type": "pipes.spark.batch.SparkOutput",
        "format": "json",
        "path": "tests/data/output",
        "mode": "overwrite",
    }

    writer = buildOutput(conf)

    assert isinstance(writer, BatchOutput)
    assert writer.format == "json"
    assert writer.path == "tests/data/output"
    assert writer.mode == "overwrite"
    assert writer.partitionColumn is None
    assert writer.options == {}


def test_buildSparkOutput_streaming():
    conf: dict = {
        "name": "events",
        "type": "pipes.spark.streaming.SparkOutput",
        "format": "json",
        "path": "tests/data/output",
        "mode": "overwrite",
        "partitionColumn": "date",
        "sinkProcessor": "tests.dummies.DummyProcessor",
        "timeout": "2 minutes",
        "trigger": "AvailableNowTrigger",
        "options": {"header": "true"},
    }

    writer = buildOutput(conf)

    assert isinstance(writer, StreamingOutput)
    assert writer.outputName == "events"
    assert writer.format == "json"
    assert writer.path == "tests/data/output"
    assert writer.mode == "overwrite"
    assert writer.partitionColumn == "date"
    assert writer.timeout == 120
    assert isinstance(writer.trigger, AvailableNowTrigger)
    assert writer.options == {"header": "true"}


def test_buildSparkOutput_steaming_not_optional():
    conf: dict = {
        "name": "events",
        "type": "pipes.spark.streaming.SparkOutput",
        "format": "json",
        "path": "tests/data/output",
        "mode": "overwrite",
        "timeout": "2 minutes",
        "trigger": "AvailableNowTrigger",
    }

    writer = buildOutput(conf)

    assert isinstance(writer, StreamingOutput)
    assert writer.outputName == "events"
    assert writer.format == "json"
    assert writer.path == "tests/data/output"
    assert writer.mode == "overwrite"
    assert writer.partitionColumn is None
    assert writer.timeout == 120
    assert isinstance(writer.trigger, AvailableNowTrigger)
    assert writer.options == {}
    assert writer.sinkProcessor is None


def test_buildSparkOutput_none():
    conf = None

    writer = buildOutput(conf)

    assert writer is None
