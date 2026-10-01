my-aws-project/
├── .venv/                      # Managed automatically by uv (git-ignored)
├── .python-version             # Specifies the Python version for the environment
├── pyproject.toml              # Global dependencies, uv configuration, and metadata
├── uv.lock                     # Pinning exact dependency versions
├── README.md
├── .gitignore
├── src/                        # Main application logic folder
│   └── sandbox_aws_project/
│       ├── __init__.py
│       ├── main.py             # Orchestrates operations sequentially
│       ├── aws/                # Dedicated package for AWS SDK / Boto3 modules
│       │   ├── __init__.py
│       │   ├── s3.py           # S3 client wrapper, wrappers for bucket/object operations
│       │   ├── dynamodb.py     # DynamoDB interaction layer
│       │   └── sqs.py          # SQS queue operations
│       └── utils/              # Shared helper functions (logging, formatting, config)
│           ├── __init__.py
│           ├── logger.py
│           └── config.py
└── tests/                      # Unit and integration test suite
    ├── __init__.py
    ├── test_s3.py
    └── test_dynamodb.py



## S3

In Boto3, S3 operations are available through either a **resource** (the style used in your `s3.py`) or a **client**. The resource API is object-oriented; the client exposes AWS API operation names directly.

**Common resource operations**
| Operation | Boto3 call | Purpose |
|---|---|---|
| List buckets | `s3.buckets.all()` | Iterate over buckets in the account. |
| Create bucket | `s3.create_bucket(...)` | Create a bucket. For most regions, include `CreateBucketConfiguration={"LocationConstraint": region}`. |
| Check bucket | `s3.Bucket(name). creation_date` or client `head_bucket(...)` | Check whether a bucket exists and is accessible. |
| List objects | `s3.Bucket(name).objects.all()` | Iterate over objects in a bucket. |
| Upload file | `s3.Bucket(name).upload_file(Filename=path, Key=key)` | Upload a local file. |
| Download file | `s3.Bucket(name).download_file(Key=key, Filename=path)` | Download an object to a local file. |
| Read object | `s3.Object(name, key).get()` | Get object metadata and its streaming `Body`. Call `Body.read()` to read bytes. |
| Write/replace object | `s3.Object(name, key).put(Body=data)` | Create or replace an object. `Body` accepts bytes or a binary file stream. |
| Delete object | `s3.Object(name, key).delete()` | Delete one object. |
| Delete bucket | `s3.Bucket(name).delete()` | Delete an empty bucket. Delete its objects first. |

Equivalent commonly used **client methods** include `list_buckets()`, `create_bucket()`, `head_bucket()`, `list_objects_v2()`, `put_object()`, `get_object()`, `delete_object()`, and `delete_bucket()`.

Your functions `create_bucket`, `upload_s3`, `read_files_s3`, `update_files_s3`, `delete_s3_objects`, and `delete_s3_bucket` are your own helper functions; they call Boto3 methods internally.

**Important:** the current `if __name__ == "__main__":` block calls `delete_s3_bucket("boto3-vg")`. Running this file will delete the objects in that bucket and then delete the bucket. Remove or comment out that call unless you intend to perform that deletion.
