import trading
import search
import yaml
import json
import os
import numpy as np

def get_config():
    with open("ebay.yaml", 'r') as stream:
        try:
            config = yaml.load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)

config = get_config()
DOMAIN = 'api.ebay.com'
S3_URL='https://s3.amazonaws.com/qwiklist/'
OPTS = {
    'domain':DOMAIN,
    'debug':True,
    'config_fpath':'ebay.yaml',
    'appid':config[DOMAIN]['appid'],
    'devid':config[DOMAIN]['devid'],
    'certid':config[DOMAIN]['certid'],
    'token':config[DOMAIN]['token'],
}
USER_EBAY_EMAIL = 'bfortuner@gmail.com' # "tkeefdddder@gmail.com",

TEST_IMG_URL = 'http://s3.amazonaws.com/qwiklist/images/image-11c9cc70-02ec-4fae-89b0-8b0ce026b511.jpg' #'http://i.ebayimg.com/images/g/kLAAAOSwol5Yx1Mf/s-l1600.jpg'#'https://s3.amazonaws.com/qwiklist/images/image2.jpg'
TEST_PREDICTIONS = {
   u'PK':'images/image-61e16b6c-ecd8-432b-be2c-244babe233f8.jpg',
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
        "PictureDetails": {"PictureURL": ""},
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

#https://developer.ebay.com/devzone/xml/docs/reference/ebay/types
##https://developer.ebay.com/devzone/finding/callref/Enums/conditionIdList.html
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
        "PayPalEmailAddress": "",
        "PictureDetails": {"PictureURL": ""},
        "PostalCode": "98102", #THIS ONE NEEDS FIXING
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
                "ShippingServiceCost": "5.00"
            }
        },
        "Site": "US"
    }
}

FILTERED_LABELS = set(['person', 'human', 'dog'])
TEST_KEYWORDS = 'computer mouse'


def get_median(lst):
    return np.median(np.array(lst))

def search_by_keyword(keywords, category_id):
    items = search.search(OPTS, keywords, category_id)
    items = items['searchResult']['item']
    return items

def get_auction_price(keywords, category_id):
    items = search_by_keyword(keywords, category_id)
    prices = []
    for item in items:
        price = float(item['sellingStatus']['currentPrice']['value'])
        prices.append(price)
    return round(get_median(prices),2)

def add_item(predictions):
    labels = get_labels_from_predictions(predictions)
    img_url = os.path.join(S3_URL, predictions['PK'])
    print(img_url)
    item = build_item(labels, img_url)
    print("ITEM",item)
    trading.verifyAddItem(OPTS, item)

def get_labels_from_predictions(predictions, max_labels=5):
    labels = []
    i = 0
    for label in predictions['Labels']['Labels']:
        if label['Name'] not in FILTERED_LABELS:
            labels.append(label['Name'])
        i += 1
        if i >= max_labels:
            return labels
    return labels

def build_item(labels, img_url):
    item = EBAY_ADD_ITEM_TEMPLATE.copy()
    item['Item']['Title'] = labels[0]
    item['Item']['Description'] = ' '.join(labels)
    category_id = get_suggested_category(labels)
    item['Item']['PrimaryCategory']['CategoryID'] = category_id
    item['Item']['PayPalEmailAddress'] = USER_EBAY_EMAIL
    item['Item']['PictureDetails']['PictureURL'] = img_url
    estimated_price = get_auction_price(' '.join(labels), category_id)
    item['Item']['StartPrice'] = estimated_price
    return item

def get_item_price(keywords):
    return str(10.0)

def get_category_id(labels):
    for l in labels:
        l = l.lower()
        if l in EBAY_CATEGORIES:
            return EBAY_CATEGORIES[l]
    raise Exception("category not found")

def get_categories(tree_level=1):
    categories = trading.categories(OPTS, tree_level)
    cat_json = json.dumps(categories)
    with open('ebay_categories.json', 'w') as f:
        f.write(cat_json)

def save_dict_to_file(obj_dict, fpath):
    obj_json = json.dumps(obj_dict)
    with open(fpath, 'w') as f:
        f.write(obj_json)

def load_json_from_file(fpath):
    #python -m json.tool ebay_categories.json >> ebay_cats.json
    with open(fpath, 'r') as f:
        categories_dict = json.load(f)
    return categories_dict

def upload_picture(img_url):
    img_name = img_url.split('/')[-1]
    return trading.uploadPicture(OPTS, img_url, img_name)

def get_category_json_from_file(fpath='ebay_categories.json'):
    with open(fpath,'r') as f:
        return json.load(f)['CategoryArray']['Category']

def create_category_to_id_mappings():
    our_categories = {} #'name':id
    ebay_categories = get_category_json_from_file()
    for cat in ebay_categories:
        cat_name = cat['CategoryName'].lower().split(' ')[0]
        cat_id = cat['CategoryID']
        our_categories[cat_name] = cat_id
    save_dict_to_file(our_categories, 'our_supported_ebay_categories.json')
    return our_categories

def get_suggested_category(labels):
    DOMAIN
    query_str = ' '.join(labels)
    print(query_str)
    categories = trading.get_suggested_categories(OPTS, query_str)
    if categories['CategoryCount'] == 0:
        return get_category_id(labels)
    category = categories['SuggestedCategoryArray']['SuggestedCategory'][0]['Category']
    name = category['CategoryName']
    cat_id = category['CategoryID']
    print("Found category", name)
    return cat_id

EBAY_CATEGORIES = load_json_from_file('our_supported_ebay_categories.json')

if __name__ == "__main__":
    labels = get_labels_from_predictions(TEST_PREDICTIONS, 3)
    print(labels)
    print(build_item(labels, TEST_IMG_URL))
    #add_item(TEST_PREDICTIONS)
    #print(get_suggested_category(['laptop','computer']))
    #print(TEST_IMG_URL)
    #upload_picture()
    #labels = get_labels_from_predictions(TEST_PREDICTIONS)
    #print(build_item(labels,'http://myimgurl'))
    #print(get_first_category(['hairy','laptop']))
    #add_item(TEST_LABEL)
    # get_categories(1)
    # load_categories()
    #get_category_to_id_mapping(categories)
