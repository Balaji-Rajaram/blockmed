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
address='0x29B7F7dDbbA6B09dF3A026226cFd068A4537aabF'
abi=json.loads('[{"constant":true,"inputs":[{"name":"med_id","type":"string"}],"name":"med_votes","outputs":[{"name":"","type":"uint256"},{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"med_id","type":"string"}],"name":"manf_data","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"med_id","type":"string"}],"name":"like_med","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"med_id","type":"string"},{"name":"licence_num","type":"string"},{"name":"d_name","type":"string"},{"name":"d_address","type":"string"},{"name":"recived_time","type":"string"},{"name":"transport_by","type":"string"}],"name":"distributor_entry","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"med_id","type":"string"},{"name":"medicin_name","type":"string"},{"name":"licence_num","type":"string"},{"name":"m_name","type":"string"},{"name":"m_address","type":"string"},{"name":"m_date","type":"string"},{"name":"e_date","type":"string"}],"name":"manfucture_entry","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"med_id","type":"string"}],"name":"local_dis_data","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"med_id","type":"string"}],"name":"dislike_med","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"med_id","type":"string"},{"name":"licence_num","type":"string"},{"name":"l_name","type":"string"},{"name":"l_address","type":"string"},{"name":"recived_time","type":"string"},{"name":"transport_by","type":"string"}],"name":"local_distributor_entry","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"med_id","type":"string"}],"name":"dis_data","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')

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
            user_address=req['address']
            medic_id=req['med_id']
            medicin_name=req['medicin_name']
            licence_num=req['licence_num']
            m_name=req['name']
            m_address=req['m_address']
            manifacture_date=req['manifacture_date']
            expiry_date=req['expiry_date']
            web3.eth.defaultAccount=user_address
            contract.functions.manfucture_entry(medic_id,medicin_name,licence_num,m_name,m_address,manifacture_date,expiry_date).transact()
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
            user_address=req['address']
            licence_num=req['licence_num']
            d_name=req['name']
            d_address=req['d_address']
            recived_time=req['recived_time']
            transport_by=req['transport_by']
            web3.eth.defaultAccount=user_address
            contract.functions.distributor_entry(medic_id,licence_num,d_name,d_address,recived_time,transport_by).transact()
            res={'message':'data inserted'}
        except:
            res={'message':'error-occured'}
    return res

@app.route('/localDistributor', methods=["GET","POST"])
def localDistributor():
    if(request.method=='POST'):
        try:
            req=request.json
            medic_id=req['med_id']
            user_address=req['address']
            licence_num=req['licence_num']
            l_name=req['name']
            l_address=req['l_address']
            recived_time=req['recived_time']
            transport_by=req['transport_by']
            web3.eth.defaultAccount=user_address
            contract.functions.distributor_entry(medic_id,licence_num,l_name,l_address,recived_time,transport_by).transact()
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
            data=[]
            manifacture_data=contract.functions.manf_data(medic_id).call()
            if(len(manifacture_data[0])):
                distributor_data=contract.functions.dis_data(medic_id).call()
                local_distributor_data=contract.functions.local_dis_data(medic_id).call()
                vote=contract.functions.med_votes(medic_id).call()
                m={
                    'medicin':manifacture_data[0],
                    'name':manifacture_data[1],
                    'address':manifacture_data[2],
                    'manifacture date':manifacture_data[3],
                    'expiry date':manifacture_data[4],
                    'Type':manifacture_data[5]
                }
                data.append(m)
                if(len(distributor_data[0])):
                    d={
                        'name':distributor_data[0],
                        'address':distributor_data[1],
                        'recived time':distributor_data[2],
                        'transport by':distributor_data[3],
                        'Type':distributor_data[4]
                    }
                    data.append(d)
                
                if(len(local_distributor_data[0])):
                    l={
                        'name':local_distributor_data[0],
                        'address':local_distributor_data[1],
                        'recived time':local_distributor_data[2],
                        'transport by':local_distributor_data[3],
                        'Type':local_distributor_data[4]
                    }
                    data.append(l)
                v={
                    'like':vote[0],
                    'dislike':vote[1]
                }
                
                
                data.append(v)
                res={'message':'data found','data':data}
            else:
                res={'message':'data not found'}
        except:
            res={'message':'data not found'}
    return res

@app.route('/like', methods=["GET","POST"])
def like():
    if(request.method=='POST'):
        try:
            req=request.json
            medic_id=req['med_id']
            web3.eth.defaultAccount=web3.eth.accounts[0]
            contract.functions.like_med(medic_id).transact()
            res={'message':'liked successfully'}
        except:
            res={'message':'error-occured'}
    return res

@app.route('/disLike', methods=["GET","POST"])
def disLike():
    if(request.method=='POST'):
        try:
            req=request.json
            medic_id=req['med_id']
            web3.eth.defaultAccount=web3.eth.accounts[0]
            contract.functions.dislike_med(medic_id).transact()
            res={'message':'disliked successfully'}
        except:
            res={'message':'error-occured'}
    return res



if __name__ == '__main__':
    app.run()