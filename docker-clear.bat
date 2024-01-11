@echo off

echo "Stopping and removing Docker containers..."
FOR /f "tokens=*" %%i IN ('docker ps -aq') DO (
    docker stop %%i
    docker rm %%i
)

echo "Removing Docker images..."
FOR /f "tokens=*" %%i IN ('docker images --format "{{.ID}}"') DO docker rmi -f %%i

echo "Waiting for 20 seconds..."
timeout /t 20 /nobreak >nul

echo "Inspecting Docker network..."
docker network inspect hitchhiking-network

echo "Removing Docker network..."
docker network rm hitchhiking-network