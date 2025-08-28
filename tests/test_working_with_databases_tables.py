def test_connect(db_handler):
    """Тест для метода connect."""
    handler, mock_cursor = db_handler
    handler.connect()
    assert handler.cursor is not None
    assert handler.connection is not None


def test_create_database(db_handler):
    """Тест для метода create_database."""
    handler, mock_cursor = db_handler
    handler.create_database()

    # Проверяем, что соединение было установлено и курсор использован
    mock_cursor.execute.assert_called_once_with(
        f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{handler.db_name}'"
    )


def test_create_tables(db_handler):
    """Тест для метода create_tables."""
    handler, mock_cursor = db_handler
    handler.create_tables()

    # Проверяем, что команды на создание таблиц были выполнены
    assert mock_cursor.execute.call_count == 2  # Должно быть два вызова execute


def test_insert_company_existing(db_handler):
    """Тест для метода insert_company при существующей компании."""
    handler, mock_cursor = db_handler

    mock_cursor.fetchone.return_value = (1,)  # Компания уже существует

    existing_company_id = handler.insert_company("Company A", 1)

    assert existing_company_id == 1
    mock_cursor.execute.assert_called_with(
        "SELECT id FROM employers WHERE hh_id = %s;", (1,)
    )


def test_insert_vacancy_existing(db_handler):
    """Тест для метода insert_vacancy при существующей вакансии."""
    handler, mock_cursor = db_handler

    mock_cursor.fetchone.side_effect = [
        (1,),
        (1,),
    ]  # Работодатель существует, вакансия уже существует

    existing_vacancy_id = handler.insert_vacancy(
        "Vacancy A", "Description", "http://example.com", 1
    )

    assert existing_vacancy_id == 1
    mock_cursor.execute.assert_called_with(
        "SELECT id FROM vacancies WHERE url = %s;", ("http://example.com",)
    )
