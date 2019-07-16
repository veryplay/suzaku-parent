#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from suzaku_driver.drivers.ipmitool import IPMITool


logger = logging.getLogger(__name__)

OUT_OF_BOND_ADAPTERS = [ IPMITool ]

class OutOfBondAdapterFactory(object):

    def __init__(self, engine):
        self.engine = engine
    
    def get_out_of_bond_adapter(self, out_of_bond_type = 'ipmi'):
        for ooba in OUT_OF_BOND_ADAPTERS:
            if (ooba.OUT_OF_BOND_PROTOCOL == out_of_bond_type):
                return ooba(self.engine)
        logger.warn("out of bond protocol `%(out_of_bond_type)s` not support, \
            use default protocol `ipmi`." % {
            "out_of_bond_type" : out_of_bond_type})
        engine = self.engine
        return IPMITool(engine)
