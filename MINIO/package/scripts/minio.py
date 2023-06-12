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
import collections
import os

from resource_management.libraries.functions.version import format_stack_version
from resource_management.libraries.resources.properties_file import PropertiesFile
from resource_management.libraries.resources.template_config import TemplateConfig
from resource_management.core.resources.system import Directory, Execute, File, Link
from resource_management.core.source import StaticFile, Template, InlineTemplate
from resource_management.libraries.functions import format
from resource_management.libraries.functions.stack_features import check_stack_feature
from resource_management.libraries.functions import StackFeature
from resource_management.libraries.functions import Direction

from resource_management.core.logger import Logger


def minio(upgrade_type=None):
    import params
    ensure_base_directories()

    # minio server all configuration, return result type dict

    Directory(params.minio_log_dir,
              mode=0755,
              cd_access='a',
              owner=params.minio_user,
              group=params.minio_group,
              create_parents=True,
              recursive_ownership=True,
              )

    # On some OS this folder could be not exists, so we will create it before pushing there files
    Directory(params.limits_conf_dir,
              create_parents=True,
              owner='root',
              group='root'
              )

    File(os.path.join(params.limits_conf_dir, 'minio.conf'),
         owner='root',
         group='root',
         mode=0644,
         content=Template("minio.conf.j2")
         )
    File(os.path.join(params.minio_run_dir, 'startMinio.sh'),
	 owner='root',
         group='root',
         mode=0755,
         content=Template("startMinio.sh.j2")
	 )


def ensure_base_directories():
    import params
    Directory([params.minio_log_dir, params.minio_pid_dir, params.minio_run_dir],
              mode=0755,
              cd_access='a',
              owner=params.minio_user,
              group=params.minio_group,
              create_parents=True,
              recursive_ownership=True,
              )
    Directory(params.paths,
              mode=0755,
              cd_access='a',
              owner=params.minio_user,
              group=params.minio_group,
              create_parents=True,
              recursive_ownership=True,
              )
