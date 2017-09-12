'''
This program creates snapshots for all tagged volumes in a aws region specified with the --region option

'''

import boto3
import pprint
import datetime
import argparse

argparser = argparse.ArgumentParser(description='Creating snapshots for all EC2 instance tagged volumes in a region')
argparser.add_argument('--region', help='AWS region name')

args = argparser.parse_args()

if not args.region:
    print('You must specify a region')
    exit()

ec2 = boto3.resource('ec2',region_name=args.region)
snapshots = ec2.snapshots.all()
volumes = ec2.volumes.all()

now = datetime.datetime.utcnow() # timezone-aware datetime.utcnow()
today = datetime.datetime(now.year, now.month, now.day, tzinfo=datetime.timezone.utc) # midnight

#print(today)
'''
for res in snapshots:
    if res.tags:
        #print(res.tags)
        if res.start_time < today:
            print(res.tags,res.start_time,res.meta)
        #print(type(res.start_time.tzinfo))
'''

volume_ids = []
for vol in volumes:
    if vol.tags:
        print(vol.tags[0]['Value'],vol.id)
        volume_ids.append(vol.id)

print(volume_ids)


'''
#snapshot info
#print('snaps')
for snaps in snapshots:
    if snaps.start_time > datetime.datetime(2017,9,10, tzinfo=datetime.timezone.utc) and snaps.tags:
        print(snaps.id,"-",snaps.start_time, "-",snaps.tags ,snaps.volume.id, "\n")
'''


# In[69]:

# create specific volume snapshot
#vol_id = ['vol-059b06737467aa987']

for ent in volumes.filter(Filters=[{'Name': 'volume-id', 'Values': volume_ids}]).all():
    #print(ent.tags[0]['Value'])
    snapshot_name = 'BU '+str(datetime.datetime.now().day)+'/'+ str(datetime.datetime.now().month)+'/'+str(datetime.datetime.now().year)+' '+ ent.tags[0]['Value']
    print(snapshot_name)
    #snapshot = ec2.create_snapshot(VolumeId=ent.volume_id, Description='created by backup script')
    #snapshot.create_tags(Resources=[snapshot.id], Tags=[{'Key': 'Name', 'Value': snapshot_name}])
    

