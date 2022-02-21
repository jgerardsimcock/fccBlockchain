from scripts.helper import get_account, SimpleCollectible

def main():

    account = get_account()
     
    collectible = SimpleCollectible.deploy({"from": account})