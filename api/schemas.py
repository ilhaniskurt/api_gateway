from pydantic import BaseModel, validator, root_validator

callable_events = [
    'test',
    'login',
    'two_factor',
    'customer_list',
    'customer_connect',
    'transaction'
]

# TODO: Check there are no more or less keys in values sent in by using root validator

class EventSchema(BaseModel):
    event: str
    data: dict

    @validator("event")
    def event_validator(cls, value, values, **kwargs):
        if value not in callable_events:
            raise ValueError(f'cannot call ({value}) event')
        else:
            return value

    @validator("data")
    def data_validator(cls, value, values, **kwargs):
        match values.get('event'):
            case 'login':
                LoginData(**value)
            case 'two_factor':
                TwoFaData(**value)
            case 'customer_list':
                TokenData(**value)
            case 'customer_connect':
                CustomerConnectData(**value)
            case 'transaction':
                TokenData(**value)
                
        return value

class LoginData(BaseModel):
    username: str
    password: str

    @validator("username")
    def username_validator(cls, value, values, **kwargs):
        return value

    @validator("password")
    def password_validator(cls, value, values, **kwargs):
        return value

class TokenData(BaseModel):
    token: str

    @validator("token")
    def token_validator(cls, value, values, **kwargs):
        return value

class TwoFaData(BaseModel):
    token: str
    pin: int

    @validator("token")
    def token_validator(cls, value, values, **kwargs):
        TokenData(token=value)
        return value

    @validator("pin")
    def pin_validator(cls, value, values, **kwargs):
        return value

class CustomerConnectData(BaseModel):
    token: str
    customer_no: int

    @validator("token")
    def token_validator(cls, value, values, **kwargs):
        TokenData(token=value)
        return value

    @validator("customer_no")
    def customer_no_validator(cls, value, values, **kwargs):
        return value