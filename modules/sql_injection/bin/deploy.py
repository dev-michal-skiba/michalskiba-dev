import os

import boto3

LOCAL_SOURCE_DIRECTORY = ".aws-sam/build/SQLInjectionAPI"
LOCAL_LAMBDA_PACKAGE_FILENAME = "lambda_package.zip"
LAMBDA_FUNCTION_NAME = "michalskiba-dev-sql-injection"


def build_module() -> None:
    print("Building module ...")
    os.remove(LOCAL_LAMBDA_PACKAGE_FILENAME)
    os.system(
        f"cd {LOCAL_SOURCE_DIRECTORY} && " f"zip -r ../../../{LOCAL_LAMBDA_PACKAGE_FILENAME} ."
    )
    print("Module built")


def upload() -> None:
    print("Uploading ...")
    with open(LOCAL_LAMBDA_PACKAGE_FILENAME, "rb") as lambda_package_file:
        lambda_package = lambda_package_file.read()
    lambda_client = boto3.client("lambda")
    lambda_client.update_function_code(FunctionName=LAMBDA_FUNCTION_NAME, ZipFile=lambda_package)
    print("Uploaded")


def deploy() -> None:
    build_module()
    upload()


if __name__ == "__main__":
    deploy()
