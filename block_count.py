import torch.nn as nn
import torchquantum as tq
import torchquantum.functional as tqf
import numpy as np

from typing import Iterable
from torchquantum.plugins.qiskit_macros import QISKIT_INCOMPATIBLE_FUNC_NAMES
from torchpack.utils.logging import logger

class Block_Count(object):
    def __init__(self):
        self.times = 0
        self.tot_score=0.0
        self.avg=0.0

    def show(self):
        print(self.tot_score," / ",self.times," = ", self.avg)