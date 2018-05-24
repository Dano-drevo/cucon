from redis import StrictRedis
from datetime import timedelta
from json import loads
import requests
import logging
    
#class representing communication with the currency rates API server
class Server():
    def __init__(self):
        self.private_access_key = 'd572ff8fcf4cfad6ac91e8223341379b'
        self.url = 'http://data.fixer.io/api/latest?access_key=' + self.private_access_key

    def get_server_response(self, base):
        url = self.url + '&base=' + str(base)
        response = requests.get(url)
        return response

#class containing all the methods for fetching and maintaining the currency rates data 
class My_redis():
    def __init__(self, static_object, from_currency, to_currency=None):
        self.host = 'localhost'
        self.port = 6379
        self.db = StrictRedis(host=self.host, port=self.port, db=0)
        self.from_curr = from_currency
        self.to_curr = to_currency
        self.obj = static_object
        self.other_currencies = self.obj.codes_set ^ {self.from_curr}

#firstly check if there is need of the update
    def get_rates(self, force_update=False):
        if self.to_curr is self.from_curr:
            return {self.from_curr : '1.0'}

#"if 'msg' in output" means that some problem occured with the request  
        output = self.update_base(force_update)
        if 'msg' in output: 
                return output

#if there is no output currency convert to all
        if self.to_curr is None:
            if not output:
                for other_curr in self.other_currencies:
                    output[other_curr] = self.db.get(self.from_curr + other_curr)
            else:   
                pass
        else:
            if self.db.exists(self.from_curr+self.to_curr):
                if not output:
                    output[self.to_curr] = self.db.get(self.from_curr + self.to_curr)
                else:
                    output = {self.to_curr:output[self.to_curr]}               

            else:
                if self.to_curr not in output:
                    return {'msg':'Could not obtain actual rates for conversion: {}-->{}'.format(self.from_curr, self.to_curr)}
        return output

#function for checking validity and expiration of the rates, eventually 
#when used with force_update=True, it automatically invokes getting a latest available currency rates
    def update_base(self, force_update):
            if force_update is True:
                if self.db.exists(self.from_curr):
                    timestamp = self.db.get(self.from_curr+'TIME') 
                    if int(timestamp) + 3600 < int(self.db.time()[0]):
                        self.db.delete(self.from_curr)
                        return self.set_rates()
                    else:   
                        pass

            if self.db.exists(self.from_curr):
                    return {}
            else:
                return self.set_rates()

#method that creates the Server instance and menage the set/get data process   
    def set_rates(self): 
        response = Server().get_server_response(self.from_curr)
        response_dic = loads(response.text)
        status = response.status_code 
        if status != 200:
            self.db.delete(self.from_curr)
            return {'msg':'Very naughty server !' , 'status_code': +str(status)}
        
        elif response_dic['base'] != self.from_curr:
            return {'msg':"Couldn't obtain data for '"+self.from_curr+"'.", 'status_code':str(status)}

        else:
            result = self.set_and_save(response_dic['rates'])
            number_of_others = len(self.obj.codes_set)-1
            if len(result) == number_of_others:
                print('Base UPDATE: ' + self.from_curr + ' --> SUCCESS')
            elif len(result) != 0: 
                if self.to_curr is not None:
                    additional='To get list of successfully updated codes for base {}, execute without output currency option.'.format(self.from_curr)
                else:
                    additional=''
                print('Base UPDATE: {} --> FAIL, SUCCESSFULL: {}/{}\n{}'.format(self.from_curr, str(len(result)), str(number_of_others),additional))
            return result

              
#final step of this method waterfall, sets a rate and expiration mark on base KEY and generate output             
    def set_and_save(self, dic):
        self.db.set(self.from_curr+'TIME', self.db.time()[0])
        self.obj.update_freq = timedelta(**self.obj.update_freq)  
        self.db.set(self.from_curr,'')
        self.db.expire(self.from_curr, self.obj.update_freq)
        valid_rates = dict()
        error = None
        other_currs = self.other_currencies
        for currency in other_currs:
            try:
                self.db.set(self.from_curr + currency, dic[currency])
                self.db.expire(self.from_curr + currency, self.obj.update_freq)
                valid_rates[currency] = dic[currency]
            except Exception as e:
                error = e            
                pass
        if len(valid_rates) > 0:
            return valid_rates
        else:
            return {'msg':"Base {} couldn't be updated. Server must have sent us some ugly data or redis is not working correctly.".formt(self.currency), 'status_code':503,'error': str(error)}

