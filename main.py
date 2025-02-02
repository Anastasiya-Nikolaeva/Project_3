import logging

from src.DB_manager import DBManager
from src.vacancy_api_handler import HeadHunter
from src.working_with_databases_tables import DatabaseHandler


def main():
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)

    # Список работодателей
    employers = [
        {"name": "Яндекс", "hh_id": 1740},
        {"name": "Т-банк", "hh_id": 78638},
        {"name": "Сбер. IT", "hh_id": 3529},
        {"name": "МТС", "hh_id": 3776},
        {"name": "Роснефть", "hh_id": 239363},
        {"name": "Газпром", "hh_id": 5778059},
        {"name": "Ростелеком", "hh_id": 2748},
        {"name": "Лаборатория Касперского", "hh_id": 1057},
        {"name": "Ozon", "hh_id": 1057},
        {"name": "Все Инструменты.ру", "hh_id": 208707},
    ]

    # Инициализация классов
    db_handler = DatabaseHandler()
    db_handler.create_database()  # Создаем базу данных, если она не существует
    db_handler.connect()
    db_handler.create_tables()

    hh_api = HeadHunter()
    db_manager = DBManager(db_handler)  # Создаем экземпляр DBManager

    # Заполнение базы данных
    for employer in employers:
        # Вставка компании
        company_id = db_handler.insert_company(employer["name"], employer["hh_id"])
        if company_id is None:
            print(f"Failed to insert company: {employer['name']}")
            continue  # Пропустить, если кодировка неверная или компания уже существует

        # Получаем вакансии для текущего работодателя
        vacancies = hh_api.get_vacancies_by_employer(employer["hh_id"])

        for vacancy in vacancies:
            if vacancy is None:
                continue

            # Получаем информацию о зарплате
            salary_info = vacancy.get("salary")
            salary = salary_info.get("from") if salary_info else None  # Получаем зарплату, если она указана

            # Вставка вакансии в базу данных
            vacancy_id = db_handler.insert_vacancy(
                vacancy["name"],
                vacancy.get("description", ""),
                vacancy.get("url", ""),
                company_id,
                salary,
            )
            if vacancy_id is None:
                print(f"Failed to insert vacancy: {vacancy['name']} for company id: {company_id}")

    # Сохраняем изменения в базе данных
    db_handler.connection.commit()

    # Используем методы из db_manager
    employers_and_vacancies = db_manager.get_employers_and_vacancies_count()
    print("Работодатели и количество вакансий:")
    for employer in employers_and_vacancies:
        print(f"Работодатель: {employer[0]}, Количество вакансий: {employer[1]}")

    all_vacancies = db_manager.get_all_vacancies()
    print("Все вакансии:")
    for vacancy in all_vacancies:
        print(f"Вакансия: {vacancy[0]}, Зарплата: {vacancy[1]}, Компания: {vacancy[2]}")

    avg_salary = db_manager.get_avg_salary()
    print(f"Средняя зарплата: {avg_salary}")

    higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    print("Вакансии с зарплатой выше средней:")
    for vacancy in higher_salary_vacancies:
        print(f"Вакансия: {vacancy[0]}, Зарплата: {vacancy[1]}, Компания: {vacancy[2]}")

    keyword = input("Введите ключевое слово для поиска вакансий: ")
    keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
    print(f"Вакансии по ключевому слову '{keyword}':")
    for vacancy in keyword_vacancies:
        print(f"Вакансия: {vacancy[0]}, Зарплата: {vacancy[1]}, Компания: {vacancy[2]}")

    # Закрытие соединения с БД
    db_handler.close()


if __name__ == "__main__":
    main()
