class Blockchain() :
    def __init__(self) :
        self.chain = []
        self.currentTransactions = []

    def newBlock(self) :
        #Create a new block and adds it to the chain
        pass

    def newTransaction(self) :
        #Adds new transaction to the list of transactions
        pass
    
    @staticmethod
    def hash(block):
        #Hashes a block
        pass

    @property
    def lasBlock(self):
        #Returns the last blockin the chain
        pass