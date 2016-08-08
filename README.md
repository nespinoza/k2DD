k2DD
----

This code downloads a K2 lightcurve ("detrended" using the EVEREST algorithm; see [Luger et al., 2016](http://arxiv.org/abs/1607.00524)) 
along with the meta-data (i.e., V-magnitude, RA, DEC, etc.) for the star obtained from the EPIC catalog. 
All this is saved on a easy-to-use dictionary. 

Author: Néstor Espinoza (nespino@astro.puc.cl)

USAGE
-----
To use this code, run the `get_data.py` script as follows:

    python get_data.py -epicid EPICID -campaign nc

where `EPICID` is the EPIC ID of the target and `nc` is the campaign number (01,02,03..). This 
will download the lightcurves and meta-data from the MAST and save everything in a file called 
`EPICID.pkl` which can then be opened in python by doing:

    import pickle
    data = pickle.load(open('EPICID.pkl','r'))

The `data` dictionary will have both the lightcurve data and meta-data, which includes:

    data['times']                The times (in BJD TBD)
    
    data['fluxes']               The EVEREST corrected flux

Along with meta-data in the MAST format (https://archive.stsci.edu/k2/epic/search.php). For example, 
`data['Vmag']` stores the V magnitude of the star, `data['KepMag']` the Kepler Magnitude, etc.

EXAMPLE
-------
Suppose we want to get all the data for the K2-34 hot-Jupiter, a.k.a. EPIC 212110888 (see, [Brahm et al., 
2016](https://arxiv.org/abs/1603.01721)). This was a target from Campaign 5 so, in this case, we call 
the algorithm as:

    python get_data.py -epicid 212110888 -campaign 05

This will download the data, and save everything in a file called `212110888.pkl`. Once this is done, 
we can play with the data stored in this pickle file. For example, the following script uses this 
data to generate the phased lightcurve, taking the period of P = 2.995629 and t0 = 2457144.34703 
days found in [Brahm et al., 2016](https://arxiv.org/abs/1603.01721), and plots the V-magnitude in the title of the plot:

    import pickle
    import numpy as np
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')

    # Open downloaded data:
    data = pickle.load(open('212110888.pkl','r'))
    # Filter the flux:
    from scipy.signal import medfilt
    from scipy.ndimage.filters import gaussian_filter
    filter = aussian_filter(medfilt(data['fluxes'],39),5)
    filtered_flux = data['fluxes']/mg_filter
    # Phase the lightcurve:
    P = 2.995629
    t0 = 2457144.34703
    phase = ((data['times'] - t0)/P) % 1
    ii = np.where(phase>=0.5)[0]
    phase[ii] = phase[ii]-1.0
    # Plot:
    plt.plot(phase,filtered_flux,'.')
    plt.xlabel('Phase')
    plt.ylabel('Relative flux')
    plt.title('EPIC 212110888, V = '+str(data['Vmag']))
    plt.show()
    
The result of this script is the following plot:

![Awesome plot of K2-34](/imgs/example.png)
