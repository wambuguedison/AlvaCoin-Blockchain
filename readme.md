# ALVACOIN

#### Summary

A basic blockchain that is leveraged as a cryptocurrency.

It written in python and implements the high level of security using **hashlib**.  _sha256_ to be exact. 

For all this to be put together, the **flask** library comes into play to create the different API endpoints for the different functions.

#### Functions

**newblock()** Create a new Block in the BlockChain
			         :param proof: <int> The proof given by the Proof of Work Algorithm
        			 :param previousHash: (optional) <str> Hash of the previous block
        			 :return: <dict> New block

**newTransaction()** Creates a new transaction to go into the next mined block
						        :param sender: <str> Address of the sender
						        :param recipient: <str> Address of the recipient
						        :param amount: <int> Amount
						        :return: <int> The index of the Block that will hold this transaction

**hash()** Creates a SHA-256 hash of a Block
    	    :param block: <dict> Block
	        :return: <str>

**lastBlock()** Returns the last block in the chain

**proofOfWork()** Simple Proof Of Work Algorithm:
        				   -find a number 'p' such that hash(pp') contains 4 zeroes, where p is the previous p'
				           -p is the previous proof, and p' is the new proof
				          :param lastProof: <int>
        				  :return: <int>

**validProof()** Validates the proof: Does hash(last_proof, proof)contain 4 leading zeroes?
			        :param lastProof: <int> Prevoius Proof
        			:param proof: <int> current proof
			        :return: <bool> True if correct, False if incorrect

**registerNode()** Add a new node to the list of nodes
				           :param address: <str> Address of the node. Eg 'http://192.168.0.5:5000'
				           :return: None

**validChain()** Determine if a given blockchain is valid
			          :param chain: <list>A Blockchain
			          :return: <bool> True if valid, False if not

**resolveConflicts()** This is our Concensus Algorithm, it resolves conflicts
						        by replacing our chain with the longest in the network.
						        :return: <bool> True if the chain was replaced, False if not



#### API Endpoints

**mine** `GET http://localhost:<port>/mine/`

Calculate the proof of work algorithm to get the next proof.

You must receive a reward for finding the proof

_Response :_

```json
{
    "message": "New Block Forged",
    "index": "This is the index of the new block",
    "transactions": "Shows the transactions of the block",
    "proof": "Proof of work",
    "previousHash": "The hash of the previous block"
}
```
**new transaction** `POST http://localhost:<port>/transactions/new`

Create a new Transaction from posted values

posted values : _sender, recipient, amount_

_Response :_

```json
{"message" : "Transaction will be added to block {index}"}
```

**fullChain** `GET http://localhost:<port>/chain`

Get the full chain of the blockchain.

_Response :_

```json
{
	"chain": "The full blockchain",
    "length": "The length of the blockchain"
}
```

**register nodes** `POST http://localhost:<port>/nodes/register`

Register new nodes to the blockchain

posted values : _a <list>  of  nodes_

_Response :_ 

```
{
        "message": "New nodes have been added",
        "totalNodes": "A list of blockchain nodes"
}
```

**consensus** `GET http://localhost:<port>/nodes/resolve`

> If the chain is replaced; 

_Response :_

```json
{
	"message": "Our chain was replaced",
	"newChain": "The blockchain chain"
}
```

> If the chain is not replaced;

_Response :_

```
{
	"message": "Our Chain is still authoritative",
    "chain": "The blockchain chain"
}
```

