def test_df():
    import pandas as pd
    return pd.DataFrame({'a':[2,4],'b':[6,8]})


def data_dir():
    
    from pathlib import Path
    
    path = Path.cwd()
    while not any(i.name == 'data' for i in path.iterdir()):
        path = path.parent   
        
    return path / 'data'
            
def get_file(filespec):
    
    file_dict = {'weather':'epvars90m_ChiLoopOnly_2015.Loop.csv',
                 'buildings':'chi0_90m_coord2bldg_smc.csv',
                 'morphology':'bldgenergyuse/4 - Simulate buildings for urban morphologies/morphology_data/NoMorph.json'} # morphology specifies folder, not file!

    if filespec in file_dict:
        fname = file_dict[filespec]
        if filespec == 'morphology':
            path = data_dir() / fname
#             paths = list(path.iterdir())
            return path
        else:
            path = data_dir() / filespec / fname
            return path
    else:
        print('File not found')


def get_data(filespec, old_weather_read = False):
    
    import pandas as pd
    from datetime import datetime
            
    if filespec == 'weather':
        weather_path = get_file('weather')
        conv_dt = lambda x : datetime.strptime(x, '%Y-%m-%d_%H:%M:%S')
        if not old_weather_read:
            weather_df_iter = pd.read_csv(weather_path, chunksize=880, parse_dates=['time'], date_parser=conv_dt)
        else:
            weather_df_iter = pd.read_csv(weather_path, chunksize=880)
        return weather_df_iter
    elif filespec == 'bldgs':
        bdf = pd.read_csv('temp/bldgs.csv')
        return bdf
    else:
        print('File not found')

def random_ids(df):
    
    '''
    Input dataframe without ids.
    Return dataframe with column of random IDs of length 4.
    '''
    
    import random
    
    ids = random.sample(range(1000, 9999), len(df))
    df.insert(0, 'id', ids)
    
    return df

def clean_data(df, filespec='mic'):
    
    '''
    Clean data.
    '''
    
    if filespec == 'coc':
        df['shape_area'] = df.shape_area.astype(float)*0.092903 
        print('double check if values already changed')
    return df

def plot_bldgs():
    
    import pandas as pd
    import geoviews as gv
    
    bdf = pd.read_csv('temp/bldgs.csv')
    bldgs = gv.Points(bdf, kdims=['Lon','Lat'], vdims=['area_total', 'MEAN_AVGHT']).opts(size=3, color='r')
    return bldgs


def plot_footprints(df, filespec='mic'):
    
    import pandas as pd
    import geoviews as gv
    
    params = {'coc':['shape_area', 'stories'], 'mic':[]}[filespec]
    return gv.Polygons(df, vdims=params)

def plot_centroid(shapely_obj):
    
    import geoviews as gv
    
    shape = gv.Shape(shapely_obj)
    centroid = gv.Points(gv.Shape(shapely_obj.centroid).dframe()).opts(size=10, color='r')   
    return shape*centroid

def geodf_to_csv(geodf, fname):
    df = pd.DataFrame(geodf)
    if 'geometry' in geodf.columns:
        df.geometry = df.geometry.astype('object')
    df.to_csv(fname, index=False)
    
def tile():
    import geoviews as gv
    return gv.tile_sources.Wikipedia

def conv_temp(temp_in, in_scale='K', out_scale='F'):
    
    if in_scale == 'K':
        if out_scale == 'F':
            temp_out = temp_in*9/5 - 459.67
    elif in_scale == 'C':
        if out_scale == 'F':
            temp_out = temp_in*9/5 + 32
    else:
        print('Conversion not possible.')
        return
    return temp_out
            
def conv_dt(x):
    from datetime import datetime
    return datetime.strptime(x, '%Y-%m-%d_%H:%M:%S')