# STORE.io

STORE.io is a django app api.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.
```bash
pip install -r requirements.txt
```

## Usage
set env file as below:
```bash
export STORE_DEBUG=1
export STORE_IO_SECRET_KEY='0@58!5ku+@*^o@pf#uh5=u+r1$w0vok*c9)4mri3()2vcxh6md'
export STORE_ALLOWED_HOSTS=*
export SUPER_USERNAME=admin
export SUPER_PASSWORD=admin

export STORE_DB_HOST=db
export STORE_DB_NAME=targetio_db
export STORE_DB_USERNAME=admin
export STORE_DB_PASSWORD=admin
export STORE_DB_PORT=5432

export STORE_CACHE_LOCATION='redis://cache:6379/0'
export STORE_TOKEN_CACHE_LOCATION='redis://cache:6379/1'
export STORE_IDEMPOTENT_CACHE_URL='redis://cache:6379/2'

export STORE_S3_ENDPOINT_URL='http://minio:9000'
export STORE_S3_ACCESS_KEY_ID='minioadmin'
export STORE_S3_SECRET_ACCESS_KEY='minioadmin'
export STORE_S3_STORAGE_BUCKET_NAME='store.io'
```
once time run command for build image:
```bash
make builddev
```

### for run app in `debug  mode`:
```bash
make debug
```

### for run app in `stage  mode`:
```bash
make stage
```

Note: for build super user with config `username=admin, password=admin`you must run command :
```bash
python manage.py createadminuser
```

### Check Health
you get healthly status:
```bash
{ip server}/ht/
```
### TODO:
- [ ] upload file in minio/s3