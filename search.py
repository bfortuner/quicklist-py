import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection

try:
    api = Connection(appid='JonFerna-qwiklist-PRD-a69e0185b-1b78dc2f', config_file=None)
    response = api.execute('findItemsAdvanced', {'keywords': 'legos'})        

    assert(response.reply.ack == 'Success')  
    assert(type(response.reply.timestamp) == datetime.datetime)
    assert(type(response.reply.searchResult.item) == list)

    items = response.reply.searchResult.item
    item = response.reply.searchResult.item[1]
    assert(type(item.listingInfo.endTime) == datetime.datetime)
    assert(type(response.dict()) == dict)
    print(len(items))
    print(response.reply.searchResult.item[1])

except ConnectionError as e:
    print(e)
    print(e.response.dict())
