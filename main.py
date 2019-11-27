class Blockchain() :
    def __init__(self) :
        self.chain = []
        self.currentTransactions = []

    def newBlock(self) :
        #Create a new block and adds it to the chain
        pass

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
        #Hashes a block
        pass

    @property
    def lastBlock(self):
        #Returns the last blockin the chain
        pass