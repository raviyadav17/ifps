import hashlib  
from time import time
from pprint import pprint

class blockchain():
    def __init__(self):
        self.blocks = []
        self.__secret = ''
        self.__difficulty = 4 
        i = 0
        secret_string = '/*SECRET*/'
        while True:
            _hash = hashlib.sha256(str(secret_string+str(i)).encode('utf-8')).hexdigest()
            if(_hash[:self.__difficulty] == '0'*self.__difficulty):
                self.__secret = _hash
                break
            i+=1
    def create_block(self, sender:str, receiver:str,information:str):
        block = {
            'index': len(self.blocks),
            'sender': sender,
            'receiver': receiver,
            'timestamp': time(),
            'file_unique_id': information
        }
        if(block['index'] == 0): block['previous_hash'] = self.__secret 
        else: block['previous_hash'] = self.blocks[-1]['hash']
        i = 0
        while True:
            block['nonce'] = i
            _hash = hashlib.sha256(str(block).encode('utf-8')).hexdigest()
            if(_hash[:self.__difficulty] == '0'*self.__difficulty):
                block['hash'] = _hash
                break
            i+=1
        self.blocks.append(block)
    def validate_blockchain(self):
        valid = True
        n = len(self.blocks)-1
        i = 0
        while(i<n):
            if(self.blocks[i]['hash'] != self.blocks[i+1]['previous_hash']):
                valid = False
                break
            i+=1
        if valid: print('The blockchain is valid...')
        else: print('The blockchain is not valid...')
    def show_blockchain(self):
        for block in self.blocks: 
            pprint(block)
            print()
    def mine_block(self, new_block):
        while True:
            if new_block.hash[:self.difficulty] == "0" * self.difficulty:
                self.chain.append(new_block)
                break
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()

b = blockchain()
b.create_block('Ram','shyam', 'vfvvfyqvyuVLVFEVFEYYUvmavshgdyqvqhvcyavLVUCYVYU')
b.create_block('Vishnu','shashank', 'vfvvfyqvyuVLVFEVFEYYUvmavshgdyqvqhvcyavLVUCYVYU')
b.show_blockchain()
b.validate_blockchain()