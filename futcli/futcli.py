
import sys
import json

from sbc import get_sbc_options
from sbc import get_sbc_items
from sbc import get_sbc
from evolutions import get_evolution_items
from evolutions import get_evolutions


if __name__ == "__main__":
    if len(sys.argv) != 3:
        if len(sys.argv) == 2 and sys.argv[1].lower() == 'sbc':
            sbc_options = get_sbc_options()
            print(json.dumps(sbc_options, indent=4))

    category = sys.argv[1].lower()

    if category == 'sbc':
        option = sys.argv[2].lower()
        sbc_data = get_sbc(option)
        if sbc_data:
            print(json.dumps(sbc_data, indent=4))
        else:
            print("No SBC data available.")
    elif category == 'evolutions':
        evolutions_data = get_evolutions()
        if evolutions_data:
            print(json.dumps(evolutions_data, indent=4))
        else:
            print("No SBC data available.")
