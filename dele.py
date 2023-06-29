"""import requests
from bs4 import BeautifulSoup
import csv
import json
cookies = {
    'ASP.NET_SessionId': '3aq051lb0qyp5rkfp3wmqakt',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,gu;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'ASP.NET_SessionId=3aq051lb0qyp5rkfp3wmqakt',
    'Origin': 'http://168.63.234.13',
    'Pragma': 'no-cache',
    'Referer': 'http://168.63.234.13/patrikaadd/Pages/FrmEdit_Address.aspx',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'X-MicrosoftAjax': 'Delta=true',
    'X-Requested-With': 'XMLHttpRequest',
}


def dataFetcher(code, id):
    data = {
        'ctl00$ScriptManager1': 'ctl00$MainContent$UP2|ctl00$MainContent$BtnSearch',
        'ctl00$MainContent$DdlDistrict_S': code,
        'ctl00$MainContent$TxtSrNo1_S': id,
        '__VIEWSTATE': '/wEPDwUKLTY0Nzg4MzIwMg8WAh4FcHJvbGQyxgQAAQAAAP////8BAAAAAAAAAAwCAAAASEFwcF9Db2RlLnR3eTVzdXduLCBWZXJzaW9uPTAuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbAUBAAAAD1BhdHJpa2FSZWdpc3RlchoAAAAFeFNyTm8GeFJlY05vBnhSZWNEdAh4U3ViWWVhcgZ4RW5kRHQFeE5hbWUFeEFkZDEFeEFkZDIFeEFkZDMHeENpdHlJZAl4Q2l0eU5hbWUHeEFyZWFJZAl4QXJlYU5hbWUHeFpvbmVJZAl4Wm9uZU5hbWUHeE1vYmlsZQl4RG9udFNlbmQIeE5ld0ZsYWcIeEFtYnJpc2gFeEZyZWUGeFNyTm8xBXhLS0lEB3hSZW1hcmsGeEVudER0CHhQaW5jb2RlB3hVc2VySWQAAAAAAAEBAQEAAQABAAEBAAAAAAAAAQABAAgJDQgNCAgIAQEBAQgIDQgCAAAA2QYAAAUoAQAAAAAAAMBORfzr2AgBAAAAAICcnIdy2ggGAwAAABhOaXJhdiBSYW1lc2hiaGFpIFZhc295YSAGBAAAAA5BSi9NYWxhbiAtIDQwMgYFAAAAF1ZlZXIgU2F2YXJrYXIgSGVpZ2h0cy00BgYAAAAYT2duYWogLSBHb3RhIFJvYWQsIE9nbmFqCQEAAAoAAAAACgAAAAAKBgcAAAAKOTk3ODkwMDExNwEAAAACAAAAAAAAAAYIAAAAAAAAAAAAAAAABgkAAAAGMzgwMDYwAAAAAAsWAmYPZBYCAgMPZBYEAgMPDxYCHgRUZXh0BQRheGFyZGQCCw9kFgICAQ9kFgJmD2QWJAIBDxAPFgYeDURhdGFUZXh0RmllbGQFDERpc3RyaWN0Q29kZR4ORGF0YVZhbHVlRmllbGQFDERpc3RyaWN0Q29kZR4LXyFEYXRhQm91bmRnZBAVHQNBREQCQUwDQU5EAkJDA0JISwNCSFICQlkCREcDR1JEAUgCSkQCSlICS0QCTEECTU4CTVACTkkDTlJNAk5WAlBMA1JURANTRUwCU0kCU0sCU1IDU1REAlRQAlZEA1ZSRBUdA0FERAJBTANBTkQCQkMDQkhLA0JIUgJCWQJERwNHUkQBSAJKRAJKUgJLRAJMQQJNTgJNUAJOSQNOUk0CTlYCUEwDUlREA1NFTAJTSQJTSwJTUgNTVEQCVFACVkQDVlJEFCsDHWdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZGQCCw8PFgIfAWVkZAINDw8WAh8BBQQxNzUzZGQCEQ8PFgIfAQUKMDEvMDEvMDAwMWRkAhMPDxYEHgdFbmFibGVkZx8BBQU3NTc4MWRkAhcPDxYCHwVnZGQCHQ8QDxYCHwVnZGQWAQIBZAIfDxYCHwEFATFkAiEPDxYCHwEFCjMxLzA3LzIwMjJkZAIjDxYCHwEFCjMxLzA3LzIwMjJkAjEPEA8WBh8CBQhEaXN0cmljdB8DBQpEaXN0cmljdElkHwRnZBAVrAEJQWhtZWRhYmFkBkFtcmVsaQVBbmFuZAtCYW5hc2thbnRoYQdCaGFydWNoCUJoYXZuYWdhcgVEYWhvZAVEYW5ncwtHYW5kaGluYWdhcghKYW1uYWdhcghKdW5hZ2FkaAZLdXRjaGgFS2hlZGEITWFoZXNhbmEHTmFybWFkYQdOYXZzYXJpBVBhdGFuClBhbmNobWFoYWwJUG9yYmFuZGFyBlJhamtvdAtTYWJhcmthbnRoYQ1TdXJlbmRyYW5hZ2FyBVN1cmF0BFRhcGkIVmFkb2RhcmEGVmFsc2FkC0dpci1Tb21uYXRoCEFyYXZhbGxpBUJvdGFkDkNoaG90YSBVZGFpcHVyCU1haGlzYWdhcgVNb3JiaQ9EZXZiaHVtaS1Ed2Fya2EIMS1TZWxlY3QISGFyaWRoYW0HU3dpa3J1dAZLYW5wdXIJTmFuZHVyYmFyB1BhbGdoYXIGR29uZGlhCFlhdmF0bWFsB1NvbGFwdXIKQWhtZWRuYWdhcgVKYWxuYQZOYXNoaWsGV2FyZGhhBUFrb2xhBk5hbmRlZAZWYXJkaGEFRGh1bGUKQXVyYW5nYWJhZAZTYXRhcmEFVGhhbmULTmF2aSBNdW1iYWkGTXVtYmFpBlJhaWdhZARQdW5lB0phbGdhb24IS29saGFwdXIGTmFncHVyCFBhcmJoYW5pBk5hZ2F1cgRLb3RhB0pvZGhwdXIFQWptZXIGSmFpcHVyBlNpcm9oaQlSYWpzYW1hbmQIQmhpbHdhZGEEUGFsaQdVZGFpcHVyBkJhcm1lcgVKYWxvcgtDaGl0dG9yZ2FyaAhCYW5zd2FyYQlKaHVuamh1bnUGTW9oYWxpCEFtcnV0c2FyBE1vZ2EJSmFsYW5kaGFyCkNoYW5kaWdhcmgITHVkaGlhbmEHTHVja25vdwhKYXVucHVyIAhHaGF6aXB1cghWYXJhbmFzaQhCYXJlaWxseQlBbGxhaGFiYWQHQmhhZG9oaQRBZ3JhC0J1bGFuZHNoYWhyBkhhcmRvaQpQcmF0YXBnYXJoBkJ1ZGF1bghBemFtZ2FyaAhTYWhhcnNoYQVQYXRuYQdLb2xrYXRhBU5hZGlhC011cnNoaWRhYmFkCU1lZGluaXB1cghBbmFudHB1cgpLYXJpbW5hZ2FyDVZpc2FraGFwYXRuYW0HQ2hlbm5haQdWZWxsb3JlD1RpcnVjaGlyYXBwYWxsaQxWaXJ1ZGh1bmFnYXIKQ29pbWJhdG9yZQZKaGFidWEERHVyZwREaGFyB0JhcndhbmkJQWxpcmFqcHVyBlVqamFpbgVQYW5uYQZSYXRsYW0GSW5kb3JlBkJob3BhbAtIb3NoYW5nYWJhZAVEZXdhcwlLYWxhYnVyZ2kJTWFuZ2Fsb3JlBk15c29yZQVHYWRhZwdEaGFyd2FkCUJhbmdhbG9yZQhCYWdhbGtvdAdCZWxnYXVtCEd1bGJhcmdhCUtvemhpa29kZRJUaGlydXZhbmFudGhhcHVyYW0KVHJpdmFuZHJ1bQhUaHJpc3N1cg5FYXN0IFNpbmdoYmh1bQpKYW1zaGVkcHVyCUZhcmlkYWJhZAlQYW5jaGt1bGEIR3VyZ2FvbiAHU3VyZ3VqYQpEdXJnIEMuIEcuDkphbmpnaXItQ2hhbXBhCEJpbGFzcHVyBlJhaXB1cgVEZWxoaQlOZXcgRGVsaGkLTm9ydGggRGVsaGkQTm9ydGggV2VzdCBEZWxoaQpXZXN0IERlbGhpEFNvdXRoIFdlc3QgRGVsaGkLU291dGggRGVsaGkQU291dGggRWFzdCBEZWxoaQ1DZW50cmFsIERlbGhpEE5vcnRoIEVhc3QgRGVsaGkIU2hhaGRhcmEKRWFzdCBEZWxoaQhEZWhyYWR1bghIYXJpZHdhcgVLdWxsdQdTaGltbGEgA1VuYQdLYW5hZ3JhBVNvbGFuCU5vcnRoIEdvYQZQYW5hamkKUHVkdWNoZXJyeRJEYWRyYSBOYWdhciBIYXZlbGkDRGl1BURhbWFuCUh5ZGVyYWJhZAhBZGlsYWJhZAhXYXJhbmdhbBWsAQExATIBMwE0ATUBNgE3ATgBOQIxMAIxMQIxMgIxMwIxNAIxNQIxNgIxNwIxOAIxOQIyMAIyMQIyMgIyMwIyNAIyNQIyNgMxMDcDMjEzAzIxNAMyMTUDMjE2AzIxNwMyMTgDMTk1AzI0NgMyNDcDMjUzAzE5NgMyMjUDMjI2AzE1MwMxNTUDMTU2AzE1OAMxNjADMTc3AzE3OAMxNzkDMTg2AzE5MwMxMTYCMzADMTAyAzEwMwIyNwMxMTgDMTE5AzEyMAMxMzcDMTQyAzE0NgMxNDEDMTM4AzEzNQMxMzYDMTMzAjI4AzE5MAMxNzQDMTc1AzE2MwMxNjgDMTY5AzE3MAMxNzEDMjE5AzE1OQIyOQMxMTcDMTM0AzEyNgMxNDADMTM5AzE0NwMxMzADMTIyAzEyMwMxMTUCMzEDMTYxAzE5NAMxOTkDMjAwAzE5MgMyNTUDMjI5AjMyAzEyNQMxODQDMTUyAzE3MgMxODUDMjEyAzEwNgIzMwMxNDgDMTQ5AzE2NwMxNTcDMTczAzE4MAMxODcDMjIzAzIyNwMxNTEDMTQ0AzE0NQMxMzIDMTI0AzEyOAMyNTQDMjU2AzI0MwMyNDUDMTI5AzEzMQMxMjEDMjIxAzIyMgMxOTgDMjExAzE4OAMxNTADMjUyAzI0NAMxNTQDMTkxAzE0MwMxMTQDMTA4AzEwOQMxMTADMTExAzI0OAIzNQMyMzEDMjMyAzIzMwMyMzQDMjM1AzIzNgMyMzcDMjM4AzIzOQMyNDADMjQxAzIzMAMxNjIDMTY0AzE2NQMyMjQDMjQ5AzI1MAMyMjgDMTEzAzE2NgMxMjcDMTEyAjM0AzEwNAMyMjADMjUxFCsDrAFnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnFgFmZAIzDw8WAh8BBQEyZGQCOw8QDxYGHwIFBlRhbHVrYR8DBQhUYWx1a2FJZB8EZ2QQFQwIQW1hZGF2YWQHQmFyd2FsYQVCYXZsYQdEYXNrcm9pDkRldHJvai1SYW1wdXJhCURoYW5kaHVrYQdEaG9sZXJhBkRob2xrYQZNYW5kYWwGUmFucHVyBlNhbmFuZAhWaXJhbWdhbRUMATUCMTABOAE2ATICMTEDNTY2ATcBMQE5ATQBMxQrAwxnZ2dnZ2dnZ2dnZ2cWAWZkAj0PEA8WBh8CBQNjdHAfAwUGQ2l0eUlkHwRnZBAVFg1BaG1lZGFiYWQgLSAwD0FzYXJ2YSAtIDM4MDAxNg9DaGFuZGxvZGl5YSAtIDAOR2hhdGxvZGl5YSAtIDALR3lhc3B1ciAtIDALSm9kaHB1ciAtIDAIS2FsaSAtIDALTWFrYXJiYSAtIDANTWFrdGFtcHVyIC0gMAxNZW1uYWdhciAtIDAKTmFyb2RhIC0gMBxOaXJuYXluYWdhcihDaGFuZGxvZGl5YSkgLSAwG05pcm5heW5hZ2FyKEdoYXRsb2RpeWEpIC0gMAlPZGhhdiAtIDAKUGlwbGFqIC0gMAlSYW5pcCAtIDAWU2FpanB1ciAtIEdvcGFscHVyIC0gMBBTYXJraGVqIC0gMzgyMjEwDFNoYWh3YWRpIC0gMApUcmFnYWQgLSAwDVZhc3RyYXB1ciAtIDAMVmVqYWxwdXIgLSAwFRYDMjY1AzI2NgMyNjcDMjY4AzI2OQMyNzADMjcxAzI3MgMyNzMDMjc0AzI3NQMyNzYDMjc3AzI3OAMyNzkDMjgwAzI4MQMyODIDMjgzAzI4NAMyODUDMjg2FCsDFmdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2cWAWZkAkEPEA8WAh4HQ2hlY2tlZGhkZGRkAkMPEA8WCB8CBQRab25lHwMFBlpvbmVJRB8EZx8FaGQQFQULTWFkaHlhIENpdHkHTmFkaXBhcglNYW5pbmFnYXIGTmFyb2RhBUJvcGFsFQUDODM5Azg0MAM4NDEDODQyAzg0NBQrAwVnZ2dnZxYBZmQCRw8QDxYCHwVnZGRkZAJJDxAPFgIfBWdkZGRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYEBRljdGwwMCRNYWluQ29udGVudCRDaGtDaXR5BRhjdGwwMCRNYWluQ29udGVudCRDYlpvbmUFG2N0bDAwJE1haW5Db250ZW50JENiTmV3RmxhZwUgY3RsMDAkTWFpbkNvbnRlbnQkQ2JEb250U2VuZEZsYWfg0rdk+J0/IKbEU1oDT3MupE45Uf60rko+kXtFGMO8+A==',
        '__VIEWSTATEGENERATOR': '15CADAE4',
        '__ASYNCPOST': 'true',
        'ctl00$MainContent$BtnSearch': 'Search',
    }

    response = requests.post(
        'http://168.63.234.13/patrikaadd/Pages/FrmEdit_Address.aspx',
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )

    soup = BeautifulSoup(response.text, "html5lib")
    try:
        entryDate = soup.find(
            "input", {"id": "MainContent_TxtEntryDate"})["value"]
    except:
        entryDate = ""
    try:
        receiptNo = soup.find("input", {"id": "MainContent_TxtRecNo"})["value"]
    except:
        receiptNo = ""
    try:
        receiptDate = soup.find(
            "input", {"id": "MainContent_TxtRecDate"})["value"]
    except:
        receiptDate = ""
    try:
        subYear = soup.find("select", {"id": "MainContent_DdlSubYear"}).find(
            "option", {"selected": "selected"})["value"]
    except:
        subYear = ""
    try:
        endDate = soup.find("input", {"id": "MainContent_TxtEndDate"})["value"]
    except:
        endDate = ""
    try:
        Name = soup.find("input", {"id": "MainContent_TxtName"})["value"]
    except:
        Name = ""
    try:
        Add1 = soup.find("input", {"id": "MainContent_TxtAdd1"})["value"]
    except:
        Add1 = ""
    try:
        Add2 = soup.find("input", {"id": "MainContent_TxtAdd2"})["value"]
    except:
        Add2 = ""
    try:
        Add3 = soup.find("input", {"id": "MainContent_TxtAdd3"})["value"]
    except:
        Add3 = ""
    try:
        district = soup.find("select", {"id": "MainContent_DdlDistrict"}).find(
            "option", {"selected": "selected"}).text
    except:
        district = ""
    try:
        disCode = soup.find("input", {"id": "MainContent_TxtSrNo1"})["value"]
    except:
        disCode = ""
    try:
        taluka = soup.find("select", {"id": "MainContent_DdlTaluka"}).find(
            "option", {"selected": "selected"}).text
    except:
        taluka = ""
    try:
        city = soup.find("select", {"id": "MainContent_DdlCity"}).find(
            "option", {"selected": "selected"}).text
    except:
        city = ""
    try:
        pincode = soup.find("input", {"id": "MainContent_TxtPincode"})["value"]
    except:
        pincode = ""
    try:
        if soup.find("input", {"id": "MainContent_CbZone"})["checked"] == "checked":
            is_zone = "True"
        else:
            is_zone = "False"
    except:
        is_zone = "False"
    try:
        zone = soup.find("select", {"id": "MainContent_DdlZone"}).find(
            "option", {"selected": "selected"}).text
    except:
        zone = ""
    try:
        mobile = soup.find("input", {"id": "MainContent_TxtMobile"})["value"]
    except:
        mobile = ""
    try:
        if soup.find("input", {"id": "MainContent_CbNewFlag"})["checked"] == "checked":
            newFlag = "True"
        else:
            newFlag = "False"
    except:
        newFlag = "False"
    try:
        if soup.find("input", {"id": "MainContent_TxtRemark"})["checked"] == "checked":
            dontSendFlag = "True"
        else:
            dontSendFlag = "False"
    except:
        dontSendFlag = "False"
    try:
        remark = soup.find("input", {"id": "MainContent_TxtRemark"})["value"]
    except:
        remark = ""
    data = {}
    data["entryDate"] = entryDate
    data["receiptNo"] = receiptNo
    data["receiptDate"] = receiptDate
    data["subYear"] = subYear
    data["endDate"] = endDate
    data["Name"] = Name
    data["Add1"] = Add1
    data["Add2"] = Add2
    data["Add3"] = Add3
    data["district"] = district
    data["disCode"] = disCode
    data["taluka"] = taluka
    data["city"] = city
    data["pincode"] = pincode
    data["entryDate"] = entryDate
    data["is_zone"] = is_zone
    data["zone"] = zone
    data["entryDate"] = entryDate
    data["mobile"] = mobile
    data["newFlag"] = newFlag
    data["dontSendFlag"] = dontSendFlag
    data["remark"] = remark
    return data


finalData = []
count = 1
file = open("ExpiredData.csv", "r")
reader = csv.reader(file)
for line in reader:
    data = dataFetcher(str(line[0]), str(line[1]))
    finalData.append(data)
    print(count)
    count = count + 1


with open('ExpiredData.json', 'w') as f:
    json.dump(finalData, f)
"""


