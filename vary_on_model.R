# Script vary faces on a model dimension by projecting on preset values (-3 to 3 SDs) 
# rather than added/subtracted value from original face values
# Note the difference from vary_on_model_add.R
#
# original code by Ron Dotsch (rdotsch@gmail.com) circa 2017
# modified by DongWon Oh (dongwonohphd@gmail.com) 2024

# System prerequisite: none

library(dplyr)
library(tidyr)
setwd("/path/to/FGBinTools/")    

# Read files
models <- read.csv('/path/to/models.csv', header=F)    
names(models) <- c('name', paste0('c', 1:100))
identities <- read.csv('/path/to/identities.csv', header=F)
names(identities)[1] <- 'name'

# Select relevant models
models <- models %>% filter(name %in% c('Particular Model 1','Particular Model 2'))    # you need this one particular social trait model

#############################
#### Compute projections ####
#############################
# Function to compute projection of v1 on v2
project <- function(v1, v2) {
  return(as.numeric((v1 %*% v2) / (v2 %*% v2)))
}

projections <- data.frame()

for (d in 1:nrow(models)) {
  model.label <- models[d, 1]
  model <- as.vector(as.matrix(models[d, 2:101]) * 1000)
  
  for (i in 1:nrow(identities)) {
    
    identity.label <- identities[i, 1]
    identity <- as.vector(as.matrix(identities[i, 2:101]))
    
    projections <- rbind(projections, data.frame(
      identity=identity.label, 
      trait=model.label, 
      projection.type='shape.and.texture',
      projection=project(identity, model)))
    
    projections <- rbind(projections, data.frame(
      identity=identity.label, 
      trait=model.label, 
      projection.type='shape.only',
      projection=project(identity[1:50], model[1:50])))
    
    projections <- rbind(projections, data.frame(
      identity=identity.label, 
      trait=model.label, 
      projection.type='texture.only',
      projection=project(identity[51:100], model[51:100])))
  }
}

projections <- projections %>% spread(trait, projection) 
#write.csv(projections, 'Projections.csv', row.names=F)   # saves what values each of the initial faces has on the social trait model


####################################
#### Select relevant identities ####
####################################

#### Select identities to manipulate ####
identities <- identities %>% filter(name %in% c('face1','face2'))

# For each identity, find the closest point in range, and move to that point (shape & texture)
range.shape = seq(from=-2,to=2,length.out=2)
range.texture = seq(from=2,to=-2,length.out=2)
points <- data.frame()

niter <- nrow(models) * nrow(identities) * length(range.shape)  
pb <- progress_estimated(niter)
for (d in 1:nrow(models)) {
  model.label <- models[d, 1]
  model <- as.vector(as.matrix(models[d, 2:101]) * 1000)
  for (i in 1:nrow(identities)) {
    
    identity.label <- identities[i, 1]
    identity <- as.vector(as.matrix(identities[i, 2:101]))
    
    #### Create trait variations of identities ####
    # Find closest point in range to projection (shape & texture)
    projection.shape <- project(identity[1:50], model[1:50])
    closest.point.in.range.shape <- which.min(abs(range.shape - projection.shape))
    
    projection.texture <- project(identity[51:100], model[51:100])
    closest.point.in.range.texture <- which.min(abs(range.texture - projection.texture))
    
    # Translate identity to that point to create the base.coordinate (shape & texture)
    base.coord.shape   <- identity[1:50]   + (  range.shape[closest.point.in.range.shape]   - projection.shape  ) * model[1:50]
    base.coord.texture <- identity[51:100] + (range.texture[closest.point.in.range.texture] - projection.texture) * model[51:100]
    
    # Create all points
    for (point in 1:length(range.shape)) {
      pb$tick()$print()
      point.coord <- cbind(base.coord.shape     + (range.shape[point]   - range.shape[closest.point.in.range.shape])     * model[1:50],
                           base.coord.texture   + (range.texture[point] - range.texture[closest.point.in.range.texture]) * model[51:100])
      point.coord <- data.frame(matrix(point.coord, nrow = 1))
      names(point.coord) <-paste0('c', 1:100)
      points <- rbind(points, cbind(data.frame(identity=identity.label,
                                               manipulated.trait=model.label,
                                               identity.point.shape  =closest.point.in.range.shape,
                                               identity.point.texture=closest.point.in.range.texture,
                                               point=point,
                                               projection.shape  = range.shape[point],
                                               projection.texture= range.texture[point]),
                                    round(point.coord))
                      )   
    }
  }
}
pb$stop()

# Write the resulting coordinates of identities after variation
write.csv(points, 'identities_outcome.csv', row.names=F)
