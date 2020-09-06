# legendasws 2.0
Legendas.tv API completely rewritten in Node, with docker included.

## Environment Variables
GUESSIT_HOST: GuessIt Rest URL, required for some APIs to work - https://github.com/guessit-io/guessit-rest  

PORT: Set the server port, defaults to 3000  

USER_AGENT: Configure the user agent that will be used by the crawler, defaults to:
```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 
```
## API Usages:  
##### Searching for Arrow S01E01 (url encode it) on page 1
```
GET /search/Arrow.S01E01  
```
Response (stripped):
```json
{
  "releases": [
    {
      "id": "5ab439fc94ecb",
      "name": "Harrow.S01E01.WEBRIP.HDTV.PDTV.720p.x264-ORENJI-FQM-MFO",
      "download": "http://legendas.tv/downloadarquivo/5ab439fc94ecb"
    },
    {
      "id": "54e54773ef245",
      "name": "Arrow.s01e01.480p.BRRip.x264-Encodeking",
      "download": "http://legendas.tv/downloadarquivo/54e54773ef245"
    }
  ],
  "last_page": true
}
```
##### Searching for Arrow on page 2
```
GET /search/Arrow/2  
```
Response (stripped):
```json
{
  "releases": [
    {
      "id": "5cea489850d77",
      "name": "Arrow.S07E22.You.Have.Saved.This.City.1080p.AMZN.WEB-DL.DDP5.1.H.264-CasStudio",
      "download": "http://legendas.tv/downloadarquivo/5cea489850d77"
    },
    {
      "id": "5ce341e10e75d",
      "name": "Arrow.S07.1080p.AMZN.WEB-DL.DDP5.1.H.264-CasStudio",
      "download": "http://legendas.tv/downloadarquivo/5ce341e10e75d"
    }
  ],
  "last_page": false
}
```
##### Try to automatically find the best subtitle for the given file name (GuessIt Rest URL Required)
```
GET /autodetect/Once.Upon.a.Time.S03E15.720p.HDTV.X264-DIMENSION.mkv
```
Response:
```json
{
  "id": "5338e1207dfee",
  "name": "Once.Upon.a.Time.S03E15.HDTV.x264-LOL-AFG-EVO-DIMENSION",
  "download": "http://legendas.tv/downloadarquivo/5338e1207dfee"
}  
```
##### Retrieve result from GuessIt rest service, just an alias (GuessIt Rest URL Required)
```
GET /guessit/guess/Once.Upon.a.Time.S03E15.720p.HDTV.X264-DIMENSION.mkv
```
Response:
```json
{
  "title": "Once Upon a Time",
  "season": 3,
  "episode": 15,
  "screen_size": "720p",
  "source": "HDTV",
  "video_codec": "H.264",
  "release_group": "DIMENSION",
  "container": "mkv",
  "mimetype": "video/x-matroska",
  "type": "episode"
}
 ```
##### Given a filename and a list of names, find the most suitable (GuessIt Rest URL Required)
```
POST /guessit/choosebest
```
Body - Content-Type: application/json
```json
{
    "filename": "Mulan.2020.1080p.WEBRip.DDP5.1.x264-EVO",
    "names": [
        "Mulan.2020.720p.DSNP.WEBRip.DDP5.1.x264-NOGRP",
        "Mulan.2020.1080p.WEBRip.DDP5.1.x264-EVO",
        "Mulan.2020.720p.DSNP.WEB-DL.DDP5.1.Atmos.H.264-CMRG",
        "Mulan.2020.1080p.WEBRip.x264-RARBG"
    ]
}
```
Response:
```
Mulan.2020.1080p.WEBRip.DDP5.1.x264-EVO
```

#### Docker:
```
docker run -p 5000:80 -it guessit/guessit-rest
docker run -p 3000:3000 -e GUESSIT_HOST=http://localhost:5000 uilton/legendasws:latest
```
#### Docker Compose:
Start both this LegendasWS and GuessIt-Rest containers, in the same network.
```
docker-compose up -d
```
