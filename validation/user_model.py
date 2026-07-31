from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone: str
    website: str
    city: str
    zipcode: str
    company_name: str