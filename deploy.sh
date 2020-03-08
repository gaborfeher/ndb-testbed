#!/bin/bash

gcloud  app deploy --project $1 --version 2 --no-promote
