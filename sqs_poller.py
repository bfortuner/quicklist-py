import json
import time
import quicklist


conf = {
  "sqs-access-key": "AKIAIDO5S4VEGRTLZMAQ",
  "sqs-secret-key": "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",
  "sqs-queue-name": "qwiklist",
  "sqs-region": "us-east-1",
  "sqs-path": "sqssend"
}

import boto.sqs
conn = boto.sqs.connect_to_region(
        conf.get('sqs-region'),
        aws_access_key_id = conf.get('sqs-access-key'),
        aws_secret_access_key = conf.get('sqs-secret-key')
)

q = conn.create_queue(conf.get('sqs-queue-name'))

while(True):
    for m in q.get_messages():
      try:
        print '%s: %s' % (m, m.get_body())
        json_string = m.get_body()
        obj = json.loads(json_string)
        quicklist.add_item(obj)
      except:
        print("SQS ERROR PROCESSING ITEM", m.get_body())
      finally:
        q.delete_message(m)
        time.sleep(1)




