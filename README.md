# CUCON - Currency Converter Naive #
Entry task for a junior python developer position at KIWI.com
- - - -
## About ##
CLI currency converter application and web API written in Python 
- - - -
## Requirements ##
### CLI: ###
* Python 3.X
* Redis
* redis-server
### Web API: ###
* Python 3.X
* Redis
* redis-server
* flask
* gunicorn

_You can install those by 'sudo pip install [redis|flask|gunicorn]' or use 'pip3' if your default python version is 2.X_
This was tested on:
* gunicorn 19.8.1
* Python 3.5.2
* Redis server 3.0.6
* Redis 2.10.6
* flask 1.0.2
- - - -
## Source of conversion rates ##
cucon itself is using web API and in this application, it is API provided by **fixer.io** Its API stores currency rates for more than 168 currencies.
You can see more on <https://github.com/fixerAPI/fixer/>
- - - -
## Usage and functionality ##
Execute CLI with [-h|--help] flag to display program usage shown below.
```
./converter.py -h
```

```
usage: converter.py [-h] [-i INPUT_CURRENCY] [-o OUTPUT_CURRENCY] [-a AMOUNT]
                    [-l] [-u]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_CURRENCY, --input_currency INPUT_CURRENCY
                        Base/input currency - 3 letters name or currency
                        symbol.
  -o OUTPUT_CURRENCY, --output_currency OUTPUT_CURRENCY
                        Requested/output currency - 3 letters name or currency
                        symbol. If missing, convert to all known currencies.
  -a AMOUNT, --amount AMOUNT
                        Amount which we want to convert - float. It's set to
                        1.0 by default.
  -l, --list-available  List 168 available currencies along with the optional
                        symbols.
  -u, --force-update    Force update of the rates even if they are "still
                        valid" accroding to the update frequency.
```
- - - -

Web API string query arguments: 
```
?incurr=<input currency>&outcurr=<output currency>&amount=<amount to convert>&update&available
```
If there is present 'available' argument, server responds with JSON of available currency codes.
Otherwise only required argument when making a currency conversion request is 'incurr'.

EXAMPLES:
```
GET /cucon/?amount=0.9&incurr=¥&outcurr=AUD HTTP/1.1
GET /cucon/?incurr=£ HTTP/1.1
GET /cucon/?incurr=usd&update HTTP/1.1
GET /cucon?available HTTP/1.1
```
```
The output looks the same in both cases: It's JSON that looks with following structure:
{
    "input": { 
        "amount": <float>,
        "currency": <3 letter currency code>
    }
    "output": {
        <3 letter currency code>: <float>
    }
}
```
If the operation hasn't been completed successfully, JSON with following structure is returned:
```
{"msg" : "Message with some further information", "status_code" : <response status code>}
```
- - - -
## Supported currency codes table with optional unicode symbols##
COMMING SOON
- - - -
##  Note ##
This is just the most basic configuration for this purpose. If you want to use this tool in serious production, consider using gunicorn more widely with asynchronous workers, more options and ideally(recommended) deployed on nginx or other robust HTTP server.

* redis: <https://redis.io/>
* gunicorn: <http://gunicorn.org/>
* gevent: <http://www.gevent.org/>
* nginx: <https://www.nginx.com/>
