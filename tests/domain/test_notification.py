from just_chat.domain.models.user import UserId
from just_chat.domain.services.notification import NotificationsSettingsService


def test_create_settings():
    settings = NotificationsSettingsService().create_settings(
        user_id=UserId(5),
        websocket_uri="ws://localhost"
    )

    assert settings.user_id == 5
    assert settings.websocket_uri == "ws://localhost"
