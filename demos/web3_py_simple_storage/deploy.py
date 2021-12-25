from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from web3.middleware import geth_poa_middleware

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

install_solc("0.6.0")

# Compile Our Solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
# print(compiled_sol)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# Get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get ABI
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
# print(abi)


# For connecting to our virtual blockchain in Ganache, we use HTTP directly instead of
# Metamask, which is the HTTP provider for Blockchain connectivity
# We have changed the HTTP from our local IP in Ganache to the Rinkeby end-point in Infura

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/8f96b39155ab414dad408731882ab569")
)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
chain_id = 4
my_address = "0xd28000A545e8838Bc50bCb74c22ab3C1E4beAB68"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)

# For the tx nonce, we need the lates transaction in order to assign the consecutive one
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction

# 1
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
# print(transaction)

# 2
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract deployed!!")

# Working with the contract, we need:
# Contract address
# Contract ABI

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Two ways to interact with a function/smart contracts:
# Call --> Simulate making the call and getting a return value. They don't make a state change
# Transact --> Actually making a state change

# Initial value of favorite number
print(simple_storage.functions.retrieve().call())

# This returns a blank because it does not have a return type
# We change the function in SimpleStorage so that it returns the right value
print(simple_storage.functions.store(15).call())

# Since we have CALLED the function, and not TRANSACTED, the value remains unchanged
print(simple_storage.functions.retrieve().call())


# We build a tx to actually change the state of the blockchain
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
print("Updating contract")
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Contract updated!!")

print(simple_storage.functions.retrieve().call())
