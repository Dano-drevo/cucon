#!/usr/bin/python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from json import dumps
from decimal import Decimal
from my_redis import Server, My_redis


#object containing the important manually configurable data the app is using,
#as update frequency or set of codes (that are usable by app) along with their optional symbols in unicode decoding.
class Static():
    def __init__(self):
        #Update frequency for all currencies, default is 1 day, rates for each currency are updated at different time.
        #The currency rates are updated only if there is a request made for the base. 
        #However, you can obtain current rates by passing [-u|--update] flag with the command.
        #This private key unlocks hourly updated rates, therefore, updating more often is considered useless
        self.update_freq = {'weeks' : 0,                            
                            'days' : 0,
                            'hours' : 1}
 
                            
        self.codes_set = {'TJS', 'COP', 'FKP', 'DJF', 'BGN', 'SCR', 'IRR', 'CAD', 'ZMW', 'LKR', 'BSD', 'MWK', 'KES', 'BRL', 'BIF', 'PKR', 'GHS', 'EUR', 'ALL', 'SLL', 'JMD', 'RON', 'KRW', 'BAM', 'GIP', 'UGX', 'XAG', 'INR', 'TWD', 'CHF', 'TTD', 'PLN', 'XDR', 'XCD', 'AUD', 'PGK', 'LYD', 'PEN', 'SVC', 'MRO', 'UYU', 'AFN', 'GMD', 'ISK', 'TZS', 'EGP', 'MKD', 'THB', 'ANG', 'STD', 'DOP', 'PAB', 'HNL', 'CLF', 'CRC', 'BHD', 'JEP', 'SEK', 'YER', 'TRY', 'CNY', 'GBP', 'HRK', 'RUB', 'SBD', 'CUC', 'BND', 'MUR', 'VND', 'GNF', 'RSD', 'SOS', 'SZL', 'JPY', 'TMT', 'MYR', 'NOK', 'MAD', 'XPF', 'MMK', 'BTN', 'SHP', 'GGP', 'KGS', 'KPW', 'KYD', 'BMD', 'BBD', 'AOA', 'JOD', 'AMD', 'HTG', 'XOF', 'MOP', 'BYR', 'RWF', 'LAK', 'TOP', 'AWG', 'VUV', 'NZD', 'CDF', 'LVL', 'IDR', 'QAR', 'LSL', 'UZS', 'MNT', 'OMR', 'WST', 'BOB', 'TND', 'HKD', 'DZD', 'MGA', 'BDT', 'GEL', 'MDL', 'ERN', 'XAU', 'AED', 'NIO', 'IMP', 'KWD', 'KHR', 'GTQ', 'PYG', 'XAF', 'LTL', 'CZK', 'MVR', 'LRD', 'DKK', 'ZAR', 'SRD', 'KMF', 'UAH', 'CVE', 'NPR', 'NAD', 'GYD', 'FJD', 'BYN', 'HUF', 'LBP', 'SDG', 'BWP', 'SAR', 'ARS', 'ILS', 'BZD', 'ZMK', 'MXN', 'AZN', 'SGD', 'CUP', 'KZT', 'IQD', 'PHP', 'MZN', 'NGN', 'VEF', 'SYP', 'CLP', 'ZWL', 'BTC', 'ETB', 'USD'}

        self.dic={u'\u20b4':'UAH', u'\u0631.\u0633':'SAR', u'\u0631.\u0639.':'OMR', u'\u0434\u0435\u043d':'MKD', u'\u062f.\u0645.':'MAD', u'\u0644.\u0644':'LBP', u'\u062f.\u0643':'KWD', u'\u062f.\u0627':'JOD', u'\ufdfc':'IRR', u'\u10da':'GEL', u'\u20a3':'XAF', u'Rp': 'IDR', u'\u0534':'AMD', u'\u20ac': 'EUR', u'\u0783.': 'MVR', u'FMG': 'MGA', u'\u20ae': 'MNT', u'Sh.': 'SOS', u'\u0024': 'USD', u'\u20ab': 'VND', u'K\u010d': 'CZK', u'RM': 'MYR', u'D': 'GMD', u'Nfa': 'ERN', u'\u043b\u0432': 'KGS', u'KY\u0024': 'KYD', u'R\u0024': 'BRL', u'\u062f.\u0639': 'IQD', u'\u3012': 'KZT', u'HK\u0024': 'HKD', u'SI\u0024': 'SBD', u'J\u0024': 'JMD', u'\u0192': 'AWG', u'Afs': 'AFN', u'BD\u0024': 'BMD', u'KSh': 'KES', u'\u0e3f': 'THB', u'G': 'HTG', u'ZK': 'ZMK', u'TT\u0024': 'TTD', u'\u20b5': 'GHS', u'NA\u0192': 'ANG', u'MK': 'MWK', u'S/.': 'PEN', u'UM': 'MRO', u'Le': 'SLL', u'B./': 'PAB', u'FG': 'GNF', u'NT\u0024': 'TWD', u'S\u0024': 'SGD', u'\u20a1': 'CRC', u'\u20b1': 'PHP', u'Ft': 'HUF', u'C\u0024': 'NIO', u'Nu.': 'BTN', u'RD\u0024': 'DOP', u'\u20b9': 'INR', 'Col$': 'COP', u'\u0024U': 'UYU', u'Bds\u0024': 'BBD', u'EC\u0024': 'XCD', u'FBu': 'BIF', u'din.': 'RSD', u'Fdj': 'DJF', u'N\u0024': 'NAD', u'Fr.': 'CHF', u'Kr': 'DKK', u'Kz': 'AOA', u'\u17db': 'KHR', u'Rs.': 'PKR', u'\u20ad': 'LAK', u'KM': 'BAM', u'FJ\u0024': 'FJD', u'\u09f3': 'BDT', u'BZ\u0024': 'BZD', u'Lt': 'LTL', u'Esc': 'CVE', u'Ls': 'LVL', u'DT': 'TND', u'\u0644.\u062f': 'LYD', u'\u062f.\u062c': 'DZD', u'\u20a6': 'NGN', u'\u20aa': 'ILS', u'z\u0142': 'PLN', u'USh': 'UGX', u'\u20b2': 'PYG', u'\u0644.\u0633': 'SYP', u'NZ\u0024': 'NZD', u'L\u0024': 'LRD', u'GY\u0024': 'GYD', u'E': 'SZL', u'M': 'LSL', u'Q': 'GTQ', u'VT': 'VUV', u'NRs': 'NPR', u'\u062f.\u0625;': 'AED', u'\u0631.\u0642': 'QAR', u'WS\u0024': 'WST', u'SDR': 'XDR', u'm': 'TMT', u'kn': 'HRK', u'.\u062f.\u0628': 'BHD', u'Bs.': 'BOB', u'\u00A5' : 'CNY',  u'\u00A3' : 'GBP'}

