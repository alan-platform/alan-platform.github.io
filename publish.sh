#!/bin/bash

rsync -avz --exclude=".git*" . alan@office.m-industries.com:sites/alan.m-industries.com/
