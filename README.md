
## Test assigment

#### Rules and examples: `/rules`

## How to spin it for the first time:

0. Unzip test data in `/mongo` folder as `/mongo/data.json`

   Copy `/Deploy/.env.example`, save it as `/Deploy/.env` and tweak envs if you wish.
1.
    ```shell
    docker compose -f Deploy/dev_compose.yml build 
    ```
2. ```shell
    docker exec -it MongoTst /bin/sh -c  'mongoimport --host=localhost:$MONGO_PORT -d $MONGO_TSDB -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin -c $MONGO_TCOL --file mongo_tst/data.json --jsonArray'
    ```
3. 
    ```shell
   docker compose -f Deploy/dev_compose.yml up -d rabbitmq mongo && sleep 10; docker compose -f Deploy/dev_compose.yml up -d
    ```

## Results and reasons

- The main target was specified as **speed**. That's why my first idea was to put all phone data reports in redis cache and shedule task for report compilation.
- After clarifying question I found that accuracy of data is very important aswell, so I made the second solution, with mongo aggregation at requirement.
- But Redis solution was much, much faster, so I made it optional and set it to random value in test sending service with option to make all messages with one mode (in .env).
- Some ports in docker compose are open only because that's docker compose for development. Same story with mounted volumes.


## Failures and limitations

- I had a no expirience working with RabbitMQ RPC pattern before. More precisely RPC I used gRPC, and RabbitMQ for convenient queues. That's why I was carried away from test assigment rules and really not sure in my final implementation.
- After some home-brew solutions with different queues and topics, I just used aio-pika RPC pattern from-the-box, and that made some fields in answer meaningless. I still left them, lol.
- Error handling and logging are pretty much not existing for saving me some workhours.
- In real world, I'd start with metrics, but for the sake of test assigment I chose to use only info I have in task. That was a mistake too.


## Steps to make this service good
#### In the world where I have all time in it.

1. Unit Tests.
2. Metrics + Compliance Tests.
3. Logs.
4. User-friendly error handling.
5. Adaptive redis caching sheduler.