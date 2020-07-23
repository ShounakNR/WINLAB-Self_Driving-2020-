import os
import glob
import argparse
import struct
import datetime
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torchvision.transforms import ToTensor
import time
from collections import OrderedDict
from torch.utils.data import Dataset, DataLoader,TensorDataset
from model import Net
from loader import drivingData
from torch.utils.data.sampler import SubsetRandomSampler

timestr='%Y-%m-%d_%H-%M-%S'

magic_word=[1, 9, 8, 3]

image_size=424*240*3

def train(model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        #print data,target
        data, target = data.to(device), target.to(device)
        #print data.shape(),target.shape()
        optimizer.zero_grad()
        output  = model(data)
        #target = target.long()
        #loss = F.nll_loss(output, target, reduction='sum').item() # sum up batch loss
        criterion = nn.MSELoss() # sum up batch loss
        #target = target.long()
        loss = criterion(output,target)
        #loss = nn.NLLLoss()
        #l = loss(output,long(target))
        loss.backward()
        optimizer.step()
        #print output.shape,target.shape
        
        if True:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))

def test( model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item() # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True) # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()
    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

def main():
    parser = argparse.ArgumentParser(description="Create Dataset from directory")
    parser.add_argument("epochs", default=2, help="number of epochs")
    parser.add_argument("data_dir", help="Directory of npz files")
    parser.add_argument("weights_path", help="directory having the weights after being trined", default="" )
    args = parser.parse_args()

    #epochs = 10
    lr = 0.05
    no_cuda = True
    save_model = False
    use_cuda = not no_cuda and torch.cuda.is_available()
    torch.manual_seed(100)
    dev = torch.device("cpu")
  
    dataset = drivingData(args.data_dir)
    ntrain = len(dataset)
    indices = list(range(ntrain))
    train_sampler = SubsetRandomSampler(indices)
    train_loader=torch.utils.data.DataLoader(dataset, batch_size=32, sampler=train_sampler, num_workers=4)
    
    net=Net().to(device=dev)    
    optimizer = optim.SGD(net.parameters(), lr=lr, momentum=0.9, weight_decay=5e-4)
    
    for epoch in range(1, int(args.epochs) + 1):
        train( net, dev, train_loader, optimizer, epoch)
        #test( net, dev, test_loader)
    
    
    torch.save(net.state_dict(),os.path.join(args.weights_path, "weights.pt"))


if __name__ == '__main__':
    main()




