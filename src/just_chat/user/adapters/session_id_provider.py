from just_chat.user.application.get_user_by_token import GetUserIdByToken
from just_chat.user.application.id_provider import IdProvider
from just_chat.user.application.interfaces.session_gateway import SessionToken
from just_chat.user.domain.user import UserId


# Он нужен в частности для того, чтобы прокидывать token в вызов интерактора GetUserIdByToken
# Вызвать сам интерактор получения по токену мы не можем, ибо:
# - Нам придется передавать токен при вызове, а в месте вызова мы не должны знать ни о каком токене и об аутенфикации вообще
# ИЛИ
# - Нам придется прокидывать токен в конструктор интерактора, но тогда мы не сможем применять один интерактор к нескольким
# токенам - только к одному, который и прокинули в конструктор. Ну или делать интерактору метод set_token,
# короче какой-то хуйней заниматься, лучше просто сделать обертку над всем этим аутенфикации в виде IdProvider
class SessionIdProvider(IdProvider):
    def __init__(self, token: SessionToken, user_id_provider: GetUserIdByToken) -> None:
        self._token = token
        self._user_id_provider = user_id_provider

    async def get_current_user_id(self) -> UserId:
        return await self._user_id_provider(self._token)
