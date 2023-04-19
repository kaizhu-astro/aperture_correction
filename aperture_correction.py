import numpy as np


'''
    Copyright (C) 2023, Kai Zhu
    E-mail: kaizhu@nao.cas.cn
    
    If you have found this software useful for your research,
    I would appreciate a citation for Zhu et al (2023).
    See example at the bottom for usage instructions.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
    PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

def get_alpha(Mr, g_i, n_Ser, q=None):
    '''
    The required quantities and ranges are:
    *    Mr:    [-18, -24]    SDSS r-band absolute magnitude
    *    g_i:   [0.4, 1.6]    SDSS g-band absolute magnitude minus SDSS i-band absolute magnitude
    *    n_Ser: [0, 8]        Sersic index
    Optional:
    *    q:     [0, 1]        Axial ratio. If q is not None, apply the corrections to obtain the alpha
                              within circular aperture, see Equation (5) from Zhu et al. 2023
    '''
    assert (Mr>=-24) & (Mr<=-18) & (g_i>=0.4) & (g_i<=1.6) & (n_Ser>0) & (n_Ser<=8), 'The input quantities are not appropriate for this table'
    alpha1 = np.array([[np.nan,np.nan,0.044,0.026,0.005,np.nan],
                       [0.110,0.106,0.069,0.037,0.004,np.nan],
                       [0.113,0.118,0.084,0.041,-0.001,np.nan],
                       [0.152,0.144,0.114,0.051,-0.025,np.nan],
                       [0.180,0.175,0.135,0.069,np.nan,np.nan],
                       [0.221,0.187,0.145,np.nan,np.nan,np.nan]])
    alpha_err1 = np.array([[np.nan,np.nan,0.013,0.019,0.021,np.nan],
                           [0.014,0.008,0.004,0.008,0.013,np.nan],
                           [0.009,0.004,0.005,0.0005,0.009,np.nan],
                           [0.008,0.006,0.005,0.007,0.019,np.nan],
                           [0.009,0.005,0.008,0.012,np.nan,np.nan],
                           [0.019,0.012,0.012,np.nan,np.nan,np.nan]])
    alpha2 = np.array([[np.nan,np.nan,0.002,-0.024,-0.025,-0.011],
                       [0.063,0.001,-0.010,-0.022,-0.033,-0.004],
                       [0.059,0.026,0.001,-0.017,-0.045,np.nan],
                       [0.077,0.067,0.043,0.000,np.nan,np.nan],
                       [0.090,0.091,np.nan,np.nan,np.nan,np.nan],
                       [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]])
    alpha_err2 = np.array([[np.nan,np.nan,0.009,0.005,0.004,0.009],
                           [0.021,0.006,0.003,0.003,0.004,0.011],
                           [0.007,0.005,0.005,0.004,0.006,np.nan],
                           [0.019,0.012,0.014,0.009,np.nan,np.nan],
                           [0.026,0.020,np.nan,np.nan,np.nan,np.nan],
                           [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]])
    alpha3 = np.array([[np.nan,np.nan,-0.059,-0.046,-0.043,-0.025],
                       [np.nan,-0.019,-0.047,-0.045,-0.040,-0.025],
                       [np.nan,-0.004,-0.043,-0.050,-0.039,-0.015],
                       [np.nan,-0.013,-0.029,-0.050,-0.047,np.nan],
                       [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],
                       [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]])
    alpha_err3 = np.array([[np.nan,np.nan,0.010,0.004,0.002,0.003],
                           [np.nan,0.011,0.003,0.002,0.001,0.002],
                           [np.nan,0.009,0.004,0.003,0.003,0.007],
                           [np.nan,0.014,0.013,0.007,0.010,np.nan],
                           [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],
                           [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]])
    Mr_bin = np.array([-18,-19,-20,-21,-22,-23,-24])
    g_i_bin = np.array([1.6,1.4,1.2,1.0,0.8,0.6,0.4])
    n_Ser_bin = np.array([0,2,4,8])
    if (n_Ser>n_Ser_bin[0]) and (n_Ser<n_Ser_bin[1]):
        i = (Mr_bin>Mr).sum()-1
        j = (g_i_bin>g_i).sum()-1
        alpha = alpha1[j,i]
        alpha_err = alpha_err1[j,i]
    elif (n_Ser>n_Ser_bin[1]) and (n_Ser<n_Ser_bin[2]):
        i = (Mr_bin>Mr).sum()-1
        j = (g_i_bin>g_i).sum()-1
        alpha = alpha2[j,i]
        alpha_err = alpha_err2[j,i]
    elif (n_Ser>n_Ser_bin[2]) and (n_Ser<n_Ser_bin[3]):
        i = (Mr_bin>Mr).sum()-1
        j = (g_i_bin>g_i).sum()-1
        alpha = alpha3[j,i]
        alpha_err = alpha_err3[j,i]
    if (Mr in Mr_bin) or (g_i in g_i_bin) or (n_Ser in n_Ser_bin):
        print ('#######################################################################################')
        print ('Be careful! The input quantities are positioned exactly on the bin edges of this table.')
        print ('#######################################################################################')
    print("Alpha value for Mr={}, g-i={}, n_Ser={} is: {} with an error of {}".format(Mr, g_i, n_Ser, alpha, alpha_err))
    if q is None:
        return alpha, alpha_err
    if q is not None:
        alpha_circ = alpha-0.106*(1-q)**4.73
        print("Alpha_cric value for Mr={}, g-i={}, n_Ser={}, q={} is: {:.3f}".format(Mr, g_i, n_Ser, q, alpha_circ))
        return alpha, alpha_err, alpha_circ
    


def test():
    Mr = -22.1
    g_i = 1.1
    n_Ser = 1.2
    alpha,alpha_err,alpha_circ=get_alpha(Mr,g_i,n_Ser,q=0.3)

if __name__ == '__main__':

    test()
