# pip install kazoo
from concurrent.futures import ThreadPoolExecutor
from kazoo.client import KazooClient
import sys

# zookeeper address
zk_addr="localhost:2181"

# True: enable all jobs, False: disable all jobs.
switch=False

# app names
apps = []

# excluded job names
excl_jobs = []

# jobs are enabled/disable asynchronously
worker_size = 100

zk = KazooClient(hosts=zk_addr)
zk.start()
pool = ThreadPoolExecutor(max_workers=worker_size)

def run(zk, node, switch):
    try:
        if not zk.exists(node): return
        if switch: zk.set(node, "".encode("utf-8"))
        else: zk.set(node, "DISABLED".encode("utf-8"))
        print(f"Processed node {node}")
    except KeyboardInterrupt:
        zk.stop()
        sys.exit()
    except Exception as e:
        print(f"Process node {node} failed, {e}")

for app in apps:
    app_path = f"/{app}"
    if not zk.exists(app_path): continue
    jobs = zk.get_children(app_path)
    if jobs:
        for job in jobs:
            jp = f"/{app}/{job}"
            if jp in excl_jobs:
                print(f"Skipped job: {jp}")
                continue

            sp = f"{jp}/servers"
            if not zk.exists(sp): continue
            servers = zk.get_children(sp)
            for s in servers:
                node = f"{sp}/{s}"
                pool.submit(run, zk, node, switch)

pool.shutdown(True)
zk.stop()
