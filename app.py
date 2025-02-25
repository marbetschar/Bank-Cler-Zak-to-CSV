import argparse
import zak
import csv
import json
from collections.abc import MutableMapping

def get_transactions(username, password, app_version):
    client = zak.ApiClient(app_version)
    client.login(username, password)
    transactions = client.transactions()
    client.logout()

    return reversed(transactions)

def write_transactions_to_csv(transactions):
    with open('Zak.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

        keys = []
        for i, tx in enumerate(transactions):
            flat_tx = __flatten(tx)

            if i == 0:
                keys = flat_tx.keys()
                csv_writer.writerow(keys)

            csv_writer.writerow([flat_tx.get(key, '') for key in keys])

# https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys?page=1&tab=scoredesc#tab-top
def __flatten(dictionary, parent_key='', separator='_'):
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(__flatten(value, new_key, separator=separator).items())
        else:
            items.append((new_key, value))
    return dict(items)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read data from Bank Clear Zak REST API')
    parser.add_argument(
        '--username',
        metavar='username',
        required=False,
        help='The username to log into Bank Cler Zak account'
    )
    parser.add_argument(
        '--password',
        metavar='password',
        required=False,
        help='The password to log into Bank Cler Zak account'
    )
    parser.add_argument(
        '--app-version',
        metavar='app_version',
        required=False,
        help='The app version to log into Bank Cler Zak account. Fetched from API if not provided.'
    )
    parser.add_argument(
        '--transactions',
        metavar='transactions',
        required=False,
        help='The path to a *.json file containing all transactions fetched from the API'
    )
    args = parser.parse_args()

    if args.transactions is not None:
        with open(args.transactions) as f:
            tx = json.load(f)["transactionsList"]
    else:
        tx = get_transactions(args.username, args.password, args.app_version)

    write_transactions_to_csv(tx)
