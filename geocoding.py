import json
import requests
from util.utils import imagine_address

"""
You can get information for a location in any country/region by setting one or more of the parameters in the following URL.
http://dev.virtualearth.net/REST/v1/Locations?countryRegion={countryRegion}&adminDistrict={adminDistrict}&locality={locality}&postalCode={postalCode}&addressLine={addressLine}&userLocation={userLocation}&userIp={userIp}&usermapView={usermapView}&includeNeighborhood={includeNeighborhood}&maxResults={maxResults}&key={BingMapsKey}
Example that return a xml result:
http://dev.virtualearth.net/REST/v1/Locations/US/WA/98052/Redmond/1%20Microsoft%20Way?o=xml&key={BingMapsKey}
Example that return json result (the o (output) parameter is not set.):
http://dev.virtualearth.net/REST/v1/Locations/US/WA/98052/Redmond/1%20Microsoft%20Way?&key={BingMapsKey}
"""

# 定义一个函数，用于解析url返回的json数据


def geocode_chn(full_address = None,countryRegion=None,
                adminDistrict=None,
                locality=None,
                postalCode=None,
                addressLine=None,
                userLocation=None,
                userIp=None,
                usermapView=None,
                includeNeighborhood=None,
                maxResults=None,
                BingMapsKey=None):
    if BingMapsKey is None:
        return {"Error in Bing Maps request. Status: api key required."}
    
    """
        {'province': '广东省', 'city': '佛山市', 'county': '南海区', 'detail': '南海万科广场', 
        'full_location': '广东省佛山市南海区南海万科广场', 'orig_location': '南海区南海万科广场'}
    """

    if full_address is not None:
        address_dict = imagine_address(full_address)
        countryRegion="CHN"
        adminDistrict=address_dict["province"]
        locality=address_dict["city"]
        addressLine=address_dict["detail"]
        postalCode=None
        userLocation=None
        userIp=None
        usermapView=None 
        includeNeighborhood=None 
        maxResults=None

    # 构建请求URL
    base_url = "http://dev.virtualearth.net/REST/v1/Locations"
    params = {
        'countryRegion': countryRegion,
        'adminDistrict': adminDistrict,
        'locality': locality,
        'postalCode': postalCode,
        'addressLine': addressLine,
        'userLocation': userLocation,
        'userIp': userIp,
        'usermapView': usermapView,
        'includeNeighborhood': includeNeighborhood,
        'maxResults': maxResults,
        'key': BingMapsKey,
    }

    # 移除为空的参数
    params = {k: v for k, v in params.items() if v is not None}

    # 发起GET请求
    response = requests.get(base_url, params=params)

    # 检查HTTP响应状态
    if response.status_code == 200:
        # 解析JSON响应
        result = response.json()
        # print(result)

        return simplify_output(result)
    else:
        # 打印错误信息
        print("Error in Bing Maps API request. Status:", response.status_code)
        return None

def simplify_output(response):
    # 如果传入json为None 返回0
    if response is None:
        return {"Error in Bing Maps API request. Status:", response.status_code}
        
    keys_to_remove = ['authenticationResultCode', 'brandLogoUri', 'copyright','traceId']
    formatted_response = {k: v for k, v in response.items() if k not in keys_to_remove}

    return formatted_response

# if __name__ == "__main__":
    # 分开传参
    # res = geocode_chn(countryRegion="CHN", adminDistrict="广东省",locality="佛山市", addressLine="半岛路17号", postalCode="", userLocation=None, userIp=None,usermapView=None,includeNeighborhood=None, maxResults=None, BingMapsKey=<your_key>)
    # 传单一地址（尽可能详细）
    # res = geocode_chn(full_address="南海区南海万科广场",BingMapsKey=<your_key>)
    # print(res)