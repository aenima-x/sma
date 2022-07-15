# Stock Market API Service

----------------

### How to run local

Clone the repo

```bash
git clone https://github.com/aenima-x/sma.git
cd sma
```

Launch docker-compose
```bash
docker-compose up
```

Run tests

```bash
docker-compose run app python manage.py test
```

### How to use the API

Get token

```bash
curl -X POST http://localhost:8000/api/signup -H 'Content-Type: application/json' -d '{"email":"user@email.com","name":"name", "lastname": "lastname"}'
# {"token":"ABC"}
```

Request stock info

```bash
curl -X POST -H "Authorization: Token ABC" http://localhost:8000/api/stocks/AAPL
# {"symbol":"AAPL","open":142.99,"lower":142.1201,"higher":146.45,"close_variation":0.37}
```


### Throttling

I've implemented Throttling using the DRF Throttling option
```bash
curl -X POST -H "Authorization: Token e6a745ab7a7aa5651d925e3a32031e6df0570d03" http://localhost:8000/api/stocks/AAPL
#{"symbol":"AAPL","open":142.99,"lower":142.1201,"higher":146.45,"close_variation":0.37}
curl -X POST -H "Authorization: Token e6a745ab7a7aa5651d925e3a32031e6df0570d03" http://localhost:8000/api/stocks/AAPL
#{"symbol":"AAPL","open":142.99,"lower":142.1201,"higher":146.45,"close_variation":0.37}
curl -X POST -H "Authorization: Token e6a745ab7a7aa5651d925e3a32031e6df0570d03" http://localhost:8000/api/stocks/AAPL
#{"symbol":"AAPL","open":142.99,"lower":142.1201,"higher":146.45,"close_variation":0.37}
curl -X POST -H "Authorization: Token e6a745ab7a7aa5651d925e3a32031e6df0570d03" http://localhost:8000/api/stocks/AAPL
#{"symbol":"AAPL","open":142.99,"lower":142.1201,"higher":146.45,"close_variation":0.37}
curl -X POST -H "Authorization: Token e6a745ab7a7aa5651d925e3a32031e6df0570d03" http://localhost:8000/api/stocks/AAPL
#{"detail":"Request was throttled. Expected available in 54 seconds."}
```

### Heroku

The app is deployed in Heroku on https://aenima-sma.herokuapp.com

The deploy is made on merge to master using github actions

