import os
import time
import json
import boto3
from botocore import exceptions as botoexcept
import string
import random
import threading
import sys
import values
import shutil
from getpass import getpass

os.system("cls")
def strgen(size=34, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False

print("\033[42mPlaybox CLI V1.0\033[0m")
while True:
    cinput = input("$ ")
    try:
        command, args = cinput.split(" ", 1)
    except ValueError:
        command = cinput
    if command.lower() == "ip":
        try:
            with open(f"boxes/{args}/box.json") as f:
                boxdata = json.load(f)
            ip = boxdata["ipadr"]
            print(f"\033[42m{args}\033[0m IP address: {ip}")
        except FileNotFoundError:
            print(f"\033[91mBox '{args}' doesnt exist\033[0m")
        except NameError:
            print(f"\033[91minvalid number of arguments\033[0m")

    elif command.lower() == "list":
       print([name for name in os.listdir("boxes") if os.path.isdir(os.path.join("boxes", name))])

    elif command.lower() == "session":
        try:
            with open(f"boxes/{args}/box.json") as file:
                boxdata = json.load(file)
            ip = boxdata["ipadr"]
            ssh_session = f'ssh -o StrictHostKeyChecking=no -T -t -t -i "boxes/{args}/key.pem" ubuntu@{ip} "tmux attach-session -t server01"'
            os.system(ssh_session)
        except FileNotFoundError:
            print(f"\033[91mBox '{args}' doesnt exist\033[0m")
        except NameError:
            print(f"\033[91minvalid number of arguments\033[0m")

    elif command.lower() == "upload":
        try:
            BoxName, FilePath = args.split(" ", 1)
            with open(f"boxes/{BoxName}/box.json") as file:
                boxdata = json.load(file)
            ip = boxdata["ipadr"]
            scp_session = f'scp -o StrictHostKeyChecking=no -i "boxes/{BoxName}/key.pem" {FilePath} ubuntu@{ip}:/home/ubuntu/server01'
            os.system(scp_session)
        except FileNotFoundError:
            print(f"\033[91mBox '{BoxName}' doesnt exist\033[0m")
            continue
        except ValueError:
            print(f"\033[91mInvalid number of arguments\033[0m")
            continue
        except NameError:
            print(f"\033[91mInvalid number of arguments\033[0m")

    elif command.lower() == "kill":
        BoxName = args
        invalidboxname = os.path.isdir(f"boxes/{args}")

        if invalidboxname == False:
            print(f"\033[91mBox '{args}' doesnt exist\033[0m")
            continue

        YorN = input(f'\033[97;41mWARNING, YOUR ABOUT TO DELETE "{args}". KILLING A BOX WILL DELETE EVERYING AND SHUT DONW THE SERVER. ARE YOU SURE (Y/N)\033[0m ').lower()

        if YorN == "n":
            print("Canceling...")
            continue
        elif YorN == 'y':
            session = boto3.session.Session()

            ec2 = session.client(
                service_name="ec2",
                aws_access_key_id=values.aws_access_key_id,
                aws_secret_access_key=values.aws_secret_access_key,
                region_name=values.region_name
            )

            with open(f"boxes/{BoxName}/box.json", "r") as f:
                boxdata = json.load(f)

            InstanceId = boxdata["instanceid"]
            try:
                response = ec2.terminate_instances(
                    InstanceIds=[InstanceId]
                )
            except:
                print("\033[91mError deleting. Deleteing box data anyways. You might have to delete the EC2 instance manually.\033[0m")

            shutil.rmtree(f'boxes/{BoxName}')
            print(f"The deed is done. {BoxName} has been fully deleted")
            continue
        else:
            print("Recived invalid input. Canceling...")
            continue

    # Syntax: create <Box Name> <Instance Type> <Server Type>
    # Box Name: Must be unique.
    # Instance Type: Must be a ARM type architecture (i.e. t4g.large).
    # Server Type: Must be ether Vanilla or Spigot. More coming soon.
    elif command.lower() == "create":
        try:
            BoxName, InstanceType, ServerType = args.split(" ", 2)
        except (NameError, ValueError) as e:
            print(f"\033[91mInvalid number of arguments\033[0m")
            continue
        InvalidBoxName = os.path.isdir(f"boxes/{BoxName}")

        if InvalidBoxName != False:
            print(f"\033[91mBox '{BoxName}' already exists\033[0m")
            continue

        session = boto3.session.Session()

        ec2 = session.client(
            service_name="ec2",
            aws_access_key_id=values.aws_access_key_id,
            aws_secret_access_key=values.aws_secret_access_key,
            region_name=values.region_name
        )

        keyname = strgen()

        keyresponse = ec2.create_key_pair(
            KeyName=keyname,
        )

        os.mkdir(f"boxes/{BoxName}")

        with open(f"boxes/{BoxName}/key.pem", "w+") as keyfile:
            keyfile.write(keyresponse['KeyMaterial'])
            keyfile.close()
        try:
            instance = ec2.run_instances(
                ImageId='ami-0acb327475c6fd498',      # Replace with the desired AMI ID
                InstanceType=InstanceType,
                MinCount=1,
                MaxCount=1,
                KeyName=keyname,
                NetworkInterfaces=[
                    {
                        'DeviceIndex': 0,
                        'AssociatePublicIpAddress': True,
                    }
                ]
            )
        except botoexcept.ClientError:
            print(f"\033[91mInstance '{InstanceType}' doesn't exist\033[0m")
            shutil.rmtree(f'boxes/{BoxName}')
            continue


        print("Waiting for instance to start running...")
        with Spinner():

            InstanceId = instance["Instances"][0]["InstanceId"]

            state = "pending"

            while state == "pending":
                descinstance = ec2.describe_instances(
                    InstanceIds=[InstanceId]
                )
                time.sleep(2)

                state = descinstance["Reservations"][0]["Instances"][0]["State"]["Name"]

            time.sleep(15)

            ip = descinstance["Reservations"][0]["Instances"][0]["PublicIpAddress"]
            with open(f"boxes/{BoxName}/box.json", "w+") as boxdata:
                boxdata.write('{ "ipadr": "' + ip + '", "instanceid": "' + InstanceId + '" }')
                boxdata.close()

            print("Successfully launched EC2 instance")
        if ServerType.lower() == "vanilla":
            upload_setup = f'scp -o StrictHostKeyChecking=no -i "boxes/{BoxName}/key.pem" scripts/vanillaserver.sh ubuntu@{ip}:/home/ubuntu'
            ssh_session = f'ssh -o StrictHostKeyChecking=no -T -t -t -i "boxes/{BoxName}/key.pem" ubuntu@{ip} "sh vanillaserver.sh"'

        elif ServerType.lower() == "spigot":
            upload_setup = f'scp -o StrictHostKeyChecking=no -i "boxes/{BoxName}/key.pem" scripts/spigotserver.sh ubuntu@{ip}:/home/ubuntu'
            ssh_session = f'ssh -o StrictHostKeyChecking=no -T -t -t -i "boxes/{BoxName}/key.pem" ubuntu@{ip} "sh spigotserver.sh"'

        else:
            print(f"\033[91m'{ServerType}' is a invalid server type\033[0m")
            shutil.rmtree(f'boxes/{BoxName}')
            continue

        os.system(upload_setup)

        os.system(ssh_session)
    else:
        print(f"\033[91m{command} is a invalid command\033[0m")
