import requests
import time
import random
from multiprocessing import Process, Value
import subprocess
import logging
import traceback
from visualize import TestVisualizer

DATA_FILE = "data.txt"
BACKEND_URL = "http://localhost:8080"

traffic_should_stop = None

def _worker_create_traffic(ids, prio, finish):
    try:
        while True:
            #for index in ids:
            if bool(finish.value):
                return
            index = ids[random.randint(0, len(ids) - 1)]
            query = {
                "id": index
            }
            res = requests.get(f"{BACKEND_URL}/items", params=query)
            if res.status_code == 200:
                data = res.json()
                print(f"{data['index']}: {data['_backend']}")
            else:
                print(f"Error status {res.status_code}")       
            if not prio:
                time.sleep(0.05)
    
    except Exception as e:
        logging.error(traceback.format_exc())

class TestAgent:
    def __init__(self, n_workers=8):
        global traffic_should_stop
        self.ids = []
        self.prio_ids = []
        self.n_workers = n_workers
        self.worker_procs = []
        self.prio_backends = [ "backend_1", "backend_2" ]
        self.workers_should_stop = Value('i', 0)
        
        n_normal_workers = n_workers/2 + 1
        #n_normal_workers = n_workers
        for i in range(self.n_workers):
            if i <= n_normal_workers: 
                worker_proc = Process(target=_worker_create_traffic, args=(self.ids, False, self.workers_should_stop, ))
            else:
                worker_proc = Process(target=_worker_create_traffic, args=(self.prio_ids, True, self.workers_should_stop, ))
            self.worker_procs.append(worker_proc)

    def setup_infra(self):
        subprocess.run("docker compose -f ../docker-compose.yaml up -d", shell=True, check=True)
    
    def populate_data(self):
        seen_prio_backends = []
        with open(DATA_FILE) as file:
            for line in file:
                index, value = line.split(",")
                self.ids.append(index)
                data = {
                    "index": index,
                    "value": value
                }
                query = {
                    "id": index
                }
                while True:
                    res = requests.post(f"{BACKEND_URL}/items", json=data, params=query)
                    if res.status_code == 201:
                        backend = res.text
                        print(f"Item {index} saved to {backend}")
                        if backend in self.prio_backends and backend not in seen_prio_backends:
                            self.prio_ids.append(index)
                            seen_prio_backends.append(backend)
                        break
                    else:
                        print(f"Failed populating data {index}, try again ...")
                        time.sleep(1)
                time.sleep(0.05)

        
        print("Finish populating the data")

    def create_traffic(self):
        try:
            for i in range(len(self.worker_procs)):
                self.worker_procs[i].start()
        except KeyboardInterrupt:
            print("Keyboard interrupt! Exitting ...")
            for i in range(len(self.worker_procs)):
                self.worker_procs[i].terminate()
    
    def stop_traffic(self):
        try:
            print("Stopping traffic")
            self.workers_should_stop.value = 1
            for i in range(len(self.worker_procs)):
                self.worker_procs[i].join()
        except KeyboardInterrupt:
            print("Keyboard interrupt! Exitting ...")
            for i in range(len(self.worker_procs)):
                self.worker_procs[i].terminate()
    
    def visualize_result(self):
        v = TestVisualizer()
        v.visualize()

    def teardown_infra(self):
        subprocess.run("docker compose down", shell=True, check=True)


if __name__ == "__main__":
    agent = TestAgent(n_workers=8)
    agent.setup_infra()
    agent.populate_data()
    agent.create_traffic()
    time.sleep(5*60)
    agent.stop_traffic()
    time.sleep(5)
    agent.visualize_result()
    agent.teardown_infra()