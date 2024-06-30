from __future__ import print_function
import numpy as np
from hyperion.model import Model
from hyperion.grid import AMRGrid
import powderday.config as cfg
from powderday.analytics import proj_plots
from powderday.helpers import energy_density_absorbed_by_CMB
from hyperion.dust import SphericalDust


from powderday.grid_construction import ramses_grid_generate



import yt
import os
import six



def ramses_m_gen(fname,field_add):
    
    refined, dust_smoothed, fc1, fw1, reg, ds1 = ramses_grid_generate(fname,field_add)

    m = Model()

    center = ds1.arr([cfg.model.x_cent, cfg.model.y_cent, cfg.model.z_cent], 'code_length')
    [xcent,ycent,zcent] = center.in_units('cm')
    print('[ramses_HANNAH] center :', center.in_units('kpc'))

    boost = np.array([xcent,ycent,zcent])
    print('[ramses_tributary] boost = ', boost)

    dx = 2.* ds1.quan(cfg.par.zoom_box_len,'kpc').to('cm')
    dy = 2.* ds1.quan(cfg.par.zoom_box_len,'kpc').to('cm')
    dz = 2.* ds1.quan(cfg.par.zoom_box_len,'kpc').to('cm')

    m.__dict__['grid_type'] = 'oct'
    m.set_octree_grid(0, 0, 0, dx/2, dy/2, dz/2, refined)
    
    xmin = ds1.quan(xcent-dx/2., 'kpc')
    xmax = ds1.quan(xcent+dx/2., 'kpc')
    ymin = ds1.quan(ycent-dy/2., 'kpc')
    ymax = ds1.quan(ycent+dy/2., 'kpc')
    zmin = ds1.quan(zcent-dz/2., 'kpc')
    zmax = ds1.quan(zcent+dz/2., 'kpc')

    print('[ramses_tributary] xmin (pc)= ', xmin.to('pc')) #(xcent-dx/2.).to('pc'))
    print('[ramses_tributary] xmax (pc)= ', xmax.to('pc')) #(xcent+dx/2.).to('pc'))
    print('[ramses_tributary] ymin (pc)= ', ymin.to('pc')) #(ycent-dy/2.).to('pc'))
    print('[ramses_tributary] ymax (pc)= ', ymax.to('pc')) #(ycent+dy/2.).to('pc'))
    print('[ramses_tributary] zmin (pc)= ', zmin.to('pc')) #(zcent-dz/2.).to('pc'))
    print('[ramses_tributary] zmax (pc)= ', zmax.to('pc')) #(zcent+dz/2.).to('pc'))
    

    return m,xcent,ycent,zcent,dx,dy,dz,reg,ds1,boost
    
