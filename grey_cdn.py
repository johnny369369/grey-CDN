#!/usr/bin/env python
# ! coding=utf-8
import requests, json,sys,os
import pysnooper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylog import mylogger
from Params import Params
from grey_api import Grey_operating
# @pysnooper.snoop()

class Grey_menu():

    def __init__(self,token=None):
        self.init_class_params = Params()
        self.token = token
        self.init_calss = Grey_operating(token=self.token)

    def add_website_whitelist(self):
        website_uid = self.website_info() 
        ipList_input = input('要添加的IP,多个以逗号分隔:').split(',')
        result = self.init_calss.add_website_whiteList(website_uid=website_uid,ipList=ipList_input)
        if result['response'] == 'success':
           print(f'{ipList_input}白名单添加到站点:{choose_site}成功!')
           mylogger.info(f'{ipList_input}添加到站点:{choose_site}')
        elif result['response'] == 'error':
           print(f'{ipList_input}白名单添加到站点:{choose_site}失败!!!')
           mylogger.error(f'{ipList_input}白名单添加到站点:{choose_site}失败!!!')
        else:
           print(result) 
           mylogger.warning(result)
        
    def refresh_cdn_grey(self):
        website_uid = self.website_info()
        result = self.init_calss.refresh_cdn(website_uid=website_uid)
        if result['response'] == 'success':
           print(f'=====GREY-CDN刷新成功====,返回信息为:{result}')
           mylogger.info(f'=====GREY-CDN刷新成功====,返回信息为:{result}')
        elif result['response'] == 'error':
           print(f'=====grey-CDN刷新失败:{result}')
           mylogger.error(f'=====grey-CDN刷新失败:{result}')
        else:
           print(result)
           mylogger.warning(result)

    def add_domain_to_grey(self):
        uid = self.website_info()
        domain_record_list= []
        if os.stat('./domain_list').st_size == 0:
           print('=====>>domain_list文件为空请检查===========================')
           mylogger.error('=====>>domain_list文件为空请检查===========================')
        with open('./domain_list', 'r',encoding='utf-8') as domain_file:
             for domain in domain_file.readlines():
                 domain_record_list.append(domain)
                 domain_record_list.append(f'*.{domain}')
        record_list = list(map(lambda x:x.strip(),domain_record_list))
        for domainR in record_list:
             result = self.init_calss.add_domain_to_grey(domain=domainR,uid=uid)
             if result['response'] == 'success':
                print(f'域名:{domainR}添加到灰域成功,返回信息为:{result}')
                mylogger.info(f'域名:{domainR}添加到灰域成功,返回信息为:{result}')
             elif result['response'] == 'error':
                print(f'域名:{domainR}添加到灰域失败,报错为:{result}')
                mylogger.error(f'域名:{domainR}添加到灰域失败,报错为:{result}')
             else:
                 print(result)
                 mylogger.warning(result)
   
    def get_website_info(self):
        get_site_result = self.init_calss.get_grey_site_list()
        if get_site_result['response'] == 'success':
            for site_info in get_site_result['result']:
                print('站点名:{:40} UID:{:60} 站点类型:{:25}'.format(site_info['name'],site_info['uid'],site_info['type']))
                mylogger.info('站点名:{:20} UID:{:50} 站点类型:{:20}'.format(site_info['name'],site_info['uid'],site_info['type']))
        elif result['response'] == 'error':
             print('站点信息查询失败:{}'.format(get_site_result['result']))
             mylogger.info('站点信息查询失败:{}'.format(get_site_result['result']))
        else:
            print(result)
            mylogger.warning(result)

    def upload_domainSsl_to_grey(self):
        #证书路径
        cert_path = 'your ssl dir'
        with open('./domain_list', 'r', encoding='utf-8') as domain_file:
             for domain in domain_file.read().splitlines():
                 domainKey = self.find(f'{domain}.key',cert_path)
                 domainCrt = self.find(f'{domain}.crt',cert_path)
                 with open(f'{domainKey}','r') as fkey:
                      domainkey = fkey.read()
                 with open(f'{domainCrt}','r') as fcrt:
                      domaincrt = fcrt.read()
                 result = self.init_calss.upload_domain_cert_to_grey(domaincrt=domaincrt,domainkey=domainkey)
                 if result['response'] == 'success':
                     print(f'域名:{domain},证书添加到灰域成功,返回信息为:{result}')
                     mylogger.info(f'域名:{domain},证书添加到灰域成功,返回信息为:{result}')
                 elif result['response'] == 'error':
                     print(f'域名:{domain},证书添加到灰域失败,报错为:{result}')
                     mylogger.error(f'域名:{domain},证书添加到灰域失败,报错为:{result}')
                 else:
                    print(result)
                    mylogger.warning(result)

    def website_info(self):
        website_list = self.init_calss.get_grey_site_list()
        website_dict = {}
        return_website = {}
        for i in website_list['result']:
            website_dict[i['name']] = i['uid']
        for k in enumerate(website_dict.keys()):
            n_str = str(k[0])
            return_website[n_str] = k[1]
        select_site = self.init_class_params.check_menu_dict(return_website,'你的站点')
        return website_dict[return_website[select_site]]

    def find(self,name,cert_path):
        for root, dirs, files in os.walk(cert_path):
            if name in files:
               return os.path.join(root,name)

    def oper_menu(self):
         operating_dict = {'1':'刷新CDN',
                           '2':'新增域名和上传证书',
                           '3':'上传域名证书',
                           '4':'获取站点信息',
                           '5':'添加站点白名单',
                           '6':'website'}
         select_operating = self.init_class_params.check_menu_dict(operating_dict,'你的操作')
         if select_operating == '1':
            self.refresh_cdn_grey()
         elif select_operating == '2':
            self.add_domain_to_grey()
            self.upload_domainSsl_to_grey()
         elif select_operating == '3':
            self.upload_domainSsl_to_grey()
         elif select_operating == '4':
            self.get_website_info()
         elif select_operating == '5':
            self.add_website_whitelist()
 
if __name__ == '__main__':
   init_params = Params()
   product_dict = {'1': 'product', '2': 'product'}
   grey_token_dict = {'product_1': 'your token',
                 'product_2': 'your token'}
   producu_select = init_params.check_menu_dict(product_dict,'你的操作')
   product_token = product_dict[producu_select]
   token = grey_token_dict[product_token]
   init_gray = Grey_menu(token=token)
   init_gray.oper_menu()
