from brownie import SimpleStorage, accounts, config


def read_contract():
    # By calling SimpleStorage as an array, we access the existing deployments (in the deployments folder)
    # With SimpleStorage[-1] we access the latest one, and SimpleStorage[0] the first one
    simple_storage = SimpleStorage[-1]

    # If we have run previously the deploy script updating the value to 15, we should see 15
    print(simple_storage.retrieve())


def main():
    read_contract()
