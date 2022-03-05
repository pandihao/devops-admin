import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cdn.v20180606 import cdn_client, models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CdnConnect(object):

    def instance_connect(self):
        cred = credential.Credential("", "")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cdn.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cdn_client.CdnClient(cred, "", clientProfile)
        return client

class UrlFlush(APIView,CdnConnect):

    def url_flush(self,params,client):
        req = models.PurgeUrlsCacheRequest()
        params = {
            "Urls": params
        }
        req.from_json_string(json.dumps(params))
        resp = client.PurgeUrlsCache(req)
        return resp.to_json_string()

    def post(self, request, *args, **kwargs):
        urls = request.data
        client = self.instance_connect()
        try:
            result=self.url_flush(params=urls,client=client)
            return  Response(status=status.HTTP_200_OK,data=result)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DirFlush(APIView,CdnConnect):

    def dir_flush(self,params,client):
        req = models.PurgePathCacheRequest()
        print(params['paths'])
        params = {
            "Paths": params['paths'],
            "FlushType": params['type']
        }
        req.from_json_string(json.dumps(params))
        resp = client.PurgePathCache(req)
        return resp.to_json_string()

    def post(self, request, *args, **kwargs):
        params = request.data
        client = self.instance_connect()
        try:
            result=self.dir_flush(params=params,client=client)
            return  Response(status=status.HTTP_200_OK,data=result)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UrlPreHeat(APIView,CdnConnect):

    def url_preheat(self,params,client):
        req = models.PushUrlsCacheRequest()
        print(params)
        params = {
            "Urls": params['urls'],
            "Area": params['area']
        }
        req.from_json_string(json.dumps(params))
        resp = client.PushUrlsCache(req)
        return resp.to_json_string()

    def post(self, request, *args, **kwargs):
        params = request.data
        client = self.instance_connect()
        try:
            result=self.url_preheat(params=params,client=client)
            return  Response(status=status.HTTP_200_OK,data=result)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class History(APIView,CdnConnect):

    def operator_history(self,req_params,client):
        params = {
            "StartTime": req_params['starttime'],
            "EndTime":  req_params['endtime'],
            "PurgeType": req_params['type'],
        }
        if 'keyword' in req_params and req_params['keyword'] != '':
            params['Keyword'] = req_params['keyword']

        if params['PurgeType'] != 'preheat':

            req = models.DescribePurgeTasksRequest()
            req.from_json_string(json.dumps(params))
            resp = client.DescribePurgeTasks(req)
        else:
            req = models.DescribePushTasksRequest()
            req.from_json_string(json.dumps(params))
            resp = client.DescribePushTasks(req)

        return resp.to_json_string()

    def post(self, request, *args, **kwargs):
        params = request.data
        client = self.instance_connect()
        try:
            result=self.operator_history(req_params=params,client=client)
            return  Response(status=status.HTTP_200_OK,data=result)
        except Exception as e:
            print(repr(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,data={"error":repr(e)})





