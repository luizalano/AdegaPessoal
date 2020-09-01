# coding: utf-8
from apelacao import *
from pais import *
from pacotesMG.conectaDataBaseMG import *

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

        label03, self.txtPaisChave = self.criaCaixaDeTexto(self.painel, 13, 10, 250, 'Entre com o termo para pesquisa do país',
                                                             self.pais.sqlBuscaTamanho('nomepais'), xcol = 1, tamanho = 30)

        iconePesquisa = wx.Bitmap(self.caminho + 'search32.ico')
        self.botaoPesquisa = wx.BitmapButton(self.painel, bitmap=iconePesquisa,
            pos=(250, self.posy(13)))
        self.botaoPesquisa.Bind(wx.EVT_BUTTON, self.pesquisaPais)

        label04, self.txtIdPais = self.criaCaixaDeTexto(self.painel, 13, 340, 40, 'ID', 0, xcol = 42, tamanho = 6)
        label05, self.txtNomePais = self.criaCaixaDeTexto(self.painel, 13, 400, 200, 'Nome do país', 0, xcol = 52, tamanho = 30)

        self.limpaElementos()

        # self.grid.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha, self.grid)

        self.encheGrid()

        self.Show()

    def pesquisaPais(self, event):
        chave = self.txtPaisChave.GetValue()

        if len(chave) > 0:
            lista = self.pais.pesquisaPais(chave)

            resultado = None

            pesquisaDialog = wx.SingleChoiceDialog(None, 'Escolha o país correto',
                                                   'Pesquisa países', lista, style=wx.OK | wx.CANCEL | wx.CENTRE,
                                                   pos=wx.DefaultPosition)
            if pesquisaDialog.ShowModal() == wx.ID_OK:
                resultado = pesquisaDialog.GetStringSelection()

            if resultado:
                res = resultado.split('|')
                self.txtNomePais.SetValue(res[1])
                self.txtIdPais.SetValue(str(res[0]))

            pesquisaDialog.Destroy

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

    def limpaElementos(self):
        self.txtId.Clear()
        self.txtNomeApelacao.Clear()
        self.txtPaisChave.Clear()
        self.txtIdPais.Clear()
        self.txtNomePais.Clear()

        self.txtId.Disable()
        self.txtNomeApelacao.Disable()
        self.txtPaisChave.Disable()
        self.txtIdPais.Disable()
        self.txtNomePais.Disable()

        self.botaoSalva.Disable()
        self.botaoDelete.Disable()
        self.botaoPesquisa.Disable()

    def selecionaLinha(self, event):
        item = self.grid.GetFocusedItem()

        idApelacao = self.grid.GetItemText(item, 0)

        if idApelacao.isdigit():
            lista = self.apelacao.buscaApelacao(idApelacao)

            self.txtId.SetValue(str(lista[0]))
            self.txtNomeApelacao.SetValue(lista[1])
            self.txtIdPais.SetValue(str(lista[2]))
            self.txtNomePais.SetValue(lista[3])

            self.txtNomeApelacao.Enable()
            self.txtPaisChave.Enable()

            self.botaoSalva.Enable()
            self.botaoDelete.Enable()
            self.botaoPesquisa.Enable()

    def salvaElemento(self, event):
        self.apelacao.setnomeApelacao(self.txtNomeApelacao.GetValue())
        self.apelacao.setidPais(self.txtIdPais.GetValue())

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
        self.txtPaisChave.Enable()

        self.botaoSalva.Enable()
        self.botaoPesquisa.Enable()

        self.insert = True

    def cancelaOperacao(self, event):
        self.limpaElementos()

def main():
    app = wx.App()
    frmApelacao = FrmApelacao()
    app.MainLoop()


if __name__ == '__main__':
    main()

