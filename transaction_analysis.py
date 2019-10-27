import json
import http.client
import plotly.graph_objects as go
import datetime
from datetime import timedelta, date, time
from dateutil import parser
import pytz
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

#expects a list of lists, where the one at index has times for the corresponding other ones
#data[0] and data[1] are both numbers that can be summed within the time delta given
def combine_data_by_time(data, time_index, delta=timedelta(hours=1), indices={0,1}):
    new_data = []
    for d in data:
        new_data.append([])
    first_day = min(data[time_index])
    first_day = parser.isoparse(first_day).date()
    current_time_block_start = parser.isoparse(datetime.datetime.isoformat(datetime.datetime.combine(first_day,time.min))+"Z")
    new_index = 0
    i = 0
    while i < len(data[time_index]):
        for ind in indices:
            new_data[ind].append(0)
        new_data[time_index].append(datetime.datetime.isoformat(current_time_block_start))
        while i < len(data[time_index]) and parser.isoparse(data[time_index][i]) < current_time_block_start + delta:
            for ind in indices:
                new_data[ind][-1] += data[ind][i]
            i += 1
        current_time_block_start += delta
        new_index += 1
    return new_data


all_data = get_all_data(time="2019-10-20T00:00:00Z")
num = count_shtuff(all_data)
print(all_data[0])
print(num)
sorted_data_thing = collect_data_dict(all_data,['grandAmount','itemCount','transactionNumber','employeeIds','closeDateTimeUtc'])
print(sorted_data_thing[4])
# zip_data_thing = zip(sorted_data_thing)
data_by_time = combine_data_by_time(sorted_data_thing,4)
new_fig = go.Figure({"data": [{"type": "scatter", "mode": "markers",  "x": data_by_time[2], "y": data_by_time[0]}]})
new_fig.write_html("my_html.html", auto_open=True)
#, "hovertext": sorted_data_thing[4], "hoverinfo": "text"
# "marker.size": sorted_data_thing[1], "mode": "markers",
# for thingy in zip_data_thing:
# new_graph = go.Bar(data=sorted_data_thing,hovertext=
# new_fig = go.Figure(data=go.

my_file = open("data.txt","w")
my_file.write(json.dumps(all_data))
my_file.close()

# print(get_all_data())
