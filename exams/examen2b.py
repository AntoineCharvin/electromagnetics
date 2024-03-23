#nom: CHARVIN
#prenom: Antoine
#Exercice 2b


# -*- coding: utf-8 -*-
#***********************************************************************
#     2-D FDTD TE code with PML absorbing boundary conditions
#***********************************************************************
#
#     Program author: Susan C. Hagness
#                     Department of Electrical and Computer Engineering
#                     University of Wisconsin-Madison
#                     1415 Engineering Drive
#                     Madison, WI 53706-1691
#                     hagness@engr.wisc.edu
#
#     Copyright 2005
#
#     This MATLAB M-file implements the finite-difference time-domain
#     solution of Maxwell's curl equations over a two-dimensional
#     Cartesian space lattice comprised of uniform square grid cells.
#
#     To illustrate the algorithm, a 6-cm-diameter metal cylindrical 
#     scatterer in free space is modeled. The source excitation is 
#     a Gaussian pulse with a carrier frequency of 5 GHz.
#
#     The grid resolution (dx  =  3 mm) was chosen to provide 20 samples
#     per wavelength at the center frequency of the pulse (which in turn
#     provides approximately 10 samples per wavelength at the high end
#     of the excitation spectrum, around 10 GHz).
#
#     The computational domain is truncated using the perfectly matched
#     layer (PML) absorbing boundary conditions.  The formulation used 
#     in this code is based on the original split-field Berenger PML. 
#     Exponential time stepping is implemented in the PML regions. 
#     The PML regions are labeled as shown in the following diagram: 
#
#            ----------------------------------------------
#           |  |                BACK PML                |  |
#            ----------------------------------------------
#           |L |                                       /| R|
#           |E |                                (ib,jb) | I|
#           |F |                                        | G|
#           |T |                                        | H|
#           |  |                MAIN GRID               | T|
#           |P |                                        |  |
#           |M |                                        | P|
#           |L | (1,1)                                  | M|
#           |  |/                                       | L|
#            ----------------------------------------------
#           |  |                FRONT PML               |  |
#            ----------------------------------------------
#
#     To execute this M-file, type "fdtd2D" at the MATLAB prompt.  
#
#     This code has been tested in the following Matlab environments:
#     Matlab version 6.1.0.450 Release 12.1 (May 18, 2001)
#     Matlab version 6.5.1.199709 Release 13 Service Pack 1 (August 4, 2003)
#     Matlab version 7.0.0.19920 R14 (May 6, 2004)
#     Matlab version 7.0.1.24704 R14 Service Pack 1 (September 13, 2004)
#     Matlab version 7.0.4.365 R14 Service Pack 2 (January 29, 2005)
#
#     Note: if you are using Matlab version 6.x, you may wish to make
#     one or more of the following modifications to this code: 
#       --uncomment line numbers 418 and 419
#       --comment out line numbers 610, 619, and 628
#
#***********************************************************************

#***********************************************************************
#  Numerical and plotting libraries
#***********************************************************************

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

#***********************************************************************
#     Fundamental constants
#***********************************************************************

cc = 2.99792458e8            #speed of light in free space
muz = 4.0*np.pi*1.0e-7          #permeability of free space
epsz = 1.0/(cc*cc*muz)       #permittivity of free space
etaz = np.sqrt(muz/epsz)

freq = 5.0e+9                #center frequency of source excitation
lambda0 = cc/freq             #center wavelength of source excitation
omega = 2.0*np.pi*freq          

#***********************************************************************
#     Grid parameters
#***********************************************************************

im = 151           #nombre de noeuds pour hz dans la direction x
jm = 81            #nombre de noeuds pour hz dans la direction y

#calcul des bornes supérieures pour i et j quand les indices débutent à 1
ie = im+1
je = jm+1

ib = ie+1
jb = je+1

isource = 30            #location of z-directed hard source
jsource = int(je/2)          #location of z-directed hard source

