import boto3
import json
import requests
import datetime

#log_file as a global variable.
log_file=''

#Open a log file
def open_log(FileName):
    global log_file
    log_file = open(FileName, 'a')
    return log_file

#Write message to log file
def write_log(message):
    global log_file
    #Get the current date and time
    CurrentDate = datetime.datetime.now()
    CurrentDate = CurrentDate.strftime("%Y-%m-%d %H:%M:%S")
    log_file.write(CurrentDate+": "+message + '\n')


# Function to load configuration from a JSON file
def load_config(filename):
    try:
        with open(filename, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        write_log(f"Config file '{filename}' not found.")
        return None
    except Exception as e:
        write_log(f"Error loading config: {e}")
        return None


# Use an HTTP service to get your current public IP address
def get_current_public_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        if response.status_code == 200:
            return response.json().get('ip')
    except Exception as e:
        write_log(f"Failed to retrieve public IP address: {e}")
    return None

# Update the Route 53 record
def update_route53_record(config, new_ip):
    client = boto3.Session(profile_name=config['aws_profile']).client('route53')
    domain_name = config['domain_name']
    record_name = config['record_name']
    hosted_zone_id = config['hosted_zone_id']

    try:
        response = client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': record_name + '.' + domain_name,
                            'Type': 'A',
                            'TTL': 300,
                            'ResourceRecords': [{'Value': new_ip}],
                        }
                    }
                ]
            }
        )
        write_log(f"Route 53 Record Updated: {response}")
    except Exception as e:
        write_log(f"Failed to update Route 53 record: {e}")

if __name__ == "__main__":
    config = load_config('./config.json')
    open_log(config['logfilename'])
    write_log("Starting Public IP Update")
    if config:
        current_ip = get_current_public_ip()
        if current_ip !=config['current_ip']:
            if current_ip:
                update_route53_record(config, current_ip)
                config['current_ip'] = current_ip
                with open('./config.json', 'w') as file:
                    json.dump(config, file)
                    
        else:
            write_log("IP address has not changed.")
    write_log("Public IP Update Complete")
