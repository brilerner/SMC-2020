
def data_dir():
    
    from pathlib import Path
    
    path = Path.cwd()
    while not any(i.name == 'data' for i in path.iterdir()):
        path = path.parent   
        
    return path / 'data'
            
def get_file(filespec):
    
    file_dict = {'weather':'epvars90m_ChiLoopOnly_2015.Loop.csv',
                 'buildings':'chi0_90m_coord2bldg_smc.csv',
                 'morphology':'bldgenergyuse/4 - Simulate buildings for urban morphologies/morphology_data'} # morphology specifies folder, not file!

    if filespec in file_dict:
        fname = file_dict[filespec]
        if filespec == 'morphology':
            path = data_dir() / fname
            paths = list(path.iterdir())
            return paths
        else:
            path = data_dir() / filespec / fname
            return path
    else:
        print('File not found')


def get_data(filespec):
    
    import pandas as pd
            
    if filespec == 'weather':
        weather_path = get_file('weather')
        weather_df_iter = pd.read_csv(weather_path, chunksize=880)
        return weather_df_iter
    else:
        print('File not found')
