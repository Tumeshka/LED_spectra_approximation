# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:35:13 2023

@author: Alexander Kalyanov
"""

import scipy.stats as stats
import numpy as np

def johnson(qnt, x):
    ''' Compute Johnson PDF
    '''
    
    # Slifker and Shapiro algorithm
    z0 = 0
    dz = 0.5
    
    m = qnt[3] - qnt[2]
    n = qnt[1] - qnt[0]
    p = qnt[2] - qnt[1]
    q0 = .5*(qnt[1]+qnt[2])
    
    mop = m / p
    nop = n / p
    
    tol = 1e-4
    
    '''
    Define type of Jonhson distribution and comopute PDF accordingly
    
    Given the output "itype", you can choose to instantiate either a normal 
    curve, exponential curve, Johnson-SU or Johnson-SB via SciPy. When you do 
    this, beta and gamma correspond to SciPy's "a" and "b" parameters, whereas 
    sigma and lam correspond to the "location" and "scale" parameters. You can 
    test this by pulling the Mean, StdDev, Skewness and Kurtosis from the SciPy 
    distribution you instantiated and checking to see that they match the 
    inoputs you passed to the JNSN function.
    '''
    if mop*nop < 1-tol:
        johnson_type = 'SB'         # bounded Johnson distribution
        # print(johnson_type)
        
        pom = p / m
        pon = p / n
        a = dz / np.arccosh(0.5 * ((1 + pom) * (1 + pon))**0.5)
        b = z0 + a * np.arcsinh((pon - pom) * (((1 + pom) * (1 + pon) - 4)**0.5) / (2 * (pom * pon - 1)))
        scale = p * ((((1 + pom) * (1 + pon) - 2)**2 - 4))**0.5 / (pom * pon - 1)
        loc = q0 - .5 * scale + p * (pon - pom) / (2 * (pom * pon - 1))
        
        # calculate distribution
        rv = stats.johnsonsb(b, a, loc=loc, scale=scale)    
        pdf = rv.pdf(x)
        
        # calculate statistics
        ## mean
        mean = rv.mean()                                    
        ## median
        median = rv.median()
        ## mode (peak of pdf)
        xm = x[np.argmax(rv.pdf(x))]
        x1=np.linspace(xm-2,xm+2,4001)
        mode = x1[np.argmax(rv.pdf(x1))]
        
        param = [johnson_type, a, b, loc, scale]
        
    elif mop*nop > 1 + tol:
        johnson_type = 'SU'          # unbounded Johnson distribution
        # print(johnson_type)
        
        a = 2 * dz / np.arccosh(0.5 * (mop + nop))
        b = z0 + a * np.arcsinh((nop - mop) / (2 * (mop * nop - 1)**0.5))
        scale = 2 * p * ((mop * nop - 1)**0.5) / ((mop + nop - 2) * (mop + nop + 2)**0.5)
        loc = q0 + p * (nop - mop) / (2 * (mop + nop - 2))
        
        # pdf = stats.johnsonsu.pdf(x, b, a, loc=loc, scale=scale)
        
        # calculate distribution
        rv = stats.johnsonsu(b, a, loc=loc, scale=scale)    
        pdf = rv.pdf(x)
        
        # calculate statistics
        # mean
        mean = rv.mean()
        ## median
        median = rv.median()
        ## mode (peak of pdf)
        xm = x[np.argmax(rv.pdf(x))]
        x1=np.linspace(xm-2,xm+2,4001)
        mode = x1[np.argmax(rv.pdf(x1))]
        
        param = [johnson_type, a, b, loc, scale]
        
    else:
        johnson_type = 'SN'          # normal distribution
        # print(johnson_type)
        
        a = 2 * dz / m
        b = (z0 - q0 * a)
        loc = - b / a
        scale = 1 / a
        
        # pdf = stats.norm.pdf(x, loc=loc, scale=scale)
        
        # calculate distribution
        rv = stats.norm(loc=loc, scale=scale)    
        pdf = rv.pdf(x)
        
        # calculate statistics
        ## mean
        mean = rv.mean()
        ## median
        median = mean
        ## mode (peak of pdf)
        mode = mean
        
        param = [johnson_type, None, None, loc, scale]
        
        ''' 
        TODO: solve lognormal parametrization when have time
        if abs(mop-1)>tol:
            johnson_type = 'SL'          # lognormal distribution
            print(johnson_type)
            
            # When mp < 1, gamma/eta will have -pi imaginary part.  After
            # exponentiating, that's equivalent to lambda == -1 instead of 1.
            a = 2 * dz / np.log(mop)
            gamma = z0 + a * np.log(abs(mop - 1) / (p * (mop)**0.5))
            scale = np.log(-gamma/a)
            scale = (-gamma/a)

            # lambda = sign(mp-1);
            epsilon = q0 - .5 * p * (mop + 1) / (mop - 1)

            s =np.exp(a/gamma)
            
            u = np.log(np.exp(-gamma/a) + epsilon)
            
            s = np.log(np.mean([(qnt[2] / np.exp(u))**0.5, \
                                 (np.exp(u) / qnt[1])**0.5]))
            print([u, s, np.log(qnt[2] / np.exp(u)), np.log(np.exp(u) / qnt[1])])
            print([np.log((qnt[2] / np.exp(u))**0.5)])
            
            loc = np.exp(-gamma/a)+epsilon
            
            pdf = stats.lognorm.pdf(x, s, loc=loc, scale=scale)
            param = [johnson_type, s, None, loc, scale]
            
            # r = lambda.*exp((randn(sizeOut) - gamma) ./ eta) + epsilon;  
        else:
            johnson_type = 'SN'          # normal distribution
            print(johnson_type)
            
            a = 2 * dz / m
            b = (z0 - q0 * a)
            loc = - b / a
            scale = 1 / a
            
            pdf = stats.norm.pdf(x, loc=loc, scale=scale)
            param = [johnson_type, None, None, loc, scale]

            # r = (randn(sizeOut) - gamma) ./ eta;
        '''
    stc = {'mean': mean, 'median': median, 'mode': mode}
        
    return pdf, param, stc