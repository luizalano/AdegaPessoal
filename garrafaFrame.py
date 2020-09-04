# coding: utf-8
from garrafa import *
from pais import *
from pacotesMG.wxComponetesMG import FrameMG
import wx
import wx.grid as gridlib


class FrmGarrafa(FrameMG):
    insert = False
    caminho = '..\\pacotesMG\\icones\\'

    def __init__(self):
        self.garrafa = Garrafa()

        super(FrmGarrafa, self).__init__(None, 'Cadastro de Garrafas', 800, 700, 0)

        self.criaComponentes()

    def criaComponentes(self):
        X = self.posx(1)
        Y = self.posy(0)
        tamX = self.larguraEmPx(106)
        tamY = self.alturaEmPx(13)

        self.grid = wx.ListCtrl(self.painel, pos=(X, Y), size=(tamX, tamY),
                                style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.BORDER_SUNKEN)

        label01, self.txtId = self.criaCaixaDeTexto(self.painel, 13, 10, 40, 'ID', 0, xcol=1, tamanho = 6)
        self.txtId.Disable()

        label02, self.txtNomeGarrafa = self.criaCaixaDeTexto(self.painel, 13, 80, 520, 'Nome da garrafa',
                                                             self.garrafa.sqlBuscaTamanho('nomegarrafa'), xcol = 11, tamanho = 50)

        label03, self.txtVolume = self.criaCaixaDeTexto(self.painel, 13, 10, 250, 'Volume (ml)',
                                                             self.garrafa.sqlBuscaTamanho('volume'), xcol = 75, tamanho = 10)

        self.limpaElementos()

        # self.grid.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha, self.grid)

        self.encheGrid()

        self.Show()

    def encheGrid(self):
        '''
        u.idgarrafa, u.nomegarrafa, u.idpais, p.nomepais
        '''
        self.grid.ClearAll()
        self.grid.InsertColumn(0, 'id', width=self.larguraEmPx(8))
        self.grid.InsertColumn(1, 'Nome da garrafa', width=self.larguraEmPx(40))
        self.grid.InsertColumn(3, 'Volume', width=self.larguraEmPx(20))

        self.lista = self.garrafa.getAll()

        for row in self.lista:
            self.grid.Append([row[0], row[1], row[2]])

    def limpaElementos(self):
        self.txtId.Clear()
        self.txtNomeGarrafa.Clear()
        self.txtVolume.Clear()

        self.txtNomeGarrafa.Disable()
        self.txtVolume.Disable()

        self.botaoSalva.Disable()
        self.botaoDelete.Disable()

    def selecionaLinha(self, event):
        item = self.grid.GetFocusedItem()

        idGarrafa = self.grid.GetItemText(item, 0)

        if idGarrafa.isdigit():
            lista = self.garrafa.buscaGarrafa(idGarrafa)

            self.txtId.SetValue(str(lista[0]))
            self.txtNomeGarrafa.SetValue(lista[1])
            self.txtVolume.SetValue(str(lista[2]))

            self.txtNomeGarrafa.Enable()
            self.txtVolume.Enable()

            self.botaoSalva.Enable()
            self.botaoDelete.Enable()

    def salvaElemento(self, event):
        self.garrafa.setnomeGarrafa(self.txtNomeGarrafa.GetValue())
        self.garrafa.setvolume(int(self.txtVolume.GetValue()))

        if self.insert:
            self.garrafa.insere()
            self.insert = False
        else:
            self.garrafa.update(str(self.txtId.GetValue()))

        self.limpaElementos()

        self.encheGrid()

    def deletaElemento(self, event):
        super(FrmGarrafa, self).deletaElemento(event)
        if self.prossegueEliminacao:
            self.garrafa.delete(str(self.txtId.GetValue()))

            self.limpaElementos()

            self.encheGrid()

    def habilitaNovo(self, event):
        self.limpaElementos()

        self.txtNomeGarrafa.Enable()
        self.txtVolume.Enable()

        self.botaoSalva.Enable()

        self.insert = True

    def cancelaOperacao(self, event):
        self.limpaElementos()

def main():
    app = wx.App()
    frmGarrafa = FrmGarrafa()
    app.MainLoop()


if __name__ == '__main__':
    main()

