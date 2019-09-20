FROM kennethreitz/pipenv as build

ADD . /priority
WORKDIR /priority

RUN pipenv install \
 && pipenv lock -r > requirements.txt \
 && pipenv run python setup.py bdist_wheel

FROM ubuntu:bionic
COPY --from=build /priority/dist/*.whl .
ARG DEBIAN_FRONTEND=noninteractive
RUN set -xe \
 && apt-get update -q \
 && apt-get install -y -q \
        python3-wheel \
        python3-pip \
        uwsgi-plugin-python3 \
 && python3 -m pip install *.whl \
 && apt-get remove -y python3-pip python3-wheel \
 && apt-get autoremove -y \
 && apt-get clean -y \
 && rm -f *.whl \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /priority \
 && useradd _uwsgi --no-create-home --user-group
USER _uwsgi
ENTRYPOINT ["/usr/bin/uwsgi", \
            "--master", \
            "--die-on-term", \
            "--plugin", "python3"]
CMD ["--http-socket", "0.0.0.0:8000", \
     "--processes", "4", \
     "--chdir", "/priority", \
     "--check-static", "static", \
     "--module", "priority:run"]
