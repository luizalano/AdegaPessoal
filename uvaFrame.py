# coding: utf-8
from uva import *
from pais import *

from pacotesMG.wxComponetesMG import FrameMG
import wx
import wx.grid as gridlib


class FrmUva(FrameMG):
    insert = False
    caminho = '..\\pacotesMG\\icones\\'

    def __init__(self):
        self.uva = Uva()
        self.pais = Pais()

        super(FrmUva, self).__init__(None, 'Cadastro de uvas', 800, 700, 0)

        self.criaComponentes()

    def criaComponentes(self):
        X = self.posx(1)
        Y = self.posy(0)
        tamX = self.larguraEmPx(106)
        tamY = self.alturaEmPx(12)

        self.grid = wx.ListCtrl(self.painel, pos=(X, Y), size=(tamX, tamY),
                                style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.BORDER_SUNKEN)

        label01, self.txtId = self.criaCaixaDeTexto(self.painel, 12, 10, 40, 'ID', 0, xcol=1, tamanho = 6)
        label02, self.txtNomeUva = self.criaCaixaDeTexto(self.painel, 12, 80, 520, 'Nome da uva',
                                                             self.uva.sqlBuscaTamanho('nomeuva'), xcol = 11, tamanho = 71)
        Y = self.posy(12)
        lista = ['Branca','Tinta']
        self.rbCorCasca = wx.RadioBox(self.painel, label='Casca', pos=(610, Y),
            choices=(lista[0], lista[1]), style=wx.RA_SPECIFY_ROWS)

        label03, self.cbPais = self.criaCombobox(self.painel, label = 'País', linha=13, coluna = 1,
                                                 tamanho=81, maxlen=self.pais.sqlBuscaTamanho('nomepais'))


        self.limpaElementos()

        # self.grid.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha, self.grid)

        self.encheGrid()

        self.Show()

    def encheComboBoxPais(self):
        lista = self.pais.getAll()
        self.cbPais.Clear()

        for row in lista:
            self.cbPais.Append(row[1])

    def encheGrid(self):
        '''
        u.iduva, u.nomeuva, u.corcasca, u.idpais, p.nomepais
        '''
        self.grid.ClearAll()
        self.grid.InsertColumn(0, 'id', width=self.larguraEmPx(6))
        self.grid.InsertColumn(1, 'Nome da uva', width=self.larguraEmPx(41))
        self.grid.InsertColumn(2, 'Casca', width=self.larguraEmPx(8))
        self.grid.InsertColumn(3, 'Pais de origem', width=self.larguraEmPx(41))

        self.lista = self.uva.getAll()

        for row in self.lista:
            if row[2] == 1:
                corcasca = 'Tinta'
            else:
                corcasca = 'Branca'
            self.grid.Append([row[0], row[1], corcasca, row[4]])

        self.encheComboBoxPais()

    def limpaElementos(self):
        self.txtId.Clear()
        self.txtNomeUva.Clear()
        self.cbPais.SetSelection(-1)

        self.txtId.Disable()
        self.txtNomeUva.Disable()
        self.cbPais.Disable()
        self.rbCorCasca.Disable()

        self.botaoSalva.Disable()
        self.botaoDelete.Disable()

    def selecionaLinha(self, event):
        item = self.grid.GetFocusedItem()

        idUva = self.grid.GetItemText(item, 0)

        if idUva.isdigit():
            lista = self.uva.buscaUva(idUva)

            self.txtId.SetValue(str(lista[0]))
            self.txtNomeUva.SetValue(lista[1])

            self.cbPais.SetSelection(self.indiceDoPaisCb(lista[4]))

            self.rbCorCasca.SetSelection(lista[2])

            self.txtNomeUva.Enable()
            self.cbPais.Enable()
            self.rbCorCasca.Enable()

            self.botaoSalva.Enable()
            self.botaoDelete.Enable()

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

    def salvaElemento(self, event):
        self.uva.setnomeUva(self.txtNomeUva.GetValue())
        self.uva.setcorCasca(self.rbCorCasca.GetSelection())
        self.uva.setidPais(str(self.pais.buscaIdPais(self.cbPais.GetValue())))

        if self.insert:
            self.uva.insere()
            self.insert = False
        else:
            self.uva.update(str(self.txtId.GetValue()))

        self.limpaElementos()

        self.encheGrid()

    def deletaElemento(self, event):
        super(FrmUva, self).deletaElemento(event)
        if self.prossegueEliminacao:
            self.uva.delete(str(self.txtId.GetValue()))

            self.limpaElementos()

            self.encheGrid()

    def habilitaNovo(self, event):
        self.limpaElementos()

        self.txtNomeUva.Enable()
        self.cbPais.Enable()
        self.rbCorCasca.Enable()

        self.botaoSalva.Enable()

        self.insert = True

    def cancelaOperacao(self, event):
        self.limpaElementos()

def main():
    app = wx.App()
    frmUva = FrmUva()
    app.MainLoop()


if __name__ == '__main__':
    main()

