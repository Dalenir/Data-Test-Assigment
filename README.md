docker exec -it MongoTst /bin/sh -c  'mongoimport --host=localhost:$MONGO_PORT -d $MONGO_TSDB -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin -c $MONGO_TCOL --file /
mongo_tst/data.json --jsonArray'
