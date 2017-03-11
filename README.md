# YeoulParking

Return Montreal's free parking lot during snow removal operations.

## Build

```bash
docker build -t yeoulparking .
```

## Run

"Production" mode:

```bash
docker run -d \
    -p 5000:5000 \
    --name yeoulparking \
    yeoulparking
```

Development mode:

```bash
docker run -d \
    -p 5000:5000 \
    -e FLASK_DEBUG=1 \
    --name yeoulparking \
    -v $PWD:/usr/src/app \
    yeoulparking
```

## API

`/ping` (validate the server is working):

```bash
curl http://localhost:5000/ping
```

`/parking` returns the available parking lots:

```bash
curl -d http://localhost:5000/parkings?latitude=0.0000&longitude=1.0000
```

Additionally, `latitude` and `longitude`can be provided in the query string,
in which case the distance to each parking will be returned,
and the results will be ordered with the closest parkings first.