import datetime

from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    email: str
    username: str
    password: str
    ime: str
    prezime: str
    telefon: str
    datumRodjenja: datetime.date
    pol: str
