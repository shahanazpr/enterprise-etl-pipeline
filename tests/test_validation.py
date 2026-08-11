import pytest
from pydantic import ValidationError
from validation.user_model import User


def test_valid_user():
    user = User(
        id=1,
        name="John Doe",
        username="john",
        email="john@example.com",
        phone="9876543210",
        website="example.com",
        city="Bangalore",
        zipcode="560001",
        company_name="ABC Pvt Ltd"
    )

    assert user.id == 1
    assert user.email == "john@example.com"


def test_invalid_email_format():
    with pytest.raises(ValidationError):
        User(
            id=2,
            name="Jane Doe",
            username="jane",
            email="not-an-email",
            phone="9876543210",
            website="example.com",
            city="Bangalore",
            zipcode="560001",
            company_name="ABC Pvt Ltd"
        )


def test_null_name_rejected():
    with pytest.raises(ValidationError):
        User(
            id=3,
            name=None,
            username="jane",
            email="jane@example.com",
            phone="9876543210",
            website="example.com",
            city="Bangalore",
            zipcode="560001",
            company_name="ABC Pvt Ltd"
        )


def test_empty_string_rejected():
    with pytest.raises(ValidationError):
        User(
            id=4,
            name="   ",
            username="jane",
            email="jane@example.com",
            phone="9876543210",
            website="example.com",
            city="Bangalore",
            zipcode="560001",
            company_name="ABC Pvt Ltd"
        )


def test_missing_required_field():
    with pytest.raises(ValidationError):
        User(
            id=5,
            name="Jane Doe",
            username="jane",
            email="jane@example.com",
            phone="9876543210",
            website="example.com",
            city="Bangalore",
            company_name="ABC Pvt Ltd"
            # zipcode missing entirely
        )