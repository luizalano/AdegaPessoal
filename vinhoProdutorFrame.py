# coding: utf-8
from vinhoProdutor import *
from tenuta import *
from apelacao import *
from tipovinho import *
from pais import *

from pacotesMG.wxComponetesMG import FrameMG
import wx
import wx.grid as gridlib


class FrmVinhoProdutor(FrameMG):
    insert = False
    caminho = '..\\pacotesMG\\icones\\'

    def __init__(self):
        self.vinhoProdutor = VinhoProdutor()
        self.tenuta = Tenuta()
        self.apelacao = Apelacao()
        self.tipoVinho = TipoVinho()
        self.pais = Pais()

        self.idTenuta = 0
        self.idPais = 0
        self.idVinhoProdutor = 0
        self.idApelacao = 0
        self.idTipoVinho = 0

        super(FrmVinhoProdutor, self).__init__(None, 'Cadastro de vinho por produtor', 1250, 700, 0)

        self.criaComponentes()

    def criaComponentes(self):
        X = self.posx(1)
        Y = self.posy(2)
        tamX = self.larguraEmPx(80)
        tamY = self.alturaEmPx(9)

        X0 = 84

        label00, self.cbTenuta = self.criaCombobox(self.painel, label = 'Produtor', linha=0, coluna = 1,
                                                 tamanho=80, maxlen=self.tenuta.sqlBuscaTamanho('nometenuta'))
        self.cbTenuta.Bind(wx.EVT_COMBOBOX, self.tenutaSelecionada)

        label03, self.txtNomePais = self.criaCaixaDeTexto(self.painel, 1, 10, 40, 'País onde está o produtor',
                                                          0, xcol=1, tamanho = 80)
        self.txtNomePais.Disable()

        label98, self.txtSelecao = self.criaCaixaDeTexto(self.painel, 1, 10, 40, 'Seleção',
                                                          0, xcol=X0 + 1, tamanho = 80)
        self.txtNomePais.Disable()


        self.grid = wx.ListCtrl(self.painel, pos=(X, Y), size=(tamX, tamY),
                                style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.BORDER_SUNKEN)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.clicou, self.grid)

        label04, self.txtNomeVinho = self.criaCaixaDeTexto(self.painel, 11, 80, 520, 'Nome do vinho',
                                                           self.vinhoProdutor.sqlBuscaTamanho('nomevinho'),
                                                                   xcol = 1, tamanho = 80)

        label05, self.cbApelacao = self.criaCombobox(self.painel, label = 'Apelação', linha=12, coluna = 1,
                                                 tamanho=40, maxlen=self.apelacao.sqlBuscaTamanho('nomapelacao'))
        self.cbApelacao.Bind(wx.EVT_COMBOBOX, self.apelacaoSelecionada)

        label06, self.cbTipoVinho = self.criaCombobox(self.painel, label = 'Tipo de vinho', linha=12, coluna = 47,
                                                 tamanho=34, maxlen=self.tipoVinho.sqlBuscaTamanho('nometipovinho'))
        self.cbTipoVinho.Bind(wx.EVT_COMBOBOX, self.tipoVinhoSelecionado)

        label07, self.txtComplemento = self.criaCaixaDeTexto(self.painel, 13, 80, 520, 'Complemento',
                                                           self.vinhoProdutor.sqlBuscaTamanho('complemento'),
                                                                   xcol = 1, tamanho = 80)

        self.limpaElementos()

        # self.grid.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha, self.grid)

        self.encheComboBoxProdutor()

        self.Show()

    def clicou(self, event):
        item = self.grid.GetFocusedItem()
        print (item)
        self.txtSelecao.SetValue(self.grid.GetItemText(item, 1))

    def encheComboBoxProdutor(self):
        lista = self.tenuta.getAll()
        self.cbTenuta.Clear()

        for row in lista:
            self.cbTenuta.Append(row[1])

    def encheComboBoxApelacao(self):
        lista = self.apelacao.getAll(idpais=self.idPais)
        self.cbApelacao.Clear()

        for row in lista:
            self.cbApelacao.Append(row[1])

    def encheComboBoxTipoVinho(self):
        lista = self.tipoVinho.getAll()
        self.cbTipoVinho.Clear()

        for row in lista:
            self.cbTipoVinho.Append(row[1])

    def tenutaSelecionada(self, event):
        chave = self.cbTenuta.GetValue()

        lista = self.tenuta.buscaTenutaPorNome(chave)

        if len(lista) > 0:
            self.idTenuta = lista[0]
            self.idPais = lista[2]
            self.txtNomePais.SetValue(lista[3])
            self.encheGrid(self.idTenuta)

    def apelacaoSelecionada(self, event):
        chave = self.cbApelacao.GetValue()

        lista = self.apelacao.buscaApelacaoPorNome(chave)

        if len(lista) > 0:
            self.idApelacao = lista[0]

    def tipoVinhoSelecionado(self, event):
        chave = self.cbTipoVinho.GetValue()

        lista = self.tipoVinho.buscaTipoVinhoPorNome(chave)

        if len(lista) > 0:
            self.idTipoVinho = lista[0]

    def encheGrid(self, argId):
        '''
        vp.idvinhoprodutor, vp.idprodutor, t.nometenuta, vp.nomevinho,
        vp.idapelacao, a.nomeapelacao, cp.idtipovinho, t.nometipovinho,
        vp.complemento, t.idpais, p.nomepais
        '''
        self.grid.ClearAll()
        self.grid.InsertColumn(0, 'id', width=self.larguraEmPx(2))
        self.grid.InsertColumn(1, 'Nome do vinho', width=self.larguraEmPx(30))
        self.grid.InsertColumn(2, 'Tipo do vinho', width=self.larguraEmPx(20))
        self.grid.InsertColumn(3, 'Apelação', width=self.larguraEmPx(20))

        self.lista = self.vinhoProdutor.getAll(idtenuta = self.idTenuta)

        for row in self.lista:
            self.grid.Append([row[0], row[3], row[7], row[5]])

        self.encheComboBoxApelacao()
        self.encheComboBoxTipoVinho()

    def limpaElementos(self):
        self.IdVinhoProdutor = 0
        self.idApelacao = 0
        self.idTipoVinho = 0

        self.txtNomeVinho.Clear()
        self.cbApelacao.SetSelection(-1)
        self.cbTipoVinho.SetSelection(-1)
        self.txtComplemento.Clear()

        self.txtNomeVinho.Disable()
        self.cbApelacao.Disable()
        self.cbTipoVinho.Disable()
        self.txtComplemento.Disable()

        self.botaoSalva.Disable()
        self.botaoDelete.Disable()

    def indiceCb(self, cb, chave):
        indice = 0
        i = 0
        max = cb.Count
        while i < max:
            lido = cb.GetString(i)
            if lido == chave:
                indice = i
                i = max
            i += 1

        return indice


    def selecionaLinha(self, event):
        item = self.grid.GetFocusedItem()

        idVinhoProdutor = self.grid.GetItemText(item, 0)

        if idVinhoProdutor.isdigit():
            lista = self.vinhoProdutor.buscaVinhoProdutor(idVinhoProdutor)

            self.idVinhoProdutor = lista[0]

            self.txtNomeVinho.SetValue(lista[3])

            self.cbApelacao.SetSelection(self.indiceCb(self.cbApelacao, lista[5]))
            self.cbTipoVinho.SetSelection(self.indiceCb(self.cbTipoVinho, lista[7]))

            self.idApelacao = lista[4]
            self.idTipoVinho = lista[6]

            self.txtComplemento.SetValue(lista[8])

            self.txtNomeVinho.Enable()
            self.cbApelacao.Enable()
            self.cbTipoVinho.Enable()
            self.txtComplemento.Enable()

            self.botaoSalva.Enable()
            self.botaoDelete.Enable()

    def salvaElemento(self, event):
        self.vinhoProdutor.setidApelacao(self.idApelacao)
        self.vinhoProdutor.setidTenuta(self.idTenuta)
        self.vinhoProdutor.setnomeVinho(self.txtNomeVinho.GetValue())
        self.vinhoProdutor.setcomplemento(self.txtComplemento.GetValue())
        self.vinhoProdutor.setidTipoVinho(self.idTipoVinho)

        if self.insert:
            self.vinhoProdutor.insere()
            self.insert = False
        else:
            self.vinhoProdutor.update(str(self.idVinhoProdutor))

        self.limpaElementos()

        self.encheGrid(self.idTenuta)

    def deletaElemento(self, event):
        super(FrmVinhoProdutor, self).deletaElemento(event)
        if self.prossegueEliminacao:
            self.vinhoProdutor.delete(str(self.IdVinhoProdutor))

            self.limpaElementos()

            self.encheGrid(self.idTenuta)

    def habilitaNovo(self, event):
        self.limpaElementos()

        self.txtNomeVinho.Enable()
        self.cbApelacao.Enable()
        self.cbTipoVinho.Enable()
        self.txtComplemento.Enable()

        self.botaoSalva.Enable()

        self.insert = True

    def cancelaOperacao(self, event):
        self.limpaElementos()

def main():
    app = wx.App()
    frmVinhoProdutor = FrmVinhoProdutor()
    app.MainLoop()


if __name__ == '__main__':
    main()

