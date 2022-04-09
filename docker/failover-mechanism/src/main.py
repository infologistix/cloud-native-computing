from random import randint
import time
from datetime import datetime


if __name__=="__main__":
    for i in range(randint(5,10), 0, -1):
        time.sleep(1)
        print(f"Preparing Failover {i}: {datetime.now().isoformat()}")
    raise Exception("Manual simulated Failover")