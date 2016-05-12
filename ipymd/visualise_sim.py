# -*- coding: utf-8 -*-
"""
Created on Sun May  1 23:47:03 2016

@author: cjs14
"""
from io import BytesIO

import numpy as np

from chemlab.graphics.qtviewer import QtViewer
from chemlab.graphics.renderers.atom import AtomRenderer
from chemlab.graphics.renderers.box import BoxRenderer
from chemlab.graphics.renderers.line import LineRenderer
from chemlab.graphics.colors import get as str_to_colour
from chemlab.graphics import colors as chemlab_colors
from chemlab.db import ChemlabDB
from chemlab.graphics.transformations import rotation_matrix
def orbit_z(self, angle):
    # Subtract pivot point
    self.position -= self.pivot        
    # Rotate
    rot = rotation_matrix(-angle, self.c)[:3,:3]
    self.position = np.dot(rot, self.position)        
    # Add again the pivot point
    self.position += self.pivot
    
    self.a = np.dot(rot, self.a)
    self.b = np.dot(rot, self.b)
    self.c = np.dot(rot, self.c)     
from chemlab.graphics.camera import Camera
Camera.orbit_z = orbit_z


from IPython.display import Image as ipy_Image
from PIL import Image, ImageChops

class Visualise_Sim(object):
    """ 
    A class to visualise atom data    
    """
    _unit_dict = {'real':{'distance':0.1}}
    
    def __init__(self, colormap=None, radiimap=None, units='real'):
        """
        colormap: dict, should contain the 'Xx' key,value pair
           A dictionary mapping atom types to colors. By default it is the color
           scheme provided by `chemlab.graphics.colors.default_atom_map`. The 'Xx'
           symbol value is taken as the default color.        
        radii_map: dict, should contain the 'Xx' key,value pair.
           A dictionary mapping atom types to radii. The default is the
           mapping contained in `chemlab.db.vdw.vdw_dict`        
        For units *real*, these are the units:
        
            mass = grams/mole
            distance = Angstroms
            time = femtoseconds
            energy = Kcal/mole
            velocity = Angstroms/femtosecond
            force = Kcal/mole-Angstrom
            torque = Kcal/mole
            temperature = Kelvin
            pressure = atmospheres
            dynamic viscosity = Poise
            charge = multiple of electron charge (1.0 is a proton)
            dipole = charge*Angstroms
            electric field = volts/Angstrom
            density = gram/cm^dim
        """
        assert units=='real', 'currently only supports real units'
        self._units = units
        self._atomcolors = None
        self.change_atom_colormap()
        self._atomradii = None  
        self.change_atom_radiimap()
        
    def change_atom_colormap(self, colormap=None, colorstrs=False):
        """
        colormap : dict, should contain the 'Xx' key,value pair
           A dictionary mapping atom types to colors, in RGBA format (0-255) 
           By default it is the color scheme provided by 
           `chemlab.graphics.colors.default_atom_map`. The 'Xx' symbol value is 
           taken as the default color.   
        colorstrs : bool
            if True, colors should be strings matching colors in `chemlab.graphics.colors`
        """
        if colormap is None:
            self._atomcolors = chemlab_colors.default_atom_map
        else:
            assert colormap.has_key('Xx'), "colormap should contain an 'Xx' default key"
            if colorstrs:
                colormap = dict([[k,str_to_colour(v)] for k,v in colormap.iteritems()])
                if None in colormap.values():
                    raise ValueError('one or more colors not found')
            self._atomcolors = colormap

    def change_atom_radiimap(self, radiimap=None):
        """
        radii_map: dict, should contain the 'Xx' key,value pair.
           A dictionary mapping atom types to radii. The default is the
           mapping contained in `chemlab.db.vdw.vdw_dict`        
        """
        if radiimap is None:
            self._atomradii = ChemlabDB().get("data", 'vdwdict')
        else:
            assert radiimap.has_key('Xx'), "radiimap should contain an 'Xx' default key"
            self._atomradii = radiimap

    def _unit_conversion(self, values, measure):
        """ 
        values : np.array 
        measure : str       
        """
        if not self._unit_dict.has_key(self._units):
            raise NotImplementedError
        if not self._unit_dict[self._units].has_key(measure):
            raise NotImplementedError

        return values * self._unit_dict[self._units][measure]
        
    def _trim_image(self, im):
        """
        a simple solution to trim whitespace on the image
        
        1. It gets the border colour from the top left pixel, using getpixel, 
        so you don't need to pass the colour.
        2. Subtracts a scalar from the differenced image, 
        this is a quick way of saturating all values under 100, 100, 100 to zero. 
        So is a neat way to remove any 'wobble' resulting from compression.
        """
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)

    def visualise(self, atoms_df, type_dict={}, bounds=None, spheres=True, 
                  xrot=0, yrot=0, zrot=0, fov=10., 
                  show_axes=True, axes_offset=(-0.2,0.2), axes_length=1,
                  width=400, height=400):
        """ 
        bounds : np.array((3,2), dtype=float)
            simulation box
        sphere : render spheres, otherwise points
        rotx: rotation about x (degrees)
        roty: rotation about y (degrees)
        rotz: rotation about z (degrees)
        (start x-axis horizontal, y-axis vertical)
        
        """
        assert set(['xs','ys','zs','type']).issubset(set(atoms_df.columns))
        r_array = np.array([s[['xs','ys','zs']] for i,s in atoms_df.iterrows()])
        r_array = self._unit_conversion(r_array, 'distance')
        all_array = r_array
        
        type_array = [type_dict.get(s['type'], 'Xx') for i,s in atoms_df.iterrows()]

        # initialize graphic engine
        v = QtViewer()
        w = v.widget 
        w.initializeGL()
        w.camera.fov = fov

        ## add renderers
        ## ---------------
        rends = []

        #simulation bounding box render
        if not bounds is None:
            bounds = self._unit_conversion(bounds, 'distance')
            x0, y0, z0 = bounds[:,0]
            x1, y1, z1 = bounds[:,1]
            
            # move r_array so origin is at (0,0,0)
            r_array[:,0] = r_array[:,0] - x0           
            r_array[:,1] = r_array[:,1] - y0           
            r_array[:,2] = r_array[:,2] - z0           
            
            vectors = np.array([[x1-x0,0,0],[0,y1-y0,0],[0,0,z1-z0]])
            rends.append(v.add_renderer(BoxRenderer, vectors))
            
            #TODO account for other corners of box?
            all_array = np.concatenate([r_array,vectors])
         
        #atoms renderer
        backend = 'impostors' if spheres else 'points'
        rends.append(v.add_renderer(AtomRenderer, r_array, type_array,
                    color_scheme=self._atomcolors, radii_map=self._atomradii,
                    backend=backend))            
        
        # transfrom coordinate system
        w.camera.orbit_x(xrot*np.pi/180.)
        w.camera.orbit_y(yrot*np.pi/180.)
        w.camera.orbit_z(zrot*np.pi/180.)
        
        # axes renderer
        if show_axes:
            # find top-left coordinate after transformations and 
            # convert to original coordinate system
            
            ones = np.ones((all_array.shape[0],1))
            trans_array = np.apply_along_axis(w.camera.matrix.dot,1,np.concatenate((all_array,ones),axis=1))[:,[0,1,2]]
            t_top_left = [trans_array[:,0].min() + axes_offset[0] - axes_length, 
                          trans_array[:,1].max() + axes_offset[1], 
                          trans_array[:,2].min(), 1]
            
            x0, y0, z0 = np.linalg.inv(w.camera.matrix).dot(t_top_left)[0:3]
            origin = [x0, y0, z0]
            all_array = np.concatenate([all_array, [origin]])
            
            vectors = [[x0+axes_length,y0,z0], 
                       [x0,y0+axes_length,z0], 
                       [x0,y0,z0+axes_length]]
            # colors consistent with ovito
            colors = [str_to_colour('red'),str_to_colour('green'),str_to_colour('blue')]
            for vector, color in zip(vectors, colors):
                # for some reason it won't render if theres not a 'dummy' 2nd element
                startends = [[origin, vector],[origin, vector]]                      
                colors = [[color, color],[color, color]]
                #TODO add as arrows instead of lines 
                rends.append(v.add_renderer(LineRenderer, startends, colors))
                #TODO add x,y,z labels (look at chemlab.graphics.__init__)

        w.camera.autozoom(all_array)

        # convert scene to image
        image = w.toimage(width, height)
        image = self._trim_image(image)
        b = BytesIO()
        image.save(b, format='png')
        data = b.getvalue()

        # Cleanup
        for r in rends:
            del r
        del v
        del w
        
        return ipy_Image(data=data)