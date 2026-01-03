import math

import numpy as np
import pyvista as pv

MATRICULA = 202210504463

# ------------------------------------------------------------
# Parâmetros físicos
# ------------------------------------------------------------
eps_0 = 8.854e-12
eps_g = eps_0
eps_d = 5 * eps_0

r_a = 13.5e-3
r_d = 14.8e-3
r_b = 18e-3

L = 20e-2

V_0 = 10e3

geometric_factor = eps_g / (
    eps_g * math.log(r_d / r_a)
    +
    eps_d * math.log(r_b / r_d)
)

# ------------------------------------------------------------
# Geometria do cilindro
# ------------------------------------------------------------
density = 0.15   # distância mínima entre vetores

N_r = int(R / density)
N_theta = int(2*np.pi*R / density)
N_z = int(L / (2*density))

r     = np.linspace(0, R, N_r)
theta = np.linspace(0, 2*np.pi, N_theta)
z     = np.linspace(-L/2, L/2, N_z)

rr, tt, zz = np.meshgrid(r, theta, z, indexing="ij")
x = rr * np.cos(tt)
y = rr * np.sin(tt)
z = zz

x = x.flatten()
y = y.flatten()
z = z.flatten()

eps = 1e-6
mask = np.sqrt(x*x + y*y) > eps

x = x[mask]
y = y[mask]
z = z[mask]

# ------------------------------------------------------------
# Cálculo de E_r(r,z) e E_z(r, z)
# ------------------------------------------------------------
r = np.sqrt(x*x + y*y)
r[r == 0] = 1e-12

term1 = (z + L/2) / np.sqrt(r**2 + (z + L/2)**2)
term2 = (z - L/2) / np.sqrt(r**2 + (z - L/2)**2)
Er = (V_0 * geometric_factor) / (2 * r) * (term1 - term2)

Ez = -(V_0 * geometric_factor) / (2 * r) * (
    r**2 / (r**2 + (z + L/2)**2)**1.5
    -
    r**2 / (r**2 + (z - L/2)**2)**1.5
)

# Vetor radial
Ex = Er * (x / r)
Ey = Er * (y / r)

vectors = np.vstack((Ex, Ey, Ez)).T
points  = np.vstack((x, y, z)).T

# ------------------------------------------------------------
# PREVINIR FLECHAS GIGANTES:
# Normalizar vetores e mostrar magnitude apenas na cor
# ------------------------------------------------------------
mag = np.linalg.norm(vectors, axis=1)
mag[mag == 0] = 1e-12
vectors_unit = vectors / mag[:,None]   # << DIREÇÃO SOMENTE <<

# ------------------------------------------------------------
# Plot com tamanho de seta constante
# ------------------------------------------------------------
pv.close_all()
plotter = pv.Plotter()
plotter.clear()

cloud = pv.PolyData(points)
cloud["vectors"] = vectors_unit
cloud["mag"] = mag                  # coloração

glyphs = cloud.glyph(
    orient="vectors",
    scale=False,     # <<--- TAMANHO FIXO
    factor=0.15,      # <<--- AJUSTE O TAMANHO AQUI
)

plotter.add_mesh(glyphs, scalars="mag", cmap="viridis")

# Cilindro transparente
cyl = pv.Cylinder(center=(0,0,0), direction=(0,0,1), radius=R, height=L)
plotter.add_mesh(cyl, color="white", opacity=0.1)

plotter.add_axes()
plotter.show()
