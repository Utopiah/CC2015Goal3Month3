class Item(object):

    def __init__(self):
        pass

    def item_details(item):
        detailed_item = {}
        for element in item:
            if element == 'title':
                detailed_item['title'] = item[element].encode('ascii', 'ignore') 
            if element == 'id':
                detailed_item['id'] = item[element]
            if element == 'duration':
                detailed_item['duration'] = item[element]
            # problem with recorded
            """
            if element == 'recorded':
                pass
            if element == 'title' or element == 'description':
                print element, last[element].encode('ascii', 'ignore')
            else:
                print element, last[element]
            """
        return detailed_item
    
    def item_details_by_id(item_id):
        req = requests.get("http://gdata.youtube.com/feeds/api/videos/" + item_id + "?v=2&alt=jsonc")
        data = json.loads(req.text)
        return item_details(data['data'])

    def get_bpm(seg):    
        #    cf analysis.tempo() http://atl.me/overvie
        #       consider pydub high/low-pass filters and dBFS attribute
        #       e.g. https://gist.github.com/jiaaro/faa96fabd252b8552066
        # from https://gist.github.com/jiaaro/faa96fabd252b8552066
        # reduce loudness of sounds over 120Hz (focus on bass drum, etc)
        seg = seg.low_pass_filter(120.0)
        # we'll call a beat: anything above average loudness
        beat_loudness = seg.dBFS
        # the fastest tempo we'll allow is 240 bpm (60000ms / 240beats)
        minimum_silence = int(60000 / 240.0)
        nonsilent_times = detect_nonsilent(seg, minimum_silence, beat_loudness)
        spaces_between_beats = []
        last_t = nonsilent_times[0][0]
        for peak_start, _ in nonsilent_times[1:]:
            spaces_between_beats.append(peak_start - last_t)
            last_t = peak_start
        # We'll base our guess on the median space between beats
        spaces_between_beats = sorted(spaces_between_beats)
        space = spaces_between_beats[len(spaces_between_beats) / 2]
        bpm = 60000 / space 
        return bpm
