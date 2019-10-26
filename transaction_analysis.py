import json
import http.client
import plotly.graph_objects as go

#requests a given page number of the data and returns just that page content
def get_data(page_num, time="2019-10-24T13:00:04Z"):
    conn = http.client.HTTPSConnection("gateway-staging.ncrcloud.com")
    payload = "{\"siteInfoIds\": [\"6\"],\"pageNumber\": "+str(page_num)+",\"pageSize\": 100,\"fromTransactionDateTimeUtc\": {\"dateTime\": \""+time+"\"}}"
    headers = {'accept':"application/json",'content-type':"application/json",'authorization':"Basic YWNjdDpyb290QGhhY2tfc3BhY2U6Tn5pWXY4KzUheA==",'nep-application-key':"8a008d406ddb112d016e0689bb85003c",'nep-organization':"ur-hack",'nep-enterprise-unit':"219eb40f24b544a1908fb51d0b6d16e7",'nep-service-version':"2:1"}
    conn.request("POST", "/transaction-document/transaction-documents/find", payload, headers)
    resp = conn.getresponse()
    # data = resp.read()
    # utf8data = data.decode("utf-8")
    return json.loads(resp.read().decode("utf-8"))

#gives you all the data after applying given filters to the transaction data
def get_all_data(filters=['businessDayUtc','destinationAccount','endTransactionDateTimeUtc','sourceAccount','isVoided','isTrainingMode','siteInfoId','employeeNames','transactionCategory','tlogId']):
    # conn = http.client.HTTPSConnection("gateway-staging.ncrcloud.com")
    # payload = "{\"siteInfoIds\": [\"6\"],\"pageSize\": 100,\"fromTransactionDateTimeUtc\": {\"dateTime\": \"2019-10-24T13:00:04Z\"}}"
    # headers = {'accept':"application/json",'content-type':"application/json",'authorization':"Basic YWNjdDpyb290QGhhY2tfc3BhY2U6Tn5pWXY4KzUheA==",'nep-application-key':"8a008d406ddb112d016e0689bb85003c",'nep-organization':"ur-hack",'nep-enterprise-unit':"219eb40f24b544a1908fb51d0b6d16e7",'nep-service-version':"2:1"}
    # conn.request("POST", "/transaction-document/transaction-documents/find", payload, headers)
    # resp = conn.getresponse()
    # data = resp.read()
    # utf8data = data.decode("utf-8")
    data_dict = get_data(0) #dictionary of list of dictionaries
    page_content = filter_results(data_dict['pageContent'],filters) #list of transactions, each tr. is a dict.
    page_size = data_dict['totalPages']
    page_num = 0
    while page_num < page_size:
        resp_page_num = get_data(page_num)
        page_content += filter_results(resp_page_num['pageContent'],filters)
        page_num += 1
    return page_content

def filter_results(data, filters):
    num = 0
    for line in data:
        for filter in filters:
            pop = line.pop(filter)
    return data




def count_shtuff(all_data):
    num = 0
    for thing in all_data:
        num += 1
    return num

all_data = get_all_data()
num = count_shtuff(all_data)
print(all_data[0])
print(num)

file = open("data.txt","w")
file.write(json.dumps(all_data))
file.close()

fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
fig.write_html('first_figure.html', auto_open=True)

# print(get_all_data())
