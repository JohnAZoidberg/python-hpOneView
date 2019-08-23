# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

import logging

from hpOneView.resources.resource import ResourceClient

logger = logging.getLogger(__name__)


class FirmwareBundles(object):
    """
    Firmware Bundles API client.

    """
    URI = '/rest/firmware-bundles'

    def __init__(self, con):
        self._connection = con
        self._bundle_client = ResourceClient(con, self.URI)
        self._compsig_client = ResourceClient(con, '{}/addCompsig'.format(self.URI))

    def upload(self, file_path, timeout=-1, compsig_path=None):
        """
        Upload an SPP ISO image file or a hotfix file to the appliance.
        The API supports upload of one hotfix at a time into the system.
        For the successful upload of a hotfix, ensure its original name and extension are not altered.

        Args:
            file_path: Full path to firmware.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            compsig_path: Full path to the signature of the bundle. If omitted OneView might complain abouto missing signature.

        Returns:
          (dict, dict): Information about the updated firmware bundle and potential compsig signature.
        """
        bundle_res = self._bundle_client.upload(file_path, timeout=timeout)

        if compsig_path is None:
            return (bundle_res, None)

        if self._connection._apiVersion < 1000:
            logger.warning('API Version {} does not support compsig upload. Skipping it.'.format(
                self._connection._apiVersion))
            return (bundle_res, None)

        compsig_res = self._compsig_client.upload(compsig_path, timeout=timeout)

        return (bundle_res, compsig_res)
