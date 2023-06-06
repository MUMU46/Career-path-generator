import requests
import json
#https://api.bilibili.com/x/web-interface/search/type?&page=1&order=click&keyword=mmd&search_type=video
url = "https://api.bilibili.com/x/web-interface/search/type"
headers = {
    'cookie': "buvid3=3FF44B8A-4F4B-42DF-B7F4-3E092D5F3300167638infoc; nostalgia_conf=-1; CURRENT_BLACKGAP=0; buvid_fp_plain=undefined; DedeUserID=392392678; DedeUserID__ckMd5=5954f62d60edb61a; i-wanna-go-back=-1; b_ut=5; LIVE_BUVID=AUTO3416591904326772; blackside_state=0; b_nut=100; rpdid=|(umm)m|~)Rm0J'uYY)YY|Y~k; _uuid=D3344124-21FF-A494-B2310-4186D8DE5106774734infoc; hit-new-style-dyn=0; hit-dyn-v2=1; CURRENT_FNVAL=4048; CURRENT_PID=f06322b0-cf9c-11ed-ba84-132d1a25cb1f; buvid4=DED8D592-70D8-FEF1-CF2A-35E7AE470AEB36421-022022610-G%2FkDBVQKlngthXrIma%2FyiQ%3D%3D; CURRENT_QUALITY=80; bsource=search_bing; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=4; browser_resolution=1398-707; bp_video_offset_392392678=794088115544260600; innersign=0; SESSDATA=35059ee9%2C1699371367%2C31aaf%2A52; bili_jct=048419ca62e4527a7e397db12c7f9fe2; b_lsid=7D5B3439_1880B794BF7; fingerprint=b0fe590022c5f2cbd223a59f4ca6a75c; buvid_fp=b0fe590022c5f2cbd223a59f4ca6a75c; sid=5my72vlf; PVID=2",
    'Referer': "https://search.bilibili.com",
    'origin': 'https://search.bilibili.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}


def spiderbili(s_word, keys):
    length = int(len(keys))
    videos = []
    for i in range(0, length):
        if keys[i].lower() == s_word.lower():#和搜索词相同的技能词不搜索
            continue
        s = s_word + keys[i]
        params = {
            'page': 1,
            'keyword': s,
            'search_type': 'video'
        }
        list_res = requests.get(url, headers=headers, params=params)
        #只要前三个视频的url，封面图，标题

        data = list_res.text
        print(data)
        jons_str = json.loads(data)
        # for t in jons_str['data']['result']:
        #     t1 = t["title"]
        #     t2 = t1.replace('<em class="keyword">', "")
        #     t3 = t2.replace("</em>", "")
        #一个关键词
        if jons_str['data']['numResults'] >= 3:
            data_item = {
                'skill': keys[i],
                'video': [{
                'url': jons_str['data']['result'][0]['arcurl'],
                'cover': '//images.weserv.nl/?url=https:' + jons_str['data']['result'][0]['pic'],
                'title': (jons_str['data']['result'][0]['title'].replace('<em class="keyword">', "")).replace("</em>", "")
                },
                {
                'url': jons_str['data']['result'][1]['arcurl'],
                'cover':'//images.weserv.nl/?url=https:' + jons_str['data']['result'][1]['pic'],
                'title': (jons_str['data']['result'][1]['title'].replace('<em class="keyword">', "")).replace("</em>", "")
                },
                {
                    'url': jons_str['data']['result'][2]['arcurl'],
                    'cover': '//images.weserv.nl/?url=https:' + jons_str['data']['result'][2]['pic'],
                    'title': (jons_str['data']['result'][2]['title'].replace('<em class="keyword">', "")).replace("</em>", "")
                }]
                 }
            videos.append(data_item)
    #全部关键词的搜索结果
    print(videos)
    return videos
    # print(list_res.text)
    # print(data.url)
    # print(data.cover)



