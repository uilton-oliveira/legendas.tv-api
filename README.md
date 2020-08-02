# legendasws
Legendas.tv Web Service, with docker included.

#### Exemplos de uso:
{URL}/busca=R3JpbW0gczAxZTAx/pagina=1 _[A busca está usando encode base64, buscando na pagina 1]_  
{URL}/busca=Grimm s01e01/pagina=1 _[Buscando sem encode e na pagina 1]_  
{URL}/busca=Grimm/pagina=2 _[Buscando sem encode e na pagina 2]_  
{URL}/autodetect=Once.Upon.a.Time.S03E15.720p.HDTV.X264-DIMENSION.mkv  
{URL}/guess=Once.Upon.a.Time.S03E15.720p.HDTV.X264-DIMENSION.mkv  
 
#### Explicação:
busca= Aqui entra o termo que irá ser buscado no legendas.tv, é recomendado que seja usado encode base64 neste campo.  
pagina= Pagina que será exibida (legendas.tv), começa em 1.  
autodetect= Procura automaticamente a melhor legenda de acordo com o grupo que lançou, resolução, formato e codecs (apenas legendas.tv)  
guess= Extrai as informações do filme/serie baseado pelo nome e exibe via JSON (guessit.io)  

#### Docker:
docker run -p 8000:8000 uilton/legendasws:latest

#### Docker Compose:
docker-compose up -d
