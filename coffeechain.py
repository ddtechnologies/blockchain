import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import jsonify, request

from hashlib import sha256
import json
import time
import socket



class Transaction:

    def __init__(self, index, current_hash, previous_hash, timestamp, sender, recipient, action, coffee_type, amount,message):
        
        self.index = index
        self.current_hash = current_hash
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.sender = sender
        self.recipient = recipient
        self.action= action
        self.coffee_type=coffee_type
        self.amount=amount
        self.message=message

    def compute_change(self):

        index=self.index+1
        previous_hash = self.current_hash    
        coffee_type=self.coffee_type[0]
        timestamp=time.time()
        old_sender=self.sender
        old_recipient=self.recipient

        if self.coffee_type == ["americano"]:
            amount=self.amount-2.50
        if self.coffee_type == ["espresso"]:
            amount=self.amount-1.50
        if self.coffee_type == ["cappucino"]:  
            amount=self.amount-3.50

        message="your change is " + str(amount)
        change=Transaction(index, [], previous_hash, timestamp, old_recipient, old_sender, ["return"], coffee_type, amount,message)
        
        return change   

    def compute_hash(self):

        transaction_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(transaction_string.encode()).hexdigest()


class Blockchain:

    def __init__(self):
        self.unconfirmed_transactions = [] # data yet to get into blockchain
        self.chain = []
        self.create_genesis_transaction()


    def create_genesis_transaction(self):

        genesis_transaction = Transaction(0,[], [], time.time(),[],[],[],[],0,[])
        genesis_transaction.current_hash = genesis_transaction.compute_hash()
        self.chain.append(genesis_transaction)

    @property
    def last_transaction(self):

        return self.chain[-1]

    def proof_of_work(self, transaction):

        transaction.nonce = 0

        computed_hash = transaction.compute_hash()
        while not computed_hash.startswith('0' * 3):
            transaction.nonce += 1
            computed_hash = transaction.compute_hash()

        return computed_hash


    def add_transaction(self, transaction, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of a latest block
          in the chain match.
        """
        previous_hash = self.last_transaction.current_hash

        if previous_hash != transaction.previous_hash:
            return False

        if not Blockchain.is_valid_proof(transaction, proof):
            return False

        transaction.current_hash = proof
        self.chain.append(transaction)
        return True

    def is_valid_proof(self, transaction, hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (transaction_hash.startswith('0' * 3) and
                current_hash == transaction.compute_hash())


    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)


    def mine(self):

        if not self.unconfirmed_transactions:
            return False

        last_transaction = self.last_transaction

        mining_transaction = Transaction(last_transaction.index + 1,
                                      [],
                                      last_transaction.current_hash,
                                      time.time(),
                                      [""],
                                      socket.gethostbyname(socket.gethostname()),
                                      ["mine"],
                                      last_transaction.coffee_type,
                                      1,
                                      [""])
                          

        proof = self.proof_of_work(mining_transaction)

#        add the new transactions to the ledger one by one
        for item in unconfirmed_transactions:
            self.add_transaction(item)


#       add the transaction compensating the miner, this shouldn't happen for all the miners but this is a simple example
        self.add_transaction(mining_transaction, proof)

#       empty the list of pending transaction
        self.unconfirmed_transactions = []

#       send the non mining nodes with the new version of the chain
        requests.post("http://172.20.0.3", self.chain)
        requests.post("http://172.20.0.2", self.chain)

    def sync_new_chain(self):

        incoming_chain=request.get_json()
        for item in incoming_chain:
            self.chain.append(item)
        



    def valid_chain(self, chain):

        last_transaction = chain[0]
        current_index = 1

        while current_index < len(chain):
            transaction = chain[current_index]
            print(f'{last_transaction}')
            print(f'{transaction}')
            print("\n-----------\n")
            # check transaction hash correct
            if transaction['previous_hash'] != self.hash(last_transaction):
                return False

            # check pow correct
            if not self.valid_proof(last_transaction['proof'], transaction['proof']):
                return False

            last_transaction = transaction
            current_index += 1

        return True



if __name__ == '__main__':

    for time_index in range(1,200):

        from argparse import ArgumentParser

        parser = ArgumentParser()
        parser.add_argument('-p', '--port', default=5000, type=int)
        args = parser.parse_args()
        port = args.port



    #    initialize blockchain with genesis transaction and create Alice's order
        coffeechain = Blockchain()
        genesis_transaction=coffeechain.chain[0]
        genesis_hash=genesis_transaction.current_hash
        alice_order=Transaction(1,[], [genesis_hash], time.time(),["172.20.0.2"],["172.20.0.3"],["buy"],["Americano"],5,[""])
        

        
        ip_address=socket.gethostbyname(socket.gethostname())
        print(ip_address)

    # send Alice's order to Bob's coffee shop (docker container at IP 172.20.0.3)
        if ip_address in ["172.20.0.2"]:
                    
            requests.post("http://172.20.0.3", alice_order)
            

    #Bob's coffee shop receives Alice's order, sends transaction to miners 172.20.0.4 and 172.20.0.5      
        if ip_address in ["172.20.0.3"]:

            incoming_order=request.get_json()
            print(incoming_order)

            alice_order=Transaction(incoming_order)
            compute_change=alice_order.compute_change()

            coffeechain.chain.append(incoming_order)
            coffeechain.chain.append(compute_change)

            requests.post("http://172.20.0.4", coffeechain.chain)
            requests.post("http://172.20.0.5", coffeechain.chain)

        # miners receive Alice's order and Bob's change 

        if ip_address in ["172.20.0.4","172.20.0.5"]:
            incoming_chain=request.get_json()

            for item in incoming_chain:

                coffeechain.add_new_transaction(item)
            
        # miners launch consensus mechanism, checking with entire network whether the chain to be mined is the longest
            new_chain = None
            max_length = len(сoffeechain.chain) 

            for container_ip in ["172.20.0.2","172.20.0.3","172.20.0.4","172.20.0.5"]:
                response = requests.get(CONTAINER_IP_LIST,chain)

                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']
                   
                    if length > max_length and self.valid_chain(chain):
                        max_length = length
                        new_chain = chain

            # Replace the chain if there is a valid chain longer than the current
            if new_chain:
                coffeechain.unconfirmed_transactions = new_chain

            #now mine the new chain
            coffeechain.mine()


        #now sync the non mining nodes

        if ip_address in ["172.20.0.2","172.20.0.3"]:
            coffeechain.sync_new_chain()

        time.sleep(3)
        

   

        
    

            
        

        

        
            

        
        

            
            


        

        

        

            

        

        
        


        
        

        


        

        

        

     

       
        


        

    
    
    
    
    
        

    

    

    
    


        
        

    
  
    
