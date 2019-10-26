import json
import http.client
import plotly.graph_objects as go
# import plotly.express as px

#requests a given page number of the data and returns just that page content
def get_data(page_num=0, time="2019-10-24T13:00:04Z"):
    conn = http.client.HTTPSConnection("gateway-staging.ncrcloud.com")
    payload = "{\"siteInfoIds\": [\"6\"],\"pageNumber\": "+str(page_num)+",\"pageSize\": 100,\"fromTransactionDateTimeUtc\": {\"dateTime\": \""+time+"\"}}"
    headers = {'accept':"application/json",'content-type':"application/json",'authorization':"Basic YWNjdDpyb290QGhhY2tfc3BhY2U6Tn5pWXY4KzUheA==",'nep-application-key':"8a008d406ddb112d016e0689bb85003c",'nep-organization':"ur-hack",'nep-enterprise-unit':"219eb40f24b544a1908fb51d0b6d16e7",'nep-service-version':"2:1"}
    conn.request("POST", "/transaction-document/transaction-documents/find", payload, headers)
    resp = conn.getresponse()
    # data = resp.read()
    # utf8data = data.decode("utf-8")
    return json.loads(resp.read().decode("utf-8"))

#gives you all the data after applying given filters to the transaction data
def get_all_data(filters=['businessDayUtc','destinationAccount','endTransactionDateTimeUtc','sourceAccount','isVoided','isTrainingMode','siteInfoId','employeeNames','transactionCategory','tlogId'], time="2019-10-24T13:00:04Z"):
    # conn = http.client.HTTPSConnection("gateway-staging.ncrcloud.com")
    # payload = "{\"siteInfoIds\": [\"6\"],\"pageSize\": 100,\"fromTransactionDateTimeUtc\": {\"dateTime\": \"2019-10-24T13:00:04Z\"}}"
    # headers = {'accept':"application/json",'content-type':"application/json",'authorization':"Basic YWNjdDpyb290QGhhY2tfc3BhY2U6Tn5pWXY4KzUheA==",'nep-application-key':"8a008d406ddb112d016e0689bb85003c",'nep-organization':"ur-hack",'nep-enterprise-unit':"219eb40f24b544a1908fb51d0b6d16e7",'nep-service-version':"2:1"}
    # conn.request("POST", "/transaction-document/transaction-documents/find", payload, headers)
    # resp = conn.getresponse()
    # data = resp.read()
    # utf8data = data.decode("utf-8")
    data_dict = get_data(0, time) #dictionary of list of dictionaries
    page_content = filter_results(data_dict['pageContent'],filters) #list of transactions, each tr. is a dict.
    page_size = data_dict['totalPages']
    page_num = 0
    while page_num < page_size:
        resp_page_num = get_data(page_num, time)
        page_content += filter_results(resp_page_num['pageContent'],filters)
        page_num += 1
    return page_content

def filter_results(data, filters):
    num = 0
    for line in data:
        for filter in filters:
            pop = line.pop(filter)
    return data
#
# def collect_data(data, filters):
#     out = []
#     for index, line in enumerate(data):
#         for filter in filters:
#             out[index] += line[filter]
#     return out

def collect_data_dict(data, filters):
    out = []
    for filter in filters:
        out.append([])
    for line in data:
        # line_list = []
        for index, filter in enumerate(filters):
            out[index].append([line[filter]][0])
            # line_list.append(line[filter])
        # if isinstance(line[key], list):
        #     out[line[key][0]] = line_list
        # else:
        #     out[line[key]] = line_list
    for index in range(len(filters)):
        out[index].reverse()
    return out

def count_shtuff(all_data):
    num = 0
    for thing in all_data:
        num += 1
    return num

all_data = get_all_data(time="2019-10-24T05:00:00Z")
num = count_shtuff(all_data)
print(all_data[0])
print(num)
sorted_data_thing = collect_data_dict(all_data,['grandAmount','itemCount','transactionNumber','employeeIds','closeDateTimeUtc'])
print(sorted_data_thing[4])
# zip_data_thing = zip(sorted_data_thing)
new_fig = go.Figure({"data": [{"type": "scatter", "mode": "markers", "x": list(range(len(sorted_data_thing[0]))), "y": sorted_data_thing[0], "marker.size": sorted_data_thing[1]}]})
new_fig.write_html("my_html.html", auto_open=True)
#, "hovertext": sorted_data_thing[4], "hoverinfo": "text"
# for thingy in zip_data_thing:
# new_graph = go.Bar(data=sorted_data_thing,hovertext=
# new_fig = go.Figure(data=go.

my_file = open("data.txt","w")
my_file.write(json.dumps(all_data))
my_file.close()

# print(get_all_data())
