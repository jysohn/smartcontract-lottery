from web3 import Web3
from brownie import Lottery, accounts, config, network

def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(config["networks"][network.show_active()]["eth_usd_price_feed"],
    {"from": account},
    )
    assert lottery.getEntranceFee() > Web3.toWei(0.018, "ether")