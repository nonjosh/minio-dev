# Learn MinIO

## Setup with Docker Compose

```sh
docker-compose up -d
```

## TODO

- [x] mc
    Download binary for Linux
    ```sh
    wget https://dl.min.io/client/mc/release/linux-amd64/mc
    ```
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
- [ ] [Select API](https://docs.min.io/docs/minio-select-api-quickstart-guide.html)
    - [x] enable parquet support
        To enable Parquet set the environment variable `MINIO_API_SELECT_PARQUET=on`
    - [ ] single `csv` or `parquet` file
    - [ ] directory of `csv` files
    - [ ] directory of `parquet` files
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
- [ ] MinFS

# References

- [Getting started with Delta Lake with Jupiter Notebook](https://laptrinhx.com/getting-started-with-delta-lake-with-jupiter-notebook-3085750171/)
- [Big Data without Hadoop/HDFS? MinIO tested on Jupyter + PySpark](https://python.plainenglish.io/big-data-without-hadoop-hdfs-minio-tested-on-jupter-pyspark-7b89a249ec94)
- [s3-userguide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-userguide.pdf)
- []
