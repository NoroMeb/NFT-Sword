from brownie import accounts, Sword


def main():
    deploy()


def deploy():
    account = accounts.load("MyAccount")
    sword = Sword.deploy({"from": account})
    return sword
