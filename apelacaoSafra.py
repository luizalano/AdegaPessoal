# coding: utf-8
from pacotesMG.conectaDataBaseMG import *
from pacotesMG.diversos import *

class ApelacaoSafra():
    idApelacaoSafra = 0
    idApelacao = 0
    nomeApelacao = ''
    safra = 0
    nota = 0
    banco = 'mysql'

    def __init__(self):
        self.con, self.cursor = conectaMySql('masteradega', 'Adeg@W!ne1', 'adega.mysql.uhserver.com', 'adega')
        if self.con == None:
            sys.exit()

    def getAll(self):
        clausulaSql  = 'select aps.idapelacaosafra, aps.idapelacao, a.nomeapelacao, aps.safra, aps.nota '
        clausulaSql += 'from apelacaosafra as aps join apelacao as a on aps.idapelacao = a.idapelacao '
        clausulaSql += 'order by a.nomeapelacao, aps.safra desc;'

        try:
            self.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler safras por apelações', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.cursor.fetchone()
        while row != None:
            lista.append([row[0], row[1], row[2], row[3], row[4]])

            row = self.cursor.fetchone()

        return lista

    def getMinSafra(self):
        clausulaSql  = 'select min(safra) from apelacaosafra'

        try:
            self.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler safras por apelações', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        row = self.cursor.fetchone()
        while row != None:
            return row[0]

        return 0

    def getMaxSafra(self):
        clausulaSql = 'select max(safra) from apelacaosafra'

        try:
            self.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler safras por apelações', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        row = self.cursor.fetchone()
        while row != None:
            return row[0]
        a = 0
        return 0

    def buscaApelacaoSafraPorNomeSafra(self, argNomeApelacao, argSafra):
        clausulaSql  = "select aps.idapelacaosafra, aps.idapelacao, a.nomeapelacao, aps.safra, aps.nota "
        clausulaSql += "from apelacaosafra as aps join apelacao as a on aps.idapelacao = a.idapelacao "
        clausulaSql += "where aps.safra = " +  str(argSafra) + " and a.nomeapelacao = '"
        clausulaSql += argNomeApelacao + "';"

        try:
            self.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao buscar safra ' + str(argSafra) + ' de ' + argNomeApelacao + '!',
                                   wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.cursor.fetchone()
        if row != None:
            lista.append(row[0])
            lista.append(row[1])
            lista.append(row[2])
            lista.append(row[3])
            lista.append(row[4])

        return lista


    def buscaApelacaoSafra(self, argId):
        clausulaSql  = 'select aps.idapelacaosafra, aps.idapelacao, a.nomeapelacao, aps.safra, aps.nota '
        clausulaSql += 'from apelacaosafra as aps join apelacao as a on aps.idapelacao = a.idapelacao '
        clausulaSql += 'where aps.idapelacaosafra = '
        clausulaSql += str(argId) + ';'

        try:
            self.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao buscar safra de apelação com ID ' + str(argId) + '!',
                                   wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.cursor.fetchone()
        if row != None:
            lista.append(row[0])
            lista.append(row[1])
            lista.append(row[2])
            lista.append(row[3])
            lista.append(row[4])

        return lista

    def setidApelacaoSafra(self, arg):
        self.idApelacaoSafra = arg

    def setnota(self, arg):
        self.nota = arg

    def setidApelacao(self, arg):
        self.idApelacao = arg

    def setsafra(self, arg):
        self.safra = arg

    def insere(self):
        clausulaSql = "insert into apelacaosafra (idapelacao, nota, safra) values ("
        clausulaSql += str(self.idApelacao) + ", "
        clausulaSql += str(self.nota) + ", "
        clausulaSql += str(self.safra) + ");"

        try:
            self.cursor.execute(clausulaSql)
            self.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao inserir dados da safra por apelação!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def update(self, argId):
        clausulaSql = "update apelacaosafra set "
        clausulaSql += "idapelacao = " + str(self.idApelacao) + ", "
        clausulaSql += "nota = " + str(self.nota) + ", "
        clausulaSql += "safra = " + str(self.safra) + " "
        clausulaSql += "where idapelacaoSafra = " + str(argId) + ";"

        try:
            self.cursor.execute(clausulaSql)
            self.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao atualizar os dados da safra por apelação!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def delete(self, argId):
        clausulaSql = 'delete from apelacaosafra '
        clausulaSql += 'where idapelacaosafra = ' + str(argId) + ';'

        try:
            self.cursor.execute(clausulaSql)
            self.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao eliminar os dados da safra por apelação!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def sqlBuscaTamanho(self, coluna):
        if self.banco == 'postgres':
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_catalog = 'adega' and table_name = 'apelacaosafra'"
            clausulaSql += "and column_name = '" + coluna + "';"
        else:
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_name = 'apelacaosafra' and column_name = '" + coluna + "';"

        try:
            self.cursor.execute(clausulaSql)
            row = self.cursor.fetchone()
            while row != None:
                return row[0]
        except:
            return 0



