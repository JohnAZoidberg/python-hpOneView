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

from pprint import pprint

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Example updates - change to what you want to upload
spp_path = "SPPgen9snap6.2015_0405.81.iso"
patch_path = "CP036110.zip"
compsig_path = "CP036110.compsig"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)

# Upload a firmware bundle
print("\nUpload a firmware bundle")

# Upload an entire SPP
(bundle_information, compsig_information) = oneview_client.firmware_bundles.upload(file_path=spp_path)

print("\n Upload successful! Firmware information returned: \n")
pprint(bundle_information)

# Upload just a single patch
(bundle_information, compsig_information) = oneview_client.firmware_bundles.upload(
    file_path=patch_path, compsig_path=compsig_path)

print("\n Upload successful! Firmware information returned: \n")
pprint(bundle_information)
print("\n Firmware information returned: \n")
pprint(compsig_information)
