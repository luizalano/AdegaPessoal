# coding: utf-8
import wx
import sys
from paisFrame import *
from apelacaoFrame import *
from apelacaoSafraFrame import *
from vinhoProdutorFrame import *
from garrafaFrame import *
from uvaFrame import *
from tenutaFrame import *
from tipoVinhoFrame import *



class Menu(wx.Frame):
    # Extendendo a classe Frame

    ID_EXIT = 110
    '''
    Número aleatório para poder usar em MAC
    Por padrão o Mac não aceita fechar o aplicativo na opção quit, apenas no menu padrão
    Mudando o padrão da saída, força a aparecer também no Mac a opção de saída
    '''

    def __init__(self):
        estilo = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)

        super(Menu, self).__init__(None, -1, title='Adega ', size=(800, 600), style=estilo)

        self.interfaceBasica()

    def interfaceBasica(self):
        self.painel = wx.Panel(self, pos=(0, 0), size=(800, 600))

        bitmap = wx.Bitmap('.\\imagens\\Adega1.jpg')
        bitmap = self.redimensiona(bitmap, 800, 600)
        control = wx.StaticBitmap(self, -1, bitmap)
        control.SetPosition((0, 0))


        self.CreateStatusBar()
        self.SetStatusText('Barra de status')

        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu2 = wx.Menu()
        menuItemPais = menu1.Append(0, '&Pais', 'Cadastro de países')
        self.Bind(wx.EVT_MENU, self.chamaPais, menuItemPais)
        menuItemApelacao = menu1.Append(1, '&Apelação', 'Cadastro de apelações')
        self.Bind(wx.EVT_MENU, self.chamaApelacao, menuItemApelacao)
        menuItemGarrafa = menu1.Append(2, '&Garrafa', 'Cadastro de garrafas')
        self.Bind(wx.EVT_MENU, self.chamaGarrafa, menuItemGarrafa)
        menuItemTipoVinho = menu1.Append(3, '&Tipo de vinho', 'Cadastro de tipos de vinhos')
        self.Bind(wx.EVT_MENU, self.chamaTipoVinho, menuItemTipoVinho)
        menuSeparador1 = menu1.Append(wx.ID_SEPARATOR, '', '',)

        menuItemSaida = menu1.Append(self.ID_EXIT, '&Finalizar', 'Termina a execução da aplicação')

        menuBar.Append(menu1, '&Tabelas e saída')

        menuBar.Append(menu2, '&Cadastros')
        menuItemApelacaoSafra = menu2.Append(100, '&Safra por apelação', 'Cadastro de safras por apelações')
        self.Bind(wx.EVT_MENU, self.chamaApelacaoSafra, menuItemApelacaoSafra)
        menuItemProdutor = menu2.Append(101, '&Produtor', 'Cadastro de produtores')
        self.Bind(wx.EVT_MENU, self.chamaProdutor, menuItemProdutor)
        menuItemProdutoProdutor = menu2.Append(102, '&Vinhos por produtor', 'Cadastro de vinhos por produtores')
        self.Bind(wx.EVT_MENU, self.chamaProdutoProdutor, menuItemProdutoProdutor)

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.encerraAplicacao, menuItemSaida)

        self.Centre()  # Centraliza o componente
        self.Show()

    def redimensiona(self, bitmap, width, height):
        #image = wx.ImageFromBitmap(bitmap)
        image = wx.Bitmap.ConvertToImage(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.Bitmap(image)
        return result

    def encerraAplicacao(self, e):
        self.Close(force=False)

    def chamaPais(self, event):
        app1 = wx.App()
        frm = FrmPais()
        app1.MainLoop()
        frm.Destroy()
        app1.Destroy()

    def chamaApelacao(self, event):
        app1 = wx.App()
        frm = FrmPais()
        app1.MainLoop()
        frm.Destroy()
        app1.Destroy()

    def chamaGarrafa(self, event):
        app1 = wx.App()
        frm = FrmGarrafa()
        app1.MainLoop()
        frm.Destroy()
        app1.Destroy()

    def chamaTipoVinho(self, event):
        app1 = wx.App()
        frm = FrmTipoVinho()
        app1.MainLoop()
        frm.Destroy()
        app1.Destroy()

    def chamaApelacaoSafra(self, event):
        app1 = wx.App()
        frm = FrmApelacaoSafra()
        app1.MainLoop()
        frm.Destroy()
        app1.Destroy()

    def chamaProdutor(self, event):
        app1 = wx.App()
        frm = FrmTenuta()
        app1.MainLoop()
        frm.Destroy()
        app1.Destroy()

    def chamaProdutoProdutor(self, event):
        app1 = wx.App()
        frm = FrmVinhoProdutor()
        app1.MainLoop()
        frm.Destroy()
        app1.Destroy()


def main():
    app = wx.App()
    menu = Menu()
    app.MainLoop()


if __name__ == '__main__':
    main()

