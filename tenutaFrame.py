# coding: utf-8
from tenuta import *
from pais import *
from pacotesMG.conectaDataBaseMG import *

from pacotesMG.wxComponetesMG import FrameMG
import wx
import wx.grid as gridlib


class FrmTenuta(FrameMG):
    insert = False
    caminho = '..\\pacotesMG\\icones\\'

    def __init__(self):
        self.tenuta = Tenuta()
        self.pais = Pais()

        super(FrmTenuta, self).__init__(None, 'Cadastro de vinícolas', 1200, 700, 600)

        self.criaComponentes()

    def criaComponentes(self):
        X = self.posx(1)
        Y = self.posy(0)
        tamX = self.larguraEmPx(80)
        tamY = self.alturaEmPx(15)
        
        x0 = 83

        self.grid = wx.ListCtrl(self.painel, pos=(X, Y), size=(tamX, tamY),
                                style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.BORDER_SUNKEN)
        
        label01, self.txtId = self.criaCaixaDeTexto(self.painel, 0, 10, 40, 'ID', 0, xcol=x0+1, tamanho = 6)
        label02, self.txtNomeTenuta = self.criaCaixaDeTexto(self.painel, 0, 80, 520, 'Nome da vinícola',
                                                             self.tenuta.sqlBuscaTamanho('nometenuta'), xcol = x0 + 11, tamanho = 70)

        label03, self.txtPaisChave = self.criaCaixaDeTexto(self.painel, 1, 10, 250, 'Pesquisa do país',
                                                             self.pais.sqlBuscaTamanho('nomepais'), xcol = x0 + 1, tamanho = 20)

        iconePesquisa = wx.Bitmap(self.caminho + 'search32.ico')
        self.botaoPesquisa = wx.BitmapButton(self.painel, bitmap=iconePesquisa,
            pos=(self.posx(x0 + 24), self.posy(1)))
        self.botaoPesquisa.Bind(wx.EVT_BUTTON, self.pesquisaPais)

        label04, self.txtIdPais = self.criaCaixaDeTexto(self.painel, 1, 340, 40, 'ID', 0, xcol = x0 + 32, tamanho = 6)
        label05, self.txtNomePais = self.criaCaixaDeTexto(self.painel, 1, 400, 200, 'Nome do país', 0, xcol = x0 + 42, tamanho = 39)

        label06, self.txtRegiao = self.criaCaixaDeTexto(self.painel, 2, -1, -1, 'Região',
                                                          self.tenuta.sqlBuscaTamanho('regiao'),
                                                          xcol = x0 + 1, tamanho = 30)
        label07, self.txtCidade = self.criaCaixaDeTexto(self.painel, 2, -1, -1, 'Cidade',
                                                          self.tenuta.sqlBuscaTamanho('cidade'),
                                                          xcol = x0 + 35, tamanho = 38)
        label08, self.txtEstado = self.criaCaixaDeTexto(self.painel, 2, -1, -1, 'Estado',
                                                          self.tenuta.sqlBuscaTamanho('estado'),
                                                          xcol = x0 + 77, tamanho = 4)

        label09, self.txtEndereco1 = self.criaCaixaDeTexto(self.painel, 3, -1, -1, 'Endereço 1',
                                                          self.tenuta.sqlBuscaTamanho('endereco1'),
                                                          xcol = x0 + 1, tamanho = 80)
        label10, self.txtEndereco2 = self.criaCaixaDeTexto(self.painel, 4, -1, -1, 'Endereço 2',
                                                          self.tenuta.sqlBuscaTamanho('endereco2'),
                                                          xcol = x0 + 1, tamanho = 80)
        label11, self.txtEndereco3 = self.criaCaixaDeTexto(self.painel, 5, -1, -1, 'Endereço 3',
                                                          self.tenuta.sqlBuscaTamanho('endereco3'),
                                                          xcol = x0 + 1, tamanho = 80)

        label12, self.txtCep = self.criaCaixaDeTexto(self.painel, 6, -1, -1, 'CEP',
                                                          self.tenuta.sqlBuscaTamanho('cep'),
                                                          xcol = x0 + 1, tamanho = 10)
        label13, self.txtTelefone = self.criaCaixaDeTexto(self.painel, 6, -1, -1, 'Telefone',
                                                          self.tenuta.sqlBuscaTamanho('telefone'),
                                                          xcol = x0 + 35, tamanho = 25)

        label14, self.txtEmail = self.criaCaixaDeTexto(self.painel, 7, -1, -1, 'E-mail',
                                                          self.tenuta.sqlBuscaTamanho('email'),
                                                          xcol = x0 + 1, tamanho = 80)

        label15, self.txtContato = self.criaCaixaDeTexto(self.painel, 8, -1, -1, 'Contato',
                                                          self.tenuta.sqlBuscaTamanho('contato'),
                                                          xcol = x0 + 1, tamanho = 80)

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
        t.idtenuta, t.nometenuta, t.idpais, p.nomepais, t.regiao, t.cidade, t.estado,
        t.endereco1, t.endereco2, t.endereco3, t.cep, t.telefone, t.email, t.contato

        '''
        self.grid.ClearAll()
        self.grid.InsertColumn(0, 'id', width=self.larguraEmPx(4))
        self.grid.InsertColumn(1, 'Nome da tenuta', width=self.larguraEmPx(40))
        self.grid.InsertColumn(2, 'Pais de origem', width=self.larguraEmPx(20))
        self.grid.InsertColumn(3, 'Região', width=self.larguraEmPx(30))

        self.lista = self.tenuta.getAll()

        for row in self.lista:
            self.grid.Append([row[0], row[1], row[3], row[4]])

    def limpaElementos(self):
        self.txtId.Clear()
        self.txtNomeTenuta.Clear()
        self.txtPaisChave.Clear()
        self.txtIdPais.Clear()
        self.txtNomePais.Clear()
        self.txtRegiao.Clear()
        self.txtCidade.Clear()
        self.txtEstado.Clear()
        self.txtEndereco1.Clear()
        self.txtEndereco2.Clear()
        self.txtEndereco3.Clear()
        self.txtCep.Clear()
        self.txtTelefone.Clear()
        self.txtEmail.Clear()
        self.txtContato.Clear()

        self.txtId.Disable()
        self.txtNomeTenuta.Disable()
        self.txtPaisChave.Disable()
        self.txtIdPais.Disable()
        self.txtNomePais.Disable()
        self.txtRegiao.Disable()
        self.txtCidade.Disable()
        self.txtEstado.Disable()
        self.txtEndereco1.Disable()
        self.txtEndereco2.Disable()
        self.txtEndereco3.Disable()
        self.txtCep.Disable()
        self.txtTelefone.Disable()
        self.txtEmail.Disable()
        self.txtContato.Disable()

        self.botaoSalva.Disable()
        self.botaoDelete.Disable()
        self.botaoPesquisa.Disable()

    def selecionaLinha(self, event):
        '''
        t.idtenuta, t.nometenuta, t.idpais, p.nomepais, t.regiao, t.cidade, t.estado,
        t.endereco1, t.endereco2, t.endereco3, t.cep, t.telefone, t.email, t.contato

        '''
        item = self.grid.GetFocusedItem()

        idTenuta = self.grid.GetItemText(item, 0)

        if idTenuta.isdigit():
            lista = self.tenuta.buscaTenuta(idTenuta)

            self.txtPaisChave.Clear()
            self.txtId.SetValue(str(lista[0]))
            self.txtNomeTenuta.SetValue(lista[1])
            self.txtIdPais.SetValue(str(lista[2]))
            self.txtNomePais.SetValue(lista[3])

            self.txtRegiao.SetValue(lista[4])
            self.txtCidade.SetValue(lista[5])
            self.txtEstado.SetValue(lista[6])
            self.txtEndereco1.SetValue(lista[7])
            self.txtEndereco2.SetValue(lista[8])
            self.txtEndereco3.SetValue(lista[9])
            self.txtCep.SetValue(lista[10])
            self.txtTelefone.SetValue(lista[11])
            self.txtEmail.SetValue(lista[12])
            self.txtContato.SetValue(lista[13])

            self.txtNomeTenuta.Enable()
            self.txtPaisChave.Enable()
            self.txtRegiao.Enable()
            self.txtCidade.Enable()
            self.txtEstado.Enable()
            self.txtEndereco1.Enable()
            self.txtEndereco2.Enable()
            self.txtEndereco3.Enable()
            self.txtCep.Enable()
            self.txtTelefone.Enable()
            self.txtEmail.Enable()
            self.txtContato.Enable()

            self.botaoSalva.Enable()
            self.botaoDelete.Enable()
            self.botaoPesquisa.Enable()

    def salvaElemento(self, event):
        self.tenuta.setnomeTenuta(self.txtNomeTenuta.GetValue())
        self.tenuta.setidPais(str(self.txtIdPais.GetValue()))
        self.tenuta.setregiao((self.txtRegiao.GetValue()))
        self.tenuta.setcidade(self.txtCidade.GetValue())
        self.tenuta.setestado(self.txtEstado.GetValue())
        self.tenuta.setendereco1(self.txtEndereco1.GetValue())
        self.tenuta.setendereco2(self.txtEndereco2.GetValue())
        self.tenuta.setendereco3(self.txtEndereco3.GetValue())
        self.tenuta.setcep(self.txtCep.GetValue())
        self.tenuta.settelefone(self.txtTelefone.GetValue())
        self.tenuta.setemail(self.txtEmail.GetValue())
        self.tenuta.setcontato(self.txtContato.GetValue())

        if self.insert:
            self.tenuta.insere()
            self.insert = False
        else:
            self.tenuta.update(str(self.txtId.GetValue()))

        self.limpaElementos()

        self.encheGrid()

    def deletaElemento(self, event):
        super(FrmTenuta, self).deletaElemento(event)
        if self.prossegueEliminacao:
            self.tenuta.delete(str(self.txtId.GetValue()))

            self.limpaElementos()

            self.encheGrid()

    def habilitaNovo(self, event):
        self.limpaElementos()

        self.txtNomeTenuta.Enable()
        self.txtPaisChave.Enable()
        self.txtRegiao.Enable()
        self.txtCidade.Enable()
        self.txtEstado.Enable()
        self.txtEndereco1.Enable()
        self.txtEndereco2.Enable()
        self.txtEndereco3.Enable()
        self.txtCep.Enable()
        self.txtTelefone.Enable()
        self.txtEmail.Enable()
        self.txtContato.Enable()

        self.botaoSalva.Enable()
        self.botaoPesquisa.Enable()

        self.insert = True

    def cancelaOperacao(self, event):
        self.limpaElementos()

def main():
    app = wx.App()
    frmTenuta = FrmTenuta()
    app.MainLoop()


if __name__ == '__main__':
    main()

