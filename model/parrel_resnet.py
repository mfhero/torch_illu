#!/usr/bin/env python
##########################################################
# File Name: parrel_resnet.py
# Author: gaoyu
# mail: gaoyu14@pku.edu.cn
# Created Time: 2018-05-10 22:17:30
##########################################################

import torch
import torch.nn as nn

from torchvision.models.resnet import BasicBlock, ResNet, model_zoo, model_urls

class Discriminator(ResNet):
    def __init__(self, ngpu):
        ResNet.__init__(self, BasicBlock, [3, 4, 6, 3])
        self.load_state_dict(model_zoo.load_url(model_urls['resnet34']))
        self.ngpu = ngpu
        self.output = nn.Sequential(
                  nn.Linear(512, 1),
                  nn.Sigmoid()
                )
        #self.output = nn.Sequential(
        #          nn.Conv2d(512, 32, 1, 1, 0, bias = True),
        #          nn.LeakyReLU(0.2, inplace=True),
        #          nn.MaxPool2d(7, 1),
        #          nn.Conv2d(32, 1, 1, 1, 0, bias = True),
        #          nn.Sigmoid()
        #        )



    def main(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        return x

    def forward(self, x):
        x, y = torch.split(x, 3, dim = 1)
        x = self.main(x)
        #y = self.main(y)
        #z = torch.cat([x, y], dim = 1)
        #z = self.output(z)
        z = self.output(x)

        return z
