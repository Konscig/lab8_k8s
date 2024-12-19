#!/bin/bash

# Убедитесь, что kubectl и docker настроены правильно

# Функция для сборки Docker образа
build_docker_image() {
  local service_name=$1
  echo "Building Docker image for $service_name..."
  cd "$service_name" || exit 1  # Переход в директорию сервиса
  docker build -t "konscig/$service_name:latest" .  # Сборка образа
  if [ $? -eq 0 ]; then
    echo "Docker image for $service_name built successfully."
  else
    echo "Failed to build Docker image for $service_name."
    exit 1
  fi
  cd ..  # Возврат в исходную директорию
}

# Функция для деплоя манифеста
deploy() {
  local manifest_file=$1
  echo "Deploying $manifest_file..."
  kubectl apply -f "$manifest_file"
  if [ $? -eq 0 ]; then
    echo "$manifest_file deployed successfully."
  else
    echo "Failed to deploy $manifest_file."
    exit 1
  fi
}

# Сборка Docker образов для каждого сервиса
services=("stars" "sequences" "fibonacci" "coinflip" "word-count")

for service in "${services[@]}"; do
  build_docker_image "$service"
  docker push "konscig/$service:latest"
done

# Деплой манифестов из файла
deploy "deployment.yaml"

echo "Deployment completed."
