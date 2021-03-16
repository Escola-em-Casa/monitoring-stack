# Como subir o ambiente

## Dependências

- Docker
- Docker-compose
- crontab


## Se você nunca subiu o ambiente

### Configurando o ElasticSearch e o Kibana
1. Execute o comando para criar e deixar rodando em background o elasticsearch

``` 
sudo docker-compose up -d
```

2. Execute o comando 

``` 
sudo docker-compose exec elasticsearch bash
```

3. Agora vamos definir os usuários (dentro do container do elasticsearch):

``` 
./bin/elasticsearch-setup-passwords interactive
```

4. Definidos no elasticsearch. precisamos criar o usuário no Kibana (dentro do container do kibana):

``` 
sudo docker-compose exec kibana bash
```

5. Dentro do container, execute os seguintes comandos, digitando, quando necessário, o usuário kibana, e a senha criada no passo anterior.

``` 
./bin/kibana-keystore create
./bin/kibana-keystore add elasticsearch.username
./bin/kibana-keystore add elasticsearch.password
```

6. Por fim, reinicie os containers:
```
sudo docker-compose restart
```

### Configurando os dados do Escola em Casa no ElasticSearch

1. Atualize as credenciais no arquivo init_data.py
```python
DATAMI_USERNAME = "edf"
DATAMI_PASSWORD = "edf"
ELASTIC_USER = "elastic"
ELASTIC_PASSWORD = "elastic"
URL_ELASTIC = "127.0.0.1:9200"
```

1. Rode o script init_data.py

```
python3 init_data.py
```

### Configurando os dados do Escola em Casa no Kibana

1. Acesse o Kibana e vá na opção Saved Objects (Kibana) ou pelo link http://localhost:5601/app/management/kibana/objects.

2. Clique na opção Import e selecione o arquivo "dashboard_visualizations.ndjson" que está na raiz deste projeto.

3. Agora todos as visualizações e o dashboard foram criados e já estão consumindo os dados do elasticSearch.

### Configurando o coletor de métricas

1. Atualize as credenciais/variáveis de ambiente no arquivo send_data_elastic.py
```python
DATAMI_USERNAME = "edf"
DATAMI_PASSWORD = "edf"
ELASTIC_USER = "elastic"
ELASTIC_PASSWORD = "elastic"
URL_ELASTIC = "127.0.0.1:9200"
```

2. Crie um cronjob para rodar diariamente às 7 horas da manhã executando a seguinte função. OBS: Substitua o <path_to_repository> para a pasta do repositório do projeto, caso tenha dificuldade, entre na pasta raiz deste projeto e digite ```pwd```, copie o resultado e substitua.
```
# Descrição do cronjob
0 7 * * * python3 <path_to_repository>/send_data_elastic.py >> <path_to_repository>/data_usage.log 2>&1 
```

Pronto, agora tudo estará funcionando corretamente.