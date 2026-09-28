<p align="center">
  <img src="app/static/relo_logo_slogan.png" width="400" height="220">
</p>

# Description
Team Members: Amelia Bell, Michael Bodie, Aravinda Dassanayake, Joseph Janicki, Riesling Meyer, Nathan Smooha

Contents of File:
*Instructions
*Data Collection
*Data Cleaning
*Data Integration
*Analysis
*Visualization

## Instructions

The following are instructions to run the FULL app with all prepared clusters. Note that this takes 16-20 GB of RAM to run. The file `README.txt` describes how to run a Docker image that was prepared with pared down data (only ~3 GB required).

The following process only works on MacOS and Linux (tested with Ubuntu 20.04) installations. Dependencies for some requirements are not easily installed on Windows. If you are using Windows, we strongly recommend using the Docker image instead. You can see how the Docker image was prepared by referring to `build_submissions_and_demo.py`


1. Install Anaconda (3.8) Python Distribution
2. Run `conda create -n project python=3.7.9`
3. Run `conda activate project`
4. Run `pip install -r requirements.txt`
5. From app folder, run `python flask_app.py`

---

## Approaches

### Data Collection
#### Census Data
1. The Census data used was obtained from the 5-year American Community Survey Responses for 2018 via data.census.gov. The data was found using an interface to first view the data table needed, then column selection was customized. All "tract" geographies were selected for all states, and the resulting data table was downloaded into a zip folder from where the csv file was extracted. We identified eight tables that contained columns relevant to our project for clustering and visualization.

2. Gazetteer Data: 2018 Census Gazetteer file holds geographical information necessary for performing data integration with the amenities data. This data maps the "center" (not necessarily the geometric center) of each Census tract to a latitude and longitude coordinate, and it also includes estimates for the land and water areas in each tract. This data was gathered via a direct download from the following link, and it was prepared into geoJSON format via Python. (https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2018_Gazetteer/2018_Gaz_tracts_national.zip)

3. All Census data was then read into Python dataframes and written to pickle files to be utilized for further data processing.


#### Amenities Data
1. A Python script was used to make API calls to the Foursquare Places API. Prior to making the API calls, the code takes in a list of states (in the continental USA) and returns a list of zip codes. For each zip code, an API call is then made to the "venues" API endpoint with the category type parameter set to the amenity type in question (https://developer.foursquare.com/docs/api-reference/venues/search/). The returned data is then checked for completeness, and stored in a CSV file per state. Once all states' data is retrieved, the script performs a merge across all state level CSV files to consolidate all in to a single CSV file. To obtain the necessary data, this process was executed on each of the following amenities: grocery stores, gyms, parks (local only, state and national excluded), harware stores, and medical facilities.

#### Locations

* Raw census data: `/raw_data/census_tables`
* Census data description: `/docs/Census Data Gathering and Prep.docx`
* Census data preparation code: `/data/etl_scripts/2018_5Yr_ACS/01_process_data.census.gov_downloads__v4.ipynb`
* Census tract shape data preparation code: `/data/etl_scripts/census_tract_geojson_prep/prepare_census_tract_geojson.ipynb`
* Census tract raw shape data: `/raw_data/census_tract_geometries`
* Census tract prepared shape data: `/data/shape_data/all_census_tract_shapes.json.gz`
* Amenities scraping code: `/data/amenities/data-import/` (NOTE: See the README_AMENITIES.md in this folder for additional info on the scraping process.)
* Amenities raw data: `/data/amenities/source-data`


### Data Cleaning
#### Census Data
1. Initial Steps: Each column was evaluated for relevance, based on the column name. An initial list was narrowed down to the columns that were deemed vital to keep. As necessary, ad-hoc histograms were created in Python to evaluate the data setup, completeness, range, etc.

2. A Python script was created to read in the raw data, and a new dataframe was generated for the columns that did not need further alteration. Those columns that required transformation (i.e. to be transformed into a percentage of the total) were calculated and added to the aforementioned dataframe. Any calculation errors were corrected, and the initially cleaned data was written to a pickle file for later integration with the amenities data for visualization use. The data was then evaluated for nulls, and records with a high count of nulls were removed. The remaining data was then truncated to 3 standard deviations from the mean, and any remaning nulls were imputed with the mean of their respective column. Columns were evaluated for skewness, and a Box-Cox transformation was performed on highly skewed or non-normal columns. The data was then standardized using the StandardScaler from scikit-learn. Finally, a profile was created for the fully processed data, and the dataset was written to a pickle file for later integration with amenities data for clustering.


#### Amenities Data
1. Initial Steps: A consolidated CSV file for a specific amenity was loaded into OpenRefine, and the latitude and longitude was truncated to be of equal length. The names of entities associated with the amenity were then grouped by similarity and converted to the appropriate one. Addresses were clustered and duplicates were removed. Finally, the entitiy names were evaluated in multiple ways using text facets to identify and remove any records that appeared to be different than the amenity in question.

#### Locations

* Cleaning steps performed in OpenRefine for Amenities data: `/data/amenities/openrefine-cleaning/`
* Amenities processed dataframes: `/data/amenities/dataframes/`
* Census data cleaning code: `/data/etl_scripts/data_cleaning/`
* Prepared Census data features profile: `/data/features/Census_Data_Profile_v4_Prelim_Cleaned_v4.html`
* Prepared Amenities data features profile: `/data/features/Amenities_Features_Profile*`

### Data Integration
#### Census Geography & Amenities
1. The data for each amenity was joined with the Census geography data based on the latitude and longitude of the locations associated with a specific amenity category. For each Census tract, the number of venues of a specific amenity category were counted within 2, 5, 10, 25, and 50 miles of the center and placed into distinct columns. The location counts in these columns were weighted by the inverse of the search radius. To calculate the distance, the following algorithm was applied: 1) project the coordinate system onto a 2D plane; 2) build a KDTree of all the amenity’s points; 3) iterate through Census tracts and use a tract’s center as a query to the KDTree, along with the distance limit.

