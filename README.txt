RELO: Relocation Made Easy

Contributors: Amelia Bell, Michael Bodie, Aravinda Dassanayake, Joseph Janicki, Riesling Meyer, Nathan Smooha

CONTENTS OF THE README
---------------------

 * Description
 * Installation
 * EXECUTION


DESCRIPTION
------------

Welcome to RELO: Relocation made Easy! RELO incorporates a clustering-based approach to find the best neighborhoods to live. While utilizing Census and amenities data, Relo is able to give people the confidence to relocate to a location they are sure to enjoy. 

Please note that the instructions found in this README file relate to running a demo of our application with a small (toy) dataset.

Every directory described in this README file is located in the main CODE folder. Due to large file sizes, all data files were excluded from the Canvas submission. The full repository for RELO (team046repo.zip), including all data files, can be downloaded from the following location: https://drive.google.com/drive/folders/1fLpTlLICH0b0PzTqubKvYd0obrnpSyfj?usp=sharing

For additional information regarding RELO, including instructions on how to run the full non-demo application, please refer to the README.md file in the 'CODE' folder: CODE/README.md 


MAIN DIRECTORY

The individual files in the 'main' directory of the CODE folder, except README.md, are used for setting up the environment and creating the Docker demo. All subfolders are described in the subsequent 'directory' sections.

Please refer to Diagram_0 below for more information about the structure of the 'main' directory of the CODE folder.

Diagram_0
├── CODE/
│   ├── app/
│   ├── data/
│   ├── docs/
│   ├── model/
│   ├── raw_data/
│   ├── boot.sh
│   ├── build_submission_and_demo.py
│   ├── environment.yml
│   ├── Dockerfile
│   ├── README.md
└── └── requirements.txt


APP DIRECTORY

The 'app' directory is used to store all code associated with the visual application for Relo. 

Inside the app directory, we have the following structure:

	The 'static' directory contains images and stylesheets used in the application. 

	The 'templates' directory contains the files used for building the front end UI. 

	Finally, the flask_app.py file is the main Python code for the application, which utilizes clustervis.py for data processing. 

Please refer to Diagram_1 below for more information about the structure of the 'app' directory. Note, the images that are stored in the 'static' directory are not included in the diagram below. 

Diagram_1
├── app/
│   ├── static/
│   │   │   ├── stylesheets
│   │   │   │ 	├── index_style.css
│   │   │   │ 	├── result.css
│   │   │   │ 	└── search_form.css
│   ├── templates/
│   │       ├── about.html
│   │       ├── index.html
│   │       └── search_results.html
│   ├── clustervis.py
└── └── flask_app.py


DATA DIRECTORY

The 'data' directory contains all scripts used for gathering the data. This includes data related to our clustering algorithm and ranking system.

The 'data' directory contains the following structure:
	
	The 'amenities' directory contains the content related to capture of amenities data. This includes the Foursquare location data capture script, raw data, OpenRefine data cleaning steps and intermediate processed data. 

	The 'cluster_model_output' directory contains the output data produced by 'Clustering_Pipeline.ipynb'.

	The 'etl_scripts' contains code related to ETL processes for the amenities and Census tracts data, including data retrieval, data cleaning, and data processing.

	The 'gaz' directory contains Census data.

	The 'shape_data' contains code relating to the shapes of the Census tracts.

Please refer to Diagram_2 below for more information about the structure of the 'data' directory. Note, the elements inside the directories are not displayed in the diagram. 

Diagram_2
├── data/
│   ├── amenities/
│   ├── cluster_model_output/
│   ├── etl_scripts/
│   ├── features/
│   ├── gaz/
└── └── shape_data/


DOCS DIRECTORY

The 'docs' directory contains files relating to flow charts and diagrams that help depict the structure of the project.

Please refer to Diagram_3 below for more information about the structure of the 'docs' directory.    

Diagram_3
├── docs/
│   ├── Census Data Gathering and Prep.docx
│   ├── Census_Data_Cleanup_Process.vsdx
│   ├── RELO Process Flow Diagram.odg
│   ├── RELO Process Flow Diagram.pdf
│   ├── Visual Component.docx
└── └── amenity-data-capture-approach.docx


MODEL DIRECTORY

The 'model' directory contains code related to the clustering pipeline and the generation and evaluation of various clustering models.

The 'Clustering_Model_Testing.ipynb' file contains the initial code that was used to test a wide variety of different clustering methods on a subset of our final processed dataset.

The 'Clustering_Pipeline.ipynb' file contains the primary code for the clustering pipeline. Using our entired processed dataset, we performed in-depth evaluations on five alogirthms: KMeans, Mini-Batch KMeans, Spectral, Hierarchical Ward, and Hierarchical Birch.

The 'Clustering_Pipeline-rerun_with_uniform_optimal_clusters.ipynb' file is practically identical to 'Clustering_Pipeline.ipynb', but it generated and evaluated five clustering models using each of the aforementioned algorithms and a parameter of 50 clusters for all.

Please refer to Diagram_4 below for more information about the structure of the 'model' directory.    

Diagram_4
├── model/
│   ├── Clustering_Model_Testing.ipynb
│   ├── Clustering_Pipeline-rerun_with_uniform_optimal_clusters.ipynb
└── └── Clustering_Pipeline.ipynb


RAW_DATA DIRECTORY

The 'raw_data' directory contains the raw Census data. 

Please refer to Diagram_5 below for more information about the structure of the 'raw_data' directory.    

Diagram_5
├── model/
│   ├── census_tables/
└── └── census_tract_geometries/2018/


INSTALLATION
------------

1. Check to ensure you have docker installed. If it is not installed, please install it. Once installed, start docker.
2. Use the following link: https://drive.google.com/drive/folders/1fLpTlLICH0b0PzTqubKvYd0obrnpSyfj?usp=sharing
	 - This link will bring you to the Docker image. Download the Docker image named relodemo.tar.


EXECUTION
----------------

Please follow the following steps to run the code:

1. Open a Powershell or Terminal window and navigate into the directory where the docker image was downloaded in the Installation section.
2. Run 'docker load -i relodemo.tar' (note, you may need to run as root/with sudo on linux/mac)
	 - Please note on some platforms, the text being printed to the terminal may freeze for a bit. You may press enter several times to avoid the delay.
3. Run 'docker run -it -p 5000:5000 relodemo' (note, you may need to run as root/with sudo on linux/mac)
4. In your Powershell or Terminal window, once you see "Running on http://0.0.0.0:5000/", navigate to localhost:5000 in your browser (NOT 0.0.0.0:5000) and begin using the app!

Note that the demo docker application has data limited to only a single cluster of neighborhoods to ensure that it will run on the grader's hardware.

The full application currently consumes >16GB of memory, which is why the decision was made to limit that data.
Although any address given to the app should work since the code locates the nearest neighborhood to the input address,
here are some sample addresses to try that fall within neighborhoods that appear in the demo cluster:
1) 300 Madison Ave, New York, NY
2) Inman park, Atlanta, GA
3) Chamberlain Park, Raleigh


DEMO VIDEO
----------------

A demo video that shows how to install and execute the tool can be found at the following link:
https://www.youtube.com/watch?v=fqh-CT0eUXo
