"""
Author : Neha Oudin
Licence : GPLv3
Date : 01/03/2021

A simple blockchain implementation with a Flask API
"""

import datetime
import json
import hashlib
from typing import List

from flask import Flask, jsonify

def _hash_operation(new_proof, previous_proof):
    return hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

# Create a custom encoder
class BlockChainEncoder(json.JSONEncoder):
    def default(self, o):
        # Encode differently for different types
        if isinstance(o, Block):
            return o.__dict__
        return super().default(o)


class Block():
    def __init__(self, proof: int, previous_hash: str, index: int) -> "Block":
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.proof = proof
        self.previous_hash = previous_hash

    def __str__(self) -> str:
        return json.dumps(self.__dict__, sort_keys=True, indent=4)

    def __repr__(self) -> str:
        # I have just created a serialized version of the object
        return json.dumps(self.__dict__, sort_keys=True, indent=4)

    def encode(self) -> str:
        return json.dumps(self.__dict__, sort_keys=True).encode()

    @property
    def dict(self) -> dict:
        return self.__dict__


class BlockChain:
    def __init__(self) -> "BlockChain":
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof: int, previous_hash: str) -> "Block":
        block = Block(proof, previous_hash, len(self.chain)+1)
        self.chain.append(block)
        return block

    def print_previous_block(self)-> "Block":
        return self.chain[-1]

    def hash(self, block: "Block") -> str:
        return hashlib.sha256(block.encode()).hexdigest()

    def proof_of_work(self, previous_proof: int) -> int:
        new_proof = 1
        check_proof = False

        while not check_proof:
            hash_operation = _hash_operation(new_proof, previous_proof)

            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def chain_valid(self, chain: List):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block.previous_hash != self.hash(previous_block):
                return False

            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = _hash_operation(proof, previous_proof)

            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1
        return True


########################
# Blockchain Flask API #
########################

app = Flask(__name__)
app.json_encoder = BlockChainEncoder

blockchain = BlockChain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block.proof

    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)

    new_block = blockchain.create_block(proof, previous_hash)

    response = dict({'message' : 'A block is MINED'}, **new_block.dict)

    return jsonify(response), 200

@app.route("/get_chain", methods=["GET"])
def display_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/valid', methods=['GET'])
def valid():
    valid_chain = blockchain.chain_valid(blockchain.chain)

    if valid_chain:
        response = {'message' : 'The blockchain is valid'}
    else:
        response = {'message' : 'The blockchain is invalid'}
    return jsonify(response), 200

app.run(host='127.0.0.1', port=5000)
