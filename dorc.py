import numpy as np
from pyod.models.iforest import IForest
from scipy import stats
import time


def dorc(preprocessedData, random_state, outliers_fraction=0.1):

    t0 = time.time()
    clf = IForest(contamination=outliers_fraction, random_state=random_state, n_jobs=-1)
    clf.fit(preprocessedData)
    scores = clf.decision_function(preprocessedData)

    # Apply IQR-based criteria to identify rare cells for further downstream analysis.
    q3 = np.percentile(scores, 75)
    iqr = stats.iqr(scores)
    th = q3 + (1.5 * iqr)

    # Select indexes that satisfy IQR-based thresholding criteria.
    indIqr = np.where(scores >= th)[0]
    print('shape of selected cells : {}'.format(indIqr.shape))

    # Create a file with binary predictions
    predictions = np.zeros(preprocessedData.shape[0])
    predictions[indIqr] = 1  # Replace predictions for rare cells with '1'.

    t1 = time.time()
    duration = round(t1 - t0, ndigits=4)
    print("Total running DoRC time is :" + str(duration) + " s")

    return predictions, scores, duration