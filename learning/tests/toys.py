"""
"""

from __future__ import division


def get_toy_data():
    from learning.dataset import BarsData
    return BarsData(which_set="train", n_datapoints=500)

def get_toy_model():
    from learning.isws import ISStack
    from learning.sbn import SBN, SBNTop

    p_layers = [
        SBN( 
            n_X=25,
            n_Y=10
        ),
        SBNTop(
            n_X=10,
        )
    ]
    q_layers = [
        SBN(
            n_X=10,
            n_Y=25,
        )
    ]
    model = ISStack(
        p_layers=p_layers,
        q_layers=q_layers,
    )
    return model
