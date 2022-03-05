import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312 import cvm_client, models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cmdb.models import ServerData


class InstanceData(APIView):

    def __init__(self):
        self.cloud = 'tencent'

    def instance_connect(self,zone):

        cred = credential.Credential("", "")

        httpProfile = HttpProfile()
        httpProfile.endpoint = "cvm.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cvm_client.CvmClient(cred, zone, clientProfile)
        req = models.DescribeInstancesRequest()
        return client,req

    def instance_total(self,req,client):
        params = {}
        req.from_json_string(json.dumps(params))
        resp = client.DescribeInstances(req)
        res_dict = json.loads(resp.to_json_string())
        total_count = res_dict['TotalCount']
        return total_count



    def instance_list(self,req,client,count):
        init_set_limit = 20
        # init_set_offset = 20

        total_page = count // init_set_limit
        instance_list  = []

        for i in range(total_page+1):
            offset_first = i * init_set_limit
            params = {
            "Offset": offset_first,
            "Limit": init_set_limit
            }
            req.from_json_string(json.dumps(params))
            resp = client.DescribeInstances(req)
            res_dict = json.loads(resp.to_json_string())
            instance = res_dict['InstanceSet']
            instance_list.extend(instance)
        return instance_list

    def instance_list_filter(self,instance_list,zone):
        new_instance_list =[]
        instacne_field = {'InstanceState','OsName','CreatedTime','ExpiredTime','Memory','IPv6Addresses','CPU','PublicIpAddresses','Tags',
        'InstanceId','PrivateIpAddresses','InstanceName','InstanceState'}
        for instance in instance_list:
            new_instance_dict={key: value for key, value in instance.items() if key in instacne_field}
            if  new_instance_dict['IPv6Addresses'] is not None:
                new_instance_dict['IPv6Addresses'] = new_instance_dict['IPv6Addresses'][0]
            if  new_instance_dict['PrivateIpAddresses'] is not None:
                new_instance_dict['PrivateIpAddresses'] = new_instance_dict['PrivateIpAddresses'][0]
            if  new_instance_dict['PublicIpAddresses'] is not None:
                new_instance_dict['PublicIpAddresses'] = new_instance_dict['PublicIpAddresses'][0]
            if new_instance_dict['Tags'] is not None:
                temp_tags=[]
                for tag in new_instance_dict['Tags']:
                    temp_tags.append({tag['Key']: tag['Value']})
                new_instance_dict['Tags']=temp_tags
            new_instance_dict['Zone'] = zone
            new_instance_dict['Cloud'] = self.cloud
            new_instance_list.append(new_instance_dict)
        return new_instance_list

    def update_create_server(self,new_server_list_data):
        for update_instance in new_server_list_data:
            obj, created = ServerData.objects.update_or_create(
                name=update_instance['InstanceName'],
                defaults={
                    "ipv6": update_instance['IPv6Addresses'], "pub_ip": update_instance['PublicIpAddresses'],
                    "status": update_instance['InstanceState'], "os": update_instance['OsName'],
                    "create_date": update_instance['CreatedTime'], "expired_date": update_instance['ExpiredTime'],
                    "zone": update_instance['Zone'], "cloud": update_instance['Cloud'],
                    "memory": update_instance['Memory'], "cpu": update_instance['CPU'],
                    "name": update_instance['InstanceName'], "instance_id": update_instance['InstanceId'],
                    "ipv4": update_instance['PrivateIpAddresses'], "tags": update_instance['Tags']
                }
            )


    def get(self,request):
        zones=["ap-shanghai-fsi","ap-shenzhen-fsi"]   #要获取的数据在腾讯云的分区
        total = 0
        for zone in zones:
            client,req = self.instance_connect(zone=zone)
            instance_total = self.instance_total(client=client,req=req)
            new_servers_list = self.instance_list(req=req,client=client,count=instance_total)
            new_server_list_data = self.instance_list_filter(new_servers_list,zone)
            self.update_create_server(new_server_list_data)
            total = total + instance_total
        return Response(data={"count":total},status=status.HTTP_200_OK)
