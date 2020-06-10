#!/bin/bash

docker build -t vsc-app:1.0 .
docker login
docker tag vsc-app:1.0 sapdi/vsc-app:1.0
docker push sapdi/vsc-app:1.0
rm -f vscode-app.zip
zip -r vscode-app.zip manifest.json content/
