import json
import boto3
import pandas as pd
import datetime

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("MetadataTable")

def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        response = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(response["Body"])
        
        metadata = {
            "filename": key,
            "upload_timestamp": datetime.datetime.utcnow().isoformat(),
            "file_size_bytes": response["ContentLength"],
            "row_count": df.shape[0],
            "column_count": df.shape[1],
            "column_names": df.columns.tolist()
        }
        
        table.put_item(Item=metadata)
        
    return {"statusCode": 200, "body": json.dumps(metadata)}
