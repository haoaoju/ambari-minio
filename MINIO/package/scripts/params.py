#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import os
from resource_management.libraries.functions import format
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.version import format_stack_version
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.get_stack_version import get_stack_version
from resource_management.libraries.functions.is_empty import is_empty
import status_params
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions import conf_select
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources
import socket

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()
stack_name = default("/hostLevelParams/stack_name", None)


stack_version_unformatted = config['serviceLevelParams']['version']
stack_version_formatted = format_stack_version(stack_version_unformatted)

print "------------------------------------"
print "server configuratioins : %s %s" % (stack_root, stack_name)
print "------------------------------------"

# Version being upgraded/downgraded to
version = default("/commandParams/version", stack_version_formatted)

# hostname = config['hostname']
hostname = config['agentLevelParams']['hostname'].lower()

print "------------------------------------"
print "hostname : %s %s" % (hostname, version)   # hostname : master 3.0.0.0-512
print "------------------------------------"

# default minio parameters
limits_conf_dir = "/etc/security/limits.d"

minio_user_nofile_soft = config['configurations']['minio-env']['minio_user_nofile_soft']
minio_user_nofile_hard = config['configurations']['minio-env']['minio_user_nofile_hard']
minio_user = config['configurations']['minio-env']['minio_user']
minio_group = config['configurations']['minio-env']['minio_group']

minio_pid_dir = status_params.minio_pid_dir
minio_pid_file = minio_pid_dir + "/minio-server.pid"

# minio log configuratioins
minio_log_dir = config['configurations']['minio-env']['minio_log_dir']

minio_log_file = default('/configurations/minio-env/minio_log_file', minio_log_dir + '/minio.log')


# minio cluster configurations
minio_hosts = config['clusterHostInfo']['minio_server_hosts']
minio_hosts.sort()

print "------------------------------------"
print "------------------------------------"

# minio-config.xml
minio_port = config['configurations']['minio-config']['minio_port']
minio_console_port = config['configurations']['minio-config']['minio_console_port']
paths = config['configurations']['minio-config']['path']
minio_config = ""
for minio_host in minio_hosts:
    for path in paths.split(","):
        minio_config = minio_config + "http://" + minio_host + ":" + minio_port + "/" + path + " "
    
minio_root_user = config['configurations']['minio-user']['MINIO_ROOT_USER']

minio_root_password = config['configurations']['minio-user']['MINIO_ROOT_PASSWORD']



hdp_version = config['repositoryFile']['repoVersion']

minio_install_dir = "/usr/hdp/" + hdp_version + "/minio"
minio_run_dir = minio_install_dir + "/bin"
minio_run_file = minio_run_dir + "/startMinio.sh"


hostname = socket.gethostname()

ip = socket.gethostbyname(hostname)

network_host = ip

