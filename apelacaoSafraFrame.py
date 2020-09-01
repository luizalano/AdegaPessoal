# coding: utf-8
from apelacaoSafra import *
from apelacao import *
from pacotesMG.conectaDataBaseMG import *
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

        super(FrmApelacaoSafra, self).__init__(None, 'Cadastro de safras por apelações', 800, 700, 0)

        self.criaComponentes()

    def criaComponentes(self):
        X = self.posx(1)
        Y = self.posy(0)
        tamX = self.larguraEmPx(106)
        tamY = self.alturaEmPx(12)

        self.grid = wx.ListCtrl(self.painel, pos=(X, Y), size=(tamX, tamY),
                                style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.BORDER_SUNKEN)

        label01, self.txtId = self.criaCaixaDeTexto(self.painel, 12, 10, 40, 'ID', 0, xcol=1, tamanho=6)

        label02, self.txtApelacaoChave = self.criaCaixaDeTexto(self.painel, 12, 10, 250,
                                                               'Entre com o termo para pesquisa da apelação',
                                                               self.apelacao.sqlBuscaTamanho('nomeapelacao'),
                                                               xcol=11, tamanho=80)

        iconePesquisa = wx.Bitmap(self.caminho + 'search32.ico')
        self.botaoPesquisa = wx.BitmapButton(self.painel, bitmap=iconePesquisa,
                                             pos=(680, self.posy(12)))
        self.botaoPesquisa.Bind(wx.EVT_BUTTON, self.pesquisaApelacao)

        label03, self.txtIdApelacao = self.criaCaixaDeTexto(self.painel, 13, 340, 40, 'ID', 0, xcol=1, tamanho=6)
        label04, self.txtNomeApelacao = self.criaCaixaDeTexto(self.painel, 13, 400, 200, 'Nome da apelação', 0,
                                                              xcol=11, tamanho=60)

        label05, self.txtSafra = self.criaCaixaDeTexto(self.painel, 13, 80, 520, 'Safra', 4, xcol=78, tamanho=5)
        # validator=self.validaSafra())
        label06, self.txtNota = self.criaCaixaDeTexto(self.painel, 13, 80, 520, 'Nota', 2, xcol=88, tamanho=3)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha, self.grid)
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

    def pesquisaApelacao(self, event):
        chave = self.txtApelacaoChave.GetValue()

        if len(chave) > 0:
            lista = self.apelacao.pesquisaApelacao(chave)

            resultado = None

            pesquisaDialog = wx.SingleChoiceDialog(None, 'Escolha a apelação correta',
                                                   'Pesquisa apelações', lista, style=wx.OK | wx.CANCEL | wx.CENTRE,
                                                   pos=wx.DefaultPosition)
            if pesquisaDialog.ShowModal() == wx.ID_OK:
                resultado = pesquisaDialog.GetStringSelection()

            if resultado:
                res = resultado.split('|')
                self.txtNomeApelacao.SetValue(res[1])
                self.txtIdApelacao.SetValue(str(res[0]))

            pesquisaDialog.Destroy

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
        for i in range(menor, maior + 1):
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

                for i in range(menor, maior + 1):
                    listaApelacao.append(0)

            if atual != anterior:
                self.grid.Append(listaApelacao)

                anterior = atual
                listaApelacao.clear()
                listaApelacao.append(row[2])

                for i in range(menor, maior + 1):
                    listaApelacao.append(0)
            else:
                ano = row[3]
                indice = ano - menor + 1
                listaApelacao[indice] = row[4]

        self.grid.Append(listaApelacao)

    def limpaElementos(self):
        self.txtId.Clear()
        self.txtApelacaoChave.Clear()
        self.txtIdApelacao.Clear()
        self.txtNomeApelacao.Clear()
        self.txtSafra.Clear()
        self.txtNota.Clear()

        self.txtId.Disable()
        self.txtApelacaoChave.Disable()
        self.txtIdApelacao.Disable()
        self.txtNomeApelacao.Disable()
        self.txtSafra.Disable()
        self.txtNota.Disable()

        self.botaoSalva.Disable()
        self.botaoDelete.Disable()
        self.botaoPesquisa.Disable()

    def selecionaLinha(self, event):
        item = self.grid.GetFocusedItem()

        idApelacaoSafra = self.grid.GetItemText(item, 0)

        if idApelacaoSafra.isdigit():
            lista = self.apelacaoSafra.buscaApelacaoSafra(idApelacaoSafra)

            self.txtId.SetValue(str(lista[0]))
            self.txtNomeApelacao.SetValue(lista[2])
            self.txtIdApelacao.SetValue(str(lista[1]))
            self.txtSafra.SetValue(str(lista[3]))
            self.txtNota.SetValue(str(lista[4]))

            self.txtApelacaoChave.Enable()
            self.txtSafra.Enable()
            self.txtNota.Enable()

            self.botaoSalva.Enable()
            self.botaoDelete.Enable()
            self.botaoPesquisa.Enable()

    def salvaElemento(self, event):
        self.apelacaoSafra.setidApelacao(self.txtIdApelacao.GetValue())
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

        self.txtApelacaoChave.Enable()
        self.txtSafra.Enable()
        self.txtNota.Enable()

        self.botaoSalva.Enable()
        self.botaoPesquisa.Enable()

        self.insert = True

    def cancelaOperacao(self, event):
        self.limpaElementos()


def main():
    app = wx.App()
    frmApelacaoSafra = FrmApelacaoSafra()
    app.MainLoop()


if __name__ == '__main__':
    main()

