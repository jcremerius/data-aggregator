import json
import web3
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
import requests


def connect_to_blockchain():
    connected = False
    while not connected:
        try:
            time.sleep(10)
            web3 = Web3(HTTPProvider('http://localhost:8545'))
            return web3
        except Exception:
            pass
        connected = True


def start_mining(web3):
    web3.miner.start(1)


# Gets the last mined blocks since last send cycle
def retrieve_last_blocks(number_of_last_sent_block, web3):
    last_blocks = []
    number_of_last_block = web3.eth.getBlock('latest').number
    if number_of_last_block > number_of_last_sent_block:
        number_of_blocks_to_send = number_of_last_block - number_of_last_sent_block
        for i in range(0, number_of_blocks_to_send):
            last_blocks.append(web3.eth.getBlock(number_of_last_block - i))
        return(number_of_last_block, last_blocks)
    else:
        print("Nothing to send")
        return(number_of_last_sent_block, last_blocks)


# get the avg block difficulty of the current send cycle
def calculate_avg_block_difficulty(blocks_to_send):
    avg_block_difficulty = 0
    if not blocks_to_send:  # checks if list is empty
        return None
    else:
        for block in blocks_to_send:
            print("Single Difficulty:")
            print(block.totalDifficulty)
            avg_block_difficulty += block.totalDifficulty
        avg_block_difficulty = avg_block_difficulty / len(blocks_to_send)
        return avg_block_difficulty


def provide_data(web3):  # Loop, which runs on the nodes to get and send the data
    number_of_last_sent_block = 0
    while True:
        time.sleep(10)
        retrieved_blocks = retrieve_last_blocks(number_of_last_sent_block, web3)
        number_of_last_sent_block = retrieved_blocks[0]
        blocks_to_send = retrieved_blocks[1]
        avg_block_difficulty = calculate_avg_block_difficulty(blocks_to_send)
        node_id = web3.admin.nodeInfo.id
        hash_rate = web3.eth.hashrate
        gas_price = web3.eth.gasPrice
        node_data = {'node_id': node_id, 'hashrate': hash_rate, 'gas_price': gas_price, 'Avg Block difficulty': avg_block_difficulty}
        print(node_data)
        send_data(node_data)


def send_data(node_data):  # send the data to the server
    try:
        SERVER_ADRESS = 'http://localhost:3030'
        requests.post(SERVER_ADRESS, data=node_data)
        print("Request has been sent")
    except Exception:
        print("Connection has not been established")
        pass




    start_mining(web3)
    provide_data(web3)
