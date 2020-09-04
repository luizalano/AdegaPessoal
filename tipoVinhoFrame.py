# coding: utf-8
from tipovinho import *
from pacotesMG.wxComponetesMG import FrameMG
import wx
import wx.grid as gridlib


class FrmTipoVinho(FrameMG):
    insert = False
    caminho = '..\\pacotesMG\\icones\\'

    def __init__(self):
        self.tipoVinho = TipoVinho()

        super(FrmTipoVinho, self).__init__(None, 'Cadastro de tipos de vinhos', 800, 700, 0)

        self.criaComponentes()

    def criaComponentes(self):
        X = self.posx(1)
        Y = self.posy(0)
        tamX = self.larguraEmPx(106)
        tamY = self.alturaEmPx(12)

        self.grid = wx.ListCtrl(self.painel, pos=(X, Y), size=(tamX, tamY),
                                style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.BORDER_SUNKEN)

        label01, self.txtId = self.criaCaixaDeTexto(self.painel, 12, 10, 40, 'ID', 0, xcol=1, tamanho = 6)
        label02, self.txtNomeTipoVinho = self.criaCaixaDeTexto(self.painel, 13, 80, 520, 'Nome do tipo de vinho',
                                                             self.tipoVinho.sqlBuscaTamanho('nometipovinho'), xcol = 1, tamanho = 90)

        self.limpaElementos()

        # self.grid.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha, self.grid)

        self.encheGrid()

        self.Show()

    def encheGrid(self):
        '''
        u.idtipoVinho, u.nometipoVinho, u.corcasca, u.idpais, p.nomepais
        '''
        self.grid.ClearAll()
        self.grid.InsertColumn(0, 'id', width=self.larguraEmPx(6))
        self.grid.InsertColumn(1, 'Nome do tipo de vinho', width=self.larguraEmPx(90))

        self.lista = self.tipoVinho.getAll()

        for row in self.lista:
            self.grid.Append([row[0], row[1]])

    def limpaElementos(self):
        self.txtId.Clear()
        self.txtNomeTipoVinho.Clear()

        self.txtId.Disable()
        self.txtNomeTipoVinho.Disable()

        self.botaoSalva.Disable()
        self.botaoDelete.Disable()

    def selecionaLinha(self, event):
        item = self.grid.GetFocusedItem()

        idTipoVinho = self.grid.GetItemText(item, 0)

        if idTipoVinho.isdigit():
            lista = self.tipoVinho.buscaTipoVinho(idTipoVinho)

            self.txtId.SetValue(str(lista[0]))
            self.txtNomeTipoVinho.SetValue(lista[1])

            self.txtNomeTipoVinho.Enable()

            self.botaoSalva.Enable()
            self.botaoDelete.Enable()

    def salvaElemento(self, event):
        self.tipoVinho.setnomeTipoVinho(self.txtNomeTipoVinho.GetValue())

        if self.insert:
            self.tipoVinho.insere()
            self.insert = False
        else:
            self.tipoVinho.update(str(self.txtId.GetValue()))

        self.limpaElementos()

        self.encheGrid()

    def deletaElemento(self, event):
        super(FrmTipoVinho, self).deletaElemento(event)
        if self.prossegueEliminacao:
            self.tipoVinho.delete(str(self.txtId.GetValue()))

            self.limpaElementos()

            self.encheGrid()

    def habilitaNovo(self, event):
        self.limpaElementos()

        self.txtNomeTipoVinho.Enable()

        self.botaoSalva.Enable()

        self.insert = True

    def cancelaOperacao(self, event):
        self.limpaElementos()

def main():
    app = wx.App()
    frmTipoVinho = FrmTipoVinho()
    app.MainLoop()


if __name__ == '__main__':
    main()

