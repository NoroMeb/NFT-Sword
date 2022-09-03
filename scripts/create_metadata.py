import json
from turtle import update
from brownie import Sword, network
from metadata.sample_metadata import metadata_template
from pathlib import Path
import os
import requests

MATERIAL_MAPPING = {0: "SILVER", 1: "GOLD", 2: "PLATINIUM"}

sword_metadate_dic = {}


def main():
    sword = Sword[-1]
    number_of_swords = sword.tokenCounter()
    print(f"NUMBER OF SWORDS : {number_of_swords}")
    for token_id in range(number_of_swords):
        material = get_material(token_id)
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{material}.json"
        )
        sword_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            sword_metadata["name"] = material
            sword_metadata["description"] = f"An adorable {material} sword!"
            image_path = "./img/" + material.lower() + ".png"
            image_uri = upload_to_ipfs(image_path)
            sword_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(sword_metadata, file)
            token_uri = upload_to_ipfs(metadata_file_name)
            sword_metadate_dic[material] = token_uri

    with open("./metadata/sword_metadata.json") as fp:
        data = json.load(fp)
    data.update(sword_metadate_dic)
    with open("./metadata/sword_metadata.json", "w") as fp:
        json.dump(data, fp)


def get_material(material_number):
    return MATERIAL_MAPPING[material_number]


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
