from __future__ import print_function
import numpy as np
import yt
#from yt.fields.particle_fields import add_volume_weighted_smoothed_field
import powderday.config as cfg
from powderday.mlt.dgr_extrarandomtree_part import dgr_ert

def ramses_field_add(fname, bounding_box=None, ds=None):
    
    # metallicity fraction
    def _starmetallicityfraction(field, data):
        return data[('star', 'particle_chem_Fe')] / data[('star','particle_chem_H')]
    # starmetals_00
    # starmetals
    def _starmetals(field, data):
        return data[('star','particle_metallicity')]
    # starcoordinates
    def _starcoordinates(field,data):
        xpos = data[('star','particle_position_x')].in_units("cm")
        ypos = data[('star','particle_position_y')].in_units("cm")
        zpos = data[('star','particle_position_z')].in_units("cm")
        coordinates = data.ds.arr(np.c_[xpos, ypos, zpos], "cm")
        return coordinates
    # starformationtime
    # starmasses
    def _starmasses(field,data):
        return data[('star','particle_mass')]
    # diskstarcoordinates
    # diskstarmasses
    # bulgestarmasses
    # bulgestarcoordinates

    # gassmoothinglength
    # gasdensity
    def _gasdensity(field,data):
        return data[('gas','density')]
    # gasmetals_00
    # gasmetals
    def _gasmetals(field,data):
        return data[('gas','metallicity')]
    # gascoordinates
    # gasmasses
    def _gasmasses(field,data):
        return data[('gas','mass')]
    # gasfh2
    def _gasfh2(field,data):
        try:
            return data[('gas','FractionH2')]
        except:
            return data[('gas','metallicity')]*0. # just some dimensionless array
    # gassfr
    # gassmootheddensity
    # gassmothedmetals
    # gassmoothedmasses

    # metaldens_00
    # metaldens
    def _gasmetaldensity(field,data):
        return (data[('gas', 'metal_mass')]/data[('gas','volume')])
    # metalmass_00
    # metalmass_00
    # metalmass
    # metalsmoothedmasses

    # dustmass_manual
    # dustmass_dtm
    # li_ml_dustmass
    # dustmass_rr
    # dustmass_li_bestfit
    # dustsmoothedmasses
    # li_ml_dustsmoothedmasses
    # return_dust_mass
    # dust_density
    # particle_dust_numgrains
    # particle_dust_carbon_fraction
    # particle_dust_mass
    # particle_dust_coordinates

    # stellarages
    def _stellarages(field,data):
        return data[('star','age')].in_units('Gyr') # or star_age?
    # starsmoothedmasses

    # bhluminosity
    # bhcoordinates
    # bhsed_nu
    # bhsed_sed
    # size_with_units

    # 
    # (only arepo) dustcoordinates

    if fname !=  None:
        ds = yt.load(fname)
        ds.index

    ad = ds.all_data()

    ds.add_field(('star','metallicity_fraction'),function=_starmetallicityfraction,units="dimensionless",sampling_type='particle')
    ds.add_field(('star','metals'),function=_starmetals,units="code_metallicity",sampling_type='particle')
    ds.add_field(('star','coordinates'),function=_starcoordinates,units="cm",sampling_type='particle')
    ds.add_field(('stellar','ages'),function=_stellarages,units='Gyr',sampling_type='particle')
    ds.add_field(('star','masses'),function=_starmasses,units='g',sampling_type='particle')
    ds.add_field(('gas','density'),function=_gasdensity,units='g/cm**3',sampling_type='cell')
    ds.add_field(('gas','metals'),function=_gasmetals,units="code_metallicity",sampling_type='cell')
    ds.add_field(('gas','metal_density'),function=_gasmetaldensity,units="g/cm**3",sampling_type='cell')
    ds.add_field(('gas','fh2'),function=_gasfh2,units='dimensionless',sampling_type='cell')
    ds.add_field(('gas','masses'),function=_gasmasses,units='g',sampling_type='cell')
    

    ad = ds.all_data()
    return ds