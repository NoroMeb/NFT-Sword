import json
from brownie import accounts, Sword

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

from scripts.create_metadata import get_material


def main():
    sword = Sword[-1]
    number_f_swords = sword.tokenCounter()
    print(f"You have {number_f_swords} tokenIds")

    for token_id in range(number_f_swords):
        material = get_material(token_id)
        print(material)
        with open("./metadata/sword_metadata.json", "r") as json_file:
            sword_metadate_dic = json.load(json_file)
        if not sword.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_token_uri(token_id, sword, sword_metadate_dic[material])


def set_token_uri(token_id, nft_contract, tokenURI):
    account = accounts.load("MyAccount")
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
