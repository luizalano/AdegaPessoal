# coding: utf-8
from pacotesMG.conectaDataBaseMG import *
from pacotesMG.diversos import *

class Apelacao():
    idApelacao = 0
    nomeApelacao = ''
    corCasca = 0
    idPais = 0
    nomePais = ''
    banco = 'mysql'

    def __init__(self):

        #self.con, self.cursor = conectaMySql('masteradega', 'Adeg@W!ne1', 'adega.mysql.uhserver.com', 'adega')
        listacon = conectaBanco('mysql', 'masteradega', 'Adeg@W!ne1', 'adega.mysql.uhserver.com', 'adega', 0)
        self.con = listacon[0]
        self.cursor = listacon[1]

        if self.con == None:
            sys.exit()

    def getAll(self):
        clausulaSql  = 'select a.idapelacao, a.nomeapelacao, a.idpais, p.nomepais '
        clausulaSql += 'from apelacao as a join pais as p on a.idpais = p.idpais '
        clausulaSql += 'order by a.nomeapelacao;'

        try:
            self.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler apelações', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.cursor.fetchone()
        while row != None:
            lista.append([row[0], row[1], row[2], row[3]])

            row = self.cursor.fetchone()

        return lista

    def pesquisaApelacao(self, chave):
        clausulaSql = "select idapelacao, nomeapelacao from apelacao where "
        clausulaSql += " upper(nomeapelacao) like upper('%" + chave + "%') order by nomeapelacao;"

        try:
            self.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao pesquisar apelação', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.cursor.fetchone()
        while row != None:
            lista.append(str(row[0]) + '|' + row[1])

            row = self.cursor.fetchone()

        return lista

    def buscaApelacao(self, argId):
        clausulaSql  = 'select a.idapelacao, a.nomeapelacao, a.idpais, p.nomepais '
        clausulaSql += 'from apelacao as a join pais as p on a.idpais = p.idpais '
        clausulaSql += 'where a.idapelacao = '
        clausulaSql += str(argId) + ';'

        try:
            self.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao buscar apelação com ID ' + str(argId) + '!',
                                   wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.cursor.fetchone()
        if row != None:
            lista.append(row[0])
            lista.append(row[1])
            lista.append(row[2])
            lista.append(row[3])

        return lista

    def setidApelacao(self, arg):
        self.idApelacao = arg

    def setnomeApelacao(self, arg):
        self.nomeApelacao = arg

    def setidPais(self, arg):
        self.idPais = arg

    def insere(self):
        clausulaSql = "insert into apelacao (nomeapelacao, idpais) values ("
        clausulaSql += "'" + tiraAspas(self.nomeApelacao) + "', "
        clausulaSql += str(self.idPais) + ");"

        try:
            self.cursor.execute(clausulaSql)
            self.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao inserir dados da apelação!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def update(self, argId):
        clausulaSql = "update apelacao set "
        clausulaSql += "nomeapelacao = '" + tiraAspas(self.nomeApelacao) + "', "
        clausulaSql += "idpais = " + str(self.idPais) + " "
        clausulaSql += "where idapelacao = " + str(argId) + ";"

        try:
            self.cursor.execute(clausulaSql)
            self.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao atualizar os dados da apelação!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def delete(self, argId):
        clausulaSql = 'delete from apelacao '
        clausulaSql += 'where idapelacao = ' + str(argId) + ';'

        try:
            self.cursor.execute(clausulaSql)
            self.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao eliminar os dados da apelação!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def sqlBuscaTamanho(self, coluna):
        if self.banco == 'postgres':
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_catalog = 'adega' and table_name = 'apelacao'"
            clausulaSql += "and column_name = '" + coluna + "';"
        else:
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_name = 'apelacao' and column_name = '" + coluna + "';"

        try:
            self.cursor.execute(clausulaSql)
            row = self.cursor.fetchone()
            while row != None:
                return row[0]
        except:
            return 0



