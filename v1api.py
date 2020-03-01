from flask import Flask
from flask import request
from flask import make_response
from datetime import date
import json
import requests
from web3 import Web3

# Blockchain connction
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
address='0x76C65cb7a1a3a870a528546C8273bb520507d88E'
abi=json.loads('[{"constant":false,"inputs":[{"name":"med_id","type":"string"},{"name":"m_name","type":"string"},{"name":"m_address","type":"string"},{"name":"weight","type":"string"},{"name":"m_date","type":"string"},{"name":"e_date","type":"string"}],"name":"manfucture_entry","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"med_id","type":"string"}],"name":"manf_data","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"med_id","type":"string"},{"name":"d_name","type":"string"},{"name":"d_address","type":"string"},{"name":"recived_time","type":"string"},{"name":"transport_by","type":"string"}],"name":"distributor_entry","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"med_id","type":"string"}],"name":"dis_data","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')

# contract connection eshtablishment
contract=web3.eth.contract(address=address,abi=abi)
web3.eth.defaultAccount=web3.eth.accounts[0]

app = Flask(__name__)

#handling the webhook request
@app.route('/manifacture', methods=["GET","POST"])
def manifacture():
    if(request.method=='POST'):
        try:
            req=request.json
            medic_id=req['med_id']
            m_name=req['name']
            m_address=req['address']
            weight=req['weight']
            manifacture_date=req['manifacture_date']
            expiry_date=req['expiry_date']
            contract.functions.manfucture_entry(medic_id,m_name,m_address,weight,manifacture_date,expiry_date).transact()
            res={'message':'data inserted'}
        except:
            res={'message':'error-occured'}
    return res

@app.route('/distributor', methods=["GET","POST"])
def distributor():
    if(request.method=='POST'):
        try:
            req=request.json
            medic_id=req['med_id']
            d_name=req['name']
            d_address=req['address']
            recived_time=req['recived_time']
            transport_by=req['transport_by']
            contract.functions.distributor_entry(medic_id,d_name,d_address,recived_time,transport_by).transact()
            res={'message':'data inserted'}
        except:
            res={'message':'error-occured'}
    return res


@app.route('/callMedicId', methods=["GET","POST"])
def callMedicId():
    if(request.method=='POST'):
        try:
            req=request.json
            medic_id=req['med_id']
            manifacture_data=contract.functions.manf_data(medic_id).call()
            distributor_data=contract.functions.dis_data(medic_id).call()
            res={'message':'data inserted'}
            m={
                'name':manifacture_data[0],
                'address':manifacture_data[1],
                'weight':manifacture_data[2],
                'manifacture date':manifacture_data[3],
                'expiry date':manifacture_data[4]
            }
            d={
                'name':distributor_data[0],
                'address':distributor_data[1],
                'recived time':distributor_data[2],
                'transport by':distributor_data[3]
            }
            data=[]
            data.append(m)
            data.append(d)
            res={'message':'data found','data':data}
        except:
            res={'message':'data not found'}
    return res



if __name__ == '__main__':
    app.run()