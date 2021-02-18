==========
cloud-user
==========

Configure custom Cloud-init default user. The following environment variables
can be useful for configuration:

Environment Variables
---------------------

DIB_CLOUD_INIT_DEFAULT_USER_NAME
  :Required: No
  :Default: cloud
  :Description: Username for the cloud-init user.

DIB_CLOUD_INIT_DEFAULT_USER_SHELL
  :Required: No
  :Default: /bin/bash
  :Description: Full path for the shell of the user. Note that this does not
    install the (possibly) required shell package.

DIB_CLOUD_INIT_DEFAULT_USER_PASSWORD
  :Required: No
  :Default: Password is disabled
  :Description: Set the default password for this user. This is a fairly
    insecure method of setting the password and is not advised.

DIB_CLOUD_INIT_DEFAULT_USER_GECOS
  :Required: No
  :Default: None
  :Description: A short description of the login.

DIB_CLOUD_INIT_CONFIG_FILE
  :Required: No
  :Default: /etc/cloud/cloud.cfg
  :Description: Full path for the clouf-init configuration file.

DIB_CLOUD_INIT_ENABLE_SSH_PASSWORD
  :Required: No
  :Default: False
  :Description: Enable the SSH daemon password authentication.

DIB_CLOUD_INIT_DISABLE_ROOT
  :Required: No
  :Default: True
  :Description: Prevent the root user to access via SSH.

DIB_CLOUD_INIT_VERSION
  :Required: No
  :Default: None
  :Description: Install specific git branch or tag of cloud-init.
