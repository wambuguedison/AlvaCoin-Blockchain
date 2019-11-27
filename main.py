import hashlib
import json

from time import time
from uuid import uuid4

class Blockchain() :
    def __init__(self) :
        self.chain = []
        self.currentTransactions = []

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
            'index': len(self.chain) + 1
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
        return guessHash[:4] ==== "0000"