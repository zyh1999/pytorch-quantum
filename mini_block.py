import torch.nn as nn
import torchquantum as tq
import torchquantum.functional as tqf
import numpy as np

from typing import Iterable
from torchquantum.plugins.qiskit_macros import QISKIT_INCOMPATIBLE_FUNC_NAMES
from torchpack.utils.logging import logger




class QuantumModuleFromOps(tq.QuantumModule):
    def __init__(self, ops):
        super().__init__()
        self.ops = tq.QuantumModuleList(ops)

    @tq.static_support
    def forward(self, q_device: tq.QuantumDevice):
        self.q_device = q_device
        for op in self.ops:
            op(q_device)



class RandomLayer(tq.QuantumModule):
    def __init__(self,
                 wires,
                 n_depth=None,
                 op_types=[tq.RX, tq.RY, tq.RZ, tq.Hadamard, tq.I, tq.CNOT],
                 seed=None,
                 ):
        super().__init__()
        self.n_depth = n_depth
        self.n_wires = len(wires)
        self.op_types= op_types
        self.gate_que=[]

        self.seed = seed
        self.op_list = tq.QuantumModuleList()
        if seed is not None:
            np.random.seed(seed)
        self.op_list = tq.QuantumModuleList()    
        self.build_block_layer()

    def build_block_layer(self):
        i=0
        while i <(self.n_depth*(self.n_wires)):
            idx = np.random.randint(0,len(self.op_types)-1)
            op = self.op_types[idx]
            self.gate_que.append(idx)
            op_wires = i % (self.n_wires)
            if idx==(len(self.op_types)-1):  #if it is CNOT, need 2 wires
                if op_wires!=0:
                    op=tq.I
                    self.gate_que.pop()
                    self.gate_que.append(4)   #delete tq.CNOT, add tq.I
                else:
                    op_wires =[0,1]
                    i=i+1
            if op().name in tq.Operator.parameterized_ops:
                operation = op(has_params=True, trainable=True, wires=op_wires)
            else:
                operation = op(wires=op_wires)
            self.op_list.append(operation)

            i=i+1
        
        op_ctr = tq.CZ    
        ctr_idx = np.random.randint(self.n_wires-2,self.n_wires-1)
        be_ctr_idx_list =list(range(self.n_wires-1))
        be_ctr_idx_list.remove(ctr_idx)
        be_ctr_idx = np.random.choice(be_ctr_idx_list)
        
        operation_ctr_after = op_ctr(wires=[ctr_idx, be_ctr_idx])
        self.op_list.append(operation_ctr_after)
    @tq.static_support
    def forward(self, q_device: tq.QuantumDevice):
        self.q_device = q_device
        for op in self.op_list:
            op(q_device)
