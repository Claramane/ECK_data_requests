import requests
from bs4 import BeautifulSoup
import json
import time
import re



def scrape_data(ChartNo):
    ChartNo = ChartNo.zfill(10)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    rs = requests.session()
    data = rs.get(f"http://172.20.110.185/login/RedirectHisCall?clerkid=MDIwMDM&chart={ChartNo}", headers = headers)
    soup = BeautifulSoup(data.text, "lxml")
    redirect_url = data.url
    code = redirect_url.split("=")[1]
    # print(code)
    payload = {"chart": str(code)}
    info = rs.post(f"http://172.20.110.185/home/BasePatientInfo", headers = headers, data = payload)
    # print(info.text)
    info = BeautifulSoup(info.text, "lxml")

    # 取得身高體重
    BMI = info.find(id = "BmiContainer")
    BMI = BMI.find_all("strong")[2]
    BH = str(BMI.text).split("/")[0]
    BW = str(BMI.text).split("/")[1]
    BH = BH.split(":")[1].strip()
    BW = BW.split(":")[1].strip()
    # print(f'{BH} cm')
    # print(f'{BW} kg')

    info = info.find_all("strong")
    name = info[0].text
    sex = info[2].text
    age = str(info[4].text).split("歲")[0]
    print(name)
    print(sex)
    print(age)
    # for i in info:

        # print(i.text)


    # for i in info:
        # name = i.text
        # print(name)
        # print(i.text)

    return soup

labdata_key_dict = {
    '動態產生eGFR': 'CeGFR', 'Albumin': 'C6309038', 'Alk-P': 'C6309027', 'Amylase': 'C6309017', 'BE(B)': 'C6BEB', 'BNP': 'C6312193', 'BUN': 'C6309002', 'CA': 'C6309011', 'Cholesterol-T': 'C6309001', 'CK-MB': 'C6399086', 'CPK': 'C6309032', 'Creatinine': 'C6309015', 'Creatinine (U)': 'C6309016', 'CRP': 'C6312903', 'CTCO2': 'C7CTCO2', 'Glucose': 'C5GLUCO', 'Glucose,AC': 'C6309901', 'GOT (AST)': 'C6309025', 'GPT (ALT)': 'C6309026', 'HbA1C': 'C6309006', 'HCO3-ACT': 'C4HCO3A', 'HDL-C': 'C6309043', 'Iron': 'CIRON', 'K': 'C6309022', 'LDL-C': 'C6309044', 'Lipase': 'C6309064', 'Microalbumin (Nephelometry)': 'C6312111', 'NA': 'C6309021', 'O2SAT': 'C8O2SAT', 'pCO2': 'C3PCO2', 'pH': 'C3PH', 'pO2': 'C2PO2', 'r-GT': 'C6309031', 'T-Bilirubin': 'C6309029', 'TIBC': 'CTIBC', 'Triglyceride': 'C6309004', 'Troponin I': 'C6399035', 'Uric Acid': 'C6309013', 'Urine microalbumin/creatinine ratio': 'C6300012', 'A-Lym': 'C7ALYM', 'ABO Typing  自述血型:(     )': 'C6311001', 'APTT': 'C6308036', 'Band': 'C6BAND', 'Baso': 'C5BA', 'Blast': 'C8BLAST', 'Eosin': 'C4EO', 'Hb': 'C6308003', 'Ht': 'C6308004', 'Lym': 'C2LY', 'MCH': 'CMCH', 'MCHC': 'CMCHC', 'MCV': 'CMCV', 'Metamyelo': 'CAMETAMY', 'Mono': 'C3MO', 'Myelocyte': 'CBMYELO', 'Neutro': 'C1NE', 'NRBC': 'CCNRBC', 'Other': 'CUOTHER', 'Platelet': 'C6308006', 'Promyelo': 'C9PROMYE', 'PT': 'C6308026', 'RBC': 'C6308001', 'RH(D)': 'C6311003', 'WBC': 'C6308002', 'Anti-HAV IgM': 'C6314039', 'Anti-HBc': 'C6314037', 'Anti-HBs': 'C6314033', 'Anti-HCV': 'C6314051', 'Ferritin': 'C6327017', 'HBsAg': 'C6314032', 'Bacteria/HPF': 'CW4BACT', 'Bacteria/uL': 'CW4BACT1', 'Bilirubin': 'C8BILI', 'Cast': 'CWCAST', 'Clarity': 'C2CLARI', 'Color': 'C1COLOR', 'Crystal': 'CWCRYSTA', 'Epith.cell/HPF': 'CW3EPITH', 'Epith.cell/uL': 'CW3EPIT1', 'Fungi': 'CWFUNGI', 'Ketone': 'C6KETON', 'Leukocyte': 'CCLEUKO', 'Mucus': 'CW5MUCUS', 'Nitrite': 'CBNITR', 'OB': 'C9OB', 'Protein': 'C4PROTE', 'R.B.C./HPF': 'CW1RBC', 'R.B.C./uL': 'CW1RBC1', 'SP.GR.': 'C7SPGR', 'Stool-O.B.(定量免疫法)': 'C6399121', 'Synovial Crystal (關節液偏光檢查)': 'C6316013', 'Trichomonas': 'CWTRICHO', 'Urobilinogen': 'CAUROB', 'W.B.C./HPF': 'CW2WBC', 'W.B.C./uL': 'CW2WBC1', 'Blood culture': 'C6313016', 'Influenza A Ag': 'C6314065', 'Influenza B Ag': 'C6314066'
}


