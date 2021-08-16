from torchquantum.operators import Observable
import torch
import torch.nn.functional as F
import torch.optim as optim
import argparse

import torchquantum as tq
import torchquantum.functional as tqf

from examples.core.datasets import MNIST
from torch.optim.lr_scheduler import CosineAnnealingLR
import mini_block as mb
from block_count import Block_Count
import mnist_example as me

Block_dict={}
iteration=10
def main():
    for i in range(iteration):
        acc, block_que = me.main()
        print(acc,block_que)
        for block in block_que:
            tmp = "".join(str(x) for x in block)
            if(Block_dict.get(tmp)  is None):
                Block_dict[tmp]=Block_Count()
            Block_dict[tmp].times = Block_dict[tmp].times + 1
            Block_dict[tmp].tot_score = Block_dict[tmp].tot_score + acc
            Block_dict[tmp].avg = Block_dict[tmp].tot_score / Block_dict[tmp].times
            print(tmp,':')
            Block_dict[tmp].show()
if __name__ == '__main__':
    main()


