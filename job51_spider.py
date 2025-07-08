import re
import time
import math
import execjs
import urllib.parse

import scrapy
from scrapy import Request
from job51.items import Job51Item

class Job51SpiderSpider(scrapy.Spider):
    name = "job51_spider"
    allowed_domains = ["51job.com"]
    start_urls = ["https://we.51job.com/api/job/search-pc"]

    cookies = {
        'partner': 'SEM_pcbingpz_02',
        'guid': '98235d6c307944cb400705c9a32ec965',
        'ps': 'needv%3D0',
        '51job': 'cuid%3D212242951%26%7C%26cusername%3D%252FOy0gqSoqcKKQZboM3bFsNHfgTi47DfKAkac2F2wu2M%253D%26%7C%26cpassword%3D%26%7C%26cname%3DfZIrhZdFS7ODWaMsvBjjtw%253D%253D%26%7C%26cemail%3D%26%7C%26cemailstatus%3D0%26%7C%26cnickname%3D%26%7C%26ccry%3D.0WGSQvIdMuBc%26%7C%26cconfirmkey%3D%25241%2524lo0blpuj%2524C8773.AE832Oq4pXbjDD9.%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3D%25241%2524x9l.i5Si%2524iStczijPEJIPjAV9gjfiQ0%26%7C%26to%3D029ed5368643c311a00ee4e1f94223da6831ce77%26%7C%26',
        'sensor': 'createDate%3D2022-06-16%26%7C%26identityType%3D1',
        'acw_tc': 'ac11000117480945839377259e0092ebd97de0adc181c8a98898562f731679',
        'sajssdk_2015_cross_new_user': '1',
        'slife': 'lowbrowser%3Dnot%26%7C%26lastlogindate%3D20250524%26%7C%26securetime%3DADwDNwBiUT1SMFFmW2RbNVJoUWA%253D',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22212242951%22%2C%22first_id%22%3A%22197028e4d5234-04741870ef5acfc-4c657b58-1327104-197028e4d53a7e%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk3MDI4ZTRkNTIzNC0wNDc0MTg3MGVmNWFjZmMtNGM2NTdiNTgtMTMyNzEwNC0xOTcwMjhlNGQ1M2E3ZSIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjIxMjI0Mjk1MSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22212242951%22%7D%2C%22%24device_id%22%3A%22197028e4d5234-04741870ef5acfc-4c657b58-1327104-197028e4d53a7e%22%7D',
        'acw_sc__v2': '6831ce916d612ea804381f08cbeb2e0d03ec4907',
        'nsearch': 'jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D',
        'search': 'jobarea%7E%60%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21',
        'JSESSIONID': 'BB285BC1D005E53C195E84C5A686EE38',
        'ssxmod_itna': 'eqjxyDBCGQD=d4Bc4B4DKS3tQ=mPYvKG8iKFFQ+8jW5DBk7Q4iNDnD8x7YDv+0Z7O+pPwjQ8ndwDIOuApezEA2LPvFeu4nHFBUo4GLDmKDyFfr4GGBxBYDQxAYDGDDPDorKD1D3qDkD7rtlBLNSDi3DbrtDf4DmDGYg7qDgDYQDGuK2D7QDILtdDDNdY=eDefhxWlr2ICX=ukE557DgD0UtxBLrRc4gUWHz6Y05ppFesh=DzTODtLXZemj=EAUxZq2oARhYe4+Yb8GpKDxrn+GK9GC4YDxb8iPqjGGWFGDdbsGUVR4DG8DdANoG4xD==',
        'ssxmod_itna2': 'eqjxyDBCGQD=d4Bc4B4DKS3tQ=mPYvKG8iKFFQ+8jQD8u1APGXrLxGa8QRk8YKD7IOD8OriCYqtmAxCdnOEYx1B3G7FqLoHQuxtdCuSQC0xcDhLE7qtotYH0UxTTmflOPW5XhyCec3YEQT6DM44cKrjxWjjhmxjPuoQFRkRmtkh0zk2=hfhuifQifoblY4o=Tkmr7xLyjDhmWfdMm1Gnt1eA7QEr3fxmmZWSb3oq3SmYdi37ydU8al=p7bN7u2D43+0I+wW+KgNqRZjyDEUwWWY6xeEyWQYmsTd0Pqc4s8ElmKHQv2=hAwQhXPnflAIWa0qKITCKRBNA0iqjDboeBxPuBv00wPZxCiDq=qiDpPCvhYAvCqCD4t0Uo8fRZDcQj/G3ypL8cXcYYGhNTmPfWIuQDb7f8aicirAGDqW=gjvhadIUvdFeFEKRaeqBoQK=OOmMCn=E5ZrmXK0Txvm46mxpyncmrpye5IYHpWUK=Lmo=QFtZYnmpK9+3KFawAPczfaPp+YdvCfk=7vDERSeCtpaSNtpwbFuY+wFaG98n+lPp13mIBw3LC2eiZmh2e38PBgHzrLbkpBe3xwM1OQliAfzeGyPYaIUCd9eoi6i1Gj=hM=hBGg4DQKA0cXGnrAkTPA96W/ltbtHz4q3i4wC4x+cUesSEZmNRgsRtjb2e+N0+810muXiWstifQ4WrMOxN4vPQNrx8PyDDjKDYFA0350/CKIiilDgrH0qVwpBPvy5jN17Y448q4i37r5mPlyVQe7xxQ44D===',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'account-id': '212242951',
        'cache-control': 'no-cache',
        'from-domain': '51job_web',
        'partner': 'SEM_pcbingpz_02',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'property': '%7B%22partner%22%3A%22SEM_pcbingpz_02%22%2C%22webId%22%3A2%2C%22fromdomain%22%3A%2251job_web%22%2C%22frompageUrl%22%3A%22https%3A%2F%2Fwe.51job.com%2F%22%2C%22pageUrl%22%3A%22https%3A%2F%2Fwe.51job.com%2Fpc%2Fsearch%3Fkeyword%3Dpython%22%2C%22identityType%22%3A%22%E8%81%8C%E5%9C%BA%E4%BA%BA%22%2C%22userType%22%3A%22%E8%80%81%E7%94%A8%E6%88%B7%22%2C%22isLogin%22%3A%22%E6%98%AF%22%2C%22accountid%22%3A%22212242951%22%2C%22keywordType%22%3A%22%E8%BE%93%E5%85%A5%E5%90%8E%E9%80%89%E6%8B%A9%E8%81%94%E6%83%B3%E8%AF%8D%22%7D',
        'referer': 'https://we.51job.com/pc/search?keyword=python',
        'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sign': 'c26c29ec647183ac02ac8125ae2e6a0c3c9336ca2effe8d0dd9066f8bd342994',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'user-token': '029ed5368643c311a00ee4e1f94223da6831ce77',
        'uuid': '98235d6c307944cb400705c9a32ec965',
        # 'cookie': 'partner=SEM_pcbingpz_02; guid=98235d6c307944cb400705c9a32ec965; ps=needv%3D0; 51job=cuid%3D212242951%26%7C%26cusername%3D%252FOy0gqSoqcKKQZboM3bFsNHfgTi47DfKAkac2F2wu2M%253D%26%7C%26cpassword%3D%26%7C%26cname%3DfZIrhZdFS7ODWaMsvBjjtw%253D%253D%26%7C%26cemail%3D%26%7C%26cemailstatus%3D0%26%7C%26cnickname%3D%26%7C%26ccry%3D.0WGSQvIdMuBc%26%7C%26cconfirmkey%3D%25241%2524lo0blpuj%2524C8773.AE832Oq4pXbjDD9.%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3D%25241%2524x9l.i5Si%2524iStczijPEJIPjAV9gjfiQ0%26%7C%26to%3D029ed5368643c311a00ee4e1f94223da6831ce77%26%7C%26; sensor=createDate%3D2022-06-16%26%7C%26identityType%3D1; acw_tc=ac11000117480945839377259e0092ebd97de0adc181c8a98898562f731679; sajssdk_2015_cross_new_user=1; slife=lowbrowser%3Dnot%26%7C%26lastlogindate%3D20250524%26%7C%26securetime%3DADwDNwBiUT1SMFFmW2RbNVJoUWA%253D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22212242951%22%2C%22first_id%22%3A%22197028e4d5234-04741870ef5acfc-4c657b58-1327104-197028e4d53a7e%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk3MDI4ZTRkNTIzNC0wNDc0MTg3MGVmNWFjZmMtNGM2NTdiNTgtMTMyNzEwNC0xOTcwMjhlNGQ1M2E3ZSIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjIxMjI0Mjk1MSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22212242951%22%7D%2C%22%24device_id%22%3A%22197028e4d5234-04741870ef5acfc-4c657b58-1327104-197028e4d53a7e%22%7D; acw_sc__v2=6831ce916d612ea804381f08cbeb2e0d03ec4907; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; JSESSIONID=BB285BC1D005E53C195E84C5A686EE38; ssxmod_itna=eqjxyDBCGQD=d4Bc4B4DKS3tQ=mPYvKG8iKFFQ+8jW5DBk7Q4iNDnD8x7YDv+0Z7O+pPwjQ8ndwDIOuApezEA2LPvFeu4nHFBUo4GLDmKDyFfr4GGBxBYDQxAYDGDDPDorKD1D3qDkD7rtlBLNSDi3DbrtDf4DmDGYg7qDgDYQDGuK2D7QDILtdDDNdY=eDefhxWlr2ICX=ukE557DgD0UtxBLrRc4gUWHz6Y05ppFesh=DzTODtLXZemj=EAUxZq2oARhYe4+Yb8GpKDxrn+GK9GC4YDxb8iPqjGGWFGDdbsGUVR4DG8DdANoG4xD==; ssxmod_itna2=eqjxyDBCGQD=d4Bc4B4DKS3tQ=mPYvKG8iKFFQ+8jQD8u1APGXrLxGa8QRk8YKD7IOD8OriCYqtmAxCdnOEYx1B3G7FqLoHQuxtdCuSQC0xcDhLE7qtotYH0UxTTmflOPW5XhyCec3YEQT6DM44cKrjxWjjhmxjPuoQFRkRmtkh0zk2=hfhuifQifoblY4o=Tkmr7xLyjDhmWfdMm1Gnt1eA7QEr3fxmmZWSb3oq3SmYdi37ydU8al=p7bN7u2D43+0I+wW+KgNqRZjyDEUwWWY6xeEyWQYmsTd0Pqc4s8ElmKHQv2=hAwQhXPnflAIWa0qKITCKRBNA0iqjDboeBxPuBv00wPZxCiDq=qiDpPCvhYAvCqCD4t0Uo8fRZDcQj/G3ypL8cXcYYGhNTmPfWIuQDb7f8aicirAGDqW=gjvhadIUvdFeFEKRaeqBoQK=OOmMCn=E5ZrmXK0Txvm46mxpyncmrpye5IYHpWUK=Lmo=QFtZYnmpK9+3KFawAPczfaPp+YdvCfk=7vDERSeCtpaSNtpwbFuY+wFaG98n+lPp13mIBw3LC2eiZmh2e38PBgHzrLbkpBe3xwM1OQliAfzeGyPYaIUCd9eoi6i1Gj=hM=hBGg4DQKA0cXGnrAkTPA96W/ltbtHz4q3i4wC4x+cUesSEZmNRgsRtjb2e+N0+810muXiWstifQ4WrMOxN4vPQNrx8PyDDjKDYFA0350/CKIiilDgrH0qVwpBPvy5jN17Y448q4i37r5mPlyVQe7xxQ44D===',
    }

    params_template = {
        'api_key': '51job',
        'timestamp': '1748094703',
        'keyword': 'python',
        'searchType': '2',
        'function': '',
        'industry': '',
        'jobArea': '000000',
        'jobArea2': '',
        'landmark': '',
        'metro': '',
        'salary': '',
        'workYear': '',
        'degree': '',
        'companyType': '',
        'companySize': '',
        'jobType': '',
        'issueDate': '',
        'sortType': '0',
        'pageNum': '2',
        'requestId': '',
        'pageSize': '20',
        'source': '1',
        'accountId': '212242951',
        'pageCode': 'sou|sou|soulb',
        'scene': '7',
    }

    # JS执行上下文（单例）
    js_ctx = None

    def start_requests(self):
        # 初始化请求参数
        params = self.params_template.copy()
        params['timestamp'] = str(int(time.time()))  # 秒级时间戳
        params['pageNum'] = '1'  # 初始页码

        # 发送初始请求
        yield Request(
            url='https://we.51job.com/api/job/search-pc',
            method='GET',
            cookies=self.cookies,
            headers=self.headers,
            callback=self.parse_first_response,
            meta={'params': params, 'page': 1},
            dont_filter=True
        )

    def parse_first_response(self, response):
        """处理首次响应，提取arg1并计算acw_sc__v2"""
        # 提取arg1
        arg1 = re.search(r"var\s+arg1\s*=\s*'([^']+)'", response.text)
        if not arg1:
            self.logger.error("未找到arg1参数")
            return

        arg1 = arg1.group(1)
        self.logger.info(f"成功获取arg1: {arg1}")

        # 初始化JS执行环境
        if not self.js_ctx:
            with open('job51/spiders/demo26.js', 'r', encoding='utf-8') as f:
                self.js_ctx = execjs.compile(f.read())

        # 计算acw_sc__v2
        acw_sc__v2 = self.js_ctx.call('get_acw_sc__v2', arg1)
        self.logger.info(f"计算得到acw_sc__v2: {acw_sc__v2}")

        # 更新cookies
        self.cookies['acw_sc__v2'] = acw_sc__v2

        # 开始爬取第1页
        meta = response.meta
        yield self.build_page_request(meta['params'], meta['page'])

        # 继续爬取第2-10页
        for page in range(2, 11):
            params = meta['params'].copy()
            params['pageNum'] = str(page)
            yield self.build_page_request(params, page)

    def build_page_request(self, params, page):
        """构建分页请求"""
        # 计算毫秒级时间戳
        timestamp_ms = str(int(time.time() * 1000))
        params['timestamp'] = timestamp_ms

        # 构建参数字符串
        param_str = urllib.parse.urlencode(params)
        full_url = f"/api/job/search-pc?{param_str}"

        # 计算sign
        sign = self.js_ctx.call('get_sign', full_url)

        # 更新headers
        headers = self.headers.copy()
        headers['sign'] = sign

        return Request(
            url='https://we.51job.com/api/job/search-pc',
            method='GET',
            cookies=self.cookies,
            headers=headers,
            callback=self.parse_job_page,
            meta={'page': page},
            dont_filter=True,
            cb_kwargs={'params': params}
        )

    def parse_job_page(self, response, params):
        """解析职位页面"""
        page = response.meta['page']
        self.logger.info(f"正在解析第 {page} 页数据")

        data = response.json()
        items = data.get('resultbody', {}).get('job', {}).get('items', [])

        for item in items:
            job_item = Job51Item()
            job_item['jobName'] = item.get('jobName', '')
            job_item['jobArea'] = item.get('jobAreaString', '')
            job_item['Salary'] = item.get('provideSalaryString', '')
            job_item['fullCompanyName'] = item.get('fullCompanyName', '')
            job_item['updateDateTime'] = item.get('updateDateTime', '')
            job_item['jobHref'] = item.get('jobHref', '')
            job_item['jobDescribe'] = item.get('jobDescribe', '').replace('\n', ' ')
            job_item['companyHref'] = item.get('companyHref', '')
            yield job_item


