#!/usr/bin/env python
###
# (C) Copyright (2012-2015) Hewlett Packard Enterprise Development LP
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
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import range
from future import standard_library
standard_library.install_aliases()
import sys
import re

PYTHON_VERSION = sys.version_info[:3]
PY2 = (PYTHON_VERSION[0] == 2)
if PY2:
    if PYTHON_VERSION < (2, 7, 9):
        raise Exception('Must use Python 2.7.9 or later')
elif PYTHON_VERSION < (3, 4):
    raise Exception('Must use Python 3.4 or later')

import hpOneView as hpov
from pprint import pprint


def acceptEULA(con):
    # See if we need to accept the EULA before we try to log in
    con.get_eula_status()
    try:
        if con.get_eula_status() is True:
            print('EULA display needed')
            con.set_eula('no')
    except Exception as e:
        print('EXCEPTION:')
        print(e)


def login(con, credential):
    # Login with givin credentials
    try:
        con.login(credential)
    except:
        print('Login failed')


def add_san_manager(fcs, sanmgr, port, user, passwd, ssl):
    providers = fcs.get_providers()
    for provider in providers:
        if provider['displayName'] == 'Brocade Network Advisor':
            uri = provider['deviceManagersUri']

    if not uri:
        print('ERROR, Brocade Network Advisor Provider not found')

    connInfo = hpov.make_connectionInfo_dict(sanmgr, port, user, passwd, ssl)
    ret = fcs.add_device_manager(uri, connInfo)
    print(ret)


def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Add a new SAN Manager

    Usage: ''')
    parser.add_argument('-a', dest='host', required=True,
                        help='''
    HPE OneView Appliance hostname or IP address''')
    parser.add_argument('-u', dest='user', required=False,
                        default='Administrator',
                        help='''
    HPE OneView Username''')
    parser.add_argument('-p', dest='passwd', required=True,
                        help='''
    HPE OneView Password''')
    parser.add_argument('-c', dest='cert', required=False,
                        help='''
    Trusted SSL Certificate Bundle in PEM (Base64 Encoded DER) Format''')
    parser.add_argument('-y', dest='proxy', required=False,
                        help='''
    Proxy (host:port format''')
    parser.add_argument('-j', dest='domain', required=False,
                        default='Local',
                        help='''
    HPE OneView Authorized Login Domain''')
    parser.add_argument('-sm', dest='sanmgr',
                        required=True,
                        help='''
    FQDN or IP Address of the SAN Manager''')
    parser.add_argument('-so', dest='port',
                        required=False,
                        default=5989,
                        help='''
    TCP Port of the SAN Manager

    Default: 5989''')
    parser.add_argument('-su', dest='suser',
                        required=True,
                        help='''
    Username used to authenticate and manage the SAN Manager''')
    parser.add_argument('-sp', dest='spass',
                        required=True,
                        help='''
    Password used to authenticate and manage the SAN Manager''')
    parser.add_argument('-e', dest='ssl',
                        required=False,
                        action='store_true',
                        help='''
    Use to enable SSL communication with the SAN Manager''')

    args = parser.parse_args()
    credential = {'authLoginDomain': args.domain.upper(), 'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    fcs = hpov.fcsans(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    add_san_manager(fcs, args.sanmgr, args.port, args.suser,
                    args.spass, args.ssl)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
