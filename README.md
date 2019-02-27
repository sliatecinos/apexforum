# Scrapy Python dos fóruns no site do game APEX Legends

## Descrição
Este projeto é um spider de captura dos posts realizados pelos usuários no site de fóruns do novo game "Apex Legends", localizados no site [Apex Legends Fóruns](https://answers.ea.com/t5/Apex-Legends/ct-p/apex-legends-pt).

## Dados capturados
|Coluna|Dados|
|:---:|:---:|
|forum_url|Url da página do fórum|
|forum_topic|Descrição do tópico|
|forum_title|Título do tópico|
|forum_post_date|Data da postagem|
|forum_kudos|Kudo points atribuídos ao post|
|forum_user|Usuário da postagem|
|forum_posts|Mensagem postada|

## Funcionamento
Primeiro define-se na lista `url` o endereço da página do primeiro tópico que será usada para a navegação inicial do spider _apexforum\spiders\apexforum.py_:

> `url = [
>            'https://answers.ea.com/t5/Problemas-tecnicos/Possiveis-solucoes-para-crashes-erros-desconexoes-congelamento/td-p/7571666',
>        ]`

O mesmo arquivo spider fará toda a paginação a partir daí:
- _primeiro navegar dentro de cada página do mesmo tópico (usando o link "SEGUINTE", no final dos tópicos);_
- _caso não encontre uma nova página, redireciona pelo link "Próximo tópico >" que está no início de cada tópico._

Tal navegação pode ser explicada pelo trecho em _apexforum.py_:
```python

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        elif next_topic is not None:
            yield response.follow(next_topic, callback=self.parse)

```

## Instalação
Descompacte o projeto para a sua pasta que será acessada pelo framework Scrapy do Python ([instalação e tutorial do Scrapy aqui](https://docs.scrapy.org/en/latest/intro/overview.html)).

Em seguida, execute o comando de "crawl" via conda prompt, como no exemplo abaixo que salva os dados capturados no formato JSON, dentro do diretório _json_ (criado na mesma pasta acessada pelo Scrapy):
```
(env) C:\Users\<seu_usuario>\Documents\Python Scripts\Scrapies\apexforum> scrapy crawl apexforum -t json -o - > "json/apexforum.json"
```

