import sys
import json
import argparse

from tabulate import tabulate

from sbc import get_sbc_types, get_sbc_item_properties, get_sbc_items
from evolutions import get_evolution_item_properties, get_evolution_items

def futcli():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "-o", "--output",
        choices=["table", "json"],
        default="table",
        help="Choose the output format (table or json)."
    )

    subparsers = parser.add_subparsers(dest='data_type', title='args', metavar="[sbc.{options}, evolutions]")
    for sbc_type in get_sbc_types():
        sbc_parser = subparsers.add_parser(f"sbc.{sbc_type}", help=f'Outputs list of SBC {sbc_type}')
    subparsers.add_parser("sbc.all", help='Outputs list of all SBC types')
    subparsers.add_parser("evolutions", help='Outputs list of all active Evolutions')

    args = parser.parse_args()

    if args.data_type:
        if args.data_type.startswith('sbc'):
            data_type, option = args.data_type.split('.')
        else:
            data_type = args.data_type

        sbc_data = get_sbc_items()
        evolutions_data = get_evolution_items()

        if data_type == 'sbc':
            combined_data = []

            if option == 'all':
                for data_list in sbc_data.values():
                    combined_data.extend(data_list)

                    if args.output == 'json':
                        print(json.dumps(combined_data, indent=4))
                    else:
                        print(tabulate(combined_data, headers='keys', tablefmt='grid'))
            else:
                if args.output == 'json':
                    print(json.dumps(sbc_data[option], indent=4))
                else:
                    print(tabulate(sbc_data[option], headers='keys', tablefmt='grid'))
        elif data_type == 'evolutions':
            if args.output == 'json':
                print(json.dumps(evolutions_data, indent=4))
            else:
                tabulated_data = []
                for item in evolutions_data:
                    tabulated_item = {}
                    for key, value in item.items():
                        if isinstance(value, dict):
                            tabulated_item[key] = json.dumps(value, indent=4)
                        else:
                            tabulated_item[key] = value
                    tabulated_data.append(tabulated_item)

                print(tabulate(tabulated_data, headers='keys', tablefmt='grid'))

if __name__ == "__main__":
    futcli()