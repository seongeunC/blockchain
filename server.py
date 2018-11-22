from flask import Flask,request,jsonify
#import json
from time import time
#from textwrap import dedent
from flask import render_template
from flask import redirect,url_for
from blockchain import Blockchain


app = Flask(__name__)

blockchain = Blockchain()
@app.route('/')
def index():
    hash = blockchain.block_hash
    response = blockchain.chain


    return render_template('index.html',chain=response,hash=hash)

@app.route('/mine')
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    ##mine 시 previous_hash를 추가
    previous_hash = blockchain.hash(last_block)
    proof = blockchain.pow(last_proof, previous_hash)

    blockchain.new_transaction(
    From = '0',
    To = node_identifier,
    Amount = 1
    )
    #previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)


    response = {
    'message' : 'new block found',
    'index' : block['index'],
    'transactions' : block['transactions'],
    'proof' : block['proof'],
    'previous_hash' : block['previous_hash'],
    'hash' : blockchain.hash(block)
    }

    blockchain.block_hash.append(blockchain.hash(block))

    return render_template('mine.html',response=response)

@app.route('/transactions/new')
def new_transaction():
    return render_template('transactions_new.html')

@app.route('/transactions/pending', methods = ['POST','GET'])
def pending():
    if request.method == 'POST':
        From = request.form['From']
        To = request.form['To']
        Amount = request.form['Amount']
        blockchain.new_transaction(From,To,Amount)

        pd_tx = request.form
        return render_template("pending.html",transaction=pd_tx)

if __name__ == '__main__':
	app.run('localhost', 5000,debug=True)
