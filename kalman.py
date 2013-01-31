from pylab import *
from numpy import *

class Kalman:
      def __init__(self, ndim):
        self.ndim = ndim
        self.Sigma_x = eye(ndim)*1e-5
        self.A = eye(ndim)
        self.H = eye(ndim)
        self.mu_hat = 0
        self.cov = eye(ndim)
        self.R = eye(ndim)*0.01
        self.index = 0
        self.mu_init = array([0] * 50)
        self.k = Kalman(self.ndim)
        self.nsteps = 50

        cov_init=0.1*ones((ndim))


      def update(self, obs):
        
        self.index += 1
        self.mu_init[self.index] = obs

        if self.index > 50 
                self.index = 0

        # Make prediction
        self.mu_hat_est = dot(self.A,self.mu_hat)
        self.cov_est = dot(self.A,dot(self.cov,transpose(self.A))) + self.Sigma_x

        # Update estimate
        self.error_mu = obs - dot(self.H,self.mu_hat_est)
        self.error_cov = dot(self.H,dot(self.cov,transpose(self.H))) + self.R
        self.K = dot(dot(self.cov_est,transpose(self.H)),linalg.inv(self.error_cov))
        self.mu_hat = self.mu_hat_est + dot(self.K,self.error_mu)
        if ndim>1:
            self.cov = dot((eye(self.ndim) - dot(self.K,self.H)),self.cov_est)
        else:
            self.cov = (1-self.K)*self.cov_est 
        
        return 
 
    
