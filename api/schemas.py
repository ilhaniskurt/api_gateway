from pydantic import BaseModel, validator, root_validator

callable_events = ['test', 'login', 'two_factor']

class EventSchema(BaseModel):
    event: str
    data: dict

    @validator("event")
    def event_validator(cls, value, values, **kwargs):
        if value not in callable_events:
            raise ValueError(f'cannot call "{value}" event')
        else:
            return value
        
