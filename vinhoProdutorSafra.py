# coding: utf-8
import sys

from pacotesMG.diversos import *
from pacotesMG.dataBaseFunctionMG import *

class VinhoProdutorSafra():
    idVinhoProdutorSafra = 0
    idVinhoProdutor = 0
    safra = 0
    beberde = 0
    beberate = 0
    observacoes = ''

    def __init__(self):

        self.conexao = ConMG('parametros.json')

        if self.conexao.con == None:
            sys.exit()

    def getAll(self, **kwargs):
        '''

        :param kwargs:
            idvinho -> id da tenuta para busca
            idsafra -> id da tabela vinhopdodutorsafra
        :return:
        '''

        onde =""
        if len(kwargs) > 0:
            if 'idvinho' in kwargs:
                onde = "where vps.idvinhoprodutor = " +  str(kwargs['idvinho']) + " "
            if 'idsafra' in kwargs:
                onde = "where vps.idvinhoprodutorsafra = " +  str(kwargs['idsafra']) + " "

        clausulaSql  = "select vps.idvinhoprodutorsafra, vps.idvinhoprodutor, vp.nomevinho, vp.idtenuta, " \
                       "t.nometenuta, vps.safra, vps.beberde, vps.beberate, vps.observacoes " \
                       "from vinhoprodutorsafra as vps " \
                       "join vinhoprodutor as vp on vps.idvinhoprodutor = vp.idvinhoprodutor " \
                       "join tenuta as t on vp.idtenuta = t.idtenuta "
        clausulaSql += onde + "order by t.nometenuta, vp.nomevinho, vps.safra;"

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler as safras de vinhos por produtor', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append([row[0], row[1], row[2], row[3],row[4], row[5], row[6], row[7], row[8]])

            row = self.conexao.cursor.fetchone()

        return lista

    def setidVinhoProdutor(self, arg):
        self.idVinhoProdutor = arg

    def setsafra(self, arg):
        self.safra = arg

    def setbeberde(self, arg):
        self.beberde = arg

    def setbeberate(self, arg):
        self.beberate = arg

    def setobservacoes(self, arg):
        self.observacoes = arg

    def insere(self):
        clausulaSql = "insert into vinhoprodutorsafra (idvinhoprodutor, safra, beberde, beberate, observacoes) values ("
        clausulaSql += "" + str(self.idVinhoProdutor) + ", "
        clausulaSql += "" + str(self.safra) + ", "
        clausulaSql += "" + str(self.beberde) + ", "
        clausulaSql += "" + str(self.beberate) + ", "
        clausulaSql += "'" + tiraAspas(self.observacoes) + "');"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao inserir dados da safra do vinho do produtor!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def update(self, argId):
        clausulaSql = "update vinhoprodutorsafra set "
        clausulaSql += "idvinhoprodutor = " + str(self.idVinhoProdutor) + ", "
        clausulaSql += "safra = '" + str(self.safra) + "', "
        clausulaSql += "beberde = " + str(self.beberde) + ", "
        clausulaSql += "beberate = " + str(self.beberate) + ", "
        clausulaSql += "observacoes = '" + tiraAspas(self.observacoes) + "' "
        clausulaSql += "where idvinhoprodutorsafra = " + str(argId) + ";"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao atualizar os dados da safra do vinho do produtor!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def delete(self, argId):
        clausulaSql = 'delete from vinhoprodutorsafra '
        clausulaSql += 'where idvinhoprodutorsafra = ' + str(argId) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao eliminar os dados da safra do vinho do produtor!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def sqlBuscaTamanho(self, coluna):
        if self.conexao.banco == 'postgres':
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_catalog = 'adega' and table_name = 'vinhoprodutorsafra'"
            clausulaSql += "and column_name = '" + coluna + "';"
        else:
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_name = 'vinhoprodutorsafra' and column_name = '" + coluna + "';"

        try:
            self.conexao.cursor.execute(clausulaSql)
            row = self.conexao.cursor.fetchone()
            while row != None:
                return row[0]
        except:
            return 0



