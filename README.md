# Install docker in linux

[Install Docker](https://docs.docker.com/engine/install/ubuntu/)


# Install Conda

[Install Conda](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html)

# Create DB with docker

```bash
docker run -d -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=P4ssW0rD -e POSTGRES_DB=postgres_db -p 5432:5432 --name db postgres:19-alphine

```
# Create Conda Environment

```bash
conda create -n socket python=3
```
# Activate Environment

```bash
conda activate socket
```

# Install requirements

```bash
pip install -r requirements.txt
```
# Start socket server

```bash
python server.py
```

# Start socket client

```bash
python client.py
```