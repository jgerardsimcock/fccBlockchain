from brownie import StokedToken, accounts, network, config
from scripts.helper import get_account, get_contract, fund_with_link
from web3 import Web3


initial_supply = Web3.toWei(1000, "ether")




def main():
    account = get_account()
    my_token = StokedToken.deploy(initial_supply, {"from": account})
    print(my_token.name())