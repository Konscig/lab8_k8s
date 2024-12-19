# Используем официальный образ Ubuntu для сборки
FROM ubuntu:20.04 AS builder

# Устанавливаем нужные зависимости в неинтерактивном режиме
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        golang \
        libc6-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем исходные файлы в контейнер
COPY . .

# Обновляем зависимости и собираем приложение
RUN go mod tidy && \
    go build -o main .

# Используем тот же базовый образ Ubuntu для исполнения
FROM ubuntu:20.04

# Устанавливаем нужные зависимости в неинтерактивном режиме
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libc6-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем скомпилированный бинарный файл из стадии сборки
COPY --from=builder /app/main /app/main

# Указываем команду для запуска контейнера
CMD ["/app/main"]
