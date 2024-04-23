# Off-Request

## Dependencies:
+ Python version: 3.10

## Installation:

+ Clone project from github
```shell
git clone git@github.com:mahdizojaji/Off-Request.git
```

+ Copy env file from template
```shell
cp .env.example .env
```

+ Edit env varaibles
```shell
nano .env
```
|        Varaible          | Description / Example            |
| ------------------------ | -------------------------------- |
|       SECRET_KEY         | random string                    |
|          DEBUG           | 0 or 1 recommed 0 for production |       
|      ALLOWED_HOSTS       | localhost,domain.com,1.2.3.4 (insert your domain or ip)  |
|     POSTGRES_DB_NAME     | postgres                         |
|      POSTGRES_USER       | postgres                         |
|    POSTGRES_PASSWORD     | postgres                         |
|      POSTGRES_PORT       | 5432                             |
|      POSTGRES_HOST       | postgres                         |
| BALETHON__BALE_BOT_TOKEN | 123:abcdfdsfghjdgsdsgd  get from @botfather |
|     EMPLOYER_BALE_ID     | 283469498 get from @userinfo_robot |
|   CSRF_TRUSTED_ORIGINS   | http://localhost:8000,https://domain.com,http://1.2.3.4:8000 (insert your domain or ip:port)|

+ Install docker & docker compose
  + You should install docker & docker compose on your os

+ Set docker mirror
```shell
sudo bash -c 'cat > /etc/docker/daemon.json <<EOF
{
  "insecure-registries" : ["https://docker.arvancloud.ir"],
  "registry-mirrors": ["https://docker.arvancloud.ir"]
}
EOF'
```
```shell
docker logout
```
```shell
$ sudo systemctl restart docker
```

+ Run docker compose services
```shell
docker compose up --build -d
```

+ Create superuser
```shell
docker compose exec django python manage.py createsuperuser
```

+ Collect static files
```shell
docker compose exec django python manage.py collectstatic
```
