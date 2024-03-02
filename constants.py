import numpy as np
import math

WORKSPACE_LIMITS = np.asarray([[0.276, 0.724], [-0.224, 0.224], [-0.0001, 0.4]])

# image
PIXEL_SIZE = 0.002
IMAGE_SIZE = 224