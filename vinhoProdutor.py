# coding: utf-8
import sys

from pacotesMG.diversos import *
from pacotesMG.dataBaseFunctionMG import *

class VinhoProdutor():
    idVinhoProdutor = 0
    idTenuta = 0
    nomeTenuta = ''
    nomeVinho = ''
    idApelacao = 0
    nomeApelacao = ''
    idTipoVinho = 0
    nomeTipoVinho = ''
    complemento = ''
    idPais = 0
    nomePais = ''

    def __init__(self):

        self.conexao = ConMG('parametros.json')

        if self.conexao.con == None:
            sys.exit()

    def getAll(self, **kwargs):
        '''

        :param kwargs:
            nome -> nome do produto para busca
            idtenuta -> id da tenuta para busca
        :return:
        '''

        onde =""
        if len(kwargs) > 0:
            if 'nome' in kwargs:
                onde = "where t.nometenuta = '" +  kwargs['nome'] + "' "
            if 'idtenuta' in kwargs:
                onde = "where vp.idtenuta = " +  str(kwargs['idtenuta']) + " "

        clausulaSql  = 'select vp.idvinhoprodutor, vp.idtenuta, p.nometenuta, vp.nomevinho, ' \
                       'vp.idapelacao, a.nomeapelacao, vp.idtipovinho, t.nometipovinho, ' \
                       'vp.complemento, p.idpais, c.nomepais ' \
                       'from vinhoprodutor as vp join tenuta as p on vp.idtenuta = p.idtenuta ' \
                       'join apelacao as a on vp.idapelacao = a.idapelacao ' \
                       'join tipovinho as t on vp.idtipovinho = t.idtipovinho ' \
                       'join pais as c on p.idpais = c.idpais '
        clausulaSql += onde + ' order by c.nomepais, p.nometenuta, vp.nomevinho;'

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler vinhos por produtor', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.conexao.cursor.fetchone()
        while row != None:
            lista.append([row[0], row[1], row[2], row[3],row[4], row[5], row[6], row[7], row[8], row[9], row[10]])

            row = self.conexao.cursor.fetchone()

        return lista

    def pesquisaVinhoProdutor(self, chave):
        clausulaSql = "select idvinhoProdutor, nomevinhoProdutor from vinhoProdutor where "
        clausulaSql += " upper(nomevinhoProdutor) like upper('%" + chave + "%') order by nomevinhoProdutor;"

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

    def buscaVinhoProdutorPorNome(self, chave):
        clausulaSql = "select idvinhoProdutor, nomevinhoProdutor from vinhoProdutor where "
        clausulaSql += " upper(nomevinhoProdutor) = upper('" + chave + "');"

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

    def buscaVinhoProdutor(self, argId):
        clausulaSql  = 'select vp.idvinhoprodutor, vp.idtenuta, p.nometenuta, vp.nomevinho, ' \
                       'vp.idapelacao, a.nomeapelacao, vp.idtipovinho, t.nometipovinho, ' \
                       'vp.complemento, p.idpais, c.nomepais ' \
                       'from vinhoprodutor as vp join tenuta as p on vp.idtenuta = p.idtenuta ' \
                       'join apelacao as a on vp.idapelacao = a.idapelacao ' \
                       'join tipovinho as t on vp.idtipovinho = t.idtipovinho ' \
                       'join pais as c on p.idpais = c.idpais '
        clausulaSql += 'where vp.idvinhoprodutor = ' + str(argId) + ' order by c.nomepais, p.nometenuta, vp.nomevinho;'

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao buscar vinho do produtor com ID ' + str(argId) + '!',
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
            lista.append(row[5])
            lista.append(row[6])
            lista.append(row[7])
            lista.append(row[8])
            lista.append(row[9])
            lista.append(row[10])

        return lista

    def buscaIdVinhoProdutor(self, argNome):
        clausulaSql = "select idvinhoProdutor "
        clausulaSql += "from vinhoProdutor where nomevinhoProdutor = '" + argNome + "';"

        try:
            self.conexao.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao buscar apelação pelo nome ' + argNome + '!',
                                   wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        row = self.conexao.cursor.fetchone()

        idVinhoProdutor = 0
        if row != None:
            idVinhoProdutor =row[0]

        return idVinhoProdutor

    def setidTenuta(self, arg):
        self.idTenuta = arg

    def setnomeVinho(self, arg):
        self.nomeVinho = arg

    def setidApelacao(self, arg):
        self.idApelacao = arg

    def setidTipoVinho(self, arg):
        self.idTipoVinho = arg

    def setcomplemento(self, arg):
        self.complemento = arg

    def insere(self):
        clausulaSql = "insert into vinhoprodutor (idtenuta, nomevinho, idapelacao, idtipovinho, complemento) values ("
        clausulaSql += "" + str(self.idTenuta) + ", "
        clausulaSql += "'" + tiraAspas(self.nomeVinho) + "', "
        clausulaSql += "" + str(self.idApelacao) + ", "
        clausulaSql += "" + str(self.idTipoVinho) + ", "
        clausulaSql += "'" + tiraAspas(self.complemento) + "');"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao inserir dados do vinho do produtor!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def update(self, argId):
        clausulaSql = "update vinhoprodutor set "
        clausulaSql += "idtenuta = " + str(self.idTenuta) + ", "
        clausulaSql += "nomevinho = '" + tiraAspas(self.nomeVinho) + "', "
        clausulaSql += "idapelacao = " + str(self.idApelacao) + ", "
        clausulaSql += "idtipovinho = " + str(self.idTipoVinho) + ", "
        clausulaSql += "complemento = '" + tiraAspas(self.complemento) + "' "
        clausulaSql += "where idvinhoprodutor = " + str(argId) + ";"

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao atualizar os dados do vinho do produtor!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def delete(self, argId):
        clausulaSql = 'delete from vinhoprodutor '
        clausulaSql += 'where idvinhoprodutor = ' + str(argId) + ';'

        try:
            self.conexao.cursor.execute(clausulaSql)
            self.conexao.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao eliminar os dados do vinho do produtor!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def sqlBuscaTamanho(self, coluna):
        if self.conexao.banco == 'postgres':
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_catalog = 'adega' and table_name = 'vinhoprodutor'"
            clausulaSql += "and column_name = '" + coluna + "';"
        else:
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_name = 'vinhoprodutor' and column_name = '" + coluna + "';"

        try:
            self.conexao.cursor.execute(clausulaSql)
            row = self.conexao.cursor.fetchone()
            while row != None:
                return row[0]
        except:
            return 0



