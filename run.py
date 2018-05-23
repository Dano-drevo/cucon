#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
import logging
from converter import get, Static


app = Flask(__name__)

#home and only index of the app, the arguemnts are any combination of from_curr, to_curr, amount, update|latest but from_curr should be mandatory
#if there is present keyword 'available' in the string query. then the server will only respond with available currency codes it support.W
@app.route("/cucon/", methods=['GET'])
def run():
    immutable_dic = request.args    
    if 'available' in immutable_dic:
        var=Static()
        return jsonify(var.list_codes())

    else:
        kwargs = {'input_currency': immutable_dic.get('incurr', None, type=str),
                 'output_currency': immutable_dic.get('outcurr', None,),
                 'amount': immutable_dic.get('amount', 1.0, type=float),
                 'force_update': immutable_dic.get('update', False, type=bool)}
        if 'update' or 'latest' in immutable_dic:
            kwargs['force_update']=True
        output = get(**kwargs)
        if 'msg' in output:
                app.logger.debug(output)
                return jsonify(output), output['status_code']
                
        return output

if __name__ == "__main__":
    app.run(debug=True)


