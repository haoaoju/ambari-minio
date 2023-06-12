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
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.validate import call_and_match_output
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions.format import format
from resource_management.core.logger import Logger
from resource_management.core import sudo


class ServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)
	import commands

        # TODO, Minio Service check should be more robust , It should get all the broker_hosts
        # Produce some messages and check if consumer reads same no.of messages.
	print "------------------------------------"
	print "Create a storage bucket called miniochecktest on s3"
	print "------------------------------------"
	#miniochecktest_cmd = format('{params.minio_install_dir}/bin/mc ls s3/miniochecktest')
	#_,miniochecktest = commands.getstatusoutput(miniochecktest_cmd)
	#if miniochecktest != "":
	#    minio_rm = format('{params.minio_install_dir}/bin/mc rm --recursive --force s3/miniochecktest')
        #    Execute(minio_rm, user='root')
	minio_create = format('{params.minio_install_dir}/bin/mc mb --ignore-existing s3/miniochecktest')
	Execute(minio_create,user='root',)

	print "------------------------------------"
        print "Output Hello World to Amazon S3"
        print "------------------------------------"
	minio_pipe = format('echo "Hello World" | {params.minio_install_dir}/bin/mc pipe s3/miniochecktest/minio.txt')

	Execute(minio_pipe, user='root')

	print "------------------------------------"
        print "Display the content of the minio.txt file"
        print "------------------------------------"
	minio_cat = format('{params.minio_install_dir}/bin/mc cat s3/miniochecktest/minio.txt')	

	Execute(minio_cat, user='root')
	
	print "------------------------------------"
        print "Delete a storage bucket named miniochecktest on s3"
        print "------------------------------------"
        minio_rm = format('{params.minio_install_dir}/bin/mc rm --recursive --force s3/miniochecktest')
	Execute(minio_rm, user='root')


if __name__ == "__main__":
    ServiceCheck().execute()
