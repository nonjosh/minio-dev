import os
import io
import sys
import logging
import time
from datetime import datetime
import boto3

DEFAULT_ENDPOINT_URL = "http://192.168.0.101:9000"


def get_string_io_logger(log_stringio_obj, logger_name):
    # create logger
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s \t[%(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
    )
    logger.setLevel(logging.INFO)

    # add normal steam handler to display logs on screen
    io_log_handler = logging.StreamHandler()
    logger.addHandler(io_log_handler)

    # create stream handler and initialise it with string io buffer
    string_io_log_handler = logging.StreamHandler(log_stringio_obj)

    # add stream handler to logger
    logger.addHandler(string_io_log_handler)

    return logger


def rename_file(key, backup_key, backup_strategy):
    """
    Helper Function for put_content_to_s3 to rename file with backup key name or backup key folder
    Arguments:
            key {str} -- s3 file key
            backup_key {str} -- backup key
    Returns:
            renamed_key{str} -- renamed key
    """
    renamed_file = key + "_" + backup_key
    try:
        file_name = os.path.basename(key)
        folder = key.split(file_name)[0]
        if backup_strategy == "file":
            if key.count(".") == 1:
                file_name = (
                    file_name.split(".")[0]
                    + "_"
                    + backup_key
                    + "."
                    + file_name.split(".")[-1]
                )
                renamed_file = folder + file_name
        else:
            renamed_file = "{0}{1}/{2}".format(folder, backup_key, file_name)
    except Exception as err:
        print("Error Renaming file " + str(err))

    return renamed_file


def put_content_to_s3(
    s3_path,
    content,
    s3_client=None,
    s3_resource=None,
    region_name="us-east-1",
    backup_key=None,
    backup_strategy="file",
    endpoint_url=DEFAULT_ENDPOINT_URL,
):
    """
    Function to put string content to s3 for a given s3 path and region
    Arguments:
            s3_path {str} -- s3 path
            content {str} -- string content to be put into s3
    Keyword Arguments:
            s3_client {boto3.client.s3} (default: {None'})-- boto3 client for s3 , new client will be created if not provided
            s3_resource {boto3.resource.s3} (default: {None'}) -- boto3 resource for s3 , new resource will be created if not provided
            region_name {str}(default: {'us-east-1'}) -- AWS region
            backup_key {str} (default: {None}) -- backup key name, if provided and if file already exists in given s3 path a backup of existing content will be taken in same s3 path appedning the sepcified backup_key at the end of file name
    Returns:
            return_object {dict} -- return_object['data'] {str} -- error message if return_object['success'] is False
    """
    return_object = {"success": True, "data": ""}
    try:

        # create s3 client for given s3 path
        bucket = s3_path.split("/")[2]
        key = "/".join(s3_path.split("/")[3:])
        if not s3_client:
            s3_client_ = boto3.client("s3", region_name, endpoint_url=endpoint_url)
        else:
            s3_client_ = s3_client

        # if backup_key is specified take backup of old content
        if backup_key:
            results = s3_client_.list_objects(Bucket=bucket, Prefix=key)
            if "Contents" in results:
                if not s3_resource:
                    s3_resource_ = boto3.resource("s3", region_name)
                else:
                    s3_resource_ = s3_resource
                old_content = (
                    s3_resource_.Object(bucket, key)
                    .get()["Body"]
                    .read()
                    .decode("utf-8")
                )
                s3_client_.put_object(
                    Body=old_content,
                    Bucket=bucket,
                    Key=rename_file(key, backup_key, backup_strategy),
                )

        # put current content to s3
        s3_put_response = s3_client_.put_object(Body=content, Bucket=bucket, Key=key)
        if s3_put_response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception("Unable to put data to s3: {0}".format(s3_put_response))

    except Exception as err:
        return_object["success"] = False
        exception_message = "message: {0}\nline no:{1}\n".format(
            str(err), sys.exc_info()[2].tb_lineno
        )
        return_object["data"] = exception_message

    return return_object


def my_function():
    # create string i/o object as string buffer
    log_stringio_obj = io.StringIO()

    # create stream log handler with string i/o buffer
    log_handler = logging.StreamHandler(log_stringio_obj)
    logger = get_string_io_logger(log_stringio_obj, logger_name="my_s3_logger")

    # s3 log path
    timestamp = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
    s3_log_path = "s3://test/python_s3_loggger_demo/{0}/".format(timestamp)
    try:
        # do any task
        logger.info("Running my_function")

    except Exception as err:
        exception_message = "message: {0}\nline no:{1}\n".format(
            str(err), sys.exc_info()[2].tb_lineno
        )
        logger.error(exception_message)

    finally:
        # persist logs in s3
        s3_store_response = put_content_to_s3(
            s3_path=s3_log_path + "logs.txt", content=log_stringio_obj.getvalue()
        )
        assert s3_store_response["success"], "Error Putting logs to S3:\n{0}".format(
            s3_store_response["data"]
        )


def main():
    my_function()


main()
