# MOEX PREDICTOR

#### The app can be useful for next month prediction by tickers from the MOEX exchange.

## *Version:* 0.1.0


### Algorithm:
0. Running the app:
    - Get credentials from s3 minio and write it credentials in file - *init-dvc.sh* (you can use the script - *minio.sh*)
    - `docker-compose up -d --build`
    - Create a [Jenkins job](http://127.0.0.1:8000/) - *pipe-1-Init-project* file and start one
1. Getting tickers from the local storage
2. Downloading price data from the MOEX exchange for the last 10 years with prices for each month.
3. Preparing price data: clean empty line which does not contain price more than 80 percents.
4. Learning model: RandomForestRegressor as first version.
5. Saving model as pickle file.
6. Provision of REST API as [Swagger](http://127.0.0.1:8001/)


### Swagger methods

#### Data

You will be able to:

* **Init DVC** - dvc initialization with prices on tickers. (jenkins alternative)
* **Init new price downloading** - request for new price data from MOEX with saving at DVC (s3:minio).
* **Get all versions** - getting all versions of price data with date and time 
* **Get current version** - getting current version of price data 
* **Create new data version** - save current prices as new data version
* **Switch on specific version** - switching on a specific version of price data 
* **Switch on last version** - switching on a last version of price data 

#### Tickers

You will be able to:

* **Get all tickers** - getting all tickers

#### Model

You will be able to:

* **Init prediction** - initial prediction for all tickers and return all prices
* **Get prediction** - get prediction by ticker name
