# coding: utf-8
import sys
from pacotesMG.dataBaseFunctionMG import *
from pacotesMG.diversos import *

class Garrafa():
    idGarrafa = 0
    nomeGarrafa = ''
    volume = 0

    def __init__(self):

        self.conexao = ConMG('parametros.json')

        if self.conexao.con == None:
            sys.exit()

    def getAll(self):
        clausulaSql  = 'select idgarrafa, nomegarrafa, volume '
        clausulaSql += 'from garrafa order by volume;'

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler tipos de garafas', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append([row[0], row[1], row[2]])

            row = self.conexao.cursor.fetchone()

        return lista

    def pesquisaGarrafa(self, chave):
        clausulaSql = "select idgarrafa, nomegarrafa from garrafa where "
        clausulaSql += " upper(nomegarrafa) like upper('%" + chave + "%') order by nomegarrafa;"

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao pesquisar garrafa', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append(str(row[0]) + '|' + row[1])

            row = self.conexao.cursor.fetchone()

        return lista

    def buscaGarrafaPorNome(self, chave):
        clausulaSql = "select idgarrafa, nomegarrafa, volume from garrafa where "
        clausulaSql += " upper(nomegarrafa) = upper('" + chave + "');"

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao pesquisar garrafa', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()

        if row != None:
            lista.clear()
            lista.append(row[0])
            lista.append(row[1])
            lista.append(row[2])

        return lista

    def buscaGarrafa(self, argId):
        clausulaSql  = 'select idgarrafa, nomegarrafa, volume '
        clausulaSql += 'from garrafa ' + 'where idgarrafa = ' + str(argId) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao buscar garrafa com ID ' + str(argId) + '!',
                                   wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        if row != None:
            lista.append(row[0])
            lista.append(row[1])
            lista.append(row[2])

        return lista

    def setidGarrafa(self, arg):
        self.idGarrafa = arg

    def setnomeGarrafa(self, arg):
        self.nomeGarrafa = arg

    def setvolume(self, arg):
        self.volume = arg

    def insere(self):
        clausulaSql = "insert into garrafa (nomegarrafa, volume) values ("
        clausulaSql += "'" + tiraAspas(self.nomeGarrafa) + "', "
        clausulaSql += str(self.volume) + ");"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao inserir dados da garrafa!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def update(self, argId):
        clausulaSql = "update garrafa set "
        clausulaSql += "nomegarrafa = '" + tiraAspas(self.nomeGarrafa) + "', "
        clausulaSql += "volume = " + str(self.volume) + " "
        clausulaSql += "where idgarrafa = " + str(argId) + ";"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao atualizar os dados da garrafa!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def delete(self, argId):
        clausulaSql = 'delete from garrafa '
        clausulaSql += 'where idgarrafa = ' + str(argId) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao eliminar os dados da garrafa!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def sqlBuscaTamanho(self, coluna):
        if self.conexao.banco == 'postgres':
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_catalog = 'adega' and table_name = 'garrafa'"
            clausulaSql += "and column_name = '" + coluna + "';"
        else:
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_name = 'garrafa' and column_name = '" + coluna + "';"

        try:
            self.conexao.cursor.execute(clausulaSql)
            row = self.conexao.cursor.fetchone()
            while row != None:
                return row[0]
        except:
            return 0



