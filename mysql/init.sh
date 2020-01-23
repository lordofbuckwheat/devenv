#!/bin/bash
mysql -u root -proot < /mysql/init.sql
mysql -u root -proot master < /mysql/migrations/201808201058-init.sql
mysql -u root -proot master < /mysql/after-init.sql
