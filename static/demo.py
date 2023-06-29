#UCGaV7wf8doFQlYFDQfxTbVg
import scrapetube
import json

videos = scrapetube.get_channel("UCGaV7wf8doFQlYFDQfxTbVg")
data = {"data": []}
for video in videos:
  temp = {}
  temp['link'] = "https://www.youtube.com/watch?v=" + video['videoId']
  temp['thumbnail'] = video['thumbnail']['thumbnails'][-1]['url']
  temp['title'] = video['title']['runs'][0]['text']
  temp['created'] = video['publishedTimeText']['simpleText']
  temp['viewCount'] = video['viewCountText']['simpleText']
  temp['time'] = video['thumbnailOverlays'][0][
    'thumbnailOverlayTimeStatusRenderer']['text']['simpleText']
  try:
    temp['hoverVideo'] = video['richThumbnail']['movingThumbnailRenderer'][
      'movingThumbnailDetails']['thumbnails'][0]['url']
  except:
    pass
  data['data'].append(temp)

json_object = json.dumps(data, indent=4)
with open("data2.json", "w") as outfile:
  outfile.write(json_object)