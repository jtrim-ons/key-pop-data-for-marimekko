import glob
import gzip
import json
import re

for i, filename in enumerate(glob.glob('../key-pop-api-downloader/downloaded/2var/*.gz')):
    if i % 100 == 0:
        print(i, 'completed') 
    with gzip.open(filename, 'rt', encoding='utf-8') as zipfile:
        data = json.load(zipfile)
    out_filename = 'results/' + re.sub(r'(.*/)|(.gz$)', '', filename)
    if data['blocked_areas'] == 1:
        with open(out_filename, 'w') as f:
            json.dump({'blocked': True}, f)
    else:
        short_data = {'blocked': False, 'observations': []}
        for obs in data['observations']:
            out_obs = {'count': obs['observation']}
            out_obs['dims'] = {
                o['dimension_id']: o['option_id']
                for o in obs['dimensions']
                if o['dimension_id'] != 'nat'
            }
            short_data['observations'].append(out_obs)
        with open(out_filename, 'w') as f:
            json.dump(short_data, f)
