k2DD
----

This code downloads the K2 lightcurve (using the EVEREST algorithm) along with the meta-data for the 
EPIC target in dictionary form. All this is saved on a easy-to-use dictionary. 

Author: Néstor Espinoza (nespino@astro.puc.cl)

USAGE
-----
To use this code, modify the `get_data.py` file with the EPIC ID of interest along with the campaign name and do

    python get_data.py

This will save an `EPICID.pkl` file (where EPICID is the EPIC ID of the target)  which can then be 
called from python by doing:

    import pickle
    data = pickle.load(open('EPICID.pkl','r'))

The `data` dictionary will then have all the data of the target stored in it, which includes:

    data['times']                The times (in BJD TBD)
    
    data['fluxes']               The EVEREST corrected flux

Along with meta-data in the MAST format (https://archive.stsci.edu/k2/epic/search.php). For example, 
`data['Vmag']` stores the V magnitude of the star, `data['KepMag']` the Kepler Magnitude, etc.


