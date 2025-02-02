import pytest


def test_connect_to_api_success(headhunter, mocker):
    """Тест для метода _connect_to_api при успешном подключении."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}

    mocker.patch("requests.get", return_value=mock_response)

    result = headhunter._connect_to_api({"per_page": 1, "page": 0})

    assert result == {"key": "value"}
    mock_response.json.assert_called_once()


def test_connect_to_api_failure(headhunter, mocker):
    """Тест для метода _connect_to_api при ошибке подключения."""
    mock_response = mocker.Mock()
    mock_response.status_code = 404

    mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(Exception) as excinfo:
        headhunter._connect_to_api({"per_page": 1, "page": 0})

    assert "Ошибка при подключении к API: 404" in str(excinfo.value)


def test_get_companies_success(headhunter, mocker):
    """Тест для метода get_companies при успешном запросе."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "1", "name": "Company A"}

    mocker.patch("requests.get", return_value=mock_response)

    result = headhunter.get_companies(["1"])

    assert result == [{"id": "1", "name": "Company A"}]


def test_get_companies_failure(headhunter, mocker):
    """Тест для метода get_companies при ошибке запроса."""
    mock_response = mocker.Mock()
    mock_response.status_code = 404

    mocker.patch("requests.get", return_value=mock_response)

    result = headhunter.get_companies(["1"])

    assert result == []


def test_get_vacancies_success(headhunter, mocker):
    """Тест для метода get_vacancies при успешном запросе."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"id": "1", "title": "Vacancy A"}]}

    mocker.patch("requests.get", return_value=mock_response)

    result = headhunter.get_vacancies("1")

    assert result == [{"id": "1", "title": "Vacancy A"}]


def test_get_vacancies_failure(headhunter, mocker):
    """Тест для метода get_vacancies при ошибке запроса."""
    mock_response = mocker.Mock()
    mock_response.status_code = 404

    mocker.patch("requests.get", return_value=mock_response)

    result = headhunter.get_vacancies("1")

    assert result == []
