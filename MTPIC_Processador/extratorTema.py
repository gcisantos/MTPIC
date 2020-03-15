class ExtratorTema:
    #biblioteca utilizada para medir o tempo de processamento
    import time,datetime,sys,os

    sys.path.insert(0,os.getcwd()+"\\PreprocessamentoTexto\\")

    import preprocess_stemming,threading,operator,gensim,gzip

    from gensim.models.doc2vec import Doc2Vec

    
    import nltk

    titulos = []

    subTemas = []

    sims =None
    dictionary = None
    tf_idf = None
    sent_tokenizer =None
    #variavel utilizada para realizar o doc2Vec
    model = None

    linguagem = ""
    CAMINHO_RAIZ = ""

    def __init__(self,linguagem,CAMINHO_RAIZ):

        tempo =self.time.time()
        self.linguagem = linguagem
        self.CAMINHO_RAIZ = CAMINHO_RAIZ

        ##ATUALIZAÇÃO GUSTAVO 11/12/2019
        with self.gzip.open(self.CAMINHO_RAIZ+"TitulosWikipedia_"+self.linguagem+".gz",'r') as arquivo:
            for linha in arquivo.readlines():
                    self.titulos.append(linha.decode('utf8'))

        # Obtem similaridades
        self.sims = self.gensim.similarities.Similarity.load(self.CAMINHO_RAIZ+"Analisadores\\similaridades_"+self.linguagem+".sims")

        # Obtem dicionario dos documentos
        self.dictionary = self.gensim.corpora.Dictionary.load(self.CAMINHO_RAIZ+"Analisadores\\dicionario_"+self.linguagem+".dict")
        
        #Obtem matriz similaridades
        self.tf_idf = self.gensim.models.TfidfModel.load(self.CAMINHO_RAIZ+"Analisadores\\tf_idf_"+self.linguagem+".tfidf_model")

        # Obtem Doc2Vec        
        self.model= self.Doc2Vec.load(self.CAMINHO_RAIZ+"Doc2Vec\\dv2_"+self.linguagem+".model")

        if(linguagem=='pt'):         

            self.sent_tokenizer=self.nltk.data.load('tokenizers/punkt/portuguese.pickle')   

            self.consultaSubtema("teste")

            lista = []
            self.buscaDoc2Vec_subTema(0,(0,0,0,0),lista)

            self.consultaTemaCentral("teste",85,3)
        elif(linguagem=='en'):       
    
            self.sent_tokenizer=self.nltk.data.load('tokenizers/punkt/english.pickle')   

            self.consultaSubtema("test")

            lista = []
            self.buscaDoc2Vec_subTema(0,(0,0,0,0),lista)

            self.consultaTemaCentral("test",85,3)
        elif(linguagem=='es'):

            self.sent_tokenizer=self.nltk.data.load('tokenizers/punkt/spanish.pickle')   

            self.consultaSubtema("prueba")

            lista = []
            self.buscaDoc2Vec_subTema(0,(0,0,0,0),lista)

            self.consultaTemaCentral("prueba",85,3)


        print("\n\nServidor iniciado em : %s \nTempo: %s \n" % (self.time.time()-tempo,self.datetime.datetime.now()))
    
    #################################################################################################    
    ##                               ÁREA DE CONSULTA DE TEMA CENTRAL                              ##
    #################################################################################################    

    def consultaStemming(self, termos, texto):
        #Cria documento que deseja saber a similaridade
        query_doc = self.preprocess_stemming.preProcess(texto,self.linguagem)
        #cria corpus desse documento
        query_doc_bow = self.dictionary.doc2bow(query_doc.split(' '))

        #cria tf-idf desse documento
        query_doc_tf_idf = self.tf_idf[query_doc_bow]

        #Com base no dicionario criado de titulos consigo exibir a qual titulo esse texto mais se adequa
        #index, value = max(enumerate(self.sims[query_doc_tf_idf]), key=self.operator.itemgetter(1))     
        
        #cria nova lista com os itens e valores
        novaLista = [value for index,value in enumerate(self.sims[query_doc_tf_idf])]
        
        retornoTemas =""
        #percorre para poder exibir a quantidade que foi selecionada
        for x in range(0,termos):
            #obtem o maior
            index,value = max(enumerate(novaLista), key=self.operator.itemgetter(1))
            #armazena o maior
            retornoTemas += str(x+1)+"|@@#_#@@|"+self.titulos[index]+"__"+str(index)+"|@@#_#@@|"+str(value)+"|@@##@@|"
            #deleta o maior da lista
            del novaLista[index] 

        return (retornoTemas,'','',self.datetime.datetime.now())

    def comparaCabeca(self,c1,c2):
        a,b,c,d = c1
        a1,b1,c1,d1 = c2
        return c==c1

    def verificaInter(self,g1,g2):
        for a,b,c,d,e in g1:
            for a1,b1,c1,d1,e1 in g2:
                if(c==c1):
                    return True
        return False

    def retornaTemaCentral(self, texto,taxaAceitacao,euristica):
                
        dadosParavisualziacao = ""
        
        print("\n\n******* TEMA CENTRAL ******* ")
        contagem = 1
        tempo = self.time.time()
        temaCentral = self.consultaTemaCentral(texto,taxaAceitacao,euristica)
        for t_t_indice,t_t_titulo,t_t_codTitulo,t_t_simTexto in temaCentral:            
            dadosParavisualziacao += str(contagem)+"|@@#_#@@|"+t_t_titulo+"|@@#_#@@|"+str(t_t_simTexto)+"|@@##@@|"
            contagem+=1
               
        print("\n\nTema Central encontrado em %s " % (self.time.time()-tempo))
        return (dadosParavisualziacao,'','',self.datetime.datetime.now())

    def consultaTemaCentral(self, texto,taxaAceitacao,euristica):
        
        resultado = []

        if(euristica==1):
            cabeca,grupoTema = self.euristica_busca1(texto,taxaAceitacao)
            a,b,c,d = cabeca
            resultado.append((a,b,c,d))
            for a,b,c,d,e in grupoTema:                   
                resultado.append((a,b,c,d))

        elif(euristica==2):
            cabeca,grupoTema = self.euristica_busca2(texto,taxaAceitacao)
            a,b,c,d = cabeca
            resultado.append((a,b,c,d))
            for a,b,c,d,e in grupoTema:                   
                resultado.append((a,b,c,d))

        elif(euristica==3):
            cabeca1,grupoTema1 =self.euristica_busca1(texto,taxaAceitacao)
            cabeca2,grupoTema2 =self.euristica_busca2(texto,taxaAceitacao)           

            igual2 = self.verificaInter(grupoTema1,grupoTema2) or self.comparaCabeca(cabeca1,cabeca2)

            #obtem itens grupo1 pois já é certeza que algum é igual
            a,b,c,d = cabeca1
            resultado.append((a,b,c,d))
            for a,b,c,d,e in grupoTema1:                   
                resultado.append((a,b,c,d))

            #obtem itens dos que são iguais
            if(igual2):
                a,b,c,d = cabeca2
                resultado.append((a,b,c,d))
                for a,b,c,d,e in grupoTema2:                   
                    resultado.append((a,b,c,d))            

        
        return sorted(list(set(resultado)),key=self.operator.itemgetter(3),reverse = True)
   
    def buscaDoc2Vec(self,id1,id2):
        return self.model.docvecs.similarity(str(id1),str(id2))

    def buscaDoc2Vec_Thread(self,id1,id2,lista_doc2vec_thread):        
        lista_doc2vec_thread.append((id2,self.model.docvecs.similarity(str(id1),str(id2))))

    """
    Essa euritica considera os 10 primeiros temas como os mais possiveis de estarem certos

    Compara cada um com os outros 99 obtendo a distancia entre cada um, em seguida realiza a limpeza
    dos temas que não estão dentro da taxa de aceitação. Após essa limpeza realiza a soma da proximidade
    dos temas restante em seguida retorna o possivel valor correto
    """
    def euristica_busca2(self,texto,taxaAceitacao):
        #Cria documento que deseja saber a similaridade
        query_doc = self.preprocess_stemming.preProcess(texto,self.linguagem)
        #cria corpus desse documento
        query_doc_bow = self.dictionary.doc2bow(query_doc.split(' '))

        #cria tf-idf desse documento
        query_doc_tf_idf = self.tf_idf[query_doc_bow]

        #Com base no dicionario criado de titulos consigo exibir a qual titulo esse texto mais se adequa
        #index, value = max(enumerate(self.sims[query_doc_tf_idf]), key=self.operator.itemgetter(1))     
        
        #cria nova lista com os itens e valores
        novaLista = [value for index,value in enumerate(self.sims[query_doc_tf_idf])]
        

        #OBTEM OS CEM TERMOS MAIS PROXIMOS E ARMAZENA

        cemTermosProximo = []
        #percorre 100 vezes para obter os 100 mais próximos termos
        for x in range(0,50):
            #obtem o maior
            index,value = max(enumerate(novaLista), key=self.operator.itemgetter(1))
            #armazena o maior em uma combinação de (indice, titulo, codTitulo, valorSimilaridade)
            cemTermosProximo.append((x,self.titulos[index],index,value))
            #deleta o maior da lista
            del novaLista[index] 

        """
        Cria uma nova lista com os dez primeiros termos mais proximo

        Cada uma dessa dez nova lista possui um cabeça, 
        esse cabeça será usado para realizar a comparação com todos os outros 100 termos
        """
        #Cria nova lista
        dezGruposTemas =[]
        #Realiza o loop 10 vezes para obter os novos dez vetores
        for i in range(0,10):
            #Cria uma lista temporaria para armazenar os 99 não cabeça
            listaTemp =[]
            #Cria a variavel que ira armazena o cabeça da lista
            cabecaLista = []
            #percorre pelos 100 mais proximos econtrados
            for termoProximo in cemTermosProximo:
                #Obtem o conjunto de informações de cada termo
                indice,titulo,codTitulo,simTexto = termoProximo

                #Verifica se o item é o cabeça
                if i!=indice:                 
                    #Caso não seja adiciona na lista temporaria   
                    listaTemp.append( (indice,titulo,codTitulo,simTexto))
                else:
                    #Caso seja armazena na variavel do cabeça
                    cabecaLista = (indice,titulo,codTitulo,simTexto)
            #Ao final do loop adiciona o cabeça mais a lista desse cabeça
            dezGruposTemas.append((cabecaLista,listaTemp))
        """
        Esse trecho realiza a comparação da similaridade entre o cabeça e todos os seus 99 subtemas

        Utilizando o doc2Vec
        """
        #Crio novo vetor para poder armazenar o resultado das buscar com doc2Vec
        dezGruposTemasDoc2Vec = []
        #Inicia loop pelos dez maiores temas
        for itemGrupo in dezGruposTemas:
            #obtem a cabeça do tema e o seu subGrupo
            cabeca,grupoTema = itemGrupo
            #obtem os campos da cabeça
            c_indice,c_titulo,c_codTitulo,c_simTexto = cabeca
            #cria uma lista temporaria para armazenar o novo resultado
            listaTemp =[]
            #percorro pelos subTemas da cabeça
            for tema in grupoTema:
                #armazeno os valores do tema
                t_indice,t_titulo,t_codTitulo,t_simTexto = tema
                #obtenho a semelhança dos subtemas com a cabeça
                t_doc2Vec = self.buscaDoc2Vec(c_codTitulo,t_codTitulo)
                #adiciono o tema mais o doc2vec na lista temporaria
                listaTemp.append((t_indice,t_titulo,t_codTitulo,t_simTexto,t_doc2Vec))
            #adiciono item com o doc2vec na nova lista
            dezGruposTemasDoc2Vec.append((cabeca,listaTemp))

        #zera listas anteriores
        cemTermosProximo = None
        dezGruposTemas = None
        listaTemp = None


        #reorganiza a lista com base nos valores do doc2vec
        dezGruposTemasDoc2Vec_Desc = []
        for itemGrupo in dezGruposTemasDoc2Vec:
            #obtem itens do grupos
            cabeca,grupoTema = itemGrupo            
            #reorganiza os itens em order decrescente pelo campo do doc2Vec
            grupoTema = sorted(grupoTema,key=self.operator.itemgetter(4),reverse = True)
            #cria nova lista com os itens dentro da taxa de aceitação
            novogrupoTema = []
            #obtem o primeiro item da lista
            maiorSimilaridade = grupoTema[0]
            
            c_indice,c_titulo,c_codTitulo,c_simTexto = cabeca
            
            #considera essa como 100 por cento
            t_indice,t_titulo,t_codTitulo,t_simTexto,maiorSemelhanca = maiorSimilaridade
            if(t_simTexto>=(c_simTexto/2)):

                novogrupoTema.append((t_indice,t_titulo,t_codTitulo,t_simTexto,maiorSemelhanca))
                #avança para poder partir da segunda
                grupoTema = grupoTema[1:]
                
                #percorre pelos grupos tema para verificar se estão dentro da taxa de aceitação
                for tema in grupoTema:
                    #obtem itens do tema
                    t_t_indice,t_t_titulo,t_t_codTitulo,t_t_simTexto,t_t_doc2Vec = tema
                    #verifica se está dentro da taxa de aceitação
                    if (((t_t_doc2Vec*100)/maiorSemelhanca)>=taxaAceitacao and (t_t_simTexto>=(c_simTexto/2))):
                        #caso esteja adiciona no novo grupo
                        novogrupoTema.append((t_t_indice,t_t_titulo,t_t_codTitulo,t_t_simTexto,t_t_doc2Vec))

            #adiciona o novo grupo ao doc2Vec desc
            dezGruposTemasDoc2Vec_Desc.append((cabeca,novogrupoTema))

        dezGruposTemasDoc2Vec = None
        
        #realiza o processo de encontrar qual cabeça possui o maior número de semelhanças com os seus subtemas

        #vetor par armazenar a combinação mais adequada
        temasMaisAdequadosEncontrados = None

        #variavel para descobrir maior soma
        maiorSomaDoc2Vec = 0
    
        #percorre por todos para encontrar o grupo com melhor soma
        for itemGrupo in dezGruposTemasDoc2Vec_Desc:
            #obtem itens do grupos
            cabeca,grupoTema = itemGrupo 
            #zera o valor da soma a cada loop
            soma = 0
            for tema in grupoTema:
                #obtem itens do tema
                t_t_indice,t_t_titulo,t_t_codTitulo,t_t_simTexto,t_t_doc2Vec = tema
                """
                #realiza a soma de todos os termos aceitaveis de um grupo
                soma +=t_t_doc2Vec
                """
                #teste realizando a soma com a proximidade do texto
                soma +=t_t_simTexto
            #verifica se esse grupo é a maior soma, caso seja, torna ele a melhor opção de resultado
            if soma>maiorSomaDoc2Vec:
                temasMaisAdequadosEncontrados =(cabeca,grupoTema)
      
        dezGruposTemasDoc2Vec_Desc = None

        return temasMaisAdequadosEncontrados

        """            
        #obtem a cabeca e os temas adequados para retornar
        cabeca,grupoTema = temasMaisAdequadosEncontrados 
      
        #variavel que retorna dados para exibir na tela
        dadosParavisualziacao = ""

        contagem = 1

        indice,titulo,codTitulo,simTexto = cabeca

        dadosParavisualziacao += str(contagem)+"|@@#_#@@|"+titulo+"|@@#_#@@|"+str(simTexto)+"|@@##@@|"
        #zera o valor da soma a cada loop

        for tema in grupoTema:
            contagem+=1
            #obtem itens do tema
            t_t_indice,t_t_titulo,t_t_codTitulo,t_t_simTexto,t_t_doc2Vec = tema
            dadosParavisualziacao += str(contagem)+"|@@#_#@@|"+t_t_titulo+"|@@#_#@@|"+str(t_t_simTexto)+"|@@##@@|"

        return (dadosParavisualziacao,'','',self.datetime.datetime.now())
        """

     
    """
    Essa euritica considera os o primeiro termo como o tema mais próximo do texto em seguida
    Compara o mesmo os outros 99 obtendo a distancia entre cada um, em seguida realiza a limpeza
    dos temas que não estão dentro da taxa de aceitação. Após essa limpeza retorna os itens dentro da taxa
    de aceitação
    """
    def euristica_busca1(self,texto,taxaAceitacao):
        #Cria documento que deseja saber a similaridade
        query_doc = self.preprocess_stemming.preProcess(texto,self.linguagem)
        #cria corpus desse documento
        query_doc_bow = self.dictionary.doc2bow(query_doc.split(' '))

        #cria tf-idf desse documento
        query_doc_tf_idf = self.tf_idf[query_doc_bow]

        #Com base no dicionario criado de titulos consigo exibir a qual titulo esse texto mais se adequa
        #index, value = max(enumerate(self.sims[query_doc_tf_idf]), key=self.operator.itemgetter(1))     
        
        #cria nova lista com os itens e valores
        novaLista = [value for index,value in enumerate(self.sims[query_doc_tf_idf])]        

        #OBTEM OS CEM TERMOS MAIS PROXIMOS E ARMAZENA

        cemTermosProximo = []
        #percorre 100 vezes para obter os 100 mais próximos termos
        for x in range(0,50):
            #obtem o maior
            index,value = max(enumerate(novaLista), key=self.operator.itemgetter(1))
            #armazena o maior em uma combinação de (indice, titulo, codTitulo, valorSimilaridade)
            cemTermosProximo.append((x,self.titulos[index],index,value))
            #deleta o maior da lista
            del novaLista[index] 

        """
        Cria uma nova lista com os dez primeiros termos mais proximo

        Cada uma dessa dez nova lista possui um cabeça, 
        esse cabeça será usado para realizar a comparação com todos os outros 100 termos
        """
        #Cria nova lista
        gruposTema = None
        
        #Cria uma lista temporaria para armazenar os 99 não cabeça
        listaTemp =[]
        #Cria a variavel que ira armazena o cabeça da lista
        cabecaLista = []
        #percorre pelos 100 mais proximos econtrados
        for termoProximo in cemTermosProximo:
            #Obtem o conjunto de informações de cada termo
            indice,titulo,codTitulo,simTexto = termoProximo

            #Verifica se o item é o cabeça
            if indice!=0:                 
                #Caso não seja adiciona na lista temporaria   
                listaTemp.append( (indice,titulo,codTitulo,simTexto))
            else:
                #Caso seja armazena na variavel do cabeça
                cabecaLista = (indice,titulo,codTitulo,simTexto)
        #Ao final do loop adiciona o cabeça mais a lista desse cabeça
        gruposTema = (cabecaLista,listaTemp)
        """
        Esse trecho realiza a comparação da similaridade entre o cabeça e todos os seus 99 subtemas

        Utilizando o doc2Vec
        """

        #obtem a cabeça do tema e o seu subGrupo
        cabeca,grupoTema = gruposTema
        #obtem os campos da cabeça
        c_indice,c_titulo,c_codTitulo,c_simTexto = cabeca
        #cria uma lista temporaria para armazenar o novo resultado
        listaTemp =[]
        #percorro pelos subTemas da cabeça
        for tema in grupoTema:
            #armazeno os valores do tema
            t_indice,t_titulo,t_codTitulo,t_simTexto = tema
            #obtenho a semelhança dos subtemas com a cabeça
            t_doc2Vec = self.buscaDoc2Vec(c_codTitulo,t_codTitulo)
            #adiciono o tema mais o doc2vec na lista temporaria
            listaTemp.append((t_indice,t_titulo,t_codTitulo,t_simTexto,t_doc2Vec))
        #adiciono item com o doc2vec na nova lista
        gruposTema =(cabeca,listaTemp)

        #zera listas anteriores
        cemTermosProximo = None

        listaTemp = None

        #obtem itens do grupos
        cabeca,grupoTema = gruposTema            
        #reorganiza os itens em order decrescente pelo campo do doc2Vec
        grupoTema = sorted(grupoTema,key=self.operator.itemgetter(4),reverse = True)
        #cria nova lista com os itens dentro da taxa de aceitação
        novogrupoTema = []
        #obtem o primeiro item da lista
        maiorSimilaridade = grupoTema[0]
        
        
        c_indice,c_titulo,c_codTitulo,c_simTexto = cabeca
        
        #considera essa como 100 por cento
        t_indice,t_titulo,t_codTitulo,t_simTexto,maiorSemelhanca = maiorSimilaridade
        if(t_simTexto>=(c_simTexto/2)):
   

            novogrupoTema.append((t_indice,t_titulo,t_codTitulo,t_simTexto,maiorSemelhanca))
            #avança para poder partir da segunda
            grupoTema = grupoTema[1:]
            
            #percorre pelos grupos tema para verificar se estão dentro da taxa de aceitação
            for tema in grupoTema:
                #obtem itens do tema
                t_t_indice,t_t_titulo,t_t_codTitulo,t_t_simTexto,t_t_doc2Vec = tema
                #verifica se está dentro da taxa de aceitação
                if (((t_t_doc2Vec*100)/maiorSemelhanca)>=taxaAceitacao and (t_t_simTexto>=(c_simTexto/2))):
                    #caso esteja adiciona no novo grupo
                    novogrupoTema.append((t_t_indice,t_t_titulo,t_t_codTitulo,t_t_simTexto,t_t_doc2Vec))

        #adiciona o novo grupo ao doc2Vec desc
        return (cabeca,novogrupoTema)
        """ 
        #variavel que retorna dados para exibir na tela
        dadosParavisualziacao = ""

        contagem = 1  

        indice,titulo,codTitulo,simTexto = cabeca

        dadosParavisualziacao += str(contagem)+"|@@#_#@@|"+titulo+"|@@#_#@@|"+str(simTexto)+"|@@##@@|"
        #zera o valor da soma a cada loop

        for tema in novogrupoTema:
            contagem+=1
            #obtem itens do tema
            t_t_indice,t_t_titulo,t_t_codTitulo,t_t_simTexto,t_t_doc2Vec = tema
            dadosParavisualziacao += str(contagem)+"|@@#_#@@|"+t_t_titulo+"|@@#_#@@|"+str(t_t_simTexto)+"|@@##@@|"

        return (dadosParavisualziacao,'','',self.datetime.datetime.now())
        """
    #################################################################################################   

    def retornaTema_subTema(self,texto,taxaAceitacao,euristica):
        resultado_temaCentral = ""
        resultado_subTemas =""
        resultado_grafo_retorno=""

        print("\n\n\n\n******* INICIANDO NOVA BUSCA ******* ")        

        print("\n******* TEMA CENTRAL ******* ")        
        tempo = self.time.time()
        temaCentral = self.consultaTemaCentral(texto,taxaAceitacao,euristica)   

        print("\n\nTema Central encontrado em %s " % (self.time.time()-tempo))
        
        tempo = self.time.time()        
        print("\n\n******* SUBTEMAS ******* ")
        subTemas = self.consultaSubtema(texto)
        print("\n\nSubTemas encontrados em %s " % (self.time.time()-tempo))
        

        subTemaSimilaridadeTema = []

        #realiza verificação de similaridade dos subtemas com o tema
        t_t_indice,t_t_titulo,t_t_codTitulo,t_t_simTexto = temaCentral[0]

        for t_sub_titulo,t_sub_codTitulo,t_sub_simTexto in subTemas: 
            if(not self.existeItemLista_Geral(t_sub_codTitulo,t_sub_titulo,temaCentral)):
                self.buscaDoc2Vec_subTema(t_t_codTitulo,(0,t_sub_titulo,t_sub_codTitulo,t_sub_simTexto),subTemaSimilaridadeTema)
        
        
        subTemaSimilaridadeTema_retorno = []
        resultado_retorno = []
        if(len(subTemaSimilaridadeTema)>0):
            #reordena para obter o maior
            subTemaSimilaridadeTema_retorno = sorted(subTemaSimilaridadeTema, key=self.operator.itemgetter(4),reverse = True)
            
            resultado_retorno = []
            
            #obtem a maior similaridade para considerar como 100% na taxa de aceitação
            indice,titulo,id_titulo,sim_texto,similar = subTemaSimilaridadeTema_retorno[0]
        
            #Armazena item
            resultado_retorno.append((titulo,id_titulo,sim_texto))
            
            #percorre pelos grupos tema para verificar se estão dentro da taxa de aceitação
            for tema in subTemaSimilaridadeTema_retorno[1:]:
                #obtem itens do tema
                indice,titulo,id_titulo,sim_texto,t_similar = tema
                #verifica se está dentro da taxa de aceitação
                if ((t_similar*100)/similar)>=(taxaAceitacao-20) :
                    #caso esteja adiciona no novo grupo
                    resultado_retorno.append((titulo,id_titulo,sim_texto))
                    
            #reordena de acordo com a similaridade com a sentença
            resultado_retorno = sorted(resultado_retorno, key=self.operator.itemgetter(2),reverse = True)
        

        #Cria lista unica com tema e subtema
        #cod_titulo,titulo,simTexto,tipo
        lista_unica = []

        for t_t_indice,t_t_titulo,t_t_codTitulo,t_t_simTexto in temaCentral:  
            if(not self.existeItemLista_Final(t_t_codTitulo,t_t_titulo,lista_unica)):
                lista_unica.append((t_t_codTitulo,t_t_titulo,t_t_simTexto,"TC"))

        for titulo,id_titulo,sim_texto in resultado_retorno:
            if(not self.existeItemLista_Final(id_titulo,titulo,lista_unica)):
                lista_unica.append((id_titulo,titulo,sim_texto,"SB"))

        
        #encontra similaridade de todos com todos para poder fazer o grafo
        lista_doc2vecGeral = []
        
        threads = []

        for cod_titulo,titulo,simTexto,tipo in lista_unica:
            lista_doc2vec = []
            lista_doc2vecGeral.append((cod_titulo,titulo,simTexto,tipo,lista_doc2vec))
            for cod_titulo2,titulo2,simTexto2,tipo2 in lista_unica:
                if(cod_titulo!=cod_titulo2):
                    threads.append(self.threading.Thread(target=self.buscaDoc2Vec_Thread, args=(cod_titulo,cod_titulo2,lista_doc2vec,)))
        
    
        [t.start() for t in threads]
        [t.join() for t in threads]


        #gera os nós e a ligação de cada nó
        resultado_grafo = []
        #calcula as ligações mais fortes
        for cod_titulo,titulo,simTexto,tipo,lista_doc2vec in lista_doc2vecGeral:
            novosArestasGrafo = []
            if(len(lista_doc2vec)>0):
                
                lista_doc2vec = sorted(lista_doc2vec, key=self.operator.itemgetter(1),reverse = True)
                idMaior,maiorSims = lista_doc2vec[0]
                if(not self.existeRelacao(cod_titulo,idMaior,resultado_grafo)):
                    if(maiorSims>=65):
                        novosArestasGrafo.append((idMaior,maiorSims))
                for idMaior_sub,maiorSims_sub in lista_doc2vec[1:]:
                    #print(((maiorSims_sub*100)/maiorSims))
                    if(((maiorSims_sub*100)/maiorSims)>=80):
                        if(not self.existeRelacao(cod_titulo,idMaior_sub,resultado_grafo)):
                            novosArestasGrafo.append((idMaior_sub,maiorSims_sub))
            
            resultado_grafo.append((cod_titulo,titulo,simTexto,tipo,novosArestasGrafo))


        #Escreve grafo na estrutura de json
        resultado_grafo_retorno = "["
        for cod_titulo,titulo,simTexto,tipo,lista_doc2vec in resultado_grafo:
            resultado_grafo_retorno+="{\"cod_titulo\":"+str(cod_titulo)+",\"titulo\":\""+str(titulo.replace('\n', ''))+"\",\"similaridade\":"+str(simTexto)+", \"tipo\":\""+str(tipo)+"\",\"conexoes\":"
            if(len(lista_doc2vec)>0):
                resultado_grafo_retorno+="["
                for idMaior_sub,maiorSims_sub in lista_doc2vec:
                    resultado_grafo_retorno+="{\"cod_titulo\":"+str(idMaior_sub)+"},"
                resultado_grafo_retorno = resultado_grafo_retorno[:-1] + "]},"
            else:
                resultado_grafo_retorno+="null},"
            
        if(len(resultado_grafo_retorno)>1):    
            resultado_grafo_retorno = resultado_grafo_retorno[:-1]+"]"
        else:
            resultado_grafo_retorno = "[]"




        resultado_temaCentral =""  
        contagem = 1 
        for cod_titulo,titulo,simTexto,tipo in lista_unica:
            if(tipo=="TC"):              
                resultado_temaCentral += str(contagem)+"|@@#_#@@|"+str(titulo)+"_"+str(cod_titulo)+"|@@#_#@@|"+str(simTexto)+"|@@##@@|"
                contagem+=1  


        contagem = 1
        resultado_subTemas = ""
        for cod_titulo,titulo,simTexto,tipo in lista_unica:
            if(tipo=="SB"):             
                resultado_subTemas += str(contagem)+"|@@#_#@@|"+str(titulo)+"_"+str(cod_titulo)+"|@@#_#@@|"+str(simTexto)+"|@@##@@|"
                contagem+=1

        return (resultado_temaCentral,resultado_subTemas,resultado_grafo_retorno,self.datetime.datetime.now())

    def existeItemLista_Geral(self,cod,tit,lista):
        for a1,b1,c1,d1 in lista:
            if str.lower(b1)==str.lower(tit) or c1==cod:
                return True
        return False

    def existeItemLista_Final(self,cod,tit,listaFim):
        if(len(listaFim)<=0): return False
        for a1,b1,c1,d1 in listaFim:
            if str.lower(b1)==str.lower(tit) or a1==cod:
                return True
        return False

    def existeRelacao(self,atual,comparar,listaComparar):
        for a,b,c,d,e in listaComparar:
            if a==comparar:
                for a1,b1 in e:                    
                    if(a1==atual):
                        return True
        return False

    #################################################################################################    
    ##                                  ÁREA DE CONSULTA DE SUBTEMAS                               ##
    #################################################################################################    

    def retornaSubtemas(self, texto):
                
        dadosParavisualziacao = ""

        contagem = 1
        tempo = self.time.time()
        
        print("\n\n******* SUBTEMAS ******* ")
        subTemas = self.consultaSubtema(texto)
        for t_t_titulo,t_t_codTitulo,t_t_simTexto in subTemas:            
            dadosParavisualziacao += str(contagem)+"|@@#_#@@|"+t_t_titulo+"|@@#_#@@|"+str(t_t_simTexto)+"|@@##@@|"
            contagem+=1
        
        print("\n\nSubTemas encontrados em %s " % (self.time.time()-tempo))
        return (dadosParavisualziacao,'','',self.datetime.datetime.now())

    def consultaSubtema(self, texto):
        #obtem as sentenças do texto
        sentencasTexto = self.obtemSentencas(texto)  

        print("\nQuantidade de sentenças a processar: %s \nTempo estimado: %ss" % (len(sentencasTexto),((len(sentencasTexto)/2)+ (len(sentencasTexto)/4)+1.5)))

        #variavel que irá armazenar os subtemas encontrados
        resultado_geral = []

        #Cria as threads para realizar processo paralelo
        threads = [self.threading.Thread(target=self.busca_subTemas, args=(texto,resultado_geral,)) for texto in sentencasTexto]
        [t.start() for t in threads]
        [t.join() for t in threads]


        
        return self.obtemSubTemasContexto(resultado_geral)            
    
    def obtemSubTemasContexto(self,subTemasEncontrados):
        #Variavel para armazenar os temos não repetidos
        temasEncontrados = []
        
        #percorre lista para remover os termos não repeditos
        for resul in subTemasEncontrados:
            for indice,titulo,id_titulo,sim_texto in resul:
                if(not self.existeItemLista(id_titulo,titulo,temasEncontrados) and sim_texto>0.10):
                    temasEncontrados.append((titulo,id_titulo,sim_texto))
        
        #Percorre a lista obtendo a soma das similaridades com todos os outros itens da lista
        resultado_contexto= []
        for titulo,id_titulo,sim_texto in temasEncontrados:
            similar = 0
            for t_titulo,t_id_titulo,t_sim_texto in temasEncontrados:
                similar += self.model.docvecs.similarity(str(id_titulo),str(t_id_titulo))
            resultado_contexto.append((titulo,id_titulo,sim_texto,similar))
        
        #reordena para obter o maior
        resultado_contexto = sorted(resultado_contexto, key=self.operator.itemgetter(3),reverse = True)
        
        resultado_retorno = []
        
        #obtem a maior similaridade para considerar como 100% na taxa de aceitação
        titulo,id_titulo,sim_texto,similar = resultado_contexto[0]
    
        #Armazena item
        resultado_retorno.append((titulo,id_titulo,sim_texto))
        
        #percorre pelos grupos tema para verificar se estão dentro da taxa de aceitação
        for tema in resultado_contexto[1:]:
            #obtem itens do tema
            titulo,id_titulo,sim_texto,t_similar = tema
            #verifica se está dentro da taxa de aceitação
            if ((t_similar*100)/similar)>=65 :
                #caso esteja adiciona no novo grupo
                resultado_retorno.append((titulo,id_titulo,sim_texto))
        
        #reordena de acordo com a similaridade com a sentença
        resultado_retorno = sorted(resultado_retorno, key=self.operator.itemgetter(2),reverse = True)

        return resultado_retorno

    def existeItemLista(self,cod,tit,lista):
        if(len(lista)<0):
            return False
        for a1,b1,c1 in lista:
            if str.lower(a1)==str.lower(tit) or b1==cod:
                return True
        return False


    def obtemSentencas(self,texto):
        #Realiza tokenização já realizando também o preprocessamento do texto
        sentencas = self.sent_tokenizer.tokenize(self.preprocess_stemming.preProcess(texto,self.linguagem))

        #variavel para aceitação de tamanho minimo de sentenca
        minSent = 255

        #variavel que armazena as novas sentencas geradas
        novasSentecas = []

        #variavel que agrupa as sentencas para chegar ao tamanho desejado
        groupSent = ""

        #Percorre pelas sentenças para saber se todas estão no tamanho aceitavel
        for sentenca in sentencas:
            #verifica se o tamanho da sentença é maior que o minimo
            if len(sentenca) < minSent:
                #Caso não seja agrupo
                groupSent += sentenca
                
                #verifica se o grupo é maior que o aceitavel
                if len(groupSent) >= minSent:
                    #Caso seja adiciona a sentenca e limpa o grupo
                    novasSentecas.append(groupSent)
                    groupSent = ""
            #caso o tamanho da sentenca seja aceitavel verifica se tem algo a agrupar
            else:                
                if(groupSent != ""):
                    novasSentecas.append(groupSent+" "+sentenca)
                else:
                    novasSentecas.append(sentenca)
                groupSent = ""
        #Verifica se as novas sentenças foram criadas caso não adiciona uma sentença que não tem o tamanno minino
        if len(novasSentecas) == 0:
            novasSentecas.append(groupSent)
            groupSent = ""
        else:
            if(groupSent != ""):
                novasSentecas[-1] += " "+ groupSent
                groupSent = ""
        
        #retorna as sentenças criadas
        return novasSentecas

    def busca_subTemas(self,texto,resultado_geral):
        #cria corpus desse documento
        query_doc_bow = self.dictionary.doc2bow(texto.split(' '))
        

        #cria tf-idf desse documento
        query_doc_tf_idf = self.tf_idf[query_doc_bow]
        
        #obtem resultado similaridade
        resultado = list(self.sims[query_doc_tf_idf])
        
        #reoordena resultados em ordem crescente
        resultado = sorted(enumerate(resultado), key=self.operator.itemgetter(1),reverse = True)
        
        temasMaisProximos = []
        #percorre obter o nome dos mais proximos
        for indice,resul in enumerate(resultado[:50]):        
            index,value = resul
            temasMaisProximos.append((indice,self.titulos[index],index,value))    
    
        #considera o primeiro como o mais correto
        cabecaLista = temasMaisProximos[0]
        
        #armazena o restante para obter os valores de similaridades em relação ao primeiro
        restanteItens = temasMaisProximos[1:]
        
        #obtem separadamente os itens da cabeça
        c_indice,c_titulo,c_codTitulo,c_simTexto = cabecaLista
        
        #matriz que irá armazenar o resultado das similaridaes dos itens em relação a cabeça
        resultadosDoc2Vec = []
        [self.buscaDoc2Vec_subTema(c_codTitulo,item,resultadosDoc2Vec) for item in restanteItens]

        #realiza ordenação dos resultados obtidos
        resultadosDoc2Vec = sorted(resultadosDoc2Vec,key=self.operator.itemgetter(4),reverse = True)

        temasMaisProximos = []
        
        #obtem a maior similaridade para considerar como 100% na taxa de aceitação
        t_indice,t_titulo,t_codTitulo,t_simTexto,maiorSemelhanca = resultadosDoc2Vec[0]
        
        #Verifica se esse item tem mais de 50% de semelahnça com a sentença
        if(t_simTexto>=(c_simTexto/2)):
    
            #Armazena item
            temasMaisProximos.append((t_indice,t_titulo,t_codTitulo,t_simTexto,maiorSemelhanca))
            
            #percorre pelos grupos tema para verificar se estão dentro da taxa de aceitação
            for tema in resultadosDoc2Vec[1:]:
                #obtem itens do tema
                t_t_indice,t_t_titulo,t_t_codTitulo,t_t_simTexto,t_t_doc2Vec = tema
                #verifica se está dentro da taxa de aceitação
                if (((t_t_doc2Vec*100)/maiorSemelhanca)>=85 and (t_t_simTexto>=(c_simTexto/2))):
                    #caso esteja adiciona no novo grupo
                    temasMaisProximos.append((t_t_indice,t_t_titulo,t_t_codTitulo,t_t_simTexto,t_t_doc2Vec))
        
        resultado_final = []
        
        resultado_final.append((c_indice,c_titulo,c_codTitulo,c_simTexto))
        
        [resultado_final.append((t_indice,t_titulo,t_codTitulo,t_simTexto)) for t_indice,t_titulo,t_codTitulo,t_simTexto,t_doc2Vec in temasMaisProximos]
        
        resultado_geral.append(resultado_final)

    def buscaDoc2Vec_subTema(self,codPrincipal,item,lista):
        t_indice,t_titulo,t_codTitulo,t_simTexto = item
        lista.append((t_indice,t_titulo,t_codTitulo,t_simTexto,self.model.docvecs.similarity(str(codPrincipal),str(t_codTitulo))))
   
   #################################################################################################    

