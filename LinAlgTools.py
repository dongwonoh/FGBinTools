# Linear Algebra Tools supporting FaceGen scripts
# by Ron Dotsch (rdotsch@gmail.com)

from numpy import *
from scipy.linalg import norm
	
def normalize(vec) :
	return vec / norm(vec)

# orthogonalizes vec2 to be orthogonal to vec1 within the 2D plane spanned by the two vectors; 
# translation of Nick Oosterhof's Java code to Python code
def orthogonalize(vec1, vec2) :
	weights = array([1.0, -1.0/dot(vec1, vec2)])
	weights = normalize(weights)
	orthovec = normalize((weights[0] * vec1) + (weights[1] * vec2))
	return (orthovec, weights)