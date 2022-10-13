from brownie import Lottery, config, network
from scripts.helpful_scripts import get_account, get_contract, fund_link
import time


def deploy():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_priceFeed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = lottery.startLottery({"from": account})
    tx.wait(1)


def enterLottery():
    account = get_account()
    lottery = Lottery[-1]
    entranceFee = lottery.getEntranceFee()
    tx = lottery.enter({"from": account, "value": entranceFee})
    tx.wait(1)


def end_Lottery():
    account = get_account()
    lottery = Lottery[-1]
    fund_link(lottery.address)
    lottery.endLottery({"from": account})
    time.sleep(240)
    print(f"lottery winner:{lottery.recentWinner()}")


def main():
    deploy()
    start_lottery()
    enterLottery()
    end_Lottery()
