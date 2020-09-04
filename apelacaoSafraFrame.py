# coding: utf-8
from apelacaoSafra import *
from apelacao import *
from datetime import date, datetime
from pacotesMG.wxComponetesMG import FrameMG
import wx
import wx.grid as gridlib


class FrmApelacaoSafra(FrameMG):
    insert = False
    caminho = '..\\pacotesMG\\icones\\'

    def __init__(self):
        self.apelacaoSafra = ApelacaoSafra()
        self.apelacao = Apelacao()

        self.hoje = datetime.now()
        self.anoAtual = self.hoje.year
        self.colunaGrid = 0

        super(FrmApelacaoSafra, self).__init__(None, 'Cadastro de safras por apelações', 800, 700, 0)

        self.criaComponentes()

    def criaComponentes(self):
        X = self.posx(1)
        Y = self.posy(0)
        tamX = self.larguraEmPx(106)
        tamY = self.alturaEmPx(13)

        self.grid = wx.ListCtrl(self.painel, pos=(X, Y), size=(tamX, tamY),
                                style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.BORDER_SUNKEN)

        label01, self.txtId = self.criaCaixaDeTexto(self.painel, 13, 10, 40, 'ID', 0, xcol=1, tamanho=6)


        label02, self.cbNomeApelacao = self.criaCombobox(self.painel, label = 'Nome da Apelação', linha=13, coluna = 11,
                                                 tamanho=60, maxlen=self.apelacao.sqlBuscaTamanho('nomeapelacao'))


        label05, self.txtSafra = self.criaCaixaDeTexto(self.painel, 13, 80, 520, 'Safra', 4, xcol=78, tamanho=5)
        # validator=self.validaSafra())
        label06, self.txtNota = self.criaCaixaDeTexto(self.painel, 13, 80, 520, 'Nota', 2, xcol=88, tamanho=3)

        self.grid.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha)
        self.grid.Bind(wx.EVT_LIST_COL_CLICK, self.pegaColuna)
        self.Bind(wx.EVT_TEXT, self.validaSafra(), self.txtSafra)

        self.encheGrid()

        self.Show()

    def validaSafra(self):
        conteudo = self.txtSafra.GetValue()
        if len(conteudo) > 0:
            if not conteudo.isdigit():
                dlg = wx.MessageDialog(None, 'Valor digitado nao é um inteiro!', 'Erro de conteúdo',
                                       wx.OK | wx.ICON_ERROR)
                result = dlg.ShowModal()
            else:
                valor = int(conteudo)
                if valor < 1900 or valor > self.anoAtual:
                    dlg = wx.MessageDialog(None, 'Safra deve estar entre 1900 e ' + str(self.anoAtual) + ' !',
                                           'Erro de conteúdo', wx.OK | wx.ICON_ERROR)
                    result = dlg.ShowModal()

    def encheComboBoxApelacao(self):
        lista = self.apelacao.getAll()
        self.cbNomeApelacao.Clear()

        for row in lista:
            self.cbNomeApelacao.Append(row[1])

    def encheGrid(self):
        '''
        select as.idapelacaosafra, as.idapelacao, a.nomeapelacao, as.safra, as.nota
        '''
        self.limpaElementos()

        menor = self.apelacaoSafra.getMinSafra()
        maior = self.apelacaoSafra.getMaxSafra()

        self.grid.ClearAll()
        self.grid.InsertColumn(0, 'Nome da apelação', width=self.larguraEmPx(30))

        indice = 0

        for i in range(maior, menor -1, -1):
            indice += 1
            self.grid.InsertColumn(indice, str(i), width=self.larguraEmPx(5))

        self.lista = self.apelacaoSafra.getAll()

        anterior = ''
        listaApelacao = []
        for row in self.lista:
            atual = row[2]
            if anterior == '':
                anterior = atual
                listaApelacao.clear()
                listaApelacao.append(row[2])

                for i in range(maior, menor -1, -1):
                    listaApelacao.append(0)

            if atual != anterior:
                self.grid.Append(listaApelacao)

                anterior = atual
                listaApelacao.clear()
                listaApelacao.append(row[2])

                for i in range(maior, menor -1, -1):
                    listaApelacao.append(0)

            ano = row[3]

            indice = maior - ano + 1
            listaApelacao[indice] = row[4]

        self.grid.Append(listaApelacao)

        self.encheComboBoxApelacao()

    def limpaElementos(self):
        self.txtId.Clear()
        self.cbNomeApelacao.SetSelection(-1)
        self.txtSafra.Clear()
        self.txtNota.Clear()

        self.txtId.Disable()
        self.cbNomeApelacao.Disable()
        self.txtSafra.Disable()
        self.txtNota.Disable()

        self.botaoSalva.Disable()
        self.botaoDelete.Disable()

    def pegaColuna(self, event):
        self.colunaGrid = event.GetColumn()

    def indiceDaApelacaoCb(self, nomeApelacao):
        indice = 0
        i = 0
        max = self.cbNomeApelacao.Count
        while i < max:
            lido = self.cbNomeApelacao.GetString(i)
            if lido == nomeApelacao:
                indice = i
                i = max
            i += 1

        return indice

    def selecionaLinha(self, event):
        #self.colunaGrid = event.GetColumn()
        if self.colunaGrid > 0:
            item = self.grid.GetFocusedItem()
            nomeApelacao = self.grid.GetItemText(item, 0)

            rowid = self.grid.GetColumn(self.colunaGrid)
            safra = int(rowid.GetText())

            if len(nomeApelacao) > 0:
                lista = self.apelacaoSafra.buscaApelacaoSafraPorNomeSafra(nomeApelacao, safra)

                if len(lista) >= 1:
                    self.txtId.SetValue(str(lista[0]))

                    self.cbNomeApelacao.SetSelection(self.indiceDaApelacaoCb(lista[2]))

                    self.txtSafra.SetValue(str(lista[3]))
                    self.txtNota.SetValue(str(lista[4]))

                    self.cbNomeApelacao.Enable()
                    self.txtSafra.Enable()
                    self.txtNota.Enable()

                    self.botaoSalva.Enable()
                    self.botaoDelete.Enable()
                else:
                    listaApelacao = self.apelacao.buscaApelacaoPorNome(nomeApelacao)
                    self.habilitaNovo(event)
                    self.cbNomeApelacao.SetSelection(self.indiceDaApelacaoCb(listaApelacao[1]))
                    self.txtSafra.SetValue(str(safra))

    def salvaElemento(self, event):
        self.apelacaoSafra.setidApelacao(self.apelacao.buscaIdApelacao(self.cbNomeApelacao.GetValue()))
        self.apelacaoSafra.setnota(int(self.txtNota.GetValue()))
        self.apelacaoSafra.setsafra(int(self.txtSafra.GetValue()))

        if self.insert:
            self.apelacaoSafra.insere()
            self.insert = False
        else:
            self.apelacaoSafra.update(str(self.txtId.GetValue()))

        self.limpaElementos()

        self.encheGrid()

    def deletaElemento(self, event):
        super(FrmApelacaoSafra, self).deletaElemento(event)
        if self.prossegueEliminacao:
            self.apelacaoSafra.delete(str(self.txtId.GetValue()))

            self.limpaElementos()

            self.encheGrid()

    def habilitaNovo(self, event):
        self.limpaElementos()

        self.cbNomeApelacao.Enable()
        self.txtSafra.Enable()
        self.txtNota.Enable()

        self.botaoSalva.Enable()

        self.insert = True

    def cancelaOperacao(self, event):
        self.limpaElementos()


def main():
    app = wx.App()
    frmApelacaoSafra = FrmApelacaoSafra()
    app.MainLoop()


if __name__ == '__main__':
    main()

