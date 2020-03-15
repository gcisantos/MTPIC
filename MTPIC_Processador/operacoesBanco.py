class OperacoesBanco:
    import sqlite3
    from sqlite3 import Error

    conexao = None
    
    def __init__(self, arquivo,parametros):        
        self.conexao = self.cria_conexao(arquivo)
        self.define_configuracoes(parametros)    

    def cria_conexao(self, arquivo):
        try:
            conexao = self.sqlite3.connect(arquivo)
            return conexao
        except self.Error as e:
            print(e)

        return None

    def itens_pendentes(self):
        cur = self.conexao.cursor()

        cur.execute(
            "SELECT id_busca,texto_busca,taxaAceitacao,euristicaProcessamento,tipoBusca FROM processamento_buscas where processado_busca = 0")

        rows = cur.fetchall()

        return rows

    def define_configuracoes(self,parametros):        
        try:
            
            sql = '''delete from processamento_configuracoes where id_config = 1 '''
            cur = self.conexao.cursor()
            cur.execute(sql)
            self.conexao.commit()

            sql='''Insert into 
            processamento_configuracoes(id_config,idioma,linguagem,caminho_raiz_programas,caminho_padrao_arquivo) 
            values(?,?,?,?,?)'''
            cur = self.conexao.cursor()
            cur.execute(sql,parametros)
            self.conexao.commit()

        except self.Error as e:
            print(e)




    def itens_processado(self,id_processado):
        cur = self.conexao.cursor()

        cur.execute("SELECT processado_busca,resultadoTema_busca FROM processamento_buscas where id_busca = ?",id_processado)

        rows = cur.fetchall()

        return rows

    def processa_item(self, parametros):
        try:
            sql = '''update processamento_buscas set 
            resultadoTema_busca =?,
            dataFim_busca =?,processado_busca = 1 where id_busca = ? '''
            cur = self.conexao.cursor()
            cur.execute(sql, parametros)
            self.conexao.commit()
        except self.Error as e:
            print(e)

    
    def processa_item_sub(self, parametros):
        try:
            sql = '''update processamento_buscas set 
            resultadoAssuntos_proximidades_busca =?,
            dataFim_busca =?,processado_busca = 1 where id_busca = ? '''
            cur = self.conexao.cursor()
            cur.execute(sql, parametros)
            self.conexao.commit()
        except self.Error as e:
            print(e)

    def processa_item_sub_Tema(self, parametros):
        try:
            sql = '''update processamento_buscas set 
            resultadoTema_busca =?,
            resultadoAssuntos_proximidades_busca =?,
            resultado_Grafo = ?,
            dataFim_busca =?,processado_busca = 1 where id_busca = ? '''
            cur = self.conexao.cursor()
            cur.execute(sql, parametros)
            self.conexao.commit()
        except self.Error as e:
            print(e)

    def cadastra_item(self,parametros):
        try:
            sql="Insert into processamento_buscas(texto_busca,taxaAceitacao,euristicaProcessamento,dataIni_busca) values(?,?,?)"
            cur = self.conexao.cursor()
            cur.execute(sql, parametros)
            self.conexao.commit()
            return cur.lastrowid
        except self.Error as e:
            print(e)    