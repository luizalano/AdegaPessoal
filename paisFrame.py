# coding: utf-8
from pais import *
from pacotesMG.conectaDataBaseMG import *

from pacotesMG.wxComponetesMG import FrameMG
import wx
import wx.grid as gridlib


class FrmPais(FrameMG):
    insert = False
    caminho = '..\\pacotesMG\\icones\\'

    def __init__(self):
        self.pais = Pais()

        super(FrmPais, self).__init__(None, 'Cadastro de países', 800, 700, 0)

        self.criaComponentes()

    def criaComponentes(self):
        self.grid = wx.ListCtrl(self.painel, pos=(10, 10), size=(770, 480),
                                style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.BORDER_SUNKEN)

        label01, self.txtId = self.criaCaixaDeTexto(self.painel, 12, 10, 50, 'ID', 0)
        label02, self.txtNomePais = self.criaCaixaDeTexto(self.painel, 12, 80, 610, 'Nome do país',
                                                             self.pais.sqlBuscaTamanho('nomepais'))
        label03, self.txtNomeCapital = self.criaCaixaDeTexto(self.painel, 13, 10, 560, 'Nome da capital',
                                                          self.pais.sqlBuscaTamanho('nomecapital'))
        label04, self.txtIso2 = self.criaCaixaDeTexto(self.painel, 13, 590, 40, 'ISO 2',
                                                        self.pais.sqlBuscaTamanho('iso2'))
        label05, self.txtIso3 = self.criaCaixaDeTexto(self.painel, 13, 650, 40, 'ISO 3',
                                                        self.pais.sqlBuscaTamanho('iso3'))
        self.txtId.Disable()
        self.txtNomePais.Disable()
        self.txtNomeCapital.Disable()
        self.txtIso2.Disable()
        self.txtIso3.Disable()

        # self.grid.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha, self.grid)

        self.encheGrid()

        self.Show()

    def encheGrid(self):
        '''
        0, 1, 6, 7, 8
        '''
        self.grid.ClearAll()
        self.grid.InsertColumn(0, 'id', width=40)
        self.grid.InsertColumn(1, 'Nome da pais', width=300)
        self.grid.InsertColumn(2, 'Nome da Capital', width=300)
        self.grid.InsertColumn(3, 'ISO 2', width=40)
        self.grid.InsertColumn(4, 'ISO 3', width=50)

        self.lista = self.pais.getAll()

        for row in self.lista:
            self.grid.Append([row[0], row[1], row[2], row[3], row[4]])

    def limpaElementos(self):
        self.txtId.Clear()
        self.txtNomePais.Clear()
        self.txtNomeCapital.Clear()
        self.txtIso2.Clear()
        self.txtIso3.Clear()

        self.txtId.Disable()
        self.txtNomePais.Disable()
        self.txtNomeCapital.Disable()
        self.txtIso2.Disable()
        self.txtIso3.Disable()

        self.botaoSalva.Disable()
        self.botaoDelete.Disable()

    def selecionaLinha(self, event):
        item = self.grid.GetFocusedItem()

        idPais = self.grid.GetItemText(item, 0)

        if idPais.isdigit():
            lista = self.pais.buscaPais(idPais)

            self.txtId.SetValue(str(lista[0]))
            self.txtNomePais.SetValue(lista[1])
            self.txtNomeCapital.SetValue(lista[2])
            self.txtIso2.SetValue(lista[3])
            self.txtIso3.SetValue(lista[4])

            self.txtNomePais.Enable()
            self.txtNomeCapital.Enable()
            self.txtIso2.Enable()
            self.txtIso3.Enable()

            self.botaoSalva.Enable()
            self.botaoDelete.Enable()

    def salvaElemento(self, event):
        self.pais.setnomePais(self.txtNomePais.GetValue())
        self.pais.setnomeCapital(self.txtNomeCapital.GetValue())
        self.pais.setiso2(self.txtIso2.GetValue())
        self.pais.setiso3(self.txtIso3.GetValue())

        if self.insert:
            self.pais.insere()
            self.insert = False
        else:
            self.pais.update(str(self.txtId.GetValue()))

        self.limpaElementos()

        self.encheGrid()

    def deletaElemento(self, event):
        super(FrmPais, self).deletaElemento(event)
        if self.prossegueEliminacao:
            self.pais.delete(str(self.txtId.GetValue()))

            self.limpaElementos()

            self.encheGrid()

    def habilitaNovo(self, event):
        self.txtId.Clear()
        self.txtNomePais.Clear()
        self.txtNomeCapital.Clear()
        self.txtIso2.Clear()
        self.txtIso3.Clear()

        self.txtNomePais.Enable()
        self.txtNomeCapital.Enable()
        self.txtIso2.Enable()
        self.txtIso3.Enable()

        self.botaoSalva.Enable()
        self.insert = True

    def cancelaOperacao(self, event):
        self.limpaElementos()

def main():
    app = wx.App()
    frmPais = FrmPais()
    app.MainLoop()


if __name__ == '__main__':
    main()

