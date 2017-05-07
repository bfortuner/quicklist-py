import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection

PROD_DOMAIN = 'api.ebay.com'

def search(opts, keywords, category_id, n_listings=100):
    print("KEYWORDS",keywords)
    try:
        api = Connection(config_file=opts['config_fpath'], appid=opts['appid'])
        response = api.execute('findItemsAdvanced', {'keywords': keywords})

        assert(response.reply.ack == 'Success')
        assert(type(response.reply.timestamp) == datetime.datetime)
        print(response.dict())
        assert(type(response.reply.searchResult.item) == list)

        items = response.reply.searchResult.item[:n_listings]
        assert(type(response.dict()) == dict)
        return response.dict()


    except ConnectionError as e:
        print(e)
        print(e.response.dict())
