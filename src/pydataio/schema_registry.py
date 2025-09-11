from pyspark.sql.types import StructType


class SchemaRegistry:
    """
    Class to represent a schema registry
    """

    def __init__(self):
        self.schemas = {}

    def get_schema(self, shemaName: str):
        """
        Get a schema from the registry
        Args:
            shemaName: name of the schema

        Returns: the schema

        """
        return self.schemas.get(shemaName, None)

    def registerSchema(self, schemaName: str, schema: StructType):
        """
        Register a schema in the registry

        Args:
            schemaName: name of the schema
            schema:  the schema to register

        """
        self.schemas[schemaName] = schema
        return self