dx = 3.0e-3        #space increment of square lattice
xmin = 0
xmax = xmin+(im-1)*dx
ymin = 0
ymax = ymin+(jm-1)*dx
dt = dx/(2.0*cc)   #time step

nmax = 500         #total number of time steps

imbc = 8            #épaisseur des PML à gauche et à droite
jmbc = 8            #épaisseur des PML à l'avant et à l'arrière

#calcul des bornes supérieures pour i et j quand les indices débutent à 1
iebc = imbc+1
jebc = imbc+1
rmax = 1.0e-7
orderbc = 2
ibbc = iebc+1
jbbc = jebc+1
iefbc = ie+2*iebc
jefbc = je+2*jebc
ibfbc = iefbc+1
jbfbc = jefbc+1

#***********************************************************************
#     Material parameters
#***********************************************************************

media = 2

eps = [1.0, 1.9**2]
sig = [0.0, 0.0]
mur = [1.0, 1.0]
sim = [0.0, 0.0]

#***********************************************************************
#     Wave excitation
#***********************************************************************

rtau = 160.0e-12
tau = rtau/dt
delay = 3*tau

source = np.zeros(nmax)
for n in range(int(7.0*tau)):
  source[n] = np.sin(omega*(n-delay)*dt)*np.exp(-((n-delay)**2/tau**2))

#***********************************************************************
#     Field arrays
#***********************************************************************

# initialisation des tableaux de la grille principale
def ct(i,j):
    return np.zeros((i,j+1)), np.zeros((i+1,j)), np.zeros((i,j))

# initialisation des tableaux pour les conditions aux limites
def ctbc(i,j):
    return np.zeros((i,j+1)), np.zeros((i+1,j)), np.zeros((i,j)), np.zeros((i,j))

#fields and coefs in main grid 
ex, ey, hz = ct(ie,je)
caex, caey, dahz = ct(ie,je)
cbex, cbey, dbhz = ct(ie,je)

#fields and coefs in front PML region
exbcf, eybcf, hzxbcf, hzybcf = ctbc(iefbc,jebc)   
caexbcf, caeybcf, dahzxbcf, dahzybcf = ctbc(iefbc,jebc)
cbexbcf, cbeybcf, dbhzxbcf, dbhzybcf = ctbc(iefbc,jebc)   

#fields and coefs in back PML region
exbcb, eybcb, hzxbcb, hzybcb = ctbc(iefbc,jebc) 
caexbcb, caeybcb, dahzxbcb, dahzybcb = ctbc(iefbc,jebc)
cbexbcb, cbeybcb, dbhzxbcb, dbhzybcb = ctbc(iefbc,jebc)

#fields and coefs in left PML region
exbcl, eybcl, hzxbcl, hzybcl = ctbc(iebc,je) 
caexbcl, caeybcl, dahzxbcl, dahzybcl = ctbc(iebc,je)
cbexbcl, cbeybcl, dbhzxbcl, dbhzybcl = ctbc(iebc,je) 

#fields and coefs in right PML region
exbcr, eybcr, hzxbcr, hzybcr = ctbc(iebc,je) 
caexbcr, caeybcr, dahzxbcr, dahzybcr = ctbc(iebc,je)
cbexbcr, cbeybcr, dbhzxbcr, dbhzybcr = ctbc(iebc,je)

#***********************************************************************
#     Updating coefficients
#***********************************************************************

ca  =  np.zeros(media)
cb  =  np.zeros(media)
da  =  np.zeros(media)
db  =  np.zeros(media)

for i in range(media):
  eaf   = dt*sig[i]/(2.0*epsz*eps[i])
  ca[i] = (1.0-eaf)/(1.0+eaf)
  cb[i] = dt/epsz/eps[i]/dx/(1.0+eaf)
  haf   = dt*sim[i]/(2.0*muz*mur[i])
  da[i] = (1.0-haf)/(1.0+haf)
  db[i] = dt/muz/mur[i]/dx/(1.0+haf)

