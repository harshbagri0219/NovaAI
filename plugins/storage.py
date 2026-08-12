from system.device import get_storage

def run():

    storage = get_storage()

    return (
        f"Total Storage : {storage['total']} GB\n"
        f"Used Storage : {storage['used']} GB\n"
        f"Free Storage : {storage['free']} GB\n"
        f"Usage : {storage['percent']}%"
    )