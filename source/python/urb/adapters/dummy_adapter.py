#!/usr/bin/env python

# Copyright 2017 Univa Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from urb.adapters.adapter_interface import Adapter
from urb.log.log_manager import LogManager
import gevent
import subprocess

class DummyAdapter(Adapter):
    """ Dummy Adapter class. """

    DELETE_WAIT_PERIOD_IN_SECONDS = 2.0

    def __init__(self):
        self.logger = LogManager.get_instance().get_logger(
            self.__class__.__name__)
        self.channel_name = None
        self.pids = []
        self.processes = []
        self.configure()

    def configure(self):
        self.logger.debug('configure')

    def set_channel_name(self, channel_name):
        self.logger.debug('set_channel_name')
        self.channel_name = channel_name

    def authenticate(self, request):
        self.logger.debug('Authenticate: %s' % request)

    def deactivate_framework(self, request):
        self.logger.debug('Deactivate framework: %s' % request)

    def exited_executor(self, request):
        self.logger.debug('Exited executor: %s' % request)

    def kill_task(self, request):
        self.logger.debug('Kill task: %s' % request)

    def launch_tasks(self, framework_id, tasks, *args, **kwargs):
        self.logger.debug('Launch tasks for framework id: %s' % framework_id)

    def reconcile_tasks(self, request):
        self.logger.debug('Reconcile tasks: %s' % request)

    def register_executor_runner(self, framework_id, slave_id, *args,
            **kwargs):
        self.logger.debug(
            'Register executor runner for framework id %s, slave id %s' %
            (framework_id, slave_id))

    def register_framework(self, max_tasks, concurrent_tasks, framework_env, user=None, *args, **kwargs):
        self.logger.info("register_framework: max_tasks=%s, concurrent_tasks=%s, framework_env=%s, user=%s, kwargs: %s" %
                         (max_tasks, concurrent_tasks, framework_env, user, kwargs))
        cmd="/scratch/urb/etc/urb-executor-runner"
        job_ids = set([])
        for i in range(0,concurrent_tasks):
            if i >= max_tasks:
                break
            self.logger.info('Submit job: user=%s, command: %s' % (user, cmd))
            p = subprocess.Popen([cmd])
            pid = p.pid
            job_ids.add(pid)
        return job_ids

    def register_slave(self, request):
        self.logger.debug('Register slave: %s' % request)

    def reregister_framework(self, request):
        self.logger.debug('Reregister framework: %s' % request)

    def reregister_slave(self, request):
        self.logger.debug('Reregister slave: %s' % request)

    def resource_request(self, request):
        self.logger.debug('Resource request: %s' % request)

    def revive_offers(self, request):
        self.logger.debug('Revive offers: %s' % request)

    def submit_scheduler_request(self, request):
        self.logger.debug('Submit scheduler request: %s' % request)

    def status_update_acknowledgement(self, request):
        self.logger.debug('Status update acknowledgement: %s' % request)

    def status_update(self, request):
        self.logger.debug('Status update: %s' % request)

    def scale(self, framework, count):
        self.logger.debug('scale: framework=%s, count=%s' % (framework, count))

    def unregister_framework(self, framework):
        self.logger.debug('Unregister framework: %s' % framework['name'])
        self.delete_jobs_delay(framework)

    def delete_jobs_delay(self, framework):
        # Delete all jobs
        job_ids = framework.get('job_id')
        if job_ids is not None:
            # Spawn job to make sure the actual executors exit...
            gevent.spawn(self.delete_jobs, job_ids)

    def delete_jobs(self, job_ids):
        for job_id in job_ids:
            try:
                self.delete_job(job_id)
            except Exception, ex:
                self.logger.warn("Error deleteing job: %s" % ex)

    def delete_job(self, job_id):
        if len(str(job_id)) != 0:
            try:
                self.logger.debug('Request deleting job: %s', job_id)
                subprocess.Popen(["kill", str(job_id)])
            except Exception, ex:
                self.logger.warn("Error requesting deleting job: %s" % ex)
            gevent.sleep(DummyAdapter.DELETE_WAIT_PERIOD_IN_SECONDS)
            try:
                self.logger.debug('Deleting job: %s', job_id)
                subprocess.call(["kill", "-9", str(job_id)])
            except Exception, ex:
                self.logger.warn("Error deleting job: %s" % ex)
        else:
            self.logger.warn("Deleting job: '%s' - empty job id string", job_id)

    def get_job_id_tuple(self, job_id):
        # Try to get job status and extract task array info
        # If things do not work, assume no task array
        return (job_id,None,None)

    def get_job_status(self, job_id):
        self.logger.debug('Getting status for job: %s', job_id)

    def unregister_slave(self, request):
        self.logger.debug('Unregister slave: %s' % request)


# Testing
if __name__ == '__main__':
    adapter = DummyAdapter()
    print 'Done'


