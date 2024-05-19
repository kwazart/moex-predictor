import pandas as pd
import os
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "data.csv")
temp_data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "prepared-data.csv")
df = pd.read_csv(data_path)


def prepare_data():
    if 'ticker' in df.columns:
        df.index = df.ticker
        df.drop(['ticker'], axis=1, inplace=True)

    # Удалим строки в которых нет 80% значений
    df.dropna(thresh=len(df.index)/1.25, axis=0, inplace=True)

    # Удалим колонки с отсутствующими значениями. Т.к. "начинаются" с конца периода,
    # то данные будут отсутствовать у "ранних" колонок. В данном случае они нам не нужны.
    # По мере заполнения значений с биржи, колонок будет удаляться все меньше.
    df.dropna(axis=1, inplace=True)

    # В нашем случае у нас данные по каждому месяцу. Для тренировочных данных возьмем за таргет
    # данные за последний месяц. Для теста у нас будут те же самые данные,
    # но последний месяц уже не будет таргетом

    df.to_csv(temp_data_path, index=True)


def learn_model():

    # Найдем колонку с максимальной датой
    last_date_col = max(df.columns)

    # Разделяем данные на тренировочные и тестовые
    x = df.drop([last_date_col], axis=1)
    y = df[last_date_col]

    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10]
    }

    # Создание модели случайного леса
    rf = RandomForestRegressor(random_state=42)

    # Поиск по сетке для оптимизации гиперпараметров
    grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='neg_mean_squared_error')
    grid_search.fit(x, y)

    # Получение лучших параметров и обучение на них
    RFR = grid_search.best_estimator_
    RFR.fit(x, y)

    return RFR


def save_model(model):
    model_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "model.pkl")
    pickle.dump(model, open(model_path, 'wb'))


def process_model():
    prepare_data()
    model = learn_model()
    save_model(model)
