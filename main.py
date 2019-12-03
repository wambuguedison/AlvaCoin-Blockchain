import hashlib
import json
import requests
from textwrap import dedent
from time import time
from urllib.parse import urlparse
from uuid import uuid4

from flask import Flask, jsonify, render_template, request

class Blockchain() :
    def __init__(self) :
        self.chain = []
        self.currentTransactions = []
        self.nodes = set()

        #Create Genesis Block
        self.newBlock(previousHash = 1, proof = 100)

    def newBlock(self, proof, previousHash = None) :
        """
        Create a new Block in the BlockChain
        :param proof: <int> The proof given by the Proof of Work Algorithm
        :param previousHash: (optional) <str> Hash of the previous block
        :return: <dict> New block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.currentTransactions,
            'proof': proof,
            "previousHash": previousHash or self.hash(self.chain[-1])
        }
        #reset the current list of transactions
        self.currentTransactions = []
        self.chain.append(block)
        return block

    def newTransaction(self, sender, recipient, amount) :
        """
        Creates a new transaction to go into the next mined block
        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the recipient
        :param amount: <int> Amount
        :return: <int> The index of theBlock that will hold this transaction
        """
        self.currentTransactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.lastBlock['index'] + 1
    
    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        #we must ensure that the Dictionary is ordered or we'll have inconsistent hashes
        blockString =json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(blockString).hexdigest()

    @property
    def lastBlock(self):
        return self.chain[-1]

    def proofOfWork(self, lastProof):
        """
        Simple Proof Of Work Algorithm:
        -find a number 'p' such that hash(pp') contains 4 zeroes, where p is the previous p'
        -p is the previous proof, and p' is the new proof
        :param lastProof: <int>
        :return: <int>
        """

        proof = 0
        while self.validProof(lastProof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def validProof(lastProof, proof):
        """
        Validates the proof: Does hash(last_proof, proof)contain 4 leading zeroes?
        :param lastProof: <int> Prevoius Proof
        :param proof: <int> current proof
        :return: <bool> True if correct, False if incorrect
        """

        guess = f'{lastProof}{proof}'.encode()
        guessHash = hashlib.sha256(guess).hexdigest()
        return guessHash[:4] == "0000"

    def registerNode(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of the node. Eg 'http://192.168.0.5:5000'
        :return: None
        """
        parsedUrl = urlparse(address)
        self.nodes.add(parsedUrl.netloc)

    def validChain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list>A Blockchain
        :return: <bool> True if valid, False if not
        """
        
        lastBlock = chain[0]
        currentIndex = 1

        while currentIndex < len(chain):
            block = chain[currentIndex]
            print("{}".format(lastBlock))
            print("{}".format(block))
            print("\n-------------------\n")
            #check the hash of the block is correct
            if block["previousHash"]!= self.hash(lastBlock):
                return False

            #check that the proof of work is correct
            if not self.validProof(lastBlock["proof"], block["proof"]):
                return False

            lastBlock = block
            currentIndex += 1

        return True

    def resolveConflicts(self):
        """
        This is our Concensus Algorithm, it resolves conflicts
        by replacing our chain with the longest in the network.
        :return: <bool> True if the chain was replaced, False if not
        """

        neighbours = self.nodes
        newChain = None

        #We're only looking for chains longer than ours
        maxLength = len(self.chain)

        #Grab and verify the chains from all the nodes in our network
        for node in neighbours :
            response = requests.get("http://{}/chain".format(node))

            if response.status_code == 200 :
                length = response.json()["length"]
                chain = response.json()["chain"]

                #check if the lenth uis longer and the chain is valid
                if length > maxLength and self.validChain(chain):
                    maxLength = length
                    newChain = chain

        #Replace our chaionif we discovered a new, valid chain longer than ours
        if newChain:
            self.chain = newChain
            return True

        return False


#Instantiate our node
app = Flask(__name__)

#Generate a globally unique address for this node
nodeIdentifier = str(uuid4()).replace("-", "")

#instantiate our blockchain
blockchain = Blockchain()

@app.route('/')
def index() :
    return render_template("index.html")

@app.route('/mine', methods=['GET'])
def mine() :
    #We ru the proof of work algorithm to get the next proof...
    lastBlock = blockchain.lastBlock
    lastProof = lastBlock['proof']
    proof = blockchain.proofOfWork(lastProof)

    #we must recieve a reward for finding the proof
    #the sender is "0" to signify that this node has mined a new coin
    blockchain.newTransaction(
        sender="0",
        recipient=nodeIdentifier,
        amount=1
    )

    #Forge the new block by adding it to the chain
    previousHash = blockchain.hash(lastBlock)
    block = blockchain.newBlock(proof, previousHash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previousHash': block['previousHash']
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def newTransaction() :
    values = request.get_json()

    #Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required) :
        return "Missing values", 400

    #Create a new Transaction
    index = blockchain.newTransaction(values['sender'], values['recipient'], values['amount'])
    response = {"message" : f'Transaction will be added to block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def fullChain() :
    response ={
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(debug=True)