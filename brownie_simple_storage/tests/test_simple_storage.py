from tracemalloc import start
from unittest import expectedFailure
from brownie import SimpleStorage, accounts


def test_deploy():
    #Arrange: Set up context
    account = accounts[0]
    #Act: Do something
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    #Assert: make sure it is what you expect
    assert starting_value == expected


def test_update():
    #Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    #Act
    expected = 15
    simple_storage.store(expected, {"from": account})

    #Assert
    assert expected == simple_storage.retrieve()