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


# if image name changed here it has to be updated in Vagrantfile
IMAGE=urb-build

.PHONY:all

all:
	docker images $(IMAGE) | grep $(IMAGE) >/dev/null 2>&1 || docker build --rm -t $(IMAGE) .

.PHONY:clean
clean:
	IM=$$(docker ps | awk '/$(IMAGE)/ {print $$$\1}'); if [ ! -z "$$IM" ]; then docker stop $$IM; fi
	IM=$$(docker ps -a| awk '/$(IMAGE)/ {print $$$\1}'); if [ ! -z "$$IM" ]; then docker rm $$IM; fi
	-docker rmi $(IMAGE)

