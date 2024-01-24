##########################################################################################################################################################
#
#Currently, this seems to be the best working plotting script. It still needs an input datafile
#
##########################################################################################################################################################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib import cm
from matplotlib.cm import ScalarMappable

# Load data from file
data = np.loadtxt('ChiSquared.txt')  # Level energies outpu
#data = np.loadtxt('gs_properties.txt') # Ground state properties, such as momentums
#data = np.loadtxt('properties_2J=3.txt') # First 3/2+ properties, such as momentums

# Extract data columns
gamma = data[:, 0]
beta2 = data[:, 1]
values = data[:, 2]

# Create polar plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# Set theta limit to display only the first sector (0 to 60 degrees)
ax.set_thetamin(0)
ax.set_thetamax(60)

# In the case of chi squares
vmin = 200.  # Minimum value
vmax = 350.   # Maximum value


# Create a custom colormap with a specific number of colors
# Set the number of colors in the custom colormap
num_colors = 1024  # You can adjust this number
# Create a custom colormap using the 'jet' colormap as a base
custom_cmap = plt.get_cmap('jet', num_colors)
colors = custom_cmap(np.linspace(0., 1., num_colors))

# Plot the contour plot on the polar subplot
contour = ax.tricontourf(np.radians(gamma), beta2, values, cmap=ListedColormap(colors),levels=512, vmin=vmin, vmax=vmax, extend='neither')##To limit the z-axis values plotted
#contour = ax.tricontourf(np.radians(gamma), beta2, values, cmap=ListedColormap(colors),levels=512)
#contour = ax.tricontourf(np.radians(gamma_filtered), beta2_filtered, values_filtered, cmap=ListedColormap(colors), levels=512)


# Add a colorbar to the right of the plot
cbar = plt.colorbar(contour, label='Values', orientation='vertical', pad=0.2)
#plt.colorbar(ScalarMappable(norm=contour.norm, cmap=contour.cmap),ticks=range(int(vmin), int(vmax), 2))

# Customize the radial axes
ax.set_yticks([0.1, 0.2, 0.3, 0.4, 0.5])  # Adjust the radial ticks as per your data
ax.set_yticklabels(['0.1', '0.2', '0.3', '0.4', '0.5'])  # Label the radial ticks

# Customize the polar axis
ax.set_xticks([np.deg2rad(0.), np.deg2rad(10.), np.deg2rad(20.), np.deg2rad(30.), np.deg2rad(40.), np.deg2rad(50.), np.deg2rad(60.)])  # Adjust the polar ticks as per your data

# Set the title
plt.title("Ground state spin", fontsize=18, position=(0.5, 1.3), ha='center', va='center')

# Add labels to the polar plot
ax.set_xlabel(r"$\beta_2$", fontsize=18, labelpad=10)
ax.set_ylabel(r"$\gamma$ (degrees)", fontsize=18, labelpad=10, position=(0.9, 0.5), ha='center', va='center')


# Filter out the point (0, 0)
non_zero_indices = np.nonzero((gamma != 0) & (beta2 != 0))
gamma_filtered = gamma[non_zero_indices]
beta2_filtered = beta2[non_zero_indices]
values_filtered = values[non_zero_indices]
# Find the indices of the minimum value
min_index = np.argmin(values_filtered)
# Extract gamma and beta2 values at the minimum point
min_gamma = gamma_filtered[min_index]
min_beta2 = beta2_filtered[min_index]
# Mark the minimum point on the plot
ax.plot(np.radians(min_gamma), min_beta2, 'y*', markersize=10, markerfacecolor='yellow')  # 'y*' means yellow color, star marker
print('Minimum Chi^2=',min(values_filtered),' located at beta_2= ', min_beta2, ' gamma= ', min_gamma)


# Show the plot
plt.show()


