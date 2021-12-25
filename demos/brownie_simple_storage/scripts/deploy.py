from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    # Ways to create an account:
    # 1. Local Ganache blockchain deployed automatically by Brownie - Select any of the accounts
    # account = accounts[0]

    # 2. In the CLI
    # brownie accounts new carlitros - Promts to introduce private key (with 0x at the beginning)
    # brownie accounts list -- muestra las accounts
    # brownie accounts delete carlitros
    # account = accounts.load("carlitros")
    # This is a very secure way, always recommended

    # 3. Environment variables
    # Less secure, (2) is recommended
    # We create .env and export PRIVATE_KEY=0x..... and create brownie-config.yaml
    # account = accounts.add(config["wallets"]["from_key"])

    # We implement a function that selects the option automatically
    account = get_account()

    print(account)

    # We deploy the contract
    # Brownie knows it's a Transact (not Call) because we want to deploy a SC
    simple_storage = SimpleStorage.deploy({"from": account})

    print(simple_storage)

    # Recreate all the flow we did with web3.py
    stored_value = simple_storage.retrieve()
    print(stored_value)

    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
