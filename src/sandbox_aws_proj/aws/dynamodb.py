from sandbox_aws_proj.session import aws_session
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key 

# access the dynamodb resource 
dynamodb_sandbox = aws_session.resource("dynamodb")

# table object 
employees = dynamodb_sandbox.Table(name="employees")

# getItems - Scan()
def getItems():
    try:
        response = employees.scan(ReturnConsumedCapacity="TOTAL")

        if response is not None:
            output = {
                "Items" : response["Items"],
                "ConsumedCapacity" : response["ConsumedCapacity"] 
            }
            return output
    except Exception as exp:
        print(f"Exception Details - {exp}")


# getItemsbyPartition - Query
def getItemsbyPartition(partition_key):
    '''
        Query
            → Multiple items possible
            → PK required
            → SK condition optional
    '''
    try:
        response  = employees.query(KeyConditionExpression=partition_key)

        if "Items" in response:
            return response["Items"]
        else:
            print(f"No items found for partition-key : {partition_key}")
    except ClientError as exp:
        print(f"Exp - {exp}")


#getItem - single Item 
def getItem(partition_key):
    '''
        GetItem
            → Exact ONE item
            → Complete PK + SK required
    '''

    try:
        # either you can send partition key or composite key (partition + sort)
        response = employees.get_item(Key= partition_key,ReturnConsumedCapacity="TOTAL")

        if "Item" in response:
            output = {
                "Item" : response["Item"],
                "ConsumedCapacity" : response["ConsumedCapacity"]
            }
            return output
        else:
            print(f"Item not found for partition-key : {partition_key}")
    except ClientError as exp:
        print(f"exception details - {exp}")

# putItem
def putItem():
    emp_data = {
                "department":"IT",
                "employee_id":"E103",
                "email":"e103@gmail.com"
            }

    try:
        response = employees.put_item(Item=emp_data)

        status_code = response.get("ResponseMetadata",{}).get("HTTPStatusCode")

        if status_code == 200:
            print(f"Item inserted successfully - {response["ResponseMetadata"]["RequestId"]}")
        else:
            print(f"PitItem failed : Status-Code : {status_code}")
    except ClientError as exp:
        print(f"Exception Details - {exp}")
    except Exception as exp:
        print(f"Exception  - {exp}")


# update existing item
def updateItem(empdata):
    try:
        response = employees.update_item(
            Key={
                "department":empdata["department"],
                "employee_id":empdata["employee_id"]
            },
            UpdateExpression="SET email=:email",
            ExpressionAttributeValues={
                ":email":empdata["email"]
            },
            ReturnValues="UPDATED_NEW"
        )

        status_code = response.get("ResponseMetadata",{}).get("HTTPStatusCode")

        if status_code == 200:
            print(f"Item updated successfully - {response['Attributes']}")
        else:
            print(f"updateItem failed : Status-Code : {status_code}")
    except ClientError as exp:
        print(f"exception - {exp}")


def DeleteItem(emp_data):
    try:
        response = employees.delete_item(
            Key={
                "department":emp_data["department"],
                "employee_id":emp_data["employee_id"]
            }
        )

        status_code = response.get("ResponseMetadata",{}).get("HTTPStatusCode")

        if status_code == 200:
            print(f"Item deleted successfully - {response['ResponseMetadata']['RequestId']}")
        else:
            print(f"DeleteItem failed : Status-Code : {status_code}")
    except ClientError as exp:
        print(f"exception - {exp}")


if __name__ == "__main__":
    # print(getItems()) 

    # pk = Key("department").eq('IT')
     
    # print(getItemsbyPartition(partition_key=pk))



    parti_sort_key = {
        "department":"Legal",
        "employee_id":"E101"
    }

    print(getItem(parti_sort_key))

    # updated_employee = {
    #     "department":"IT",
    #     "employee_id":"E061",
    #     "email":"E061@gmail.com"
    # }
    # print(updateItem(empdata=updated_employee))


    # emp_data = {
    #     "department":"Legal",
    #     "employee_id":"E091"
    # }
    # DeleteItem(emp_data=emp_data)


