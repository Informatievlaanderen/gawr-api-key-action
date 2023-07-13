# GAWR - API gateway action integrations

## Add API key
See [README](./action-add/README.md).

## Update API key
See [README](./action-update/README.md).

## Remove API key
See [README](./action-remove/README.md).

# Developer information

## Build and deploy
Make sure you do a `docker login ghcr.io` and use a [PAT](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) with the correct permissions.

Execute `deploy.sh` to build and push the docker images.
It will tag those images with the version set in `VERSION.txt`.

## Actions
In the `action.yml` for each api key action, the version is hardcoded for the specific docker image.
So if you've updated the image, don't forget to update these as well.

