# Scrapy Python dos fóruns no site do game APEX Legends

## Descrição
Este projeto é um spider de captura dos posts realizados pelos usuários no site de fóruns do novo game "Apex Legends", localizados no site [Apex Legends Fóruns](https://answers.ea.com/t5/Apex-Legends/ct-p/apex-legends-pt).

## Funcionamento
Primeiro define-se como parâmetro a página do primeiro tópico que será usada para a navegação inicial do spider _apexforum.py_, na variável:

> url = [
>            'https://answers.ea.com/t5/Problemas-tecnicos/Possiveis-solucoes-para-crashes-erros-desconexoes-congelamento/td-p/7571666',
>        ]

O mesmo arquivo spider fará toda a paginação a partir daí:
- primeiro navegar dentro de cada página do mesmo tópico (usando o link "SEGUINTE", no final dos tópicos);
- caso não encontre uma nova página, segue o link "Próximo tópico >" que está no início de cada tópico.

Essa navegação pode ser explicado pelo trecho:
```
...
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        elif next_topic is not None:
            yield response.follow(next_topic, callback=self.parse)
...
```

## Instalação
Descompacte o projeto para a sua pasta que será acessada pelo framework Scrapy do Python ([instalação e documentação do Scrapy aqui](https://docs.scrapy.org/en/latest/intro/overview.html)).
Em seguida, execute o comando de "crawl" via conda prompt, como no exemplo abaixo (que salva os dados capturados no formato JSON dentro do diretório _json_, criado na mesma pasta acessada pelo Scrapy):
```
(env) C:\Users\<seu_usuario>\Documents\Python Scripts\Scrapies\apexforum> scrapy crawl apexforum -t json -o - > "json/apexforum.json"
```

