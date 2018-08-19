# Build and run

1. Build:

```bash
docker build -t <container-name>
```

2. Run:

```bash
docker run --env HANA_USER=<HANA_USER> --env HANA_PWD=<HANA_PWD> --rm -it -p 8000:8000 <container-name>
```

3. Start Server:

```bash
python3 backend/__main__.py
```

Additional Information:

Run commands in docker container:

```bash
docker run -i -t <container-name> /bin/bash
```
