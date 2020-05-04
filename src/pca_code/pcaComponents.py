import numpy as np
from sklearn.decomposition import PCA


# takes in raw data then calculates the (by default 2) most significant components
# and saves them to a file. only needs to be run once on a data set unless the
# the data set gets updated
def genComponents(data, compCount = 2 , path = "components"):

	pca = PCA(n_components=compCount)
	pca.fit(data)
	np.save(path,pca.components_)
	return pca

	# print(pca.explained_variance_ratio_)
	# print(pca.singular_values_)
	# print(pca.components_)
	# print(pca.transform([[-0.83849224, -0.54491354]]))


# takes in a specific data point (typically a test point that you want to classify)
# then returns the projection onto the components from genComponents
def calcCovariance(x, path = "components.npy"):
	components = np.load(path)
	print(np.dot(components,x).astype(int))
	return np.dot(components,x)

def main():
	X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])

	print(np.array([	[-0.83849224, -0.54491354], 
						[ 0.54491354, -0.83849224], 
						[2*-0.83849224, 2*-0.54491354]]).T)

	pca = genComponents(X)

	calcCovariance(np.array([	[-0.83849224, -0.54491354], 
								[ 0.54491354, -0.83849224], 
								[2*-0.83849224, 2*-0.54491354]]).T)

if __name__ == "__main__":
    main()