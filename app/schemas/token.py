from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    

class Token(AccessToken):
    refresh_token: str

