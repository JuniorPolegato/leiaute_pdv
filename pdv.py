#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gdk
import re
import locale

class PDV(object):
    def __init__(self):
        # Objeto para carregar a "user interface" (ui) feita no Glade
        self.ui = Gtk.Builder()

        self.ui.add_from_file('pdv.ui')

        # Conectar as funções da ui com as da classe atual
        self.ui.connect_signals(self)

        # Ponteiro para widgets de uso frequente
        self.lista_itens = self.ui.get_object('ls_itens')
        self.descricao = self.ui.get_object('lb_descricao')
        self.cod_barras = self.ui.get_object('ed_cod_barras')
        self.itens = self.ui.get_object('lb_itens')
        self.total = self.ui.get_object('lb_total')

    def ao_liberar_tecla(self, editor, evento):
        codigo = re.sub('[^0-9]', '', self.cod_barras.get_text())
        if (len(codigo) == 13 # EAN 13 para produtos
                or evento.keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter)):
            # Consultar o produto no BD (vou acochambrar) e adicionar
            descricao = 'Produto %s' % codigo
            valor = locale.format("%.2f", float(codigo[:6]) / 100, True)
            self.lista_itens.append((codigo, descricao, valor))
            # Calcular o totais
            total = sum(map(locale.atof, zip(*self.lista_itens)[2]))
            itens = len(self.lista_itens)
            # Preencher grade e outros widgets
            self.descricao.set_text(descricao)
            self.itens.set_text(locale.format("%i", itens, True))
            self.total.set_text(locale.format("%.2f", total, True))
            self.cod_barras.set_text('')
        else:
            self.cod_barras.set_text(codigo)

    def ao_sair(self, editor, *evento):
        Gtk.main_quit()

if __name__ == "__main__":

    locale.setlocale(locale.LC_ALL, '')

    provider = Gtk.CssProvider()
    provider.load_from_data('GtkWindow {'
                            '   background-image: url("pdv.jpg");'
                            '}'
                            '.entry {'
                            '   background: transparent;'
                                'color: white;'
                                'font-weight: bold;'
                                'font-size: 16px;'
                            '}')
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    pdv = PDV()
    Gtk.main()
