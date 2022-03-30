# Learn MinIO

## Setup

### Start MinIO server with Docker Compose

```sh
docker-compose up -d
```

### Import sample data

```sh
./bin/mc -C .mc mb myminio/mycsvbucket
curl "https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv" > data/TotalPopulation.csv
gzip data/TotalPopulation.csv
./bin/mc -C .mc cp data/TotalPopulation.csv.gz myminio/mycsvbucket/sampledata/
./bin/mc -C .mc sql --query "select * from S3Object where Location like '%United States%'" myminio/mycsvbucket/sampledata/TotalPopulation.csv.gz

./bin/mc -C .mc mb myminio/test
./bin/mc -C .mc cp --recursive data/test/ myminio/test/
```

## TODO

- [x] mc
  Download binary for Linux

  ```sh
  wget https://dl.min.io/client/mc/release/linux-amd64/mc
  ```

- [x] create shareable link for object (with expiry time)
- [x] bucket policy
  Create public access to a bucket/directory

  ```sh
  # change bucket policy: mc policy {policy} {host}/{bucket}
  mc policy set public myminio/mybucket
  ```

- [x] user policy

  ```sh
  #Add a new user 'myuser' on MinIO.
  mc admin user add myminio/ myuser password

  #Disable a user 'myuser' on MinIO.
  mc admin user disable myminio/ myuser

  #List all users on MinIO.
  mc admin user list --json myminio/

  #Display info of a user
  mc admin user info myminio myuser

  #Example: Add a user to a group 'mygroup' on MinIO.
  #Group is created if it does not exist.

  mc admin group add myminio mygroup myuser

  #Remove user from a group 'mygroup' on MinIO.
  mc admin group remove myminio mygroup myuser

  #Get info on a group 'mygroup' on MinIO.
  mc admin group info myminio mygroup

  #List all groups on MinIO.
  mc admin group list myminio


  #Create a new user with policy
  #readonly
  #Grants read-only permissions for all buckets and objects on the MinIO server.

  #readwrite
  #Grants read and write permissions for all buckets and objects on the MinnIO server.

  #diagnostics
  #Grants permission to perform diagnostic actions on the MinIO server.

  #writeonly
  #Grants write-only permissions for all buckets and objects on the MinIO server.

  ./mc admin policy set myminio readwrite user=myuser
  ./mc admin policy set myminio readonly user=myuser
  ./mc admin policy set myminio diagnostics user=myuser
  ./mc admin policy set myminio writeonly user=myuser
  ```

- [x] [Select API](https://docs.min.io/docs/minio-select-api-quickstart-guide.html)
  - [x] enable parquet support
    To enable Parquet set the environment variable `MINIO_API_SELECT_PARQUET=on`
  - [x] single `csv` or `parquet` file
  - [x] directory of `csv` files
  - [x] directory of `parquet` files
- [ ] [Delta Lake](https://docs.delta.io/latest/quick-start.html)
- [ ] [Deploy MinIO Operator on Kubernetes](https://github.com/minio/operator)

  ```sh
  helm repo add minio https://operator.min.io/
  helm install --namespace minio-operator --create-namespace --generate-name minio/minio-operator
  kubectl apply -f https://raw.githubusercontent.com/minio/operator/master/examples/tenant.yaml
  ```

  replace [deprecated chart](https://github.com/minio/charts)

  ```sh
  helm repo remove minio
  helm repo add minio https://operator.min.io/
  helm install --namespace minio-operator --create-namespace --generate-name minio/minio-operator
  kubectl apply -f https://github.com/minio/operator/blob/master/examples/tenant.yaml
  ```
  
- [ ] troubleshoot `413 Request Entity Too Large` when using nginx
- [x] [MinFS](https://github.com/minio/minfs)

## References

- [Getting started with Delta Lake with Jupiter Notebook](https://laptrinhx.com/getting-started-with-delta-lake-with-jupiter-notebook-3085750171/)
- [Big Data without Hadoop/HDFS? MinIO tested on Jupyter + PySpark](https://python.plainenglish.io/big-data-without-hadoop-hdfs-minio-tested-on-jupter-pyspark-7b89a249ec94)
- [s3-userguide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-userguide.pdf)
- [mc admin guide](https://docs.min.io/docs/minio-admin-complete-guide.html#user)
- [Simple AWS S3 Logging in Python3 Using Boto3](https://medium.com/nerd-for-tech/simple-aws-s3-logging-in-python3-using-boto3-cfbd345ef65b)
