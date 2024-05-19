import pandas as pd
import os
import pickle


model_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "model.pkl")
prediction_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "prediction.csv")
temp_data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "prepared-data.csv")


def get_dataframe():
    df = pd.read_csv(temp_data_path)
    if 'ticker' in df.columns:
        df.index = df['ticker']
        df.drop(['ticker'], axis=1, inplace=True)
    return df


def predict():
    df = get_dataframe()

    # Найдем колонку с максимальной датой
    last_date_col = max(df.columns)

    df_new = df.copy()
    df_new.shift(-1, axis=1)
    df_new[last_date_col] = df[last_date_col]
    df_new.drop([last_date_col], axis=1, inplace=True)

    model = pickle.load(open(model_path, 'rb'))

    return model.predict(df_new)


def save_predictions(predictions):
    df = get_dataframe()
    result_df = pd.DataFrame(predictions, index=df.index, columns=['price'])
    result_df.to_csv(prediction_path, index=True)


def process_predictions():
    predictions = predict()
    save_predictions(predictions)
    return predictions


def get_predictions(predictions):
    df = get_dataframe()
    predictions = pd.DataFrame(predictions, index=df.index)
    os.remove(temp_data_path)
    return predictions.iloc[:, 0].to_dict()
