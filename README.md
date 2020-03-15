
<h2>Tutorial MTPIC (Mineração de Texto para Identificação de Conteúdos)</h2>

<p>Esse Notebook tem como principal objetivo explicar a utilização da ferramenta desenvolvida por <b>Gustavo Campos</b> para mineração de texto. Também serão abordados assuntos sobre como usar a aplicação e como reaproveitar métodos desenvolvidos na ferramenta.

<h3>A Ferramenta</h3>

<p>Com o propósito de facilitar e otimizar a forma como extraimos conhecimento de texto foi desenvolvido essa ferramenta. A mesma permite que sejam identificados o tema central e os conteúdos presentes em um texto, além de exibir os resultados extraídos em forma de texto.</p>

<p>Para permitir a criação de algoritmos para realizarem a extração de conteúdos em textos foi necessário a utilização de técnicas e frameworks para realizar o feito</p>

<p><b>Para execução deste projeto foi necessário uso das seguintes técnicas e ferramentas</b></p>


<b>Técnicas:</b>
<ul>
    <li>StopWords</li>
    <li>Tokenization</li>
    <li>Stemming</li>
    <li>DataPrep</li>
    <li>TF-IDF</li>
    <li>Cosseno do Angulo entre Vetores</li>
    <li>Doc2Vec</li>
    <li>Principios do LSA</li>
    <li>Processamento Paralelo</li>    
    <li>Grafos</li>
</ul>


<b>Ferramentas:</b>
<ul>
    <li>Gensim</li>
    <li>NLTK</li>
    <li>Django</li>
    <li>Python 3</li>
    <li>BS4</li>
    <li>DOCXPY</li>
    <li>PYTESSERACT</li>
    <li>PYMUPDF</li>    
    <li>PYTHON-PPTX</li>    
    <li>VisJs</li>    
</ul>

As ferramentas podem ser instaladas através do PIP, somente o Tesseract e o NLTK que precisam de passos a mais, conforme citado abaixo. No caso do VisJs é uma bilioteca utilziada para interface gráfica no HTML.

Pytesseract necessita do arquivo executavel para funcionar. No meu meu caso o mesmo encontra-se 

C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe

O programa utilizado encontra-se junto ao fonte com o nome de Tesseract-OCR.7z, basta descompactar no local citado acima.

Instalação NLTK<br>
Python<br>
    >>Import nltk<br>
    nltk.download()
    
    

<h3>Estrutura da aplicação</h3>

<p>A ferramenta desenvolvida se divide em 3 partes.</p>
<ul>
    <li>Preparação e Treinamento dos Dados</li>
    <li>Processador de Textos</li>
    <li>Interface Gráfica</li>  
</ul>


<h4>Preparação e Treinamento dos Dados</h4>
<p>A primeira parte do projeto diz respeito ao processo de extração, tratamento e treinamento das informações para gerar as bases de texto oriundas do wikipédia que servirão de inteligência para a aplicação.</p>

<p>Nessa etapa temos 4 processos que são realizados para gerarem esses dados.</p> 

<ul>
    <li>Extração dos dados da wikipédia</li>
    <li>Aplicação do processo de Stemming nos dados extraidos</li>
    <li>Execução da técnica TF-IDF na base tratada</li>  
    <li>Treinamento do Doc2Vec para identificar similaridade dos documentos</li>  
</ul>

<h4>Processador de Textos</h4>
<p>O processador de textos realiza a aplicação de técnicas como Stemming, TF-IDF, Doc2Vec nos textos ao qual se deseja obter o tema central e os conceitos. Para que seja possivel extrair tais dados foi desenvolvido uma metodologia especifica de busca. </p>
<p>Através dos dados treinados é identificado o documento ao qual mais se assemelha do texto a ser buscado, em seguida são processados uma lista de 100 documentos similares ao texto em questão. Desses 100 documentos são mantidos apenas os que possuem uma maior semelhança com o documento inicialmente identificado como o mais semelhante. Feito isso são considerados como subtemas ou temas apenas os que estão acima da taxa de assertividade definida pelo usuário no momento da busca. </p>
<p>Para identificação de subtemas é aplicado a mesma metodologia, porém ao invés de verificar se os itens identificados são semelhantes ao primeiro encontrado de maior relação, é analisado se os documentos identificados são semelhantes ao tema central encontra. Dessa forma a cada paragrafo são verificados os temas condinzentes que estão presentes nos mesmos e possuem relação com o tema central </p>

