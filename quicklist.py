import trading
# import connect
#import search
import yaml


with open("ebay.yaml", 'r') as stream:
    try:
        config = yaml.load(stream)
        print("loading config")
    except yaml.YAMLError as exc:
        print(exc)

DOMAIN = 'api.sandbox.ebay.com'

TEST_LABEL = {
   u'PK':u'images/image2.jpg',
   u'Labels':{
      u'Labels':[
         {
            u'Confidence':73.2657470703125,
            u'Name':u'Appliance'
         },
         {
            u'Confidence':73.2657470703125,
            u'Name':u'Fridge'
         },
         {
            u'Confidence':73.2657470703125,
            u'Name':u'Refrigerator'
         },
         {
            u'Confidence':56.701107025146484,
            u'Name':u'Book'
         },
         {
            u'Confidence':56.701107025146484,
            u'Name':u'Text'
         },
         {
            u'Confidence':53.809852600097656,
            u'Name':u'Brochure'
         },
         {
            u'Confidence':53.809852600097656,
            u'Name':u'Flyer'
         },
         {
            u'Confidence':53.809852600097656,
            u'Name':u'Poster'
         },
         {
            u'Confidence':50.91508102416992,
            u'Name':u'Label'
         }
      ],
      u'ResponseMetadata':{
         u'RetryAttempts':0,
         u'HTTPStatusCode':200,
         u'RequestId':u'a96902fe-32cf-11e7-9abf-05782b946463',
         u'HTTPHeaders':{
            u'date':u'',
            u'x-amzn-requestid':u'a96902fe-32cf-11e7-9abf-05782b946463',
            u'content-length':u'495',
            u'content-type':u'application/x-amz-json-1.1',
            u'connection':u'keep-alive'
         }
      },
      u'OrientationCorrection':u'ROTATE_0'
   }
}

S3_URL='https://s3.amazonaws.com/qwiklist/'

        # api = Trading(domain=EBAY_DOMAIN, debug=opts.debug, config_file=opts.yaml, appid=opts.appid,
        #               certid=opts.certid, devid=opts.devid, warnings=False)

opts = {
    'domain':DOMAIN,
    'debug':True,
    'config_fpath':'ebay.yaml',
    'appid':config[DOMAIN]['appid'],
    'devid':config[DOMAIN]['devid'],
    'certid':config[DOMAIN]['certid'],
    'token':config[DOMAIN]['token'],
}
print("OPTIONS------")
print(opts)

EBAY_TEST_ITEM = {
    "Item": {
        "Title": "Harry Potter and the Philosopher's Stone",
        "Description": "This is the first book in the Harry Potter series. In excellent condition!",
        "PrimaryCategory": {"CategoryID": "377"},
        "StartPrice": "1.0",
        "CategoryMappingAllowed": "true",
        "Country": "US",
        "ConditionID": "3000",
        "Currency": "USD",
        "DispatchTimeMax": "3",
        "ListingDuration": "Days_7",
        "ListingType": "Chinese",
        "PaymentMethods": "PayPal",
        "PayPalEmailAddress": "tkeefdddder@gmail.com",
        "PictureDetails": {"PictureURL": "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007"},
        "PostalCode": "95125",
        "Quantity": "1",
        "ReturnPolicy": {
            "ReturnsAcceptedOption": "ReturnsAccepted",
            "RefundOption": "MoneyBack",
            "ReturnsWithinOption": "Days_30",
            "Description": "If you are not satisfied, return the book for refund.",
            "ShippingCostPaidByOption": "Buyer"
        },
        "ShippingDetails": {
            "ShippingType": "Flat",
            "ShippingServiceOptions": {
                "ShippingServicePriority": "1",
                "ShippingService": "USPSMedia",
                "ShippingServiceCost": "2.50"
            }
        },
        "Site": "US"
    }
}

EBAY_ADD_ITEM_TEMPLATE = {
    "Item": {
        "Title": "",
        "Description": "",
        "PrimaryCategory": {
            "CategoryID": "377"
        },
        "StartPrice": "10.0",
        "CategoryMappingAllowed": "true",
        "Country": "US",
        "ConditionID": "3000",
        "Currency": "USD",
        "DispatchTimeMax": "3",
        "ListingDuration": "Days_7",
        "ListingType": "Chinese",
        "PaymentMethods": "PayPal",
        "PayPalEmailAddress": "tkeefdddder@gmail.com",
        "PictureDetails": {"PictureURL": "http://i1.sandbox.ebayimg.com/03/i/00/30/07/20_1.JPG?set_id=8800005007"},
        "PostalCode": "95125",
        "Quantity": "1",
        "ReturnPolicy": {
            "ReturnsAcceptedOption": "ReturnsAccepted",
            "RefundOption": "MoneyBack",
            "ReturnsWithinOption": "Days_30",
            "Description": "If you are not satisfied, return the book for refund.",
            "ShippingCostPaidByOption": "Buyer"
        },
        "ShippingDetails": {
            "ShippingType": "Flat",
            "ShippingServiceOptions": {
                "ShippingServicePriority": "1",
                "ShippingService": "USPSMedia",
                "ShippingServiceCost": "2.50"
            }
        },
        "Site": "US"
    }
}


FILTERED_LABELS = ['person', 'human', 'dog']

def get_keywords_from_labels(n=3):




def build_item(labels, img_url):
    get_keywords = get_keywords_from_labels()

    return EBAY_ITEM_TEMPLATE

def add_item(labeled_item):
    print("Adding Item", labeled_item)
    img_url = S3_URL + labeled_item['PK']
    labels = labeled_item['Labels']['Labels']
    print(img_url)
    print(labels)
    trading.verifyAddItem(opts, myitem)




if __name__ == "__main__":
    add_item(TEST_LABEL)
