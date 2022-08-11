# Hvordan koble til prod (dette kan være enklere, men farligere hehe)

# Hvordan sette opp database lokalt?

Installere en klient som kan snakke med databasen

```
$ brew install pgcli #eventuelt installer hele postgresql
```

Starte databasen
```
docker run --name mydb -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres
```

Koble til databasen
```
psql -h localhost -U postgres --password
```
Det vil komme en prompt hvor du legger inn passordet "password"

Populere databasen med data
Filen ligger på [drive](https://drive.google.com/file/d/1Z0xOdDjZLqWo47UxYHsHqdF0_cEXUTZy/view?usp=sharing)

```
psql -h localhost -U postgres --password < pizzabot_dump.sql
```
