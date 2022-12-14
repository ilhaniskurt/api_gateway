import json
from pydantic import BaseModel, error_wrappers

# Returns data and errors
def valid_schema_data_or_error(raw_data: str, SchemaModel: BaseModel):
    data = None
    errors = None
    error_str = None

    try:
        raw_data = json.loads(raw_data)
        cleaned_data = SchemaModel(**raw_data)
        data = cleaned_data.dict()
    except json.decoder.JSONDecodeError as e:
        error_str = json.dumps([{'loc': 'non_field_error', 'msg': 'invalid JSON', 'type': 'json.decoder.JSONDecodeError'}])
    except error_wrappers.ValidationError as e:
        error_str = e.json()
    
    if error_str is not None:
        try:
            errors = json.loads(error_str)
        except Exception as e:
            errors = [{"loc":"non_field_error", "msg": "Unknown error"}]
    return data, errors