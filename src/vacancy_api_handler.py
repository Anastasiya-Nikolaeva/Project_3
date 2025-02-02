from typing import Any, Dict, List

import requests


class HeadHunter:
    """Класс для работы с API HeadHunter"""

    def __init__(self) -> None:
        self._url: str = "https://api.hh.ru/vacancies"
        self._headers: Dict[str, str] = {"User-Agent": "HH-User-Agent"}
        self._params: Dict[str, Any] = {"per_page": 1, "page": 0}

    def _connect_to_api(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Подключается к API hh.ru и проверяет статус-код ответа"""
        response = requests.get(self._url, headers=self._headers, params=params)
        print(f"Запрос: {response.url}")  # Логирование URL запроса
        print(f"Статус код: {response.status_code}")  # Логирование статуса
        print(f"Ответ: {response.text}")  # Логирование текста ответа
        if response.status_code != 200:
            raise Exception(f"Ошибка при подключении к API: {response.status_code}")
        return response.json()

    def get_companies(self, company_ids: List[str]) -> List[Dict]:
        """Получает данные о компаниях по их ID."""
        companies = []
        for company_id in company_ids:
            response = requests.get(f"{self._url}/employers/{company_id}")
            if response.status_code == 200:
                companies.append(response.json())
        return companies

    def get_vacancies(self, company_id: str) -> List[Dict]:
        """Получает вакансии для указанной компании."""
        response = requests.get(f"{self._url}/vacancies?employer_id={company_id}")
        if response.status_code == 200:
            return response.json().get("items", [])
        return []

    @staticmethod
    def get_vacancies_by_employer(hh_id):
        response = requests.get(f"https://api.hh.ru/vacancies?employer_id={hh_id}")
        if response.status_code == 200:
            data = response.json()
            print(
                f"Vacancies for employer ID {hh_id}: {data.get('items', [])}"
            )  # Отладочный вывод
            return data.get("items", [])
        else:
            print(
                f"Error fetching vacancies for employer ID {hh_id}: {response.status_code}"
            )
            return None
