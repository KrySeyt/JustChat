from just_chat.user.domain.user import User, UserId, UserService


def test_create_user():
    user = UserService().create_user(
        username="User",
        hashed_password="123",
    )

    assert user.id is None
    assert user.username == "User"
    assert user.hashed_password == "123"


def test_update_user():
    user = User(
        id=UserId(15),
        username="User",
        hashed_password="123",
    )

    updated_user = UserService().update_user(
        user=user,
        new_username="NewUser",
        new_hashed_password="456",
    )

    assert updated_user.id == 15
    assert updated_user.username == "NewUser"
    assert updated_user.hashed_password == "456"
