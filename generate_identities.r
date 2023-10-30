# Script to generate identities that are maximally different from each other
# then get statistics on scores on social dimensions (actually, these scores are projections)
# original code by Ron Dotsch (rdotsch@gmail.com) and Alex Todorov
# 2012 in Nijmegen

# Set working directory to wherever you're running this script from
setwd("/path/to/faces/")

library(fields)
library(plyr)
library(psych)

##### Settings #####

# Set number of identities
nIdentities = 25
nSimulatedIdentities = 1000

# Set mean and standard deviations of normal distributions used to generate identities
mu = 0
sigma = 1

# Set scaling factor
scalingFactor = 0.5

# Set random number generator seed
set.seed(2)

##### Simulations #####

# Carry out simulations to get some sense of average euclidean distances of random face space coordinates
simulatedCoords <- matrix(rnorm(nSimulatedIdentities * 100, mean = mu, sd = sigma), nSimulatedIdentities, 100) * scalingFactor

# Get the Euclidean distance matrix for these coordinates
distances <- rdist(simulatedCoords)

# Display histogram of this matrix
hist(distances[lower.tri(distances)])

# On each step remove identities taht have the least average distance to all other identities, until those left with greatest distance
for (i in 1:(nSimulatedIdentities - nIdentities)) {

  # Compute average distances
  avgDistances <- rowMeans(distances)
  
  # Get identities with lowest average distances
  minAvgDistances <- avgDistances == min(avgDistances)
  
  # Remove those from the simulatedCoords matrix
  simulatedCoords <- simulatedCoords[!minAvgDistances,]
  
  # Recalcuate Euclidean distance matrix for surviving identities
  distances <- rdist(simulatedCoords)
  
  # Break out of loop if minimum number of identities reached
  if (dim(simulatedCoords)[1] <= nIdentities) break
}

# Show histogram of final coordinates distances
hist(distances[lower.tri(distances)])
hist(simulatedCoords)

#### Calculate scores for social dimensions ####

# Get social dimensions scores
socialDimensions <- read.csv(file='/path/to/si-todorov.csv', header=FALSE)
row.names(socialDimensions) <- socialDimensions[,1]
socialDimensions <- as.matrix(socialDimensions[,2:length(socialDimensions)])


# Calculate orthogonal projections of each identity on each individual social dimension
projectShape <- function(v, s) { 
  v <- v[1:50]
  s <- s[1:50]
  return(((v %*% s) / (s %*% s)))
}

projectTexture <- function(v, s) { 
  v <- v[51:100]
  s <- s[51:100]
  return(((v %*% s) / (s %*% s)))
}

projectionsShape <- matrix(0, nIdentities, dim(socialDimensions)[1])
projectionsTexture <- matrix(0, nIdentities, dim(socialDimensions)[1])


for (d in 1:dim(socialDimensions)[1]) {
  for (i in 1:nIdentities) {  

    projectionsShape[i, d] <- projectShape(simulatedCoords[i,], socialDimensions[d,])
    projectionsTexture[i, d] <- projectTexture(simulatedCoords[i,], socialDimensions[d,])
    
  }
}

projectionsShape <- as.data.frame(projectionsShape)
names(projectionsShape) <- row.names(socialDimensions)

projectionsTexture <- as.data.frame(projectionsTexture)
names(projectionsTexture) <- row.names(socialDimensions)

# Look at distributions
describe(projectionsShape)
describe(projectionsTexture)

# Write coordinates to file
write.table(round(simulatedCoords*1000), 'ids.csv',sep=',',col.names=F)

# Write projections to file
write.csv(projectionsShape, 'ids_projections_shape.csv')
write.csv(projectionsTexture, 'ids_projections_reflect.csv')

