# coding: utf-8
import sys
from pacotesMG.conectaDataBaseMG import *
from pacotesMG.diversos import *
from pacotesMG.dataBaseFunctionMG import *

class Apelacao():
    idApelacao = 0
    nomeApelacao = ''
    corCasca = 0
    idPais = 0
    nomePais = ''

    def __init__(self):

        self.conexao = ConMG('parametros.json')

        if self.conexao.con == None:
            sys.exit()

    def getAll(self):
        clausulaSql  = 'select a.idapelacao, a.nomeapelacao, a.idpais, p.nomepais '
        clausulaSql += 'from apelacao as a join pais as p on a.idpais = p.idpais '
        clausulaSql += 'order by a.nomeapelacao;'

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler apelações', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append([row[0], row[1], row[2], row[3]])

            row = self.conexao.cursor.fetchone()

        return lista

    def pesquisaApelacao(self, chave):
        clausulaSql = "select idapelacao, nomeapelacao from apelacao where "
        clausulaSql += " upper(nomeapelacao) like upper('%" + chave + "%') order by nomeapelacao;"

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao pesquisar apelação', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append(str(row[0]) + '|' + row[1])

            row = self.conexao.cursor.fetchone()

        return lista

    def buscaApelacaoPorNome(self, chave):
        clausulaSql = "select idapelacao, nomeapelacao from apelacao where "
        clausulaSql += " upper(nomeapelacao) = upper('" + chave + "');"

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao pesquisar apelação', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()

        if row != None:
            lista.clear()
            lista.append(row[0])
            lista.append(row[1])

        return lista

    def buscaApelacao(self, argId):
        clausulaSql  = 'select a.idapelacao, a.nomeapelacao, a.idpais, p.nomepais '
        clausulaSql += 'from apelacao as a join pais as p on a.idpais = p.idpais '
        clausulaSql += 'where a.idapelacao = '
        clausulaSql += str(argId) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao buscar apelação com ID ' + str(argId) + '!',
                                   wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        if row != None:
            lista.append(row[0])
            lista.append(row[1])
            lista.append(row[2])
            lista.append(row[3])

        return lista

    def buscaIdApelacao(self, argNome):
        clausulaSql = "select idapelacao "
        clausulaSql += "from apelacao where nomeapelacao = '" + argNome + "';"

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao buscar apelação pelo nome ' + argNome + '!',
                                   wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        row = self.conexao.cursor.fetchone()

        idApelacao = 0
        if row != None:
            idApelacao =row[0]

        return idApelacao

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
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao inserir dados da apelação!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def update(self, argId):
        clausulaSql = "update apelacao set "
        clausulaSql += "nomeapelacao = '" + tiraAspas(self.nomeApelacao) + "', "
        clausulaSql += "idpais = " + str(self.idPais) + " "
        clausulaSql += "where idapelacao = " + str(argId) + ";"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao atualizar os dados da apelação!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def delete(self, argId):
        clausulaSql = 'delete from apelacao '
        clausulaSql += 'where idapelacao = ' + str(argId) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao eliminar os dados da apelação!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def sqlBuscaTamanho(self, coluna):
        if self.conexao.banco == 'postgres':
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_catalog = 'adega' and table_name = 'apelacao'"
            clausulaSql += "and column_name = '" + coluna + "';"
        else:
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_name = 'apelacao' and column_name = '" + coluna + "';"

        try:
            self.conexao.cursor.execute(clausulaSql)
            row = self.conexao.cursor.fetchone()
            while row != None:
                return row[0]
        except:
            return 0



