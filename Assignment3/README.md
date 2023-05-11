# How to run

### How to run docker compose

1. cd compose (move into the compose folder)
2. sudo docker compose up

### How run in kubernetes

1. cd kubernetes
2. cd mongo-statefulset
3. kubectl apply -k .(Note: change the persistant volume paths in PersistantVolume.yaml)
4. cd ../
5. kubectl apply -f ./mysql-statefulset/
6. kubectl apply -f ./Namespace/
7. kubectl apply -f ./goAuth/
8. kubectl apply -f ./python-tiny-url/
9. kubectl apply -f ./nginx/

####Optional

10. kubectl apply -f ./Bonus\ -\ Network-Policy/
11. kubectl apply -f ./Bonus\ -\ rbac/

