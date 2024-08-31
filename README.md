# HAProxy Consistent Hashing with Bounded Load Testbed

This repository desmonstrates the performance of the Consistent Hashing with Bounded Load algorithm of HAProxy.

We also evaluated some algorithmic changes on the original algorithm regardings the process of choosing the next server when the targeted server is full.

- Rotor routing

- Random jump

For the experiment, we leverage release v2.9.0 of HAProxy. The implementations can be found in our [forked repository](https://github.com/hviet2603/haproxy), within the following branches and tags:

- Tag `v2.9.0`

- Branch `v2.9.0-rotor`

- Branch `v2.9.0-randomjump`

## The experiment

The experiment sets up a docker-compose based test bed with up to 20 servers, each with its own cache server, and a HAProxy instance that distributes the requests to the servers. We also set up Prometheus and Grafana servers to monitor the overall cache hits rate as well as the hits rate for each servers.

### Set up the test bed

#### Build the HAProxy Docker images

The following bash scripts can be run to build the images:

- `build.sh`: original version, image name: `vdocker2603/haproxy-v2.9.0-nap:normal`.

- `build-rotor.sh`: rotor routing algorithm, image name: `vdocker2603/haproxy-v2.9.0-nap:rotor`.

- `build-chrj.sh`: random jump algorithm, image name: `vdocker2603/haproxy-v2.9.0-nap:chrj`.

Custom implementations can also be applied by pulling the forked repository, making change to the code and built with the `haproxy-local.dockerfile` file.

#### Generate the templates for docker-compose

The docker-compose templates can be generated using the bash script `TestBed/template/gen_templates.sh`.

`bash gen_templates.sh {number of backend servers}`

Up to 20 backend servers can be set up.

### Running the experiments

Comment and uncomment lines in the `docker-compose.yaml` file to select the algorithm:

```yaml
  ### load balancer ###
  haproxy:
    image: vdocker2603/haproxy-v2.9.0-nap:normal
    #image: vdocker2603/haproxy-v2.9.0-nap:chrj
    #image: vdocker2603/haproxy-v2.9.0-nap:rotor
    ports:
      - 8080:80
      - 8404:8404
    volumes:
      - ./haproxy_conf/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg
    depends_on:
      - backend_1
      - backend_2
      - backend_3
      - backend_4
      - backend_5
      - backend_6
      - backend_7
      - backend_8
```

Run the test bed with `docker compose up -d`.

**Note:** Before starting the test bed, the access right to the folder `TestBed/monitoring/grafana` and all of its content may need to be changed. This can be done with e.g. `chmod -R 777 TestBed/monitoring/grafana`. 

Requests to the servers can be sent to the HAProxy instance through `localhost:8080`.

The cache hits rate can be viewed with the Grafana UI at `http://localhost:3000`.

We also provide a test script to send requests to the servers at `TestBed/test/test.py`. The test script populates data from `data.txt` to the servers and sends requests to retrieve these items. The requests will be sent continuously in 5 minutes. At the end, the results will be visualized and saved to the folder `TestBed/test/plots`.

- Install the dependencies required by the test script with `python3 -m pip install -r requirements.txt`.

- Run the test script: `python3 test.py`

