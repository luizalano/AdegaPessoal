# coding: utf-8
from pacotesMG.dataBaseFunctionMG import *
from pacotesMG.diversos import *


class Uva():
    idUva = 0
    nomeUva = ''
    corCasca = 0
    idPais = 0
    nomePais = ''

    def __init__(self):
        self.conexao = ConMG('parametros.json')
        
        if self.conexao.con == None:
            sys.exit()

    def getAll(self):
        clausulaSql  = 'select u.iduva, u.nomeuva, u.corcasca, u.idpais, p.nomepais '
        clausulaSql += 'from uva as u join pais as p on u.idpais = p.idpais '
        clausulaSql += 'order by u.nomeuva;'

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler uvas', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append([row[0], row[1], row[2], row[3], row[4]])

            row = self.conexao.cursor.fetchone()

        return lista

    def pesquisaUva(self, chave):
        clausulaSql = "select iduva, nomeuva from uva where "
        clausulaSql += " upper(nomeuva) like upper('%" + chave + "%') order by nomeuva;"

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao pesquisar uva', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append(str(row[0]) + '|' + row[1])

            row = self.conexao.cursor.fetchone()

        return lista

    def buscaUva(self, argId):
        clausulaSql  = 'select u.iduva, u.nomeuva, u.corcasca, u.idpais, p.nomepais '
        clausulaSql += 'from uva as u join pais as p on u.idpais = p.idpais '
        clausulaSql += 'where u.iduva = '
        clausulaSql += str(argId) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao buscar uva com ID ' + str(argId) + '!',
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

    def setidUva(self, arg):
        self.idUva = arg

    def setnomeUva(self, arg):
        self.nomeUva = arg

    def setcorCasca(self, arg):
        self.corCasca = arg

    def setidPais(self, arg):
        self.idPais = arg

    def insere(self):
        clausulaSql = "insert into uva (nomeuva, corcasca, idpais) values ("
        clausulaSql += "'" + tiraAspas(self.nomeUva) + "', " + str(self.corCasca) + ", "
        clausulaSql += str(self.idPais) + ");"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao inserir dados da uva!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def update(self, argId):
        clausulaSql = "update uva set "
        clausulaSql += "nomeuva = '" + tiraAspas(self.nomeUva) + "', "
        clausulaSql += "corcasca = " + str(self.corCasca) + ", "
        clausulaSql += "idpais = " + str(self.idPais) + " "
        clausulaSql += "where iduva = " + str(argId) + ";"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao atualizar os dados da uva!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def delete(self, argId):
        clausulaSql = 'delete from uva '
        clausulaSql += 'where iduva = ' + str(argId) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao eliminar os dados da uva!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def sqlBuscaTamanho(self, coluna):
        if self.conexao.banco == 'postgres':
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_catalog = 'adega' and table_name = 'uva'"
            clausulaSql += "and column_name = '" + coluna + "';"
        else:
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_name = 'uva' and column_name = '" + coluna + "';"

        try:
            self.conexao.cursor.execute(clausulaSql)
            row = self.conexao.cursor.fetchone()
            while row != None:
                return row[0]
        except:
            return 0



