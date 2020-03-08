```
gcloud datastore indexes create index.yaml
gcloud app deploy
gcloud app logs tail -s default
HOST=https://<your project>.appspot.com
curl $HOST/cleanup  # optional
curl $HOST/init/0
# if crashes, check the logs and restart from the last saved
# batch ID, e.g. if you see "saved until 3300", then run:
curl $HOST/init/3300
curl $HOST/test
```
