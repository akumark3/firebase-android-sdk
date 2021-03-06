# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import os
import requests

_logger = logging.getLogger('fireci.uploader')


def post_report(test_report, metrics_service_url, access_token):
  """Post a report to the metrics service backend."""

  endpoint = _construct_request_endpoint()
  headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
  data = json.dumps(test_report)

  _logger.info('Posting to the metrics service ...')
  _logger.info(f'Request endpoint: {endpoint}')
  _logger.info(f'Request data: {data}')

  request_url = f'{metrics_service_url}{endpoint}'
  result = requests.post(request_url, data=data, headers=headers)

  _logger.info(f'Response: {result.text}')


def _construct_request_endpoint():
  repo_owner = os.getenv('REPO_OWNER')
  repo_name = os.getenv('REPO_NAME')
  branch = os.getenv('PULL_BASE_REF')
  base_commit = os.getenv('PULL_BASE_SHA')
  head_commit = os.getenv('PULL_PULL_SHA')
  pull_request = os.getenv('PULL_NUMBER')

  commit = head_commit if head_commit else base_commit

  endpoint = f'/repos/{repo_owner}/{repo_name}/commits/{commit}/reports?branch={branch}'
  if pull_request:
    endpoint += f'&pull_request={pull_request}&base_commit={base_commit}'

  return endpoint
