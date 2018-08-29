# Build and run

To build and run the server we use Docker.

1. Set Mapbox Token:

You need to set a API acces token for Mapbox. You can get your public token [here](https://www.mapbox.com/account/).

You have to set the environment variable `REACT_APP_MAPBOX_ACCESS_TOKEN=<YourToken>` for npm in the `.env` file under `./frontend`.

2. Build:

```bash
docker build -t <container-name> .
```

3. Run:

```bash
docker run --env HANA_USER=<HANA_USER> --env HANA_PWD=<HANA_PWD> --rm -it -p 8000:8000 <container-name>
```

4. Start Server:

```bash
python3 backend/__main__.py
```

Additional Information:

Run commands in docker container:

```bash
docker run -i -t <container-name> /bin/bash
```