<h4>Interface Gráfica</h4>
<p>A interface gráfica da aplicação permite a interação do usuário com a metodologia desenvolvida de uma forma clara e usual. A mesma conta com os modulos separados pelos processos executados pela aplicação como Tokenização, Stemmização, Identificação do Tema central, Identificação dos Subtemas e o minerador completo que reúne todas os métodos citados anteriomente.</p>
<p>O minerador completo permite o usuário realizar a extração de conteúdos de diversas fontes. Como Sites, Textos simples, PDF,Docx,ppt além de imagens. Como resultado a aplicação permite o usuário verificar os temas e conceitos identificados em uma estrutura de grafos, na qual é possivel identificar a relação entre os temas encontrados. Também é exibido uma tabela contendo informações da probabilidade para cada conteudo identificado.</p>

<h3>Utilização da aplicação</h3>

Para treinar uma base com uma maior quantidade de dados é demandado um tempo maior de processamento e também é recomendável uma quantidade maior de memória RAM.

<h5>Obs.: Para a execução desse notebook foi utilizado um computador desktop com as seguintes caracteristicas:</h5>


<b>Sistema operacional	Windows:</b> 8.1 Pro Professional<br>
                 <b>Processador:</b>  Intel Core i7 4770k 3.5 Ghz<br>
                 <b>Memória Ram:</b>  8Gb 1600Mhz<br>
               <b>Armazenamento:</b>  SSD SAMSUNG EVO 250GB<br>
             <b> Placa de Video:</b>  Gigabyte NVIDIA GTX750 TI<br>

<h4>Treinamento dos dados</h4>

<p>Para que seja possivel a utilização da ferramenta desenvolvida é necessário executar o treinamento das informações para serem utilizadas como inteligencia da aplicação.</p>

<p>Os dados do wikipédia podem ser baixados através do seguinte link <a href="https://dumps.wikimedia.org/">https://dumps.wikimedia.org/</a> para seleção do idioma basta acrescentar 'idioma'+wiki na url, segue exemplo dos dados da wikipédia em Português <a href="https://dumps.wikimedia.org/ptwiki/">https://dumps.wikimedia.org/ptwiki/</a> o arquivo completo com as páginas da wikipédia é sempre o que contém o texto <b>pages-articles-multistream.xml.bz2</b>. Para o exemplo em questão utilizaremos os dados parciais da wikipédia <b>ptwiki-20190701-pages-articles-multistream6.xml-p5862698p6032963.bz2</b></p>

<p>Para o treinamento das informações iremos utilizar o script <b>Prep_Script.py</b> disponível em <b>MTPIC\MTPIC_DataPrep</b>.</p>


```python
!dir D:\MTPIC\MTPIC_DataPrep\


```

     O volume na unidade D ‚ DADOS
     O N£mero de S‚rie do Volume ‚ 4A93-D151
    
     Pasta de D:\MTPIC\MTPIC_DataPrep
    
    22/07/2019  23:26    <DIR>          .
    22/07/2019  23:26    <DIR>          ..
    21/07/2019  00:44    <DIR>          .vs
    22/07/2019  22:51            13.663 Prep.py
    20/07/2019  23:02             2.275 Prep_Script.py
    16/07/2019  21:59    <DIR>          Referˆncias
    22/09/2018  19:01            30.164 reimplementado_make_wikicorupus.py
    16/07/2019  22:03                 0 __init__.py
    21/07/2019  01:36    <DIR>          __pycache__
                   4 arquivo(s)         46.102 bytes
                   5 pasta(s)   251.163.443.200 bytes dispon¡veis
    

<p>O script possui parametros para definirmos arquivos de entrada, saida e linguagem a ser processada. A sintaxe pode ser verificada utilizando o -h no comando.</p>


```python
!python D:\MTPIC\MTPIC_DataPrep\Prep_Script.py -h
```

    
    
    Para utilização devem ser inseridos os dados no seguinte formato:
    
    Prep.py -i <arquivoWikipedia> -o <pastaSaida> -l <linguagem>
    
    Linguagens aceitas:
    da - danish
    nl - dutch
    en - english
    fi - finnish
    fr - french
    de - german
    hu - hungarian
    it - italian
    no - norwegian
    pt - portuguese
    ro - romanian
    ru - russian
    es - spanish
    sv - swedish
    

Para o exemplo iremos treinar os dados em português da base parcial adquirida no wikipédia.<a href="https://dumps.wikimedia.org/ptwiki/">Disponível aqui</a> com cerca de apenas 56MB.


```python
!python D:\MTPIC\MTPIC_DataPrep\Prep_Script.py -i D:\MTPIC\DadosTeste\ptwiki-20190701-pages-articles-multistream6.xml-p5862698p6032963.bz2 -o D:\MTPIC\DadosProcessados\ -l pt
```

<p>Após os dados serem processados é criado a seguinte estrutura de arquivos na pasta de destino.</p>

