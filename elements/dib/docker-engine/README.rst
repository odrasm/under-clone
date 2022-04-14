=========
docker-ce
=========
This is the docker-ce element.

This element install Docker CE as described in the official
Docker documentation: https://docs.docker.com/install/.

Environment Variables
---------------------

DIB_DOCKER_VERSION
  :Required: No
  :Description: Install a specific version of Docker Engine.
  :Example: ``DIB_DOCKER_VERSION=19.03.5``

DIB_DOCKER_LOCK
  :Required: No
  :Default: ``true`` if DIB_DOCKER_VERSION is not empy, ``false`` otherwise.
  :Description: Prevent automatic upgrade of Docker Engine packages.

DIB_DOCKER_DAEMON_JSON_FILE
  :Required: No
  :Default: ``/etc/docker/daemon.json``
  :Description: Full path of Docker daemon.json.

DIB_DOCKER_DAEMON_JSON
  :Required: No
  :Default: {}
  :Description: JSON values to inject into the daemon.json file.

DIB_DOCKER_DAEMON_JSON_APPEND
  :Required: No
  :Default: {}
  :Description: JSON values to append to the daemon.json file.
