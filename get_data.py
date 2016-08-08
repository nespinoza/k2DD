# -*- coding: utf-8 -*-
from scipy.signal import medfilt
from scipy.ndimage.filters import gaussian_filter
import numpy as np
import argparse
import pyfits
import urllib
import os

# Read user input:
parser = argparse.ArgumentParser()
parser.add_argument('-epicid',default=None)
parser.add_argument('-campaign',default=None)

args = parser.parse_args()
EPICID = args.epicid
campaign = args.campaign

def get_metadata(epicid):
    url = 'http://archive.stsci.edu/k2/epic/search.php?'
    url += 'action=Search'
    url += '&target='+epicid
    url += '&outputformat=CSV'
    lines = urllib.urlopen(url)
    data = {}
    counter = 0
    for line in lines:
        if counter == 0:
            names = line.split(',')
            names[-1] = names[-1].split('\n')[0]
            counter += 1
        elif counter == 1:
            dtypes = line.split(',')
            dtypes[-1] = dtypes[-1].split('\n')[0]
            counter += 1
        else:
            values = line.split(',')
            values[-1] = values[-1].split('\n')[0]
            for j in range(len(values)):
                if dtypes[j] == 'integer':
                    if values[j] != '':
                        data[names[j]] = int(values[j])
                    else:
                        data[names[j]] = -1
                elif dtypes[j] == 'float':
                    if values[j] != '':
                        data[names[j]] = float(values[j])
                    else:
                        data[names[j]] = -1
                else:
                    data[names[j]] = values[j]
    return data

# Create folder where we will save the downloads:
if not os.path.exists('outputs'):
    os.mkdir('outputs')

# First, download lightcurve:
print '\n\t Retrieving lightcurve for '+EPICID+'...'
print '\t -----------------------------------------\n'
fname = 'hlsp_everest_k2_llc_'+EPICID+'-c'+campaign+'_kepler_v1.0_lc.fits'
if not os.path.exists('outputs/'+fname):
    os.system('wget --no-check-certificate https://archive.stsci.edu/missions/hlsp/everest/c'\
               +campaign+'/'+EPICID[0:4]+'00000/'+EPICID[4:]+\
               '/'+fname)
    os.system('mv '+fname+' outputs/'+fname)

print '\t Done!\n'

# Extract data:
lc,h = pyfits.getdata('outputs/'+fname,header=True)
t = lc['TIME']
flux = lc['FLUX']

# Take out the nans, add zeroth time to get BJD times:
idx_not_nans = np.where(~np.isnan(flux))[0]
t = t[idx_not_nans] + np.double(h['TUNIT1'].split()[-1])
flux = flux[idx_not_nans]

# Now get meta-data:
print '\t Retrieving meta-data...'
print '\t -----------------------'
meta_data = get_metadata(EPICID)

# Plot lightcurve, print important EPIC data:
print '\t Success! Important meta-data for target:'
print '\t      RA: ',meta_data['RA']
print '\t     Dec: ',meta_data['Dec']
print '\t       V: ',meta_data['Vmag']
print '\t       g: ',meta_data['gmag']
print '\t       r: ',meta_data['rmag']
print '\t       i: ',meta_data['imag']
print ''

# Save times and fluxes:
meta_data['times'] = t
meta_data['fluxes'] = flux

# Save file:
if not os.path.exists(EPICID+'.pkl'):
    import pickle
    FILE = open(EPICID+'.pkl','w')
    pickle.dump(meta_data, FILE)
    FILE.close()
    print '\t ----------------------------------'
    print '\t Data saved to file '+EPICID+'.pkl'
    print '\t ----------------------------------\n'
