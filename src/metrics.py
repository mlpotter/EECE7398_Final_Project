from lifelines.utils import concordance_index
import numpy as np
import pandas as pd
from src.utils import lower_bound
import torch



def concordance(clf,dataloader,epsilons):
    X,T,E = dataloader.dataset.tensors

    cis = np.zeros_like(epsilons)
    for i,epsilon in enumerate(epsilons):
        lb,ub = lower_bound(clf,X,epsilon)
        ub = ub.detach()
        if ub.isnan().sum()>1:
            ub[ub.isnan()] = (np.nanmax(ub) + torch.tensor(np.random.randn(ub.isnan().sum(),1)).ravel()).type(torch.float)
            print("NaN values in UB!")
        ci = concordance_index(event_times=T, predicted_scores=-ub, event_observed=E)
        print("CI @ eps={}".format(epsilon),ci)

        cis[i] = ci

    return epsilons, cis
