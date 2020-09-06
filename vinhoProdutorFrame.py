# coding: utf-8
from vinhoProdutor import *
from vinhoProdutorSafra import *
from corte import *
from uva import *
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
        self.vinhoProdutorSafra = VinhoProdutorSafra()
        self.corte = Corte()
        self.tenuta = Tenuta()
        self.apelacao = Apelacao()
        self.tipoVinho = TipoVinho()
        self.pais = Pais()
        self.uva = Uva()

        self.idTenuta = 0
        self.idPais = 0
        self.idVinhoProdutor = 0
        self.idApelacao = 0
        self.idTipoVinho = 0

        self.idVinhoProdutorSafra = 0
        self.idVinhoProdutor = 0
        self.safra = 0
        self.beberde = 0
        self.beberate = 0
        self.observacoes = ''

        self.idCorte = 0
        self.idUva = 0
        self.nomeUva = ''
        self.percentual = 0.0
        self.safraDoCorte = 0.0

        self.focoem = 1

        super(FrmVinhoProdutor, self).__init__(None, 'Cadastro de vinho por produtor', 1250, 700, 0, split=True)

        self.criaComponentes()

    def criaComponentes(self):
        X = self.posx(1)
        Y = self.posy(2)
        tamX = self.larguraEmPx(80)
        tamY = self.alturaEmPx(9)

        label00, self.cbTenuta = self.criaCombobox(self.painel, label = 'Produtor', linha=0, coluna = 1,
                                                 tamanho=80, maxlen=self.tenuta.sqlBuscaTamanho('nometenuta'))
        self.cbTenuta.Bind(wx.EVT_COMBOBOX, self.tenutaSelecionada)

        label03, self.txtNomePais = self.criaCaixaDeTexto(self.painel, 1, 10, 40, 'País onde está o produtor',
                                                          0, xcol=1, tamanho = 80)
        self.txtNomePais.Disable()

        self.grid = wx.ListCtrl(self.painel, pos=(X, Y), size=(tamX, tamY),
                                style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.BORDER_SUNKEN)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.clicou, self.grid)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinha, self.grid)


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

        '''
        Segundo Painel 
        '''

        labelSelecao = wx.StaticText(self.painel2, -1, 'Propriedades do Vinho selecionado',
                                     (self.posx(1),25))
        fonteTexto = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        labelSelecao.SetFont(fonteTexto)

        label101, self.txtSelecao = self.criaCaixaDeTexto(self.painel2, 1, 10, 40, 'Vinho selecionado',
                                                          0, xcol=1, tamanho = 80)
        fonteTexto = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.txtSelecao.SetFont(fonteTexto)
        self.txtSelecao.Disable()

        X = self.posx(1)
        Y = self.posy(2)
        tamX = self.larguraEmPx(30)
        tamY = self.alturaEmPx(4)
        self.gridSafra = wx.ListCtrl(self.painel2, pos=(X, Y), size=(tamX, tamY),
                                style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.BORDER_SUNKEN)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.clicouSafra, self.gridSafra)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinhaSafra, self.gridSafra)

        label102, self.txtSafra = self.criaCaixaDeTexto(self.painel2, 2, 10, 40, 'Safra',
                                                          4, xcol=34, tamanho = 4)

        label103, self.txtBeberDe = self.criaCaixaDeTexto(self.painel2, 2, 10, 40, 'Beber de',
                                                          4, xcol=55, tamanho = 6)

        label103, self.txtBeberAte = self.criaCaixaDeTexto(self.painel2, 2, 12, 40, 'Beber até',
                                                          4, xcol=75, tamanho = 6)

        label104, self.txtObservacoes = self.criaCaixaDeTextoMultiLinhas(self.painel2, 3, 0, 0, 92, 'Observações',
                                                                         self.vinhoProdutorSafra.sqlBuscaTamanho('observacoes'),
                                                                        xcol=34, tamanhox=47)

        economia = 330
        larg, alt = self.painel2.GetSize()
        self.painel2.SetSize(size=(larg, alt-economia))

        self.levantaBotao(self.botaoSaida, economia)
        self.levantaBotao(self.botaoSalva2, economia)
        self.levantaBotao(self.botaoNovo2, economia)
        self.levantaBotao(self.botaoDelete2, economia)
        self.levantaBotao(self.botaoCancela2, economia)

        self.criaPainel3()

        self.limpaElementos()
        self.limpaElementos2()

        self.encheComboBoxProdutor()

        self.Show()

    def criaPainel3(self):
        larguraPainel1, alturaPainel1 = self.painel.GetSize()
        larguraPainel2, alturaPainel2 = self.painel2.GetSize()

        lar = larguraPainel2
        alt = alturaPainel1 - alturaPainel2

        X = larguraPainel1
        Y = alturaPainel2

        gapx = 40
        gapy = 20

        lp = lar
        ap = alt

        self.painel3 = wx.Panel(self, pos=(X, Y), size=(lar, alt), style=wx.BORDER_RAISED)

        iconeSaida3 = wx.Bitmap(self.caminho + 'close64.ico')
        lb, ab = iconeSaida3.GetSize()
        self.botaoSaida3 = wx.BitmapButton(self.painel3, id=101, bitmap=iconeSaida3,
                                     pos=(lp - lb - gapx, ap - ab - gapy))
        self.Bind(wx.EVT_BUTTON, self.encerraAplicacao, self.botaoSaida3)
        self.botaoSaida.Hide()

        lb, ab = self.iconeNovo.GetSize()
        self.botaoNovo3 = wx.BitmapButton(self.painel3, id=202, bitmap=self.iconeNovo,
            pos=(10, ap - ab - gapy))
        self.Bind(wx.EVT_BUTTON, self.habilitaNovo3, self.botaoNovo3)

        lb, ab = self.iconeSalva.GetSize()
        self.botaoSalva3 = wx.BitmapButton(self.painel3, id=203, bitmap=self.iconeSalva,
            pos=(50, ap - ab - gapy))
        self.botaoSalva3.Disable()
        self.Bind(wx.EVT_BUTTON, self.salvaElemento3, self.botaoSalva3)

        lb, ab = self.iconeDelete.GetSize()
        self.botaoDelete3 = wx.BitmapButton(self.painel3, id=204, bitmap=self.iconeDelete,
            pos=(90, ap - ab - gapy))
        self.botaoDelete3.Disable()
        self.Bind(wx.EVT_BUTTON, self.deletaElemento3, self.botaoDelete3)

        lb, ab = self.iconeCancela.GetSize()
        self.botaoCancela3 = wx.BitmapButton(self.painel3, id=205, bitmap=self.iconeCancela,
            pos=(130, ap - ab - gapy))
        self.Bind(wx.EVT_BUTTON, self.cancelaOperacao3, self.botaoCancela3)


        labelSelecao3 = wx.StaticText(self.painel3, -1, 'Corte do vinho',
                                     (self.posx(1),5))
        fonteTexto = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        labelSelecao3.SetFont(fonteTexto)

        label201, self.txtSelecao3 = self.criaCaixaDeTexto(self.painel3, 0, 10, 40, '',
                                                          0, xcol=1, tamanho = 80)
        fonteTexto = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.txtSelecao3.SetFont(fonteTexto)
        self.txtSelecao3.Disable()

        X = self.posx(1)
        Y = self.posy(1)
        tamX = self.larguraEmPx(40)
        tamY = self.alturaEmPx(5)
        self.gridUva = wx.ListCtrl(self.painel3, pos=(X, Y), size=(tamX, tamY),
                                style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.BORDER_SUNKEN)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.selecionaLinhaUva, self.gridUva)


        label202, self.cbUva = self.criaCombobox(self.painel3, label = 'Uva', linha=1, coluna = 45, tamanho=37)

        label203, self.txtPercentual = self.criaCaixaDeTexto(self.painel3, 2, 12, 40, 'Uso (%)',
                                                          4, xcol=45, tamanho = 6)

        self.botaoRepeteSafra = wx.Button(self.painel3, id=wx.ID_ANY, label='Corte igual à safra anterior',
                                    pos=(self.posx(45), self.posy(4)), size=(self.larguraEmPx(37), self.alturaEmPx(2)))
        self.botaoRepeteSafra.SetFont(fonteTexto)
        self.Bind(wx.EVT_BUTTON, self.repeteSafra, self.botaoRepeteSafra)

        self.limpaElementos3()

    def levantaBotao(self, botao, quanto):
        x, y = botao.GetPosition()
        ponto = wx.Point(x, y-quanto)
        botao.SetPosition(ponto)

    def clicou(self, event):
        item = self.grid.GetFocusedItem()
        self.txtSelecao.SetValue(self.grid.GetItemText(item, 1))
        self.idVinhoProdutor = self.grid.GetItemText(item, 0)
        self.encheGrid2()

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
        self.idVinhoProdutor = 0
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

        self.focoem= 0

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
        if self.focoem == 0 or self.focoem == 1:
            item = self.grid.GetFocusedItem()

            idVinhoProdutor = self.grid.GetItemText(item, 0)

            if idVinhoProdutor.isdigit():
                self.focoem = 1
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
        if self.focoem == 1:
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
        if self.focoem == 1:
            super(FrmVinhoProdutor, self).deletaElemento(event)
            if self.prossegueEliminacao:
                self.vinhoProdutor.delete(str(idVinhoProdutor))

                self.limpaElementos()

                self.encheGrid(self.idTenuta)

    def habilitaNovo(self, event):
        if self.focoem == 0 or self.focoem == 1:
            self.limpaElementos()

            self.txtNomeVinho.Enable()
            self.cbApelacao.Enable()
            self.cbTipoVinho.Enable()
            self.txtComplemento.Enable()

            self.botaoSalva.Enable()

            self.insert = True

            self.focoem = 1

    def cancelaOperacao(self, event):
        self.limpaElementos()

    '''
    
    Segundo painel - Safras
    
    '''

    def clicouSafra(self, event):
        item = self.gridSafra.GetFocusedItem()
        estaSafra = str(self.gridSafra.GetItemText(item, 1))
        esteVinho = self.txtSelecao.GetValue()
        self.safraDoCorte = int(estaSafra)
        self.txtSelecao3.SetValue(estaSafra + ' - ' + esteVinho)
        self.idVinhoProdutorSafra = self.gridSafra.GetItemText(item, 0)
        self.encheGrid3()

    def encheGrid2(self):
        '''
        vps.idvinhoprodutorsafra, vps.idvinhoprodutor, vp.nomevinho, vp.idtenuta
        t.nometenuta, vps.safra, vps.beberde, vps.beberate, vps.observacoes
        '''
        self.gridSafra.ClearAll()
        self.gridSafra.InsertColumn(0, 'id', width=self.larguraEmPx(2))
        self.gridSafra.InsertColumn(1, 'Safra', width=self.larguraEmPx(6))
        self.gridSafra.InsertColumn(2, 'Beber de', width=self.larguraEmPx(8))
        self.gridSafra.InsertColumn(3, 'Até', width=self.larguraEmPx(6))

        self.lista2 = self.vinhoProdutorSafra.getAll(idvinho = self.idVinhoProdutor)
        for row in self.lista2:
            self.gridSafra.Append([row[0], row[5], row[6], row[7]])


    def limpaElementos2(self):
        self.idVinhoProdutorSafra = 0
        self.safra = 0
        self.beberde = 0
        self.beberate = 0
        self.observacoes = ''

        self.txtSafra.Clear()
        self.txtBeberDe.Clear()
        self.txtBeberAte.Clear()
        self.txtObservacoes.Clear()

        self.txtSafra.Disable()
        self.txtBeberDe.Disable()
        self.txtBeberAte.Disable()
        self.txtObservacoes.Disable()

        self.botaoSalva2.Disable()
        self.botaoDelete2.Disable()

        self.focoem= 0

    def selecionaLinhaSafra(self, event):
        if self.focoem == 0 or self.focoem == 2:
            item = self.gridSafra.GetFocusedItem()

            self.idVinhoProdutorSafra = self.gridSafra.GetItemText(item, 0)

            if self.idVinhoProdutorSafra.isdigit():
                self.focoem = 2
                lista = self.vinhoProdutorSafra.getAll(idsafra = self.idVinhoProdutorSafra)

                self.txtSafra.SetValue(str(lista[0][5]))
                self.txtBeberDe.SetValue(str(lista[0][6]))
                self.txtBeberAte.SetValue(str(lista[0][7]))
                self.txtObservacoes.SetValue(lista[0][8])

                self.txtSafra.Enable()
                self.txtBeberDe.Enable()
                self.txtBeberAte.Enable()
                self.txtObservacoes.Enable()

                self.botaoSalva2.Enable()
                self.botaoDelete2.Enable()

    def salvaElemento2(self, event):
        if self.focoem == 2:
            self.vinhoProdutorSafra.setidVinhoProdutor(self.idVinhoProdutor)
            self.vinhoProdutorSafra.setsafra(self.txtSafra.GetValue())
            self.vinhoProdutorSafra.setbeberde(self.txtBeberDe.GetValue())
            self.vinhoProdutorSafra.setbeberate(self.txtBeberAte.GetValue())
            self.vinhoProdutorSafra.setobservacoes(self.txtObservacoes.GetValue())

            if self.insert:
                self.vinhoProdutorSafra.insere()
                self.insert = False
            else:
                self.vinhoProdutorSafra.update(str(self.idVinhoProdutorSafra))

            self.limpaElementos2()

            self.encheGrid2()

    def deletaElemento2(self, event):
        if self.focoem == 2:
            super(FrmVinhoProdutor, self).deletaElemento2(event)
            if self.prossegueEliminacao:
                self.vinhoProdutor.delete(str(self.idVinhoProdutorSafra))

                self.limpaElementos2()

                self.encheGrid2()

    def habilitaNovo2(self, event):
        if self.focoem == 0 or self.focoem == 2:
            if len(self.txtSelecao.GetValue()) > 0:
                self.limpaElementos2()

                self.txtSafra.Enable()
                self.txtBeberDe.Enable()
                self.txtBeberAte.Enable()
                self.txtObservacoes.Enable()

                self.botaoSalva2.Enable()

                self.insert = True

                self.focoem = 2

    def cancelaOperacao2(self, event):
        self.limpaElementos2()


    '''
    
    Terceiro painel - Cortes
    
    '''

    def encheComboBoxUva(self):
        lista = self.uva.getAll()
        self.cbUva.Clear()

        for row in lista:
            self.cbUva.Append(row[1])

    def encheGrid3(self):

        '''
        vpsu.idvinhoprodutorsafrauva, vpsu.iduva, u.nomeuva, vpsu.percentual, vpsu.idvinhoprodutorsafra
        '''
        self.gridUva.ClearAll()
        self.gridUva.InsertColumn(0, 'id', width=self.larguraEmPx(2))
        self.gridUva.InsertColumn(1, 'Uva', width=self.larguraEmPx(25))
        self.gridUva.InsertColumn(2, 'Uso (%)', width=self.larguraEmPx(6))

        self.lista3 = self.corte.getAll(idsafra=self.idVinhoProdutorSafra)
        for row in self.lista3:
            self.gridUva.Append([row[0], row[2], row[3]])

        self.encheComboBoxUva()

    def limpaElementos3(self):
        self.idCorte = 0
        self.idUva = 0
        self.nomeUva = ''
        self.percentual = 0.0

        self.txtPercentual.Clear()
        self.cbUva.SetSelection(-1)

        self.txtPercentual.Disable()
        self.cbUva.Disable()

        self.botaoSalva3.Disable()
        self.botaoDelete3.Disable()

        self.focoem = 0


    def selecionaLinhaUva(self, event):
        if self.focoem == 0 or self.focoem == 3:
            item = self.gridUva.GetFocusedItem()

            self.idCorte = self.gridUva.GetItemText(item, 0)

            if self.idCorte.isdigit():
                self.focoem = 3
                lista = self.corte.getAll(idvpsu=self.idCorte)

                self.txtPercentual.SetValue(str(lista[0][3]))
                self.cbUva.SetSelection(self.indiceCb(self.cbUva, lista[0][2]))

                self.txtPercentual.Enable()
                self.cbUva.Enable()

                self.botaoSalva3.Enable()
                self.botaoDelete3.Enable()

    def repeteSafra(self, event):
        if len(self.txtSelecao3.GetValue()) > 0:

            clausulaSql = ''

            cursor2 = self.corte.conexao.con.cursor()

            try:
                '''
                Primeiro le a safra atual e tenta eliminar o corte
                '''
                clausulaSql = 'select ' \
                              'corte.idcorte, corte.iduva, corte.percentual, corte.idvinhoprodutorsafra, vps.safra, vp.idvinhoprodutor ' \
                              'from corte join vinhoprodutorsafra as vps on vps.idvinhoprodutorsafra = corte.idvinhoprodutorsafra ' \
                              'join  vinhoprodutor as vp on vp.idvinhoprodutor = vps.idvinhoprodutor ' \
                              'where vp.idvinhoprodutor = '
                clausulaSql += str(self.idVinhoProdutor) + ' and vps.safra = ' + str(self.safraDoCorte) + ';'

                self.corte.conexao.cursor.execute(clausulaSql)
                print (clausulaSql)

                row = self.corte.conexao.cursor.fetchone()
                if row != None:
                    clausulaSql  = 'delete from corte '
                    clausulaSql += 'where idvinhoprodutorsafra = ' + str(row[3]) + ';'

                    self.corte.conexao.cursor.execute(clausulaSql)

                '''
                Agora le a safra anterior e repete o corte
                '''
                clausulaSql = 'select ' \
                              'corte.idcorte, corte.iduva, corte.percentual, corte.idvinhoprodutorsafra, vps.safra, vp.idvinhoprodutor ' \
                              'from corte join vinhoprodutorsafra as vps on vps.idvinhoprodutorsafra = corte.idvinhoprodutorsafra ' \
                              'join  vinhoprodutor as vp on vp.idvinhoprodutor = vps.idvinhoprodutor ' \
                              'where vp.idvinhoprodutor = '
                clausulaSql += str(self.idVinhoProdutor) + ' and vps.safra = ' + str(self.safraDoCorte-1) + ';'

                self.corte.conexao.cursor.execute(clausulaSql)

                row = self.corte.conexao.cursor.fetchone()

                while row != None:
                    clausulaSql = "insert into corte (iduva, percentual, idvinhoprodutorsafra) values ("
                    clausulaSql += "" + str(row[1]) + ", "
                    clausulaSql += "" + str(row[2]) + ", "
                    clausulaSql += "" + str(self.idVinhoProdutorSafra) + ");"

                    cursor2.execute(clausulaSql)

                    row = self.corte.conexao.cursor.fetchone()

                self.corte.conexao.con.commit()

            except:
                self.corte.conexao.con.rollback()
                dlg = wx.MessageDialog(None, clausulaSql, 'Erro ao repetir os dados do corte!', wx.OK | wx.ICON_ERROR)
                result = dlg.ShowModal()

            self.encheGrid3()

    def salvaElemento3(self, event):
        if self.focoem == 3:
            self.corte.setidVinhoProdutorSafra(self.idVinhoProdutorSafra)
            self.corte.setidUva(self.uva.getIdPorNome(self.cbUva.GetValue()))
            self.corte.setpercentual(float(self.txtPercentual.GetValue()))

            if self.insert:
                self.corte.insere()
                self.insert = False
            else:
                self.corte.update(str(self.idCorte))

            self.limpaElementos3()

            self.encheGrid3()


    def deletaElemento3(self, event):
        if self.focoem == 3:
            prossegueEliminacao = False
            dlg = wx.MessageDialog(None, 'Confirma a eliminação dos dados?',
                                   'Prestes a eliminar definitivamente!',
                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                prossegueEliminacao = True

            if prossegueEliminacao:
                self.corte.delete(str(self.idCorte))


                self.limpaElementos3()

                self.encheGrid3()


    def habilitaNovo3(self, event):
        if self.focoem == 0 or self.focoem == 3:
            if len(self.txtSelecao3.GetValue()) > 0:
                self.limpaElementos3()

                self.cbUva.Enable()
                self.txtPercentual.Enable()

                self.botaoSalva3.Enable()

                self.insert = True

                self.focoem = 3


    def cancelaOperacao3(self, event):
        self.limpaElementos3()


def main():
    app = wx.App()
    frmVinhoProdutor = FrmVinhoProdutor()
    app.MainLoop()


if __name__ == '__main__':
    main()

