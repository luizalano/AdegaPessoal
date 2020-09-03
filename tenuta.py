# coding: utf-8
import sys
from pacotesMG.conectaDataBaseMG import *
from pacotesMG.diversos import *

class Tenuta():
    idTenuta = 0
    idPais = 0
    nomeTenuta = ''
    regiao = ''
    cidade = ''
    estado = ''
    endereco1 = ''
    endereco2 = ''
    endereco3 = ''
    cep = ''
    telefone = ''
    email = ''
    contato = ''
    banco = 'mysql'

    def __init__(self):
        self.con, self.cursor = conectaMySql('masteradega', 'Adeg@W!ne1', 'adega.mysql.uhserver.com', 'adega')
        if self.con == None:
            sys.exit()

    def getAll(self):
        clausulaSql  = 'select t.idtenuta, t.nometenuta, t.idpais, p.nomepais, t.regiao, t.cidade, t.estado, '
        clausulaSql += 't.endereco1, t.endereco2, t.endereco3, t.cep, t.telefone, t.email, t.contato '
        clausulaSql += 'from tenuta as t join pais as p on t.idpais = p.idpais '
        clausulaSql += 'order by t.nometenuta;'

        try:
            self.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao ler tenutas', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

        lista = []

        row = self.cursor.fetchone()
        while row != None:
            lista.append([row[0], row[1], row[2], row[3], row[4],
                          row[5], row[6], row[7], row[8], row[9],
                          row[10], row[11], row[12], row[13]])

            row = self.cursor.fetchone()

        return lista

    def buscaTenuta(self, argId):
        clausulaSql  = 'select t.idtenuta, t.nometenuta, t.idpais, p.nomepais, t.regiao, t.cidade, t.estado, '
        clausulaSql += 't.endereco1, t.endereco2, t.endereco3, t.cep, t.telefone, t.email, t.contato '
        clausulaSql += 'from tenuta as t join pais as p on t.idpais = p.idpais '
        clausulaSql += 'where t.idtenuta = ' + str(argId) + ';'

        try:
            self.cursor.execute(clausulaSql)
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao buscar tenuta com ID ' + str(argId) + '!',
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
            lista.append(row[5])
            lista.append(row[6])
            lista.append(row[7])
            lista.append(row[8])
            lista.append(row[9])
            lista.append(row[10])
            lista.append(row[11])
            lista.append(row[12])
            lista.append(row[13])

        return lista

    def setidTenuta(self, arg):
        self.idTenuta = arg

    def setnomeTenuta(self, arg):
        self.nomeTenuta = arg

    def setidPais(self, arg):
        self.idPais = arg

    def setregiao(self, arg):
        self.regiao = arg

    def setcidade(self,arg):
        self.cidade = arg

    def setestado(self, arg):
        self.estado = arg
    
    def setendereco1(self, arg):
        self.endereco1 = arg

    def setendereco2(self, arg):
        self.endereco2 = arg

    def setendereco3(self, arg):
        self.endereco3 = arg
        
    def setcep(self, arg):
        self.cep = arg
        
    def settelefone(self, arg):
        self.telefone = arg
        
    def setemail(self, arg):
        self.email = arg
        
    def setcontato(self, arg):
        self.contato = arg

    def insere(self):
        clausulaSql = "insert into tenuta (idtenuta, nometenuta, idpais, regiao, cidade, estado" \
                      ", endereco1, endereco2, endereco3, cep, telefone, email, contato) values ("
        clausulaSql +=       str(self.idTenuta) + ", "
        clausulaSql += "'" + self.nomeTenuta + "', "
        clausulaSql +=       str(self.idPais) + ","
        clausulaSql += "'" + self.regiao + "', "
        clausulaSql += "'" + self.cidade + "', "
        clausulaSql += "'" + self.estado + "', "
        clausulaSql += "'" + self.endereco1 + "', "
        clausulaSql += "'" + self.endereco2 + "', "
        clausulaSql += "'" + self.endereco3 + "', "
        clausulaSql += "'" + self.cep + "', "
        clausulaSql += "'" + self.telefone + "', "
        clausulaSql += "'" + self.email + "', "
        clausulaSql += "'" + self.contato + "'); "

        try:
            self.cursor.execute(clausulaSql)
            self.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao inserir dados da tenuta!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def update(self, argId):
        clausulaSql = "update tenuta set "

        clausulaSql += "nometenuta = '" + self.nomeTenuta + "', "
        clausulaSql += "idpais = "      + str(self.idPais) + ", "
        clausulaSql += "regiao = '"     + self.regiao + "', "
        clausulaSql += "cidade = '"     + self.cidade + "', "
        clausulaSql += "estado = '"     + self.estado + "', "
        clausulaSql += "endereco1 = '"  + self.endereco1 + "', "
        clausulaSql += "endereco2 = '"  + self.endereco2 + "', "
        clausulaSql += "endereco3 = '"  + self.endereco3 + "', "
        clausulaSql += "cep = '"        + self.cep + "', "
        clausulaSql += "telefone = '"   + self.telefone + "', "
        clausulaSql += "email = '"      + self.email + "', "
        clausulaSql += "contato = '"    + self.contato + "' "
        clausulaSql += "where idtenuta = " + str(argId) + ";"

        print(clausulaSql)

        try:
            self.cursor.execute(clausulaSql)
            self.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao atualizar os dados da tenuta!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def delete(self, argId):
        clausulaSql = 'delete from tenuta '
        clausulaSql += 'where idtenuta = ' + str(argId) + ';'

        try:
            self.cursor.execute(clausulaSql)
            self.con.commit()
        except:
            dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao eliminar os dados da tenuta!', wx.OK | wx.ICON_ERROR)
            result = dlg.ShowModal()

    def sqlBuscaTamanho(self, coluna):
        if self.banco == 'postgres':
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_catalog = 'adega' and table_name = 'tenuta'"
            clausulaSql += "and column_name = '" + coluna + "';"
        else:
            clausulaSql = "select character_maximum_length from INFORMATION_SCHEMA.COLUMNS "
            clausulaSql += "where table_name = 'tenuta' and column_name = '" + coluna + "';"

        try:
            self.cursor.execute(clausulaSql)
            row = self.cursor.fetchone()
            while row != None:
                return row[0]
        except:
            return 0



