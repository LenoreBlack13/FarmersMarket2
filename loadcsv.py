import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from config import host, user, password, db_name, port


def load_csv():
    try:
        connection_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'
        engine = create_engine(connection_string)

        df = pd.read_csv('Export/Export.csv')

        # Приведение названий столбцов к нижнему регистру
        df.columns = [col.lower() for col in df.columns]

        # Преобразование столбца updatetime к правильному формату
        df['updatetime'] = pd.to_datetime(df['updatetime'], format='%m/%d/%Y %I:%M:%S %p')
        df['updatetime'] = df['updatetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Заменяем символ "-" на None в boolean столбцах
        bool_columns = ['credit', 'wic', 'wiccash', 'sfmnp', 'snap', 'organic', 'bakedgoods',
                        'cheese', 'crafts', 'flowers', 'eggs', 'seafood', 'herbs', 'vegetables',
                        'honey', 'jams', 'maple', 'meat', 'nursery', 'nuts', 'plants', 'poultry',
                        'prepared', 'soap', 'trees', 'wine', 'coffee', 'beans', 'fruits', 'grains',
                        'juices', 'mushrooms', 'petfood', 'tofu', 'wildharvested']

        for col in bool_columns:
            df[col] = df[col].replace('-', None)

        df.to_sql('markets', engine, index=False, if_exists='append')
        print(f'Данные из файла успешно загружены')
    except Exception as e:
        print(f'Произошла ошибка:{e}')


if __name__ == '__main__':
    load_csv()