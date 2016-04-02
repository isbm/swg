#!/bin/sh

curl -H "Contenty-Type: application/json" -X POST --data @add.json http://localhost:6543/api/add
