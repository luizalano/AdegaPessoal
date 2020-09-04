# coding: utf-8
from pacotesMG.dataBaseFunctionMG import *
from pacotesMG.diversos import *


class Pais():
    idPais = 0
    nomePais = ''
    nomeCapital = ''
    iso2 = ''
    iso3 = ''

    def __init__(self):
        
        self.conexao = ConMG('parametros.json')
        
        if self.conexao.con == None:
            sys.exit()

    def getAll(self):
        clausulaSql = 'select idpais, nomepais, nomecapital, iso2, iso3 '
        clausulaSql += 'from pais order by nomepais;'

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler país', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append([row[0], row[1], row[2], row[3], row[4]])

            row = self.conexao.cursor.fetchone()

        return lista

    def pesquisaPais(self, chave):
        clausulaSql = "select idpais, nomepais from pais where "
        clausulaSql += " upper(nomepais) like upper('%" + chave + "%') order by nomepais;"

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao pesquisar país', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append(str(row[0]) + '|' + row[1])

            row = self.conexao.cursor.fetchone()

        return lista

    def buscaIdPais(self, argNome):
        clausulaSql = "select idpais "
        clausulaSql += "from pais where nomepais = '" + argNome + "';"

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao buscar pais com pelo nome ' + argNome + '!',
                                   wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        row = self.conexao.cursor.fetchone()

        idPais = 0
        if row != None:
            idPais =row[0]

        return idPais

    def buscaPais(self, argId):
        clausulaSql = 'select idpais, nomepais, nomecapital, iso2, iso3 '
        clausulaSql += 'from pais where idpais = '
        clausulaSql += str(argId) + ' order by nomepais;'

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao buscar pais com ID ' + str(argId) + '!',
                                   wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        if row != None:
            lista.append(row[0])
            lista.append(row[1])
            lista.append(row[2])
            lista.append(row[3])
            lista.append(row[4])

        return lista

    def setidPais(self, arg):
        self.idPais = arg

    def setnomePais(self, arg):
        self.nomePais = arg

    def setnomeCapital(self, arg):
        self.nomeCapital = arg

    def setiso2(self, arg):
        self.iso2 = arg.upper()

    def setiso3(self, arg):
        self.iso3 = arg.upper()

    def insere(self):
        clausulaSql = "insert into pais (nomepais, nomecapital, iso2, iso3) values ("
        clausulaSql += "'" + tiraAspas(self.nomePais) + "', '" + tiraAspas(self.nomeCapital) + "', "
        clausulaSql += "'" + tiraAspas(self.iso2) + "', '" + tiraAspas(self.iso3) + "');"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao inserir dados da pais!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def update(self, argId):
        clausulaSql = "update pais set "
        clausulaSql += "nomepais = '" + tiraAspas(self.nomePais) + "', "
        clausulaSql += "nomecapital = '" + tiraAspas(self.nomeCapital) + "', "
        clausulaSql += "iso2 = '" + tiraAspas(self.iso2) + "', "
        clausulaSql += "iso3 = '" + tiraAspas(self.iso3) + "' "
        clausulaSql += "where idpais = " + str(argId) + ";"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao atualizar os dados da pais!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def delete(self, argId):
        clausulaSql = 'delete from pais '
        clausulaSql += 'where idpais = ' + str(argId) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao eliminar os dados da pais!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def sqlBuscaTamanho(self, coluna):
        if self.conexao.banco == 'postgres':
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_catalog = 'adega' and table_name = 'pais'"
            clausulaSql += "and column_name = '" + coluna + "';"
        else:
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_name = 'pais' and column_name = '" + coluna + "';"

        try:
            self.conexao.cursor.execute(clausulaSql)
            row = self.conexao.cursor.fetchone()
            while row != None:
                return row[0]
        except:
            return 0



