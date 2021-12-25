#!/usr/bin/env python
# ! coding=utf-8
import requests, json,sys,os
import pysnooper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylog import mylogger
from Params import Params
# @pysnooper.snoop()

class Grey_operating():

      def __init__(self,token=None):
          self.grey_token = token
          self.grey_host = 'http://api2.greypanel.com'
          self.header = {}
          self.header['greycdn-token'] = self.grey_token
          self.header['User-Agent'] = "Greypanel-CDN-API-V2"
          self.header['Content-Type'] = "application/json"
          self.params = Params()

      def add_domain_to_grey(self,domain=None,uid=None):
          '''添加域名到灰域
             从外部传入test.com,*.test.com域名逐一添加
             接口/api/v1/domain/create?uid=
             必选参数domain uid
          '''
          return_data = {}
          try:
              data = {'displayName':domain,
                       'sslEnable':'0'}
              api_url = f'{self.grey_host}/api/v1/domain/create?uid={uid}'
              response = requests.post(url=api_url,data=json.dumps(data),headers=self.header).json()
          except Exception as e:
              return_data['response'] = 'error'
              return_data['message'] = e.__str__()
              return  return_data
          else:
              return response

      def upload_domain_cert_to_grey(self,domaincrt=None,domainkey=None):
          '''
          添加域名证书到灰域
          接口/api/v1/ssl/upload-cert
          必选参数 sslCrt sslKey sslAutoEnable sslForceEnable
          '''
          return_data = {}
          api_url = f'{self.grey_host}/api/v1/ssl/upload-cert'
          try:
              data = {'sslCrt':domaincrt,"sslKey":domainkey,"sslAutoEnable": '1',"sslForceEnable": '0' }
              response = requests.post(url=api_url,data=json.dumps(data),headers=self.header).json()
          except Exception as e:
              return_data['response'] = 'error'
              return_data['message'] = e.__str__()
              return  return_data
          else:
              return  response

      def get_grey_site_list(self):
          '''
          获取灰域站点列表 返回站点信息
          接口/api/v1/site/list/all
          必选参数token
          '''
          return_data = {}
          try:
              api_url = f'{self.grey_host}/api/v1/site/list/all'
              response = requests.post(url=api_url,headers=self.header).json()
          except Exception as e:
                 return_data['response'] = 'error'
                 return_data['message'] = e.__str__()
                 return return_data
          else:
              return  response

      def refresh_cdn(self,website_uid=None):
          '''
          刷新灰域CDN
          接口api/v1/cache/purge/by-site?uid=
          必选参数uid
          先获取站点列表信息 然后把获取的信息存入字典 在字典获取到站点的UID结合URL POST发出请求
          '''
          return_data = {}
          try:
              api_url = '{}/api/v1/cache/purge/by-site?uid={}'.format(self.grey_host,website_uid)
              response = requests.post(url=api_url,headers=self.header).json()
          except Exception as e:
              return_data['response'] = 'error'
              return_data['message'] = e.__str__()
              return  return_data
          else:
              return response

      def add_website_whiteList(self,website_uid=None,ipList=None):
          '''
          添加灰域站点白名单    
          website=站点名
          iplist外部传入IP列表
          接口/api/v1/site/waf/save-ip-white-list?uid=uid
          ''' 
          return_data = {}
          data = ipList
          try:
             api_url = '{}/api/v1/site/waf/save-ip-white-list?uid={}'.format(self.grey_host,website_uid)
             print(api_url)
             response = requests.post(url=api_url,data=json.dumps(data),headers=self.header).json()
          except Exception as e:
              return_data['response'] = 'error'
              return_data['message'] = e.__str__()
              return  return_data
          else:
              return response
