
import numpy as np

from learning.dataset import BarsData, FromModel, MNIST
from learning.stbp_layers import  STBPStack, SigmoidBeliefLayer, FactoizedBernoulliTop
from learning.training import Trainer
from learning.termination import LogLikelihoodIncrease, EarlyStopping
from learning.monitor import MonitorLL, DLogModelParams, SampleFromP

n_vis = 28*28

dataset = MNIST(which_set='salakhutdinov_train', n_datapoints=59000)
valiset = MNIST(which_set='salakhutdinov_valid', n_datapoints=1000)
smallset = MNIST(which_set='salakhutdinov_valid', n_datapoints=100)
testset = MNIST(which_set='test', n_datapoints=10000)

layers=[
    SigmoidBeliefLayer( 
        unroll_scan=1,
        n_lower=n_vis,
        n_qhid=400,
    ),
    FactoizedBernoulliTop(
        n_lower=200,
    )
]

model = STBPStack(
    layers=layers
)

trainer = Trainer(
    n_samples=5,
    learning_rate_p=1e-3,
    learning_rate_q=1e-3,
    learning_rate_s=1e-3,
    layer_discount=0.50,
    batch_size=10,
    dataset=dataset, 
    model=model,
    termination=EarlyStopping(),
    final_monitors=[MonitorLL(data=testset, n_samples=[1, 5, 25, 100, 500])],
    epoch_monitors=[MonitorLL(data=valiset, n_samples=100), DLogModelParams()],
    step_monitors=[MonitorLL(data=smallset, n_samples=[1, 5, 25, 100]), SampleFromP(n_samples=100)],
    monitor_nth_step=100,
)