import re
import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt

time = sys.argv[1] if len(sys.argv) > 1 else "146"

# Solid interface temperature, x = 1.0
with h5py.File("solid/output/fenicsx_solid_data.h5") as f:
    xyz = f["Mesh/mesh/geometry"][:]
    steps = f["Function/f"]
    key = min(steps, key=lambda k: abs(float(k.replace("_", ".")) - float(time)))
    T_solid = steps[key][:, 0]

on_iface = np.isclose(xyz[:, 0], 1.0)
y_solid, inverse = np.unique(np.round(xyz[on_iface, 1], 8), return_inverse=True)
T_iface = np.bincount(inverse, T_solid[on_iface]) / np.bincount(inverse)

# Fluid received values, rightWall faces
text = open(f"fluid/{time}/T").read()
block = text[text.index("rightWall"):]
values = re.search(r"\bvalue\s+nonuniform List<scalar>\s*\d+\s*\(([^)]*)\)", block).group(1)
T_fluid = np.array(values.split(), dtype=float)
y_fluid = (np.arange(len(T_fluid)) + 0.5) / len(T_fluid)

# What nearest neighbour would give
T_nearest = T_iface[np.abs(y_solid[None, :] - y_fluid[:, None]).argmin(axis=1)]

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.plot(y_solid, T_iface, "o-", color="tab:blue", label="Solid interface temperature")
ax.plot(y_fluid, T_nearest, "s--", color="tab:grey", mfc="none", label="Nearest neighbour (illustration, not a run)")
ax.plot(y_fluid, T_fluid, "x", color="tab:red", ms=10, mew=2.5, label=f"Fluid received, RBF ({len(y_fluid)} faces)")
ax.set_xlabel("y along interface (m)")
ax.set_ylabel("Temperature (K)")
ax.set_title(f"Solid to fluid transfer at t = {time} s, non-matching meshes")
ax.ticklabel_format(axis="y", useOffset=False)
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("interface.png", dpi=150)
plt.show()