# 取得所有labdata的編碼 (偶爾要重抓一次，避免資訊室改編碼或是推出新的檢查)
# labdata_key = soup.find_all(class_ = "badge badge-pill badge-secondary labitem")
# for labdata_key in labdata_key:
#     data_code = str(labdata_key["data-code"])
#     data_labname = str(labdata_key["data-labname"])
#     data_labname = data_labname.strip()
#     labdata_key_dict[f"{data_labname}"] = data_code
#     # print(data_code + " " + data_labname)
# print(labdata_key_dict)


# 花式搜尋data
def get_all_labdata():
    dict = {}
    trs = soup.find_all(class_ = re.compile("^groupCode"))
    # print(trs)
    for i in trs:
        labdata_name = str(i.find("b").text).strip()
        # print(labdata_name)
        datas = i.find_all("tbody")[1]
        data = datas.find_all("tr")
        list_all = []
        for i in data:
            time = str(i.find_all("td")[1].text)
            value = str(i.find_all("td")[2].text)
            list = [value, time]
            list_all.append(list)
        dict[labdata_name] = list_all
        # print(list)
    # print(dict)
    all_data = json.dumps(dict, indent=4)
    print(all_data)


def get_last_labdata():
    dict = {}
    trs = soup.find_all(class_ = re.compile("^groupCode"))
    # print(trs)
    for i in trs:
        labdata_name = str(i.find("b").text).strip()
        # print(labdata_name)
        datas = i.find_all("tbody")[1]
        data = datas.find_all("tr")[0] # 這行代表只取最新的值
        time = str(data.find_all("td")[1].text)
        value = str(data.find_all("td")[2].text)
        list = [value, time]
        dict[labdata_name] = list
        # print(list)
    # print(dict)
    last_data = json.dumps(dict, indent = 4)
    # print(last_data)
    return last_data, dict

def get_simple_labdata():
    dict_simple = {}
    simple_labdata_key_dict = {
        "GPT (ALT)": "C6309026", "Creatinine": "C6309015", "K": "C6309022", "Hb": "C6308003", "Platelet": "C6308006", "PT": "C6308026", "APTT": "C6308036"
    }
    last_data, dict = get_last_labdata()
    for labdata_name, labdata_value in simple_labdata_key_dict.items():
        dict_simple[labdata_name] = dict[labdata_name]
    # print(dict_simple)
    simple_data = json.dumps(dict_simple, indent = 4)
    print(simple_data)




# for labdata_name, labdata_code in labdata_key_dict.items():
#     # print(labdata_code)
#     try: 
#         print(labdata_name)
#         get_last_labdata(labdata_code)
#     except:
#         continue

# while True:
    # 病例號放這邊，補0到十個數字
    # 48251
    # ChartNo = input("請輸入病例號: ")
ChartNo = "5426687"
t1 = time.time()
soup = scrape_data(ChartNo)
get_simple_labdata()
# get_last_labdata()
# get_all_labdata()


t2 = time.time()
print("Time spend: ", t2-t1)






