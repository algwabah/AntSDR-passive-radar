#
# Copyright 2017 Ettus Research, a National Instruments Company
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
periph_manager __init__.py
"""

__version__ = "..."
__githash__ = ""
__mpm_device__ = "sim"

from .base import PeriphManagerBase

# This is where the import magic happens
from .sim import sim as periph_manager
