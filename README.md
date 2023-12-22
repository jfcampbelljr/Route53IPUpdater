# Route53IPUpdater
Gets public IP address and updates DNS Entry in Route 53

Create a config.json file in the same directory as this script with the following content:
{
    "domain_name": "-YOUR-DOMAIN-NAME",
    "record_name": "-A-RECORD-TO-UPDATE",
    "hosted_zone_id": "-ROUTE53-ZONE-ID",
    "aws_profile": "-AWSCLI-PROFILE"
}

