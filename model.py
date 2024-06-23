import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from config import host, user, password, db_name, port


class MarketsModel:
    def __init__(self):
        self.connection_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'
        self.engine = create_engine(self.connection_string)
        self.controller = None
        self.data_frame = None  # Инициализация пустого data_frame

    def set_controller(self, controller):
        self.controller = controller

    def load_data(self):
        engine = create_engine(self.connection_string)
        # Чтение из SQL базы данных
        query = """
        SELECT m.marketname as Market, r.rating as Rating
        FROM markets m
        LEFT JOIN reviews r ON m.fmid = r.marketid
        ORDER BY m.marketname ASC
        """
        self.data_frame = pd.read_sql(query, engine)

        # Группировка по рынку и вычисление среднего рейтинга
        self.data_frame = self.data_frame.groupby('market', as_index=False).agg({'rating': 'mean'}).round(2)

    def reload_data(self):
        self.load_data()
        if self.controller:
            self.controller.update_table()

    def search_markets(self, city=None, state=None, zip_code=None):
        engine = create_engine(self.connection_string)

        # SQL-запрос с использованием %s параметров
        query = """
        SELECT m.marketname as market, r.rating as rating
        FROM markets m
        LEFT JOIN reviews r ON m.fmid = r.marketid
        WHERE 1=1
        """
        params = {}
        filters = []
        if city:
            query += " AND m.city ILIKE %(city)s"
            params['city'] = f'%{city}%'

        if state:
            query += " AND m.state ILIKE %(state)s"
            params['state'] = f'%{state}%'

        if zip_code:
            query += " AND m.zip = %(zip)s"
            params['zip'] = zip_code

        if filters:
            query += " AND " + " AND ".join(filters)

        query += " ORDER BY m.marketname ASC"

        self.data_frame = pd.read_sql(query, engine, params=params)

        # Группировка по рынку и вычисление среднего рейтинга
        self.data_frame = self.data_frame.groupby('market', as_index=False).agg({'rating': 'mean'}).round(2)

    def get_page(self, page_number, page_size):
        if self.data_frame is not None:
            start_index = page_number * page_size
            end_index = start_index + page_size
            return self.data_frame.iloc[start_index:end_index]
        return pd.DataFrame()

    def get_total_pages(self, page_size):
        if self.data_frame is not None:
            return (len(self.data_frame) + page_size - 1) // page_size
        return 0

    def get_market_details(self, market_name):
        engine = create_engine(self.connection_string)
        query = """
        SELECT *
        FROM markets
        WHERE marketname = %(market_name)s
        """
        details = pd.read_sql(query, engine, params={'market_name': market_name})

        # Удаление столбца 'fmid' из DataFrame, если он существует
        if 'fmid' in details.columns:
            details = details.drop(columns=['fmid'])

        # Удаление столбцов с NaN значениями (метод dropna())
        details = details.dropna(axis=1, how='all')

        # Заменяем значения TRUE на "Yes"
        details = details.replace({True: "Yes"})

        # Создание нового DataFrame только со столбцами, равными True
        boolean_columns = [col for col in details.columns if details[col].dtype == bool and details[col].all()]
        non_boolean_columns = [col for col in details.columns if details[col].dtype != bool]

        # Формируем итоговый результат
        result_columns = non_boolean_columns + boolean_columns
        filtered_details = details[result_columns]

        return filtered_details

    def insert_user(self, first_name, last_name):
        with self.engine.connect() as conn:
            query = text("""
            INSERT INTO users (firstname, lastname) 
            VALUES (:first_name, :last_name)
            RETURNING userid
            """)
            result = conn.execute(query, {'first_name': first_name, 'last_name': last_name})
            user_id = result.scalar()
            conn.commit()  # commit для подтверждения транзакции
            # print(f"Inserted user ID: {user_id}")  # Проверить возвращаемый user_id
            return user_id

    def check_user_exists(self, user_id):
        with self.engine.connect() as conn:
            query = text("SELECT 1 FROM users WHERE userid = :user_id")
            result = conn.execute(query, {'user_id': user_id})
            return result.fetchone() is not None

    def insert_review(self, market_id, user_id, rating, review_text):
        if not self.check_user_exists(user_id):
            print(f"User ID {user_id} does not exist in users table.")
            return

        with self.engine.connect() as conn:
            query = text("""
                INSERT INTO reviews (marketid, userid, rating, reviewtext) 
                VALUES (:marketid, :userid, :rating, :reviewtext)
            """)
            conn.execute(query, {
                'marketid': market_id,
                'userid': user_id,
                'rating': rating,
                'reviewtext': review_text
            })
            conn.commit()
            # print(f"Inserted review for user ID: {user_id}")

            # Перезагрузка данных после добавления нового отзыва
            self.reload_data()

    def get_user_id(self, first_name, last_name):
        with self.engine.connect() as conn:
            query = text("SELECT userid FROM users WHERE firstname = :first_name AND lastname = :last_name")
            result = conn.execute(query, {'first_name': first_name, 'last_name': last_name})
            row = result.fetchone()
            return row[0] if row else None

    def get_market_id(self, market_name):
        with self.engine.connect() as conn:
            query = text("SELECT fmid FROM markets WHERE marketname = :market_name")
            result = conn.execute(query, {'market_name': market_name})
            row = result.fetchone()
            return row[0] if row else None
