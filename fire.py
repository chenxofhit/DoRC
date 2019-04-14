import FiRE
import numpy as np
from scipy import stats
import time

def fire(preprocessedData, L=100, M=50):

    t0 = time.time()
    ##Create model of FiRE.
    model = FiRE.FiRE(L=L, M=M)
    model.fit(preprocessedData)

    #Assign FiRE score to every cell.
    scores = np.array(model.score(preprocessedData))

    #Apply IQR-based criteria to identify rare cells for further downstream analysis.
    q3 = np.percentile(scores, 75)
    iqr = stats.iqr(scores)
    th = q3 + (1.5*iqr)

    #Select indexes that satisfy IQR-based thresholding criteria.
    indIqr = np.where(scores >= th)[0]
    print('shape of selected cells : {}'.format(indIqr.shape))

    #Create a file with binary predictions
    predictions = np.zeros(preprocessedData.shape[0])
    predictions[indIqr] = 1 #Replace predictions for rare cells with '1'.

    t1 = time.time()
    duration = round(t1 - t0, ndigits=4)
    print("Total running FiRE time is :" + str(duration) + " s")

    return predictions, scores, duration