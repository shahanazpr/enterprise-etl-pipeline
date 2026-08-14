from pydantic import BaseModel, EmailStr, field_validator


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

    @field_validator("name", "username", "phone", "website", "city", "zipcode", "company_name")
    @classmethod
    def not_empty(cls, value: str, info):
        if value is None or str(value).strip() == "":
            raise ValueError(f"{info.field_name} must not be empty")
        return value