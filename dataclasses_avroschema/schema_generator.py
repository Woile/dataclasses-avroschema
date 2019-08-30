import json
import dataclasses
import typing

from dataclasses_avroschema.schema_definition import AvroSchemaDefinition


class SchemaGenerator:

    def __init__(self, klass_or_instance, include_schema_doc: bool = True) -> None:
        self.dataclass = self.generate_dataclass(klass_or_instance)
        self.include_schema_doc = include_schema_doc
        self.schema_definition = None

    @staticmethod
    def generate_dataclass(klass_or_instance):
        if dataclasses.is_dataclass(klass_or_instance):
            return klass_or_instance
        return dataclasses.dataclass(klass_or_instance)

    def generate_schema(self, schema_type: str = "avro"):
        if self.schema_definition is not None:
            return self.schema_definition

        if schema_type == "avro":
            # cache the schema
            self.schema_definition = AvroSchemaDefinition(
                "record",
                self.dataclass,
                include_schema_doc=self.include_schema_doc
            )
        else:
            raise

        return self.schema_definition.render()

    def avro_schema(self) -> str:
        return json.dumps(self.generate_schema(schema_type="avro"))

    def avro_schema_to_python(self) -> typing.Dict[str, typing.Any]:
        return json.loads(self.avro_schema())

    @property
    def get_fields(self) -> typing.List["Field"]:
        if self.schema_definition is None:
            self.generate_schema()

        return self.schema_definition.fields

