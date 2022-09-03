from brownie import accounts, Sword


def main():
    create_sword()


def create_sword():
    account = accounts.load("MyAccount")
    sword = Sword[-1]
    tx = sword.createCollectible({"from": account})
    tx.wait(1)
    print("your nft has been created!")
