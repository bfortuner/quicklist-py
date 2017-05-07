

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
 
import time
while(True):
        for m in q.get_messages():
                print '%s: %s' % (m, m.get_body())
                q.delete_message(m)
        time.sleep(1)