#***********************************************************************
#     Geometry specification (main grid)
#***********************************************************************

#     Initialize entire main grid to free space

caex[1:,1:] = ca[0]     
caey[1:,1:] = ca[0]
dahz[1:,1:] = da[0]

cbex[1:,1:] = cb[0]     
cbey[1:,1:] = cb[0]
dbhz[1:,1:] = db[0]

#     Add dielectric cylinder

diam = 3*lambda0/2 #avec par exemple 20, on voit bien un cylindre
print("remarque : je ne vois pas de cylindre sur l'animation avec un diamètre si petit")
rad = diam/2.0     # radius of cylinder: 3 cm
icenter = 2*ie/3   # i-coordinate of cylinder's center
jcenter = je/2     # j-coordinate of cylinder's center

for i in range(1,ie):
  for j in range(1,je): 
    dist2 = (i+0.5-icenter)**2 + (j-jcenter)**2
    if dist2 <= rad**2: 
       caex[i,j] = ca[1]
       cbex[i,j] = cb[1]
    dist2 = (i-icenter)**2 + (j+0.5-jcenter)**2
    if dist2 <= rad**2: 
       caey[i,j] = ca[1]
       cbey[i,j] = cb[1]

#***********************************************************************
#     Fill the PML regions
#
#     PML theory describes a continuous grading of the material properties
#     over the PML region.  In the FDTD grid it is necessary to discretize
#     the grading by averaging the material properties over a grid cell 
#     width centered on each field component.  As an example of the 
#     implementation of this averaging, we take the integral of the 
#     continuous sigma(x) in the PML region
#   
#         sigma_i  =  integral(sigma(x))/dx
#   
#     where the integral is over a single grid cell width in x, and is 
#     bounded by x1 and x2.  Applying this to the polynomial grading of 
#     Equation 7.60a produces
#
#         sigma_i  =  sigmam/(dx*(m+1)*d**m)*(x2**(m+1)-x1**(m+1))
#
#     where sigmam is the maximum value of sigma as described by Equation 
#     7.62.  In the code below, the coefficient in the expression for
#     sigma_i is denoted "bcfactor".
#         
#     The definitions of x1 and x2 depend on the position of the field 
#     component within the grid cell.  We have either
#
#         x1  =  (i-0.5)*dx,  x2  =  (i+0.5)*dx
#  
#     or
#  
#         x1  =  (i)*dx,      x2  =  (i+1)*dx
#
#     where i varies over the PML region.
#  
#***********************************************************************

delbc = (iebc-1)*dx
sigmam = -np.log(rmax)*(orderbc+1)/(2*etaz*delbc)   #Eq. 7.62 in text
bcfactor = sigmam/(dx*(orderbc+1)*(delbc**orderbc)) 

#     FRONT region 

caexbcf[1:iefbc,1] = 1.0
cbexbcf[1:iefbc,1] = 0.0
for j in range(2,jebc):
  y1 = (jebc-1-j+1.5)*dx
  y2 = (jebc-1-j+0.5)*dx
  sigmay = bcfactor*(y1**(orderbc+1)-y2**(orderbc+1))
  ca1 = np.exp(-sigmay*dt/epsz)
  cb1 = (1.0-ca1)/(sigmay*dx)
  caexbcf[1:iefbc,j] = ca1
  cbexbcf[1:iefbc,j] = cb1
sigmay  =  bcfactor*(0.5*dx)**(orderbc+1)
ca1 = np.exp(-sigmay*dt/epsz)
cb1 = (1-ca1)/(sigmay*dx)
caex[1:ie,1] = ca1
cbex[1:ie,1] = cb1
caexbcl[1:iebc,1] = ca1
cbexbcl[1:iebc,1] = cb1
caexbcr[1:iebc,1] = ca1
cbexbcr[1:iebc,1] = cb1

