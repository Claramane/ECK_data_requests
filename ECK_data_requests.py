import requests
from bs4 import BeautifulSoup
import time



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
    BMI = info.find(id = "BmiContainer")
    BMI = BMI.find_all("strong")[2]
    BMI = str(BMI.text)
    print(BMI)

    # info = info.find_all(class_ = "PatientInfoMargin")
    # for i in info:
    #     # name = 
    #     print(i.text)

    return soup, code

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
def get_all_labdata(data_code): 
    soup = scrape_data(ChartNo)
    trs = soup.find(class_ = f"{data_code} groupCode")
    datas = trs.find_all("tbody")[1]
    datas = datas.find_all("tr")
    for data in datas:
        time = str(data.find_all("td")[1].text)
        value = str(data.find_all("td")[2].text)
        print(value + " " + time)

def get_last_labdata(data_code):
    soup = scrape_data(ChartNo)
    trs = soup.find(class_ = f"{data_code} groupCode")
    datas = trs.find_all("tbody")[1]
    data = datas.find("tr")
    time = str(data.find_all("td")[1].text)
    value = str(data.find_all("td")[2].text)
    print(value + " " + time)

def get_simple_labdata():
    # soup = scrape_data(ChartNo)
    simple_labdata_key_dict = {
        "GPT (ALT)": "C6309026", "Creatinine": "C6309015", "K": "C6309022", "Hb": "C6308003", "Platelet": "C6308006", "PT": "C6308026", "APTT": "C6308036"
    }
    for labdata_name, labdata_code in simple_labdata_key_dict.items():
        print(labdata_name)
        trs = soup.find(class_ = f"{labdata_code} groupCode")
        datas = trs.find_all("tbody")[1]
        data = datas.find("tr")
        time = str(data.find_all("td")[1].text)
        value = str(data.find_all("td")[2].text)
        print(value + " " + time)

# for labdata_name, labdata_code in labdata_key_dict.items():
#     # print(labdata_code)
#     try: 
#         print(labdata_name)
#         get_last_labdata(labdata_code)
#     except:
#         continue

while True:
    # 病例號放這邊，補0到十個數字
    # 48251
    ChartNo = input("請輸入病例號: ")
    t1 = time.time()
    soup, code = scrape_data(ChartNo)
    # get_simple_labdata()

    t2 = time.time()
    print("Time spend: ", t2-t1)






