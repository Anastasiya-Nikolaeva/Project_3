import os
from typing import Optional

import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DatabaseHandler:
    """Отвечает за создание БД и таблиц"""

    def __init__(self):
        self.db_name = "project_db"
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.connection = None
        self.cursor = None

        # Отладочный вывод
        print(f"DB_USER: {self.user}")
        print(f"DB_PASSWORD: {self.password}")
        print(f"DB_HOST: {self.host}")
        print(f"DB_PORT: {self.port}")

    def connect(self):
        """Подключается к базе данных."""
        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            self.cursor = self.connection.cursor()
            print("Connection successful")
        except psycopg2.OperationalError as e:
            print(f"OperationalError: {e}")
            self.cursor = None
        except Exception as e:
            print(f"An error occurred: {e}")
            self.cursor = None

    def create_database(self):
        """Создает базу данных, если она не существует."""
        conn = psycopg2.connect(
            user=self.user, password=self.password, host=self.host, port=self.port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.db_name}'"
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {self.db_name}")
        cursor.close()
        conn.close()

    def create_tables(self):
        """Создает необходимые таблицы в базе данных."""
        if self.cursor is None:
            print("Cursor is not initialized. Cannot create tables.")
            return

        try:
            create_employers_table = """
                CREATE TABLE IF NOT EXISTS employers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    hh_id INTEGER UNIQUE NOT NULL
                );
            """
            create_vacancies_table = """
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    employer_id INTEGER REFERENCES employers(id) ON DELETE CASCADE,
                    description TEXT,
                    url VARCHAR(255) UNIQUE,
                    salary NUMERIC  -- Добавляем столбец salary
                );
            """
            self.cursor.execute(create_employers_table)
            self.cursor.execute(create_vacancies_table)
            self.connection.commit()  # Подтверждаем изменения
            print("Tables created successfully.")
        except Exception as e:
            print(f"An error occurred while creating tables: {e}")
            self.connection.rollback()  # Откат изменений в случае ошибки

    def insert_company(self, name: str, hh_id: int):
        """Вставляет работодателя в таблицу."""
        if not self.check_encoding(name):
            print(f"Invalid encoding for company name: {name}")
            return None  # Пропустить вставку, если кодировка неверная

        # Проверка существования работодателя с таким hh_id
        self.cursor.execute("SELECT id FROM employers WHERE hh_id = %s;", (hh_id,))
        existing_company = self.cursor.fetchone()

        if existing_company:
            print(
                f"Company with hh_id {hh_id} already exists. Returning id {existing_company[0]}."
            )
            return existing_company[0]  # Возвращаем id существующей записи

        # Вставка нового работодателя
        self.cursor.execute(
            "INSERT INTO employers (name, hh_id) VALUES (%s, %s) RETURNING id;",
            (name, hh_id),
        )
        new_company_id = self.cursor.fetchone()[0]
        print(f"Inserted new company {name} with id {new_company_id}.")
        return new_company_id

    def insert_vacancy(
        self,
        title: str,
        description: str,
        url: str,
        employer_id: int,
        salary: Optional[float] = None,
    ):
        """Вставляет вакансию в таблицу."""
        if not self.check_encoding(title):
            print(f"Invalid encoding for vacancy title: {title}")
            return  # Пропустить вставку, если кодировка неверная

        # Проверка существования работодателя
        self.cursor.execute("SELECT id FROM employers WHERE id = %s;", (employer_id,))
        employer_exists = self.cursor.fetchone()

        if not employer_exists:
            print(f"Employer with id {employer_id} does not exist. Skipping insert.")
            return  # Пропустить вставку, если работодатель не существует

        # Проверка существования вакансии с таким url
        self.cursor.execute("SELECT id FROM vacancies WHERE url = %s;", (url,))
        existing_vacancy = self.cursor.fetchone()

        if existing_vacancy:
            print(f"Vacancy with url {url} already exists. Skipping insert.")
            return existing_vacancy[0]  # Возвращаем id существующей записи

        # Вставка новой вакансии
        self.cursor.execute(
            "INSERT INTO vacancies (title, description, url, employer_id, salary) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (title, description, url, employer_id, salary),  # Добавляем salary в запрос
        )
        return self.cursor.fetchone()[0]

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed.")

    @staticmethod
    def check_encoding(data):
        """Проверяет кодировку строки и выводит ошибки, если они есть."""
        if not isinstance(data, str):
            print("Input data is not a string.")
            return False
        try:
            # Попробуйте декодировать строку в UTF-8
            data.encode("utf-8").decode("utf-8")
            return True
        except UnicodeDecodeError as e:
            print(f"Encoding error: {e}")
            return False
