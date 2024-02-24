
import sys
import json

from sbc import get_sbc_catalog
from sbc import get_sbc_items
from sbc import get_sbc_data
from evolutions import get_evolution_items
from evolutions import get_evolutions


if __name__ == "__main__":
    category = sys.argv[1].lower()

    if category == 'sbc':
        sbc_data = get_sbc_data()
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
