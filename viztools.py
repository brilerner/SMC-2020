### Chunk creation

def make_lookup_dct(columns):
    """
    Create lookup dictionary for formatting weather variable column names.
    """
    lookup_dct = {}
    for i in columns:
        if i=='Time':
            continue
        name = i.split('_', 1)[0]
        units = i.split('_',1)[1]
        if 'temp' in i:
            name = 'Temp'
        if 'dewpt' in i:
            name = 'Dewpt'
        if 'pres' in i:
            name = 'Pres'
        if 'RadDif' in i:
            name = 'RadDif'
        if 'W' in units:
            units = 'W/m^2'
        if 'ms' in units:
            units = 'm/s'   
        lookup_dct[name] = {}
        lookup_dct[name]['full'] = i
        lookup_dct[name]['units'] = units
    return lookup_dct

def get_chunk_dct(mode, lookup=True):
    
    """
    Prepares data into chunks for plotting.
    Returns chunk dictionary, with times as keys.
    Optionally also return lookup dictionary for formatting weather variable column names.
    """
    import pandas as pd
    
    if mode == 'daily':
        df = pd.read_csv('data/daily_avgs.csv', parse_dates=['Time'])
        df = df.set_index(['Lat','Lon'])
        unique = set(df['Time'])
        chunk_dct = {i:df[df.Time==i] for i in unique}
    elif mode == 'seasonally':
        seasons = ['winter','spring','summer','fall']
        chunks = [pd.read_csv(f'data/{i}.csv') for i in seasons]
        chunk_dct = {s:c.groupby(['Lat','Lon']).mean() for s,c in zip(seasons,chunks)} 
            
    lookup_dct = make_lookup_dct(list(chunk_dct.values())[0].columns)
    renamer = {lookup_dct[i]['full']:i for i in lookup_dct}
    chunk_dct = {i:j.rename(columns=renamer) for i,j in chunk_dct.items()}

    if lookup:
        return chunk_dct, lookup_dct
    else:
        return chunk_dct
    
### Colormap creation

def cmbar(cmap_hex_list):
    
    """
    Produces colorbar for list of hex colors
    """
    import numpy as np
    import holoviews as hv
    from geoviews import opts
    spacing = np.linspace(0, 1, len(cmap_hex_list))[np.newaxis]
    img_opts = opts.Image(cmap=cmap_hex_list, xaxis='bare', yaxis='bare', xticks=0, yticks=0, toolbar=None,\
                         frame_height=40, frame_width=300)
    return hv.Image(spacing, ydensity=1).opts(img_opts)

def color_fader(c1,c2,n): 
    """
    fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    """
    import matplotlib as mpl
    import numpy as np
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return [mpl.colors.to_hex((1-x)*c1 + x*c2) for x in np.linspace(0,1,n)]

def adjust_lightness(color, amount=0.5):
    """
    lighten or darkern colors (>1 is lighter, <1 is darker)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return mc.to_hex(colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2]))


def slice_cmap(lo, hi, total, cmap, mode='focus'):
    """
    Slice a colormap by range (section of colormap proportional 
    to range of a variable with reference to an absolute span) or 
    by focus (instead of producing a colormap slice, the range is 
    averaged to a single color, to which a gradient is applied to 
    produce a new colormap is derived by applying a gradient).
    """
    get_index = lambda x:int(round(len(cmap)*(x-total[0])/(total[1]-total[0])))
    if mode =='range':
        lo_index, hi_index = get_index(lo), get_index(hi)
        return cmap[lo_index:hi_index]
    elif mode == 'focus':
        ind = get_index(int(round((lo+hi)/2)))
        if ind == len(cmap):
            ind -= 1
        base = cmap[ind]
        return color_fader(adjust_lightness(base), base, 50) +\
               color_fader(base, adjust_lightness(base),50)  
    
def get_color_ranges(chunk_dct, variables, cmap=None, mode='range', darken=0.5, lighten=0.5):

    """
    Produces colormaps to fit chunks of timeseries data that are 
    proportional to a colormap spanning the entire timeseries.
    Input the chunks, weather variables desired to plot, and the base colormap.
    """
    # Get data ranges
    cmap_dct = {'total':{v:{} for v in variables}}
    minmax = {v:[] for v in variables}
    for i,j in chunk_dct.items():
        cmap_dct[i] = {}
        for v in variables:
            cmap_dct[i][v] = {}
            Max = j[v].max()
            Min = j[v].min()
            cmap_dct[i][v]['values'] = (Min, Max)
            minmax[v].extend([Min,Max])
    for v,j in minmax.items():
        cmap_dct['total'][v]['values'] = min(minmax[v]), max(minmax[v])

    # Get color ranges
    for time,v_dct in cmap_dct.items():
        if time != 'total':
            for v, v_rng in v_dct.items():
                add_colors = slice_cmap(*v_rng['values'], cmap_dct['total'][v]['values'], cmap, mode=mode)
                v_rng['colors'] = add_colors

    return cmap_dct