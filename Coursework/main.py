import numpy as np
import matplotlib.pyplot as plt

from solverHighBoundaryTemp import solve_heat2d

N, M = 200, 5000
L = 1
max_time = 10.0

x = np.linspace(-L, L, N, dtype=np.float32)
y = np.linspace(-L, L, N, dtype=np.float32)
time = np.linspace(0, max_time, M, dtype=np.float32)

u, center_temperature = solve_heat2d(x, y, time, sigma=1.0)

fig = plt.figure(figsize=(10,8))
xv, yv = np.meshgrid(x, y)
ax = plt.axes(projection='3d')
ax.plot_surface(xv, yv, u[1], rstride=1, cstride=1, cmap='viridis', edgecolor='none')

ax.set_title('')
ax.set_zlim((0,1))
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('u')
ax.view_init(40,30)

plt.figure(figsize=(8,6))
cs = plt.contourf(xv, yv, u[-1], 15)

plt.colorbar(cs)
plt.gca().set_aspect('equal')

from scipy.optimize import curve_fit

def func(t, a):
    return np.exp(a * t)

popt, _ = curve_fit(func, time, center_temperature)

plt.figure()
plt.plot(time, center_temperature, label='Original')
plt.plot(time, np.exp(popt[0] * time), label=f'Fitted with {popt[0]:.2f}')
plt.yscale('log')
plt.xlabel('time')
plt.ylabel('T')
plt.title('Maximum temperature')
plt.grid()
plt.legend()
plt.show()