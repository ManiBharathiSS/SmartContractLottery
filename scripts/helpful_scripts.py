from brownie import (
    network,
    accounts,
    config,
    MockV3Aggregator,
    LinkToken,
    VRFCoordinatorMock,
    Contract,
)
from web3 import Web3


LOCAL_BLOCKCHAIN_NETWORKS = ["development"]
FORKED_NETWORKS = ["mainnet-fork"]


def get_account(index=None):
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS
        or network.show_active() in FORKED_NETWORKS
    ):
        if index:
            return accounts[index]
        else:
            return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


contractToMock = {
    "eth_usd_priceFeed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    contract_type = contractToMock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        cotract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, cotract_address, contract_type.abi
        )
    return contract


DECIMALS = 8
STARTING_VALUE = 2000 * 10**8


def deploy_mocks():
    account = get_account()
    MockV3Aggregator.deploy(DECIMALS, STARTING_VALUE, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})


def fund_link(contract_address, amount=Web3.toWei(0.1, "ether")):  # 0.1 LINK
    account = get_account()
    link_token = get_contract("link_token")
    link_token.transfer(contract_address, amount, {"from": account})
