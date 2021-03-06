from multiprocessing import freeze_support

import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import scipy.ndimage.filters

import dataset.cifar10_dataset

from network import activation
from network.layers.conv_to_fully_connected import ConvToFullyConnected
from network.layers.fully_connected import FullyConnected
from network.model import Model
from network.optimizer import GDMomentumOptimizer

if __name__ == '__main__':
    """
    Goal: Compare DFA and BP training performances with respect to validation/test loss, validation/test accuracy and 
    training time on a fully connected NN
    
    Initial learning rate, regularization and learning rate decay parameters were evaluated
    by hand by comparing the training performance on the validation set for various 
    parameter combinations
    
    DFA:
    ------------------------------------
    Result:
    ------------------------------------
    loss on test set: 1.4419548950901127
    accuracy on test set: 0.5045
    
    Train statisistics:
    ------------------------------------
    time spend during forward pass: 153.39858412742615
    time spend during backward pass: 196.8211522102356
    time spend during update pass: 246.54469919204712
    time spend in total: 1082.2560546398163
    
    BP:
    ------------------------------------
    Result:
    ------------------------------------
    loss on test set: 1.6210799549655157
    accuracy on test set: 0.4367
    
    Train statisistics:
    ------------------------------------
    time spend during forward pass: 142.29144406318665
    time spend during backward pass: 294.4345464706421
    time spend during update pass: 245.75644183158875
    time spend in total: 1178.3628904819489


    
    Train statistics DFA:
    ------------------------------------
    time spend during forward pass: 186.65376925468445
    time spend during backward pass: 196.10941076278687
    time spend during update pass: 144.07492351531982
    time spend in total: 752.406553030014
    Train statistics BP:
    ------------------------------------
    time spend during forward pass: 187.12717700004578
    time spend during backward pass: 331.23116517066956
    time spend during update pass: 152.84005665779114
    time spend in total: 911.1534883975983
    
    
    FINAL
    -------
    
    Run training:
    ------------------------------------
    
    train method: bp 
    num_passes: 20 
    batch_size: 64
    
    epoch 0, step 0, loss = 2.36856, accuracy = 0.078125
    epoch 0, step 10, loss = 2.33070, accuracy = 0.25
    epoch 0, step 20, loss = 2.29341, accuracy = 0.203125
    epoch 0, step 30, loss = 2.19480, accuracy = 0.15625
    epoch 0, step 40, loss = 2.12023, accuracy = 0.28125
    epoch 0, step 50, loss = 2.13472, accuracy = 0.171875
    epoch 0, step 60, loss = 1.98790, accuracy = 0.328125
    epoch 0, step 70, loss = 1.95530, accuracy = 0.453125
    epoch 0, step 80, loss = 1.87101, accuracy = 0.390625
    epoch 0, step 90, loss = 2.01716, accuracy = 0.328125
    epoch 0, step 100, loss = 2.04261, accuracy = 0.34375
    epoch 0, step 110, loss = 2.07406, accuracy = 0.25
    epoch 0, step 120, loss = 1.86095, accuracy = 0.328125
    epoch 0, step 130, loss = 2.02660, accuracy = 0.328125
    epoch 0, step 140, loss = 1.80717, accuracy = 0.328125
    epoch 0, step 150, loss = 1.85345, accuracy = 0.375
    epoch 0, step 160, loss = 1.83906, accuracy = 0.28125
    epoch 0, step 170, loss = 1.71188, accuracy = 0.390625
    epoch 0, step 180, loss = 2.10310, accuracy = 0.25
    epoch 0, step 190, loss = 1.78432, accuracy = 0.390625
    epoch 0, step 200, loss = 1.97146, accuracy = 0.3125
    epoch 0, step 210, loss = 1.89367, accuracy = 0.328125
    epoch 0, step 220, loss = 1.77708, accuracy = 0.359375
    epoch 0, step 230, loss = 2.03572, accuracy = 0.265625
    epoch 0, step 240, loss = 1.88240, accuracy = 0.390625
    epoch 0, step 250, loss = 1.89982, accuracy = 0.421875
    epoch 0, step 260, loss = 1.83349, accuracy = 0.421875
    epoch 0, step 270, loss = 1.80565, accuracy = 0.359375
    epoch 0, step 280, loss = 1.83763, accuracy = 0.296875
    epoch 0, step 290, loss = 1.82211, accuracy = 0.4375
    epoch 0, step 300, loss = 1.85196, accuracy = 0.34375
    epoch 0, step 310, loss = 1.85327, accuracy = 0.3125
    epoch 0, step 320, loss = 1.86922, accuracy = 0.296875
    epoch 0, step 330, loss = 1.78132, accuracy = 0.375
    epoch 0, step 340, loss = 1.65472, accuracy = 0.390625
    epoch 0, step 350, loss = 1.74728, accuracy = 0.328125
    epoch 0, step 360, loss = 1.90665, accuracy = 0.375
    epoch 0, step 370, loss = 1.89304, accuracy = 0.328125
    epoch 0, step 380, loss = 1.71951, accuracy = 0.421875
    epoch 0, step 390, loss = 1.85597, accuracy = 0.421875
    epoch 0, step 400, loss = 1.76186, accuracy = 0.421875
    epoch 0, step 410, loss = 1.90346, accuracy = 0.328125
    epoch 0, step 420, loss = 1.93908, accuracy = 0.265625
    epoch 0, step 430, loss = 1.84259, accuracy = 0.28125
    epoch 0, step 440, loss = 1.65759, accuracy = 0.40625
    epoch 0, step 450, loss = 1.91707, accuracy = 0.40625
    epoch 0, step 460, loss = 1.77191, accuracy = 0.390625
    epoch 0, step 470, loss = 1.73472, accuracy = 0.4375
    epoch 0, step 480, loss = 1.80021, accuracy = 0.375
    epoch 0, step 490, loss = 1.61381, accuracy = 0.484375
    epoch 0, step 500, loss = 2.04630, accuracy = 0.328125
    epoch 0, step 510, loss = 1.87204, accuracy = 0.3125
    epoch 0, step 520, loss = 2.01833, accuracy = 0.28125
    epoch 0, step 530, loss = 1.79319, accuracy = 0.4375
    epoch 0, step 540, loss = 1.65712, accuracy = 0.421875
    epoch 0, step 550, loss = 1.63366, accuracy = 0.46875
    epoch 0, step 560, loss = 1.60934, accuracy = 0.40625
    epoch 0, step 570, loss = 1.76193, accuracy = 0.359375
    epoch 0, step 580, loss = 1.81065, accuracy = 0.34375
    epoch 0, step 590, loss = 1.59149, accuracy = 0.5
    epoch 0, step 600, loss = 1.64252, accuracy = 0.375
    epoch 0, step 610, loss = 1.65348, accuracy = 0.375
    epoch 0, step 620, loss = 1.60320, accuracy = 0.46875
    epoch 0, step 630, loss = 1.95862, accuracy = 0.328125
    epoch 0, step 640, loss = 1.84979, accuracy = 0.34375
    epoch 0, step 650, loss = 1.57324, accuracy = 0.4375
    epoch 0, step 660, loss = 1.69854, accuracy = 0.4375
    epoch 0, step 670, loss = 1.61541, accuracy = 0.421875
    epoch 0, step 680, loss = 1.71702, accuracy = 0.359375
    epoch 0, step 690, loss = 1.66535, accuracy = 0.40625
    epoch 0, step 700, loss = 1.75665, accuracy = 0.40625
    validation after epoch 0: loss = 1.72863, accuracy = 0.3732
    epoch 1, step 710, loss = 1.62195, accuracy = 0.4375
    epoch 1, step 720, loss = 1.76492, accuracy = 0.390625
    epoch 1, step 730, loss = 1.78923, accuracy = 0.375
    epoch 1, step 740, loss = 1.72571, accuracy = 0.34375
    epoch 1, step 750, loss = 1.76658, accuracy = 0.328125
    epoch 1, step 760, loss = 1.60664, accuracy = 0.4375
    epoch 1, step 770, loss = 1.79709, accuracy = 0.328125
    epoch 1, step 780, loss = 1.64574, accuracy = 0.4375
    epoch 1, step 790, loss = 1.49913, accuracy = 0.53125
    epoch 1, step 800, loss = 1.86831, accuracy = 0.359375
    epoch 1, step 810, loss = 1.77799, accuracy = 0.40625
    epoch 1, step 820, loss = 2.06700, accuracy = 0.25
    epoch 1, step 830, loss = 2.02039, accuracy = 0.265625
    epoch 1, step 840, loss = 1.48891, accuracy = 0.515625
    epoch 1, step 850, loss = 1.89105, accuracy = 0.265625
    epoch 1, step 860, loss = 1.72040, accuracy = 0.359375
    epoch 1, step 870, loss = 1.76292, accuracy = 0.390625
    epoch 1, step 880, loss = 1.78909, accuracy = 0.390625
    epoch 1, step 890, loss = 1.75976, accuracy = 0.453125
    epoch 1, step 900, loss = 1.90596, accuracy = 0.34375
    epoch 1, step 910, loss = 1.79015, accuracy = 0.296875
    epoch 1, step 920, loss = 1.72116, accuracy = 0.359375
    epoch 1, step 930, loss = 1.73617, accuracy = 0.421875
    epoch 1, step 940, loss = 1.80251, accuracy = 0.4375
    epoch 1, step 950, loss = 1.87558, accuracy = 0.3125
    epoch 1, step 960, loss = 1.79671, accuracy = 0.3125
    epoch 1, step 970, loss = 1.84454, accuracy = 0.375
    epoch 1, step 980, loss = 1.90667, accuracy = 0.359375
    epoch 1, step 990, loss = 1.71488, accuracy = 0.34375
    epoch 1, step 1000, loss = 1.75173, accuracy = 0.4375
    epoch 1, step 1010, loss = 1.79888, accuracy = 0.375
    epoch 1, step 1020, loss = 1.52702, accuracy = 0.5
    epoch 1, step 1030, loss = 1.76504, accuracy = 0.375
    epoch 1, step 1040, loss = 1.78638, accuracy = 0.375
    epoch 1, step 1050, loss = 1.67627, accuracy = 0.421875
    epoch 1, step 1060, loss = 1.88835, accuracy = 0.40625
    epoch 1, step 1070, loss = 1.61911, accuracy = 0.375
    epoch 1, step 1080, loss = 1.49219, accuracy = 0.515625
    epoch 1, step 1090, loss = 1.66523, accuracy = 0.453125
    epoch 1, step 1100, loss = 1.65813, accuracy = 0.40625
    epoch 1, step 1110, loss = 1.57586, accuracy = 0.46875
    epoch 1, step 1120, loss = 1.77984, accuracy = 0.34375
    epoch 1, step 1130, loss = 1.62327, accuracy = 0.375
    epoch 1, step 1140, loss = 1.70856, accuracy = 0.328125
    epoch 1, step 1150, loss = 1.67570, accuracy = 0.375
    epoch 1, step 1160, loss = 1.59674, accuracy = 0.421875
    epoch 1, step 1170, loss = 1.77229, accuracy = 0.359375
    epoch 1, step 1180, loss = 1.65401, accuracy = 0.46875
    epoch 1, step 1190, loss = 1.50950, accuracy = 0.5
    epoch 1, step 1200, loss = 1.57861, accuracy = 0.359375
    epoch 1, step 1210, loss = 1.85119, accuracy = 0.359375
    epoch 1, step 1220, loss = 1.71723, accuracy = 0.40625
    epoch 1, step 1230, loss = 1.57758, accuracy = 0.34375
    epoch 1, step 1240, loss = 1.76919, accuracy = 0.390625
    epoch 1, step 1250, loss = 1.71393, accuracy = 0.390625
    epoch 1, step 1260, loss = 1.75383, accuracy = 0.40625
    epoch 1, step 1270, loss = 1.68730, accuracy = 0.40625
    epoch 1, step 1280, loss = 1.63634, accuracy = 0.515625
    epoch 1, step 1290, loss = 1.71798, accuracy = 0.421875
    epoch 1, step 1300, loss = 1.68331, accuracy = 0.390625
    epoch 1, step 1310, loss = 1.82469, accuracy = 0.328125
    epoch 1, step 1320, loss = 1.72130, accuracy = 0.359375
    epoch 1, step 1330, loss = 1.67139, accuracy = 0.421875
    epoch 1, step 1340, loss = 1.76110, accuracy = 0.359375
    epoch 1, step 1350, loss = 1.67106, accuracy = 0.40625
    epoch 1, step 1360, loss = 1.60574, accuracy = 0.40625
    epoch 1, step 1370, loss = 1.96029, accuracy = 0.34375
    epoch 1, step 1380, loss = 1.85356, accuracy = 0.34375
    epoch 1, step 1390, loss = 1.63462, accuracy = 0.4375
    epoch 1, step 1400, loss = 1.84387, accuracy = 0.40625
    validation after epoch 1: loss = 1.70893, accuracy = 0.391
    epoch 2, step 1410, loss = 1.90622, accuracy = 0.28125
    epoch 2, step 1420, loss = 1.64269, accuracy = 0.34375
    epoch 2, step 1430, loss = 1.62376, accuracy = 0.3125
    epoch 2, step 1440, loss = 1.92197, accuracy = 0.34375
    epoch 2, step 1450, loss = 1.89140, accuracy = 0.265625
    epoch 2, step 1460, loss = 1.60553, accuracy = 0.5
    epoch 2, step 1470, loss = 1.69208, accuracy = 0.46875
    epoch 2, step 1480, loss = 1.77692, accuracy = 0.390625
    epoch 2, step 1490, loss = 1.75154, accuracy = 0.4375
    epoch 2, step 1500, loss = 1.62743, accuracy = 0.40625
    epoch 2, step 1510, loss = 1.73959, accuracy = 0.328125
    epoch 2, step 1520, loss = 1.72283, accuracy = 0.40625
    epoch 2, step 1530, loss = 1.80963, accuracy = 0.296875
    epoch 2, step 1540, loss = 1.79311, accuracy = 0.3125
    epoch 2, step 1550, loss = 1.60019, accuracy = 0.46875
    epoch 2, step 1560, loss = 1.94278, accuracy = 0.234375
    epoch 2, step 1570, loss = 1.52467, accuracy = 0.40625
    epoch 2, step 1580, loss = 1.81930, accuracy = 0.3125
    epoch 2, step 1590, loss = 1.70032, accuracy = 0.34375
    epoch 2, step 1600, loss = 1.47270, accuracy = 0.4375
    epoch 2, step 1610, loss = 1.62585, accuracy = 0.359375
    epoch 2, step 1620, loss = 1.63412, accuracy = 0.421875
    epoch 2, step 1630, loss = 1.79349, accuracy = 0.390625
    epoch 2, step 1640, loss = 1.64643, accuracy = 0.484375
    epoch 2, step 1650, loss = 1.83363, accuracy = 0.28125
    epoch 2, step 1660, loss = 1.77141, accuracy = 0.234375
    epoch 2, step 1670, loss = 1.53644, accuracy = 0.46875
    epoch 2, step 1680, loss = 1.65520, accuracy = 0.40625
    epoch 2, step 1690, loss = 1.76599, accuracy = 0.390625
    epoch 2, step 1700, loss = 1.80536, accuracy = 0.34375
    epoch 2, step 1710, loss = 1.87024, accuracy = 0.359375
    epoch 2, step 1720, loss = 1.75914, accuracy = 0.375
    epoch 2, step 1730, loss = 1.57912, accuracy = 0.46875
    epoch 2, step 1740, loss = 1.58546, accuracy = 0.421875
    epoch 2, step 1750, loss = 1.58867, accuracy = 0.4375
    epoch 2, step 1760, loss = 1.67959, accuracy = 0.328125
    epoch 2, step 1770, loss = 1.91484, accuracy = 0.28125
    epoch 2, step 1780, loss = 1.77956, accuracy = 0.296875
    epoch 2, step 1790, loss = 1.71644, accuracy = 0.359375
    epoch 2, step 1800, loss = 1.58915, accuracy = 0.5
    epoch 2, step 1810, loss = 1.76781, accuracy = 0.421875
    epoch 2, step 1820, loss = 1.80891, accuracy = 0.34375
    epoch 2, step 1830, loss = 1.79017, accuracy = 0.40625
    epoch 2, step 1840, loss = 1.60353, accuracy = 0.46875
    epoch 2, step 1850, loss = 1.62600, accuracy = 0.4375
    epoch 2, step 1860, loss = 1.54830, accuracy = 0.5
    epoch 2, step 1870, loss = 1.80859, accuracy = 0.390625
    epoch 2, step 1880, loss = 1.83748, accuracy = 0.359375
    epoch 2, step 1890, loss = 1.72655, accuracy = 0.40625
    epoch 2, step 1900, loss = 1.52567, accuracy = 0.484375
    epoch 2, step 1910, loss = 1.62273, accuracy = 0.40625
    epoch 2, step 1920, loss = 1.74571, accuracy = 0.40625
    epoch 2, step 1930, loss = 1.58696, accuracy = 0.421875
    epoch 2, step 1940, loss = 1.92317, accuracy = 0.4375
    epoch 2, step 1950, loss = 1.89632, accuracy = 0.296875
    epoch 2, step 1960, loss = 1.62408, accuracy = 0.453125
    epoch 2, step 1970, loss = 1.58861, accuracy = 0.421875
    epoch 2, step 1980, loss = 1.74865, accuracy = 0.46875
    epoch 2, step 1990, loss = 1.74598, accuracy = 0.453125
    epoch 2, step 2000, loss = 1.67835, accuracy = 0.4375
    epoch 2, step 2010, loss = 1.65102, accuracy = 0.375
    epoch 2, step 2020, loss = 1.70653, accuracy = 0.390625
    epoch 2, step 2030, loss = 1.68436, accuracy = 0.453125
    epoch 2, step 2040, loss = 1.59297, accuracy = 0.40625
    epoch 2, step 2050, loss = 1.77163, accuracy = 0.34375
    epoch 2, step 2060, loss = 1.80241, accuracy = 0.40625
    epoch 2, step 2070, loss = 1.64905, accuracy = 0.453125
    epoch 2, step 2080, loss = 1.56445, accuracy = 0.453125
    epoch 2, step 2090, loss = 1.62021, accuracy = 0.421875
    epoch 2, step 2100, loss = 1.48080, accuracy = 0.515625
    validation after epoch 2: loss = 1.70594, accuracy = 0.39
    Decreased learning rate by 0.5
    epoch 3, step 2110, loss = 1.59550, accuracy = 0.421875
    epoch 3, step 2120, loss = 1.72957, accuracy = 0.375
    epoch 3, step 2130, loss = 1.61244, accuracy = 0.46875
    epoch 3, step 2140, loss = 1.67187, accuracy = 0.515625
    epoch 3, step 2150, loss = 1.68138, accuracy = 0.359375
    epoch 3, step 2160, loss = 1.60664, accuracy = 0.484375
    epoch 3, step 2170, loss = 1.61669, accuracy = 0.390625
    epoch 3, step 2180, loss = 1.67537, accuracy = 0.4375
    epoch 3, step 2190, loss = 1.58647, accuracy = 0.375
    epoch 3, step 2200, loss = 1.62037, accuracy = 0.484375
    epoch 3, step 2210, loss = 1.47652, accuracy = 0.390625
    epoch 3, step 2220, loss = 1.74797, accuracy = 0.453125
    epoch 3, step 2230, loss = 1.75480, accuracy = 0.375
    epoch 3, step 2240, loss = 1.56038, accuracy = 0.34375
    epoch 3, step 2250, loss = 1.68088, accuracy = 0.40625
    epoch 3, step 2260, loss = 1.66897, accuracy = 0.375
    epoch 3, step 2270, loss = 1.56829, accuracy = 0.4375
    epoch 3, step 2280, loss = 1.39729, accuracy = 0.546875
    epoch 3, step 2290, loss = 1.69967, accuracy = 0.46875
    epoch 3, step 2300, loss = 1.67708, accuracy = 0.40625
    epoch 3, step 2310, loss = 1.54796, accuracy = 0.453125
    epoch 3, step 2320, loss = 1.55574, accuracy = 0.4375
    epoch 3, step 2330, loss = 1.56708, accuracy = 0.40625
    epoch 3, step 2340, loss = 1.56434, accuracy = 0.453125
    epoch 3, step 2350, loss = 1.68098, accuracy = 0.40625
    epoch 3, step 2360, loss = 1.72850, accuracy = 0.4375
    epoch 3, step 2370, loss = 1.73647, accuracy = 0.46875
    epoch 3, step 2380, loss = 1.93464, accuracy = 0.28125
    epoch 3, step 2390, loss = 1.72356, accuracy = 0.34375
    epoch 3, step 2400, loss = 1.38611, accuracy = 0.546875
    epoch 3, step 2410, loss = 1.90985, accuracy = 0.328125
    epoch 3, step 2420, loss = 1.68872, accuracy = 0.3125
    epoch 3, step 2430, loss = 1.60441, accuracy = 0.40625
    epoch 3, step 2440, loss = 1.61923, accuracy = 0.359375
    epoch 3, step 2450, loss = 1.56811, accuracy = 0.546875
    epoch 3, step 2460, loss = 1.77178, accuracy = 0.40625
    epoch 3, step 2470, loss = 1.61180, accuracy = 0.390625
    epoch 3, step 2480, loss = 1.51025, accuracy = 0.421875
    epoch 3, step 2490, loss = 1.90505, accuracy = 0.265625
    epoch 3, step 2500, loss = 1.35714, accuracy = 0.546875
    epoch 3, step 2510, loss = 1.48515, accuracy = 0.484375
    epoch 3, step 2520, loss = 1.64587, accuracy = 0.4375
    epoch 3, step 2530, loss = 1.82382, accuracy = 0.40625
    epoch 3, step 2540, loss = 1.67160, accuracy = 0.4375
    epoch 3, step 2550, loss = 1.88509, accuracy = 0.28125
    epoch 3, step 2560, loss = 1.80680, accuracy = 0.25
    epoch 3, step 2570, loss = 1.56731, accuracy = 0.515625
    epoch 3, step 2580, loss = 1.67140, accuracy = 0.3125
    epoch 3, step 2590, loss = 1.53200, accuracy = 0.5625
    epoch 3, step 2600, loss = 1.78493, accuracy = 0.390625
    epoch 3, step 2610, loss = 1.57369, accuracy = 0.40625
    epoch 3, step 2620, loss = 1.59045, accuracy = 0.46875
    epoch 3, step 2630, loss = 1.73719, accuracy = 0.40625
    epoch 3, step 2640, loss = 1.56717, accuracy = 0.484375
    epoch 3, step 2650, loss = 1.58655, accuracy = 0.421875
    epoch 3, step 2660, loss = 1.37899, accuracy = 0.53125
    epoch 3, step 2670, loss = 1.62601, accuracy = 0.4375
    epoch 3, step 2680, loss = 1.67190, accuracy = 0.390625
    epoch 3, step 2690, loss = 1.67405, accuracy = 0.390625
    epoch 3, step 2700, loss = 1.88840, accuracy = 0.359375
    epoch 3, step 2710, loss = 1.56619, accuracy = 0.421875
    epoch 3, step 2720, loss = 1.51350, accuracy = 0.5
    epoch 3, step 2730, loss = 1.51831, accuracy = 0.5625
    epoch 3, step 2740, loss = 1.89952, accuracy = 0.375
    epoch 3, step 2750, loss = 1.68503, accuracy = 0.4375
    epoch 3, step 2760, loss = 1.69223, accuracy = 0.453125
    epoch 3, step 2770, loss = 1.54561, accuracy = 0.421875
    epoch 3, step 2780, loss = 1.68823, accuracy = 0.390625
    epoch 3, step 2790, loss = 1.54392, accuracy = 0.46875
    epoch 3, step 2800, loss = 1.84397, accuracy = 0.34375
    epoch 3, step 2810, loss = 1.52347, accuracy = 0.46875
    validation after epoch 3: loss = 1.63400, accuracy = 0.421
    epoch 4, step 2820, loss = 1.52170, accuracy = 0.40625
    epoch 4, step 2830, loss = 1.53544, accuracy = 0.46875
    epoch 4, step 2840, loss = 1.50508, accuracy = 0.484375
    epoch 4, step 2850, loss = 1.67433, accuracy = 0.453125
    epoch 4, step 2860, loss = 1.55538, accuracy = 0.484375
    epoch 4, step 2870, loss = 1.66152, accuracy = 0.421875
    epoch 4, step 2880, loss = 1.60164, accuracy = 0.390625
    epoch 4, step 2890, loss = 1.64475, accuracy = 0.375
    epoch 4, step 2900, loss = 1.58700, accuracy = 0.453125
    epoch 4, step 2910, loss = 1.56682, accuracy = 0.390625
    epoch 4, step 2920, loss = 1.51456, accuracy = 0.484375
    epoch 4, step 2930, loss = 1.73068, accuracy = 0.46875
    epoch 4, step 2940, loss = 1.72089, accuracy = 0.421875
    epoch 4, step 2950, loss = 1.68776, accuracy = 0.40625
    epoch 4, step 2960, loss = 1.73364, accuracy = 0.390625
    epoch 4, step 2970, loss = 1.73893, accuracy = 0.375
    epoch 4, step 2980, loss = 1.67281, accuracy = 0.453125
    epoch 4, step 2990, loss = 1.58564, accuracy = 0.390625
    epoch 4, step 3000, loss = 1.74820, accuracy = 0.34375
    epoch 4, step 3010, loss = 1.70483, accuracy = 0.3125
    epoch 4, step 3020, loss = 1.65635, accuracy = 0.453125
    epoch 4, step 3030, loss = 1.45619, accuracy = 0.546875
    epoch 4, step 3040, loss = 1.45112, accuracy = 0.453125
    epoch 4, step 3050, loss = 1.59757, accuracy = 0.390625
    epoch 4, step 3060, loss = 1.73846, accuracy = 0.421875
    epoch 4, step 3070, loss = 1.27373, accuracy = 0.671875
    epoch 4, step 3080, loss = 1.53826, accuracy = 0.4375
    epoch 4, step 3090, loss = 1.56952, accuracy = 0.4375
    epoch 4, step 3100, loss = 1.45716, accuracy = 0.484375
    epoch 4, step 3110, loss = 1.46238, accuracy = 0.421875
    epoch 4, step 3120, loss = 1.70944, accuracy = 0.46875
    epoch 4, step 3130, loss = 1.56276, accuracy = 0.375
    epoch 4, step 3140, loss = 1.81897, accuracy = 0.34375
    epoch 4, step 3150, loss = 1.63465, accuracy = 0.453125
    epoch 4, step 3160, loss = 1.53994, accuracy = 0.421875
    epoch 4, step 3170, loss = 1.48729, accuracy = 0.390625
    epoch 4, step 3180, loss = 1.71414, accuracy = 0.421875
    epoch 4, step 3190, loss = 1.81873, accuracy = 0.265625
    epoch 4, step 3200, loss = 1.74877, accuracy = 0.359375
    epoch 4, step 3210, loss = 1.69793, accuracy = 0.390625
    epoch 4, step 3220, loss = 1.54617, accuracy = 0.40625
    epoch 4, step 3230, loss = 1.73498, accuracy = 0.421875
    epoch 4, step 3240, loss = 1.51834, accuracy = 0.375
    epoch 4, step 3250, loss = 1.70547, accuracy = 0.5
    epoch 4, step 3260, loss = 1.70936, accuracy = 0.328125
    epoch 4, step 3270, loss = 1.76406, accuracy = 0.390625
    epoch 4, step 3280, loss = 1.55494, accuracy = 0.40625
    epoch 4, step 3290, loss = 1.59372, accuracy = 0.46875
    epoch 4, step 3300, loss = 1.76982, accuracy = 0.453125
    epoch 4, step 3310, loss = 1.78854, accuracy = 0.375
    epoch 4, step 3320, loss = 1.66560, accuracy = 0.359375
    epoch 4, step 3330, loss = 1.50967, accuracy = 0.453125
    epoch 4, step 3340, loss = 1.47671, accuracy = 0.4375
    epoch 4, step 3350, loss = 1.40614, accuracy = 0.53125
    epoch 4, step 3360, loss = 1.71392, accuracy = 0.328125
    epoch 4, step 3370, loss = 1.38327, accuracy = 0.453125
    epoch 4, step 3380, loss = 1.81751, accuracy = 0.390625
    epoch 4, step 3390, loss = 1.70443, accuracy = 0.328125
    epoch 4, step 3400, loss = 1.64104, accuracy = 0.40625
    epoch 4, step 3410, loss = 1.55731, accuracy = 0.4375
    epoch 4, step 3420, loss = 1.75445, accuracy = 0.359375
    epoch 4, step 3430, loss = 1.64059, accuracy = 0.40625
    epoch 4, step 3440, loss = 1.71658, accuracy = 0.421875
    epoch 4, step 3450, loss = 1.48630, accuracy = 0.453125
    epoch 4, step 3460, loss = 1.55393, accuracy = 0.453125
    epoch 4, step 3470, loss = 1.55936, accuracy = 0.484375
    epoch 4, step 3480, loss = 1.60011, accuracy = 0.4375
    epoch 4, step 3490, loss = 1.68255, accuracy = 0.375
    epoch 4, step 3500, loss = 1.43536, accuracy = 0.53125
    epoch 4, step 3510, loss = 1.72088, accuracy = 0.375
    validation after epoch 4: loss = 1.63296, accuracy = 0.4234
    epoch 5, step 3520, loss = 1.63082, accuracy = 0.40625
    epoch 5, step 3530, loss = 1.51311, accuracy = 0.53125
    epoch 5, step 3540, loss = 1.53337, accuracy = 0.5
    epoch 5, step 3550, loss = 1.61983, accuracy = 0.375
    epoch 5, step 3560, loss = 1.57591, accuracy = 0.453125
    epoch 5, step 3570, loss = 1.45861, accuracy = 0.4375
    epoch 5, step 3580, loss = 1.65526, accuracy = 0.421875
    epoch 5, step 3590, loss = 1.74630, accuracy = 0.296875
    epoch 5, step 3600, loss = 1.69686, accuracy = 0.359375
    epoch 5, step 3610, loss = 1.45688, accuracy = 0.453125
    epoch 5, step 3620, loss = 1.64693, accuracy = 0.484375
    epoch 5, step 3630, loss = 1.71032, accuracy = 0.359375
    epoch 5, step 3640, loss = 1.56533, accuracy = 0.4375
    epoch 5, step 3650, loss = 1.57846, accuracy = 0.5
    epoch 5, step 3660, loss = 1.61381, accuracy = 0.46875
    epoch 5, step 3670, loss = 1.63883, accuracy = 0.515625
    epoch 5, step 3680, loss = 1.50510, accuracy = 0.390625
    epoch 5, step 3690, loss = 1.54408, accuracy = 0.484375
    epoch 5, step 3700, loss = 1.47835, accuracy = 0.4375
    epoch 5, step 3710, loss = 1.44139, accuracy = 0.4375
    epoch 5, step 3720, loss = 1.67216, accuracy = 0.375
    epoch 5, step 3730, loss = 1.47963, accuracy = 0.515625
    epoch 5, step 3740, loss = 1.61245, accuracy = 0.4375
    epoch 5, step 3750, loss = 1.51356, accuracy = 0.484375
    epoch 5, step 3760, loss = 1.59593, accuracy = 0.453125
    epoch 5, step 3770, loss = 1.44184, accuracy = 0.453125
    epoch 5, step 3780, loss = 1.48664, accuracy = 0.4375
    epoch 5, step 3790, loss = 1.63552, accuracy = 0.40625
    epoch 5, step 3800, loss = 1.46622, accuracy = 0.5
    epoch 5, step 3810, loss = 1.62875, accuracy = 0.40625
    epoch 5, step 3820, loss = 1.47685, accuracy = 0.453125
    epoch 5, step 3830, loss = 1.52520, accuracy = 0.375
    epoch 5, step 3840, loss = 1.56799, accuracy = 0.453125
    epoch 5, step 3850, loss = 1.72359, accuracy = 0.390625
    epoch 5, step 3860, loss = 1.47793, accuracy = 0.453125
    epoch 5, step 3870, loss = 1.65329, accuracy = 0.484375
    epoch 5, step 3880, loss = 1.70561, accuracy = 0.421875
    epoch 5, step 3890, loss = 1.38059, accuracy = 0.4375
    epoch 5, step 3900, loss = 1.62810, accuracy = 0.421875
    epoch 5, step 3910, loss = 1.42348, accuracy = 0.546875
    epoch 5, step 3920, loss = 1.49621, accuracy = 0.5
    epoch 5, step 3930, loss = 1.70446, accuracy = 0.3125
    epoch 5, step 3940, loss = 1.52015, accuracy = 0.421875
    epoch 5, step 3950, loss = 1.53955, accuracy = 0.4375
    epoch 5, step 3960, loss = 1.70362, accuracy = 0.421875
    epoch 5, step 3970, loss = 1.54722, accuracy = 0.484375
    epoch 5, step 3980, loss = 1.53819, accuracy = 0.46875
    epoch 5, step 3990, loss = 1.54959, accuracy = 0.46875
    epoch 5, step 4000, loss = 1.70670, accuracy = 0.375
    epoch 5, step 4010, loss = 1.50422, accuracy = 0.359375
    epoch 5, step 4020, loss = 1.60294, accuracy = 0.5
    epoch 5, step 4030, loss = 1.42802, accuracy = 0.46875
    epoch 5, step 4040, loss = 1.43222, accuracy = 0.5625
    epoch 5, step 4050, loss = 1.55931, accuracy = 0.515625
    epoch 5, step 4060, loss = 1.66652, accuracy = 0.40625
    epoch 5, step 4070, loss = 1.65705, accuracy = 0.375
    epoch 5, step 4080, loss = 1.66712, accuracy = 0.421875
    epoch 5, step 4090, loss = 1.63817, accuracy = 0.421875
    epoch 5, step 4100, loss = 1.74415, accuracy = 0.390625
    epoch 5, step 4110, loss = 1.65485, accuracy = 0.4375
    epoch 5, step 4120, loss = 1.55502, accuracy = 0.515625
    epoch 5, step 4130, loss = 1.77118, accuracy = 0.390625
    epoch 5, step 4140, loss = 1.63942, accuracy = 0.453125
    epoch 5, step 4150, loss = 1.72051, accuracy = 0.390625
    epoch 5, step 4160, loss = 1.59787, accuracy = 0.359375
    epoch 5, step 4170, loss = 1.76770, accuracy = 0.359375
    epoch 5, step 4180, loss = 1.70466, accuracy = 0.421875
    epoch 5, step 4190, loss = 1.59140, accuracy = 0.421875
    epoch 5, step 4200, loss = 1.42377, accuracy = 0.546875
    epoch 5, step 4210, loss = 1.59977, accuracy = 0.421875
    validation after epoch 5: loss = 1.61589, accuracy = 0.4298
    Decreased learning rate by 0.5
    epoch 6, step 4220, loss = 1.54125, accuracy = 0.453125
    epoch 6, step 4230, loss = 1.48722, accuracy = 0.46875
    epoch 6, step 4240, loss = 1.48466, accuracy = 0.4375
    epoch 6, step 4250, loss = 1.69229, accuracy = 0.40625
    epoch 6, step 4260, loss = 1.54451, accuracy = 0.53125
    epoch 6, step 4270, loss = 1.62125, accuracy = 0.4375
    epoch 6, step 4280, loss = 1.49712, accuracy = 0.4375
    epoch 6, step 4290, loss = 1.47210, accuracy = 0.515625
    epoch 6, step 4300, loss = 1.34849, accuracy = 0.53125
    epoch 6, step 4310, loss = 1.54700, accuracy = 0.5
    epoch 6, step 4320, loss = 1.40868, accuracy = 0.546875
    epoch 6, step 4330, loss = 1.70077, accuracy = 0.375
    epoch 6, step 4340, loss = 1.63223, accuracy = 0.375
    epoch 6, step 4350, loss = 1.34931, accuracy = 0.484375
    epoch 6, step 4360, loss = 1.53464, accuracy = 0.453125
    epoch 6, step 4370, loss = 1.50734, accuracy = 0.484375
    epoch 6, step 4380, loss = 1.41539, accuracy = 0.546875
    epoch 6, step 4390, loss = 1.55560, accuracy = 0.515625
    epoch 6, step 4400, loss = 1.60852, accuracy = 0.515625
    epoch 6, step 4410, loss = 1.57525, accuracy = 0.4375
    epoch 6, step 4420, loss = 1.56579, accuracy = 0.46875
    epoch 6, step 4430, loss = 1.63347, accuracy = 0.390625
    epoch 6, step 4440, loss = 1.39454, accuracy = 0.484375
    epoch 6, step 4450, loss = 1.57424, accuracy = 0.5
    epoch 6, step 4460, loss = 1.55105, accuracy = 0.421875
    epoch 6, step 4470, loss = 1.66601, accuracy = 0.390625
    epoch 6, step 4480, loss = 1.27322, accuracy = 0.5
    epoch 6, step 4490, loss = 1.59716, accuracy = 0.375
    epoch 6, step 4500, loss = 1.40998, accuracy = 0.5
    epoch 6, step 4510, loss = 1.41004, accuracy = 0.53125
    epoch 6, step 4520, loss = 1.65352, accuracy = 0.421875
    epoch 6, step 4530, loss = 1.61600, accuracy = 0.46875
    epoch 6, step 4540, loss = 1.57288, accuracy = 0.46875
    epoch 6, step 4550, loss = 1.41394, accuracy = 0.515625
    epoch 6, step 4560, loss = 1.54589, accuracy = 0.484375
    epoch 6, step 4570, loss = 1.50887, accuracy = 0.453125
    epoch 6, step 4580, loss = 1.51992, accuracy = 0.5
    epoch 6, step 4590, loss = 1.64217, accuracy = 0.421875
    epoch 6, step 4600, loss = 1.40028, accuracy = 0.5
    epoch 6, step 4610, loss = 1.56800, accuracy = 0.4375
    epoch 6, step 4620, loss = 1.53129, accuracy = 0.453125
    epoch 6, step 4630, loss = 1.59016, accuracy = 0.40625
    epoch 6, step 4640, loss = 1.28762, accuracy = 0.546875
    epoch 6, step 4650, loss = 1.58138, accuracy = 0.375
    epoch 6, step 4660, loss = 1.63192, accuracy = 0.4375
    epoch 6, step 4670, loss = 1.43896, accuracy = 0.5
    epoch 6, step 4680, loss = 1.52732, accuracy = 0.4375
    epoch 6, step 4690, loss = 1.40741, accuracy = 0.5625
    epoch 6, step 4700, loss = 1.40279, accuracy = 0.515625
    epoch 6, step 4710, loss = 1.38289, accuracy = 0.53125
    epoch 6, step 4720, loss = 1.54291, accuracy = 0.453125
    epoch 6, step 4730, loss = 1.46658, accuracy = 0.53125
    epoch 6, step 4740, loss = 1.31786, accuracy = 0.453125
    epoch 6, step 4750, loss = 1.57266, accuracy = 0.484375
    epoch 6, step 4760, loss = 1.52618, accuracy = 0.40625
    epoch 6, step 4770, loss = 1.42995, accuracy = 0.484375
    epoch 6, step 4780, loss = 1.46274, accuracy = 0.390625
    epoch 6, step 4790, loss = 1.75626, accuracy = 0.40625
    epoch 6, step 4800, loss = 1.35124, accuracy = 0.546875
    epoch 6, step 4810, loss = 1.58724, accuracy = 0.421875
    epoch 6, step 4820, loss = 1.63078, accuracy = 0.453125
    epoch 6, step 4830, loss = 1.65292, accuracy = 0.421875
    epoch 6, step 4840, loss = 1.46080, accuracy = 0.4375
    epoch 6, step 4850, loss = 1.55605, accuracy = 0.390625
    epoch 6, step 4860, loss = 1.32117, accuracy = 0.578125
    epoch 6, step 4870, loss = 1.56370, accuracy = 0.390625
    epoch 6, step 4880, loss = 1.51690, accuracy = 0.46875
    epoch 6, step 4890, loss = 1.45610, accuracy = 0.53125
    epoch 6, step 4900, loss = 1.36986, accuracy = 0.59375
    epoch 6, step 4910, loss = 1.48172, accuracy = 0.453125
    epoch 6, step 4920, loss = 1.83296, accuracy = 0.375
    validation after epoch 6: loss = 1.56679, accuracy = 0.4436
    epoch 7, step 4930, loss = 1.47336, accuracy = 0.578125
    epoch 7, step 4940, loss = 1.40067, accuracy = 0.5
    epoch 7, step 4950, loss = 1.92567, accuracy = 0.328125
    epoch 7, step 4960, loss = 1.37344, accuracy = 0.546875
    epoch 7, step 4970, loss = 1.21541, accuracy = 0.625
    epoch 7, step 4980, loss = 1.59536, accuracy = 0.4375
    epoch 7, step 4990, loss = 1.39142, accuracy = 0.484375
    epoch 7, step 5000, loss = 1.52789, accuracy = 0.46875
    epoch 7, step 5010, loss = 1.67142, accuracy = 0.453125
    epoch 7, step 5020, loss = 1.34054, accuracy = 0.5
    epoch 7, step 5030, loss = 1.35727, accuracy = 0.46875
    epoch 7, step 5040, loss = 1.62773, accuracy = 0.40625
    epoch 7, step 5050, loss = 1.17414, accuracy = 0.578125
    epoch 7, step 5060, loss = 1.62304, accuracy = 0.4375
    epoch 7, step 5070, loss = 1.50951, accuracy = 0.4375
    epoch 7, step 5080, loss = 1.37608, accuracy = 0.484375
    epoch 7, step 5090, loss = 1.73200, accuracy = 0.40625
    epoch 7, step 5100, loss = 1.37310, accuracy = 0.5
    epoch 7, step 5110, loss = 1.56770, accuracy = 0.5
    epoch 7, step 5120, loss = 1.31579, accuracy = 0.515625
    epoch 7, step 5130, loss = 1.49387, accuracy = 0.5
    epoch 7, step 5140, loss = 1.72256, accuracy = 0.46875
    epoch 7, step 5150, loss = 1.51662, accuracy = 0.515625
    epoch 7, step 5160, loss = 1.46960, accuracy = 0.46875
    epoch 7, step 5170, loss = 1.33374, accuracy = 0.453125
    epoch 7, step 5180, loss = 1.35571, accuracy = 0.5
    epoch 7, step 5190, loss = 1.39232, accuracy = 0.46875
    epoch 7, step 5200, loss = 1.42213, accuracy = 0.53125
    epoch 7, step 5210, loss = 1.26173, accuracy = 0.625
    epoch 7, step 5220, loss = 1.50660, accuracy = 0.5
    epoch 7, step 5230, loss = 1.59326, accuracy = 0.4375
    epoch 7, step 5240, loss = 1.57904, accuracy = 0.40625
    epoch 7, step 5250, loss = 1.31170, accuracy = 0.46875
    epoch 7, step 5260, loss = 1.42777, accuracy = 0.40625
    epoch 7, step 5270, loss = 1.49622, accuracy = 0.484375
    epoch 7, step 5280, loss = 1.39840, accuracy = 0.4375
    epoch 7, step 5290, loss = 1.33233, accuracy = 0.625
    epoch 7, step 5300, loss = 1.53668, accuracy = 0.4375
    epoch 7, step 5310, loss = 1.46856, accuracy = 0.5
    epoch 7, step 5320, loss = 1.33496, accuracy = 0.546875
    epoch 7, step 5330, loss = 1.52436, accuracy = 0.390625
    epoch 7, step 5340, loss = 1.59246, accuracy = 0.4375
    epoch 7, step 5350, loss = 1.53922, accuracy = 0.53125
    epoch 7, step 5360, loss = 1.57941, accuracy = 0.453125
    epoch 7, step 5370, loss = 1.50663, accuracy = 0.484375
    epoch 7, step 5380, loss = 1.76290, accuracy = 0.359375
    epoch 7, step 5390, loss = 1.65541, accuracy = 0.46875
    epoch 7, step 5400, loss = 1.52460, accuracy = 0.421875
    epoch 7, step 5410, loss = 1.57871, accuracy = 0.40625
    epoch 7, step 5420, loss = 1.59450, accuracy = 0.421875
    epoch 7, step 5430, loss = 1.37515, accuracy = 0.59375
    epoch 7, step 5440, loss = 1.43241, accuracy = 0.5625
    epoch 7, step 5450, loss = 1.57793, accuracy = 0.40625
    epoch 7, step 5460, loss = 1.56532, accuracy = 0.453125
    epoch 7, step 5470, loss = 1.17338, accuracy = 0.65625
    epoch 7, step 5480, loss = 1.63641, accuracy = 0.4375
    epoch 7, step 5490, loss = 1.40005, accuracy = 0.4375
    epoch 7, step 5500, loss = 1.37383, accuracy = 0.5
    epoch 7, step 5510, loss = 1.52385, accuracy = 0.375
    epoch 7, step 5520, loss = 1.61208, accuracy = 0.40625
    epoch 7, step 5530, loss = 1.42274, accuracy = 0.5
    epoch 7, step 5540, loss = 1.38003, accuracy = 0.515625
    epoch 7, step 5550, loss = 1.54484, accuracy = 0.421875
    epoch 7, step 5560, loss = 1.49844, accuracy = 0.53125
    epoch 7, step 5570, loss = 1.64075, accuracy = 0.453125
    epoch 7, step 5580, loss = 1.61800, accuracy = 0.4375
    epoch 7, step 5590, loss = 1.54018, accuracy = 0.484375
    epoch 7, step 5600, loss = 1.51838, accuracy = 0.390625
    epoch 7, step 5610, loss = 1.65826, accuracy = 0.328125
    epoch 7, step 5620, loss = 1.41533, accuracy = 0.578125
    validation after epoch 7: loss = 1.56701, accuracy = 0.4448
    epoch 8, step 5630, loss = 1.46486, accuracy = 0.46875
    epoch 8, step 5640, loss = 1.52998, accuracy = 0.359375
    epoch 8, step 5650, loss = 1.46642, accuracy = 0.515625
    epoch 8, step 5660, loss = 1.34988, accuracy = 0.46875
    epoch 8, step 5670, loss = 1.34740, accuracy = 0.484375
    epoch 8, step 5680, loss = 1.42745, accuracy = 0.515625
    epoch 8, step 5690, loss = 1.46965, accuracy = 0.46875
    epoch 8, step 5700, loss = 1.50560, accuracy = 0.40625
    epoch 8, step 5710, loss = 1.59632, accuracy = 0.421875
    epoch 8, step 5720, loss = 1.54334, accuracy = 0.4375
    epoch 8, step 5730, loss = 1.48029, accuracy = 0.515625
    epoch 8, step 5740, loss = 1.38554, accuracy = 0.5
    epoch 8, step 5750, loss = 1.47897, accuracy = 0.46875
    epoch 8, step 5760, loss = 1.45185, accuracy = 0.53125
    epoch 8, step 5770, loss = 1.54455, accuracy = 0.546875
    epoch 8, step 5780, loss = 1.32214, accuracy = 0.5625
    epoch 8, step 5790, loss = 1.29684, accuracy = 0.453125
    epoch 8, step 5800, loss = 1.32660, accuracy = 0.53125
    epoch 8, step 5810, loss = 1.48390, accuracy = 0.40625
    epoch 8, step 5820, loss = 1.43116, accuracy = 0.421875
    epoch 8, step 5830, loss = 1.51013, accuracy = 0.515625
    epoch 8, step 5840, loss = 1.38931, accuracy = 0.40625
    epoch 8, step 5850, loss = 1.45502, accuracy = 0.484375
    epoch 8, step 5860, loss = 1.44478, accuracy = 0.515625
    epoch 8, step 5870, loss = 1.27086, accuracy = 0.515625
    epoch 8, step 5880, loss = 1.36954, accuracy = 0.53125
    epoch 8, step 5890, loss = 1.45988, accuracy = 0.515625
    epoch 8, step 5900, loss = 1.57427, accuracy = 0.4375
    epoch 8, step 5910, loss = 1.46333, accuracy = 0.46875
    epoch 8, step 5920, loss = 1.45116, accuracy = 0.46875
    epoch 8, step 5930, loss = 1.55727, accuracy = 0.390625
    epoch 8, step 5940, loss = 1.39936, accuracy = 0.59375
    epoch 8, step 5950, loss = 1.29084, accuracy = 0.53125
    epoch 8, step 5960, loss = 1.61216, accuracy = 0.421875
    epoch 8, step 5970, loss = 1.42937, accuracy = 0.453125
    epoch 8, step 5980, loss = 1.76690, accuracy = 0.359375
    epoch 8, step 5990, loss = 1.60151, accuracy = 0.453125
    epoch 8, step 6000, loss = 1.50704, accuracy = 0.484375
    epoch 8, step 6010, loss = 1.41683, accuracy = 0.421875
    epoch 8, step 6020, loss = 1.50544, accuracy = 0.453125
    epoch 8, step 6030, loss = 1.28364, accuracy = 0.515625
    epoch 8, step 6040, loss = 1.52798, accuracy = 0.5
    epoch 8, step 6050, loss = 1.53508, accuracy = 0.5
    epoch 8, step 6060, loss = 1.50620, accuracy = 0.578125
    epoch 8, step 6070, loss = 1.50230, accuracy = 0.421875
    epoch 8, step 6080, loss = 1.78397, accuracy = 0.484375
    epoch 8, step 6090, loss = 1.51337, accuracy = 0.4375
    epoch 8, step 6100, loss = 1.63452, accuracy = 0.46875
    epoch 8, step 6110, loss = 1.40559, accuracy = 0.53125
    epoch 8, step 6120, loss = 1.59107, accuracy = 0.4375
    epoch 8, step 6130, loss = 1.36433, accuracy = 0.515625
    epoch 8, step 6140, loss = 1.58204, accuracy = 0.421875
    epoch 8, step 6150, loss = 1.54566, accuracy = 0.4375
    epoch 8, step 6160, loss = 1.57616, accuracy = 0.4375
    epoch 8, step 6170, loss = 1.66648, accuracy = 0.484375
    epoch 8, step 6180, loss = 1.43617, accuracy = 0.421875
    epoch 8, step 6190, loss = 1.50168, accuracy = 0.390625
    epoch 8, step 6200, loss = 1.42034, accuracy = 0.5625
    epoch 8, step 6210, loss = 1.41452, accuracy = 0.53125
    epoch 8, step 6220, loss = 1.46292, accuracy = 0.4375
    epoch 8, step 6230, loss = 1.42912, accuracy = 0.5
    epoch 8, step 6240, loss = 1.32808, accuracy = 0.515625
    epoch 8, step 6250, loss = 1.38246, accuracy = 0.4375
    epoch 8, step 6260, loss = 1.38444, accuracy = 0.453125
    epoch 8, step 6270, loss = 1.44739, accuracy = 0.453125
    epoch 8, step 6280, loss = 1.41679, accuracy = 0.453125
    epoch 8, step 6290, loss = 1.44645, accuracy = 0.5
    epoch 8, step 6300, loss = 1.62539, accuracy = 0.46875
    epoch 8, step 6310, loss = 1.63127, accuracy = 0.296875
    epoch 8, step 6320, loss = 1.43133, accuracy = 0.515625
    validation after epoch 8: loss = 1.55431, accuracy = 0.4442
    Decreased learning rate by 0.5
    epoch 9, step 6330, loss = 1.52271, accuracy = 0.453125
    epoch 9, step 6340, loss = 1.32208, accuracy = 0.5625
    epoch 9, step 6350, loss = 1.23261, accuracy = 0.5625
    epoch 9, step 6360, loss = 1.35115, accuracy = 0.515625
    epoch 9, step 6370, loss = 1.52489, accuracy = 0.46875
    epoch 9, step 6380, loss = 1.30031, accuracy = 0.5625
    epoch 9, step 6390, loss = 1.35187, accuracy = 0.546875
    epoch 9, step 6400, loss = 1.40561, accuracy = 0.453125
    epoch 9, step 6410, loss = 1.25151, accuracy = 0.421875
    epoch 9, step 6420, loss = 1.35376, accuracy = 0.53125
    epoch 9, step 6430, loss = 1.47878, accuracy = 0.453125
    epoch 9, step 6440, loss = 1.47513, accuracy = 0.484375
    epoch 9, step 6450, loss = 1.35856, accuracy = 0.578125
    epoch 9, step 6460, loss = 1.25190, accuracy = 0.53125
    epoch 9, step 6470, loss = 1.33995, accuracy = 0.515625
    epoch 9, step 6480, loss = 1.38950, accuracy = 0.484375
    epoch 9, step 6490, loss = 1.35267, accuracy = 0.484375
    epoch 9, step 6500, loss = 1.55433, accuracy = 0.453125
    epoch 9, step 6510, loss = 1.36518, accuracy = 0.484375
    epoch 9, step 6520, loss = 1.22290, accuracy = 0.65625
    epoch 9, step 6530, loss = 1.44468, accuracy = 0.421875
    epoch 9, step 6540, loss = 1.45123, accuracy = 0.484375
    epoch 9, step 6550, loss = 1.28297, accuracy = 0.53125
    epoch 9, step 6560, loss = 1.48198, accuracy = 0.4375
    epoch 9, step 6570, loss = 1.04381, accuracy = 0.609375
    epoch 9, step 6580, loss = 1.56738, accuracy = 0.4375
    epoch 9, step 6590, loss = 1.39212, accuracy = 0.515625
    epoch 9, step 6600, loss = 1.46409, accuracy = 0.4375
    epoch 9, step 6610, loss = 1.48888, accuracy = 0.546875
    epoch 9, step 6620, loss = 1.62919, accuracy = 0.4375
    epoch 9, step 6630, loss = 1.23147, accuracy = 0.578125
    epoch 9, step 6640, loss = 1.22973, accuracy = 0.5625
    epoch 9, step 6650, loss = 1.21069, accuracy = 0.5625
    epoch 9, step 6660, loss = 1.48774, accuracy = 0.484375
    epoch 9, step 6670, loss = 1.39300, accuracy = 0.484375
    epoch 9, step 6680, loss = 1.34577, accuracy = 0.546875
    epoch 9, step 6690, loss = 1.42090, accuracy = 0.390625
    epoch 9, step 6700, loss = 1.43614, accuracy = 0.484375
    epoch 9, step 6710, loss = 1.29579, accuracy = 0.5
    epoch 9, step 6720, loss = 1.45846, accuracy = 0.453125
    epoch 9, step 6730, loss = 1.38199, accuracy = 0.4375
    epoch 9, step 6740, loss = 1.47321, accuracy = 0.453125
    epoch 9, step 6750, loss = 1.33946, accuracy = 0.5
    epoch 9, step 6760, loss = 1.13007, accuracy = 0.578125
    epoch 9, step 6770, loss = 1.50258, accuracy = 0.375
    epoch 9, step 6780, loss = 1.42053, accuracy = 0.484375
    epoch 9, step 6790, loss = 1.49621, accuracy = 0.421875
    epoch 9, step 6800, loss = 1.37743, accuracy = 0.421875
    epoch 9, step 6810, loss = 1.46231, accuracy = 0.53125
    epoch 9, step 6820, loss = 1.57131, accuracy = 0.453125
    epoch 9, step 6830, loss = 1.25878, accuracy = 0.671875
    epoch 9, step 6840, loss = 1.18367, accuracy = 0.5625
    epoch 9, step 6850, loss = 1.42035, accuracy = 0.5
    epoch 9, step 6860, loss = 1.52491, accuracy = 0.5
    epoch 9, step 6870, loss = 1.28023, accuracy = 0.609375
    epoch 9, step 6880, loss = 1.41293, accuracy = 0.546875
    epoch 9, step 6890, loss = 1.40744, accuracy = 0.515625
    epoch 9, step 6900, loss = 1.77275, accuracy = 0.4375
    epoch 9, step 6910, loss = 1.29520, accuracy = 0.59375
    epoch 9, step 6920, loss = 1.22622, accuracy = 0.546875
    epoch 9, step 6930, loss = 1.27936, accuracy = 0.546875
    epoch 9, step 6940, loss = 1.36785, accuracy = 0.5
    epoch 9, step 6950, loss = 1.49701, accuracy = 0.453125
    epoch 9, step 6960, loss = 1.21676, accuracy = 0.578125
    epoch 9, step 6970, loss = 1.31673, accuracy = 0.546875
    epoch 9, step 6980, loss = 1.18541, accuracy = 0.625
    epoch 9, step 6990, loss = 1.64641, accuracy = 0.453125
    epoch 9, step 7000, loss = 1.39601, accuracy = 0.515625
    epoch 9, step 7010, loss = 1.25406, accuracy = 0.578125
    epoch 9, step 7020, loss = 1.36191, accuracy = 0.515625
    validation after epoch 9: loss = 1.53786, accuracy = 0.4496
    epoch 10, step 7030, loss = 1.29084, accuracy = 0.59375
    epoch 10, step 7040, loss = 1.44440, accuracy = 0.484375
    epoch 10, step 7050, loss = 1.14208, accuracy = 0.625
    epoch 10, step 7060, loss = 1.38352, accuracy = 0.5625
    epoch 10, step 7070, loss = 1.30345, accuracy = 0.53125
    epoch 10, step 7080, loss = 1.46129, accuracy = 0.453125
    epoch 10, step 7090, loss = 1.51400, accuracy = 0.453125
    epoch 10, step 7100, loss = 1.46130, accuracy = 0.421875
    epoch 10, step 7110, loss = 1.49894, accuracy = 0.515625
    epoch 10, step 7120, loss = 1.32584, accuracy = 0.484375
    epoch 10, step 7130, loss = 1.59902, accuracy = 0.4375
    epoch 10, step 7140, loss = 1.34977, accuracy = 0.5
    epoch 10, step 7150, loss = 1.45662, accuracy = 0.546875
    epoch 10, step 7160, loss = 1.32536, accuracy = 0.59375
    epoch 10, step 7170, loss = 1.25911, accuracy = 0.640625
    epoch 10, step 7180, loss = 1.37074, accuracy = 0.484375
    epoch 10, step 7190, loss = 1.29292, accuracy = 0.5625
    epoch 10, step 7200, loss = 1.49502, accuracy = 0.453125
    epoch 10, step 7210, loss = 1.29629, accuracy = 0.515625
    epoch 10, step 7220, loss = 1.30833, accuracy = 0.53125
    epoch 10, step 7230, loss = 1.31935, accuracy = 0.515625
    epoch 10, step 7240, loss = 1.59467, accuracy = 0.53125
    epoch 10, step 7250, loss = 1.37590, accuracy = 0.5625
    epoch 10, step 7260, loss = 1.31509, accuracy = 0.546875
    epoch 10, step 7270, loss = 1.22430, accuracy = 0.59375
    epoch 10, step 7280, loss = 1.42116, accuracy = 0.484375
    epoch 10, step 7290, loss = 1.61347, accuracy = 0.484375
    epoch 10, step 7300, loss = 1.40816, accuracy = 0.46875
    epoch 10, step 7310, loss = 1.07611, accuracy = 0.578125
    epoch 10, step 7320, loss = 1.05424, accuracy = 0.59375
    epoch 10, step 7330, loss = 1.13519, accuracy = 0.609375
    epoch 10, step 7340, loss = 1.35404, accuracy = 0.484375
    epoch 10, step 7350, loss = 1.55170, accuracy = 0.46875
    epoch 10, step 7360, loss = 1.30743, accuracy = 0.484375
    epoch 10, step 7370, loss = 1.40161, accuracy = 0.515625
    epoch 10, step 7380, loss = 1.48830, accuracy = 0.546875
    epoch 10, step 7390, loss = 1.48997, accuracy = 0.5
    epoch 10, step 7400, loss = 1.56828, accuracy = 0.453125
    epoch 10, step 7410, loss = 1.42069, accuracy = 0.578125
    epoch 10, step 7420, loss = 1.42383, accuracy = 0.5
    epoch 10, step 7430, loss = 1.25627, accuracy = 0.546875
    epoch 10, step 7440, loss = 1.41032, accuracy = 0.421875
    epoch 10, step 7450, loss = 1.36486, accuracy = 0.578125
    epoch 10, step 7460, loss = 1.46235, accuracy = 0.46875
    epoch 10, step 7470, loss = 1.43059, accuracy = 0.484375
    epoch 10, step 7480, loss = 1.48746, accuracy = 0.484375
    epoch 10, step 7490, loss = 1.36544, accuracy = 0.46875
    epoch 10, step 7500, loss = 1.50194, accuracy = 0.46875
    epoch 10, step 7510, loss = 1.34661, accuracy = 0.5
    epoch 10, step 7520, loss = 1.09507, accuracy = 0.625
    epoch 10, step 7530, loss = 1.17596, accuracy = 0.609375
    epoch 10, step 7540, loss = 1.26788, accuracy = 0.5
    epoch 10, step 7550, loss = 1.34535, accuracy = 0.515625
    epoch 10, step 7560, loss = 1.26440, accuracy = 0.53125
    epoch 10, step 7570, loss = 1.27975, accuracy = 0.609375
    epoch 10, step 7580, loss = 1.38084, accuracy = 0.515625
    epoch 10, step 7590, loss = 1.49247, accuracy = 0.46875
    epoch 10, step 7600, loss = 1.37939, accuracy = 0.578125
    epoch 10, step 7610, loss = 1.33371, accuracy = 0.5625
    epoch 10, step 7620, loss = 1.42541, accuracy = 0.484375
    epoch 10, step 7630, loss = 1.31186, accuracy = 0.5
    epoch 10, step 7640, loss = 1.48682, accuracy = 0.375
    epoch 10, step 7650, loss = 1.08820, accuracy = 0.5625
    epoch 10, step 7660, loss = 1.32128, accuracy = 0.578125
    epoch 10, step 7670, loss = 1.27372, accuracy = 0.5625
    epoch 10, step 7680, loss = 1.45698, accuracy = 0.546875
    epoch 10, step 7690, loss = 1.48408, accuracy = 0.515625
    epoch 10, step 7700, loss = 1.17725, accuracy = 0.5625
    epoch 10, step 7710, loss = 1.26450, accuracy = 0.640625
    epoch 10, step 7720, loss = 1.39074, accuracy = 0.53125
    epoch 10, step 7730, loss = 1.48130, accuracy = 0.421875
    validation after epoch 10: loss = 1.54319, accuracy = 0.4614
    epoch 11, step 7740, loss = 1.35041, accuracy = 0.5
    epoch 11, step 7750, loss = 1.24375, accuracy = 0.515625
    epoch 11, step 7760, loss = 1.27604, accuracy = 0.53125
    epoch 11, step 7770, loss = 1.37873, accuracy = 0.484375
    epoch 11, step 7780, loss = 1.57714, accuracy = 0.4375
    epoch 11, step 7790, loss = 1.19726, accuracy = 0.625
    epoch 11, step 7800, loss = 1.45706, accuracy = 0.484375
    epoch 11, step 7810, loss = 1.39723, accuracy = 0.46875
    epoch 11, step 7820, loss = 1.35503, accuracy = 0.46875
    epoch 11, step 7830, loss = 1.23358, accuracy = 0.65625
    epoch 11, step 7840, loss = 1.51361, accuracy = 0.5
    epoch 11, step 7850, loss = 1.23591, accuracy = 0.609375
    epoch 11, step 7860, loss = 1.36966, accuracy = 0.515625
    epoch 11, step 7870, loss = 1.29521, accuracy = 0.59375
    epoch 11, step 7880, loss = 1.23481, accuracy = 0.546875
    epoch 11, step 7890, loss = 1.21886, accuracy = 0.578125
    epoch 11, step 7900, loss = 1.27373, accuracy = 0.59375
    epoch 11, step 7910, loss = 1.45399, accuracy = 0.453125
    epoch 11, step 7920, loss = 1.32858, accuracy = 0.5625
    epoch 11, step 7930, loss = 1.20612, accuracy = 0.609375
    epoch 11, step 7940, loss = 1.18250, accuracy = 0.578125
    epoch 11, step 7950, loss = 1.43549, accuracy = 0.5625
    epoch 11, step 7960, loss = 1.38054, accuracy = 0.46875
    epoch 11, step 7970, loss = 1.45395, accuracy = 0.453125
    epoch 11, step 7980, loss = 1.32123, accuracy = 0.5625
    epoch 11, step 7990, loss = 1.26017, accuracy = 0.484375
    epoch 11, step 8000, loss = 1.31881, accuracy = 0.546875
    epoch 11, step 8010, loss = 1.35463, accuracy = 0.546875
    epoch 11, step 8020, loss = 1.34541, accuracy = 0.53125
    epoch 11, step 8030, loss = 1.99951, accuracy = 0.234375
    epoch 11, step 8040, loss = 1.20638, accuracy = 0.578125
    epoch 11, step 8050, loss = 1.37341, accuracy = 0.484375
    epoch 11, step 8060, loss = 1.35160, accuracy = 0.546875
    epoch 11, step 8070, loss = 1.30937, accuracy = 0.484375
    epoch 11, step 8080, loss = 1.36041, accuracy = 0.609375
    epoch 11, step 8090, loss = 1.44310, accuracy = 0.5
    epoch 11, step 8100, loss = 1.66236, accuracy = 0.40625
    epoch 11, step 8110, loss = 1.53428, accuracy = 0.46875
    epoch 11, step 8120, loss = 1.34387, accuracy = 0.5
    epoch 11, step 8130, loss = 1.47595, accuracy = 0.453125
    epoch 11, step 8140, loss = 1.34628, accuracy = 0.53125
    epoch 11, step 8150, loss = 1.26903, accuracy = 0.59375
    epoch 11, step 8160, loss = 1.51039, accuracy = 0.46875
    epoch 11, step 8170, loss = 1.44770, accuracy = 0.46875
    epoch 11, step 8180, loss = 1.58224, accuracy = 0.359375
    epoch 11, step 8190, loss = 1.58506, accuracy = 0.453125
    epoch 11, step 8200, loss = 1.55187, accuracy = 0.4375
    epoch 11, step 8210, loss = 1.26542, accuracy = 0.546875
    epoch 11, step 8220, loss = 1.34573, accuracy = 0.453125
    epoch 11, step 8230, loss = 1.50362, accuracy = 0.515625
    epoch 11, step 8240, loss = 1.36540, accuracy = 0.484375
    epoch 11, step 8250, loss = 1.31031, accuracy = 0.5625
    epoch 11, step 8260, loss = 1.26194, accuracy = 0.578125
    epoch 11, step 8270, loss = 1.39097, accuracy = 0.4375
    epoch 11, step 8280, loss = 1.57307, accuracy = 0.453125
    epoch 11, step 8290, loss = 1.31144, accuracy = 0.5625
    epoch 11, step 8300, loss = 1.31887, accuracy = 0.46875
    epoch 11, step 8310, loss = 1.34555, accuracy = 0.53125
    epoch 11, step 8320, loss = 1.29709, accuracy = 0.546875
    epoch 11, step 8330, loss = 1.34669, accuracy = 0.53125
    epoch 11, step 8340, loss = 1.32180, accuracy = 0.578125
    epoch 11, step 8350, loss = 1.49420, accuracy = 0.578125
    epoch 11, step 8360, loss = 1.15445, accuracy = 0.609375
    epoch 11, step 8370, loss = 1.33313, accuracy = 0.5625
    epoch 11, step 8380, loss = 1.39808, accuracy = 0.5625
    epoch 11, step 8390, loss = 1.60310, accuracy = 0.40625
    epoch 11, step 8400, loss = 1.28116, accuracy = 0.53125
    epoch 11, step 8410, loss = 1.43506, accuracy = 0.421875
    epoch 11, step 8420, loss = 1.44035, accuracy = 0.421875
    epoch 11, step 8430, loss = 1.56964, accuracy = 0.546875
    validation after epoch 11: loss = 1.50648, accuracy = 0.462
    Decreased learning rate by 0.5
    epoch 12, step 8440, loss = 1.36040, accuracy = 0.5
    epoch 12, step 8450, loss = 1.14735, accuracy = 0.625
    epoch 12, step 8460, loss = 1.22916, accuracy = 0.578125
    epoch 12, step 8470, loss = 1.14377, accuracy = 0.578125
    epoch 12, step 8480, loss = 1.19058, accuracy = 0.578125
    epoch 12, step 8490, loss = 1.18623, accuracy = 0.546875
    epoch 12, step 8500, loss = 1.38571, accuracy = 0.515625
    epoch 12, step 8510, loss = 1.32032, accuracy = 0.53125
    epoch 12, step 8520, loss = 1.17581, accuracy = 0.515625
    epoch 12, step 8530, loss = 1.41552, accuracy = 0.453125
    epoch 12, step 8540, loss = 1.25029, accuracy = 0.640625
    epoch 12, step 8550, loss = 1.22588, accuracy = 0.5625
    epoch 12, step 8560, loss = 1.32896, accuracy = 0.484375
    epoch 12, step 8570, loss = 1.46402, accuracy = 0.515625
    epoch 12, step 8580, loss = 1.18289, accuracy = 0.5625
    epoch 12, step 8590, loss = 1.26925, accuracy = 0.5
    epoch 12, step 8600, loss = 1.14547, accuracy = 0.46875
    epoch 12, step 8610, loss = 1.15240, accuracy = 0.59375
    epoch 12, step 8620, loss = 1.13195, accuracy = 0.515625
    epoch 12, step 8630, loss = 1.36168, accuracy = 0.484375
    epoch 12, step 8640, loss = 1.27452, accuracy = 0.484375
    epoch 12, step 8650, loss = 1.33601, accuracy = 0.53125
    epoch 12, step 8660, loss = 1.17404, accuracy = 0.609375
    epoch 12, step 8670, loss = 1.12120, accuracy = 0.65625
    epoch 12, step 8680, loss = 1.03650, accuracy = 0.6875
    epoch 12, step 8690, loss = 1.42066, accuracy = 0.484375
    epoch 12, step 8700, loss = 1.19360, accuracy = 0.5
    epoch 12, step 8710, loss = 1.24971, accuracy = 0.546875
    epoch 12, step 8720, loss = 1.33796, accuracy = 0.453125
    epoch 12, step 8730, loss = 1.26622, accuracy = 0.53125
    epoch 12, step 8740, loss = 1.30923, accuracy = 0.59375
    epoch 12, step 8750, loss = 1.25042, accuracy = 0.515625
    epoch 12, step 8760, loss = 1.34542, accuracy = 0.546875
    epoch 12, step 8770, loss = 1.04115, accuracy = 0.640625
    epoch 12, step 8780, loss = 1.43822, accuracy = 0.53125
    epoch 12, step 8790, loss = 1.09269, accuracy = 0.578125
    epoch 12, step 8800, loss = 1.08939, accuracy = 0.65625
    epoch 12, step 8810, loss = 1.47038, accuracy = 0.484375
    epoch 12, step 8820, loss = 1.15520, accuracy = 0.578125
    epoch 12, step 8830, loss = 1.31179, accuracy = 0.5625
    epoch 12, step 8840, loss = 1.26017, accuracy = 0.5625
    epoch 12, step 8850, loss = 1.10758, accuracy = 0.671875
    epoch 12, step 8860, loss = 1.37408, accuracy = 0.5625
    epoch 12, step 8870, loss = 1.24644, accuracy = 0.625
    epoch 12, step 8880, loss = 1.24988, accuracy = 0.53125
    epoch 12, step 8890, loss = 1.21000, accuracy = 0.5625
    epoch 12, step 8900, loss = 1.44903, accuracy = 0.4375
    epoch 12, step 8910, loss = 1.36681, accuracy = 0.484375
    epoch 12, step 8920, loss = 1.33449, accuracy = 0.53125
    epoch 12, step 8930, loss = 1.16046, accuracy = 0.625
    epoch 12, step 8940, loss = 1.23775, accuracy = 0.546875
    epoch 12, step 8950, loss = 1.44552, accuracy = 0.453125
    epoch 12, step 8960, loss = 1.18949, accuracy = 0.53125
    epoch 12, step 8970, loss = 1.02677, accuracy = 0.65625
    epoch 12, step 8980, loss = 1.01787, accuracy = 0.640625
    epoch 12, step 8990, loss = 1.23674, accuracy = 0.546875
    epoch 12, step 9000, loss = 1.45776, accuracy = 0.53125
    epoch 12, step 9010, loss = 1.29259, accuracy = 0.5
    epoch 12, step 9020, loss = 1.29912, accuracy = 0.59375
    epoch 12, step 9030, loss = 1.45348, accuracy = 0.546875
    epoch 12, step 9040, loss = 1.26096, accuracy = 0.5
    epoch 12, step 9050, loss = 1.41738, accuracy = 0.515625
    epoch 12, step 9060, loss = 1.32667, accuracy = 0.515625
    epoch 12, step 9070, loss = 1.07116, accuracy = 0.625
    epoch 12, step 9080, loss = 1.28261, accuracy = 0.5
    epoch 12, step 9090, loss = 1.15515, accuracy = 0.578125
    epoch 12, step 9100, loss = 1.37831, accuracy = 0.546875
    epoch 12, step 9110, loss = 1.27591, accuracy = 0.59375
    epoch 12, step 9120, loss = 1.22000, accuracy = 0.640625
    epoch 12, step 9130, loss = 0.99419, accuracy = 0.671875
    validation after epoch 12: loss = 1.50467, accuracy = 0.4654
    epoch 13, step 9140, loss = 1.41081, accuracy = 0.46875
    epoch 13, step 9150, loss = 1.26368, accuracy = 0.515625
    epoch 13, step 9160, loss = 1.41997, accuracy = 0.515625
    epoch 13, step 9170, loss = 1.21018, accuracy = 0.59375
    epoch 13, step 9180, loss = 1.33247, accuracy = 0.59375
    epoch 13, step 9190, loss = 1.41683, accuracy = 0.484375
    epoch 13, step 9200, loss = 1.39035, accuracy = 0.484375
    epoch 13, step 9210, loss = 1.46884, accuracy = 0.484375
    epoch 13, step 9220, loss = 1.10728, accuracy = 0.53125
    epoch 13, step 9230, loss = 1.36058, accuracy = 0.46875
    epoch 13, step 9240, loss = 1.15224, accuracy = 0.578125
    epoch 13, step 9250, loss = 1.47885, accuracy = 0.453125
    epoch 13, step 9260, loss = 1.38963, accuracy = 0.40625
    epoch 13, step 9270, loss = 1.25881, accuracy = 0.578125
    epoch 13, step 9280, loss = 1.22844, accuracy = 0.546875
    epoch 13, step 9290, loss = 1.24369, accuracy = 0.5625
    epoch 13, step 9300, loss = 1.20982, accuracy = 0.640625
    epoch 13, step 9310, loss = 1.31112, accuracy = 0.46875
    epoch 13, step 9320, loss = 1.40057, accuracy = 0.53125
    epoch 13, step 9330, loss = 1.19516, accuracy = 0.59375
    epoch 13, step 9340, loss = 1.16158, accuracy = 0.578125
    epoch 13, step 9350, loss = 1.17333, accuracy = 0.5625
    epoch 13, step 9360, loss = 1.27793, accuracy = 0.578125
    epoch 13, step 9370, loss = 1.21497, accuracy = 0.5625
    epoch 13, step 9380, loss = 1.26702, accuracy = 0.625
    epoch 13, step 9390, loss = 1.33769, accuracy = 0.5
    epoch 13, step 9400, loss = 1.12903, accuracy = 0.65625
    epoch 13, step 9410, loss = 1.19207, accuracy = 0.5625
    epoch 13, step 9420, loss = 1.29727, accuracy = 0.5625
    epoch 13, step 9430, loss = 1.25997, accuracy = 0.546875
    epoch 13, step 9440, loss = 1.31397, accuracy = 0.53125
    epoch 13, step 9450, loss = 1.19932, accuracy = 0.625
    epoch 13, step 9460, loss = 1.40698, accuracy = 0.515625
    epoch 13, step 9470, loss = 1.55291, accuracy = 0.4375
    epoch 13, step 9480, loss = 1.30791, accuracy = 0.484375
    epoch 13, step 9490, loss = 1.31284, accuracy = 0.5625
    epoch 13, step 9500, loss = 1.15309, accuracy = 0.59375
    epoch 13, step 9510, loss = 1.25855, accuracy = 0.5625
    epoch 13, step 9520, loss = 1.01308, accuracy = 0.6875
    epoch 13, step 9530, loss = 1.31354, accuracy = 0.546875
    epoch 13, step 9540, loss = 1.13082, accuracy = 0.578125
    epoch 13, step 9550, loss = 1.31197, accuracy = 0.5625
    epoch 13, step 9560, loss = 1.19492, accuracy = 0.546875
    epoch 13, step 9570, loss = 1.14388, accuracy = 0.578125
    epoch 13, step 9580, loss = 1.34082, accuracy = 0.484375
    epoch 13, step 9590, loss = 1.14780, accuracy = 0.65625
    epoch 13, step 9600, loss = 1.41924, accuracy = 0.53125
    epoch 13, step 9610, loss = 1.26737, accuracy = 0.53125
    epoch 13, step 9620, loss = 1.24957, accuracy = 0.484375
    epoch 13, step 9630, loss = 1.33401, accuracy = 0.546875
    epoch 13, step 9640, loss = 1.13865, accuracy = 0.625
    epoch 13, step 9650, loss = 1.52156, accuracy = 0.421875
    epoch 13, step 9660, loss = 1.50057, accuracy = 0.5
    epoch 13, step 9670, loss = 1.23786, accuracy = 0.5625
    epoch 13, step 9680, loss = 1.28860, accuracy = 0.546875
    epoch 13, step 9690, loss = 1.03195, accuracy = 0.609375
    epoch 13, step 9700, loss = 1.28175, accuracy = 0.5625
    epoch 13, step 9710, loss = 1.46202, accuracy = 0.546875
    epoch 13, step 9720, loss = 1.39702, accuracy = 0.4375
    epoch 13, step 9730, loss = 1.09632, accuracy = 0.578125
    epoch 13, step 9740, loss = 1.18121, accuracy = 0.5625
    epoch 13, step 9750, loss = 1.43299, accuracy = 0.578125
    epoch 13, step 9760, loss = 1.15233, accuracy = 0.59375
    epoch 13, step 9770, loss = 1.37131, accuracy = 0.546875
    epoch 13, step 9780, loss = 1.25399, accuracy = 0.53125
    epoch 13, step 9790, loss = 1.05133, accuracy = 0.625
    epoch 13, step 9800, loss = 1.54214, accuracy = 0.453125
    epoch 13, step 9810, loss = 1.49981, accuracy = 0.53125
    epoch 13, step 9820, loss = 1.41232, accuracy = 0.515625
    epoch 13, step 9830, loss = 1.05502, accuracy = 0.671875
    epoch 13, step 9840, loss = 1.07550, accuracy = 0.59375
    validation after epoch 13: loss = 1.48266, accuracy = 0.4732
    epoch 14, step 9850, loss = 1.31802, accuracy = 0.53125
    epoch 14, step 9860, loss = 1.35325, accuracy = 0.46875
    epoch 14, step 9870, loss = 1.09273, accuracy = 0.5625
    epoch 14, step 9880, loss = 1.15799, accuracy = 0.609375
    epoch 14, step 9890, loss = 1.21670, accuracy = 0.59375
    epoch 14, step 9900, loss = 1.37956, accuracy = 0.484375
    epoch 14, step 9910, loss = 0.98838, accuracy = 0.640625
    epoch 14, step 9920, loss = 0.96493, accuracy = 0.625
    epoch 14, step 9930, loss = 1.20112, accuracy = 0.609375
    epoch 14, step 9940, loss = 1.17817, accuracy = 0.5625
    epoch 14, step 9950, loss = 1.15715, accuracy = 0.625
    epoch 14, step 9960, loss = 1.14814, accuracy = 0.59375
    epoch 14, step 9970, loss = 1.32567, accuracy = 0.546875
    epoch 14, step 9980, loss = 1.19574, accuracy = 0.53125
    epoch 14, step 9990, loss = 1.09672, accuracy = 0.640625
    epoch 14, step 10000, loss = 1.22194, accuracy = 0.578125
    epoch 14, step 10010, loss = 1.32477, accuracy = 0.546875
    epoch 14, step 10020, loss = 1.30735, accuracy = 0.546875
    epoch 14, step 10030, loss = 1.20924, accuracy = 0.640625
    epoch 14, step 10040, loss = 1.48656, accuracy = 0.59375
    epoch 14, step 10050, loss = 1.31354, accuracy = 0.59375
    epoch 14, step 10060, loss = 1.24648, accuracy = 0.578125
    epoch 14, step 10070, loss = 0.96564, accuracy = 0.6875
    epoch 14, step 10080, loss = 1.05939, accuracy = 0.671875
    epoch 14, step 10090, loss = 1.38630, accuracy = 0.5625
    epoch 14, step 10100, loss = 1.09710, accuracy = 0.578125
    epoch 14, step 10110, loss = 1.26667, accuracy = 0.546875
    epoch 14, step 10120, loss = 1.17749, accuracy = 0.609375
    epoch 14, step 10130, loss = 1.31588, accuracy = 0.46875
    epoch 14, step 10140, loss = 1.23130, accuracy = 0.453125
    epoch 14, step 10150, loss = 1.34079, accuracy = 0.5
    epoch 14, step 10160, loss = 1.38924, accuracy = 0.4375
    epoch 14, step 10170, loss = 1.35724, accuracy = 0.484375
    epoch 14, step 10180, loss = 1.04531, accuracy = 0.671875
    epoch 14, step 10190, loss = 1.24838, accuracy = 0.640625
    epoch 14, step 10200, loss = 1.21809, accuracy = 0.5625
    epoch 14, step 10210, loss = 1.11169, accuracy = 0.59375
    epoch 14, step 10220, loss = 1.26795, accuracy = 0.5625
    epoch 14, step 10230, loss = 1.20243, accuracy = 0.578125
    epoch 14, step 10240, loss = 1.20352, accuracy = 0.640625
    epoch 14, step 10250, loss = 0.95836, accuracy = 0.671875
    epoch 14, step 10260, loss = 1.16894, accuracy = 0.59375
    epoch 14, step 10270, loss = 1.35886, accuracy = 0.5
    epoch 14, step 10280, loss = 1.41071, accuracy = 0.5625
    epoch 14, step 10290, loss = 1.26183, accuracy = 0.53125
    epoch 14, step 10300, loss = 1.15388, accuracy = 0.625
    epoch 14, step 10310, loss = 1.33623, accuracy = 0.46875
    epoch 14, step 10320, loss = 1.24341, accuracy = 0.515625
    epoch 14, step 10330, loss = 1.22840, accuracy = 0.515625
    epoch 14, step 10340, loss = 1.37254, accuracy = 0.390625
    epoch 14, step 10350, loss = 1.36497, accuracy = 0.515625
    epoch 14, step 10360, loss = 1.27997, accuracy = 0.53125
    epoch 14, step 10370, loss = 1.28248, accuracy = 0.515625
    epoch 14, step 10380, loss = 1.28577, accuracy = 0.578125
    epoch 14, step 10390, loss = 1.08258, accuracy = 0.5625
    epoch 14, step 10400, loss = 1.21713, accuracy = 0.4375
    epoch 14, step 10410, loss = 1.35184, accuracy = 0.5
    epoch 14, step 10420, loss = 1.36036, accuracy = 0.546875
    epoch 14, step 10430, loss = 1.43665, accuracy = 0.421875
    epoch 14, step 10440, loss = 1.34961, accuracy = 0.578125
    epoch 14, step 10450, loss = 1.43287, accuracy = 0.453125
    epoch 14, step 10460, loss = 1.20996, accuracy = 0.609375
    epoch 14, step 10470, loss = 1.35825, accuracy = 0.46875
    epoch 14, step 10480, loss = 1.22986, accuracy = 0.515625
    epoch 14, step 10490, loss = 1.09709, accuracy = 0.640625
    epoch 14, step 10500, loss = 1.19547, accuracy = 0.640625
    epoch 14, step 10510, loss = 1.39587, accuracy = 0.546875
    epoch 14, step 10520, loss = 1.12194, accuracy = 0.671875
    epoch 14, step 10530, loss = 1.23191, accuracy = 0.5
    epoch 14, step 10540, loss = 1.20516, accuracy = 0.5
    validation after epoch 14: loss = 1.50480, accuracy = 0.4656
    Decreased learning rate by 0.5
    epoch 15, step 10550, loss = 1.32998, accuracy = 0.46875
    epoch 15, step 10560, loss = 1.08129, accuracy = 0.625
    epoch 15, step 10570, loss = 1.25190, accuracy = 0.5
    epoch 15, step 10580, loss = 1.34486, accuracy = 0.453125
    epoch 15, step 10590, loss = 1.23787, accuracy = 0.640625
    epoch 15, step 10600, loss = 1.07399, accuracy = 0.640625
    epoch 15, step 10610, loss = 1.13801, accuracy = 0.515625
    epoch 15, step 10620, loss = 1.33846, accuracy = 0.609375
    epoch 15, step 10630, loss = 1.07840, accuracy = 0.59375
    epoch 15, step 10640, loss = 1.24553, accuracy = 0.515625
    epoch 15, step 10650, loss = 1.20389, accuracy = 0.515625
    epoch 15, step 10660, loss = 1.12384, accuracy = 0.578125
    epoch 15, step 10670, loss = 1.24601, accuracy = 0.546875
    epoch 15, step 10680, loss = 1.16374, accuracy = 0.5625
    epoch 15, step 10690, loss = 0.99705, accuracy = 0.671875
    epoch 15, step 10700, loss = 1.03363, accuracy = 0.671875
    epoch 15, step 10710, loss = 1.18327, accuracy = 0.65625
    epoch 15, step 10720, loss = 1.04615, accuracy = 0.6875
    epoch 15, step 10730, loss = 1.09549, accuracy = 0.671875
    epoch 15, step 10740, loss = 1.21164, accuracy = 0.578125
    epoch 15, step 10750, loss = 1.28649, accuracy = 0.578125
    epoch 15, step 10760, loss = 1.25163, accuracy = 0.53125
    epoch 15, step 10770, loss = 1.16754, accuracy = 0.625
    epoch 15, step 10780, loss = 1.30228, accuracy = 0.5
    epoch 15, step 10790, loss = 1.10316, accuracy = 0.59375
    epoch 15, step 10800, loss = 1.21733, accuracy = 0.5625
    epoch 15, step 10810, loss = 1.29879, accuracy = 0.4375
    epoch 15, step 10820, loss = 1.09421, accuracy = 0.609375
    epoch 15, step 10830, loss = 1.11683, accuracy = 0.5625
    epoch 15, step 10840, loss = 1.24694, accuracy = 0.5625
    epoch 15, step 10850, loss = 1.00489, accuracy = 0.640625
    epoch 15, step 10860, loss = 1.17529, accuracy = 0.578125
    epoch 15, step 10870, loss = 1.10691, accuracy = 0.5625
    epoch 15, step 10880, loss = 1.15337, accuracy = 0.578125
    epoch 15, step 10890, loss = 1.19726, accuracy = 0.5
    epoch 15, step 10900, loss = 1.25321, accuracy = 0.53125
    epoch 15, step 10910, loss = 1.21109, accuracy = 0.515625
    epoch 15, step 10920, loss = 1.18694, accuracy = 0.59375
    epoch 15, step 10930, loss = 1.31773, accuracy = 0.4375
    epoch 15, step 10940, loss = 1.34328, accuracy = 0.5
    epoch 15, step 10950, loss = 1.24568, accuracy = 0.578125
    epoch 15, step 10960, loss = 1.16523, accuracy = 0.546875
    epoch 15, step 10970, loss = 1.16304, accuracy = 0.59375
    epoch 15, step 10980, loss = 1.18284, accuracy = 0.578125
    epoch 15, step 10990, loss = 1.29741, accuracy = 0.5
    epoch 15, step 11000, loss = 1.45594, accuracy = 0.453125
    epoch 15, step 11010, loss = 1.26140, accuracy = 0.46875
    epoch 15, step 11020, loss = 1.14801, accuracy = 0.5625
    epoch 15, step 11030, loss = 0.99986, accuracy = 0.609375
    epoch 15, step 11040, loss = 1.09826, accuracy = 0.5625
    epoch 15, step 11050, loss = 1.20652, accuracy = 0.53125
    epoch 15, step 11060, loss = 1.09918, accuracy = 0.609375
    epoch 15, step 11070, loss = 1.22424, accuracy = 0.5625
    epoch 15, step 11080, loss = 1.34777, accuracy = 0.46875
    epoch 15, step 11090, loss = 1.11757, accuracy = 0.59375
    epoch 15, step 11100, loss = 1.38343, accuracy = 0.578125
    epoch 15, step 11110, loss = 1.17568, accuracy = 0.65625
    epoch 15, step 11120, loss = 1.07686, accuracy = 0.640625
    epoch 15, step 11130, loss = 1.35424, accuracy = 0.5625
    epoch 15, step 11140, loss = 1.40418, accuracy = 0.40625
    epoch 15, step 11150, loss = 1.24058, accuracy = 0.515625
    epoch 15, step 11160, loss = 1.17347, accuracy = 0.640625
    epoch 15, step 11170, loss = 1.25237, accuracy = 0.53125
    epoch 15, step 11180, loss = 1.01878, accuracy = 0.625
    epoch 15, step 11190, loss = 1.24738, accuracy = 0.5
    epoch 15, step 11200, loss = 1.21274, accuracy = 0.59375
    epoch 15, step 11210, loss = 1.21375, accuracy = 0.5625
    epoch 15, step 11220, loss = 1.28451, accuracy = 0.5
    epoch 15, step 11230, loss = 1.00115, accuracy = 0.703125
    epoch 15, step 11240, loss = 1.09103, accuracy = 0.609375
    validation after epoch 15: loss = 1.47830, accuracy = 0.4804
    epoch 16, step 11250, loss = 1.09650, accuracy = 0.5625
    epoch 16, step 11260, loss = 1.05556, accuracy = 0.65625
    epoch 16, step 11270, loss = 1.03295, accuracy = 0.671875
    epoch 16, step 11280, loss = 1.18080, accuracy = 0.546875
    epoch 16, step 11290, loss = 0.97125, accuracy = 0.65625
    epoch 16, step 11300, loss = 1.17816, accuracy = 0.59375
    epoch 16, step 11310, loss = 1.23090, accuracy = 0.515625
    epoch 16, step 11320, loss = 1.38894, accuracy = 0.5
    epoch 16, step 11330, loss = 1.32435, accuracy = 0.5
    epoch 16, step 11340, loss = 1.15424, accuracy = 0.625
    epoch 16, step 11350, loss = 1.21716, accuracy = 0.59375
    epoch 16, step 11360, loss = 1.23900, accuracy = 0.515625
    epoch 16, step 11370, loss = 1.06355, accuracy = 0.59375
    epoch 16, step 11380, loss = 1.11472, accuracy = 0.640625
    epoch 16, step 11390, loss = 1.19538, accuracy = 0.640625
    epoch 16, step 11400, loss = 1.14304, accuracy = 0.59375
    epoch 16, step 11410, loss = 1.14719, accuracy = 0.609375
    epoch 16, step 11420, loss = 1.14011, accuracy = 0.5625
    epoch 16, step 11430, loss = 1.00704, accuracy = 0.625
    epoch 16, step 11440, loss = 1.22125, accuracy = 0.578125
    epoch 16, step 11450, loss = 1.42276, accuracy = 0.46875
    epoch 16, step 11460, loss = 1.14558, accuracy = 0.5625
    epoch 16, step 11470, loss = 0.98927, accuracy = 0.671875
    epoch 16, step 11480, loss = 0.93903, accuracy = 0.703125
    epoch 16, step 11490, loss = 1.11608, accuracy = 0.59375
    epoch 16, step 11500, loss = 0.95622, accuracy = 0.765625
    epoch 16, step 11510, loss = 1.03438, accuracy = 0.671875
    epoch 16, step 11520, loss = 1.25755, accuracy = 0.515625
    epoch 16, step 11530, loss = 1.23942, accuracy = 0.546875
    epoch 16, step 11540, loss = 1.24367, accuracy = 0.546875
    epoch 16, step 11550, loss = 1.04757, accuracy = 0.6875
    epoch 16, step 11560, loss = 1.24168, accuracy = 0.53125
    epoch 16, step 11570, loss = 1.27527, accuracy = 0.640625
    epoch 16, step 11580, loss = 1.21946, accuracy = 0.640625
    epoch 16, step 11590, loss = 1.08758, accuracy = 0.59375
    epoch 16, step 11600, loss = 1.22111, accuracy = 0.53125
    epoch 16, step 11610, loss = 1.02644, accuracy = 0.6875
    epoch 16, step 11620, loss = 1.21283, accuracy = 0.625
    epoch 16, step 11630, loss = 1.13045, accuracy = 0.671875
    epoch 16, step 11640, loss = 1.33923, accuracy = 0.59375
    epoch 16, step 11650, loss = 1.17836, accuracy = 0.59375
    epoch 16, step 11660, loss = 1.25717, accuracy = 0.625
    epoch 16, step 11670, loss = 1.53098, accuracy = 0.53125
    epoch 16, step 11680, loss = 1.26450, accuracy = 0.609375
    epoch 16, step 11690, loss = 1.02688, accuracy = 0.578125
    epoch 16, step 11700, loss = 1.11885, accuracy = 0.65625
    epoch 16, step 11710, loss = 1.04611, accuracy = 0.640625
    epoch 16, step 11720, loss = 1.31454, accuracy = 0.578125
    epoch 16, step 11730, loss = 1.14519, accuracy = 0.59375
    epoch 16, step 11740, loss = 1.22999, accuracy = 0.53125
    epoch 16, step 11750, loss = 1.12359, accuracy = 0.59375
    epoch 16, step 11760, loss = 1.07586, accuracy = 0.609375
    epoch 16, step 11770, loss = 1.18017, accuracy = 0.59375
    epoch 16, step 11780, loss = 1.05710, accuracy = 0.625
    epoch 16, step 11790, loss = 1.10422, accuracy = 0.625
    epoch 16, step 11800, loss = 1.05710, accuracy = 0.546875
    epoch 16, step 11810, loss = 1.09383, accuracy = 0.515625
    epoch 16, step 11820, loss = 1.17745, accuracy = 0.609375
    epoch 16, step 11830, loss = 0.94751, accuracy = 0.671875
    epoch 16, step 11840, loss = 1.17811, accuracy = 0.625
    epoch 16, step 11850, loss = 0.96013, accuracy = 0.671875
    epoch 16, step 11860, loss = 1.05299, accuracy = 0.5625
    epoch 16, step 11870, loss = 1.10287, accuracy = 0.640625
    epoch 16, step 11880, loss = 1.47805, accuracy = 0.46875
    epoch 16, step 11890, loss = 1.31955, accuracy = 0.515625
    epoch 16, step 11900, loss = 1.25307, accuracy = 0.5
    epoch 16, step 11910, loss = 1.18825, accuracy = 0.546875
    epoch 16, step 11920, loss = 1.33626, accuracy = 0.421875
    epoch 16, step 11930, loss = 1.26169, accuracy = 0.546875
    epoch 16, step 11940, loss = 0.95428, accuracy = 0.71875
    epoch 16, step 11950, loss = 1.09625, accuracy = 0.53125
    validation after epoch 16: loss = 1.49077, accuracy = 0.481
    epoch 17, step 11960, loss = 1.30815, accuracy = 0.609375
    epoch 17, step 11970, loss = 1.12555, accuracy = 0.5625
    epoch 17, step 11980, loss = 1.15160, accuracy = 0.65625
    epoch 17, step 11990, loss = 0.89219, accuracy = 0.625
    epoch 17, step 12000, loss = 1.17625, accuracy = 0.5625
    epoch 17, step 12010, loss = 1.03738, accuracy = 0.625
    epoch 17, step 12020, loss = 1.00722, accuracy = 0.703125
    epoch 17, step 12030, loss = 1.05675, accuracy = 0.640625
    epoch 17, step 12040, loss = 1.12418, accuracy = 0.640625
    epoch 17, step 12050, loss = 1.00565, accuracy = 0.625
    epoch 17, step 12060, loss = 0.94711, accuracy = 0.640625
    epoch 17, step 12070, loss = 1.12416, accuracy = 0.59375
    epoch 17, step 12080, loss = 1.25689, accuracy = 0.609375
    epoch 17, step 12090, loss = 1.17441, accuracy = 0.640625
    epoch 17, step 12100, loss = 1.07465, accuracy = 0.65625
    epoch 17, step 12110, loss = 1.21832, accuracy = 0.59375
    epoch 17, step 12120, loss = 1.16025, accuracy = 0.578125
    epoch 17, step 12130, loss = 1.12222, accuracy = 0.625
    epoch 17, step 12140, loss = 1.25773, accuracy = 0.484375
    epoch 17, step 12150, loss = 1.22223, accuracy = 0.625
    epoch 17, step 12160, loss = 0.85655, accuracy = 0.78125
    epoch 17, step 12170, loss = 1.12250, accuracy = 0.609375
    epoch 17, step 12180, loss = 1.07293, accuracy = 0.671875
    epoch 17, step 12190, loss = 1.07633, accuracy = 0.578125
    epoch 17, step 12200, loss = 1.03586, accuracy = 0.625
    epoch 17, step 12210, loss = 1.04247, accuracy = 0.640625
    epoch 17, step 12220, loss = 1.09270, accuracy = 0.625
    epoch 17, step 12230, loss = 0.99245, accuracy = 0.703125
    epoch 17, step 12240, loss = 1.19513, accuracy = 0.609375
    epoch 17, step 12250, loss = 1.24218, accuracy = 0.53125
    epoch 17, step 12260, loss = 1.01661, accuracy = 0.6875
    epoch 17, step 12270, loss = 1.26077, accuracy = 0.609375
    epoch 17, step 12280, loss = 1.19437, accuracy = 0.59375
    epoch 17, step 12290, loss = 1.22411, accuracy = 0.53125
    epoch 17, step 12300, loss = 1.06974, accuracy = 0.546875
    epoch 17, step 12310, loss = 1.24643, accuracy = 0.53125
    epoch 17, step 12320, loss = 1.25960, accuracy = 0.5625
    epoch 17, step 12330, loss = 0.98693, accuracy = 0.609375
    epoch 17, step 12340, loss = 0.98004, accuracy = 0.65625
    epoch 17, step 12350, loss = 1.15744, accuracy = 0.484375
    epoch 17, step 12360, loss = 1.29302, accuracy = 0.515625
    epoch 17, step 12370, loss = 1.07439, accuracy = 0.65625
    epoch 17, step 12380, loss = 1.18122, accuracy = 0.59375
    epoch 17, step 12390, loss = 1.04582, accuracy = 0.609375
    epoch 17, step 12400, loss = 1.26729, accuracy = 0.59375
    epoch 17, step 12410, loss = 0.99960, accuracy = 0.703125
    epoch 17, step 12420, loss = 1.22461, accuracy = 0.578125
    epoch 17, step 12430, loss = 1.12381, accuracy = 0.5625
    epoch 17, step 12440, loss = 1.16840, accuracy = 0.546875
    epoch 17, step 12450, loss = 1.19632, accuracy = 0.59375
    epoch 17, step 12460, loss = 1.22606, accuracy = 0.59375
    epoch 17, step 12470, loss = 1.19690, accuracy = 0.515625
    epoch 17, step 12480, loss = 1.11615, accuracy = 0.625
    epoch 17, step 12490, loss = 1.03723, accuracy = 0.65625
    epoch 17, step 12500, loss = 1.17612, accuracy = 0.53125
    epoch 17, step 12510, loss = 1.19423, accuracy = 0.671875
    epoch 17, step 12520, loss = 1.07504, accuracy = 0.640625
    epoch 17, step 12530, loss = 1.29088, accuracy = 0.5625
    epoch 17, step 12540, loss = 0.97095, accuracy = 0.6875
    epoch 17, step 12550, loss = 1.06637, accuracy = 0.625
    epoch 17, step 12560, loss = 1.06824, accuracy = 0.59375
    epoch 17, step 12570, loss = 1.04747, accuracy = 0.625
    epoch 17, step 12580, loss = 0.94047, accuracy = 0.765625
    epoch 17, step 12590, loss = 1.24751, accuracy = 0.515625
    epoch 17, step 12600, loss = 1.21923, accuracy = 0.53125
    epoch 17, step 12610, loss = 1.16661, accuracy = 0.453125
    epoch 17, step 12620, loss = 1.27294, accuracy = 0.5625
    epoch 17, step 12630, loss = 1.11724, accuracy = 0.59375
    epoch 17, step 12640, loss = 1.34165, accuracy = 0.53125
    epoch 17, step 12650, loss = 1.04215, accuracy = 0.65625
    validation after epoch 17: loss = 1.50132, accuracy = 0.4716
    Decreased learning rate by 0.5
    epoch 18, step 12660, loss = 1.15967, accuracy = 0.546875
    epoch 18, step 12670, loss = 1.19942, accuracy = 0.5625
    epoch 18, step 12680, loss = 1.10344, accuracy = 0.59375
    epoch 18, step 12690, loss = 1.16117, accuracy = 0.59375
    epoch 18, step 12700, loss = 1.08567, accuracy = 0.671875
    epoch 18, step 12710, loss = 1.12083, accuracy = 0.609375
    epoch 18, step 12720, loss = 1.14360, accuracy = 0.59375
    epoch 18, step 12730, loss = 1.02995, accuracy = 0.6875
    epoch 18, step 12740, loss = 1.13310, accuracy = 0.625
    epoch 18, step 12750, loss = 0.90123, accuracy = 0.65625
    epoch 18, step 12760, loss = 1.09662, accuracy = 0.609375
    epoch 18, step 12770, loss = 1.06608, accuracy = 0.671875
    epoch 18, step 12780, loss = 1.22865, accuracy = 0.625
    epoch 18, step 12790, loss = 1.01866, accuracy = 0.625
    epoch 18, step 12800, loss = 1.15359, accuracy = 0.640625
    epoch 18, step 12810, loss = 1.22360, accuracy = 0.609375
    epoch 18, step 12820, loss = 1.27504, accuracy = 0.546875
    epoch 18, step 12830, loss = 1.01583, accuracy = 0.75
    epoch 18, step 12840, loss = 1.06461, accuracy = 0.65625
    epoch 18, step 12850, loss = 1.02543, accuracy = 0.640625
    epoch 18, step 12860, loss = 0.99653, accuracy = 0.640625
    epoch 18, step 12870, loss = 1.09280, accuracy = 0.625
    epoch 18, step 12880, loss = 1.22984, accuracy = 0.578125
    epoch 18, step 12890, loss = 1.02117, accuracy = 0.640625
    epoch 18, step 12900, loss = 1.07319, accuracy = 0.5625
    epoch 18, step 12910, loss = 1.38527, accuracy = 0.453125
    epoch 18, step 12920, loss = 1.05522, accuracy = 0.625
    epoch 18, step 12930, loss = 1.12999, accuracy = 0.59375
    epoch 18, step 12940, loss = 0.98624, accuracy = 0.703125
    epoch 18, step 12950, loss = 1.07089, accuracy = 0.5625
    epoch 18, step 12960, loss = 1.33629, accuracy = 0.453125
    epoch 18, step 12970, loss = 1.12846, accuracy = 0.5
    epoch 18, step 12980, loss = 0.98042, accuracy = 0.6875
    epoch 18, step 12990, loss = 1.22243, accuracy = 0.578125
    epoch 18, step 13000, loss = 1.13341, accuracy = 0.53125
    epoch 18, step 13010, loss = 1.06764, accuracy = 0.59375
    epoch 18, step 13020, loss = 1.12002, accuracy = 0.578125
    epoch 18, step 13030, loss = 1.28529, accuracy = 0.53125
    epoch 18, step 13040, loss = 1.10301, accuracy = 0.515625
    epoch 18, step 13050, loss = 1.17955, accuracy = 0.546875
    epoch 18, step 13060, loss = 1.06446, accuracy = 0.59375
    epoch 18, step 13070, loss = 1.17959, accuracy = 0.546875
    epoch 18, step 13080, loss = 1.02136, accuracy = 0.671875
    epoch 18, step 13090, loss = 1.17038, accuracy = 0.625
    epoch 18, step 13100, loss = 1.08711, accuracy = 0.625
    epoch 18, step 13110, loss = 1.07440, accuracy = 0.609375
    epoch 18, step 13120, loss = 0.89034, accuracy = 0.671875
    epoch 18, step 13130, loss = 1.23086, accuracy = 0.625
    epoch 18, step 13140, loss = 0.99110, accuracy = 0.6875
    epoch 18, step 13150, loss = 1.00211, accuracy = 0.671875
    epoch 18, step 13160, loss = 0.93217, accuracy = 0.75
    epoch 18, step 13170, loss = 0.97459, accuracy = 0.625
    epoch 18, step 13180, loss = 1.19496, accuracy = 0.421875
    epoch 18, step 13190, loss = 1.06881, accuracy = 0.578125
    epoch 18, step 13200, loss = 1.10893, accuracy = 0.515625
    epoch 18, step 13210, loss = 1.14511, accuracy = 0.578125
    epoch 18, step 13220, loss = 1.09557, accuracy = 0.625
    epoch 18, step 13230, loss = 1.00020, accuracy = 0.625
    epoch 18, step 13240, loss = 1.13825, accuracy = 0.53125
    epoch 18, step 13250, loss = 1.12697, accuracy = 0.5625
    epoch 18, step 13260, loss = 1.10007, accuracy = 0.546875
    epoch 18, step 13270, loss = 1.17129, accuracy = 0.625
    epoch 18, step 13280, loss = 1.06826, accuracy = 0.59375
    epoch 18, step 13290, loss = 1.25862, accuracy = 0.546875
    epoch 18, step 13300, loss = 0.94404, accuracy = 0.640625
    epoch 18, step 13310, loss = 1.03222, accuracy = 0.65625
    epoch 18, step 13320, loss = 1.27302, accuracy = 0.5
    epoch 18, step 13330, loss = 1.02360, accuracy = 0.65625
    epoch 18, step 13340, loss = 1.17278, accuracy = 0.5625
    epoch 18, step 13350, loss = 0.99101, accuracy = 0.65625
    validation after epoch 18: loss = 1.48520, accuracy = 0.484
    epoch 19, step 13360, loss = 1.07056, accuracy = 0.578125
    epoch 19, step 13370, loss = 1.22815, accuracy = 0.5625
    epoch 19, step 13380, loss = 1.01571, accuracy = 0.625
    epoch 19, step 13390, loss = 0.96380, accuracy = 0.671875
    epoch 19, step 13400, loss = 1.26443, accuracy = 0.578125
    epoch 19, step 13410, loss = 1.16892, accuracy = 0.5625
    epoch 19, step 13420, loss = 1.19396, accuracy = 0.65625
    epoch 19, step 13430, loss = 1.29547, accuracy = 0.609375
    epoch 19, step 13440, loss = 1.02242, accuracy = 0.625
    epoch 19, step 13450, loss = 1.08792, accuracy = 0.65625
    epoch 19, step 13460, loss = 0.99821, accuracy = 0.65625
    epoch 19, step 13470, loss = 0.95939, accuracy = 0.703125
    epoch 19, step 13480, loss = 1.16914, accuracy = 0.546875
    epoch 19, step 13490, loss = 1.25419, accuracy = 0.625
    epoch 19, step 13500, loss = 1.30236, accuracy = 0.578125
    epoch 19, step 13510, loss = 0.87669, accuracy = 0.71875
    epoch 19, step 13520, loss = 1.18742, accuracy = 0.546875
    epoch 19, step 13530, loss = 1.15034, accuracy = 0.609375
    epoch 19, step 13540, loss = 1.00830, accuracy = 0.671875
    epoch 19, step 13550, loss = 1.18174, accuracy = 0.578125
    epoch 19, step 13560, loss = 1.16488, accuracy = 0.53125
    epoch 19, step 13570, loss = 1.13469, accuracy = 0.546875
    epoch 19, step 13580, loss = 1.33325, accuracy = 0.46875
    epoch 19, step 13590, loss = 1.23153, accuracy = 0.5625
    epoch 19, step 13600, loss = 0.94367, accuracy = 0.734375
    epoch 19, step 13610, loss = 1.12855, accuracy = 0.609375
    epoch 19, step 13620, loss = 1.06766, accuracy = 0.640625
    epoch 19, step 13630, loss = 1.07861, accuracy = 0.5625
    epoch 19, step 13640, loss = 1.04693, accuracy = 0.640625
    epoch 19, step 13650, loss = 0.87421, accuracy = 0.71875
    epoch 19, step 13660, loss = 1.22917, accuracy = 0.59375
    epoch 19, step 13670, loss = 1.33570, accuracy = 0.5625
    epoch 19, step 13680, loss = 1.07161, accuracy = 0.65625
    epoch 19, step 13690, loss = 1.06474, accuracy = 0.625
    epoch 19, step 13700, loss = 1.01113, accuracy = 0.625
    epoch 19, step 13710, loss = 0.81936, accuracy = 0.65625
    epoch 19, step 13720, loss = 1.03644, accuracy = 0.65625
    epoch 19, step 13730, loss = 0.93930, accuracy = 0.6875
    epoch 19, step 13740, loss = 1.12524, accuracy = 0.578125
    epoch 19, step 13750, loss = 1.10280, accuracy = 0.640625
    epoch 19, step 13760, loss = 0.99240, accuracy = 0.6875
    epoch 19, step 13770, loss = 1.03324, accuracy = 0.6875
    epoch 19, step 13780, loss = 0.83071, accuracy = 0.703125
    epoch 19, step 13790, loss = 0.97714, accuracy = 0.6875
    epoch 19, step 13800, loss = 1.16313, accuracy = 0.5
    epoch 19, step 13810, loss = 1.23350, accuracy = 0.578125
    epoch 19, step 13820, loss = 1.01303, accuracy = 0.59375
    epoch 19, step 13830, loss = 0.89569, accuracy = 0.65625
    epoch 19, step 13840, loss = 1.12950, accuracy = 0.65625
    epoch 19, step 13850, loss = 1.11849, accuracy = 0.625
    epoch 19, step 13860, loss = 1.06700, accuracy = 0.609375
    epoch 19, step 13870, loss = 1.11693, accuracy = 0.671875
    epoch 19, step 13880, loss = 0.98474, accuracy = 0.765625
    epoch 19, step 13890, loss = 1.03500, accuracy = 0.6875
    epoch 19, step 13900, loss = 1.18587, accuracy = 0.625
    epoch 19, step 13910, loss = 1.05118, accuracy = 0.609375
    epoch 19, step 13920, loss = 1.25860, accuracy = 0.53125
    epoch 19, step 13930, loss = 1.18537, accuracy = 0.5625
    epoch 19, step 13940, loss = 1.15970, accuracy = 0.65625
    epoch 19, step 13950, loss = 0.92327, accuracy = 0.65625
    epoch 19, step 13960, loss = 0.92483, accuracy = 0.609375
    epoch 19, step 13970, loss = 1.12034, accuracy = 0.59375
    epoch 19, step 13980, loss = 1.05081, accuracy = 0.65625
    epoch 19, step 13990, loss = 1.17859, accuracy = 0.546875
    epoch 19, step 14000, loss = 0.92401, accuracy = 0.671875
    epoch 19, step 14010, loss = 1.01761, accuracy = 0.6875
    epoch 19, step 14020, loss = 1.11900, accuracy = 0.546875
    epoch 19, step 14030, loss = 1.12144, accuracy = 0.625
    epoch 19, step 14040, loss = 0.98339, accuracy = 0.703125
    epoch 19, step 14050, loss = 1.36414, accuracy = 0.453125
    validation after epoch 19: loss = 1.49149, accuracy = 0.4816
    
    Result:
    ------------------------------------
    loss on test set: 1.5043754924223525
    accuracy on test set: 0.4783
    
    Train statisistics:
    ------------------------------------
    time spend during forward pass: 146.21938967704773
    time spend during backward pass: 284.42598009109497
    time spend during l2 regularization: 431.52573895454407
    time spend during update pass: 241.94557929039001
    time spend in total: 1159.1003956794739
    
    Run training:
    ------------------------------------
    
    train method: dfa 
    num_passes: 20 
    batch_size: 64
    
    epoch 0, step 0, loss = 2.89163, accuracy = 0.09375
    epoch 0, step 10, loss = 2.88554, accuracy = 0.125
    epoch 0, step 20, loss = 2.82151, accuracy = 0.125
    epoch 0, step 30, loss = 2.67172, accuracy = 0.09375
    epoch 0, step 40, loss = 2.78211, accuracy = 0.140625
    epoch 0, step 50, loss = 2.54395, accuracy = 0.28125
    epoch 0, step 60, loss = 2.84415, accuracy = 0.203125
    epoch 0, step 70, loss = 2.52607, accuracy = 0.171875
    epoch 0, step 80, loss = 2.48600, accuracy = 0.3125
    epoch 0, step 90, loss = 2.55596, accuracy = 0.21875
    epoch 0, step 100, loss = 2.46394, accuracy = 0.34375
    epoch 0, step 110, loss = 2.61915, accuracy = 0.28125
    epoch 0, step 120, loss = 2.36707, accuracy = 0.34375
    epoch 0, step 130, loss = 2.32398, accuracy = 0.40625
    epoch 0, step 140, loss = 2.40982, accuracy = 0.3125
    epoch 0, step 150, loss = 2.34301, accuracy = 0.265625
    epoch 0, step 160, loss = 2.37015, accuracy = 0.34375
    epoch 0, step 170, loss = 2.32332, accuracy = 0.390625
    epoch 0, step 180, loss = 2.38770, accuracy = 0.25
    epoch 0, step 190, loss = 2.44644, accuracy = 0.265625
    epoch 0, step 200, loss = 2.23373, accuracy = 0.375
    epoch 0, step 210, loss = 2.20537, accuracy = 0.359375
    epoch 0, step 220, loss = 2.13582, accuracy = 0.375
    epoch 0, step 230, loss = 2.26575, accuracy = 0.375
    epoch 0, step 240, loss = 2.12290, accuracy = 0.390625
    epoch 0, step 250, loss = 2.44125, accuracy = 0.171875
    epoch 0, step 260, loss = 2.29072, accuracy = 0.25
    epoch 0, step 270, loss = 2.29068, accuracy = 0.375
    epoch 0, step 280, loss = 2.26969, accuracy = 0.375
    epoch 0, step 290, loss = 2.32344, accuracy = 0.328125
    epoch 0, step 300, loss = 2.21853, accuracy = 0.40625
    epoch 0, step 310, loss = 2.03353, accuracy = 0.453125
    epoch 0, step 320, loss = 2.17357, accuracy = 0.34375
    epoch 0, step 330, loss = 1.97411, accuracy = 0.375
    epoch 0, step 340, loss = 2.05794, accuracy = 0.421875
    epoch 0, step 350, loss = 2.25269, accuracy = 0.328125
    epoch 0, step 360, loss = 2.08193, accuracy = 0.390625
    epoch 0, step 370, loss = 2.21794, accuracy = 0.296875
    epoch 0, step 380, loss = 2.00994, accuracy = 0.390625
    epoch 0, step 390, loss = 2.11932, accuracy = 0.359375
    epoch 0, step 400, loss = 2.15137, accuracy = 0.390625
    epoch 0, step 410, loss = 2.08353, accuracy = 0.3125
    epoch 0, step 420, loss = 1.85519, accuracy = 0.4375
    epoch 0, step 430, loss = 2.05982, accuracy = 0.359375
    epoch 0, step 440, loss = 1.96431, accuracy = 0.4375
    epoch 0, step 450, loss = 1.98740, accuracy = 0.4375
    epoch 0, step 460, loss = 1.99007, accuracy = 0.3125
    epoch 0, step 470, loss = 1.80835, accuracy = 0.453125
    epoch 0, step 480, loss = 2.06055, accuracy = 0.34375
    epoch 0, step 490, loss = 2.21522, accuracy = 0.28125
    epoch 0, step 500, loss = 2.10076, accuracy = 0.40625
    epoch 0, step 510, loss = 2.03232, accuracy = 0.46875
    epoch 0, step 520, loss = 2.02967, accuracy = 0.359375
    epoch 0, step 530, loss = 2.19733, accuracy = 0.25
    epoch 0, step 540, loss = 2.01519, accuracy = 0.40625
    epoch 0, step 550, loss = 1.88686, accuracy = 0.375
    epoch 0, step 560, loss = 2.28108, accuracy = 0.265625
    epoch 0, step 570, loss = 2.15262, accuracy = 0.28125
    epoch 0, step 580, loss = 2.04194, accuracy = 0.390625
    epoch 0, step 590, loss = 1.89475, accuracy = 0.453125
    epoch 0, step 600, loss = 2.18698, accuracy = 0.28125
    epoch 0, step 610, loss = 2.06140, accuracy = 0.375
    epoch 0, step 620, loss = 2.06280, accuracy = 0.359375
    epoch 0, step 630, loss = 2.22292, accuracy = 0.328125
    epoch 0, step 640, loss = 1.93749, accuracy = 0.40625
    epoch 0, step 650, loss = 2.09141, accuracy = 0.375
    epoch 0, step 660, loss = 2.12592, accuracy = 0.3125
    epoch 0, step 670, loss = 2.02247, accuracy = 0.421875
    epoch 0, step 680, loss = 2.10894, accuracy = 0.421875
    epoch 0, step 690, loss = 2.02486, accuracy = 0.296875
    epoch 0, step 700, loss = 1.94362, accuracy = 0.5
    validation after epoch 0: loss = 1.77450, accuracy = 0.3714
    epoch 1, step 710, loss = 2.06698, accuracy = 0.4375
    epoch 1, step 720, loss = 1.92124, accuracy = 0.34375
    epoch 1, step 730, loss = 1.93202, accuracy = 0.453125
    epoch 1, step 740, loss = 1.99586, accuracy = 0.453125
    epoch 1, step 750, loss = 2.04168, accuracy = 0.34375
    epoch 1, step 760, loss = 1.94547, accuracy = 0.40625
    epoch 1, step 770, loss = 1.77684, accuracy = 0.5
    epoch 1, step 780, loss = 1.98846, accuracy = 0.421875
    epoch 1, step 790, loss = 2.26573, accuracy = 0.3125
    epoch 1, step 800, loss = 1.93330, accuracy = 0.390625
    epoch 1, step 810, loss = 1.97000, accuracy = 0.359375
    epoch 1, step 820, loss = 2.29645, accuracy = 0.21875
    epoch 1, step 830, loss = 2.02574, accuracy = 0.484375
    epoch 1, step 840, loss = 2.00001, accuracy = 0.390625
    epoch 1, step 850, loss = 2.15319, accuracy = 0.34375
    epoch 1, step 860, loss = 1.95074, accuracy = 0.4375
    epoch 1, step 870, loss = 1.99587, accuracy = 0.390625
    epoch 1, step 880, loss = 1.99972, accuracy = 0.359375
    epoch 1, step 890, loss = 1.71043, accuracy = 0.515625
    epoch 1, step 900, loss = 2.18901, accuracy = 0.359375
    epoch 1, step 910, loss = 1.99349, accuracy = 0.265625
    epoch 1, step 920, loss = 1.85393, accuracy = 0.40625
    epoch 1, step 930, loss = 2.27548, accuracy = 0.28125
    epoch 1, step 940, loss = 2.18766, accuracy = 0.234375
    epoch 1, step 950, loss = 1.77881, accuracy = 0.5
    epoch 1, step 960, loss = 1.99994, accuracy = 0.40625
    epoch 1, step 970, loss = 1.95601, accuracy = 0.34375
    epoch 1, step 980, loss = 2.07170, accuracy = 0.328125
    epoch 1, step 990, loss = 1.86421, accuracy = 0.484375
    epoch 1, step 1000, loss = 2.14954, accuracy = 0.328125
    epoch 1, step 1010, loss = 2.09602, accuracy = 0.375
    epoch 1, step 1020, loss = 2.02098, accuracy = 0.3125
    epoch 1, step 1030, loss = 2.10204, accuracy = 0.359375
    epoch 1, step 1040, loss = 1.90114, accuracy = 0.34375
    epoch 1, step 1050, loss = 1.89806, accuracy = 0.53125
    epoch 1, step 1060, loss = 2.02151, accuracy = 0.40625
    epoch 1, step 1070, loss = 2.10607, accuracy = 0.34375
    epoch 1, step 1080, loss = 1.93968, accuracy = 0.40625
    epoch 1, step 1090, loss = 1.98403, accuracy = 0.375
    epoch 1, step 1100, loss = 2.01434, accuracy = 0.40625
    epoch 1, step 1110, loss = 2.10951, accuracy = 0.421875
    epoch 1, step 1120, loss = 2.05594, accuracy = 0.328125
    epoch 1, step 1130, loss = 2.04961, accuracy = 0.34375
    epoch 1, step 1140, loss = 1.96521, accuracy = 0.390625
    epoch 1, step 1150, loss = 2.05416, accuracy = 0.359375
    epoch 1, step 1160, loss = 2.04487, accuracy = 0.359375
    epoch 1, step 1170, loss = 1.89760, accuracy = 0.40625
    epoch 1, step 1180, loss = 2.16987, accuracy = 0.328125
    epoch 1, step 1190, loss = 2.16119, accuracy = 0.265625
    epoch 1, step 1200, loss = 1.88328, accuracy = 0.375
    epoch 1, step 1210, loss = 1.99128, accuracy = 0.390625
    epoch 1, step 1220, loss = 1.95804, accuracy = 0.34375
    epoch 1, step 1230, loss = 2.07520, accuracy = 0.328125
    epoch 1, step 1240, loss = 2.21714, accuracy = 0.296875
    epoch 1, step 1250, loss = 1.94537, accuracy = 0.421875
    epoch 1, step 1260, loss = 2.03444, accuracy = 0.46875
    epoch 1, step 1270, loss = 2.02396, accuracy = 0.390625
    epoch 1, step 1280, loss = 1.94538, accuracy = 0.46875
    epoch 1, step 1290, loss = 2.18927, accuracy = 0.296875
    epoch 1, step 1300, loss = 2.22883, accuracy = 0.28125
    epoch 1, step 1310, loss = 2.10629, accuracy = 0.359375
    epoch 1, step 1320, loss = 2.05960, accuracy = 0.28125
    epoch 1, step 1330, loss = 2.07101, accuracy = 0.40625
    epoch 1, step 1340, loss = 1.99524, accuracy = 0.328125
    epoch 1, step 1350, loss = 2.08529, accuracy = 0.40625
    epoch 1, step 1360, loss = 1.68328, accuracy = 0.5
    epoch 1, step 1370, loss = 2.00049, accuracy = 0.34375
    epoch 1, step 1380, loss = 1.95621, accuracy = 0.390625
    epoch 1, step 1390, loss = 2.07226, accuracy = 0.34375
    epoch 1, step 1400, loss = 2.11478, accuracy = 0.234375
    validation after epoch 1: loss = 1.75574, accuracy = 0.388
    epoch 2, step 1410, loss = 2.16122, accuracy = 0.296875
    epoch 2, step 1420, loss = 1.92600, accuracy = 0.359375
    epoch 2, step 1430, loss = 1.95066, accuracy = 0.390625
    epoch 2, step 1440, loss = 2.09015, accuracy = 0.390625
    epoch 2, step 1450, loss = 2.30722, accuracy = 0.296875
    epoch 2, step 1460, loss = 2.31790, accuracy = 0.3125
    epoch 2, step 1470, loss = 1.94065, accuracy = 0.484375
    epoch 2, step 1480, loss = 1.94585, accuracy = 0.421875
    epoch 2, step 1490, loss = 2.07943, accuracy = 0.375
    epoch 2, step 1500, loss = 1.96203, accuracy = 0.375
    epoch 2, step 1510, loss = 1.94181, accuracy = 0.375
    epoch 2, step 1520, loss = 1.85828, accuracy = 0.46875
    epoch 2, step 1530, loss = 2.10532, accuracy = 0.359375
    epoch 2, step 1540, loss = 2.14231, accuracy = 0.328125
    epoch 2, step 1550, loss = 1.82813, accuracy = 0.421875
    epoch 2, step 1560, loss = 2.02185, accuracy = 0.375
    epoch 2, step 1570, loss = 2.01012, accuracy = 0.421875
    epoch 2, step 1580, loss = 2.28047, accuracy = 0.296875
    epoch 2, step 1590, loss = 1.95655, accuracy = 0.375
    epoch 2, step 1600, loss = 1.91963, accuracy = 0.453125
    epoch 2, step 1610, loss = 1.85483, accuracy = 0.40625
    epoch 2, step 1620, loss = 1.85603, accuracy = 0.421875
    epoch 2, step 1630, loss = 2.08120, accuracy = 0.28125
    epoch 2, step 1640, loss = 1.88526, accuracy = 0.421875
    epoch 2, step 1650, loss = 2.11938, accuracy = 0.40625
    epoch 2, step 1660, loss = 1.92438, accuracy = 0.40625
    epoch 2, step 1670, loss = 1.97160, accuracy = 0.3125
    epoch 2, step 1680, loss = 1.94429, accuracy = 0.453125
    epoch 2, step 1690, loss = 2.26352, accuracy = 0.296875
    epoch 2, step 1700, loss = 1.82936, accuracy = 0.34375
    epoch 2, step 1710, loss = 2.02785, accuracy = 0.4375
    epoch 2, step 1720, loss = 1.95037, accuracy = 0.359375
    epoch 2, step 1730, loss = 1.91929, accuracy = 0.40625
    epoch 2, step 1740, loss = 1.91067, accuracy = 0.40625
    epoch 2, step 1750, loss = 1.95371, accuracy = 0.375
    epoch 2, step 1760, loss = 2.09664, accuracy = 0.40625
    epoch 2, step 1770, loss = 1.92953, accuracy = 0.390625
    epoch 2, step 1780, loss = 2.08355, accuracy = 0.359375
    epoch 2, step 1790, loss = 1.79796, accuracy = 0.421875
    epoch 2, step 1800, loss = 1.80940, accuracy = 0.453125
    epoch 2, step 1810, loss = 1.97728, accuracy = 0.34375
    epoch 2, step 1820, loss = 1.99202, accuracy = 0.359375
    epoch 2, step 1830, loss = 2.00568, accuracy = 0.375
    epoch 2, step 1840, loss = 1.98829, accuracy = 0.390625
    epoch 2, step 1850, loss = 2.16408, accuracy = 0.296875
    epoch 2, step 1860, loss = 1.81386, accuracy = 0.46875
    epoch 2, step 1870, loss = 1.89892, accuracy = 0.421875
    epoch 2, step 1880, loss = 2.05334, accuracy = 0.390625
    epoch 2, step 1890, loss = 2.04085, accuracy = 0.34375
    epoch 2, step 1900, loss = 2.03656, accuracy = 0.390625
    epoch 2, step 1910, loss = 1.99473, accuracy = 0.40625
    epoch 2, step 1920, loss = 2.03701, accuracy = 0.390625
    epoch 2, step 1930, loss = 1.90935, accuracy = 0.4375
    epoch 2, step 1940, loss = 1.96666, accuracy = 0.359375
    epoch 2, step 1950, loss = 1.91656, accuracy = 0.359375
    epoch 2, step 1960, loss = 2.04934, accuracy = 0.34375
    epoch 2, step 1970, loss = 1.87631, accuracy = 0.4375
    epoch 2, step 1980, loss = 2.02424, accuracy = 0.28125
    epoch 2, step 1990, loss = 2.08723, accuracy = 0.25
    epoch 2, step 2000, loss = 1.94372, accuracy = 0.390625
    epoch 2, step 2010, loss = 1.97809, accuracy = 0.34375
    epoch 2, step 2020, loss = 2.14508, accuracy = 0.34375
    epoch 2, step 2030, loss = 1.91042, accuracy = 0.390625
    epoch 2, step 2040, loss = 1.86737, accuracy = 0.46875
    epoch 2, step 2050, loss = 2.04816, accuracy = 0.40625
    epoch 2, step 2060, loss = 2.25059, accuracy = 0.296875
    epoch 2, step 2070, loss = 2.09512, accuracy = 0.328125
    epoch 2, step 2080, loss = 2.16281, accuracy = 0.265625
    epoch 2, step 2090, loss = 1.97426, accuracy = 0.34375
    epoch 2, step 2100, loss = 1.77101, accuracy = 0.421875
    validation after epoch 2: loss = 1.78659, accuracy = 0.3672
    Decreased learning rate by 0.5
    epoch 3, step 2110, loss = 2.07771, accuracy = 0.359375
    epoch 3, step 2120, loss = 1.96612, accuracy = 0.421875
    epoch 3, step 2130, loss = 2.00860, accuracy = 0.34375
    epoch 3, step 2140, loss = 1.81537, accuracy = 0.4375
    epoch 3, step 2150, loss = 1.68803, accuracy = 0.53125
    epoch 3, step 2160, loss = 1.85191, accuracy = 0.4375
    epoch 3, step 2170, loss = 2.10383, accuracy = 0.34375
    epoch 3, step 2180, loss = 1.96019, accuracy = 0.359375
    epoch 3, step 2190, loss = 1.77934, accuracy = 0.484375
    epoch 3, step 2200, loss = 1.77183, accuracy = 0.515625
    epoch 3, step 2210, loss = 1.97719, accuracy = 0.359375
    epoch 3, step 2220, loss = 1.80567, accuracy = 0.484375
    epoch 3, step 2230, loss = 1.89368, accuracy = 0.453125
    epoch 3, step 2240, loss = 1.83115, accuracy = 0.390625
    epoch 3, step 2250, loss = 2.06137, accuracy = 0.375
    epoch 3, step 2260, loss = 1.98825, accuracy = 0.328125
    epoch 3, step 2270, loss = 1.94562, accuracy = 0.40625
    epoch 3, step 2280, loss = 1.89925, accuracy = 0.46875
    epoch 3, step 2290, loss = 1.75384, accuracy = 0.515625
    epoch 3, step 2300, loss = 2.34481, accuracy = 0.265625
    epoch 3, step 2310, loss = 2.14419, accuracy = 0.34375
    epoch 3, step 2320, loss = 1.99713, accuracy = 0.34375
    epoch 3, step 2330, loss = 2.04466, accuracy = 0.28125
    epoch 3, step 2340, loss = 1.92849, accuracy = 0.375
    epoch 3, step 2350, loss = 1.98299, accuracy = 0.21875
    epoch 3, step 2360, loss = 1.96019, accuracy = 0.375
    epoch 3, step 2370, loss = 1.96675, accuracy = 0.390625
    epoch 3, step 2380, loss = 1.81525, accuracy = 0.40625
    epoch 3, step 2390, loss = 1.87797, accuracy = 0.375
    epoch 3, step 2400, loss = 1.83992, accuracy = 0.453125
    epoch 3, step 2410, loss = 2.03596, accuracy = 0.390625
    epoch 3, step 2420, loss = 2.08299, accuracy = 0.359375
    epoch 3, step 2430, loss = 2.11017, accuracy = 0.3125
    epoch 3, step 2440, loss = 2.03523, accuracy = 0.34375
    epoch 3, step 2450, loss = 1.80805, accuracy = 0.546875
    epoch 3, step 2460, loss = 1.98665, accuracy = 0.34375
    epoch 3, step 2470, loss = 1.76498, accuracy = 0.5
    epoch 3, step 2480, loss = 1.86536, accuracy = 0.390625
    epoch 3, step 2490, loss = 1.78444, accuracy = 0.484375
    epoch 3, step 2500, loss = 1.90749, accuracy = 0.421875
    epoch 3, step 2510, loss = 2.10382, accuracy = 0.28125
    epoch 3, step 2520, loss = 1.66720, accuracy = 0.46875
    epoch 3, step 2530, loss = 1.81767, accuracy = 0.40625
    epoch 3, step 2540, loss = 1.88175, accuracy = 0.421875
    epoch 3, step 2550, loss = 1.89863, accuracy = 0.328125
    epoch 3, step 2560, loss = 1.69436, accuracy = 0.46875
    epoch 3, step 2570, loss = 1.68791, accuracy = 0.4375
    epoch 3, step 2580, loss = 1.93342, accuracy = 0.359375
    epoch 3, step 2590, loss = 1.75607, accuracy = 0.4375
    epoch 3, step 2600, loss = 1.72954, accuracy = 0.53125
    epoch 3, step 2610, loss = 1.78554, accuracy = 0.46875
    epoch 3, step 2620, loss = 1.93836, accuracy = 0.375
    epoch 3, step 2630, loss = 1.78262, accuracy = 0.375
    epoch 3, step 2640, loss = 1.85275, accuracy = 0.4375
    epoch 3, step 2650, loss = 1.74309, accuracy = 0.453125
    epoch 3, step 2660, loss = 1.91374, accuracy = 0.40625
    epoch 3, step 2670, loss = 1.86025, accuracy = 0.40625
    epoch 3, step 2680, loss = 1.86348, accuracy = 0.484375
    epoch 3, step 2690, loss = 1.82613, accuracy = 0.4375
    epoch 3, step 2700, loss = 2.04553, accuracy = 0.296875
    epoch 3, step 2710, loss = 1.75712, accuracy = 0.5
    epoch 3, step 2720, loss = 1.78611, accuracy = 0.46875
    epoch 3, step 2730, loss = 1.85788, accuracy = 0.4375
    epoch 3, step 2740, loss = 1.87676, accuracy = 0.390625
    epoch 3, step 2750, loss = 1.77387, accuracy = 0.40625
    epoch 3, step 2760, loss = 1.92159, accuracy = 0.359375
    epoch 3, step 2770, loss = 1.88397, accuracy = 0.390625
    epoch 3, step 2780, loss = 1.64989, accuracy = 0.53125
    epoch 3, step 2790, loss = 1.82008, accuracy = 0.359375
    epoch 3, step 2800, loss = 1.83374, accuracy = 0.359375
    epoch 3, step 2810, loss = 1.92321, accuracy = 0.34375
    validation after epoch 3: loss = 1.68588, accuracy = 0.3996
    epoch 4, step 2820, loss = 1.75385, accuracy = 0.484375
    epoch 4, step 2830, loss = 1.75749, accuracy = 0.421875
    epoch 4, step 2840, loss = 1.76005, accuracy = 0.4375
    epoch 4, step 2850, loss = 2.06445, accuracy = 0.359375
    epoch 4, step 2860, loss = 1.64090, accuracy = 0.5
    epoch 4, step 2870, loss = 1.66407, accuracy = 0.484375
    epoch 4, step 2880, loss = 1.72480, accuracy = 0.484375
    epoch 4, step 2890, loss = 1.86459, accuracy = 0.421875
    epoch 4, step 2900, loss = 1.79780, accuracy = 0.4375
    epoch 4, step 2910, loss = 1.83884, accuracy = 0.390625
    epoch 4, step 2920, loss = 1.79156, accuracy = 0.40625
    epoch 4, step 2930, loss = 1.78347, accuracy = 0.46875
    epoch 4, step 2940, loss = 1.77095, accuracy = 0.453125
    epoch 4, step 2950, loss = 1.81158, accuracy = 0.390625
    epoch 4, step 2960, loss = 1.87953, accuracy = 0.359375
    epoch 4, step 2970, loss = 2.05077, accuracy = 0.375
    epoch 4, step 2980, loss = 1.70963, accuracy = 0.5
    epoch 4, step 2990, loss = 1.85737, accuracy = 0.421875
    epoch 4, step 3000, loss = 1.74420, accuracy = 0.4375
    epoch 4, step 3010, loss = 1.63110, accuracy = 0.453125
    epoch 4, step 3020, loss = 1.83031, accuracy = 0.4375
    epoch 4, step 3030, loss = 1.89864, accuracy = 0.421875
    epoch 4, step 3040, loss = 1.68212, accuracy = 0.484375
    epoch 4, step 3050, loss = 1.91511, accuracy = 0.375
    epoch 4, step 3060, loss = 1.98478, accuracy = 0.375
    epoch 4, step 3070, loss = 1.78772, accuracy = 0.359375
    epoch 4, step 3080, loss = 1.75573, accuracy = 0.421875
    epoch 4, step 3090, loss = 2.00074, accuracy = 0.3125
    epoch 4, step 3100, loss = 1.68359, accuracy = 0.53125
    epoch 4, step 3110, loss = 1.75096, accuracy = 0.484375
    epoch 4, step 3120, loss = 1.91140, accuracy = 0.3125
    epoch 4, step 3130, loss = 1.81423, accuracy = 0.515625
    epoch 4, step 3140, loss = 2.08737, accuracy = 0.3125
    epoch 4, step 3150, loss = 1.73905, accuracy = 0.5
    epoch 4, step 3160, loss = 1.68269, accuracy = 0.546875
    epoch 4, step 3170, loss = 1.88574, accuracy = 0.46875
    epoch 4, step 3180, loss = 1.74327, accuracy = 0.515625
    epoch 4, step 3190, loss = 1.65852, accuracy = 0.46875
    epoch 4, step 3200, loss = 2.09565, accuracy = 0.375
    epoch 4, step 3210, loss = 1.76329, accuracy = 0.4375
    epoch 4, step 3220, loss = 1.95606, accuracy = 0.390625
    epoch 4, step 3230, loss = 1.92674, accuracy = 0.375
    epoch 4, step 3240, loss = 1.72677, accuracy = 0.4375
    epoch 4, step 3250, loss = 1.83947, accuracy = 0.46875
    epoch 4, step 3260, loss = 1.63817, accuracy = 0.5
    epoch 4, step 3270, loss = 1.72362, accuracy = 0.46875
    epoch 4, step 3280, loss = 1.69897, accuracy = 0.515625
    epoch 4, step 3290, loss = 1.80214, accuracy = 0.390625
    epoch 4, step 3300, loss = 1.76329, accuracy = 0.390625
    epoch 4, step 3310, loss = 1.65491, accuracy = 0.484375
    epoch 4, step 3320, loss = 1.79854, accuracy = 0.390625
    epoch 4, step 3330, loss = 2.09824, accuracy = 0.3125
    epoch 4, step 3340, loss = 1.78148, accuracy = 0.390625
    epoch 4, step 3350, loss = 1.67365, accuracy = 0.453125
    epoch 4, step 3360, loss = 1.86623, accuracy = 0.4375
    epoch 4, step 3370, loss = 1.69976, accuracy = 0.4375
    epoch 4, step 3380, loss = 1.93099, accuracy = 0.328125
    epoch 4, step 3390, loss = 1.70705, accuracy = 0.46875
    epoch 4, step 3400, loss = 1.95797, accuracy = 0.328125
    epoch 4, step 3410, loss = 1.82522, accuracy = 0.390625
    epoch 4, step 3420, loss = 1.70450, accuracy = 0.40625
    epoch 4, step 3430, loss = 1.71750, accuracy = 0.453125
    epoch 4, step 3440, loss = 1.87837, accuracy = 0.40625
    epoch 4, step 3450, loss = 1.79008, accuracy = 0.421875
    epoch 4, step 3460, loss = 1.71397, accuracy = 0.484375
    epoch 4, step 3470, loss = 1.57744, accuracy = 0.453125
    epoch 4, step 3480, loss = 1.92691, accuracy = 0.453125
    epoch 4, step 3490, loss = 1.79827, accuracy = 0.484375
    epoch 4, step 3500, loss = 1.62177, accuracy = 0.484375
    epoch 4, step 3510, loss = 1.51659, accuracy = 0.484375
    validation after epoch 4: loss = 1.66011, accuracy = 0.4152
    epoch 5, step 3520, loss = 1.85132, accuracy = 0.375
    epoch 5, step 3530, loss = 1.70838, accuracy = 0.484375
    epoch 5, step 3540, loss = 1.67879, accuracy = 0.46875
    epoch 5, step 3550, loss = 1.90709, accuracy = 0.390625
    epoch 5, step 3560, loss = 1.76248, accuracy = 0.375
    epoch 5, step 3570, loss = 1.91524, accuracy = 0.375
    epoch 5, step 3580, loss = 2.07413, accuracy = 0.359375
    epoch 5, step 3590, loss = 1.68502, accuracy = 0.4375
    epoch 5, step 3600, loss = 1.69527, accuracy = 0.453125
    epoch 5, step 3610, loss = 1.92784, accuracy = 0.390625
    epoch 5, step 3620, loss = 1.79766, accuracy = 0.5
    epoch 5, step 3630, loss = 1.70333, accuracy = 0.4375
    epoch 5, step 3640, loss = 1.83945, accuracy = 0.34375
    epoch 5, step 3650, loss = 1.62609, accuracy = 0.484375
    epoch 5, step 3660, loss = 1.82309, accuracy = 0.421875
    epoch 5, step 3670, loss = 1.85339, accuracy = 0.421875
    epoch 5, step 3680, loss = 1.90412, accuracy = 0.328125
    epoch 5, step 3690, loss = 1.70230, accuracy = 0.453125
    epoch 5, step 3700, loss = 1.91783, accuracy = 0.390625
    epoch 5, step 3710, loss = 1.76071, accuracy = 0.390625
    epoch 5, step 3720, loss = 1.80522, accuracy = 0.484375
    epoch 5, step 3730, loss = 2.02107, accuracy = 0.375
    epoch 5, step 3740, loss = 1.69796, accuracy = 0.453125
    epoch 5, step 3750, loss = 1.63186, accuracy = 0.53125
    epoch 5, step 3760, loss = 1.72767, accuracy = 0.515625
    epoch 5, step 3770, loss = 1.66029, accuracy = 0.375
    epoch 5, step 3780, loss = 1.76025, accuracy = 0.4375
    epoch 5, step 3790, loss = 1.82160, accuracy = 0.421875
    epoch 5, step 3800, loss = 1.83681, accuracy = 0.375
    epoch 5, step 3810, loss = 1.79024, accuracy = 0.421875
    epoch 5, step 3820, loss = 1.83153, accuracy = 0.359375
    epoch 5, step 3830, loss = 1.64450, accuracy = 0.421875
    epoch 5, step 3840, loss = 1.75932, accuracy = 0.390625
    epoch 5, step 3850, loss = 1.84397, accuracy = 0.421875
    epoch 5, step 3860, loss = 1.85709, accuracy = 0.4375
    epoch 5, step 3870, loss = 1.98756, accuracy = 0.390625
    epoch 5, step 3880, loss = 1.84630, accuracy = 0.390625
    epoch 5, step 3890, loss = 1.86536, accuracy = 0.421875
    epoch 5, step 3900, loss = 1.84846, accuracy = 0.4375
    epoch 5, step 3910, loss = 1.93737, accuracy = 0.359375
    epoch 5, step 3920, loss = 1.76376, accuracy = 0.46875
    epoch 5, step 3930, loss = 1.60957, accuracy = 0.453125
    epoch 5, step 3940, loss = 1.62213, accuracy = 0.484375
    epoch 5, step 3950, loss = 1.85709, accuracy = 0.453125
    epoch 5, step 3960, loss = 1.81319, accuracy = 0.40625
    epoch 5, step 3970, loss = 1.82335, accuracy = 0.484375
    epoch 5, step 3980, loss = 1.82790, accuracy = 0.390625
    epoch 5, step 3990, loss = 1.62210, accuracy = 0.484375
    epoch 5, step 4000, loss = 1.73792, accuracy = 0.453125
    epoch 5, step 4010, loss = 1.98734, accuracy = 0.234375
    epoch 5, step 4020, loss = 1.66384, accuracy = 0.453125
    epoch 5, step 4030, loss = 1.91248, accuracy = 0.40625
    epoch 5, step 4040, loss = 1.75072, accuracy = 0.5
    epoch 5, step 4050, loss = 2.00374, accuracy = 0.390625
    epoch 5, step 4060, loss = 1.69269, accuracy = 0.453125
    epoch 5, step 4070, loss = 1.63403, accuracy = 0.46875
    epoch 5, step 4080, loss = 1.70423, accuracy = 0.4375
    epoch 5, step 4090, loss = 1.72676, accuracy = 0.421875
    epoch 5, step 4100, loss = 1.73378, accuracy = 0.359375
    epoch 5, step 4110, loss = 1.96765, accuracy = 0.359375
    epoch 5, step 4120, loss = 1.69225, accuracy = 0.453125
    epoch 5, step 4130, loss = 1.65609, accuracy = 0.484375
    epoch 5, step 4140, loss = 1.99754, accuracy = 0.296875
    epoch 5, step 4150, loss = 1.69521, accuracy = 0.453125
    epoch 5, step 4160, loss = 1.73992, accuracy = 0.40625
    epoch 5, step 4170, loss = 1.85764, accuracy = 0.40625
    epoch 5, step 4180, loss = 1.38180, accuracy = 0.546875
    epoch 5, step 4190, loss = 1.77257, accuracy = 0.421875
    epoch 5, step 4200, loss = 1.83342, accuracy = 0.375
    epoch 5, step 4210, loss = 1.63647, accuracy = 0.4375
    validation after epoch 5: loss = 1.67659, accuracy = 0.419
    Decreased learning rate by 0.5
    epoch 6, step 4220, loss = 1.67546, accuracy = 0.4375
    epoch 6, step 4230, loss = 1.84264, accuracy = 0.375
    epoch 6, step 4240, loss = 1.80065, accuracy = 0.453125
    epoch 6, step 4250, loss = 1.72895, accuracy = 0.46875
    epoch 6, step 4260, loss = 1.68779, accuracy = 0.484375
    epoch 6, step 4270, loss = 1.84360, accuracy = 0.328125
    epoch 6, step 4280, loss = 1.87857, accuracy = 0.40625
    epoch 6, step 4290, loss = 1.55913, accuracy = 0.578125
    epoch 6, step 4300, loss = 2.21926, accuracy = 0.359375
    epoch 6, step 4310, loss = 1.47279, accuracy = 0.53125
    epoch 6, step 4320, loss = 1.54147, accuracy = 0.453125
    epoch 6, step 4330, loss = 1.68731, accuracy = 0.453125
    epoch 6, step 4340, loss = 1.58893, accuracy = 0.453125
    epoch 6, step 4350, loss = 1.86284, accuracy = 0.390625
    epoch 6, step 4360, loss = 1.70109, accuracy = 0.5
    epoch 6, step 4370, loss = 1.64106, accuracy = 0.5
    epoch 6, step 4380, loss = 1.59589, accuracy = 0.5
    epoch 6, step 4390, loss = 1.61053, accuracy = 0.546875
    epoch 6, step 4400, loss = 1.69838, accuracy = 0.4375
    epoch 6, step 4410, loss = 2.09653, accuracy = 0.34375
    epoch 6, step 4420, loss = 1.88015, accuracy = 0.390625
    epoch 6, step 4430, loss = 1.57707, accuracy = 0.53125
    epoch 6, step 4440, loss = 1.58450, accuracy = 0.484375
    epoch 6, step 4450, loss = 1.62059, accuracy = 0.484375
    epoch 6, step 4460, loss = 1.68882, accuracy = 0.5
    epoch 6, step 4470, loss = 1.67644, accuracy = 0.546875
    epoch 6, step 4480, loss = 1.65916, accuracy = 0.46875
    epoch 6, step 4490, loss = 1.91386, accuracy = 0.359375
    epoch 6, step 4500, loss = 1.77332, accuracy = 0.421875
    epoch 6, step 4510, loss = 1.63059, accuracy = 0.46875
    epoch 6, step 4520, loss = 1.59866, accuracy = 0.375
    epoch 6, step 4530, loss = 1.51650, accuracy = 0.578125
    epoch 6, step 4540, loss = 1.55399, accuracy = 0.5
    epoch 6, step 4550, loss = 1.79354, accuracy = 0.390625
    epoch 6, step 4560, loss = 1.71817, accuracy = 0.5
    epoch 6, step 4570, loss = 1.63931, accuracy = 0.5
    epoch 6, step 4580, loss = 1.68255, accuracy = 0.4375
    epoch 6, step 4590, loss = 1.77468, accuracy = 0.421875
    epoch 6, step 4600, loss = 1.73708, accuracy = 0.328125
    epoch 6, step 4610, loss = 1.76074, accuracy = 0.4375
    epoch 6, step 4620, loss = 1.98785, accuracy = 0.34375
    epoch 6, step 4630, loss = 1.72613, accuracy = 0.453125
    epoch 6, step 4640, loss = 1.45827, accuracy = 0.546875
    epoch 6, step 4650, loss = 1.96511, accuracy = 0.375
    epoch 6, step 4660, loss = 1.45005, accuracy = 0.515625
    epoch 6, step 4670, loss = 2.01409, accuracy = 0.40625
    epoch 6, step 4680, loss = 1.67531, accuracy = 0.390625
    epoch 6, step 4690, loss = 1.85915, accuracy = 0.375
    epoch 6, step 4700, loss = 1.59150, accuracy = 0.515625
    epoch 6, step 4710, loss = 1.72841, accuracy = 0.375
    epoch 6, step 4720, loss = 1.69635, accuracy = 0.484375
    epoch 6, step 4730, loss = 1.62143, accuracy = 0.515625
    epoch 6, step 4740, loss = 1.69679, accuracy = 0.40625
    epoch 6, step 4750, loss = 1.48620, accuracy = 0.515625
    epoch 6, step 4760, loss = 1.64092, accuracy = 0.453125
    epoch 6, step 4770, loss = 1.66473, accuracy = 0.484375
    epoch 6, step 4780, loss = 1.66149, accuracy = 0.5
    epoch 6, step 4790, loss = 1.78140, accuracy = 0.46875
    epoch 6, step 4800, loss = 1.73847, accuracy = 0.40625
    epoch 6, step 4810, loss = 1.68822, accuracy = 0.421875
    epoch 6, step 4820, loss = 1.82711, accuracy = 0.421875
    epoch 6, step 4830, loss = 1.77389, accuracy = 0.40625
    epoch 6, step 4840, loss = 1.81633, accuracy = 0.359375
    epoch 6, step 4850, loss = 1.57524, accuracy = 0.515625
    epoch 6, step 4860, loss = 1.62276, accuracy = 0.53125
    epoch 6, step 4870, loss = 1.89080, accuracy = 0.421875
    epoch 6, step 4880, loss = 1.55556, accuracy = 0.5
    epoch 6, step 4890, loss = 1.66051, accuracy = 0.46875
    epoch 6, step 4900, loss = 1.65880, accuracy = 0.390625
    epoch 6, step 4910, loss = 1.78865, accuracy = 0.4375
    epoch 6, step 4920, loss = 1.74904, accuracy = 0.375
    validation after epoch 6: loss = 1.57609, accuracy = 0.454
    epoch 7, step 4930, loss = 1.46898, accuracy = 0.53125
    epoch 7, step 4940, loss = 1.75918, accuracy = 0.40625
    epoch 7, step 4950, loss = 1.74215, accuracy = 0.421875
    epoch 7, step 4960, loss = 1.79742, accuracy = 0.375
    epoch 7, step 4970, loss = 1.58180, accuracy = 0.390625
    epoch 7, step 4980, loss = 1.54831, accuracy = 0.5
    epoch 7, step 4990, loss = 1.74447, accuracy = 0.4375
    epoch 7, step 5000, loss = 1.71139, accuracy = 0.484375
    epoch 7, step 5010, loss = 1.46940, accuracy = 0.578125
    epoch 7, step 5020, loss = 1.65831, accuracy = 0.421875
    epoch 7, step 5030, loss = 1.53634, accuracy = 0.515625
    epoch 7, step 5040, loss = 1.53905, accuracy = 0.53125
    epoch 7, step 5050, loss = 1.61497, accuracy = 0.53125
    epoch 7, step 5060, loss = 1.71388, accuracy = 0.46875
    epoch 7, step 5070, loss = 1.77261, accuracy = 0.40625
    epoch 7, step 5080, loss = 1.83831, accuracy = 0.359375
    epoch 7, step 5090, loss = 1.62143, accuracy = 0.421875
    epoch 7, step 5100, loss = 1.80685, accuracy = 0.359375
    epoch 7, step 5110, loss = 1.60964, accuracy = 0.46875
    epoch 7, step 5120, loss = 1.39836, accuracy = 0.578125
    epoch 7, step 5130, loss = 1.51417, accuracy = 0.53125
    epoch 7, step 5140, loss = 1.67271, accuracy = 0.46875
    epoch 7, step 5150, loss = 1.61739, accuracy = 0.46875
    epoch 7, step 5160, loss = 1.47928, accuracy = 0.578125
    epoch 7, step 5170, loss = 1.76156, accuracy = 0.375
    epoch 7, step 5180, loss = 1.63491, accuracy = 0.46875
    epoch 7, step 5190, loss = 1.66269, accuracy = 0.453125
    epoch 7, step 5200, loss = 1.55790, accuracy = 0.4375
    epoch 7, step 5210, loss = 1.66205, accuracy = 0.515625
    epoch 7, step 5220, loss = 1.58680, accuracy = 0.5
    epoch 7, step 5230, loss = 2.01368, accuracy = 0.34375
    epoch 7, step 5240, loss = 1.63214, accuracy = 0.453125
    epoch 7, step 5250, loss = 1.76995, accuracy = 0.390625
    epoch 7, step 5260, loss = 1.44020, accuracy = 0.5
    epoch 7, step 5270, loss = 1.57432, accuracy = 0.546875
    epoch 7, step 5280, loss = 1.56338, accuracy = 0.484375
    epoch 7, step 5290, loss = 1.71679, accuracy = 0.421875
    epoch 7, step 5300, loss = 1.89464, accuracy = 0.40625
    epoch 7, step 5310, loss = 1.41696, accuracy = 0.640625
    epoch 7, step 5320, loss = 1.88559, accuracy = 0.421875
    epoch 7, step 5330, loss = 1.63441, accuracy = 0.421875
    epoch 7, step 5340, loss = 1.67898, accuracy = 0.375
    epoch 7, step 5350, loss = 1.73967, accuracy = 0.40625
    epoch 7, step 5360, loss = 1.45683, accuracy = 0.53125
    epoch 7, step 5370, loss = 1.64841, accuracy = 0.5
    epoch 7, step 5380, loss = 1.83037, accuracy = 0.5
    epoch 7, step 5390, loss = 1.77130, accuracy = 0.484375
    epoch 7, step 5400, loss = 1.71990, accuracy = 0.40625
    epoch 7, step 5410, loss = 1.88024, accuracy = 0.375
    epoch 7, step 5420, loss = 1.72668, accuracy = 0.515625
    epoch 7, step 5430, loss = 1.64029, accuracy = 0.46875
    epoch 7, step 5440, loss = 1.68670, accuracy = 0.46875
    epoch 7, step 5450, loss = 1.63512, accuracy = 0.46875
    epoch 7, step 5460, loss = 1.62962, accuracy = 0.5
    epoch 7, step 5470, loss = 1.36753, accuracy = 0.53125
    epoch 7, step 5480, loss = 1.58000, accuracy = 0.5625
    epoch 7, step 5490, loss = 1.85101, accuracy = 0.375
    epoch 7, step 5500, loss = 1.58378, accuracy = 0.5
    epoch 7, step 5510, loss = 1.67447, accuracy = 0.421875
    epoch 7, step 5520, loss = 1.64871, accuracy = 0.484375
    epoch 7, step 5530, loss = 1.66588, accuracy = 0.515625
    epoch 7, step 5540, loss = 1.52102, accuracy = 0.515625
    epoch 7, step 5550, loss = 1.56815, accuracy = 0.546875
    epoch 7, step 5560, loss = 1.93795, accuracy = 0.375
    epoch 7, step 5570, loss = 1.67663, accuracy = 0.5
    epoch 7, step 5580, loss = 1.52902, accuracy = 0.53125
    epoch 7, step 5590, loss = 1.63149, accuracy = 0.421875
    epoch 7, step 5600, loss = 1.63453, accuracy = 0.46875
    epoch 7, step 5610, loss = 1.73756, accuracy = 0.421875
    epoch 7, step 5620, loss = 1.61800, accuracy = 0.5
    validation after epoch 7: loss = 1.57548, accuracy = 0.45
    epoch 8, step 5630, loss = 1.65614, accuracy = 0.484375
    epoch 8, step 5640, loss = 1.89506, accuracy = 0.4375
    epoch 8, step 5650, loss = 1.49471, accuracy = 0.546875
    epoch 8, step 5660, loss = 1.58766, accuracy = 0.53125
    epoch 8, step 5670, loss = 1.46547, accuracy = 0.546875
    epoch 8, step 5680, loss = 1.55535, accuracy = 0.546875
    epoch 8, step 5690, loss = 1.72119, accuracy = 0.40625
    epoch 8, step 5700, loss = 1.50774, accuracy = 0.578125
    epoch 8, step 5710, loss = 1.62763, accuracy = 0.484375
    epoch 8, step 5720, loss = 1.73245, accuracy = 0.53125
    epoch 8, step 5730, loss = 1.51943, accuracy = 0.515625
    epoch 8, step 5740, loss = 1.75219, accuracy = 0.421875
    epoch 8, step 5750, loss = 1.66005, accuracy = 0.5
    epoch 8, step 5760, loss = 1.66915, accuracy = 0.390625
    epoch 8, step 5770, loss = 1.47059, accuracy = 0.515625
    epoch 8, step 5780, loss = 1.52880, accuracy = 0.5625
    epoch 8, step 5790, loss = 1.59907, accuracy = 0.515625
    epoch 8, step 5800, loss = 1.30756, accuracy = 0.609375
    epoch 8, step 5810, loss = 1.64976, accuracy = 0.453125
    epoch 8, step 5820, loss = 1.28971, accuracy = 0.671875
    epoch 8, step 5830, loss = 1.56809, accuracy = 0.46875
    epoch 8, step 5840, loss = 1.76541, accuracy = 0.421875
    epoch 8, step 5850, loss = 1.43024, accuracy = 0.59375
    epoch 8, step 5860, loss = 1.64076, accuracy = 0.484375
    epoch 8, step 5870, loss = 1.72169, accuracy = 0.40625
    epoch 8, step 5880, loss = 1.69187, accuracy = 0.453125
    epoch 8, step 5890, loss = 1.76807, accuracy = 0.453125
    epoch 8, step 5900, loss = 1.72385, accuracy = 0.46875
    epoch 8, step 5910, loss = 1.73891, accuracy = 0.46875
    epoch 8, step 5920, loss = 1.69204, accuracy = 0.40625
    epoch 8, step 5930, loss = 1.71796, accuracy = 0.40625
    epoch 8, step 5940, loss = 1.63083, accuracy = 0.484375
    epoch 8, step 5950, loss = 1.46546, accuracy = 0.515625
    epoch 8, step 5960, loss = 1.66999, accuracy = 0.421875
    epoch 8, step 5970, loss = 1.71921, accuracy = 0.40625
    epoch 8, step 5980, loss = 1.60021, accuracy = 0.484375
    epoch 8, step 5990, loss = 1.63827, accuracy = 0.484375
    epoch 8, step 6000, loss = 1.86291, accuracy = 0.40625
    epoch 8, step 6010, loss = 1.46735, accuracy = 0.484375
    epoch 8, step 6020, loss = 1.64754, accuracy = 0.515625
    epoch 8, step 6030, loss = 1.84991, accuracy = 0.40625
    epoch 8, step 6040, loss = 1.66582, accuracy = 0.34375
    epoch 8, step 6050, loss = 1.69236, accuracy = 0.46875
    epoch 8, step 6060, loss = 1.76636, accuracy = 0.453125
    epoch 8, step 6070, loss = 1.65926, accuracy = 0.4375
    epoch 8, step 6080, loss = 1.58230, accuracy = 0.53125
    epoch 8, step 6090, loss = 1.72055, accuracy = 0.515625
    epoch 8, step 6100, loss = 1.41238, accuracy = 0.59375
    epoch 8, step 6110, loss = 1.31993, accuracy = 0.625
    epoch 8, step 6120, loss = 1.44714, accuracy = 0.609375
    epoch 8, step 6130, loss = 1.73961, accuracy = 0.421875
    epoch 8, step 6140, loss = 1.71877, accuracy = 0.4375
    epoch 8, step 6150, loss = 1.53834, accuracy = 0.515625
    epoch 8, step 6160, loss = 1.50229, accuracy = 0.5
    epoch 8, step 6170, loss = 1.72106, accuracy = 0.4375
    epoch 8, step 6180, loss = 1.78711, accuracy = 0.46875
    epoch 8, step 6190, loss = 1.81118, accuracy = 0.375
    epoch 8, step 6200, loss = 1.66293, accuracy = 0.40625
    epoch 8, step 6210, loss = 1.65620, accuracy = 0.4375
    epoch 8, step 6220, loss = 1.90909, accuracy = 0.375
    epoch 8, step 6230, loss = 1.66617, accuracy = 0.453125
    epoch 8, step 6240, loss = 1.55989, accuracy = 0.59375
    epoch 8, step 6250, loss = 1.65289, accuracy = 0.46875
    epoch 8, step 6260, loss = 1.56475, accuracy = 0.515625
    epoch 8, step 6270, loss = 1.80111, accuracy = 0.375
    epoch 8, step 6280, loss = 1.61662, accuracy = 0.46875
    epoch 8, step 6290, loss = 1.72120, accuracy = 0.40625
    epoch 8, step 6300, loss = 1.50044, accuracy = 0.546875
    epoch 8, step 6310, loss = 1.72716, accuracy = 0.484375
    epoch 8, step 6320, loss = 1.63318, accuracy = 0.453125
    validation after epoch 8: loss = 1.53969, accuracy = 0.4574
    Decreased learning rate by 0.5
    epoch 9, step 6330, loss = 1.44533, accuracy = 0.515625
    epoch 9, step 6340, loss = 1.46476, accuracy = 0.53125
    epoch 9, step 6350, loss = 1.40870, accuracy = 0.53125
    epoch 9, step 6360, loss = 1.53336, accuracy = 0.515625
    epoch 9, step 6370, loss = 1.65185, accuracy = 0.5
    epoch 9, step 6380, loss = 1.57134, accuracy = 0.46875
    epoch 9, step 6390, loss = 1.62564, accuracy = 0.5625
    epoch 9, step 6400, loss = 1.48410, accuracy = 0.484375
    epoch 9, step 6410, loss = 1.75012, accuracy = 0.328125
    epoch 9, step 6420, loss = 1.46164, accuracy = 0.53125
    epoch 9, step 6430, loss = 1.49980, accuracy = 0.5625
    epoch 9, step 6440, loss = 1.53708, accuracy = 0.5
    epoch 9, step 6450, loss = 1.62499, accuracy = 0.484375
    epoch 9, step 6460, loss = 1.36358, accuracy = 0.609375
    epoch 9, step 6470, loss = 1.53114, accuracy = 0.515625
    epoch 9, step 6480, loss = 1.56853, accuracy = 0.453125
    epoch 9, step 6490, loss = 1.39914, accuracy = 0.515625
    epoch 9, step 6500, loss = 1.47066, accuracy = 0.5625
    epoch 9, step 6510, loss = 1.61451, accuracy = 0.4375
    epoch 9, step 6520, loss = 1.44569, accuracy = 0.53125
    epoch 9, step 6530, loss = 1.59813, accuracy = 0.484375
    epoch 9, step 6540, loss = 1.73899, accuracy = 0.421875
    epoch 9, step 6550, loss = 1.42460, accuracy = 0.609375
    epoch 9, step 6560, loss = 1.29627, accuracy = 0.625
    epoch 9, step 6570, loss = 1.77583, accuracy = 0.40625
    epoch 9, step 6580, loss = 1.57973, accuracy = 0.4375
    epoch 9, step 6590, loss = 1.36672, accuracy = 0.578125
    epoch 9, step 6600, loss = 1.46092, accuracy = 0.578125
    epoch 9, step 6610, loss = 1.53212, accuracy = 0.578125
    epoch 9, step 6620, loss = 1.48919, accuracy = 0.515625
    epoch 9, step 6630, loss = 1.72523, accuracy = 0.4375
    epoch 9, step 6640, loss = 1.56630, accuracy = 0.46875
    epoch 9, step 6650, loss = 1.46351, accuracy = 0.5
    epoch 9, step 6660, loss = 1.68266, accuracy = 0.46875
    epoch 9, step 6670, loss = 1.37389, accuracy = 0.59375
    epoch 9, step 6680, loss = 1.56199, accuracy = 0.4375
    epoch 9, step 6690, loss = 1.36258, accuracy = 0.65625
    epoch 9, step 6700, loss = 1.45728, accuracy = 0.546875
    epoch 9, step 6710, loss = 1.46857, accuracy = 0.5
    epoch 9, step 6720, loss = 1.52194, accuracy = 0.5
    epoch 9, step 6730, loss = 1.32522, accuracy = 0.59375
    epoch 9, step 6740, loss = 1.35740, accuracy = 0.546875
    epoch 9, step 6750, loss = 1.56343, accuracy = 0.546875
    epoch 9, step 6760, loss = 1.38453, accuracy = 0.515625
    epoch 9, step 6770, loss = 1.58688, accuracy = 0.515625
    epoch 9, step 6780, loss = 1.66590, accuracy = 0.453125
    epoch 9, step 6790, loss = 1.53234, accuracy = 0.5
    epoch 9, step 6800, loss = 1.63211, accuracy = 0.4375
    epoch 9, step 6810, loss = 1.37791, accuracy = 0.5625
    epoch 9, step 6820, loss = 1.61447, accuracy = 0.421875
    epoch 9, step 6830, loss = 1.52339, accuracy = 0.4375
    epoch 9, step 6840, loss = 1.49643, accuracy = 0.515625
    epoch 9, step 6850, loss = 1.44679, accuracy = 0.484375
    epoch 9, step 6860, loss = 1.48626, accuracy = 0.546875
    epoch 9, step 6870, loss = 1.64241, accuracy = 0.46875
    epoch 9, step 6880, loss = 1.17685, accuracy = 0.640625
    epoch 9, step 6890, loss = 1.36442, accuracy = 0.609375
    epoch 9, step 6900, loss = 1.56619, accuracy = 0.5
    epoch 9, step 6910, loss = 1.78519, accuracy = 0.453125
    epoch 9, step 6920, loss = 1.76688, accuracy = 0.375
    epoch 9, step 6930, loss = 1.48361, accuracy = 0.59375
    epoch 9, step 6940, loss = 1.28866, accuracy = 0.59375
    epoch 9, step 6950, loss = 1.34873, accuracy = 0.546875
    epoch 9, step 6960, loss = 1.55307, accuracy = 0.515625
    epoch 9, step 6970, loss = 1.46714, accuracy = 0.5
    epoch 9, step 6980, loss = 1.52932, accuracy = 0.59375
    epoch 9, step 6990, loss = 1.49168, accuracy = 0.546875
    epoch 9, step 7000, loss = 1.51800, accuracy = 0.46875
    epoch 9, step 7010, loss = 1.49038, accuracy = 0.5
    epoch 9, step 7020, loss = 1.56887, accuracy = 0.484375
    validation after epoch 9: loss = 1.50466, accuracy = 0.4748
    epoch 10, step 7030, loss = 1.41266, accuracy = 0.546875
    epoch 10, step 7040, loss = 1.62870, accuracy = 0.515625
    epoch 10, step 7050, loss = 1.47928, accuracy = 0.4375
    epoch 10, step 7060, loss = 1.35106, accuracy = 0.609375
    epoch 10, step 7070, loss = 1.43186, accuracy = 0.59375
    epoch 10, step 7080, loss = 1.37424, accuracy = 0.609375
    epoch 10, step 7090, loss = 1.38345, accuracy = 0.609375
    epoch 10, step 7100, loss = 1.32539, accuracy = 0.578125
    epoch 10, step 7110, loss = 1.26749, accuracy = 0.625
    epoch 10, step 7120, loss = 1.56545, accuracy = 0.40625
    epoch 10, step 7130, loss = 1.35385, accuracy = 0.625
    epoch 10, step 7140, loss = 1.48683, accuracy = 0.53125
    epoch 10, step 7150, loss = 1.61854, accuracy = 0.484375
    epoch 10, step 7160, loss = 1.54248, accuracy = 0.484375
    epoch 10, step 7170, loss = 1.45853, accuracy = 0.609375
    epoch 10, step 7180, loss = 1.35307, accuracy = 0.53125
    epoch 10, step 7190, loss = 1.31513, accuracy = 0.609375
    epoch 10, step 7200, loss = 1.22541, accuracy = 0.609375
    epoch 10, step 7210, loss = 1.61285, accuracy = 0.484375
    epoch 10, step 7220, loss = 1.56955, accuracy = 0.5625
    epoch 10, step 7230, loss = 1.45995, accuracy = 0.546875
    epoch 10, step 7240, loss = 1.52422, accuracy = 0.4375
    epoch 10, step 7250, loss = 1.50584, accuracy = 0.515625
    epoch 10, step 7260, loss = 1.53064, accuracy = 0.453125
    epoch 10, step 7270, loss = 1.42769, accuracy = 0.453125
    epoch 10, step 7280, loss = 1.81652, accuracy = 0.4375
    epoch 10, step 7290, loss = 1.47250, accuracy = 0.515625
    epoch 10, step 7300, loss = 1.55224, accuracy = 0.4375
    epoch 10, step 7310, loss = 1.64678, accuracy = 0.5
    epoch 10, step 7320, loss = 1.34198, accuracy = 0.59375
    epoch 10, step 7330, loss = 1.29066, accuracy = 0.609375
    epoch 10, step 7340, loss = 1.47162, accuracy = 0.5625
    epoch 10, step 7350, loss = 1.64410, accuracy = 0.421875
    epoch 10, step 7360, loss = 1.55136, accuracy = 0.53125
    epoch 10, step 7370, loss = 1.69946, accuracy = 0.359375
    epoch 10, step 7380, loss = 1.62915, accuracy = 0.421875
    epoch 10, step 7390, loss = 1.59434, accuracy = 0.53125
    epoch 10, step 7400, loss = 1.57563, accuracy = 0.5
    epoch 10, step 7410, loss = 1.54197, accuracy = 0.515625
    epoch 10, step 7420, loss = 1.62701, accuracy = 0.515625
    epoch 10, step 7430, loss = 1.57053, accuracy = 0.53125
    epoch 10, step 7440, loss = 1.55249, accuracy = 0.484375
    epoch 10, step 7450, loss = 1.69794, accuracy = 0.484375
    epoch 10, step 7460, loss = 1.40043, accuracy = 0.609375
    epoch 10, step 7470, loss = 1.44689, accuracy = 0.5
    epoch 10, step 7480, loss = 1.53153, accuracy = 0.46875
    epoch 10, step 7490, loss = 1.57585, accuracy = 0.5
    epoch 10, step 7500, loss = 1.72546, accuracy = 0.390625
    epoch 10, step 7510, loss = 1.70187, accuracy = 0.53125
    epoch 10, step 7520, loss = 1.56651, accuracy = 0.453125
    epoch 10, step 7530, loss = 1.66820, accuracy = 0.484375
    epoch 10, step 7540, loss = 1.56820, accuracy = 0.484375
    epoch 10, step 7550, loss = 1.68530, accuracy = 0.421875
    epoch 10, step 7560, loss = 1.61614, accuracy = 0.453125
    epoch 10, step 7570, loss = 1.78832, accuracy = 0.421875
    epoch 10, step 7580, loss = 1.58372, accuracy = 0.53125
    epoch 10, step 7590, loss = 1.52853, accuracy = 0.59375
    epoch 10, step 7600, loss = 1.24143, accuracy = 0.671875
    epoch 10, step 7610, loss = 1.51316, accuracy = 0.5
    epoch 10, step 7620, loss = 1.50045, accuracy = 0.515625
    epoch 10, step 7630, loss = 1.69627, accuracy = 0.453125
    epoch 10, step 7640, loss = 1.44714, accuracy = 0.546875
    epoch 10, step 7650, loss = 1.62154, accuracy = 0.59375
    epoch 10, step 7660, loss = 1.31844, accuracy = 0.5625
    epoch 10, step 7670, loss = 1.38663, accuracy = 0.59375
    epoch 10, step 7680, loss = 1.37149, accuracy = 0.609375
    epoch 10, step 7690, loss = 1.50972, accuracy = 0.546875
    epoch 10, step 7700, loss = 1.44273, accuracy = 0.5625
    epoch 10, step 7710, loss = 1.43958, accuracy = 0.578125
    epoch 10, step 7720, loss = 1.45176, accuracy = 0.5
    epoch 10, step 7730, loss = 1.49511, accuracy = 0.484375
    validation after epoch 10: loss = 1.49338, accuracy = 0.482
    epoch 11, step 7740, loss = 1.51175, accuracy = 0.453125
    epoch 11, step 7750, loss = 1.63649, accuracy = 0.421875
    epoch 11, step 7760, loss = 1.40988, accuracy = 0.5625
    epoch 11, step 7770, loss = 1.68691, accuracy = 0.421875
    epoch 11, step 7780, loss = 1.50752, accuracy = 0.453125
    epoch 11, step 7790, loss = 1.46385, accuracy = 0.53125
    epoch 11, step 7800, loss = 1.24454, accuracy = 0.609375
    epoch 11, step 7810, loss = 1.52294, accuracy = 0.46875
    epoch 11, step 7820, loss = 1.55852, accuracy = 0.5
    epoch 11, step 7830, loss = 1.26062, accuracy = 0.625
    epoch 11, step 7840, loss = 1.32611, accuracy = 0.515625
    epoch 11, step 7850, loss = 1.47771, accuracy = 0.53125
    epoch 11, step 7860, loss = 1.57301, accuracy = 0.5
    epoch 11, step 7870, loss = 1.65697, accuracy = 0.5
    epoch 11, step 7880, loss = 1.42749, accuracy = 0.578125
    epoch 11, step 7890, loss = 1.70308, accuracy = 0.453125
    epoch 11, step 7900, loss = 1.16523, accuracy = 0.65625
    epoch 11, step 7910, loss = 1.46005, accuracy = 0.5625
    epoch 11, step 7920, loss = 1.36594, accuracy = 0.625
    epoch 11, step 7930, loss = 1.42806, accuracy = 0.5
    epoch 11, step 7940, loss = 1.49558, accuracy = 0.515625
    epoch 11, step 7950, loss = 1.22860, accuracy = 0.625
    epoch 11, step 7960, loss = 1.60985, accuracy = 0.484375
    epoch 11, step 7970, loss = 1.51017, accuracy = 0.5625
    epoch 11, step 7980, loss = 1.42254, accuracy = 0.5625
    epoch 11, step 7990, loss = 1.36939, accuracy = 0.546875
    epoch 11, step 8000, loss = 1.56103, accuracy = 0.546875
    epoch 11, step 8010, loss = 1.44292, accuracy = 0.578125
    epoch 11, step 8020, loss = 1.50446, accuracy = 0.5625
    epoch 11, step 8030, loss = 1.29541, accuracy = 0.578125
    epoch 11, step 8040, loss = 1.42715, accuracy = 0.5625
    epoch 11, step 8050, loss = 1.36396, accuracy = 0.59375
    epoch 11, step 8060, loss = 1.34214, accuracy = 0.609375
    epoch 11, step 8070, loss = 1.76105, accuracy = 0.484375
    epoch 11, step 8080, loss = 1.52193, accuracy = 0.40625
    epoch 11, step 8090, loss = 1.52873, accuracy = 0.484375
    epoch 11, step 8100, loss = 1.17523, accuracy = 0.59375
    epoch 11, step 8110, loss = 1.27009, accuracy = 0.578125
    epoch 11, step 8120, loss = 1.37536, accuracy = 0.5
    epoch 11, step 8130, loss = 1.33050, accuracy = 0.59375
    epoch 11, step 8140, loss = 1.66552, accuracy = 0.40625
    epoch 11, step 8150, loss = 1.51553, accuracy = 0.5625
    epoch 11, step 8160, loss = 1.47753, accuracy = 0.578125
    epoch 11, step 8170, loss = 1.64759, accuracy = 0.46875
    epoch 11, step 8180, loss = 1.31076, accuracy = 0.546875
    epoch 11, step 8190, loss = 1.35157, accuracy = 0.5625
    epoch 11, step 8200, loss = 1.64267, accuracy = 0.390625
    epoch 11, step 8210, loss = 1.41226, accuracy = 0.5625
    epoch 11, step 8220, loss = 1.62921, accuracy = 0.421875
    epoch 11, step 8230, loss = 1.65885, accuracy = 0.46875
    epoch 11, step 8240, loss = 1.48337, accuracy = 0.578125
    epoch 11, step 8250, loss = 1.58219, accuracy = 0.4375
    epoch 11, step 8260, loss = 1.36503, accuracy = 0.640625
    epoch 11, step 8270, loss = 1.27401, accuracy = 0.515625
    epoch 11, step 8280, loss = 1.68530, accuracy = 0.4375
    epoch 11, step 8290, loss = 1.57542, accuracy = 0.578125
    epoch 11, step 8300, loss = 1.46755, accuracy = 0.546875
    epoch 11, step 8310, loss = 1.49401, accuracy = 0.484375
    epoch 11, step 8320, loss = 1.28660, accuracy = 0.609375
    epoch 11, step 8330, loss = 1.41690, accuracy = 0.640625
    epoch 11, step 8340, loss = 1.38281, accuracy = 0.5625
    epoch 11, step 8350, loss = 1.45398, accuracy = 0.515625
    epoch 11, step 8360, loss = 1.37359, accuracy = 0.578125
    epoch 11, step 8370, loss = 1.55383, accuracy = 0.5
    epoch 11, step 8380, loss = 1.31416, accuracy = 0.578125
    epoch 11, step 8390, loss = 1.44803, accuracy = 0.5625
    epoch 11, step 8400, loss = 1.68598, accuracy = 0.4375
    epoch 11, step 8410, loss = 1.57764, accuracy = 0.4375
    epoch 11, step 8420, loss = 1.41172, accuracy = 0.46875
    epoch 11, step 8430, loss = 1.36810, accuracy = 0.546875
    validation after epoch 11: loss = 1.48063, accuracy = 0.4904
    Decreased learning rate by 0.5
    epoch 12, step 8440, loss = 1.50163, accuracy = 0.515625
    epoch 12, step 8450, loss = 1.40321, accuracy = 0.578125
    epoch 12, step 8460, loss = 1.34266, accuracy = 0.671875
    epoch 12, step 8470, loss = 1.43463, accuracy = 0.53125
    epoch 12, step 8480, loss = 1.42550, accuracy = 0.578125
    epoch 12, step 8490, loss = 1.41482, accuracy = 0.546875
    epoch 12, step 8500, loss = 1.30380, accuracy = 0.59375
    epoch 12, step 8510, loss = 1.22488, accuracy = 0.625
    epoch 12, step 8520, loss = 1.21062, accuracy = 0.59375
    epoch 12, step 8530, loss = 1.23642, accuracy = 0.59375
    epoch 12, step 8540, loss = 1.38289, accuracy = 0.53125
    epoch 12, step 8550, loss = 1.29843, accuracy = 0.53125
    epoch 12, step 8560, loss = 1.23235, accuracy = 0.640625
    epoch 12, step 8570, loss = 1.51946, accuracy = 0.5
    epoch 12, step 8580, loss = 1.32518, accuracy = 0.53125
    epoch 12, step 8590, loss = 1.31404, accuracy = 0.625
    epoch 12, step 8600, loss = 1.29171, accuracy = 0.578125
    epoch 12, step 8610, loss = 1.55236, accuracy = 0.5
    epoch 12, step 8620, loss = 1.44486, accuracy = 0.5625
    epoch 12, step 8630, loss = 1.11656, accuracy = 0.65625
    epoch 12, step 8640, loss = 1.50712, accuracy = 0.5
    epoch 12, step 8650, loss = 1.54460, accuracy = 0.46875
    epoch 12, step 8660, loss = 1.17171, accuracy = 0.625
    epoch 12, step 8670, loss = 1.38304, accuracy = 0.5625
    epoch 12, step 8680, loss = 1.32902, accuracy = 0.65625
    epoch 12, step 8690, loss = 1.42079, accuracy = 0.59375
    epoch 12, step 8700, loss = 1.47369, accuracy = 0.59375
    epoch 12, step 8710, loss = 1.40775, accuracy = 0.515625
    epoch 12, step 8720, loss = 1.62768, accuracy = 0.390625
    epoch 12, step 8730, loss = 1.43831, accuracy = 0.5625
    epoch 12, step 8740, loss = 1.43170, accuracy = 0.53125
    epoch 12, step 8750, loss = 1.21608, accuracy = 0.59375
    epoch 12, step 8760, loss = 1.52150, accuracy = 0.515625
    epoch 12, step 8770, loss = 1.55120, accuracy = 0.546875
    epoch 12, step 8780, loss = 1.47475, accuracy = 0.484375
    epoch 12, step 8790, loss = 1.16050, accuracy = 0.6875
    epoch 12, step 8800, loss = 1.43209, accuracy = 0.609375
    epoch 12, step 8810, loss = 1.22514, accuracy = 0.625
    epoch 12, step 8820, loss = 1.30286, accuracy = 0.671875
    epoch 12, step 8830, loss = 1.42814, accuracy = 0.609375
    epoch 12, step 8840, loss = 1.53979, accuracy = 0.578125
    epoch 12, step 8850, loss = 1.50535, accuracy = 0.5
    epoch 12, step 8860, loss = 1.26085, accuracy = 0.578125
    epoch 12, step 8870, loss = 1.03543, accuracy = 0.625
    epoch 12, step 8880, loss = 1.10094, accuracy = 0.640625
    epoch 12, step 8890, loss = 1.12421, accuracy = 0.640625
    epoch 12, step 8900, loss = 1.49539, accuracy = 0.546875
    epoch 12, step 8910, loss = 1.38333, accuracy = 0.53125
    epoch 12, step 8920, loss = 1.57583, accuracy = 0.484375
    epoch 12, step 8930, loss = 1.45517, accuracy = 0.578125
    epoch 12, step 8940, loss = 1.39861, accuracy = 0.5625
    epoch 12, step 8950, loss = 1.39603, accuracy = 0.515625
    epoch 12, step 8960, loss = 1.46310, accuracy = 0.515625
    epoch 12, step 8970, loss = 1.45977, accuracy = 0.515625
    epoch 12, step 8980, loss = 1.31973, accuracy = 0.5625
    epoch 12, step 8990, loss = 1.46589, accuracy = 0.609375
    epoch 12, step 9000, loss = 1.50182, accuracy = 0.515625
    epoch 12, step 9010, loss = 1.23867, accuracy = 0.59375
    epoch 12, step 9020, loss = 1.36654, accuracy = 0.609375
    epoch 12, step 9030, loss = 1.50008, accuracy = 0.5
    epoch 12, step 9040, loss = 1.28311, accuracy = 0.5625
    epoch 12, step 9050, loss = 1.45955, accuracy = 0.546875
    epoch 12, step 9060, loss = 1.46023, accuracy = 0.578125
    epoch 12, step 9070, loss = 1.54375, accuracy = 0.484375
    epoch 12, step 9080, loss = 1.41130, accuracy = 0.53125
    epoch 12, step 9090, loss = 1.47963, accuracy = 0.53125
    epoch 12, step 9100, loss = 1.32602, accuracy = 0.59375
    epoch 12, step 9110, loss = 1.46130, accuracy = 0.546875
    epoch 12, step 9120, loss = 1.14503, accuracy = 0.640625
    epoch 12, step 9130, loss = 1.27044, accuracy = 0.609375
    validation after epoch 12: loss = 1.46008, accuracy = 0.4926
    epoch 13, step 9140, loss = 1.15619, accuracy = 0.625
    epoch 13, step 9150, loss = 1.32603, accuracy = 0.53125
    epoch 13, step 9160, loss = 1.22494, accuracy = 0.640625
    epoch 13, step 9170, loss = 1.25879, accuracy = 0.578125
    epoch 13, step 9180, loss = 1.31485, accuracy = 0.546875
    epoch 13, step 9190, loss = 1.04648, accuracy = 0.671875
    epoch 13, step 9200, loss = 1.30924, accuracy = 0.546875
    epoch 13, step 9210, loss = 1.31824, accuracy = 0.625
    epoch 13, step 9220, loss = 1.38488, accuracy = 0.578125
    epoch 13, step 9230, loss = 1.28446, accuracy = 0.53125
    epoch 13, step 9240, loss = 1.18417, accuracy = 0.671875
    epoch 13, step 9250, loss = 1.35538, accuracy = 0.59375
    epoch 13, step 9260, loss = 1.18901, accuracy = 0.625
    epoch 13, step 9270, loss = 0.98846, accuracy = 0.765625
    epoch 13, step 9280, loss = 1.41092, accuracy = 0.546875
    epoch 13, step 9290, loss = 1.34544, accuracy = 0.5625
    epoch 13, step 9300, loss = 1.33364, accuracy = 0.578125
    epoch 13, step 9310, loss = 1.13680, accuracy = 0.625
    epoch 13, step 9320, loss = 1.60211, accuracy = 0.484375
    epoch 13, step 9330, loss = 1.28679, accuracy = 0.546875
    epoch 13, step 9340, loss = 1.46548, accuracy = 0.546875
    epoch 13, step 9350, loss = 1.30958, accuracy = 0.609375
    epoch 13, step 9360, loss = 1.24970, accuracy = 0.640625
    epoch 13, step 9370, loss = 1.31790, accuracy = 0.5625
    epoch 13, step 9380, loss = 1.18627, accuracy = 0.6875
    epoch 13, step 9390, loss = 1.34295, accuracy = 0.53125
    epoch 13, step 9400, loss = 1.48743, accuracy = 0.5625
    epoch 13, step 9410, loss = 1.11241, accuracy = 0.6875
    epoch 13, step 9420, loss = 1.28123, accuracy = 0.5625
    epoch 13, step 9430, loss = 1.28190, accuracy = 0.59375
    epoch 13, step 9440, loss = 1.34012, accuracy = 0.578125
    epoch 13, step 9450, loss = 1.32657, accuracy = 0.609375
    epoch 13, step 9460, loss = 1.55296, accuracy = 0.484375
    epoch 13, step 9470, loss = 1.37111, accuracy = 0.5625
    epoch 13, step 9480, loss = 1.33122, accuracy = 0.546875
    epoch 13, step 9490, loss = 1.19976, accuracy = 0.640625
    epoch 13, step 9500, loss = 1.18520, accuracy = 0.65625
    epoch 13, step 9510, loss = 1.28148, accuracy = 0.515625
    epoch 13, step 9520, loss = 1.27123, accuracy = 0.515625
    epoch 13, step 9530, loss = 1.10218, accuracy = 0.671875
    epoch 13, step 9540, loss = 1.32370, accuracy = 0.640625
    epoch 13, step 9550, loss = 1.35783, accuracy = 0.5625
    epoch 13, step 9560, loss = 1.24396, accuracy = 0.6875
    epoch 13, step 9570, loss = 1.20135, accuracy = 0.59375
    epoch 13, step 9580, loss = 1.36869, accuracy = 0.5
    epoch 13, step 9590, loss = 1.32144, accuracy = 0.5
    epoch 13, step 9600, loss = 1.20786, accuracy = 0.625
    epoch 13, step 9610, loss = 1.31961, accuracy = 0.5625
    epoch 13, step 9620, loss = 1.31015, accuracy = 0.546875
    epoch 13, step 9630, loss = 1.51078, accuracy = 0.515625
    epoch 13, step 9640, loss = 1.42382, accuracy = 0.5625
    epoch 13, step 9650, loss = 1.30530, accuracy = 0.625
    epoch 13, step 9660, loss = 1.23979, accuracy = 0.59375
    epoch 13, step 9670, loss = 1.26845, accuracy = 0.546875
    epoch 13, step 9680, loss = 1.42774, accuracy = 0.53125
    epoch 13, step 9690, loss = 1.33761, accuracy = 0.546875
    epoch 13, step 9700, loss = 1.04994, accuracy = 0.671875
    epoch 13, step 9710, loss = 1.20314, accuracy = 0.609375
    epoch 13, step 9720, loss = 1.40267, accuracy = 0.5625
    epoch 13, step 9730, loss = 1.23309, accuracy = 0.640625
    epoch 13, step 9740, loss = 1.16884, accuracy = 0.625
    epoch 13, step 9750, loss = 1.25712, accuracy = 0.578125
    epoch 13, step 9760, loss = 1.43538, accuracy = 0.546875
    epoch 13, step 9770, loss = 1.66892, accuracy = 0.515625
    epoch 13, step 9780, loss = 1.32612, accuracy = 0.546875
    epoch 13, step 9790, loss = 1.13268, accuracy = 0.734375
    epoch 13, step 9800, loss = 1.18258, accuracy = 0.640625
    epoch 13, step 9810, loss = 1.22206, accuracy = 0.625
    epoch 13, step 9820, loss = 1.27510, accuracy = 0.5625
    epoch 13, step 9830, loss = 1.29508, accuracy = 0.59375
    epoch 13, step 9840, loss = 1.09593, accuracy = 0.640625
    validation after epoch 13: loss = 1.46158, accuracy = 0.4908
    epoch 14, step 9850, loss = 1.15936, accuracy = 0.65625
    epoch 14, step 9860, loss = 1.39946, accuracy = 0.5625
    epoch 14, step 9870, loss = 1.38108, accuracy = 0.578125
    epoch 14, step 9880, loss = 1.13866, accuracy = 0.625
    epoch 14, step 9890, loss = 1.25509, accuracy = 0.5625
    epoch 14, step 9900, loss = 1.18668, accuracy = 0.65625
    epoch 14, step 9910, loss = 1.10190, accuracy = 0.734375
    epoch 14, step 9920, loss = 1.19335, accuracy = 0.671875
    epoch 14, step 9930, loss = 1.34285, accuracy = 0.625
    epoch 14, step 9940, loss = 1.38789, accuracy = 0.5625
    epoch 14, step 9950, loss = 1.36875, accuracy = 0.53125
    epoch 14, step 9960, loss = 1.20765, accuracy = 0.65625
    epoch 14, step 9970, loss = 1.62297, accuracy = 0.5
    epoch 14, step 9980, loss = 1.25679, accuracy = 0.609375
    epoch 14, step 9990, loss = 1.05481, accuracy = 0.75
    epoch 14, step 10000, loss = 1.27442, accuracy = 0.578125
    epoch 14, step 10010, loss = 1.25227, accuracy = 0.59375
    epoch 14, step 10020, loss = 1.39421, accuracy = 0.546875
    epoch 14, step 10030, loss = 1.58339, accuracy = 0.515625
    epoch 14, step 10040, loss = 1.20159, accuracy = 0.6875
    epoch 14, step 10050, loss = 1.38817, accuracy = 0.5
    epoch 14, step 10060, loss = 1.20160, accuracy = 0.640625
    epoch 14, step 10070, loss = 1.32729, accuracy = 0.609375
    epoch 14, step 10080, loss = 1.41240, accuracy = 0.546875
    epoch 14, step 10090, loss = 1.32657, accuracy = 0.5625
    epoch 14, step 10100, loss = 1.64916, accuracy = 0.5
    epoch 14, step 10110, loss = 1.33873, accuracy = 0.484375
    epoch 14, step 10120, loss = 1.31160, accuracy = 0.609375
    epoch 14, step 10130, loss = 1.17386, accuracy = 0.625
    epoch 14, step 10140, loss = 1.30510, accuracy = 0.625
    epoch 14, step 10150, loss = 1.11575, accuracy = 0.65625
    epoch 14, step 10160, loss = 1.11485, accuracy = 0.65625
    epoch 14, step 10170, loss = 1.51881, accuracy = 0.578125
    epoch 14, step 10180, loss = 1.33883, accuracy = 0.609375
    epoch 14, step 10190, loss = 1.17773, accuracy = 0.65625
    epoch 14, step 10200, loss = 1.23018, accuracy = 0.59375
    epoch 14, step 10210, loss = 1.39961, accuracy = 0.5
    epoch 14, step 10220, loss = 1.31615, accuracy = 0.515625
    epoch 14, step 10230, loss = 1.10946, accuracy = 0.59375
    epoch 14, step 10240, loss = 0.98418, accuracy = 0.734375
    epoch 14, step 10250, loss = 1.26857, accuracy = 0.609375
    epoch 14, step 10260, loss = 1.49406, accuracy = 0.53125
    epoch 14, step 10270, loss = 1.46354, accuracy = 0.46875
    epoch 14, step 10280, loss = 1.32909, accuracy = 0.5625
    epoch 14, step 10290, loss = 1.22332, accuracy = 0.640625
    epoch 14, step 10300, loss = 1.13144, accuracy = 0.65625
    epoch 14, step 10310, loss = 1.23438, accuracy = 0.640625
    epoch 14, step 10320, loss = 1.32552, accuracy = 0.625
    epoch 14, step 10330, loss = 1.37595, accuracy = 0.59375
    epoch 14, step 10340, loss = 1.22299, accuracy = 0.578125
    epoch 14, step 10350, loss = 1.44796, accuracy = 0.53125
    epoch 14, step 10360, loss = 1.44071, accuracy = 0.484375
    epoch 14, step 10370, loss = 1.22310, accuracy = 0.609375
    epoch 14, step 10380, loss = 1.32157, accuracy = 0.609375
    epoch 14, step 10390, loss = 1.58765, accuracy = 0.546875
    epoch 14, step 10400, loss = 1.34692, accuracy = 0.59375
    epoch 14, step 10410, loss = 1.33646, accuracy = 0.609375
    epoch 14, step 10420, loss = 1.17502, accuracy = 0.6875
    epoch 14, step 10430, loss = 1.34891, accuracy = 0.59375
    epoch 14, step 10440, loss = 1.36738, accuracy = 0.5
    epoch 14, step 10450, loss = 1.26145, accuracy = 0.53125
    epoch 14, step 10460, loss = 1.36941, accuracy = 0.609375
    epoch 14, step 10470, loss = 1.54562, accuracy = 0.5
    epoch 14, step 10480, loss = 1.30271, accuracy = 0.625
    epoch 14, step 10490, loss = 1.69151, accuracy = 0.453125
    epoch 14, step 10500, loss = 1.45050, accuracy = 0.53125
    epoch 14, step 10510, loss = 1.30551, accuracy = 0.578125
    epoch 14, step 10520, loss = 1.20079, accuracy = 0.671875
    epoch 14, step 10530, loss = 1.28322, accuracy = 0.59375
    epoch 14, step 10540, loss = 1.32893, accuracy = 0.546875
    validation after epoch 14: loss = 1.44966, accuracy = 0.5034
    Decreased learning rate by 0.5
    epoch 15, step 10550, loss = 1.26313, accuracy = 0.59375
    epoch 15, step 10560, loss = 1.28035, accuracy = 0.609375
    epoch 15, step 10570, loss = 1.14873, accuracy = 0.609375
    epoch 15, step 10580, loss = 1.37559, accuracy = 0.53125
    epoch 15, step 10590, loss = 1.25401, accuracy = 0.578125
    epoch 15, step 10600, loss = 1.20646, accuracy = 0.640625
    epoch 15, step 10610, loss = 1.24127, accuracy = 0.71875
    epoch 15, step 10620, loss = 1.30556, accuracy = 0.59375
    epoch 15, step 10630, loss = 1.10424, accuracy = 0.65625
    epoch 15, step 10640, loss = 1.28515, accuracy = 0.609375
    epoch 15, step 10650, loss = 1.13853, accuracy = 0.640625
    epoch 15, step 10660, loss = 1.24768, accuracy = 0.625
    epoch 15, step 10670, loss = 1.10909, accuracy = 0.65625
    epoch 15, step 10680, loss = 1.03014, accuracy = 0.6875
    epoch 15, step 10690, loss = 1.23162, accuracy = 0.703125
    epoch 15, step 10700, loss = 1.39562, accuracy = 0.515625
    epoch 15, step 10710, loss = 1.17636, accuracy = 0.671875
    epoch 15, step 10720, loss = 1.26604, accuracy = 0.5625
    epoch 15, step 10730, loss = 1.21443, accuracy = 0.6875
    epoch 15, step 10740, loss = 1.25684, accuracy = 0.625
    epoch 15, step 10750, loss = 1.14463, accuracy = 0.671875
    epoch 15, step 10760, loss = 1.25443, accuracy = 0.625
    epoch 15, step 10770, loss = 1.23412, accuracy = 0.65625
    epoch 15, step 10780, loss = 1.13669, accuracy = 0.671875
    epoch 15, step 10790, loss = 1.21755, accuracy = 0.578125
    epoch 15, step 10800, loss = 1.20318, accuracy = 0.59375
    epoch 15, step 10810, loss = 1.31204, accuracy = 0.59375
    epoch 15, step 10820, loss = 1.23462, accuracy = 0.5625
    epoch 15, step 10830, loss = 1.31004, accuracy = 0.6875
    epoch 15, step 10840, loss = 1.27765, accuracy = 0.640625
    epoch 15, step 10850, loss = 1.23841, accuracy = 0.59375
    epoch 15, step 10860, loss = 1.27182, accuracy = 0.609375
    epoch 15, step 10870, loss = 1.09576, accuracy = 0.65625
    epoch 15, step 10880, loss = 1.21410, accuracy = 0.640625
    epoch 15, step 10890, loss = 1.52756, accuracy = 0.578125
    epoch 15, step 10900, loss = 1.33130, accuracy = 0.578125
    epoch 15, step 10910, loss = 1.31511, accuracy = 0.546875
    epoch 15, step 10920, loss = 1.25164, accuracy = 0.640625
    epoch 15, step 10930, loss = 1.20352, accuracy = 0.6875
    epoch 15, step 10940, loss = 1.42029, accuracy = 0.53125
    epoch 15, step 10950, loss = 1.03841, accuracy = 0.671875
    epoch 15, step 10960, loss = 1.32613, accuracy = 0.578125
    epoch 15, step 10970, loss = 1.21217, accuracy = 0.640625
    epoch 15, step 10980, loss = 1.33675, accuracy = 0.5625
    epoch 15, step 10990, loss = 1.30019, accuracy = 0.5625
    epoch 15, step 11000, loss = 1.36149, accuracy = 0.5625
    epoch 15, step 11010, loss = 1.27677, accuracy = 0.671875
    epoch 15, step 11020, loss = 1.27592, accuracy = 0.578125
    epoch 15, step 11030, loss = 1.41004, accuracy = 0.53125
    epoch 15, step 11040, loss = 1.44892, accuracy = 0.59375
    epoch 15, step 11050, loss = 1.26930, accuracy = 0.625
    epoch 15, step 11060, loss = 1.29730, accuracy = 0.578125
    epoch 15, step 11070, loss = 1.12453, accuracy = 0.65625
    epoch 15, step 11080, loss = 1.23903, accuracy = 0.671875
    epoch 15, step 11090, loss = 1.41627, accuracy = 0.5625
    epoch 15, step 11100, loss = 1.42403, accuracy = 0.5625
    epoch 15, step 11110, loss = 1.30535, accuracy = 0.546875
    epoch 15, step 11120, loss = 1.20932, accuracy = 0.609375
    epoch 15, step 11130, loss = 1.38281, accuracy = 0.578125
    epoch 15, step 11140, loss = 1.28649, accuracy = 0.640625
    epoch 15, step 11150, loss = 1.09883, accuracy = 0.609375
    epoch 15, step 11160, loss = 1.12982, accuracy = 0.6875
    epoch 15, step 11170, loss = 1.17160, accuracy = 0.671875
    epoch 15, step 11180, loss = 1.24362, accuracy = 0.625
    epoch 15, step 11190, loss = 1.44500, accuracy = 0.59375
    epoch 15, step 11200, loss = 1.27256, accuracy = 0.578125
    epoch 15, step 11210, loss = 1.14912, accuracy = 0.578125
    epoch 15, step 11220, loss = 1.26947, accuracy = 0.59375
    epoch 15, step 11230, loss = 1.20452, accuracy = 0.609375
    epoch 15, step 11240, loss = 1.34585, accuracy = 0.625
    validation after epoch 15: loss = 1.43018, accuracy = 0.5056
    epoch 16, step 11250, loss = 1.33449, accuracy = 0.59375
    epoch 16, step 11260, loss = 1.26110, accuracy = 0.625
    epoch 16, step 11270, loss = 1.13442, accuracy = 0.65625
    epoch 16, step 11280, loss = 1.37018, accuracy = 0.5625
    epoch 16, step 11290, loss = 1.38144, accuracy = 0.59375
    epoch 16, step 11300, loss = 1.10985, accuracy = 0.671875
    epoch 16, step 11310, loss = 1.08842, accuracy = 0.703125
    epoch 16, step 11320, loss = 1.17322, accuracy = 0.6875
    epoch 16, step 11330, loss = 1.14327, accuracy = 0.578125
    epoch 16, step 11340, loss = 1.24138, accuracy = 0.5625
    epoch 16, step 11350, loss = 1.15692, accuracy = 0.65625
    epoch 16, step 11360, loss = 1.27084, accuracy = 0.546875
    epoch 16, step 11370, loss = 1.30340, accuracy = 0.5625
    epoch 16, step 11380, loss = 1.18389, accuracy = 0.671875
    epoch 16, step 11390, loss = 1.26216, accuracy = 0.546875
    epoch 16, step 11400, loss = 1.07915, accuracy = 0.640625
    epoch 16, step 11410, loss = 1.20082, accuracy = 0.671875
    epoch 16, step 11420, loss = 1.27260, accuracy = 0.625
    epoch 16, step 11430, loss = 1.20884, accuracy = 0.65625
    epoch 16, step 11440, loss = 1.01428, accuracy = 0.71875
    epoch 16, step 11450, loss = 1.22680, accuracy = 0.640625
    epoch 16, step 11460, loss = 1.32738, accuracy = 0.5625
    epoch 16, step 11470, loss = 1.25331, accuracy = 0.625
    epoch 16, step 11480, loss = 1.21713, accuracy = 0.65625
    epoch 16, step 11490, loss = 1.28995, accuracy = 0.65625
    epoch 16, step 11500, loss = 1.27243, accuracy = 0.59375
    epoch 16, step 11510, loss = 1.25534, accuracy = 0.515625
    epoch 16, step 11520, loss = 1.53165, accuracy = 0.5
    epoch 16, step 11530, loss = 1.16198, accuracy = 0.65625
    epoch 16, step 11540, loss = 1.06748, accuracy = 0.6875
    epoch 16, step 11550, loss = 1.16745, accuracy = 0.65625
    epoch 16, step 11560, loss = 1.33122, accuracy = 0.578125
    epoch 16, step 11570, loss = 1.12778, accuracy = 0.671875
    epoch 16, step 11580, loss = 1.28796, accuracy = 0.59375
    epoch 16, step 11590, loss = 1.10521, accuracy = 0.6875
    epoch 16, step 11600, loss = 1.30765, accuracy = 0.65625
    epoch 16, step 11610, loss = 1.45291, accuracy = 0.578125
    epoch 16, step 11620, loss = 1.16735, accuracy = 0.625
    epoch 16, step 11630, loss = 0.92191, accuracy = 0.71875
    epoch 16, step 11640, loss = 1.05050, accuracy = 0.6875
    epoch 16, step 11650, loss = 1.15259, accuracy = 0.65625
    epoch 16, step 11660, loss = 1.09023, accuracy = 0.703125
    epoch 16, step 11670, loss = 1.32524, accuracy = 0.46875
    epoch 16, step 11680, loss = 1.18096, accuracy = 0.65625
    epoch 16, step 11690, loss = 1.14352, accuracy = 0.671875
    epoch 16, step 11700, loss = 1.22799, accuracy = 0.65625
    epoch 16, step 11710, loss = 1.38903, accuracy = 0.515625
    epoch 16, step 11720, loss = 1.14943, accuracy = 0.625
    epoch 16, step 11730, loss = 1.22136, accuracy = 0.546875
    epoch 16, step 11740, loss = 1.21643, accuracy = 0.609375
    epoch 16, step 11750, loss = 1.28452, accuracy = 0.625
    epoch 16, step 11760, loss = 1.44856, accuracy = 0.53125
    epoch 16, step 11770, loss = 1.26391, accuracy = 0.625
    epoch 16, step 11780, loss = 1.22763, accuracy = 0.609375
    epoch 16, step 11790, loss = 1.02001, accuracy = 0.703125
    epoch 16, step 11800, loss = 1.12606, accuracy = 0.6875
    epoch 16, step 11810, loss = 1.01416, accuracy = 0.71875
    epoch 16, step 11820, loss = 1.12167, accuracy = 0.546875
    epoch 16, step 11830, loss = 1.45943, accuracy = 0.578125
    epoch 16, step 11840, loss = 1.21874, accuracy = 0.640625
    epoch 16, step 11850, loss = 1.11963, accuracy = 0.671875
    epoch 16, step 11860, loss = 1.27025, accuracy = 0.59375
    epoch 16, step 11870, loss = 1.25575, accuracy = 0.578125
    epoch 16, step 11880, loss = 1.24482, accuracy = 0.609375
    epoch 16, step 11890, loss = 1.33729, accuracy = 0.609375
    epoch 16, step 11900, loss = 1.13240, accuracy = 0.609375
    epoch 16, step 11910, loss = 1.07398, accuracy = 0.71875
    epoch 16, step 11920, loss = 1.17026, accuracy = 0.625
    epoch 16, step 11930, loss = 1.27984, accuracy = 0.59375
    epoch 16, step 11940, loss = 1.08188, accuracy = 0.6875
    epoch 16, step 11950, loss = 1.00155, accuracy = 0.71875
    validation after epoch 16: loss = 1.44521, accuracy = 0.5002
    epoch 17, step 11960, loss = 1.06062, accuracy = 0.765625
    epoch 17, step 11970, loss = 1.18638, accuracy = 0.65625
    epoch 17, step 11980, loss = 1.09722, accuracy = 0.671875
    epoch 17, step 11990, loss = 1.21050, accuracy = 0.5625
    epoch 17, step 12000, loss = 1.15826, accuracy = 0.671875
    epoch 17, step 12010, loss = 1.14783, accuracy = 0.671875
    epoch 17, step 12020, loss = 1.18551, accuracy = 0.640625
    epoch 17, step 12030, loss = 1.07302, accuracy = 0.6875
    epoch 17, step 12040, loss = 1.17250, accuracy = 0.65625
    epoch 17, step 12050, loss = 1.15296, accuracy = 0.640625
    epoch 17, step 12060, loss = 1.34561, accuracy = 0.5625
    epoch 17, step 12070, loss = 1.36737, accuracy = 0.578125
    epoch 17, step 12080, loss = 1.01348, accuracy = 0.6875
    epoch 17, step 12090, loss = 1.24213, accuracy = 0.625
    epoch 17, step 12100, loss = 1.11549, accuracy = 0.671875
    epoch 17, step 12110, loss = 1.12813, accuracy = 0.765625
    epoch 17, step 12120, loss = 1.27409, accuracy = 0.59375
    epoch 17, step 12130, loss = 1.22132, accuracy = 0.640625
    epoch 17, step 12140, loss = 1.45461, accuracy = 0.625
    epoch 17, step 12150, loss = 1.38281, accuracy = 0.5625
    epoch 17, step 12160, loss = 1.05592, accuracy = 0.765625
    epoch 17, step 12170, loss = 1.15526, accuracy = 0.65625
    epoch 17, step 12180, loss = 1.21514, accuracy = 0.671875
    epoch 17, step 12190, loss = 1.30172, accuracy = 0.609375
    epoch 17, step 12200, loss = 1.28263, accuracy = 0.625
    epoch 17, step 12210, loss = 1.07442, accuracy = 0.71875
    epoch 17, step 12220, loss = 1.14972, accuracy = 0.71875
    epoch 17, step 12230, loss = 1.41412, accuracy = 0.578125
    epoch 17, step 12240, loss = 1.50877, accuracy = 0.546875
    epoch 17, step 12250, loss = 1.29532, accuracy = 0.65625
    epoch 17, step 12260, loss = 1.38735, accuracy = 0.578125
    epoch 17, step 12270, loss = 1.07872, accuracy = 0.671875
    epoch 17, step 12280, loss = 1.06498, accuracy = 0.703125
    epoch 17, step 12290, loss = 1.27156, accuracy = 0.546875
    epoch 17, step 12300, loss = 1.04749, accuracy = 0.671875
    epoch 17, step 12310, loss = 1.36189, accuracy = 0.546875
    epoch 17, step 12320, loss = 1.15318, accuracy = 0.625
    epoch 17, step 12330, loss = 1.28698, accuracy = 0.546875
    epoch 17, step 12340, loss = 1.14838, accuracy = 0.65625
    epoch 17, step 12350, loss = 1.09248, accuracy = 0.671875
    epoch 17, step 12360, loss = 1.22582, accuracy = 0.65625
    epoch 17, step 12370, loss = 1.33247, accuracy = 0.578125
    epoch 17, step 12380, loss = 1.39872, accuracy = 0.578125
    epoch 17, step 12390, loss = 1.19901, accuracy = 0.671875
    epoch 17, step 12400, loss = 1.09688, accuracy = 0.65625
    epoch 17, step 12410, loss = 1.51039, accuracy = 0.515625
    epoch 17, step 12420, loss = 0.94485, accuracy = 0.71875
    epoch 17, step 12430, loss = 1.10934, accuracy = 0.65625
    epoch 17, step 12440, loss = 1.21275, accuracy = 0.625
    epoch 17, step 12450, loss = 1.04016, accuracy = 0.6875
    epoch 17, step 12460, loss = 1.05098, accuracy = 0.703125
    epoch 17, step 12470, loss = 1.12401, accuracy = 0.640625
    epoch 17, step 12480, loss = 1.13867, accuracy = 0.6875
    epoch 17, step 12490, loss = 1.28567, accuracy = 0.640625
    epoch 17, step 12500, loss = 1.23647, accuracy = 0.59375
    epoch 17, step 12510, loss = 1.28321, accuracy = 0.609375
    epoch 17, step 12520, loss = 1.27041, accuracy = 0.59375
    epoch 17, step 12530, loss = 1.05488, accuracy = 0.734375
    epoch 17, step 12540, loss = 1.29013, accuracy = 0.59375
    epoch 17, step 12550, loss = 1.45740, accuracy = 0.640625
    epoch 17, step 12560, loss = 1.02117, accuracy = 0.765625
    epoch 17, step 12570, loss = 1.29778, accuracy = 0.609375
    epoch 17, step 12580, loss = 1.26097, accuracy = 0.671875
    epoch 17, step 12590, loss = 1.17933, accuracy = 0.6875
    epoch 17, step 12600, loss = 1.16743, accuracy = 0.65625
    epoch 17, step 12610, loss = 1.14771, accuracy = 0.671875
    epoch 17, step 12620, loss = 1.22615, accuracy = 0.546875
    epoch 17, step 12630, loss = 1.04584, accuracy = 0.640625
    epoch 17, step 12640, loss = 1.11526, accuracy = 0.65625
    epoch 17, step 12650, loss = 1.03443, accuracy = 0.75
    validation after epoch 17: loss = 1.43562, accuracy = 0.5078
    Decreased learning rate by 0.5
    epoch 18, step 12660, loss = 1.09636, accuracy = 0.625
    epoch 18, step 12670, loss = 1.28262, accuracy = 0.578125
    epoch 18, step 12680, loss = 1.08476, accuracy = 0.71875
    epoch 18, step 12690, loss = 1.20836, accuracy = 0.671875
    epoch 18, step 12700, loss = 0.98993, accuracy = 0.703125
    epoch 18, step 12710, loss = 1.13281, accuracy = 0.671875
    epoch 18, step 12720, loss = 1.34707, accuracy = 0.65625
    epoch 18, step 12730, loss = 1.11740, accuracy = 0.65625
    epoch 18, step 12740, loss = 1.00551, accuracy = 0.734375
    epoch 18, step 12750, loss = 1.11268, accuracy = 0.640625
    epoch 18, step 12760, loss = 1.13750, accuracy = 0.671875
    epoch 18, step 12770, loss = 1.15671, accuracy = 0.65625
    epoch 18, step 12780, loss = 1.16271, accuracy = 0.671875
    epoch 18, step 12790, loss = 1.24514, accuracy = 0.53125
    epoch 18, step 12800, loss = 1.10261, accuracy = 0.703125
    epoch 18, step 12810, loss = 1.14870, accuracy = 0.65625
    epoch 18, step 12820, loss = 1.12532, accuracy = 0.65625
    epoch 18, step 12830, loss = 1.29705, accuracy = 0.59375
    epoch 18, step 12840, loss = 1.03850, accuracy = 0.6875
    epoch 18, step 12850, loss = 1.09790, accuracy = 0.703125
    epoch 18, step 12860, loss = 1.14790, accuracy = 0.671875
    epoch 18, step 12870, loss = 1.00826, accuracy = 0.71875
    epoch 18, step 12880, loss = 1.22868, accuracy = 0.65625
    epoch 18, step 12890, loss = 1.27610, accuracy = 0.59375
    epoch 18, step 12900, loss = 1.10341, accuracy = 0.6875
    epoch 18, step 12910, loss = 1.10382, accuracy = 0.625
    epoch 18, step 12920, loss = 1.08269, accuracy = 0.734375
    epoch 18, step 12930, loss = 1.37620, accuracy = 0.546875
    epoch 18, step 12940, loss = 1.14378, accuracy = 0.703125
    epoch 18, step 12950, loss = 1.15138, accuracy = 0.671875
    epoch 18, step 12960, loss = 1.06408, accuracy = 0.671875
    epoch 18, step 12970, loss = 1.21523, accuracy = 0.578125
    epoch 18, step 12980, loss = 1.05108, accuracy = 0.671875
    epoch 18, step 12990, loss = 1.05192, accuracy = 0.71875
    epoch 18, step 13000, loss = 1.12240, accuracy = 0.625
    epoch 18, step 13010, loss = 1.18992, accuracy = 0.625
    epoch 18, step 13020, loss = 1.16659, accuracy = 0.65625
    epoch 18, step 13030, loss = 1.05757, accuracy = 0.6875
    epoch 18, step 13040, loss = 1.31446, accuracy = 0.65625
    epoch 18, step 13050, loss = 1.07034, accuracy = 0.640625
    epoch 18, step 13060, loss = 1.16293, accuracy = 0.671875
    epoch 18, step 13070, loss = 1.00689, accuracy = 0.6875
    epoch 18, step 13080, loss = 1.00148, accuracy = 0.734375
    epoch 18, step 13090, loss = 1.28624, accuracy = 0.5625
    epoch 18, step 13100, loss = 1.04862, accuracy = 0.734375
    epoch 18, step 13110, loss = 1.24943, accuracy = 0.65625
    epoch 18, step 13120, loss = 1.23295, accuracy = 0.609375
    epoch 18, step 13130, loss = 1.10744, accuracy = 0.765625
    epoch 18, step 13140, loss = 1.02100, accuracy = 0.765625
    epoch 18, step 13150, loss = 1.16943, accuracy = 0.640625
    epoch 18, step 13160, loss = 1.20479, accuracy = 0.625
    epoch 18, step 13170, loss = 1.17188, accuracy = 0.625
    epoch 18, step 13180, loss = 1.05309, accuracy = 0.6875
    epoch 18, step 13190, loss = 1.28338, accuracy = 0.640625
    epoch 18, step 13200, loss = 1.21430, accuracy = 0.640625
    epoch 18, step 13210, loss = 1.21533, accuracy = 0.640625
    epoch 18, step 13220, loss = 1.31267, accuracy = 0.578125
    epoch 18, step 13230, loss = 1.29647, accuracy = 0.625
    epoch 18, step 13240, loss = 1.22479, accuracy = 0.625
    epoch 18, step 13250, loss = 1.17611, accuracy = 0.609375
    epoch 18, step 13260, loss = 1.14018, accuracy = 0.703125
    epoch 18, step 13270, loss = 1.16474, accuracy = 0.6875
    epoch 18, step 13280, loss = 0.95755, accuracy = 0.75
    epoch 18, step 13290, loss = 1.38349, accuracy = 0.5
    epoch 18, step 13300, loss = 1.19672, accuracy = 0.625
    epoch 18, step 13310, loss = 1.32686, accuracy = 0.578125
    epoch 18, step 13320, loss = 1.18431, accuracy = 0.578125
    epoch 18, step 13330, loss = 0.95475, accuracy = 0.703125
    epoch 18, step 13340, loss = 1.06486, accuracy = 0.6875
    epoch 18, step 13350, loss = 1.16711, accuracy = 0.625
    validation after epoch 18: loss = 1.41946, accuracy = 0.5162
    epoch 19, step 13360, loss = 0.99187, accuracy = 0.6875
    epoch 19, step 13370, loss = 1.08233, accuracy = 0.734375
    epoch 19, step 13380, loss = 1.03418, accuracy = 0.703125
    epoch 19, step 13390, loss = 1.05712, accuracy = 0.6875
    epoch 19, step 13400, loss = 1.17945, accuracy = 0.625
    epoch 19, step 13410, loss = 1.02429, accuracy = 0.703125
    epoch 19, step 13420, loss = 1.23060, accuracy = 0.65625
    epoch 19, step 13430, loss = 1.27535, accuracy = 0.59375
    epoch 19, step 13440, loss = 1.07022, accuracy = 0.71875
    epoch 19, step 13450, loss = 1.30110, accuracy = 0.5625
    epoch 19, step 13460, loss = 1.05338, accuracy = 0.75
    epoch 19, step 13470, loss = 1.02183, accuracy = 0.6875
    epoch 19, step 13480, loss = 1.04720, accuracy = 0.6875
    epoch 19, step 13490, loss = 1.18435, accuracy = 0.671875
    epoch 19, step 13500, loss = 1.02855, accuracy = 0.703125
    epoch 19, step 13510, loss = 0.81196, accuracy = 0.8125
    epoch 19, step 13520, loss = 1.31409, accuracy = 0.546875
    epoch 19, step 13530, loss = 1.07700, accuracy = 0.640625
    epoch 19, step 13540, loss = 0.92943, accuracy = 0.75
    epoch 19, step 13550, loss = 1.10445, accuracy = 0.71875
    epoch 19, step 13560, loss = 1.10391, accuracy = 0.671875
    epoch 19, step 13570, loss = 1.12002, accuracy = 0.671875
    epoch 19, step 13580, loss = 1.01890, accuracy = 0.78125
    epoch 19, step 13590, loss = 1.37748, accuracy = 0.515625
    epoch 19, step 13600, loss = 1.22793, accuracy = 0.5625
    epoch 19, step 13610, loss = 1.13105, accuracy = 0.578125
    epoch 19, step 13620, loss = 1.19883, accuracy = 0.578125
    epoch 19, step 13630, loss = 0.99405, accuracy = 0.6875
    epoch 19, step 13640, loss = 1.08391, accuracy = 0.640625
    epoch 19, step 13650, loss = 1.27409, accuracy = 0.578125
    epoch 19, step 13660, loss = 1.03361, accuracy = 0.703125
    epoch 19, step 13670, loss = 0.93112, accuracy = 0.734375
    epoch 19, step 13680, loss = 1.09554, accuracy = 0.671875
    epoch 19, step 13690, loss = 1.12566, accuracy = 0.671875
    epoch 19, step 13700, loss = 1.01845, accuracy = 0.671875
    epoch 19, step 13710, loss = 0.98506, accuracy = 0.75
    epoch 19, step 13720, loss = 1.32637, accuracy = 0.5625
    epoch 19, step 13730, loss = 1.16174, accuracy = 0.640625
    epoch 19, step 13740, loss = 0.94321, accuracy = 0.703125
    epoch 19, step 13750, loss = 1.21156, accuracy = 0.640625
    epoch 19, step 13760, loss = 1.09595, accuracy = 0.671875
    epoch 19, step 13770, loss = 1.16249, accuracy = 0.65625
    epoch 19, step 13780, loss = 1.09430, accuracy = 0.6875
    epoch 19, step 13790, loss = 1.11791, accuracy = 0.625
    epoch 19, step 13800, loss = 1.28216, accuracy = 0.625
    epoch 19, step 13810, loss = 1.15178, accuracy = 0.6875
    epoch 19, step 13820, loss = 1.19262, accuracy = 0.671875
    epoch 19, step 13830, loss = 1.23742, accuracy = 0.640625
    epoch 19, step 13840, loss = 1.11569, accuracy = 0.6875
    epoch 19, step 13850, loss = 1.33448, accuracy = 0.578125
    epoch 19, step 13860, loss = 0.83637, accuracy = 0.828125
    epoch 19, step 13870, loss = 1.12930, accuracy = 0.6875
    epoch 19, step 13880, loss = 1.16879, accuracy = 0.71875
    epoch 19, step 13890, loss = 1.00224, accuracy = 0.75
    epoch 19, step 13900, loss = 1.28994, accuracy = 0.59375
    epoch 19, step 13910, loss = 1.37919, accuracy = 0.515625
    epoch 19, step 13920, loss = 1.42918, accuracy = 0.515625
    epoch 19, step 13930, loss = 1.17700, accuracy = 0.640625
    epoch 19, step 13940, loss = 1.07153, accuracy = 0.71875
    epoch 19, step 13950, loss = 1.06767, accuracy = 0.734375
    epoch 19, step 13960, loss = 1.17894, accuracy = 0.65625
    epoch 19, step 13970, loss = 1.03036, accuracy = 0.75
    epoch 19, step 13980, loss = 1.15657, accuracy = 0.625
    epoch 19, step 13990, loss = 1.16631, accuracy = 0.625
    epoch 19, step 14000, loss = 1.09356, accuracy = 0.703125
    epoch 19, step 14010, loss = 1.20654, accuracy = 0.609375
    epoch 19, step 14020, loss = 1.17324, accuracy = 0.59375
    epoch 19, step 14030, loss = 1.20698, accuracy = 0.65625
    epoch 19, step 14040, loss = 1.18854, accuracy = 0.59375
    epoch 19, step 14050, loss = 1.21210, accuracy = 0.640625
    validation after epoch 19: loss = 1.42606, accuracy = 0.517
    
    Result:
    ------------------------------------
    loss on test set: 1.4430769560558157
    accuracy on test set: 0.5085
    
    Train statisistics:
    ------------------------------------
    time spend during forward pass: 153.72687697410583
    time spend during backward pass: 196.51766061782837
    time spend during l2 regularization: 427.95332622528076
    time spend during update pass: 249.79455137252808
    time spend in total: 1088.0380308628082
    
    Process finished with exit code 0

    """
    freeze_support()

    num_iteration = 20
    data = dataset.cifar10_dataset.load()

    layers = [
        ConvToFullyConnected(),
        FullyConnected(size=500, activation=activation.tanh),
        FullyConnected(size=500, activation=activation.tanh),
        FullyConnected(size=500, activation=activation.tanh),
        FullyConnected(size=500, activation=activation.tanh),
        FullyConnected(size=500, activation=activation.tanh),
        FullyConnected(size=10, activation=None, last_layer=True)
    ]

    # -------------------------------------------------------
    # Train with BP
    # -------------------------------------------------------

    model = Model(
        layers=layers,
        num_classes=10,
        optimizer=GDMomentumOptimizer(lr=1e-2, mu=0.9),
        regularization=0.01,
        # optimizer=GDMomentumOptimizer(lr=1e-2, mu=0.9),
        # regularization=0.0015,
        lr_decay=0.5,
        lr_decay_interval=3
    )

    print("\nRun training:\n------------------------------------")

    stats_bp = model.train(data_set=data, method='bp', num_passes=num_iteration, batch_size=64)
    loss, accuracy = model.cost(*data.test_set())

    print("\nResult:\n------------------------------------")
    print('loss on test set: {}'.format(loss))
    print('accuracy on test set: {}'.format(accuracy))

    print("\nTrain statisistics:\n------------------------------------")

    print("time spend during forward pass: {}".format(stats_bp['forward_time']))
    print("time spend during backward pass: {}".format(stats_bp['backward_time']))
    print("time spend during l2 regularization: {}".format(stats_bp['regularization_time']))
    print("time spend during update pass: {}".format(stats_bp['update_time']))
    print("time spend in total: {}".format(stats_bp['total_time']))

    # plt.title('Loss function')
    # plt.xlabel('epoch')
    # plt.ylabel('loss')
    # plt.plot(np.arange(len(stats_bp['train_loss'])), stats_bp['train_loss'])
    # plt.legend(['train loss bp'], loc='best')
    # plt.grid(True)
    # plt.show()

    # plt.title('Accuracy')
    # plt.xlabel('epoch')
    # plt.ylabel('accuracy')
    # plt.plot(np.arange(len(stats_bp['train_accuracy'])), stats_bp['train_accuracy'])
    # plt.legend(['train accuracy bp'], loc='best')
    # plt.grid(True)
    # plt.show()

    # exit()

    # -------------------------------------------------------
    # Train with DFA
    # -------------------------------------------------------

    model = Model(
        layers=layers,
        num_classes=10,
        optimizer=GDMomentumOptimizer(lr=3*1e-3, mu=0.9),
        regularization=0.09,
        lr_decay=0.5,
        lr_decay_interval=3
    )

    print("\nRun training:\n------------------------------------")

    stats_dfa = model.train(data_set=data, method='dfa', num_passes=num_iteration, batch_size=64)
    loss, accuracy = model.cost(*data.test_set())

    print("\nResult:\n------------------------------------")
    print('loss on test set: {}'.format(loss))
    print('accuracy on test set: {}'.format(accuracy))

    print("\nTrain statisistics:\n------------------------------------")

    print("time spend during forward pass: {}".format(stats_dfa['forward_time']))
    print("time spend during backward pass: {}".format(stats_dfa['backward_time']))
    print("time spend during l2 regularization: {}".format(stats_dfa['regularization_time']))
    print("time spend during update pass: {}".format(stats_dfa['update_time']))
    print("time spend in total: {}".format(stats_dfa['total_time']))

    plt.title('Loss function')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.plot(np.arange(len(stats_dfa['train_loss'])), stats_dfa['train_loss'])
    plt.plot(stats_dfa['valid_step'], stats_dfa['valid_loss'])
    plt.plot(np.arange(len(stats_bp['train_loss'])), stats_bp['train_loss'])
    plt.plot(stats_bp['valid_step'], stats_bp['valid_loss'])
    plt.legend(['train loss dfa', 'validation loss dfa', 'train loss bp', 'validation loss bp'], loc='upper right')
    plt.grid(True)
    plt.show()

    plt.title('Accuracy')
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.plot(np.arange(len(stats_dfa['train_accuracy'])), stats_dfa['train_accuracy'])
    plt.plot(stats_dfa['valid_step'], stats_dfa['valid_accuracy'])
    plt.plot(np.arange(len(stats_bp['train_accuracy'])), stats_bp['train_accuracy'])
    plt.plot(stats_bp['valid_step'], stats_bp['valid_accuracy'])
    plt.legend(['train accuracy dfa', 'validation accuracy dfa', 'train accuracy bp', 'validation accuracy bp'], loc='lower right')
    plt.grid(True)
    plt.show()

    step_to_time_bp = stats_bp['total_time'] / len(stats_bp['train_loss'])
    step_to_time_dfa = step_to_time_bp * stats_dfa['total_time'] / stats_bp['total_time']

    plt.title('Loss vs time')
    plt.xlabel('time')
    plt.ylabel('loss')
    plt.plot(np.arange(len(stats_dfa['train_loss'])) * step_to_time_dfa, stats_dfa['train_loss'])
    plt.plot(np.asarray(stats_dfa['valid_step']) * step_to_time_dfa, stats_dfa['valid_loss'])
    plt.plot(np.arange(len(stats_bp['train_loss'])) * step_to_time_bp, stats_bp['train_loss'])
    plt.plot(np.asarray(stats_bp['valid_step']) * step_to_time_bp, stats_bp['valid_loss'])
    plt.legend(['train loss dfa', 'validation loss dfa', 'train loss bp', 'validation loss bp'], loc='upper right')
    plt.grid(True)
    plt.show()

    plt.title('Accuracy vs time')
    plt.xlabel('time')
    plt.ylabel('accuracy')
    plt.plot(np.arange(len(stats_dfa['train_accuracy'])) * step_to_time_dfa, stats_dfa['train_accuracy'])
    plt.plot(np.asarray(stats_dfa['valid_step']) * step_to_time_dfa, stats_dfa['valid_accuracy'])
    plt.plot(np.arange(len(stats_bp['train_accuracy'])) * step_to_time_bp, stats_bp['train_accuracy'])
    plt.plot(np.asarray(stats_bp['valid_step']) * step_to_time_bp, stats_bp['valid_accuracy'])
    plt.legend(['train accuracy dfa', 'validation accuracy dfa', 'train accuracy bp', 'validation accuracy bp'], loc='lower right')
    plt.grid(True)
    plt.show()


    # smoothed curves

    plt.title('Loss vs epoch')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    dfa_train_loss = scipy.ndimage.filters.gaussian_filter1d(stats_dfa['train_loss'], sigma=10)
    bp_train_loss = scipy.ndimage.filters.gaussian_filter1d(stats_bp['train_loss'], sigma=10)
    plt.plot(np.arange(len(stats_dfa['train_loss'])), dfa_train_loss)
    plt.plot(stats_dfa['valid_step'], stats_dfa['valid_loss'])
    plt.plot(np.arange(len(stats_bp['train_loss'])), bp_train_loss)
    plt.plot(stats_bp['valid_step'], stats_bp['valid_loss'])
    plt.legend(['train loss dfa', 'validation loss dfa', 'train loss bp', 'validation loss bp'], loc='best')
    plt.grid(True)
    plt.show()

    plt.title('Accuracy vs epoch')
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    dfa_train_accuracy = scipy.ndimage.filters.gaussian_filter1d(stats_dfa['train_accuracy'], sigma=10)
    bp_train_accuracy = scipy.ndimage.filters.gaussian_filter1d(stats_bp['train_accuracy'], sigma=10)
    plt.plot(np.arange(len(stats_dfa['train_accuracy'])), dfa_train_accuracy)
    plt.plot(stats_dfa['valid_step'], stats_dfa['valid_accuracy'])
    plt.plot(np.arange(len(stats_bp['train_accuracy'])), bp_train_accuracy)
    plt.plot(stats_bp['valid_step'], stats_bp['valid_accuracy'])
    plt.legend(['train accuracy dfa', 'validation accuracy dfa', 'train accuracy bp', 'validation accuracy bp'], loc='best')
    plt.grid(True)
    plt.show()

    # Forward, regularization, update and validation passes are excactly the same operations for dfa and bp. Therefore
    # they should take euqally long. To ensure that inequalities don't affect the result, we normalize the time here.
    # The reference time is the one measured for bp.
    total_time_bp = stats_bp['total_time']
    total_time_dfa = total_time_bp - stats_bp['backward_time'] + stats_dfa['backward_time']
    step_to_time_bp = total_time_bp / len(stats_bp['train_loss'])
    step_to_time_dfa = step_to_time_bp * total_time_dfa / stats_bp['total_time']

    plt.title('Loss vs time')
    plt.xlabel('time')
    plt.ylabel('loss')
    dfa_train_loss = scipy.ndimage.filters.gaussian_filter1d(stats_dfa['train_loss'], sigma=10)
    bp_train_loss = scipy.ndimage.filters.gaussian_filter1d(stats_bp['train_loss'], sigma=10)
    plt.plot(np.arange(len(stats_dfa['train_loss'])) * step_to_time_dfa, dfa_train_loss)
    plt.plot(np.asarray(stats_dfa['valid_step']) * step_to_time_dfa, stats_dfa['valid_loss'])
    plt.plot(np.arange(len(stats_bp['train_loss'])) * step_to_time_bp, bp_train_loss)
    plt.plot(np.asarray(stats_bp['valid_step']) * step_to_time_bp, stats_bp['valid_loss'])
    plt.legend(['train loss dfa', 'validation loss dfa', 'train loss bp', 'validation loss bp'], loc='best')
    plt.grid(True)
    plt.show()

    plt.title('Accuracy vs time')
    plt.xlabel('time')
    plt.ylabel('accuracy')
    dfa_train_accuracy = scipy.ndimage.filters.gaussian_filter1d(stats_dfa['train_accuracy'], sigma=10)
    bp_train_accuracy = scipy.ndimage.filters.gaussian_filter1d(stats_bp['train_accuracy'], sigma=10)
    plt.plot(np.arange(len(stats_dfa['train_accuracy'])) * step_to_time_dfa, dfa_train_accuracy)
    plt.plot(np.asarray(stats_dfa['valid_step']) * step_to_time_dfa, stats_dfa['valid_accuracy'])
    plt.plot(np.arange(len(stats_bp['train_accuracy'])) * step_to_time_bp, bp_train_accuracy)
    plt.plot(np.asarray(stats_bp['valid_step']) * step_to_time_bp, stats_bp['valid_accuracy'])
    plt.legend(['train accuracy dfa', 'validation accuracy dfa', 'train accuracy bp', 'validation accuracy bp'], loc='lower right')
    plt.grid(True)
    plt.show()
