import matplotlib.pyplot as plt
from pytorch_lightning import LightningDataModule, LightningModule
import numpy as np
import torch
from collections import Counter
import torchvision
from torchvision import datasets, models, transforms
from torchvision import transforms
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning import LightningDataModule, LightningModule, Trainer,seed_everything
from torchinfo import summary
from torch import nn
import sys
import torchio as tio
from Models.unet3d import UNet3D
import sklearn
from pytorch_lightning import loggers as pl_loggers
import torchmetrics

## Model
class Classifier3D(LightningModule):
    def __init__(self, n_classes = 1, wf=5, depth=3):
        super().__init__()
        self.unet_model = UNet3D(in_channels=1, n_classes = n_classes, depth=depth,wf=wf)
        self.model      = torch.nn.Sequential(
            self.unet_model.encoder,
            torch.nn.Flatten(),
            #torch.nn.MaxPool3d((10,10,1)),
            #torch.nn.LazyLinear(128),
            #torch.nn.LazyLinear(n_classes)            
        )
        self.model.apply(self.weights_init)
        summary(self.model.to('cuda'), (3, 1, 20, 80,80),col_names = ["input_size","output_size"],depth=5)
        self.accuracy = torchmetrics.AUC(reorder=True)
        self.loss_fcn = torch.nn.BCEWithLogitsLoss()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch,batch_idx):
        image,label = batch
        prediction  = self.forward(image)
        loss = self.loss_fcn(prediction.flatten(), label.flatten())
        return {"loss":loss,"prediction":prediction.squeeze().detach(),"label":label} # NOTE: squeeze or flatten?

    def validation_step(self, batch,batch_idx):
        image,label = batch
        prediction  = self.forward(image)
        loss = self.loss_fcn(prediction.flatten(), label.flatten())
        return {"loss":loss,"prediction":prediction.squeeze().detach(),"label":label} # NOTE: squeeze or flatten?

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)
        return [optimizer], [scheduler]

    def weights_init(self,m):
        if isinstance(m, nn.Conv3d) or isinstance(m, nn.Linear):
            nn.init.xavier_uniform_(m.weight.data)
