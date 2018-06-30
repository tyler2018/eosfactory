# python3 ./tests/unittest2.py

import json
import time
import setup
import teos
import cleos
import eosf
from termcolor import colored, cprint #sudo python3 -m pip install termcolor

cprint("""
Use `cleos.dont_keosd()` instruction, then the wallets used for test are not
managed by the EOSIO keosd and, hence, can be safely manipulated.

If `setup.set_verbose(True)`, print the response messages of the
issued commands.
""", 'magenta')

cleos.dont_keosd()
setup.set_verbose(True)

def test():

    cprint("""
Start a local test EOSIO node, use `teos.node_reset()`:
    """, 'magenta')

    ok = teos.node_reset()
    
    cprint("""
Create a local wallet, use `wallet = eosf.Wallet()`:
    """, 'magenta')

    wallet = eosf.Wallet()

    cprint("""
Implement the `eosio` master account as a `cleos.AccountEosio` object,
use `account_eosio = cleos.AccountEosio()` 
and `wallet.import_key(account_eosio)`:
    """, 'magenta')

    account_eosio = cleos.AccountEosio()
    wallet.import_key(account_eosio)

    cprint("""
Deploy the `eosio.bios` contract, 
use `cleos.SetContract(account_eosio, "eosio.bios")`:
    """, 'magenta')

    contract_eosio_bios = cleos.SetContract(account_eosio, "eosio.bios")


    cprint("""
Create an account to be equipped with a smart contract, namely:
"tic_tac_toe" from the EOSIO repository, 
use `account_ttt = eosf.account()`:
    """, 'magenta')

    account_ttt = eosf.account(name="tic.tac.toe")

    cprint("""
Put the account into the wallet, use `wallet.import_key(account_ttt)`:
    """, 'magenta')
    
    wallet.import_key(account_ttt)

    cprint("""
Create a smart contract object:
    """, 'magenta')

    contract_ttt = eosf.Contract(account_ttt, "tic_tac_toe")

    cprint("""
Deploy the contract:
    """, 'magenta')
    deployed = contract_ttt.deploy()
                
    cprint("""
See the response of the node, use `print(contract.contract_ttt)`:
    """, 'magenta')

    print(contract_ttt.contract)

    cprint("""
See the response of the node, use `print(contract.contract_ttt)`:
    """, 'magenta')

    cprint("""
Confirm that the account `account_test` contains the contract code:
    """, 'magenta')

    code = account_ttt.code()
    print("code hash: {}".format(code.code_hash))

    time.sleep(1)

    cprint("""
Create accounts `alice`and `bob`, 
use `alice = eosf.account()` and `wallet.import_key(alice)`:
    """, 'magenta')

    alice = eosf.account()
    wallet.import_key(alice)

    bob = eosf.account()
    wallet.import_key(bob)        

    cprint("""
Inspect the account, use `bob.account()`:
    """, 'magenta')
    
    print(bob.account())

    cprint("""
Push actions to the contract. Begin with the `create` action:
    """, 'magenta')
    action_create = contract_ttt.push_action(
        "create", 
        '{"challenger":"' 
        + str(alice) +'", "host":"' + str(bob) + '"}', bob)

    cprint("""
See the response of the node to the `create` action, 
use `print(action_create)`:
    """, 'magenta')

    print(action_create)

    cprint("""
See the result of the action:
    """, 'magenta')

    time.sleep(2)

    t = contract_ttt.get_table("games", bob)

    print(t.json)

    assert(t.json["rows"][0]["board"][0] == 0)
    assert(t.json["rows"][0]["board"][1] == 0)
    assert(t.json["rows"][0]["board"][2] == 0)
    assert(t.json["rows"][0]["board"][3] == 0)
    assert(t.json["rows"][0]["board"][4] == 0)
    assert(t.json["rows"][0]["board"][5] == 0)
    assert(t.json["rows"][0]["board"][6] == 0)
    assert(t.json["rows"][0]["board"][7] == 0)
    assert(t.json["rows"][0]["board"][8] == 0)

        
    action_move = contract_ttt.push_action(
        "move", 
        '{"challenger":"' 
        + str(alice) + '", "host":"' 
        + str(bob) + '", "by":"' 
        + str(bob) + '", "mvt":{"row":0, "column":0} }', bob)

    action_move = contract_ttt.push_action(
        "move", 
        '{"challenger":"' 
        + str(alice) + '", "host":"' 
        + str(bob) + '", "by":"' 
        + str(alice) + '", "mvt":{"row":1, "column":1} }', alice)


    t = contract_ttt.get_table("games", bob)

    assert(t.json["rows"][0]["board"][0] == 1)
    assert(t.json["rows"][0]["board"][1] == 0)
    assert(t.json["rows"][0]["board"][2] == 0)
    assert(t.json["rows"][0]["board"][3] == 0)
    assert(t.json["rows"][0]["board"][4] == 2)
    assert(t.json["rows"][0]["board"][5] == 0)
    assert(t.json["rows"][0]["board"][6] == 0)
    assert(t.json["rows"][0]["board"][7] == 0)
    assert(t.json["rows"][0]["board"][8] == 0)


    action_restart = contract_ttt.push_action(
        "restart", 
        '{"challenger":"' 
            + str(alice) + '", "host":"' 
            + str(bob) + '", "by":"' + str(bob) + '"}',
        bob)

    t = contract_ttt.get_table("games", bob)

    assert(t.json["rows"][0]["board"][0] == 0)
    assert(t.json["rows"][0]["board"][1] == 0)
    assert(t.json["rows"][0]["board"][2] == 0)
    assert(t.json["rows"][0]["board"][3] == 0)
    assert(t.json["rows"][0]["board"][4] == 0)
    assert(t.json["rows"][0]["board"][5] == 0)
    assert(t.json["rows"][0]["board"][6] == 0)
    assert(t.json["rows"][0]["board"][7] == 0)
    assert(t.json["rows"][0]["board"][8] == 0)


    action_close = contract_ttt.push_action(
        "close", 
        '{"challenger":"' 
        + str(alice) + '", "host":"' + str(bob) + '"}', bob)


if __name__ == "__main__":
   test()