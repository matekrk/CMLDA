import nn
import numpy as np
import pandas as pd

###########################################################
# EXPERIMENTAL SETUP

dataset, nfolds, ntrials = 1, 5, 1
split_percentage = 0.8
epochs = 1000

pars = {}

###########################################################
# LOADING DATASET

fpath = '../../data/monks/'
preliminary_path = '../images/monks_preliminary_trials/'

names = ['monks-1_train',
         'monks-1_test',
         'monks-2_train',
         'monks-2_test',
         'monks-3_train',
         'monks-3_test']

datasets = {name: pd.read_csv(fpath+name+'_bin.csv').values
            for name in names}

design_set = datasets['monks-{}_train'.format(dataset)]
test_set = datasets['monks-{}_test'.format(dataset)]

y_design, X_design = np.hsplit(design_set, [1])
y_test, X_test = np.hsplit(test_set, [1])

# simmetrized X_design:
X_design = (X_design*2-1)
X_test = (X_test*2-1)
design_set = np.hstack((y_design, X_design))
test_set = np.hstack((y_test, X_test))

###########################################################
# DATASET PARTITIONING

np.random.shuffle(design_set)

training_set = design_set[:int(design_set.shape[0]*split_percentage), :]
validation_set = design_set[int(design_set.shape[0]*split_percentage):, :]

y_training, X_training = np.hsplit(training_set, [1])
y_validation, X_validation = np.hsplit(validation_set, [1])

###########################################################
# NETWORK INITIALIZATION

neural_net = nn.NeuralNetwork(X_training, y_training, hidden_sizes=[10],
                              activation='sigmoid')

###########################################################
# PRELIMINARY TRAINING

opt = raw_input("Choose an optimizer: (sgd/cgd)")

if opt == 'sgd':
    pars = {'batch_size': X_training.shape[0],
            'eta': 0.5,
            'momentum': {'type': 'standard', 'alpha': 0.},
            'reg_lambda': 0.0,
            'reg_method': 'l2'}
else:
    pars = {'max_epochs': epochs,
            'error_goal': 1e-4,
            'beta_m': 'mhs',
            'd_m': 'standard',
            'plus': True,
            'strong': True,
            'rho': 0.0}

neural_net.train(neural_net, X_training, y_training, opt, epochs, X_validation,
                 y_validation, pars)
