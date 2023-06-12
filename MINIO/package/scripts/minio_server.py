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


class MinioServer(Script):

    def install(self, env):
        config = Script.get_config()
        Logger.info("config['clusterHostInfo']: {0} ".format(config['clusterHostInfo']))
        import params
        self.install_packages(env)
        env.set_params(params)

        Logger.info(format("Install minio server success"))

    def configure(self, env, upgrade_type=None):
        import params
        env.set_params(params)
        minio(upgrade_type=upgrade_type)
        Logger.info(format("Configure minio server success"))

    def start(self, env, upgrade_type=None):
        import params
	import commands
	import sys
        env.set_params(params)
        self.configure(env, upgrade_type=upgrade_type)
	cmd = """ps -e|grep minio"""
	_,minio_pid = commands.getstatusoutput(cmd)
	if minio_pid != "":
	    Logger.info(format("The Minio Server is running"))
	    sys.exit()
	daemon_cmd = format('{params.minio_run_file}')
        no_op_test = format(
            'ls {params.minio_pid_file} >/dev/null 2>&1 && ps -p `cat {params.minio_pid_file}` >/dev/null 2>&1')
        try:
            Execute(daemon_cmd,
                    user='root',
                    not_if=no_op_test
                    )
        except Exception:
            show_logs(params.minio_log_dir, 'root')
            raise

        Logger.info(format("Start minio server success"))

    def stop(self, env, upgrade_type=None):
        import params
	import commands
        env.set_params(params)
        # minio stop flowing
        ensure_base_directories()
	minio_pid = format('ps -e|grep `cat {params.minio_pid_file}`')
	pid = format('cat {params.minio_pid_file}')
	_, PID = commands.getstatusoutput(pid)
	_, MINIO_PID = commands.getstatusoutput(minio_pid)
	if MINIO_PID == "":
	    Logger.info(format("The Minio server is not running"))
	else:
            daemon_cmd = format('kill -9 ' + PID + " && sleep 5")
            try:
                Execute(daemon_cmd,
                        user='root',
                        )
            except Exception:
                show_logs(params.minio_log_dir, 'root')
                raise

            Logger.info(format("stop minio server success"))

    def status(self, env):
        import status_params
        env.set_params(status_params)
        check_process_status(status_params.minio_pid_file)

    def get_log_folder(self):
        import params
        return params.minio_log_dir

    def get_user(self):
        import params
        return params.minio_user


if __name__ == "__main__":
    MinioServer().execute()
