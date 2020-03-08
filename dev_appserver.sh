#!/bin/bash

cd $(dirname $0)

$(gcloud beta emulators datastore env-init)

dev_appserver.py \
  --application ndbtestbed \
  --env_var DATASTORE_APP_ID=ndbtestbed \
  --port=18080 \
  --admin_port=8010 \
  --host 0.0.0.0 \
  --enable_host_checking false \
  --support_datastore_emulator=True \
  --env_var IN_LOCAL_DEV_ENV=true \
  --env_var OAUTHLIB_INSECURE_TRANSPORT=1 \
  --env_var OAUTHLIB_RELAX_TOKEN_SCOPE=1 \
  --env_var DATASTORE_DATASET=${DATASTORE_DATASET} \
  --env_var DATASTORE_EMULATOR_HOST=${DATASTORE_EMULATOR_HOST} \
  --env_var DATASTORE_EMULATOR_HOST_PATH=${DATASTORE_EMULATOR_HOST_PATH} \
  --env_var DATASTORE_HOST=${DATASTORE_HOST} \
  --env_var DATASTORE_PROJECT_ID=${DATASTORE_PROJECT_ID} \
  ./app.yaml