2. The process above was performed for each amenity category. The resulting data had the Census GEOID, the latitude and longitude for the Census tract, and the distinct weighted count columns for every amenity category (e.g., the weighted count of grocery stores within 2 miles, 5 miles, etc.). The dataframe was then written to a pickle file for further data wrangling.

3. Post Integration & Summarization with Census Geography Data: A Python script loaded the pickle file containing the amenities data with the weighted count columns. The data was initially profiled for evaluation of completeness and skewness. All feature columns were found to be skewed or non-normal. So, for all feature columns, zeroes were replaced with the next lowest value, a Box-Cox transformation was performed on each, and the data was then standardized.


#### Clustering and Visualization Datasets
1. Clustering Data: Per discussion with the project team, the only amenities columns that were deemed necessary to retain for clustering were those related to the weighted count of locations within 25 miles of a Census tract center. Via a Python script, the pickle file with the cleaned, transformed, and standardized Census data was read into a dataframe. This data was then merged with the final dataframe containing the cleaned, transformed, and standardized amenities data subset on the GEOID field. The resulting dataframe was then saved to a pickle file to be used in our cluster model analysis.

2. Visualization Data: Via a Python script, the pickle file with simply the cleaned Census data was read into a dataframe. It was then merged with the entire amenities dataset (post integration & summarization with Census Geography Data) on the GEOID field. The final dataframe was then written to a pickle file to be used in the final visualization.

#### Locations

* Code to process cleaned amenities data into features and for use with visualization: `/data/etl_scripts/amenities/amenities_prep_generalized.ipynb`
* Amenities data prepared as feature inputs for integration to clustering model: `/data/amenities/amenities_features.pkl`
* Amenities data prepared for visualization: `/data/amenities/amenities_25mi_for_vis.pkl.gz` and `/data/amenities/amenities_full.pkl.gz`
* Final Clustering Dataset: `/data/features/Final_Clustering_Input_Data.pkl`
* Final Visualization Dataset: `/data/features/Final_Visualization_Input_Data.pkl`


### Analysis
#### Dimensionality Reduction 
1. Principal Component Analysis (PCA) was performed on the Census and amenities data that was prepared for clustering. The data was transformed to have only 18 components, which accounted for 95%  of the variability. After PCA, t-Distributed Stochastic Neighbor Embedding (t-SNE) decomposition was applied to the transformed data. t-SNE was chosen due to it being well suited for the visualization of high-dimensional data. t-SNE is a probabilistic technique that minimizes the divergence between two distributions. We used two-dimensional embeddings as features, which reduced the time to fit the different clustering models and allowed for better visualization of the clustering results.

#### Model Evaluation and Construction
1. Multiple clustering algorithms were first tested on a subset of the data. To quickly test density-based and grid-based approaches, we tried to generate clusters using the DBSCAN and OPTICS algorithms with default parameters. Both models simply returned the single structure in the visualization as one cluster. Thus, density-based and grid-based approaches were disregarded. 

2. We were left to choose methods from partitioning and hierarchical approaches. We needed to select algorithms that were scalable based on the number of samples in our dataset, the number of clusters that could be produced, and the size of the generated clusters. In addition, the algorithms needed to perform well on flat geometry. After reviewing the literature, we decided to further evaluate the following algorithms: KMeans, Mini-Batch KMeans, and Spectral (Partitioning); Ward Agglomerative and BIRCH (Hierarchical).

3. To choose the correct number of clusters, we compared relevant internal validity measures with the load times of our visualization tool. Ultimately, we selected 50 clusters for all the algorithms we tested in order to improve the user experience of our tool.

4. We evaluated the Silhouette, Calinski-Harabasz, and Davies-Bouldin internal validity measures to determine the best clustering method with 50 clusters for our dataset. Based on the results, the best option was deemed to be the KMeans algorithm with 50 clusters. Again, this was determined by looking at both algorithm and visualization performance.

5. After retrieving the clustering labels from our final model, we wanted to determine the variables that accounted for the greatest differences between the various clusters. We grouped the data points based on the generated clusters, and we retrieved the mean value for each feature. Then, we calculated the variance of means between clusters within each feature, and we selected the top 7 with the highest variance.

#### Locations

* Clustering Model Testing: `/model/Clustering_Model_Testing.ipynb`
* Main Clustering Pipeline: `/model/Clustering_Pipeline.ipynb`
* Clustering Pipeline (50 Clusters): `/model/Clustering_Pipeline-rerun_with_uniform_optimal_clusters.ipynb`
* Clustering Model Outputs (50 Clusters): `/model/*.obj`
* Final clustering and ranking output: `/data/cluster_model_output/clusters_and_ranks.pkl`


### Visualization
#### Application
1. Results are visualized in a web-application, which was created using Python Flask. Users first enter an address in an area they like. The tool then identifies the Census tract that has its center point closest to the inputted address. It then gathers the cluster grouping in which that Census tract resides. The visualization shows all of the Census tracts in the cluster on a map of the continental US. Furthermore, the returned Census tracts are ranked according to their Euclidean distance in the feature space from the identified tract. The top 3 ranked locales are displayed in the tool, and the user may select any one of them. Upon selection, the map zooms into the chosen tract, and the amenities within the area are shown. Likewise, feature comparisons are displayed that showcase how closely the tract of the inputted address matches the selected tract.

#### Locations

* Flask application: `/app/flask_app.py`
* Module for visualizations used by flask_app: `/app/clustervis.py`
