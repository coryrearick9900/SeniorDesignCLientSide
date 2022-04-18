i=0

docker pull rabbitmq
docker network create data_collection

docker run -it --rm --network data_collection --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management &



for i in {1..10}
do
    if docker ps | grep -q "Server startup complete"; then
        bash ./startup-dev.sh
    else
        echo "Docker is not running yet, waiting 5 seconds"
    fi
    

done

# while docker ps | grep -q "Server startup complete"
# do
# echo "container is running"
# i=$[$i+1]

# for i in {1..10}
# do
#     echo "This is the $i th time"
# done



# done