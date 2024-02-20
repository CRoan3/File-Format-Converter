import glob
import sys
import os
import json
import re
import pandas as pd

#getting meta data (schema info)
def get_column_names(schemas, ds_name, sorting_key = 'column_position'):
    column_details = schemas[ds_name] #ds_name = dataset name
    columns = sorted(column_details, key = lambda col: col[sorting_key]) 	#sorting columns by specified sorting_key
    return [col['column_name'] for col in columns] #gives column names

#reading data from source files into dataframes
def read_csv(file, schemas):
    file_path_list = re.split('[/\\\]', file) 
    ds_name = file_path_list[-2] 	#getting dataset name
    columns = get_column_names(schemas, ds_name) 	#getting column names from schema for respective dataset
    df = pd.read_csv(file, names=columns) 	#creating dataframe by reading CSV file assigning column names
    return df

#Pandas df to json
def to_json(df, tgt_base_dir, ds_name, file_name):
    json_file_path = f'{tgt_base_dir}/{ds_name}/{file_name}'
    os.makedirs(f'{tgt_base_dir}/{ds_name}', exist_ok=True)
    df.to_json(
        json_file_path,
        orient='records',
        lines=True
    )

#driver function that invokes all prior functions - WITHOUT HARDCODING
def file_converter(src_base_dir,  tgt_base_dir, ds_name):
    schemas = json.load(open(f'{src_base_dir}/schemas.json')) #reads content of schemas in dict called schemas
    files = glob.glob(f'{src_base_dir}/{ds_name}/part-*') #gives source file names, the * chooses all files that match the pattern

    for file in files:
        print(f'Processing {file}')
        df = read_csv(file, schemas)
        file_name = re.split('[/\\\]', file)[-1]
        to_json(df, tgt_base_dir, ds_name, file_name)


#wrapper to process all files
def process_files(ds_names=None):
    src_base_dir = os.environ.get('SRC_BASE_DIR') #we will fix this hardcoding later when we deploy app
    tgt_base_dir = os.environ.get('TGT_BASE_DIR')  
    schemas = json.load(open(f'{src_base_dir}/schemas.json'))
    if not ds_names: #if ds_names = None, then we are getting the dataset names into a list using schemas.keys. If no arguments are passed, it will process all datasets
        ds_names = schemas.keys()
    for ds_name in ds_names: #is ds_names exists, it will process the datasets in that list
        print(f'Processing {ds_name}')
        file_converter(src_base_dir, tgt_base_dir, ds_name)

if __name__ == '__main__':  #only runs when executed as a script
    if len(sys.argv) == 2: #program file name + whatever argument = 2
        ds_names = json.loads(sys.argv[1]) #JSON array converted to python list
        process_files(ds_names)         
    else:
        process_files()

#> $Env:SRC_BASE_DIR = "data/retail_db"
#> $Env:TGT_BASE_DIR = "data/retail_db_json"
#> python app.py '[\"orders\", \"order_items\"]' - works
#> python app.py [] - works
#> python app.py - works after adding if-else statement in main function
        
    