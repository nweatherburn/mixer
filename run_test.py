from mixer import *

def main():
    toSend = [
        {
            "address":"Nick_1"
        },
        {
            "address":"Nick_2"
        }
    ]
    r = requests.post('http://localhost:8080/mixer/address', json=toSend)
    deposit_address_one = r.json()['deposit_address']

    toSend = [
        {
            "address":"James"
        }
    ]
    r = requests.post('http://localhost:8080/mixer/address', json=toSend)
    deposit_address_two = r.json()['deposit_address']

    transfer_from_mixer_account(deposit_address_one, '25')
    transfer_from_mixer_account(deposit_address_two, '25')


if __name__ == '__main__':
    main()