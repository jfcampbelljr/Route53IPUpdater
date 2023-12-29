# Route53IPUpdater
Gets public IP address and updates DNS Entry in Route 53

You will need to install AWS CLI (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and the boto3 python library (pip3 install boto3) for this program to work.

Once AWS CLI is installed create a profile for the updater:
aws configure --profile <Your-Profile-Name>

Create a config.json file in the same directory as this script with the following content:
{
    "domain_name": "-YOUR-DOMAIN-NAME",
    "record_name": "-A-RECORD-TO-UPDATE",
    "hosted_zone_id": "-ROUTE53-ZONE-ID",
    "aws_profile": "-AWSCLI-PROFILE",
    "current_ip":"0.0.0.0"
}

If you are going to run this using crontab, move the config.json to your home folder.

Adding the following to your crontab file (crontab -e) will cause this program to run every 15 minutes and send an update to route 53 if your public IP changes and
will also create a file called lastupdate.log that will contain messages from the last run of the program:
*/15 * * * * python3 /home/<yourusername>/PublicIPUpdate.py>lastupdate.log