"""
# Get Url
import requests
import json

url = "https://api.otpless.app/v1/client/user/session/initiate"

payload = json.dumps({
    "loginMethod": "WHATSAPP",
    "redirectionURL": "https://shaharidham.org/",
    "state": "Jagrat"
})
headers = {
    'appId': 'OTPLess:NXKKGVGYHCQGBJQFCPOOXXYGHWDACKQU',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
"""

#YktMWEtsbWFYQkNnTFd2TUFRSFBjT1lRWnhkUUFPR1ozZnRBQjlpd1BoRGhVQXdBcytBRUhMcHkxeGRJUFZPcg

"""
import requests
import json
url= "https://api.otpless.app/v1/client/user/session/userdata"
payload=json.dumps({
    "token": "VzVwYWhzUjQvRlMrZHRKdENMUnRHdEFUOG1ORlN2NlExakNJWDQxcUlBUHRqeFljLzZDMmtWRWhybFFGM0Z4eA",
    "state": "Jagrat"
})
headers={
    "appId": "OTPLess:NXKKGVGYHCQGBJQFCPOOXXYGHWDACKQU",
    "appSecret": "4JT879ptdRR7c7sqfSuhJ8ASp2klOH0c9xV4hj1LW3fnGsUE2HH2Vgryk7KQtN82j",
    "Content-Type": "application/json"
}
response =requests.request("POST",url,headers=headers,data=payload)
print(response.text)
"""

import requests

headers = {
    'Content-Type': 'application/json',
    'Cookie': 'VISITOR_INFO1_LIVE=lLVfT0Gvurc'
}

params = {
    'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
    'prettyPrint': 'false',
}

json_data = {
    'videoId': 'asynnXWJzxo',
    'context': {
        'client': {'clientName': 'WEB',
            'clientVersion': '1.20230108.00.00'
        }
    }
}

response = requests.post(
    'https://www.youtube.com/youtubei/v1/player',
    params=params,
    headers=headers,
    json=json_data,
)
print(response.json()["streamingData"]["adaptiveFormats"][-1]["url"])