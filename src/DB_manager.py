import os

from dotenv import load_dotenv

from src.working_with_databases_tables import DatabaseHandler

load_dotenv()


class DBManager:
    """Класс для управления данными в БД."""

    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler

        # Получаем данные для подключения из переменных окружения
        self.db_name = "project_db"
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")

    def get_employers_and_vacancies_count(self):
        """Получает список всех работодателей и количество вакансий у каждого работодателя."""
        self.db_handler.cursor.execute(
            """
            SELECT e.name, COUNT(v.id)
            FROM employers e
            LEFT JOIN vacancies v ON e.id = v.employer_id
            GROUP BY e.id;
            """
        )
        return self.db_handler.cursor.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия работодателя, названия вакансии и зарплаты."""
        self.db_handler.cursor.execute(
            """
            SELECT v.title, v.salary, e.name
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.id;
            """
        )
        return self.db_handler.cursor.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        self.db_handler.cursor.execute(
            "SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL;"
        )
        return self.db_handler.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        self.db_handler.cursor.execute(
            """
            SELECT v.title, v.salary, e.name
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.id
            WHERE v.salary > %s;
            """,
            (avg_salary,),
        )
        return self.db_handler.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        self.db_handler.cursor.execute(
            """
            SELECT v.title, v.salary, e.name
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.id
            WHERE v.title ILIKE %s;
            """,
            (f"%{keyword}%",),
        )
        return self.db_handler.cursor.fetchall()