for j in range(1,jebc):
  y1 = (jebc-1-j+1)*dx
  y2 = (jebc-1-j)*dx
  sigmay = bcfactor*(y1**(orderbc+1)-y2**(orderbc+1))
  sigmays = sigmay*(muz/epsz)
  da1 = np.exp(-sigmays*dt/muz)
  db1 = (1-da1)/(sigmays*dx)
  dahzybcf[1:iefbc,j] = da1
  dbhzybcf[1:iefbc,j] = db1
  caeybcf[1:ibfbc,j] = ca[0]
  cbeybcf[1:ibfbc,j] = cb[0]
  dahzxbcf[1:iefbc,j] = da[0]
  dbhzxbcf[1:iefbc,j] = db[0]

#     BACK region 

caexbcb[1:iefbc,jbbc-1] = 1.0
cbexbcb[1:iefbc,jbbc-1] = 0.0
for j in range(2,jebc):
  y1 = (j-0.5)*dx
  y2 = (j-1.5)*dx
  sigmay = bcfactor*(y1**(orderbc+1)-y2**(orderbc+1))
  ca1 = np.exp(-sigmay*dt/epsz)
  cb1 = (1-ca1)/(sigmay*dx)
  caexbcb[1:iefbc,j] = ca1
  cbexbcb[1:iefbc,j] = cb1
sigmay  =  bcfactor*(0.5*dx)**(orderbc+1)
ca1 = np.exp(-sigmay*dt/epsz)
cb1 = (1-ca1)/(sigmay*dx)
caex[1:ie,jb-1] = ca1
cbex[1:ie,jb-1] = cb1
caexbcl[1:iebc,jb-1] = ca1
cbexbcl[1:iebc,jb-1] = cb1
caexbcr[1:iebc,jb-1] = ca1
cbexbcr[1:iebc,jb-1] = cb1

for j in range(1,jebc):
  y1 = j*dx
  y2 = (j-1)*dx
  sigmay = bcfactor*(y1**(orderbc+1)-y2**(orderbc+1))
  sigmays = sigmay*(muz/epsz)
  da1 = np.exp(-sigmays*dt/muz)
  db1 = (1-da1)/(sigmays*dx)
  dahzybcb[1:iefbc,j] = da1
  dbhzybcb[1:iefbc,j] = db1
  caeybcb[1:ibfbc,j] = ca[0]
  cbeybcb[1:ibfbc,j] = cb[0]
  dahzxbcb[1:iefbc,j] = da[0]
  dbhzxbcb[1:iefbc,j] = db[0]

#     LEFT region 

caeybcl[1,1:je] = 1.0
cbeybcl[1,1:je] = 0.0
for i in range(2,iebc):
  x1 = (iebc-1-i+1.5)*dx
  x2 = (iebc-1-i+0.5)*dx
  sigmax = bcfactor*(x1**(orderbc+1)-x2**(orderbc+1))
  ca1 = np.exp(-sigmax*dt/epsz)
  cb1 = (1-ca1)/(sigmax*dx)
  caeybcl[i,1:je] = ca1
  cbeybcl[i,1:je] = cb1
  caeybcf[i,1:jebc] = ca1
  cbeybcf[i,1:jebc] = cb1
  caeybcb[i,1:jebc] = ca1
  cbeybcb[i,1:jebc] = cb1
sigmax = bcfactor*(0.5*dx)**(orderbc+1)
ca1 = np.exp(-sigmax*dt/epsz)
cb1 = (1-ca1)/(sigmax*dx)
caey[1,1:je] = ca1
cbey[1,1:je] = cb1
caeybcf[iebc+1,1:jebc] = ca1
cbeybcf[iebc+1,1:jebc] = cb1
caeybcb[iebc+1,1:jebc] = ca1
cbeybcb[iebc+1,1:jebc] = cb1

