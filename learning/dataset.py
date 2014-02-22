""" 

"""

from __future__ import division

import logging
import cPickle as pickle
import gzip

import numpy as np

_logger = logging.getLogger(__name__)

class DataSet(object):
    pass

class ToyData(DataSet):
    def __init__(self, which_set='train'):
        _logger.info("generating toy data")

        self.which_set = which_set

        X = np.array(
            [[1., 1., 1., 1., 0., 0., 0., 0.],
             [0., 0., 0., 0., 1., 1., 1., 1.]], dtype='float32')
        Y = np.array([[1., 0.], [0., 1.]], dtype='float32')

        if which_set == 'train':
            self.X = np.concatenate([X]*10)
            self.Y = np.concatenate([Y]*10)
        elif which_set == 'valid':
            self.X = np.concatenate([X]*2)
            self.Y = np.concatenate([Y]*2)
        elif which_set == 'test':
            self.X = np.concatenate([X]*2)
            self.Y = np.concatenate([Y]*2)
        else:
            raise ValueError("Unknown dataset %s" % which_set)
        
        self.n_datapoints = self.X.shape[0]


class BarsData(DataSet):
    def __init__(self, which_set='train', n_datapoints=1000, D=5):
        _logger.debug("generating bars data")

        n_vis = D**2
        n_hid = 2*D
        bar_prob = 1./n_hid
        
        X = np.zeros((n_datapoints, D, D), dtype=np.float32)
        Y = 1. * (np.random.uniform(size=(n_datapoints, n_hid)) < bar_prob)

        for n in xrange(n_datapoints):
            for d in xrange(D):
                if Y[n,d] > 0.5:
                    X[n,d,:] = 1.0
                if Y[n,D+d] > 0.5:
                    X[n,:,d] = 1.0

        self.X = X.reshape((n_datapoints, n_vis)).astype(np.float32)
        self.Y = Y.astype(np.float32)
        self.n_datapoints = n_datapoints
          

class MNIST(DataSet):
    def __init__(self, which_set='train', fname="mnist.pkl.gz"):
        _logger.info("loading MNIST data")

        with gzip.open(fname) as f:
            (train_x, train_y), (valid_x, valid_y), (test_x, test_y) = pickle.load(f)

        if which_set == 'train':
            self.X, self.Y = self.preprocess(train_x, train_y)
        elif which_set == 'valid':
            self.X, self.Y = self.preprocess(valid_x, valid_y)
        elif which_set == 'test':
            self.X , self.Y  = self.preprocess(test_x, test_y)
        else:
            raise ValueError("Unknown dataset %s" % which_set)
 
        self.n_datapoints = self.X.shape[0]

    def preprocess(self, x, y):
        N = x.shape[0]
        assert N == y.shape[0]
    
        perm = np.random.permutation(N)
        x = x[perm,:]
        y = y[perm]

        x = 1.*(x > 0.5)       # binarize x

        one_hot = np.zeros( (N, 10), dtype="float32")
        for n in xrange(N):
            one_hot[n, y[n]] = 1.

        return x.astype('float32'), one_hot.astype('float32')

def permute_cols(x, idx=None):
    if isinstance(x, list) or isinstance(x, tuple):
        if idx is None:
            _, n_vis = x[0].shape
        idx = np.random.permutation(n_vis)
        return [permute(i, idx) for i in x]
    
    if idx is None:
        _, n_vis = x.shape
        idx = np.random.permutation(n_vis)
    return x[:,idx]

       