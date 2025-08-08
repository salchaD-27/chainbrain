import json
import jsonschema

def validate_block_data(data):
    schema_path = "../schemas/ethereum_block.schema.json"
    with open(schema_path) as f:
        schema = json.load(f)

    jsonschema.validate(instance=data, schema=schema)
