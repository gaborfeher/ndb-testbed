```
gcloud app deploy
HOST=https://<your project>.appspot.com
curl $HOST/cleanup  # optional
curl $HOST/init/0
# if crashes, check the logs and restart from the last saved
# batch ID, e.g. if you see "saved until 3300", then run:
curl $HOST/init/3300

curl $HOST/offset/1000/10
curl $HOST/offset/2000/10
curl $HOST/offset/3000/10
```

Expected output:
```
gabor@axl:~/ndb-testbed$ curl https://2-dot-myproject.appspot.com/offset/1000/10
[1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010]
gabor@axl:~/ndb-testbed$ curl https://2-dot-myproject.appspot.com/offset/2000/10
[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]
gabor@axl:~/ndb-testbed$ curl https://2-dot-myproject.appspot.com/offset/3000/10
[3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010]
```

Observed output:
```
gabor@axl:~/ndb-testbed$ curl https://2-dot-myproject.appspot.com/offset/1000/10
[1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010]
gabor@axl:~/ndb-testbed$ curl https://2-dot-myproject.appspot.com/offset/2000/10
[1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010]
gabor@axl:~/ndb-testbed$ curl https://2-dot-myproject.appspot.com/offset/3000/10
[1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010]
```



