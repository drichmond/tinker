# ----------------------------------------------------------------------
# Copyright (c) 2016, The Regents of the University of California All
# rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     * Neither the name of The Regents of the University of California
#       nor the names of its contributors may be used to endorse or
#       promote products derived from this software without specific
#       prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL REGENTS OF THE
# UNIVERSITY OF CALIFORNIA BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.
# ----------------------------------------------------------------------
# Filename: DDR.py
# Version: 0.1 
# Description: Object that defines a DDR Memory Instance/Interface in a Board
# architecture
# Author: Dustin Richmond
import xml.etree.ElementTree as ET
import Tinker, Phy
from IP import parse_int
class DDR(Phy.Phy):
    _C_BURST_WIDTHS = range(1,5)
    _C_BURST_DEFAULT = 4
    _C_CLOCK_RATIOS = ["Half", "Quarter", "Full"]
    _C_RATE = 2 # Double Data Rate
    
    def __init__(self, e):
        super(DDR,self).__init__(e)

    @classmethod
    def validate(cls, d):
        """

        Validate the parameters that describe the intrinsic settings of
        this IP

        Arguments:

        d -- A Description object, containing the parsed user description
        of a custom board
        
        """
        d = super(DDR,cls).validate(d)
        return

    @classmethod
    def parse(cls,e):
        """
        Parse the description of this IP object from an element tree
        element and return a dictionary with the parameters
        found.

        Arguments:

        e -- An element tree element containing the description of this
        object
        
        """
        d = super(DDR,cls).parse(e)
        d["type"] = "DDR3"
        pow2_dq_pins = d["pow2_dq_pins"]

        bank_pins = parse_int(e, "bank_pins")
        column_pins = parse_int(e, "column_pins")
        row_pins = parse_int(e, "row_pins")

        size = pow2_dq_pins/8 * (2**bank_pins) * (2 ** column_pins) * (2 ** row_pins)
        d["size"] = int(size)

        return d

    def get_interface_element(self, sid, version, verbose):
        self.validate(self)
        e = super(DDR,self).get_interface_element(sid, version, verbose)
        e.set("size", str(hex(self["size"])))
        e.set("port","kernel_%s_if_%s_rw" % (sid,self["id"]))
        return e
