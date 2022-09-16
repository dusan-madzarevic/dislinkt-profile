from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    ime: str
    prezime: str
    telefon: str
    datumRodjenja: str
    pol: str


class ProfileCreate(BaseModel):
    user_id: str
    private: bool