#method for writing out available currency codes with optional symbols
    def list_codes(self):
        output = dict()
        single_codes = self.codes_set
        output['available'] = dict()
        for key, value in self.dic.items():
            if value in single_codes:
                self.codes_set.remove(value)
                output['available'][value] = key

        for single_code in single_codes:
            output['available'][single_code] = None
        return output

#object responsible for handling validity of input/output codes
class Code():
    def __init__(self, code, static_object):
        self.obj = static_object
        self.code = self.is_valid(code)

    def is_valid(self, code):
        if code is None:
            return code

        if len(code) > 4:
                return False

        elif code.upper() in self.obj.codes_set:
            code = code.upper()
            return code

        else:
            if code == 'د.إ':
                code += ';'           
            code = self.obj.dic.get(code)
            return code if code is not None else False

#makes the final compution using decimals
class Conversion():
    def __init__(self, rate_dic, amount, from_curr):
        self.amount = amount
        self.rate_dic = rate_dic
        self.from_curr = from_curr        
        self.output_dic = dict()

    def generate_output(self, decimals=2):
        self.output_dic['input'] = {'amount':self.amount , 'currency':self.from_curr}
        if self.rate_dic is None:
            self.output_dic['output'] == None
        elif 'msg' in self.rate_dic:
            self.output_dic['output'] = self.rate_dic
        else:
            self.output_dic['output'] = dict()
            accurancy = '0.{}1'.format((decimals-1)*'0')
            for key, value in self.rate_dic.items():
                if value is None:
                    continue
                conversion_result = Decimal(float(value))*Decimal(self.amount)
                self.output_dic['output'][key] = str(conversion_result.quantize(Decimal(accurancy)))
        return self.output_dic 

#core function of the program binding it all together
def get(input_currency=None, output_currency=None, amount=1.0, force_update=False):    
    var = Static()
    incurr = Code(input_currency , var).code
    outcurr = Code(output_currency , var).code
    
    #input validity checks
    if incurr is False:
        return {'msg':'Wrong input currency code: "'+input_currency+'".To get available currency codes, execute with list available flag.', 'status_code':400}
        
    else:
        if outcurr is False:
            return {"msg":"Wrong output currency code: '"+output_currency+"'.To view available codes, execute with list-available flag.", 'status_code':400}

        if incurr == outcurr:
            output = Conversion({outcurr : '1.0'},amount,incurr).generate_output()            
        else:      
            #starting instance of My_redis object, through which the data are gathered and kept
            r=My_redis(var, incurr, outcurr)
            db=r.db
            rates=r.get_rates(force_update)
            output = Conversion(rates, amount , incurr).generate_output()

        dump = dumps(output,  sort_keys=True, indent=4)
        return dump

def main():
    var=Static()    
    avail_codes=str(len(var.codes_set))
    parser = ArgumentParser()
    parser.add_argument("-i","--input_currency",help = "Base/input currency - 3 letters name or currency symbol.", type = str)
    parser.add_argument("-o","--output_currency",help = "Requested/output currency - 3 letters name or currency symbol. If missing, convert to all known currencies." ,type = str)
    parser.add_argument("-a","--amount",help = "Amount which we want to convert - float. It's set to 1.0 by default.".format(var.codes_set), type = float, default=1.0)
    parser.add_argument("-l","--list-available", help = "List  {} available currencies along with the optional symbols.".format(avail_codes), action="store_true")
    parser.add_argument("-u","--force-update", help = 'Force update of the rates even if they are "still valid" according to the update frequency.', action="store_true")
    kwargs = vars(parser.parse_args())

    if kwargs['list_available'] is True:
        return var.list_codes()

    del kwargs['list_available']
            
    output = get(**kwargs)
    if 'msg' in output:
        parser.print_help()

    return output

if __name__ == "__main__":
    print(main())
