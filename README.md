# JustChat
Just some chat example with Clean Architecture and more

# Setup
- Copy repo
```shell
git clone git@github.com:KrySeyt/JustChat.git
```

- Go to directory
```
cd JustChat
```

- Run with Docker
```shell
docker compose -f docker-compose.dev.yml
```

- Open http://localhost:8000/docs and use

# Tests
- Run tests with Docker
```shell
docker compose -f tests.yml up --exit-code-from just_chat_tests
```
