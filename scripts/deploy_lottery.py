from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config
import time

def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyHash"],
        {"from": account},
        publish_source = config["networks"][network.show_active()].get("verify", False)
    )
    print("Deployed lottery!\n")
    return lottery

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery has started!\n")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from":account, "value": value})
    tx.wait(1)
    print("You entered the lottery!\n")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # need to fund the contract with LINK since we call chainlink
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_tx = lottery.endLottery({"from": account})
    ending_tx.wait(1)
    time.sleep(100)
    print(f"{lottery.recentWinner()} is the new winner!\n")

def check_lottery():
    account = get_account()
    lottery = Lottery[-1]
    lottery.checkLotteryState()
    # It costs gas to emit!
    lottery_state = lottery.lottery_state({"from": account})
    print(f"Current state of the lottery is: {lottery_state}\n")

def main():
    active_network = network.show_active()
    print(f"Current active network: {active_network}\n")

    active_account = get_account()
    print(f"Current active account: {active_account}\n")

    deploy_lottery()
    check_lottery()
    start_lottery()
    check_lottery()
    enter_lottery()
    check_lottery()
    end_lottery()
    check_lottery()