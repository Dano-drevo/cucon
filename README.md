# CUCON - Currency Converter Naive #
Entry task for a junior python developer position at **KIWI.com**
- - - -
## About ##
CLI currency converter application and web API with the very same function, both written in Python.
<br/>
<br/>
The program accepts input and then searches for given base in redis database, if the key is not found, cucon obtains the latest rates by the HTTP request to fixer.io and stores them to a redis database with the pre-set expiration date according to the update frequency.
<br/>
If the key exceeds its expiration time, redis will automatically delete it along with the rates. Update frequency is 1 hour minimum because hour is the update frequency of the source rates themselves. The [--update|-u] or [latest|update] argument in CLI or API(respectively), forces updating even if the key still exists and rates are 'up to date'. However, the rates are thus updated only if they are older than one hours.

When starting the API, we use gunicorn to create various synchronious workers(separate processes) to single-handle requests sent to the server. 
- - - -
## Requirements ##
#### fixer.io private access key ####
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

You can install those by following command:
```bash
sudo pip install [redis|redis-server|flask|gunicorn]
```
or
```bash
sudo pip3 install [redis|redis-server|flask|gunicorn]
```
if your default python version is 2.X
- - - - - - - -
Cucon was tested on:
* gunicorn 19.8.1
* Python 3.5.2
* redis-server 3.0.6
* Redis 2.10.6
* flask 1.0.2
- - - -
## Source of conversion rates ##
Cucon itself is using web API and in this application, it is API provided by [**fixer.io**](https://fixer.io/ "See fixer page!"). Its API stores currency rates for more than 168 currencies.
You can see more on <https://github.com/fixerAPI/fixer/>
- - - -
## Usage and functionality ##
Execute CLI with [-h|--help] flag to display program usage shown below.
```bash
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
?available
&
incurr=<input currency>
&
outcurr=<output currency>
&
amount=<amount to convert>
&
update 
&
latest 
```
where _(/?latest == /?update)_<br/>
If there is present '**available**' argument, server responds with the JSON of available currency codes.
Otherwise the only required argument when making a currency conversion request is '**incurr**'.

### EXAMPLES: ###
```bash
./converter.py --amount 100.0 --input_currency EUR --output_currency czk
./converter.py --input_currrency $
./converter.py -i ¥ -o aud -a 0.9
./converter.py -i ¥ -o £ -a 1221 -u
./converter.py -l

```

```
GET /cucon/?amount=0.9&incurr=¥&outcurr=AUD HTTP/1.0
GET /cucon/?incurr=£ HTTP/1.0
GET /cucon/?incurr=£ HTTP/1.0latest
GET /cucon/?incurr=usd&update HTTP/1.0
GET /cucon?available HTTP/1.0
```
- - - - - - - -
```
The output looks the same in both cases: It's JSON that looks like this:
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
If the operation within cucon hasn't been completed successfully, JSON with the following structure is returned:
```
{"msg" : "Message with some further information", "status_code" : <response status code>}
```
- - - -
## Supported currency codes table with the optional unicode symbols 
See [Supported currency codes table](currency_codes.md)
- - - -
##  Note ##
This is just the most basic configuration for this purpose. If you want to use this tool in a serious production, consider using gunicorn more widely with the asynchronous workers, more running options and ideally(recommended) deployed on nginx, apache or other robust HTTP server.

* [flask](http://flask.pocoo.org/)
* [redis](https://redis.io/)
* [gunicorn](http://gunicorn.org/)
* [gevent](http://www.gevent.org/)
* [nginx](https://www.nginx.com/)
