from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib
import json
import time

app = FastAPI()

class Event(BaseModel):
    vehicle_id: str
    location: str
    speed: float
    incident: str | None = None

class Block(BaseModel):
    index: int
    timestamp: float
    events: list
    proof: int
    previous_hash: str

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_events = []
        self.create_block(proof=1, previous_hash='0')  # Genesis block

    def create_block(self, proof: int, previous_hash: str):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'events': self.pending_events,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.pending_events = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_value = hashlib.sha256(str(new_proof*2 - previous_proof*2).encode()).hexdigest()
            if hash_value[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current['previous_hash'] != self.hash(previous):
                return False
            previous_proof = previous['proof']
            current_proof = current['proof']
            hash_value = hashlib.sha256(str(current_proof*2 - previous_proof*2).encode()).hexdigest()
            if hash_value[:4] != '0000':
                return False
        return True

    def add_event(self, vehicle_id, location, speed, incident=None):
        event = {
            'vehicle_id': vehicle_id,
            'location': location,
            'speed': speed,
            'incident': incident,
            'timestamp': time.time()
        }
        self.pending_events.append(event)
        return self.get_previous_block()['index'] + 1

blockchain = Blockchain()

@app.post("/add_event")
async def add_event(event: Event):
    index = blockchain.add_event(
        event.vehicle_id, event.location, event.speed, event.incident
    )
    previous_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(previous_block['proof'])
    block = blockchain.create_block(proof, blockchain.hash(previous_block))
    return {
        "message": f"This block has been added to the chain at index {block['index']}",
        "block": block
    }, 201

@app.get("/get_chain")
async def get_chain():
    return {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }, 200

@app.get("/is_valid")
async def is_valid():
    is_valid = blockchain.is_chain_valid()
    return {"is_valid": is_valid}, 200
