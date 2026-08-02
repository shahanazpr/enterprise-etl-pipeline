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