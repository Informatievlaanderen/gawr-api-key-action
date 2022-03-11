#!/bin/sh
VERSION=`cat VERSION.txt | tr -d " \t\n\r"`

# Remove excisting containers with same version
docker image rm -f ghcr.io/informatievlaanderen/gawr-api-key-action:$VERSION-add
docker image rm -f ghcr.io/informatievlaanderen/gawr-api-key-action:$VERSION-remove
docker image rm -f ghcr.io/informatievlaanderen/gawr-api-key-action:$VERSION-update

# Build containers
docker build -t ghcr.io/informatievlaanderen/gawr-api-key-action:$VERSION-add    -f ./action-add/Dockerfile      ./action-add
docker build -t ghcr.io/informatievlaanderen/gawr-api-key-action:$VERSION-remove -f ./action-remove/Dockerfile   ./action-remove
docker build -t ghcr.io/informatievlaanderen/gawr-api-key-action:$VERSION-update -f ./action-update/Dockerfile   ./action-update

# Push containers to registry
docker push ghcr.io/informatievlaanderen/gawr-api-key-action:$VERSION-add   
docker push ghcr.io/informatievlaanderen/gawr-api-key-action:$VERSION-remove
docker push ghcr.io/informatievlaanderen/gawr-api-key-action:$VERSION-update
