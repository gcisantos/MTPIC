from django.db import models

class Configuracoes(models.Model):
    #Id para utilização de refêrencia
    id_config =models.IntegerField(primary_key=True)
    #Idioma selecionado
    idioma = models.TextField(default="")
    #linguagem
    linguagem = models.TextField(default="")
    #caminho padrão das pastas
    caminho_raiz_programas = models.TextField(default="")
    #caminho padrão arquivo
    caminho_padrao_arquivo = models.TextField(default="")


# Create your models here.
class Buscas(models.Model):
    #Id criado automatico para saber qual foi inserido e poder obter o mesmo no futuro
    id_busca = models.AutoField(primary_key = True)

    #Campo para verificar se foi processado
    processado_busca = models.BooleanField(default=False)

    #Forma de busca é para saber se foi realizado através de link, texto, documento ou imagem
    forma_busca = models.TextField()

    #caminho do arquivo caso seja escolhido arquivo omo forma de processamento
    caminho_arquivo = models.TextField(default="")

    #caminho do link, caso a busca tenha sido realizada na forma de linl
    caminho_link = models.TextField(default="")

    #texto busca é o texto original inserido na busca
    texto_busca = models.TextField()

    #dataHora que foi iniciado a busca
    dataIni_busca = models.DateTimeField()

    #dataHora que foi finalizada a busca
    dataFim_busca = models.DateTimeField(null=True, blank=True)

    #taxa de aceitação para o programa processar
    taxaAceitacao = models.IntegerField(default=0)

    #forma euristica processamento
    """
    1 - Considera 1º tema correto
    2 - Dez primeiros temas, remove fora taxa aceitação e soma simTexto    
    3 - Mescla os 2 acima e retona a intersectão do maior, caso haja intersecção realiza união caso não 
    haja intersecção consireda somente euristica 1
    """
    euristicaProcessamento = models.IntegerField(default=0)

    """
    1 - Busca Tema
    2 - Busca SubTemas
    3 - Busca os Dois
    """
    tipoBusca = models.IntegerField(default=0)

    #Informa a linguagem que foi realizada a busca
    idioma = models.TextField(null=True, blank=True)

    #retorno dos temas encontrados para texto
    resultadoTema_busca = models.TextField(null=True, blank=True)

    #resultado dos subtemas e suas proximidaes com o texo
    resultadoAssuntos_proximidades_busca = models.TextField(null=True, blank=True)

    #resultado do grafo, armazena aqui o grafo em forma de json
    resultado_Grafo =models.TextField(null=True, blank=True)