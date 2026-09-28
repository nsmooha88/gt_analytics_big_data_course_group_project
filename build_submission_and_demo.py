import os
import sys
import shutil
import pandas as pd


"""
This script is used to build
(1) The Canvas submission folder (with all data removed)
(2) The pared down version of the repo with data limited to 1 cluster + the docker app build
(3) The full repo that is uploaded to Google Drive that includes all of the data. 
"""

################################################################################
# Prepare canvas submission of just code + docs
################################################################################

################################################################################
################################################################################
DEST = './00_CANVAS_SUBMISSION/team046final/'
CODE_DEST = os.path.join(DEST, 'CODE')
DOC_DEST = os.path.join(DEST, 'DOC')
################################################################################
################################################################################

# If destination directory exists, prompt if OK to delete
# If not OK, exit
if os.path.exists(DEST):
    print('\n\n\nDestination already exists: {}. '.format(DEST))
    resp = input('Okay to delete? y/[n]: ').strip().lower()
    if resp not in ('y', 'yes'):
        print('Exiting...')
        sys.exit(1)
    # delete existing directory and start from scratch    
    os.system('rm -rf {}'.format(DEST))

# make destination directory
os.makedirs(DEST)
os.makedirs(CODE_DEST)
os.makedirs(DOC_DEST)

# copy relevant folders
for folder in ('app', 'data', 'docs', 'model', 'raw_data'):
    shutil.copytree(folder, os.path.join(CODE_DEST, folder))

# copy relevant files
for f in ('README.md', 'requirements.txt', 'Dockerfile', 'boot.sh', 'environment.yml', 'build_submission_and_demo.py'):
    shutil.copy(f, CODE_DEST)
    
# copy README.txt next to CODE folder
shutil.copy('README.txt', DEST)    
    
# delete unnecessary files/folders. delete data sets.
for item in ('.DS_Store', '__pycache__', '.vscode', '.ipynb_checkpoints',
             'source-data', 'Final_Visualization_Input_Data.zip', 
             '*.gz', '*.pkl', '*.csv', '*.obj', '*.csv', '*.json', '*.zip'):
    os.system('find {} -name {} | xargs rm -rf'.format(DEST, item))

print('Done with submission folder.')






################################################################################
# Prepare demo project
################################################################################


################################################################################
################################################################################
DEST = './00_DEMO_APP'#'./team046final'
CODE_DEST = DEST
DEMO_DEST = os.path.join(CODE_DEST, 'DEMO')
################################################################################
################################################################################


# If destination directory exists, prompt if OK to delete
# If not OK, exit
if os.path.exists(DEST):
    print('Destination already exists: {}. '.format(DEST))
    resp = input('Okay to delete? y/[n]: ').strip().lower()
    if resp not in ('y', 'yes'):
        print('Exiting...')
        sys.exit(1)
    # delete existing directory and start from scratch    
    os.system('rm -rf {}'.format(DEST))

# make destination directory
os.makedirs(DEST)
os.makedirs(DEMO_DEST)


# copy relevant folders
for folder in ('app', 'data', 'docs', 'model'):
    shutil.copytree(folder, os.path.join(CODE_DEST, folder))

# copy relevant files
for f in ('README.md', 'requirements.txt', 'Dockerfile', 'boot.sh', 'environment.yml'):
    shutil.copy(f, CODE_DEST)
    
# delete unnecessary files/folders
for item in ('.DS_Store', '__pycache__', '.vscode', '.ipynb_checkpoints', 'source-data', 'Final_Visualization_Input_Data.zip', 'amenities_full.pkl.gz', 'data-import'):
    os.system('find {} -name {} | xargs rm -rf'.format(DEST, item))


# pick a few clusters and get all associated geoids
# this will be used to limit the copied datasets.
# limit cluster data to selected clusters
clusters = [29] #[3]
###
cluster_data_path = os.path.join(CODE_DEST, 'data/cluster_model_output/clusters_and_ranks.pkl')
###
df = pd.read_pickle(cluster_data_path)
df = df[df.cluster.isin(clusters)]
GEOIDS = [int(x) for x in df.GEOID.values.tolist()]
os.system('rm {}'.format(cluster_data_path))
df.to_pickle(cluster_data_path)

# limit datasets to matching geoids
PATHS = [
    ('data/amenities/dataframes/GROCERY.pkl', None),
    ('data/amenities/dataframes/GYMS.pkl', None),
    ('data/amenities/dataframes/HARDWARE.pkl', None),
    ('data/amenities/dataframes/MEDICAL.pkl', None),
    ('data/amenities/dataframes/PARKS.pkl', None),
    ('data/amenities/amenities_25mi_for_vis.pkl.gz', 'gzip'),
    #('data/amenities/amenities_full.pkl.gz', 'gzip'),
    ('data/amenities/amenities_features.pkl', None),
    ('data/gaz/2018_5yr_cendatagov_GAZ_v4.pkl', None),
    ('data/features/Final_Visualization_Input_Data.pkl', None),
    #('data/shape_data/all_census_tract_shapes.json.gz', 'gzip'),
]


print('REDUCING SIZE/CONTENTS OF DATAFRAMES')
for path, compression in PATHS:
    PATH_ = os.path.join(CODE_DEST, path)
    print(path)
    df = pd.read_pickle(PATH_, compression=compression)
    if not 'GEOID' in df.columns:
        print('Skipping {}'.format(path))
        continue
    
    df = df[df.GEOID.astype(int).isin(GEOIDS)]
    os.system('rm {}'.format(PATH_))
    df.to_pickle(PATH_, compression=compression)


# process the json data if needed


# change directories to DEST to build docker image
os.chdir(DEST)

# Build docker image
os.system('sudo docker build -t relodemo:latest .')

# After building, can run with e.g. sudo docker run -it -p 5000:5000 relodemo

# Export image a new "DEMO" folder
os.chdir('DEMO')

# save docker image
os.system("sudo docker save relodemo > relodemo.tar")

print('Done with demo app.')






################################################################################
# Prepare full app zip
################################################################################
os.chdir('../..')
################################################################################
################################################################################
DEST = './00_REPO_GDRIVE_UPLOAD/team046repo/'
################################################################################
################################################################################

# If destination directory exists, prompt if OK to delete
# If not OK, exit
if os.path.exists(DEST):
    print('\n\n\nDestination already exists: {}. '.format(DEST))
    resp = input('Okay to delete? y/[n]: ').strip().lower()
    if resp not in ('y', 'yes'):
        print('Exiting...')
        sys.exit(1)
    # delete existing directory and start from scratch    
    os.system('rm -rf {}'.format(DEST))

# make destination directory
os.makedirs(DEST)

# copy relevant folders
for folder in ('app', 'data', 'docs', 'model', 'raw_data'):
    shutil.copytree(folder, os.path.join(DEST, folder))

# copy relevant files
for f in ('README.md', 'requirements.txt', 'Dockerfile', 'boot.sh', 'environment.yml', 'build_submission_and_demo.py'):
    shutil.copy(f, DEST)

os.system('zip -r ./00_REPO_GDRIVE_UPLOAD/team046repo.zip {}'.format(DEST, DEST))

print('DONE!')


