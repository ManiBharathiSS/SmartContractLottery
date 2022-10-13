from brownie import Lottery, network, exceptions
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_NETWORKS,
    get_account,
    get_contract,
    fund_link,
)
from scripts.deploy import deploy
import pytest
from web3 import Web3
import time


def test_all():
    if network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip()
    lottery = deploy()
    account = get_account()
    entranceFee = lottery.getEntranceFee()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": entranceFee})
    lottery.enter({"from": account, "value": entranceFee})
    lottery_balance = lottery.balance()
    account_Sbalance = account.balance()
    fund_link(lottery.address)
    lottery.endLottery({"from": account})
    time.sleep(180)
    winner = lottery.recentWinner()
    assert winner == account.address
    assert lottery.balance() == 0
