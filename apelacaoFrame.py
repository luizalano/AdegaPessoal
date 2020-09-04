# coding: utf-8
from apelacao import *
from pais import *

from pacotesMG.wxComponetesMG import FrameMG
import wx
import wx.grid as gridlib


class FrmApelacao(FrameMG):
    insert = False
    caminho = '..\\pacotesMG\\icones\\'

    def __init__(self):
        self.apelacao = Apelacao()
        self.pais = Pais()

        super(FrmApelacao, self).__init__(None, 'Cadastro de apelações', 800, 700, 0)

        self.criaComponentes()

    def criaComponentes(self):
        X = self.posx(1)
        Y = self.posy(0)
        tamX = self.larguraEmPx(106)
        tamY = self.alturaEmPx(12)

        self.grid = wx.ListCtrl(self.painel, pos=(X, Y), size=(tamX, tamY),
                                style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.BORDER_SUNKEN)

        label01, self.txtId = self.criaCaixaDeTexto(self.painel, 12, 10, 40, 'ID', 0, xcol=1, tamanho = 6)
        label02, self.txtNomeApelacao = self.criaCaixaDeTexto(self.painel, 12, 80, 520, 'Nome da apelação',
                                                             self.apelacao.sqlBuscaTamanho('nomeapelacao'), xcol = 11, tamanho = 71)

        label03, self.cbPais = self.criaCombobox(self.painel, label = 'País', linha=13, coluna = 1,
                                                 tamanho=81, maxlen=self.pais.sqlBuscaTamanho('nomepais'))

        self.limpaElementos()

        # self.grid.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha, self.grid)

        #self.txtNomeApelacao.Bind(wx.EVT_KILL_FOCUS, self.perdeufoco)

        self.encheGrid()

        self.Show()

    def perdeufoco(self, event):
        print ('Acabou de perder o foco')

    def encheComboBoxPais(self):
        lista = self.pais.getAll()
        self.cbPais.Clear()

        for row in lista:
            self.cbPais.Append(row[1])

    def encheGrid(self):
        '''
        u.idapelacao, u.nomeapelacao, u.idpais, p.nomepais
        '''
        self.grid.ClearAll()
        self.grid.InsertColumn(0, 'id', width=self.larguraEmPx(8))
        self.grid.InsertColumn(1, 'Nome da apelacao', width=self.larguraEmPx(30))
        self.grid.InsertColumn(3, 'Pais de origem', width=self.larguraEmPx(60))

        self.lista = self.apelacao.getAll()

        for row in self.lista:
            self.grid.Append([row[0], row[1], row[3]])

        self.encheComboBoxPais()

    def limpaElementos(self):
        self.txtId.Clear()
        self.txtNomeApelacao.Clear()
        self.cbPais.SetSelection(-1)

        self.txtId.Disable()
        self.txtNomeApelacao.Disable()

        self.botaoSalva.Disable()
        self.botaoDelete.Disable()

    def indiceDoPaisCb(self, nomePais):
        indice = 0
        i = 0
        max = self.cbPais.Count
        while i < max:
            paisLido = self.cbPais.GetString(i)
            if paisLido == nomePais:
                indice = i
                i = max
            i += 1

        return indice

    def selecionaLinha(self, event):
        item = self.grid.GetFocusedItem()

        idApelacao = self.grid.GetItemText(item, 0)

        if idApelacao.isdigit():
            lista = self.apelacao.buscaApelacao(idApelacao)

            self.txtId.SetValue(str(lista[0]))
            self.txtNomeApelacao.SetValue(lista[1])

            self.cbPais.SetSelection(self.indiceDoPaisCb(lista[3]))

            self.txtNomeApelacao.Enable()
            self.cbPais.Enable()

            self.botaoSalva.Enable()
            self.botaoDelete.Enable()

    def salvaElemento(self, event):
        self.apelacao.setnomeApelacao(self.txtNomeApelacao.GetValue())
        self.apelacao.setidPais(str(self.pais.buscaIdPais(self.cbPais.GetValue())))

        if self.insert:
            self.apelacao.insere()
            self.insert = False
        else:
            self.apelacao.update(str(self.txtId.GetValue()))

        self.limpaElementos()

        self.encheGrid()

    def deletaElemento(self, event):
        super(FrmApelacao, self).deletaElemento(event)
        if self.prossegueEliminacao:
            self.apelacao.delete(str(self.txtId.GetValue()))

            self.limpaElementos()

            self.encheGrid()

    def habilitaNovo(self, event):
        self.limpaElementos()

        self.txtNomeApelacao.Enable()
        self.cbPais.Enable()

        self.botaoSalva.Enable()

        self.insert = True

    def cancelaOperacao(self, event):
        self.limpaElementos()

def main():
    app = wx.App()
    frmApelacao = FrmApelacao()
    app.MainLoop()


if __name__ == '__main__':
    main()

