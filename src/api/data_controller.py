from fastapi import FastAPI
import os
import subprocess
from pathlib import Path

from src.model.predictor import process_predictions, get_predictions
from src.model.preprocessing import process_model
from src.dvc.dvc_handler import create_new_version, switch_head, get_current_tag, get_all_tags
from src.parser.price_parser import download_data, get_tickers

description = """
MOEX Predictor API helps you do prediction on future period (by default - half year). 🚀

## Data

You will be able to:

* **Init DVC** - dvc initialization with prices on tickers. (jenkins alternative)
* **Init new price downloading** - request for new price data from MOEX with saving at DVC (s3:minio).
* **Get all versions** - getting all versions of price data with date and time 
* **Get current version** - getting current version of price data 
* **Create new data version** - save current prices as new data version
* **Switch on specific version** - switching on a specific version of price data 
* **Switch on last version** - switching on a last version of price data 

## Tickers

You will be able to:

* **Get all tickers** - getting all tickers  
* **Add new ticker** - adding new ticker for future downloading (will be realized on 0.1.1 version)
* **Delete ticker by name** - remove ticker from ticker list (will be realized on 0.1.1 version)

## Model

You will be able to:

* **Init prediction** - initial prediction for all tickers and return all prices
* **Get prediction** - get prediction by ticker name
"""

tags_metadata = [
    {
        "name": "data",
        "description": "Manage price data.",
    },
    {
        "name": "ticker",
        "description": "Operations with data."
    },
    {
        "name": "model",
        "description": "Operations with data."
    }
]

app = FastAPI(
    docs_url='/',
    title='MOEX Predictor',
    summary='The app can be useful for prediction by MOEX ticker\'s.',
    description=description,
    version="0.1.0"
)
ROOT = Path(__file__).parent.parent.parent
data_path = "/data"
ticker_path = "/ticker"
model_path = "/model"
tag_version = "v"
master_branch = "master"


@app.post(data_path + "/init", tags=["data"], description="DVC and Git initialization")
def init_git_and_dvc():
    return subprocess.Popen([os.path.join(ROOT, "scripts", "init-dvc.sh")], shell=True)


@app.get(data_path, tags=["data"], description="Download data from MOEX")
def download_data():
    return download_data()


@app.get(data_path + "/versions", tags=["data"], description="Get all data versions")
def get_all_version():
    return get_all_tags()


@app.put(data_path, tags=["data"], description="Create new data version")
def create_new_data_version():
    create_new_version()
    return "OK"


@app.post(data_path + "/version/{tag}", tags=["data"], description="Switch to another data version")
def switch_version(tag: str):
    switch_head(tag)


@app.post(data_path + "/last", tags=["data"], description="Switch on the latest data version")
def switch_on_last_version():
    result = switch_head(master_branch)
    return result


@app.get(data_path + "/version", tags=["data"], description="Get current data version")
def get_current_version():
    return get_current_tag()


@app.post(model_path, tags=["model"], description="Get prediction from current price data version for all tickers")
def get_all_predictions():
    process_model()
    predictions = process_predictions()
    return get_predictions(predictions)


@app.get(model_path + "/{ticker_name}", tags=["ticker"],
         description="Get prediction from current price data version by ticker name")
def get_predictions_by_name(ticker_name):
    process_model()
    predictions = process_predictions()
    return get_predictions(predictions)[ticker_name]


@app.get(ticker_path, tags=["ticker"], description="Get all tickers")
def get_all_tickers():
    return get_tickers()