<p>Esses arquivos serão utilizados posteriormente pelo modulo de processamento de texto e pela parte gráfica.</p>

<p>Os arquivos gerados no formato .gz dizem respeito aos dados brutos que servem de base para analise. Os arquivos .dict fazem parte do dicionario utilizado para processamento dos métodos de treinamentos. Os arquivos arquivos model fazem parte dos treinamentos realizados e o sims contempla as similaridades geradas a partir do método TF-IDF </p>


----config_portuguese.ini<br>
----/portuguese/<br>
----log20190722233815.txt<br>
----/Arquivos_Gerados/<br>
--------TextosWikipedia_pt.gz<br>
--------TitulosWikipedia_pt.gz<br>
---------/Analisadores/<br>
------------.0<br>
------------dicionarioDoc2Bow_pt.dict<br>
------------dicionarioDoc2Bow_pt.dict.index<br>
------------dicionario_pt.dict<br>
------------similaridades_pt.sims<br>
------------tf_idf_pt.tfidf_model<br>
---------/Doc2Vec/<br>
------------dv2_pt.model<br>
---------/Stemming/<br>
------------BaseWikipedia_pt_Stemizado.gz<br>

<h4>Utilização do Minerador</h4>

O primeiro passo para utilizar o minerador é iniciar o processador. O processador é uma parte do sistema que realiza o processo fundamental da aplicação.

Através desse processo são realizadas as idenficações de conteúdo.

O processador funciona basicamente no seguinte formato. Para permitir que fosse possivel a execução de forma rápida e com o mesmo uso de memória para qualquer pesquisa realizada, foi desenvolvido esse serviço que fica rodando em loop ifinito aguardando os textos para processar. De forma simples podemos entender o processador com as seguintes etapas.

1 - Inicia a aplicação carregando todos os arquivos previamente treinados em memória. Isso agiliza o nosso processamento.

2 - Realiza uma busca inicial padrão para certificar que o ambiente está funcional.

3 - Entra em loop consultando infinitamente um banco de dados onde são armazenados os textos que se deseja minerar.

4 - Quando uma aplicação deseja realizar uma consulta ela deve salvar o texto desejado no banco de dados e aguardar o fim do processamento.

5 - O processador consulta a mesma base e quando encontra realiza o processamento e guarda o resultado no banco.

6 - A aplicação que solicitou deve consultar novamente esse banco e obter o resultado.

Abaixo será apresentado como realizar esse processo.

<h4>Iniciando o processador</h4>

Conforme mostrado anteriormente, o processo de treinamento gera um arquivo de configuração. Através dele devemos executar nosso processador com o seguinte script.


```python
!python D:\MTPIC\MTPIC_Processador\processadorTextos.py -h
```

<b>Teremos o seguinte resultado</b>

Para utilização devem ser inseridos os dados no seguinte formato:

processadorTextos.py -i <'arquivoConfiguracao'>

Como podemos ver no exmplo abaixo:

Obs.: não podemos executar no jupyter pois se trata de um serviço em loop infinito, o jupyter só exibe quando o comando finaliza.


```python
python processadorTextos.py -i D:\MTPIC\DadosProcessados2\config_portuguese.ini
```

Quando o servidor for iniciado será exibida a seguinte mensagem.


<br>

<b>Quantidade de sentenças a processar: 1</b>
<b>Tempo estimado: 2.25s</b>

<b>Servidor iniciado em : 2.8890669345855713</b>
<b>Tempo: 2020-02-06 17:00:14.792936</b>


Após serviço estar inciado podemos fazer uso através da interface gráfica, ou através de scripts que se comuniquem diretamente com a aplicação.

A interface gráfica permite maior facilidade para o usuário. Como podemos ver nas explicações abaixo.

<h4>Interface gráfica</h4>

Quando for necessário a utilização da interface gráfica, devemos subir outro serviço. O Django.

Toda parte gráfica foi desenvolvida para ambiente web com o framework Django.

Para iniciar o servidor é simples devemos ir executar o seguinte comando.


```python
!python D:\MTPIC\MTPIC\manage.py runserver
```

Novamente, coma trata-se de um serviço não podemos executar pelo jupyter.

Após o server estar iniciado, teremos uma mensagem conforme abaixo:



<b>Performing system checks...</b><br>

<b>System check identified no issues (0 silenced).</b><br>
<b>February 06, 2020 - 17:06:33</b><br>
<b>Django version 2.1.2, using settings 'MTPIC.settings'</b><br>
<b>Starting development server at http://127.0.0.1:8000/</b><br>
<b>Quit the server with CTRL-BREAK.</b><br>



Em seguida basta acessarmos o link informado para termos acesso a aplicação

