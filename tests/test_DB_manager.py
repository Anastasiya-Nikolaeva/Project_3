def test_get_companies_and_vacancies_count(db_manager):
    """Тест для метода get_companies_and_vacancies_count."""
    manager, mock_db_handler = db_manager
    mock_db_handler.cursor.fetchall.return_value = [("Company A", 5), ("Company B", 3)]

    result = manager.get_companies_and_vacancies_count()

    assert result == [("Company A", 5), ("Company B", 3)]
    mock_db_handler.cursor.execute.assert_called_once()


def test_get_all_vacancies(db_manager):
    """Тест для метода get_all_vacancies."""
    manager, mock_db_handler = db_manager
    mock_db_handler.cursor.fetchall.return_value = [
        ("Vacancy A", 1000, "Company A"),
        ("Vacancy B", 1500, "Company B"),
    ]

    result = manager.get_all_vacancies()

    assert result == [
        ("Vacancy A", 1000, "Company A"),
        ("Vacancy B", 1500, "Company B"),
    ]
    mock_db_handler.cursor.execute.assert_called_once()


def test_get_avg_salary(db_manager):
    """Тест для метода get_avg_salary."""
    manager, mock_db_handler = db_manager
    mock_db_handler.cursor.fetchone.return_value = (1200,)

    result = manager.get_avg_salary()

    assert result == 1200
    mock_db_handler.cursor.execute.assert_called_once()


def test_get_vacancies_with_higher_salary(db_manager):
    """Тест для метода get_vacancies_with_higher_salary."""
    manager, mock_db_handler = db_manager
    mock_db_handler.cursor.fetchone.return_value = (1200,)
    mock_db_handler.cursor.fetchall.return_value = [("Vacancy A", 1500, "Company A")]

    result = manager.get_vacancies_with_higher_salary()

    assert result == [("Vacancy A", 1500, "Company A")]
    mock_db_handler.cursor.execute.assert_called()


def test_get_vacancies_with_keyword(db_manager):
    """Тест для метода get_vacancies_with_keyword."""
    manager, mock_db_handler = db_manager
    mock_db_handler.cursor.fetchall.return_value = [("Vacancy A", 1000, "Company A")]

    result = manager.get_vacancies_with_keyword("Vacancy")

    assert result == [("Vacancy A", 1000, "Company A")]
    mock_db_handler.cursor.execute.assert_called_once()
