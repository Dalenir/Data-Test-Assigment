## Test Assignment
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)![Redis](https://img.shields.io/badge/Redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
#### Rules and examples: `/rules`

----

## How to spin it for the first time:
0. - Unzip test data in `/mongo` folder as `/mongo/data.json`
   - Copy `/Deploy/.env.example`, save it as `/Deploy/.env`, and tweak envs if you wish.
----
1. Build the Docker image:
    ```shell
    docker-compose -f Deploy/dev_compose.yml build
    ```

2. Import data into MongoDB:
    ```shell
    docker-compose -f Deploy/dev_compose.yml up -d mongo && docker exec -it MongoTst /bin/sh -c  'mongoimport --host=localhost:$MONGO_PORT -d $MONGO_TSDB -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin -c $MONGO_TCOL --file data/data.json --jsonArray'
    ```

3. Start the services:
    ```shell
    docker-compose -f Deploy/dev_compose.yml up -d rabbitmq mongo && sleep 10; docker-compose -f Deploy/dev_compose.yml up -d report_service send_service
    ```
---
## Results and reasons
- The main target was specified as **speed**. That's why my first idea was to put all phone data reports in Redis cache and schedule a task for report compilation.
- After clarifying the question, I found that accuracy of data is very important as well, so I made the second solution, with MongoDB aggregation as a requirement.
- But the Redis solution was much, much faster, so I made it optional and set it to a random value in the test sending service with an option to make all messages with one mode (in .env).
- Some ports in Docker Compose are open only because that's Docker Compose for development. The same story with mounted volumes.
---
## Failures and limitations
- I had no experience working with RabbitMQ RPC pattern before. More precisely, for RPC, I used gRPC, and RabbitMQ for convenient queues. That's why I was carried away from test assignment rules and really not sure about my final implementation.
- After some home-brew solutions with different queues and topics, I just used aio-pika RPC pattern out-of-the-box, and that made some fields in the answer meaningless. I still left them, lol.
- Error handling and logging are pretty much nonexistent to save me some work hours.
- In the real world, I'd start with metrics, but for the sake of the test assignment, I chose to use only the info I have in the task. That was a mistake too.
- Mongo import from JSON is pretty slow.
---
## Steps to make this service good
#### In a world where I have all the time in it.
1. Unit Tests.
2. Metrics + Compliance Tests.
3. Logs.
4. User-friendly error handling.
5. User-friendly and unified data classes at RPC call, RPC answer.
6. Adaptive Redis caching scheduler.
