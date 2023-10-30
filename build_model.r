# Script to build data-driven models based on rater responses
# original code by Ron Dotsch (rdotsch@gmail.com) circa 2012-2018
#
# comments and minor edit by DongWon Oh (dongwonohphd@gmail.com) 2023
#
# In this example we extract models named CV1, CV2, CV3, CV4, CV5,
# CV1_PCA, and CV2_PCA (what these models represent do not matter for
# the purpose of the model buildilng demonstration here, but for those curious:
# refer to Todorov & Oh 2022 Advances in Experimental Social Psychology (AESP)
# to learn more about these models)

# Load necessary libraries (if loading an Excel file)
library(gdata)

# Set working directory to wherever you're running this script from
setwd('/path/')

# Read your csv or Excel file containing human responses (e.g., ratings)
# and FaceGen faces' coordinates
df <- read.xls('/path/to/excel/file/faces.xlsx')

# Extract responses (in this case, ratings) into a list
ratings <- list(
  CV1 = df %>% select(fn,CV1),
  CV2 = df %>% select(fn,CV2),
  CV3 = df %>% select(fn,CV3),
  CV4 = df %>% select(fn,CV4),
  CV5 = df %>% select(fn,CV5),
  CV1_PCA = df %>% select(fn,CV1_PCA),
  CV2_PCA = df %>% select(fn,CV2_PCA)
)

# Extract face coordinates of stimuli into another list
coords <- list (
  CV1 = df %>% select(ss0:ss49,st0:st49),
  CV2 = df %>% select(ss0:ss49,st0:st49),
  CV3 = df %>% select(ss0:ss49,st0:st49),
  CV4 = df %>% select(ss0:ss49,st0:st49),
  CV5 = df %>% select(ss0:ss49,st0:st49),
  CV1_PCA = df %>% select(ss0:ss49,st0:st49),
  CV2_PCA = df %>% select(ss0:ss49,st0:st49)
)
 
## Build models
# Initialize a data frame for storing models
models <- data.frame()

# Process ratings and coordinates data
for (i in names(ratings)) {
  
  # Rename coordinates columns and throw away useless columns from coords
  co <- coords[[i]]
  names(co) <- paste0('D', 1:100)
  
  ra <- ratings[[i]]
  
  # Combine ratings with corresponding coordinates
  merged <- merge(ra, co)
  
  # Compute reverse correlation by trait
  # For details, refer to Oosterhof & Todorov 2008 PNAS or
  # Todorov & Oh 2022 AESP
  for (trait in names(ra[2:ncol(ra)])) {
    m <- crossprod(scale(as.matrix(merged[, trait]), scale=F), 
                   as.matrix(merged[, (ncol(ra)+1):ncol(merged)]))
    m <- m / norm(m)
    models <- rbind(models, data.frame(i, m))
  }
}

# Save the constructed models to a CSV
names(models)[1] <- "CV models"
write.csv(models,file="CV_models.csv",row.names=F,quote=F)


## Calculate orthogonal projections of each identity on each individual social dimension
# Load the social dimensions data
socialDimensions <- read.csv(file='si-todorov.csv', header=F)
row.names(socialDimensions) <- socialDimensions[,1]
socialDimensions <- as.matrix(socialDimensions[,2:length(socialDimensions)])

# Define functions to calculate orthogonal projections for shape and texture 
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

projectionsShape <- matrix(0, nrow(models), dim(socialDimensions)[1])
projectionsTexture <- matrix(0, nrow(models), dim(socialDimensions)[1])

# Calculate orthogonal projections for all identities across all social dimensions
for (d in 1:dim(socialDimensions)[1]) {
  for (i in 1:nrow(models)) {  
    
    projectionsShape[i, d] <- projectShape(as.matrix(models[i,3:102]), socialDimensions[d,])
    projectionsTexture[i, d] <- projectTexture(as.matrix(models[i,3:102]), socialDimensions[d,])
  }
}

projectionsShape <- as.data.frame(projectionsShape)
names(projectionsShape) <- row.names(socialDimensions)

projectionsTexture <- as.data.frame(projectionsTexture)
names(projectionsTexture) <- row.names(socialDimensions)
  
# Adjust column names and data format as needed
rownames(models)[1] <- 'modelname'

# if necessary
models <- models[-2:-1]
socialDimensions <- as.data.frame(socialDimensions)
names(socialDimensions) <-  paste0('D', 1:100)

# Compute and display correlation matrix
round(cor(t(rbind(socialDimensions,models))),2)

# Save the final models data to a CSV
write.csv(models, 'models.csv', row.names=F)
