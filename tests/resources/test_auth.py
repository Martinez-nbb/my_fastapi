import pytest

from src.resources.auth import get_password_hash, verify_password


class TestPasswordHashing:
    def test_get_password_hash_returns_string(self):
        """Тест генерации хеша пароля."""
        password = "test_password_123"
        hashed = get_password_hash(password)

        assert isinstance(hashed, str)
        assert hashed != password

    def test_verify_password_with_correct_password(self):
        """Тест проверки правильного пароля."""
        password = "my_secure_password"
        hashed = get_password_hash(password)

        result = verify_password(password, hashed)

        assert result is True

    def test_verify_password_with_wrong_password(self):
        """Тест проверки неправильного пароля."""
        password = "correct_password"
        hashed = get_password_hash(password)

        result = verify_password("wrong_password", hashed)

        assert result is False

    def test_different_hashes_for_same_password(self):
        """Тест разных хешей для одного пароля (bcrypt добавляет соль)."""
        password = "same_password"

        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        assert hash1 != hash2
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True

    def test_verify_password_with_empty_password(self):
        """Тест проверки пустого пароля."""
        hashed = get_password_hash("password")

        result = verify_password("", hashed)

        assert result is False

    def test_password_hash_truncates_long_password(self):
        """Тест обработки длинного пароля (обрезается до 72 байт)."""
        long_password = "a" * 100

        hashed = get_password_hash(long_password)

        assert isinstance(hashed, str)
        assert verify_password(long_password[:72], hashed) is True

    def test_verify_unicode_password(self):
        """Тест работы с unicode паролями."""
        password = "пароль_кириллица_123"
        hashed = get_password_hash(password)

        result = verify_password(password, hashed)

        assert result is True