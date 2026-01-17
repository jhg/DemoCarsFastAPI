# Demo Cars Booking API

## Development

A `requirements.txt` is available for setting up dependencies in your venv.

It is ready to be executed from PyCharm running `DemoCarsFastAPI`, from command line as `fastapi dev` and
 it's possible to try the dockerization that will be used in production with `docker-compose up` also.

### Helpers

There is a `manage.py` script to help to add cars, to have data for development to try features.

```bash
./manage.py add <car_id> <car_model> <car_seats>
```

### Testing

Additional dependencies for testing are in `requirements-dev.txt` to be installed in your development
 environment, but not in production and docker image. It requires yet dependencies in `requirements.txt` to
 be installed.

Tests are implemented using `pytest` and can be run with `pytest` command.

## Dockerization

The base image used has recent (01/2026) vulnerabilities, but does not affect our use case. Alpine flavor
 is chosen to minimize the image size.

IMPORTANT: image reduce user privileges for security reasons to `nobody` user. If you find a permission error
 when trying to write files or access some resources, this is probably the reason. Configure it properly
 but does not remove that to run as root. A container running as root could lead to security issues also outside
 the container.

## Demo Extra Notes
