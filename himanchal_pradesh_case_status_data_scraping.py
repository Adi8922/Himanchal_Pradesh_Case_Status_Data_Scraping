import requests
# import csv 
from bs4 import BeautifulSoup
# import pandas as pd


session = requests.session()
url = "https://hphighcourt.nic.in/"
url1 ="https://highcourt.hp.gov.in/caseinfo/casequery_action.php"
response1 = session.get(url , verify = False)
html_content1 = response1.content
soup1 = BeautifulSoup(html_content1 ,"lxml")
# print(soup)
output = []

Headers1 =  {	
        "Accept" : "*/*",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language" : "en-US,en;q=0.5",
        "Connection" : "keep-alive",
        "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
        "Host" : "highcourt.hp.gov.in",
        "Origin" : "https://hphighcourt.nic.in",
        "Referer" : "https://hphighcourt.nic.in/",
        "Sec-Fetch-Dest" : "empty",
        "Sec-Fetch-Mode" : "cors",
        "Sec-Fetch-Site" : "cross-site",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"
    }

payload1 = {
    	"type":"R",
        "case_type":"1",
        "caseNo":"5",
        "year":"2022"
    }

responce2 = session.post(url1, headers = Headers1, data = payload1, verify=False)
html_content2 = responce2.content
soup2 = BeautifulSoup(html_content2,"lxml")


case_details = soup2.find("table",attrs={"id":"case_detail_table"})
all_trs = case_details.find_all("tr")
trs_position = all_trs[1]
td = trs_position.find_all("td")
td_position = td[1].text.split("/")
case_type = td_position[0]
case_name_id = td_position[1]
case_year = td_position[2]
# print("case_type",case_type, "case_name",case_name_id, "case_year",case_year)

case_num = {}
case_details = {}
case_num["case id"] = case_name_id
case_num["case year"] = case_year
case_num["case type"] = case_type
output.append(case_num)


case_status = soup2.find("table",attrs={"id":"case_status"})
all_trs1 = case_status.find_all("tr")
trs_position1 = all_trs1[1]
td1 = trs_position1.find_all("td")
td_position1 = td1[1].text
case_details['Date Of Decision'] = td_position1


#party detail ko soup se find kiya 
party_detail = soup2.find("table",attrs={"id":"party_detail"})
#tr tag se position value find kiya 
all_trs2 = party_detail.find_all("tr")
trs_position2 = all_trs2[2]
#tr tag ke andar td tag find kita 
td2 = trs_position2.find_all("td")
Petitioner_details = td2[0]
Respondent_details = td2[1].text.split(":")

pet_name_detail = Petitioner_details.text.split(":")
pet_name_detals = pet_name_detail[1].split("Address")
pet_name = pet_name_detals[0].strip()
pet_address = pet_name_detail[2].strip()
pet_advo = pet_name_detail[3].strip()

case_details['Petitioner_name'] = pet_name
case_details['Petitioner_address'] = pet_address
case_details['Petitioner_advocate'] = pet_advo


res_first_name = Respondent_details[1].strip().split("Address")
first_name = res_first_name[0]
res_first_address = Respondent_details[2].strip().split("Address")
first_address = res_first_address[0]
case_details ["Respondent_first_name"] = first_name
case_details ["Respondent_first_address"] = first_address

res_second_name = Respondent_details[3].strip().split("Address")
second_name = res_second_name[0]
res_second_address = Respondent_details[4].strip().split("Address")
second_address = res_second_address[0]
case_details ["Respondent_second_name"] = second_name
case_details ["Respondent_second_address"] = second_address

res_third_name = Respondent_details[5].strip().split("Address")
third_name = res_third_name[0]
res_third_address = Respondent_details[6].strip().split("Address")
third_value = res_third_address[0].split("Advocate")
third_address = third_value[0]
case_details ["Respondent_third_name"] = third_name
case_details ["Respondent_third_address"] = third_address

res_advocate = Respondent_details[6].strip().split("Advocate")
advocate_data = res_advocate[1]
case_details ["Respondent_advocate"] = advocate_data

output.append(case_details)
print(output)
