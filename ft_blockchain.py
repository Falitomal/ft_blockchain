
import hashlib
import json
import datetime, time
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.create_block(proof = 1, previous_hash = '0')

    def create_block(self, proof, previous_hash):
        """ Crea un bloque en la cadena, con el proof y el hash anterior """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.get_previous_block())
        }
        self.chain.append(block)
        self.transactions = []
        return block
    

    def create_node(self, address):
        """ Para agregar el nodo a la red de blockchain """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        """ Comprueba las cadenas, si es más corta y la reemplaza por la más larga """
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            print(f"Checking node {node}...")
            try:
                response = requests.get(f'http://{node}/get_all')
                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']
                    if length > max_length and self.validate_chain(chain):
                        print(f"Found a longer valid chain on node {node}")
                        max_length = length
                        longest_chain = chain
                    else:
                        print(f"Chain on node {node} is not longer and valid")
                else:
                    print(f"Error status code {response.status_code} from node {node}")
            except Exception as e:
                print(f"Error checking node {node}: {e}")
        if longest_chain:
            print("Replacing local chain with longest valid chain from network")
            self.chain = longest_chain
            return True
        print("No valid longer chain found in network")
        return False

    def create_transaction(self, sender, receiver, amount):
        """ Crea una transacción """
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def get_previous_block(self):
        """ Devuelve el bloque anterior """
        return self.chain[-1]
        
    def hash(self, block):
        """ Devuelve el hash de un bloque """
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def proof_of_work(self, previous_proof):
        """ Prueba de trabajo """
        start_time = time.time()
        new_proof = 1
        check_proof = False
        hash_count = 0
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            hash_count += 1
            if hash_operation[-4:] == '4242':
                check_proof = True
                print(f"Hash is: {hash_operation}")
            else:
                new_proof += 1
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")
        print(f"Number of hashes calculated: {hash_count}")  
        return new_proof

    def validate_chain(self, chain):
        """ Comprueba si la cadena es válida """
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[-4:] != '4242':
                return False
            previous_block = block
            block_index += 1
            
        return True

# Crear una Web App
app = Flask(__name__)
blockchain = Blockchain()
node_address = str(uuid4()).replace('-', '')

@app.route('/mine', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.create_transaction(sender=node_address, receiver='jled', amount=42)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Congratuleixon you mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions']
    }
    return jsonify(response), 200


@app.route('/get_all', methods=['GET'])
def get_all():
    """ Obtener la cadena completa """
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid_chain', methods=['GET'])
def is_valid():
    """ Comprobar si la cadena es válida """
    is_valid_chain = blockchain.validate_chain(blockchain.chain)
    if is_valid_chain:
        response = {'message': 'All good!!! Blockchain is valid. UpToYou'}
    else:
        response = {'message': 'WRONG! Blockchain is not valid.'}
    return jsonify(response), 200


@app.route('/transactions/new', methods = ['POST'])
def add_transaction():
    """ Agregando nuevas transacciones, para una peticion post de la API"""
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transaction_keys):
        return 'Not all elements of the transaction are missing', 400
    index = blockchain.create_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    """ Reemplazar la cadena por la mas valida, si hay una cadena mas larga que la nuestra la reemplazamos """
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good!!! The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200


@app.route('/connect_node', methods=['POST'])
def connect_node():
    """ Conectar nuevos nodos, registramos nuevos modos en la red """
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No node', 401
    for node in nodes:
        blockchain.create_node(node)
    response = {
        'message': 'All the nodes are connected. The Blockchain now contains the following nodes:',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201

# Ejecutar la app server
app.run(host = "0.0.0.0", port= '5001')
