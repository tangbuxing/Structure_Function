# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 18:12:20 2021
"""
import numpy as np
import pandas as pd
import sys
sys.path.append(r'F:\Work\MODE\tra_test_Structure_Function')    #导入的函数路径
import rdist

def structurogram(loc, y, q = 2, Id = 'NULL', d = 'NULL', lon_lat = False, 
                  dmax = 'NULL', N = 'NULL', breaks = 'NULL'):
    out = {}
    #y <- cbind(y)    #R:y原本是列表，用cbind变为数组
    '''
    if (is.null(id)) {
        n <- nrow(loc)
        ind <- rep(1:n, n) > rep(1:n, rep(n, n))
        id <- cbind(rep(1:n, n), rep(1:n, rep(n, n)))[ind, ]
    }
    '''
    #ind从0开始
    if Id == 'NULL':
        n = len(loc)
        aa = np.tile(np.arange(0, n), n) 
        bb = np.repeat(np.arange(0, n), n) 
        ind = aa > bb
        Id = np.vstack((aa, bb)).T[ind, :]
    '''
    if (is.null(d)) {
        loc <- as.matrix(loc)
        if (lon.lat) {
            d <- rdist.earth(loc)[id]
        }
        else {
            d <- rdist(loc, loc)[id]
        }
    }
    '''
    if d == 'NULL':
        if lon_lat:
            d = rdist.Earth(x1=loc)[Id]
        else:
            #d <- rdist(loc, loc)[id]
            d = rdist.rdist(Id = Id, loc = loc)
    '''
    vg <- 0.5 * rowMeans(cbind(abs(y[id[, 1], ] - y[id[, 2], 
        ])^q), na.rm = TRUE)
    call <- match.call()
    '''
    #由于Id和y的数组长度不一致，二者呈倍数关系，因而先将这两个数组的长度整理一致
    #如果len(Id)>len(y)
    y1 = np.tile(y, int(len(Id)/len(y)))
    vg1 = abs(y1[Id[:, 0]] - y1[Id[:, 1]])**q
    vg = 0.5 * np.mean(vg1.reshape(len(vg1), 1), axis = 1)
    call = 'match.call()'
    '''
    if (is.null(dmax)) {
        dmax <- max(d)
    }
    '''
    if dmax == 'NULL':
        dmax = np.max(d)
    '''
    od <- order(d)
    d <- d[od]
    vg <- vg[od]
    ind <- d <= dmax & !is.na(vg)
    out <- list(d = d[ind], val = vg[ind], call = call, q = q)
    '''
    od = np.argsort(d)
    d = d[od]
    vg = vg[od]
    ind = (d <= dmax) & (vg != np.nan)
    out = {'d':d[ind], 'val':vg[ind], 'call':call, 'q':q}
    '''
    if (!is.null(breaks) | !is.null(N)) {
        out <- c(out, stats.bin(d[ind], vg[ind], N = N, breaks = breaks))
    }
    class(out) <- "structurogram"
    '''
    if breaks != 'NULL' or N != 'NULL':
        # out <- c(out, stats.bin(d[ind], vg[ind], N = N, breaks = breaks))
        out.update({})
    out['class'] = 'structurogram'
    return out 

'''
if __name__ == '__main__':
    dat = pd.read_csv("F:\\Work\\MODE\\tra_test\\FeatureFinder\\pert000.csv").values
    loc = pd.read_csv("F:\\Work\\MODE\\tra_test\\FeatureFinder\\ICPg240Locs.csv").values
    #剪裁一小部分数据，数据量过大会报错
    loc = loc[150300-1:150450,:]
    yy = dat[299, 249:400]
    q = 2
    Id = 'NULL'
    d = 'NULL'
    lon_lat = False
    dmax = 'NULL'
    N = 'NULL'
    breaks = 'NULL'
    
    look_struct = structurogram(loc = loc, y = yy)
'''











