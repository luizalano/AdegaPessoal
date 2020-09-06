# coding: utf-8
import sys

from pacotesMG.diversos import *
from pacotesMG.dataBaseFunctionMG import *

class Corte():
    idCorte = 0
    idVinhoProdutorSafra = 0
    idUva = 0
    percentual = 0.0

    def __init__(self):

        self.conexao = ConMG('parametros.json')

        if self.conexao.con == None:
            sys.exit()

    def getAll(self, **kwargs):
        '''

        :param kwargs:
            idpais
            nomepais
        :return:
        '''

        onde =""
        if len(kwargs) > 0:
            if 'nomeuva' in kwargs:
                onde = "where u.nomeuva = '" +  kwargs['nomeuva'] + "' "
            if 'idcorte' in kwargs:
                onde = "where corte.idcorte = '" +  kwargs['idcorte'] + "' "
            if 'idsafra' in kwargs:
                onde = "where corte.idvinhoprodutorsafra = '" +  kwargs['idsafra'] + "' "

        clausulaSql  = "select corte.idcorte, corte.iduva, u.nomeuva, corte.percentual, corte.idvinhoprodutorsafra " \
                       "from corte join uva as u on corte.iduva = u.iduva "
        clausulaSql += onde + "order by corte.percentual;"

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler corte', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append([row[0], row[1], row[2], row[3], row[4]])

            row = self.conexao.cursor.fetchone()

        return lista

    def getCortePorSafra(self, idProdutor, safra):
        clausulaSql  = 'select corte.idcorte, corte.iduva, corte.percentual, corte.idvinhoprodutorsafra, vps.safra ' \
                       'from corte join vinhoprodutorsafra as vps on vps.idvinhoprodutorsafra = corte.idvinhoprodutorsafra ' \
                       'where corte.idvinhoprodutorsafra = '
        clausulaSql += str(idProdutor) + ' and vps.safra = ' + str(safra) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler corte', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append([row[1], row[2], row[3]])

            row = self.conexao.cursor.fetchone()

        return lista


    def setidCorte(self, arg):
        self.idCorte = arg

    def setidUva(self, arg):
        self.idUva = arg

    def setpercentual(self, arg):
        self.percentual = arg

    def setidVinhoProdutorSafra(self, arg):
        self.idVinhoProdutorSafra = arg

    def insere(self):
        clausulaSql = "insert into corte (iduva, percentual, idvinhoprodutorsafra) values ("
        clausulaSql += "" + str(self.idUva) + ", "
        clausulaSql += "" + str(self.percentual) + ", "
        clausulaSql += "" + str(self.idVinhoProdutorSafra) + ");"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao inserir dados do corte!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def update(self, argId):
        clausulaSql = "update corte set "
        clausulaSql += "iduva = " + str(self.idUva) + ", "
        clausulaSql += "percentual = " + str(self.percentual) + ", "
        clausulaSql += "idvinhoprodutorsafra = " + str(self.idVinhoProdutorSafra) + " "
        clausulaSql += "where idcorte = " + str(argId) + ";"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao atualizar os dados do corte!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def delete(self, argId):
        clausulaSql = 'delete from corte '
        clausulaSql += 'where idcorte = ' + str(argId) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao eliminar os dados do corte!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def deleteSafra(self, argId):
        clausulaSql = 'delete from corte '
        clausulaSql += 'where idvinhoprodutorsafra = ' + str(argId) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao eliminar os dados do corte!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()


    def sqlBuscaTamanho(self, coluna):
        if self.conexao.banco == 'postgres':
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_catalog = 'adega' and table_name = 'corte'"
            clausulaSql += "and column_name = '" + coluna + "';"
        else:
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_name = 'corte' and column_name = '" + coluna + "';"

        try:
            self.conexao.cursor.execute(clausulaSql)
            row = self.conexao.cursor.fetchone()
            while row != None:
                return row[0]
        except:
            return 0



