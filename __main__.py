"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

config = pulumi.Config()
env = config.get("environment") or "dev"

# 1. Tạo bucket
bucket = aws.s3.BucketV2("my-bucket",
    bucket=f"my-test-{env}-bucket-binhminh",
    tags={
        "Environment": env,
        "ManagedBy": "Pulumi",
    }
)

# 2. Bật versioning
versioning = aws.s3.BucketVersioningV2("my-bucket-versioning",
    bucket=bucket.id,
    versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
        status="Enabled"
    )
)

# 3. Bật encryption
encryption = aws.s3.BucketServerSideEncryptionConfigurationV2("my-bucket-encryption",
    bucket=bucket.id,
    rules=[aws.s3.BucketServerSideEncryptionConfigurationV2RuleArgs(
        apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationV2RuleApplyServerSideEncryptionByDefaultArgs(
            sse_algorithm="AES256"
        )
    )]
)

# 4. Block public access
public_access = aws.s3.BucketPublicAccessBlock("my-bucket-public-access",
    bucket=bucket.id,
    block_public_acls=True,
    block_public_policy=True,
    ignore_public_acls=True,
    restrict_public_buckets=True,
)

# Exports
pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)