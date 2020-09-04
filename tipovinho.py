# coding: utf-8
from pacotesMG.dataBaseFunctionMG import *
from pacotesMG.diversos import *


class TipoVinho():
    idTipoVinho = 0
    nomeTipoVinho = ''

    def __init__(self):
        self.conexao = ConMG('parametros.json')

        if self.conexao.con == None:
            sys.exit()

    def getAll(self):
        clausulaSql  = 'select idtipovinho, nometipovinho '
        clausulaSql += 'from tipovinho  '
        clausulaSql += 'order by nometipovinho;'

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler tipos de vinhos', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append([row[0], row[1]])

            row = self.conexao.cursor.fetchone()

        return lista

    def pesquisaTipoVinho(self, chave):
        clausulaSql = "select idtipovinho, nometipovinho from tipoVinho where "
        clausulaSql += " upper(nometipovinho) like upper('%" + chave + "%') order by nometipovinho;"

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao pesquisar tipo de vinho', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append(str(row[0]) + '|' + row[1])

            row = self.conexao.cursor.fetchone()

        return lista

    def buscaTipoVinho(self, argId):
        clausulaSql  = 'select idtipovinho, nometipovinho '
        clausulaSql += 'from tipovinho '
        clausulaSql += 'where idtipovinho = '
        clausulaSql += str(argId) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao buscar tipo de vinho com ID ' + str(argId) + '!',
                                   wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        if row != None:
            lista.append(row[0])
            lista.append(row[1])

        return lista

    def setidTipoVinho(self, arg):
        self.idTipoVinho = arg

    def setnomeTipoVinho(self, arg):
        self.nomeTipoVinho = arg

    def insere(self):
        clausulaSql = "insert into tipovinho (nometipovinho) values ("
        clausulaSql += "'" + tiraAspas(self.nomeTipoVinho) + "');"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao inserir dados do tipo de vinho!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def update(self, argId):
        clausulaSql = "update tipovinho set "
        clausulaSql += "nometipovinho = '" + tiraAspas(self.nomeTipoVinho) + "'  "
        clausulaSql += "where idtipovinho = " + str(argId) + ";"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao atualizar os dados do tipo de vinho!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def delete(self, argId):
        clausulaSql = 'delete from tipovinho '
        clausulaSql += 'where idtipovinho = ' + str(argId) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao eliminar os dados do tipo de vinho!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def sqlBuscaTamanho(self, coluna):
        if self.conexao.banco == 'postgres':
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_catalog = 'adega' and table_name = 'tipovinho'"
            clausulaSql += "and column_name = '" + coluna + "';"
        else:
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_name = 'tipovinho' and column_name = '" + coluna + "';"

        try:
            self.conexao.cursor.execute(clausulaSql)
            row = self.conexao.cursor.fetchone()
            while row != None:
                return row[0]
        except:
            return 0



