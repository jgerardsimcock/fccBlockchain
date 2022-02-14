from brownie import (
        accounts,
        network,
        config,
        Contract, 
        VRFCoordinatorMock, 
        MockV3Aggregator,
        LinkToken
        )   


FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"]) 


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock, 
    "link_token": LinkToken

}

def get_contract(contract_name):
    """"
    This function grabs contract address from brownie-config, if defined,
    otherwise deploy mock version of that contract and return that mock contract


    Args:
        contract_name (string)
    
    Returns:
        brownie.network.contract.ProjectContract: 
    
    """

    contract_type = contract_to_mock[contract_name]

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:

            deploy_mocks()
        
        contract = contract_type[-1]

    else: 
        contract_address = config["networks"][network.show_active()][contract_name]
 
        contract = Contract.from_abi(
                contract_type._name, contract_address, contract_type.abi
        )
          
    return contract
DECIMALS = 8
STARTING_PRICE = 5000000000000

def deploy_mocks(decimals=DECIMALS, starting_price=STARTING_PRICE):
    account = get_account()
    MockV3Aggregator.deploy(
                    decimals, 
                    starting_price,
                    {"from":account}
                    )
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed")