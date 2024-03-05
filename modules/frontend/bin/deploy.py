import os

import boto3

MODULE_DIRECTORY = "modules/frontend/"
BUCKET_NAME = "michalskiba-dev"
LOCAL_SOURCE_DIRECTORY = f"{MODULE_DIRECTORY}src/public/"
REMOTE_DESTINATION_DIRECTORY = "frontend/"


def build_module():
    print("Building module ...")
    os.system(f"cd {MODULE_DIRECTORY} && sudo bin/hugo")
    print("Module built")


def clean_remote_destination_directory(s3_client):
    print("Cleaning remote destination directory ...")
    paginator = s3_client.get_paginator("list_objects")
    page_iterator = paginator.paginate(
        Bucket=BUCKET_NAME, Prefix=REMOTE_DESTINATION_DIRECTORY
    )
    for page in page_iterator:
        for obj in page.get("Contents") or []:
            s3_client.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])
    print("Remote destination directory cleaned")


def upload(s3_client):
    print("Uploading ...")
    for root, _, filenames in os.walk(LOCAL_SOURCE_DIRECTORY):
        for file_name in filenames:
            local_source_file_path = os.path.join(root, file_name)
            remote_destination_file_path = (
                REMOTE_DESTINATION_DIRECTORY
                + os.path.relpath(
                    path=local_source_file_path, start=LOCAL_SOURCE_DIRECTORY
                )
            )
            s3_client.upload_file(
                local_source_file_path, BUCKET_NAME, remote_destination_file_path
            )
    print("Uploaded")


def deploy() -> None:
    build_module()
    s3_client = boto3.client("s3")
    clean_remote_destination_directory(s3_client)
    upload(s3_client)


if __name__ == "__main__":
    deploy()