for i in range(1,iebc):
  x1 = (iebc-1-i+1)*dx
  x2 = (iebc-1-i)*dx
  sigmax = bcfactor*(x1**(orderbc+1)-x2**(orderbc+1))
  sigmaxs = sigmax*(muz/epsz)
  da1 = np.exp(-sigmaxs*dt/muz)
  db1 = (1-da1)/(sigmaxs*dx)
  dahzxbcl[i,1:je] = da1
  dbhzxbcl[i,1:je] = db1
  dahzxbcf[i,1:jebc] = da1
  dbhzxbcf[i,1:jebc] = db1
  dahzxbcb[i,1:jebc] = da1
  dbhzxbcb[i,1:jebc] = db1
  caexbcl[i,2:je] = ca[0]
  cbexbcl[i,2:je] = cb[0]
  dahzybcl[i,1:je] = da[0]
  dbhzybcl[i,1:je] = db[0]

#     RIGHT region 

caeybcr[ibbc-1,1:je] = 1.0
cbeybcr[ibbc-1,1:je] = 0.0
for i in range(2,iebc):
  x1 = (i-0.5)*dx
  x2 = (i-1.5)*dx
  sigmax = bcfactor*(x1**(orderbc+1)-x2**(orderbc+1))
  ca1 = np.exp(-sigmax*dt/epsz)
  cb1 = (1-ca1)/(sigmax*dx)
  caeybcr[i,1:je] = ca1
  cbeybcr[i,1:je] = cb1
  caeybcf[i+iebc+ie,1:jebc] = ca1
  cbeybcf[i+iebc+ie,1:jebc] = cb1
  caeybcb[i+iebc+ie,1:jebc] = ca1
  cbeybcb[i+iebc+ie,1:jebc] = cb1
sigmax = bcfactor*(0.5*dx)**(orderbc+1)
ca1 = np.exp(-sigmax*dt/epsz)
cb1 = (1-ca1)/(sigmax*dx)
caey[ib-1,1:je] = ca1
cbey[ib-1,1:je] = cb1
caeybcf[iebc+ib,1:jebc] = ca1
cbeybcf[iebc+ib,1:jebc] = cb1
caeybcb[iebc+ib,1:jebc] = ca1
cbeybcb[iebc+ib,1:jebc] = cb1

for i in range(1,iebc):
  x1 = i*dx
  x2 = (i-1)*dx
  sigmax = bcfactor*(x1**(orderbc+1)-x2**(orderbc+1))
  sigmaxs = sigmax*(muz/epsz)
  da1 = np.exp(-sigmaxs*dt/muz)
  db1 = (1-da1)/(sigmaxs*dx)
  dahzxbcr[i,1:je]  =  da1
  dbhzxbcr[i,1:je]  =  db1
  dahzxbcf[i+ie+iebc,1:jebc] = da1
  dbhzxbcf[i+ie+iebc,1:jebc] = db1
  dahzxbcb[i+ie+iebc,1:jebc] = da1
  dbhzxbcb[i+ie+iebc,1:jebc] = db1
  caexbcr[i,2:je] = ca[0]
  cbexbcr[i,2:je] = cb[0]
  dahzybcr[i,1:je] = da[0]
  dbhzybcr[i,1:je] = db[0]

fig  =  plt.figure() # initialise la figure
image  =  plt.imshow(hz[1:,1:].T, 
          origin="lower", extent=[xmin,xmax,ymin,ymax], vmin = -0.2, vmax = 0.2, cmap=plt.cm.bwr)

# On peut une interpolation des couleurs mais cela ralentit la visualisation
#image  =  imshow(hz[1:,1:].T, interpolation="bicubic", 
#          origin="lower", extent=[xmin,xmax,ymin,ymax], vmin = -0.2, vmax = 0.2, cmap=plt.cm.bwr)

#***********************************************************************
#     BEGIN TIME-STEPPING LOOP
#***********************************************************************

