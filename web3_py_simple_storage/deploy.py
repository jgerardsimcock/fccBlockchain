import json

from web3 import Web3

# In the video, we forget to `install_solc`
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]


#add abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]



# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/0d0a9d2159ee43eebead8253a400ad30"))
chain_id = 3

address = os.getenv("ADDRESS")
pk = os.getenv("PRIVATE_KEY")


SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(address)
print(nonce)


###########################
##  Contract Deploy      ##
###########################
#Submit transaction that deploys the contract
transaction = SimpleStorage.constructor().buildTransaction(
        { "chainId": chain_id, "from": address, "nonce": nonce })   

    
#Sign the tx
signed_tx = w3.eth.account.sign_transaction(transaction, private_key=pk)
print("deploying contract")

#Send the tx
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print("waiting for transaction to be mined")

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed at {tx_receipt.contractAddress}")



######################################
#   Working with deployed contracts  #
######################################


## need contract ABI and address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print(f"InitialStoredValue: {simple_storage.functions.retrieve().call()}")


##Create a transaction
greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id, 
        "from": address, 
        "nonce": nonce + 1,
        "gasPrice": w3.eth.gas_price
    }
)


## Sign Transaction 
signed_greeting_transaction = w3.eth.account.sign_transaction(
    greeting_transaction, 
    private_key=pk
    )
  

#Send the transaction
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_transaction.rawTransaction)

print("Updating stored Value...")

#wait for tx to finish
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())
