import os

import pytest

from src.DB_manager import DBManager
from src.vacancy_api_handler import HeadHunter
from src.working_with_databases_tables import DatabaseHandler


@pytest.fixture
def db_manager(mocker):
    """Создает экземпляр DBManager с замоканным DatabaseHandler."""
    mock_db_handler = mocker.Mock()
    return DBManager(mock_db_handler), mock_db_handler


@pytest.fixture
def headhunter(mocker):
    """Создает экземпляр HeadHunter и заменяет requests.get на мок."""
    hh = HeadHunter()
    return hh


@pytest.fixture
def db_handler(mocker):
    """Создает экземпляр DatabaseHandler и заменяет psycopg2.connect на мок."""
    mock_connection = mocker.Mock()
    mock_cursor = mock_connection.cursor.return_value

    mocker.patch("psycopg2.connect", return_value=mock_connection)

    # Устанавливаем переменные окружения для теста
    os.environ["DB_USER"] = "test_user"
    os.environ["DB_PASSWORD"] = "test_password"
    os.environ["DB_HOST"] = "localhost"
    os.environ["DB_PORT"] = "5432"

    handler = DatabaseHandler()
    handler.connect()  # Подключаемся к базе данных
    return handler, mock_cursor