def animate(n): 
  #***********************************************************************
  #     Update electric fields (EX and EY) in main grid
  #***********************************************************************

  ex[1:,2:je] = caex[1:,2:je]*ex[1:,2:je]+ \
             cbex[1:,2:je]*(hz[1:,2:je]-hz[1:,1:je-1])

  ey[2:ie,1:] = caey[2:ie,1:]*ey[2:ie,1:]+ \
             cbey[2:ie,1:]*(hz[1:ie-1,1:]-hz[2:ie,1:])

  #***********************************************************************
  #     Update EX in PML regions
  #***********************************************************************

  #     FRONT

  exbcf[1:,2:jebc] = caexbcf[1:,2:jebc]*exbcf[1:,2:jebc]- \
    cbexbcf[1:,2:jebc]*(hzxbcf[1:,1:jebc-1]+hzybcf[1:,1:jebc-1]- \
                        hzxbcf[1:,2:jebc]-hzybcf[1:,2:jebc])
  ex[1:ie,1] = caex[1:ie,1]*ex[1:ie,1]- \
    cbex[1:ie,1]*(hzxbcf[ibbc:iebc+ie,jebc-1]+ \
                  hzybcf[ibbc:iebc+ie,jebc-1]-hz[1:ie,1])
   
  #     BACK

  exbcb[1:,2:jebc-1] = caexbcb[1:,2:jebc-1]*exbcb[1:,2:jebc-1]- \
    cbexbcb[1:,2:jebc-1]*(hzxbcb[1:,1:jebc-2]+hzybcb[1:,1:jebc-2]- \
                          hzxbcb[1:,2:jebc-1]-hzybcb[1:,2:jebc-1])
  ex[1:ie,jb-1] = caex[1:ie,jb-1]*ex[1:ie,jb-1]- \
    cbex[1:ie,jb-1]*(hz[1:ie,jb-2]-hzxbcb[ibbc:iebc+ie,1]- \
                   hzybcb[ibbc:iebc+ie,1])
   
  #     LEFT

  exbcl[1:,2:je] = caexbcl[1:,2:je]*exbcl[1:,2:je]- \
    cbexbcl[1:,2:je]*(hzxbcl[1:,1:je-1]+hzybcl[1:,1:je-1]- \
                      hzxbcl[1:,2:je]-hzybcl[1:,2:je])
  exbcl[1:,1] = caexbcl[1:,1]*exbcl[1:,1]- \
    cbexbcl[1:,1]*(hzxbcf[1:iebc,jebc-1]+hzybcf[1:iebc,jebc-1]- \
                   hzxbcl[1:,1]-hzybcl[1:,1])
  exbcl[1:,jb-1] = caexbcl[1:,jb-1]*exbcl[1:,jb-1]- \
    cbexbcl[1:,jb-1]*(hzxbcl[1:,je-1]+hzybcl[1:,je-1]- \
                    hzxbcb[1:iebc,1]-hzybcb[1:iebc,1])
   
  #     RIGHT

  exbcr[1:,2:je] = caexbcr[1:,2:je]*exbcr[1:,2:je]- \
    cbexbcr[1:,2:je]*(hzxbcr[1:,1:je-1]+hzybcr[1:,1:je-1]- \
                      hzxbcr[1:,2:je]-hzybcr[1:,2:je])
  exbcr[1:,1] = caexbcr[1:,1]*exbcr[1:,1]- \
    cbexbcr[1:,1]*(hzxbcf[1+iebc+ie:iefbc,jebc-1]+ \
                   hzybcf[1+iebc+ie:iefbc,jebc-1]- \
                   hzxbcr[1:,1]-hzybcr[1:,1])
  exbcr[1:,jb-1] = caexbcr[1:,jb-1]*exbcr[1:,jb-1]- \
    cbexbcr[1:,jb-1]*(hzxbcr[1:,je-1]+hzybcr[1:,je-1]- \
                    hzxbcb[1+iebc+ie:iefbc,1]- \
                    hzybcb[1+iebc+ie:iefbc,1])
   
  #***********************************************************************
  #     Update EY in PML regions
  #***********************************************************************

  #     FRONT

  eybcf[2:iefbc,1:] = caeybcf[2:iefbc,1:]*eybcf[2:iefbc,1:]- \
    cbeybcf[2:iefbc,1:]*(hzxbcf[2:iefbc,1:]+hzybcf[2:iefbc,1:]- \
                         hzxbcf[1:iefbc-1,1:]-hzybcf[1:iefbc-1,1:])
   
  #     BACK

  eybcb[2:iefbc,1:] = caeybcb[2:iefbc,1:]*eybcb[2:iefbc,1:]- \
    cbeybcb[2:iefbc,1:]*(hzxbcb[2:iefbc,1:]+hzybcb[2:iefbc,1:]- \
                         hzxbcb[1:iefbc-1,1:]-hzybcb[1:iefbc-1,1:])
   
  #     LEFT

  eybcl[2:iebc,1:] = caeybcl[2:iebc,1:]*eybcl[2:iebc,1:]- \
    cbeybcl[2:iebc,1:]*(hzxbcl[2:iebc,1:]+hzybcl[2:iebc,1:]- \
                        hzxbcl[1:iebc-1,1:]-hzybcl[1:iebc-1,1:])
  ey[1,1:] = caey[1,1:]*ey[1,1:]- \
    cbey[1,1:]*(hz[1,1:]-hzxbcl[iebc-1,1:]-hzybcl[iebc-1,1:])
   
  #     RIGHT

  eybcr[2:iebc,1:] = caeybcr[2:iebc,1:]*eybcr[2:iebc,1:]- \
    cbeybcr[2:iebc,1:]*(hzxbcr[2:iebc,1:]+hzybcr[2:iebc,1:]- \
                        hzxbcr[1:iebc-1,1:]-hzybcr[1:iebc-1,1:])
  ey[ib-1,1:] = caey[ib-1,1:]*ey[ib-1,1:]- \
    cbey[ib-1,1:]*(hzxbcr[1,1:]+hzybcr[1,1:]- hz[ie-1,1:])


  #***********************************************************************
  #     Update magnetic fields (HZ) in main grid
  #***********************************************************************

  hz[1:ie,1:je] = dahz[1:ie,1:je]*hz[1:ie,1:je]+ \
                dbhz[1:ie,1:je]*(ex[1:ie,2:jb]-ex[1:ie,1:je]+ \
                                  ey[1:ie,1:je]-ey[2:ib,1:je])

  hz[isource,jsource] = source[n]


  #***********************************************************************
  #     Update HZX in PML regions
  #***********************************************************************

  #     FRONT

  hzxbcf[1:iefbc,1:] = dahzxbcf[1:iefbc,1:]*hzxbcf[1:iefbc,1:]- \
    dbhzxbcf[1:iefbc,1:]*(eybcf[2:ibfbc,1:]-eybcf[1:iefbc,1:])
   
  #     BACK
   
  hzxbcb[1:iefbc,1:] = dahzxbcb[1:iefbc,1:]*hzxbcb[1:iefbc,1:]- \
    dbhzxbcb[1:iefbc,1:]*(eybcb[2:ibfbc,1:]-eybcb[1:iefbc,1:])
   
  #     LEFT
   
  hzxbcl[1:iebc-1,1:] = dahzxbcl[1:iebc-1,1:]*hzxbcl[1:iebc-1,1:]- \
    dbhzxbcl[1:iebc-1,1:]*(eybcl[2:iebc,1:]-eybcl[1:iebc-1,1:])
  hzxbcl[iebc-1,1:] = dahzxbcl[iebc-1,1:]*hzxbcl[iebc-1,1:]- \
    dbhzxbcl[iebc-1,1:]*(ey[1,1:]-eybcl[iebc-1,1:])
   
  #     RIGHT
   
  hzxbcr[2:iebc,1:] = dahzxbcr[2:iebc,1:]*hzxbcr[2:iebc,1:]- \
    dbhzxbcr[2:iebc,1:]*(eybcr[3:ibbc,1:]-eybcr[2:iebc,1:])
  hzxbcr[1,1:] = dahzxbcr[1,1:]*hzxbcr[1,1:]- \
    dbhzxbcr[1,1:]*(eybcr[2,1:]-ey[ib-1,1:])
   
  #***********************************************************************
  #     Update HZY in PML regions
  #***********************************************************************

  #     FRONT
   
  hzybcf[1:,1:jebc-1] = dahzybcf[1:,1:jebc-1]*hzybcf[1:,1:jebc-1]- \
    dbhzybcf[1:,1:jebc-1]*(exbcf[1:,1:jebc-1]-exbcf[1:,2:jebc])
  hzybcf[1:iebc,jebc-1] = dahzybcf[1:iebc,jebc-1]*hzybcf[1:iebc,jebc-1]- \
    dbhzybcf[1:iebc,jebc-1]*(exbcf[1:iebc,jebc-1]-exbcl[1:iebc,1])
  hzybcf[iebc+1:iebc+ie,jebc-1] =  \
    dahzybcf[iebc+1:iebc+ie,jebc-1]*hzybcf[iebc+1:iebc+ie,jebc-1]- \
    dbhzybcf[iebc+1:iebc+ie,jebc-1]*(exbcf[iebc+1:iebc+ie,jebc-1]- \
                                    ex[1:ie,1])
  hzybcf[iebc+ie+1:iefbc,jebc-1] =  \
    dahzybcf[iebc+ie+1:iefbc,jebc-1]*hzybcf[iebc+ie+1:iefbc,jebc-1]- \
    dbhzybcf[iebc+ie+1:iefbc,jebc-1]*(exbcf[iebc+ie+1:iefbc,jebc-1]- \
                                     exbcr[1:iebc,1])

  #     BACK
   
  hzybcb[1:iefbc,2:jebc] = dahzybcb[1:iefbc,2:jebc]*hzybcb[1:iefbc,2:jebc]- \
    dbhzybcb[1:iefbc,2:jebc]*(exbcb[1:iefbc,2:jebc]-exbcb[1:iefbc,3:jbbc])
  hzybcb[1:iebc,1] = dahzybcb[1:iebc,1]*hzybcb[1:iebc,1]- \
    dbhzybcb[1:iebc,1]*(exbcl[1:iebc,jb-1]-exbcb[1:iebc,2])
  hzybcb[iebc+1:iebc+ie,1] =  \
    dahzybcb[iebc+1:iebc+ie,1]*hzybcb[iebc+1:iebc+ie,1]- \
    dbhzybcb[iebc+1:iebc+ie,1]*(ex[1:ie,jb-1]-exbcb[iebc+1:iebc+ie,2])
  hzybcb[iebc+ie+1:iefbc,1] =  \
    dahzybcb[iebc+ie+1:iefbc,1]*hzybcb[iebc+ie+1:iefbc,1]- \
    dbhzybcb[iebc+ie+1:iefbc,1]*(exbcr[1:iebc,jb-1]- \
                                  exbcb[iebc+ie+1:iefbc,2])
   
  #     LEFT
   
  hzybcl[1:,1:je] = dahzybcl[1:,1:je]*hzybcl[1:,1:je]- \
    dbhzybcl[1:,1:je]*(exbcl[1:,1:je]-exbcl[1:,2:jb])
   
  #     RIGHT
   
  hzybcr[1:,1:je] = dahzybcr[1:,1:je]*hzybcr[1:,1:je]- \
    dbhzybcr[1:,1:je]*(exbcr[1:,1:je]-exbcr[1:,2:jb])

  #***********************************************************************
  #     Visualize fields
  #***********************************************************************

  image.set_data(hz[1:,1:].T)
  return image,
 
  #***********************************************************************
  #     END TIME-STEPPING LOOP
  #***********************************************************************

ani  =  animation.FuncAnimation(fig, animate, frames = nmax, blit = True, interval = 1, repeat = False)

plt.show()






