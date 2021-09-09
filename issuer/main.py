from os import write
import time

from src.write_did import demo
from src.utils import run_coroutine


async def main():
    await demo()
    # await anoncreds.demo()
    # await crypto.demo()
    # await ledger.demo()
    # await txn_author_agreement.demo()
    # await endorser.demo()

if __name__ == '__main__':
    run_coroutine(main)
    time.sleep(1)  # FIXME waiting for libindy thread complete
