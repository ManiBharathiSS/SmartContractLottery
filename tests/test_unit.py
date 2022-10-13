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


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip()
    account = get_account()
    lottery = deploy()
    entranceFee = lottery.getEntranceFee()
    expected_entranceFee = Web3.toWei(0.025, "ether")
    print(entranceFee)
    print(expected_entranceFee)
    assert entranceFee == expected_entranceFee


def test_enter_without_start():
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip()
    lottery = deploy()
    entranceFee = lottery.getEntranceFee()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": entranceFee})


def test_enter():
    lottery = deploy()
    account = get_account()
    entranceFee = lottery.getEntranceFee()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": entranceFee})
    lottery.enter({"from": get_account(index=1), "value": entranceFee})
    lottery.enter({"from": get_account(index=2), "value": entranceFee})


def test_endLottery():
    lottery = deploy()
    account = get_account()
    entranceFee = lottery.getEntranceFee()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": entranceFee})
    fund_link(lottery.address)
    tx = lottery.endLottery({"from": account})
    tx.wait(1)
    assert lottery.lottery_state() == 2


def test_correct_winner():
    lottery = deploy()
    account = get_account()
    entranceFee = lottery.getEntranceFee()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": entranceFee})
    lottery.enter({"from": get_account(index=1), "value": entranceFee})
    lottery.enter({"from": get_account(index=2), "value": entranceFee})
    lottery_balance = lottery.balance()
    account_Sbalance = account.balance()
    fund_link(lottery.address)
    tx = lottery.endLottery({"from": account})
    requestId = tx.events["RequestedRandomness"]["requestId"]
    vrfCoordinator = get_contract("vrf_coordinator")
    STAT_RAN = 777
    vrfCoordinator.callBackWithRandomness(requestId, STAT_RAN, lottery.address)
    winner = lottery.recentWinner()
    assert winner == account.address
    assert account.balance() == lottery_balance + account_Sbalance
