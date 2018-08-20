import hashlib
import json
from time import time
import urllib.parse
import requests

####### block generation & its principle

class Blockchain():
	# initialize the blockchain info
	def __init__(self):
		self.chain = []
		self.block_hash = []
		self.current_transaction = []
		self.nodes = set()
		# genesis block
		self.new_block(previous_hash=1,proof=100)

	def new_block(self,proof,previous_hash=None):
		block = {
			'index': len(self.chain)+1,
			'timestamp': time(), # timestamp from 1970
			'transactions': self.current_transaction,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1])
		}
		self.current_transaction = []

		self.chain.append(block)
		return block

	def new_transaction(self,From,To,Amount):
		self.current_transaction.append(
			{
				'From' : From,
				'To' : To,
				'Amount' : Amount
			}
		)
		return self.last_block['index'] + 1

	def register_node(self, address):
		parsed_url = urlparse(address)
		self.nodes.add(parsed_url.netloc) # netloc attribute! network lockation

	def valid_chain(self,chain):
		last_block = chain[0]
		current_index = 1

		while current_index < len(chain):
			block = chain[current_index]
			print('{}'.format(last_block))
			print('{}'.format(block))
			print("\n---------\n")
			# check that the hash of the block is correct
			if block['previous_hash'] != self.hash(last_block):
				return False
			last_block = block
			current_index += 1
		return True

	def resolve_conflicts(self):
		neighbours = self.nodes
		new_chain = None

		max_length = len(self.chain) # Our chain length
		for node in neighbours:
			tmp_url = 'http://' + str(node) + '/chain'
			response = requests.get(tmp_url)
			if response.status_code == 200:
				length = response.json()['length']
				chain = response.json()['chain']

				if length > max_length and self.valid_chain(chain):
					max_length = length

			if new_chain:
				self.chain = new_chain
				return True

			return False

	# directly access from class, share! not individual instance use it
	@staticmethod
	def hash(block):
		block_string = json.dumps(block, sort_keys=True).encode()

		return hashlib.sha256(block_string).hexdigest()



	@property
	def last_block(self):
		return self.chain[-1]

	def pow(self, last_proof, previous_hash):
		proof = 0
		while self.valid_proof(last_proof, proof, previous_hash) is False:
			proof += 1

		return proof

#정적메소드

	@staticmethod
	def valid_proof(last_proof, proof, previous_hash):
		guess = (str(last_proof + proof)+previous_hash).encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:3] == "000" # nonce
