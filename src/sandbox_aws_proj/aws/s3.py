from typing import cast
from mypy_boto3_s3.literals import BucketLocationConstraintType
from sandbox_aws_proj import session

# instantiate boto3 resource for s3
s3 = session.aws_session.resource("s3")
all_my_buckets = [bucket.name  for bucket in s3.buckets.all()]


# check the bucket
def check_bucketname(name):
    '''
        ṅcheck the bucket name 
    '''
    
    for bucket_name in all_my_buckets:
        if bucket_name.lower() == name.lower():
            return True


# create a new bucket
def create_bucket():
    
    bucket_name =str(input("please enter the bucketname to be created : "))
    try:

        if not check_bucketname(bucket_name):
            region = s3.meta.client.meta.region_name
            if region == "us-east-1":
                s3.create_bucket(Bucket=bucket_name)
            else:
                response = s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        "LocationConstraint": cast(BucketLocationConstraintType, region)
                    },
                )
                return response
    except Exception as exp:
        print(f"Exception Details - {exp}")
    
# upload the files 
def upload_s3(bucket_name:str):

    file_1 = "./src/sandbox_aws_proj/aws/data/userdetails.txt"

    try:

        if not check_bucketname(bucket_name):
            print(f"Bucket {bucket_name} does not exist. Please create the bucket first.")
            return
        
        else:
            file_key = file_1.split('/')[5]
            response = s3.Bucket(bucket_name).upload_file(Filename=file_1,Key=file_key)
            return response
    except Exception as exp:
        print(f"Exception Details - {exp}")


def read_files_s3(bucket_name:str,file_name:str):
    try:
        obj=s3.Object(bucket_name=bucket_name,key=file_name)
        body = obj.get()['Body'].read()

        return body
    except Exception as exp:
        print(f"Exception - {exp}")


def update_files_s3(bucket_name:str,file_name:str):

    try:
        updated_file = "./src/sandbox_aws_proj/aws/data/users.txt";

        # with open(file="./src/sandbox_aws_proj/aws/data/users.txt",encoding="utf-8") as file2:
        #     file_data = file2.read()

        with open(file=updated_file, mode="rb") as file:
            s3.Object(bucket_name=bucket_name, key=file_name).put(Body=file)

        response = s3.Object(bucket_name=bucket_name,key=file_name).get()['Body'].read()

        return response

    except Exception as exp:
        print(f"Exception - {exp}")
        

def delete_s3_objects(bucket_name:str):
    list_files = s3.Bucket(name=bucket_name).objects.all();

    for file_name in list_files:
        s3.Object(bucket_name=bucket_name,key=file_name.key).delete()

def delete_s3_bucket(bucket_name:str):
    list_files = s3.Bucket(name=bucket_name).objects.all();

    if list_files:
        delete_s3_objects(bucket_name=bucket_name)
    
    s3.Bucket(name=bucket_name).delete()
    



if __name__ == "__main__":
    # print(get_buckets())
    # print(create_bucket())
    # print(upload_s3("boto3-vg"))
    # print(read_files_s3("boto3-vg",'userdetails.txt'))
    # print(update_files_s3("boto3-vg",'userdetails.txt'))
    # delete_s3_objects("boto3-vg")
    delete_s3_bucket("boto3-vg")
