# start http://localhost:15672/ &

cd ./frontend
npm run dev &
cd ..
python ./manage.py runserver


# docker run -it --rm --network test --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management &