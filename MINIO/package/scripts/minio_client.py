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
from resource_management import Script
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute, File
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions import Direction
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions import StackFeature
from resource_management.libraries.functions.stack_features import check_stack_feature
from resource_management.libraries.functions.show_logs import show_logs

from minio import minio
from minio import ensure_base_directories


class MinioClient(Script):

    def install(self, env):
        config = Script.get_config()
        Logger.info("config['clusterHostInfo']: {0} ".format(config['clusterHostInfo']))
        import params
        self.install_packages(env)
	minio_cmd = format('{params.minio_install_dir}/bin/mc config host add s3 http://{params.network_host}:{params.minio_port} {params.minio_root_user} {params.minio_root_password} --api s3v4')
	Execute(minio_cmd,
		user='root',
	       )
        env.set_params(params)

        Logger.info(format("Install minio client success"))

    def configure(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        minio(upgrade_type=upgrade_type)
	
        Logger.info(format("Configure minio server success"))

    def start(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        self.configure(env, upgrade_type=upgrade_type)

    def stop(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        ensure_base_directories()

    def status(self, env):
	raise ClientComponentHasNoStatus()

    def get_log_folder(self):
        import params
        return params.minio_log_dir

    def get_user(self):
        import params
        return params.minio_user


if __name__ == "__main__":
    MinioClient().execute()
