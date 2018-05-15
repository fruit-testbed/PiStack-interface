#!/usr/bin/env python3
#Philip Basford
# 15/05/2018
"""
    Searches the first 16 addresses for pi stack boards and turns on all the pis
"""
import pistack.comms
C = pistack.comms.Comms("/dev/ttyUSB0")
for i in C.search(0, 16)[1]:
    for j in range(0, 2):
        C.pi_on(i, j)
