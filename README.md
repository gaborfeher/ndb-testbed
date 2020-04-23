```
gcloud app deploy
HOST=https://<your project>.appspot.com
curl $HOST/demo
```

Expected output:
```
gabor@axl:~/ndb-testbed$ curl https://2-dot-incidecoder2.appspot.com/demo
[(995, 996), (996, 997), (997, 998), (998, 999), (999, 1000), (1000, 1001), (1001, 1001), (1002, 1002), (1003, 1003), (1004, 1004), (1005, 1005)]
```

Observed output:
```
gabor@axl:~/ndb-testbed$ curl https://2-dot-incidecoder2.appspot.com/demo
[(995, 996), (996, 997), (997, 998), (998, 999), (999, 1000), (1000, 1001), (1001, 1001), (1002, 1001), (1003, 1001), (1004, 1001), (1005, 1001)]
```



