import bcrypt


class User:
    _user_id: int | None
    _email: str
    _password: str
    _first_name: str
    _last_name: str

    def __init__(
        self,
        user_id: int | None,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
    ) -> None:
        self._user_id = user_id
        self._email = email
        self._password = password
        self._first_name = first_name
        self._last_name = last_name

    def compare_passwords(self, password_repeat: str) -> bool:
        return self._password == password_repeat

    def hash_password(self) -> str:
        return bcrypt.hashpw(
            password=self._password.encode(), salt=bcrypt.gensalt()
        ).decode()
