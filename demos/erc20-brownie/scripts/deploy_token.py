from brownie import OurToken, config, network
from scripts.helpful_scripts import get_account


def deploy_token():
    account = get_account()
    token_name = "FABE token"
    token_symbol = "FAB"
    initial_supply = 10 ** 26
    token = OurToken.deploy(
        initial_supply,
        token_name,
        token_symbol,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )


def main():
    deploy_token()