<h4>Estrutura</h4>

A interface foi permite navegar entre as seguintes telas:

<b>Inicio:</b> Informações gerais da aplicação.<br><br>
<b>Modulos:</b> Menu com todas as funcionalidades.<br><br>
<b>Tokenizer:</b> Módulo responsável pela quebra do texto em pequenas partes.<br><br>
<b>Remoção de Stopwords:</b> Módulo responsável remoção de palavras sem significado semântico para o texto.<br><br>
<b>Stemming:</b> Módulo responsável pela transformação das palavras em sua forma raiz.<br><br>
<b>Extrator de Tema Central:</b> Módulo responsável pela extração do tema do texto.<br><br>
<b>Extrator de Conceitos:</b> Módulo responsável pela dos conceitos encontrados no texto.<br><br>
<b>Minerador Completo:</b> Módulo responsável pela união e execução de todos os processos acima.<br><br>
<b>Visualizar Dados Processados:</b> Módulo responsável pela por permitir consultar o resultado de processos anteriores.<br><br>


![Modulos.png](https://raw.githubusercontent.com/gcisantos/MTPIC/master/Imagens/1.png)

<h4>Tela inicial</h4>

A primeira tela do sistema contém um breve resumo do que foi feito, como funciona e as principais técnicas utilizadas.

![Tela_Inicial.png](https://raw.githubusercontent.com/gcisantos/MTPIC/master/Imagens/2.png)



<h4>Tokenizer</h4>

Executa os processos de quebra de texto, transformando cada palavra em uma posição de um vetor. Esse processo é utilizado em todos os momentos da aplicação para que o sistema possa converter o texto em um formato interpretável pelo computador.

![Tokenizer.png](https://raw.githubusercontent.com/gcisantos/MTPIC/master/Imagens/3.png)


<h4>Remoção de Stopwords</h4>

Executa os processos de limpeza do texto. Removendo as palavras que não agregam conteúdo semantico, ou seja, mesmo sem essas palavras ainda é possivel entender o sentido do texto.

![StopWords.png](https://raw.githubusercontent.com/gcisantos/MTPIC/master/Imagens/4.png)


<h4>Stemming</h4>

Responsável também por realizar a limpeza do texto. Transformando as palavras em sua forma raiz. Esse processo faz uso dos dois processos anteriores.

![Stemming.png](https://raw.githubusercontent.com/gcisantos/MTPIC/master/Imagens/5.png)


<h4>Extratores de Conteúdo</h4>

O extrator de tema central, extrator de conceitos e minerador completo, executam basicamente os mesmos processos. A unica diferença é a forma como os dados são exibidos.

Esse processos são o core da aplicação, realizam toda a sistemática necessária para se atender o propósito. Eles podem ser descritos através do seguinte fluxo.

1 - Coleta dos dados(Onde são realizadas a entrada de textos).

2 - Tratamento dos dados.

3 - Processamento dos dados.


Nesse projeto em questão a parte de coleta foi desenvolvida para permitir que fosse possivel obter texto das seguintes fontes.

- WebSites
- Arquivos
- Imagens
- Textos inseridos manualmente

A tela principal do minerador permite a seleção do tipo de arquivo que deseja processar, assim como a taxa de assertividade que deseja obter. A taxa de assertividade serve como um limitador de o quão confiável você deseja obter de informação, ou quanto de abrângencia daquele assunto você dejese que o sistema encontre.

![Minerador.png](https://raw.githubusercontent.com/gcisantos/MTPIC/master/Imagens/6.png)


Os processos de extração de textos estão todos no arquivo D:\MTPIC\MTPIC\processamento\obtemTexto.py através dos métodos:

![Metodos.png](https://raw.githubusercontent.com/gcisantos/MTPIC/master/Imagens/7.png)

Após o texto ser extraído a aplicação grava o texto que deseja processar na base de dados. O processador que já estava em execução anterioremente, realiza a leitura do banco e processa o texto inserido. A aplicação fica aguardando o processador executar a mineração e ao fim o resultado é armazenado no banco de dados, onde a aplicação realiza uma nova consulta para obter um JSON com os temas encontrados.

Exibindo da seguinte forma:

Parâmetros selecionados para execução<br>

Para esse exemplo foi utilizado a forma de extração através de link, onde o sistema remove o texto da página web, realiza o preprocessament e envia para o processador.

O link utilizado foi: https://www.ebiografia.com/thomas_edison/

![Processo.png](https://raw.githubusercontent.com/gcisantos/MTPIC/master/Imagens/8.png)<br>


Resultado do processamento<br>
![Resultado.png](https://raw.githubusercontent.com/gcisantos/MTPIC/master/Imagens/9.png)
