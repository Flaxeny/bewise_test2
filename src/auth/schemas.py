from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    UUID: str

    class Config:
        orm_mode = True
