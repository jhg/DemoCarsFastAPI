# Demo Cars Booking API

## Development

A `requirements.txt` is available for setting up dependencies in your venv.

It is ready to be executed from PyCharm running `DemoCarsFastAPI`, from command line as `fastapi dev` and
 it's possible to try the dockerization that will be used in production with `docker-compose up` also.

### Testing

Additional dependencies for testing are in `requirements-dev.txt` to be installed in your development
 environment, but not in production and docker image.

Tests are implemented using `pytest` and can be run with `pytest` command.

## Dockerization

The base image used has recent (01/2026) vulnerabilities, but does not affect our use case. Alpine flavor
 is chosen to minimize the image size.

## Demo Extra Notes
