# Embedded file name: /opt/openerp/server/openerp/addons/icsc_lt_baocao/icsc_lt_baocao.py
from openerp.osv import osv, fields
from datetime import date
import datetime
import time
from datetime import timedelta
date1 = datetime.datetime.now() + datetime.timedelta(hours=7)

class icsc_year(osv.osv):
    _name = 'icsc.year'
    _columns = {'name': fields.char('N\xc4\x83m', size=4, required=True)}


icsc_year()

class icsc_month(osv.osv):
    _name = 'icsc.month'
    _columns = {'name': fields.char('Th\xc3\xa1ng', size=2, required=True)}


icsc_month()

class icsc_baocao_hangngay(osv.osv):
    _name = 'icsc.baocao.hangngay'
    _order = 'id desc'
    _columns = {'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'partner_id': fields.many2one('res.partner', 'Kh\xc3\xa1ch h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'nhom_kh': fields.many2one('res.partner.category', 'Nh\xc3\xb3m kh\xc3\xa1ch h\xc3\xa0ng'),
     'dv_thuchien': fields.many2one('sale.shop', '\xc4\x90V th\xe1\xbb\xb1c hi\xe1\xbb\x87n')}
    _defaults = {'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today}


icsc_baocao_hangngay()

class icsc_baocao_lenh_tonghop(osv.osv):
    _name = 'icsc.baocao.lenh.tonghop'
    _order = 'id desc'
    _columns = {'dv_thuchien': fields.many2one('sale.shop', '\xc4\x90V th\xe1\xbb\xb1c hi\xe1\xbb\x87n'),
     'partner_id': fields.many2one('res.partner', 'Kh\xc3\xa1ch h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'nhom_kh': fields.many2one('res.partner.category', 'Nh\xc3\xb3m kh\xc3\xa1ch h\xc3\xa0ng'),
     'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'kho_gui': fields.selection([('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3'),
                 ('cong_ty', 'Kho c\xc3\xb4ng ty'),
                 ('kho_ngoai_tt', 'Kho t\xe1\xba\xadp trung'),
                 ('kho_ngoai', 'Kho \xc4\x91\xe1\xba\xa1i l\xc3\xbd')], 'Kho g\xe1\xbb\xadi \xc4\x91\xe1\xba\xbfn', required=True)}
    _defaults = {'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today,
     'kho_gui': 'all'}


icsc_baocao_lenh_tonghop()

class icsc_baocao_tonlenh_mathang_khachhang(osv.osv):
    _name = 'icsc.baocao.tonlenh.mathang.khachhang'
    _columns = {'dv_thuchien': fields.many2one('sale.shop', '\xc4\x90v th\xe1\xbb\xb1c hi\xe1\xbb\x87n'),
     'partner_id': fields.many2one('res.partner', 'Kh\xc3\xa1ch h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'nhom_kh': fields.many2one('res.partner.category', 'Nh\xc3\xb3m kh\xc3\xa1ch h\xc3\xa0ng'),
     'date': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'kho_gui': fields.selection([('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3'),
                 ('cong_ty', 'Kho c\xc3\xb4ng ty'),
                 ('kho_ngoai_tt', 'Kho t\xe1\xba\xadp trung'),
                 ('kho_ngoai', 'Kho \xc4\x91\xe1\xba\xa1i l\xc3\xbd')], 'Kho g\xe1\xbb\xadi \xc4\x91\xe1\xba\xbfn', required=True)}
    _defaults = {'date': fields.date.context_today,
     'kho_gui': 'all'}


icsc_baocao_tonlenh_mathang_khachhang()

class icsc_baocao_sokelenh_guikho(osv.osv):
    _name = 'icsc.baocao.sokelenh.guikho'
    _columns = {'partner_id': fields.many2one('res.partner', 'Kh\xc3\xa1ch h\xc3\xa0ng', domain=[('customer', '=', True)], required=False),
     'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'hopdong': fields.many2one('icsc.hopdong.banhang', 'H\xe1\xbb\xa3p \xc4\x91\xe1\xbb\x93ng', required=True),
     'loai_hd': fields.many2one('icsc.hopdong.banhang.loai', 'H\xe1\xbb\xa3p \xc4\x91\xe1\xbb\x93ng')}
    _defaults = {'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today}


icsc_baocao_sokelenh_guikho()

class icsc_baocao_tonghop_phatsinh_khachhang(osv.osv):
    _name = 'icsc.baocao.tonghop.phatsinh.khachhang'
    _columns = {'partner_id': fields.many2one('res.partner', 'Kh\xc3\xa1ch h\xc3\xa0ng', domain=[('customer', '=', True)], required=False),
     'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'lenh_xuat': fields.many2one('icsc.lt.loai.xuat.hang', 'Lo\xe1\xba\xa1i l\xe1\xbb\x87nh xu\xe1\xba\xa5t'),
     'nhom_kh': fields.many2one('res.partner.category', 'Nh\xc3\xb3m kh\xc3\xa1ch h\xc3\xa0ng'),
     'categ_id': fields.many2one('product.category', 'Lo\xe1\xba\xa1i s\xe1\xba\xa3n ph\xe1\xba\xa9m')}
    _defaults = {'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today,
     'categ_id': 1}


icsc_baocao_tonghop_phatsinh_khachhang()

class icsc_baocao_tonghop_phatsinh_sanpham(osv.osv):
    _name = 'icsc.baocao.tonghop.phatsinh.sanpham'
    _columns = {'categ_id': fields.many2one('product.category', 'Lo\xe1\xba\xa1i s\xe1\xba\xa3n ph\xe1\xba\xa9m'),
     'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True)}
    _defaults = {'categ_id': 1,
     'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today}


icsc_baocao_tonghop_phatsinh_sanpham()

class icsc_baocao_hopdong_banhang(osv.osv):
    _name = 'icsc.baocao.hopdong.banhang'
    _columns = {'loai_hop_dong': fields.many2one('icsc.hopdong.banhang.loai', 'Lo\xe1\xba\xa1i h\xe1\xbb\xa3p \xc4\x91\xe1\xbb\x93ng'),
     'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True)}
    _defaults = {'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today}


icsc_baocao_hopdong_banhang()
icsc_baocao_hopdong_banhang()

class icsc_baocao_ketqua_tieuthu(osv.osv):
    _name = 'icsc.baocao.ketqua.tieuthu'
    _order = 'id desc'
    _columns = {'categ_id': fields.many2one('product.category', 'Lo\xe1\xba\xa1i s\xe1\xba\xa3n ph\xe1\xba\xa9m', required=True),
     'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'dv_thuchien': fields.many2one('sale.shop', '\xc4\x90V th\xe1\xbb\xb1c hi\xe1\xbb\x87n'),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'categ_id': 1,
     'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_ketqua_tieuthu()

class icsc_baocao_banhang(osv.osv):
    _name = 'icsc.baocao.banhang'
    _columns = {'partner_id': fields.many2one('res.partner', 'Kh\xc3\xa1ch h\xc3\xa0ng', domain=[('customer', '=', True)], required=False),
     'categ_id': fields.many2one('product.category', 'Lo\xe1\xba\xa1i s\xe1\xba\xa3n ph\xe1\xba\xa9m'),
     'nhom_kh': fields.many2one('res.partner.category', 'Nh\xc3\xb3m kh\xc3\xa1ch h\xc3\xa0ng'),
     'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'dv_thuchien': fields.many2one('sale.shop', '\xc4\x90v th\xe1\xbb\xb1c hi\xe1\xbb\x87n')}
    _defaults = {'categ_id': 1,
     'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today}


icsc_baocao_banhang()
icsc_baocao_banhang()

class icsc_baocao_danhgia_tieuthu(osv.osv):
    _name = 'icsc.baocao.danhgia.tieuthu'
    _order = 'id desc'
    _columns = {'tinh': fields.many2one('res.country.state', 'T\xe1\xbb\x89nh', domain=[('country_id', '=', 243)]),
     'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'dv_thuchien': fields.many2one('sale.shop', '\xc4\x90V th\xe1\xbb\xb1c hi\xe1\xbb\x87n'),
     'loai_hd': fields.many2one('icsc.hopdong.banhang.loai', 'Lo\xe1\xba\xa1i h\xe1\xbb\xa3p \xc4\x91\xe1\xbb\x93ng'),
     'partner_id': fields.many2one('res.partner', 'Kh\xc3\xa1ch h\xc3\xa0ng', domain=[('customer', '=', True)])}
    _defaults = {'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today}


icsc_baocao_danhgia_tieuthu()

class icsc_baocao_pxk_kiemvcnoibo(osv.osv):
    _name = 'icsc.baocao.pxk.kiemvcnoibo'
    _columns = {'ngay_bd_phieu': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', help='Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', required=True),
     'ngay_kt_phieu': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', help='Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', required=True),
     'tinh': fields.many2one('res.country.state', 'T\xe1\xbb\x89nh', domain=[('country_id', '=', 243)]),	 
     'categ': fields.many2one('product.category', 'Lo\xe1\xba\xa1i s\xe1\xba\xa3n ph\xe1\xba\xa9m'),
     'loai_xuat_hang': fields.many2one('icsc.lt.loai.xuat.hang', 'Lo\xe1\xba\xa1i xu\xe1\xba\xa5t h\xc3\xa0ng'),
     'partner_id': fields.many2one('res.partner', 'Kh\xc3\xa1ch h\xc3\xa0ng', domain=[('customer', '=', True)], required=False),
     'dv_thuchien': fields.many2one('sale.shop', '\xc4\x90v th\xe1\xbb\xb1c hi\xe1\xbb\x87n'),
     'lenh_xuat': fields.many2one('sale.order', 'L\xe1\xbb\x87nh xu\xe1\xba\xa5t'),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'categ': 1,
     'ngay_bd_phieu': fields.date.context_today,
     'ngay_kt_phieu': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_pxk_kiemvcnoibo()

class icsc_baocao_hoadon_banhang(osv.osv):
    _name = 'icsc.baocao.hoadon.banhang'
    _columns = {'loai_hoadon': fields.selection([('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3'), ('thongthuong', 'Th\xc3\xb4ng th\xc6\xb0\xe1\xbb\x9dng'), ('noibo', 'N\xe1\xbb\x99i b\xe1\xbb\x99')], 'Lo\xe1\xba\xa1i h\xc3\xb3a \xc4\x91\xc6\xa1n', required=True),
     'categ_id': fields.many2one('product.category', 'Lo\xe1\xba\xa1i s\xe1\xba\xa3n ph\xe1\xba\xa9m', required=True),
     'type_kho': fields.selection([('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3'),
                  ('kho_congty', 'Kho c\xc3\xb4ng ty'),
                  ('kho_taptrung', 'Kho t\xe1\xba\xadp trung'),
                  ('kho_daily', 'Kho \xc4\x91\xe1\xba\xa1i l\xc3\xbd')], 'Lo\xe1\xba\xa1i h\xc3\xacnh kho', required=True),
     'tungay': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', help='Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', required=True),
     'denngay': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', help='Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', required=True),
     'loai_xuat_hang': fields.many2one('icsc.lt.loai.xuat.hang', 'Lo\xe1\xba\xa1i xu\xe1\xba\xa5t h\xc3\xa0ng'),
     'partner_id': fields.many2one('res.partner', 'Kh\xc3\xa1ch h\xc3\xa0ng', domain=[('customer', '=', True)], required=False),
     'dv_thuchien': fields.many2one('sale.shop', '\xc4\x90v th\xe1\xbb\xb1c hi\xe1\xbb\x87n'),
     'nhom_kh': fields.many2one('res.partner.category', 'Nh\xc3\xb3m kh\xc3\xa1ch h\xc3\xa0ng'),
     'product_id': fields.many2one('product.product', 'S\xe1\xba\xa3n ph\xe1\xba\xa9m')}
    _defaults = {'loai_hoadon': 'all',
     'type_kho': 'all',
     'categ_id': 1,
     'tungay': fields.date.context_today,
     'denngay': fields.date.context_today}


icsc_baocao_hoadon_banhang()

class icsc_baocao_luongtieuthu(osv.osv):
    _name = 'icsc.baocao.luongtieuthu'
    _columns = {'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
	  
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'district': fields.many2one('res.country.district', 'Huy\xe1\xbb\x87n', required=False, domain="[('state_id','=',state)]"),
     'state': fields.many2one('res.country.state', 'T\xe1\xbb\x89nh', required=False),
     'nam': fields.char('N\xc4\x83m xu\xe1\xba\xa5t', required=True),
     'thang': fields.many2one('icsc.month', 'T\xe1\xbb\xab th\xc3\xa1ng', required=True),
     'thang2': fields.many2one('icsc.month', '\xc4\x90\xe1\xba\xbfn th\xc3\xa1ng', required=True)}
    _defaults = {'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today,
     'nam': datetime.date.today().year}


icsc_baocao_luongtieuthu()

class icsc_baocao_kehoach_phanbon(osv.osv):
    _name = 'icsc.baocao.kehoach.phanbon'
    _order = 'id desc'
    _columns = {'ngay': fields.date('Ch\xe1\xbb\x8dn ng\xc3\xa0y', required=True),
     'donvi_vc': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)]),
     'donvi_nh': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b nh\xe1\xba\xadn h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'ngay': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_kehoach_phanbon()

class icsc_baocao_kehoach_phanbon_canam(osv.osv):
    _name = 'icsc.baocao.kehoach.phanbon.canam'
    _order = 'id desc'
    _columns = {'denngay': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'loai_khvc': fields.selection([('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3'),
                   ('vat', 'VAT'),
                   ('gui_ban', 'G\xe1\xbb\xadi h\xc3\xa0ng c\xc3\xb3 \xc4\x91\xe1\xba\xa3m b\xe1\xba\xa3o'),
                   ('kho_tap_trung', 'G\xe1\xbb\xadi kho t\xe1\xba\xadp trung'),
                   ('kho_dai_ly', 'H\xc3\xa0ng nguy\xc3\xaan li\xe1\xbb\x87u gia c\xc3\xb4ng')], 'Lo\xe1\xba\xa1i KHVC', required=True),
     'donvi_vc': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)]),
     'donvi_nh': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b nh\xe1\xba\xadn h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'loai_khvc': 'all',
     'denngay': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_kehoach_phanbon_canam()

class icsc_baocao_ketquavc(osv.osv):
    _name = 'icsc.baocao.ketquavc'
    _order = 'id desc'
    _columns = {'name': fields.char('N\xc4\x83m', required=True),
     'donvi_vc': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)]),
     'donvi_nh': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b nh\xe1\xba\xadn h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'name': datetime.date.today().year,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_ketquavc()

class icsc_baocao_hopdong_vanchuyen(osv.osv):
    _name = 'icsc.baocao.hopdong.vanchuyen'
    _order = 'id desc'
    _columns = {'ngay_bd_hd': fields.date('Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u h\xe1\xbb\xa3p \xc4\x91\xe1\xbb\x93ng', required=True),
     'ngay_kt_hd': fields.date('Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac h\xe1\xbb\xa3p \xc4\x91\xe1\xbb\x93ng', required=True),
     'donvi_vc': fields.many2one('res.partner', 'Cty v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)]),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'ngay_bd_hd': fields.date.context_today,
     'ngay_kt_hd': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_hopdong_vanchuyen()

class icsc_baocao_hopdong_cuocvanchuyen(osv.osv):
    _name = 'icsc.baocao.hopdong.cuocvanchuyen'
    _order = 'id desc'
    _columns = {'ngay': fields.date('Ng\xc3\xa0y', required=True),
     'donvi_vc': fields.many2one('res.partner', 'Cty v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)], required=True),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'ngay': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_hopdong_vanchuyen()

class icsc_baocao_phieu_vanchuyen(osv.osv):
    _name = 'icsc.baocao.phieu.vanchuyen'
    _order = 'id desc'
    _columns = {'loai_phieu': fields.selection([('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3'), ('thongthuong', 'Th\xc3\xb4ng th\xc6\xb0\xe1\xbb\x9dng'), ('noibo', 'N\xe1\xbb\x99i b\xe1\xbb\x99')], 'Lo\xe1\xba\xa1i phi\xe1\xba\xbfu v\xe1\xba\xadn chuy\xe1\xbb\x83n', required=True),
     'ngay_bd_phieu': fields.date('Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', help='Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', required=False),
     'ngay_kt_phieu': fields.date('Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', help='Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', required=False),
     'donvi_vc': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)]),
     'donvi_nh': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b nh\xe1\xba\xadn h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'loai_khvc': fields.selection([('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3'),
                   ('vat', 'VAT'),
                   ('gui_ban', 'G\xe1\xbb\xadi h\xc3\xa0ng c\xc3\xb3 \xc4\x91\xe1\xba\xa3m b\xe1\xba\xa3o'),
                   ('kho_tap_trung', 'G\xe1\xbb\xadi kho t\xe1\xba\xadp trung'),
                   ('kho_dai_ly', 'H\xc3\xa0ng nguy\xc3\xaan li\xe1\xbb\x87u gia c\xc3\xb4ng')], 'Lo\xe1\xba\xa1i KHVC', required=True),
     'dv_thuchien': fields.many2one('sale.shop', '\xc4\x90v th\xe1\xbb\xb1c hi\xe1\xbb\x87n'),
     'kho_xuat': fields.many2one('res.partner', 'Kho xu\xe1\xba\xa5t', domain=['|',
                  ('is_trungchuyen', '=', True),
                  ('kho', '=', True),
                  ('is_diadiem', '!=', True)]),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'loai_phieu': 'all',
     'loai_khvc': 'all',
     'ngay_bd_phieu': fields.date.context_today,
     'ngay_kt_phieu': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_phieu_vanchuyen()

class icsc_baocao_phieu_vanchuyen_thuybo(osv.osv):
    _name = 'icsc.baocao.phieu.vanchuyen.thuybo'
    _order = 'id desc'
    _columns = {'loai_khvc': fields.selection([('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3'),
                   ('vat', 'VAT'),
                   ('gui_ban', 'G\xe1\xbb\xadi h\xc3\xa0ng c\xc3\xb3 \xc4\x91\xe1\xba\xa3m b\xe1\xba\xa3o'),
                   ('kho_tap_trung', 'G\xe1\xbb\xadi kho t\xe1\xba\xadp trung'),
                   ('kho_dai_ly', 'H\xc3\xa0ng nguy\xc3\xaan li\xe1\xbb\x87u gia c\xc3\xb4ng')], 'Lo\xe1\xba\xa1i KHVC', required=True),
     'ngay_bd_phieu': fields.date('Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', help='Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', required=False),
     'ngay_kt_phieu': fields.date('Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', help='Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', required=False),
     'donvi_vc': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)]),
     'donvi_nh': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b nh\xe1\xba\xadn h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'dv_thuchien': fields.many2one('sale.shop', '\xc4\x90v th\xe1\xbb\xb1c hi\xe1\xbb\x87n'),
     'state_id': fields.many2one('res.country.state', 'Khu v\xe1\xbb\xb1c nh\xe1\xba\xadp'),
     'diachi_giao': fields.many2one('res.partner', '\xc4\x90\xe1\xbb\x8ba ch\xe1\xbb\x89 giao', domain=[('is_diadiem', '=', True), ('active', '=', True)]),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'loai_khvc': 'all',
     'ngay_bd_phieu': fields.date.context_today,
     'ngay_kt_phieu': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_phieu_vanchuyen_thuybo()

class icsc_baocao_kho(osv.osv):
    _name = 'icsc.baocao.kho'
    _order = 'id desc'
    _columns = {'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'chang_khvc': fields.selection([('chang_1', 'Ch\xe1\xba\xb7ng 1 & Kh\xc3\xb4ng trung chuy\xe1\xbb\x83n'), ('chang_2', 'Ch\xe1\xba\xb7ng 2')], 'Ch\xe1\xba\xb7ng KHVC', required=True),
     'loai_khvc': fields.selection([('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3'),
                   ('vat', 'VAT'),
                   ('gui_ban', 'G\xe1\xbb\xadi h\xc3\xa0ng c\xc3\xb3 \xc4\x91\xe1\xba\xa3m b\xe1\xba\xa3o'),
                   ('kho_tap_trung', 'G\xe1\xbb\xadi kho t\xe1\xba\xadp trung'),
                   ('kho_dai_ly', 'H\xc3\xa0ng nguy\xc3\xaan li\xe1\xbb\x87u gia c\xc3\xb4ng')], 'Lo\xe1\xba\xa1i KHVC', required=True),
     'donvi_vc': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)]),
     'donvi_nh': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b nh\xe1\xba\xadn h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'loai_khvc': 'all',
     'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_kho()

class icsc_baocao_tonghop_vanchuyen(osv.osv):
    _name = 'icsc.baocao.tonghop.vanchuyen'
    _order = 'id desc'
    _columns = {'ngay_bd_phieu': fields.date('Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', help='Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', required=True),
     'ngay_kt_phieu': fields.date('Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', help='Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', required=True),
     'donvi_vc': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)]),
     'donvi_nh': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b nh\xe1\xba\xadn h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'loai_khvc': fields.selection([('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3'),
                   ('vat', 'VAT'),
                   ('gui_ban', 'G\xe1\xbb\xadi h\xc3\xa0ng c\xc3\xb3 \xc4\x91\xe1\xba\xa3m b\xe1\xba\xa3o'),
                   ('kho_tap_trung', 'G\xe1\xbb\xadi kho t\xe1\xba\xadp trung'),
                   ('kho_dai_ly', 'H\xc3\xa0ng nguy\xc3\xaan li\xe1\xbb\x87u gia c\xc3\xb4ng')], 'Lo\xe1\xba\xa1i KHVC', required=True),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'loai_khvc': 'all',
     'ngay_bd_phieu': fields.date.context_today,
     'ngay_kt_phieu': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_tonghop_vanchuyen()

class icsc_baocao_khoiluong_giaonhan(osv.osv):
    _name = 'icsc.baocao.khoiluong.giaonhan'
    _order = 'id desc'
    _columns = {'dv_vanchuyen': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)], required=True),
     'ngay_bd_phieu': fields.date('Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', help='T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt_phieu': fields.date('Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', help='\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'lan_bc': fields.char('L\xe1\xba\xa7n b\xc3\xa1o c\xc3\xa1o', required=True),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'ngay_bd_phieu': fields.date.context_today,
     'ngay_kt_phieu': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_khoiluong_giaonhan()

class icsc_baocao_khoiluong_tiencuoc_giaonhan(osv.osv):
    _name = 'icsc.baocao.khoiluong.tiencuoc.giaonhan'
    _order = 'id desc'
    _columns = {'dv_vanchuyen': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)]),
     'name': fields.char('N\xc4\x83m', required=True),
     'date': fields.date('Ng\xc3\xa0y'),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'name': datetime.date.today().year,
     'date': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_khoiluong_tiencuoc_giaonhan()

class icsc_baocao_denghithanhtoan(osv.osv):
    _name = 'icsc.baocao.denghithanhtoan'
    _order = 'id desc'
    _columns = {'ngay_bd_phieu': fields.date('Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', help='Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', required=True),
     'ngay_kt_phieu': fields.date('Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', help='Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', required=True),
     'donvi_vc': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)]),
     'donvi_nh': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b nh\xe1\xba\xadn h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'ngay_bd_phieu': fields.date.context_today,
     'ngay_kt_phieu': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_denghithanhtoan()

class icsc_thanhtoan_vanchuyen(osv.osv):
    _name = 'icsc.thanhtoan.vanchuyen'
    _order = 'id desc'
    _columns = {'dv_vanchuyen': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)], required=True),
     'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'chitiet_ids': fields.one2many('icsc.thanhtoan.vanchuyen.chitiet', 'phieu_id', 'Chi ti\xe1\xba\xbft'),
     'name': fields.char('M\xc3\xb4 t\xe1\xba\xa3'),
     'user_id': fields.many2one('res.users', 'Ng\xc6\xb0\xe1\xbb\x9di c\xe1\xba\xadp nh\xe1\xba\xadt')}
    _defaults = {'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today}

    def _check_category(self, cr, uid, orders_line_list, category_id):
        if len(orders_line_list) > 0:
            for line_id in orders_line_list:
                orderline = self.pool.get('icsc.thanhtoan.vanchuyen.chitiet').browse(cr, uid, line_id)
                prod_id = orderline.category_id.id
                if prod_id == category_id:
                    return line_id

        return False

    def merge_move_line(self, cr, uid, order_id, context = None):
        picking_obj = self.browse(cr, uid, order_id, context)
        if picking_obj:
            move_lines = picking_obj.chitiet_ids
            orders_line_list = []
            for line in move_lines:
                if line.category_id:
                    category_id = line.category_id.id
                    product_qty2 = line.so_phieu
                    line_get = self._check_category(cr, uid, orders_line_list, category_id)
                    if line_get:
                        move1 = self.pool.get('icsc.thanhtoan.vanchuyen.chitiet').browse(cr, uid, line_get)
                        product_qty1 = move1.so_phieu
                        self.pool.get('icsc.thanhtoan.vanchuyen.chitiet').write(cr, uid, line_get, {'so_phieu': product_qty1 + product_qty2})
                        query = 'delete from icsc_thanhtoan_vanchuyen_chitiet where id=%s'
                        cr.execute(query, (line.id,))
                    else:
                        orders_line_list.append(line.id)

        return True

    def action_load_data(self, cr, uid, ids, context = None):
        chitiet_pool = self.pool.get('icsc.thanhtoan.vanchuyen.chitiet')
        pvc_id = []
        pvc_id_tt = []
        for data in self.browse(cr, uid, ids, context=None):
            cr.execute('delete from icsc_thanhtoan_vanchuyen_chitiet where phieu_id=%s' % data.id)
            dv_vanchuyen = data.dv_vanchuyen.id
            ngay_bd = data.ngay_bd
            ngay_kt = data.ngay_kt
            query = "\n            select id from\n            (\n                select distinct pc.id as id, \n                sum(case when COALESCE(pvc.tung_phan,FALSE)=true then ct.kl_dangvc_dukien else ct.kl_vc end) as slps\n                from icsc_phieu_vanchuyen pvc\n                left join icsc_phieu_vanchuyen_chitiet ct on ct.phieu_id = pvc.id\n                left join product_product p on ct.product_id = p.id\n                left join product_template pt on p.product_tmpl_id = pt.id\n                left join product_category pc on pt.categ_id = pc.id\n                left join res_partner rp on rp.id = pvc.congty_vc\n                where pvc.state not in ('draft','cancel') and ct.state not in ('draft','cancel')\n                and pvc.ngay_vc between '%s'::date and '%s'::date and rp.id = %s\n                group by pc.id     \n            ) a order by slps desc       \n            " % (ngay_bd, ngay_kt, dv_vanchuyen)
            cr.execute(query)
            for line in cr.dictfetchall():
                nhomsp = False
                category_id = line['id']
                count = ps = tt = 0
                query_ps = "select pvc.id as pvc_id\n                             from icsc_phieu_vanchuyen pvc\n                             left join icsc_phieu_vanchuyen_chitiet ct on ct.phieu_id = pvc.id\n                             left join product_product p on ct.product_id = p.id\n                             left join product_template pt on p.product_tmpl_id = pt.id\n                             left join product_category pc on pt.categ_id = pc.id\n                             left join res_partner rp on rp.id = pvc.congty_vc\n                             where pvc.state not in ('draft','cancel') and ct.state not in ('draft','cancel')\n                             and pvc.ngay_vc between '%s'::date and '%s'::date and rp.id = %s and pc.id=%s                    \n                             " % (ngay_bd,
                 ngay_kt,
                 dv_vanchuyen,
                 category_id)
                cr.execute(query_ps)
                for item_ps in cr.dictfetchall():
                    if item_ps['pvc_id'] not in pvc_id:
                        ps += 1
                        pvc_id.append(item_ps['pvc_id'])

                query_tt = "select pvc.id as pvc_id\n                            from icsc_denghithanhtoan_vanchuyen dn\n                            left join icsc_denghithanhtoan_vanchuyen_chitiet dnt on dnt.phieu_id = dn.id\n                            left join icsc_phieu_vanchuyen pvc on pvc.id = dnt.so_phieu_vc\n                            left join icsc_phieu_vanchuyen_chitiet ct on ct.phieu_id = pvc.id\n                            left join product_product p on ct.product_id = p.id\n                            left join product_template pt on p.product_tmpl_id = pt.id\n                            left join product_category pc on pt.categ_id = pc.id\n                            left join res_partner rp on rp.id = pvc.congty_vc\n                            where dn.state not in ('draft','cancel') and pvc.state not in ('draft','cancel')\n                            and dn.thanhtoan_tungay >= '%s'::date and dn.thanhtoan_denngay <= '%s'::date\n                            and rp.id = %s and pc.id = %s                    \n                             " % (ngay_bd,
                 ngay_kt,
                 dv_vanchuyen,
                 category_id)
                cr.execute(query_tt)
                for item_tt in cr.dictfetchall():
                    if item_tt['pvc_id'] not in pvc_id_tt:
                        tt += 1
                        pvc_id_tt.append(item_tt['pvc_id'])

                vals = {'category_id': category_id,
                 'so_phieu_ps': ps,
                 'so_phieu_tt': tt,
                 'so_phieu_ton': ps - tt,
                 'phieu_id': data.id}
                chitiet_pool.create(cr, uid, vals, context=context)

        self.write(cr, uid, ids, {'user_id': uid}, context)
        return True

    def create(self, cr, uid, vals, context = None):
        new_id = super(icsc_thanhtoan_vanchuyen, self).create(cr, uid, vals, context)
        self.merge_move_line(cr, uid, new_id, context=None)
        self.action_load_data(cr, uid, [new_id], context=None)
        return new_id

    def write(self, cr, uid, ids, vals, context = None):
        res = super(icsc_thanhtoan_vanchuyen, self).write(cr, uid, ids, vals, context=context)
        if ids:
            try:
                if ids[0]:
                    self.merge_move_line(cr, uid, ids[0], context=context)
                    self.action_load_data(cr, uid, ids[0], context=context)
            except:
                return res

        return res

    _defaults = {'name': 'B\xe1\xba\xa2NG THANH TO\xc3\x81N V\xc3\x80 X\xc3\x81C NH\xe1\xba\xacN K.L\xc6\xaf\xe1\xbb\xa2NG, \xc4\x90.GI\xc3\x81 V\xc3\x80 C\xc6\xaf\xe1\xbb\x9aC PH\xc3\x8d V\xe1\xba\xacN CHUY\xe1\xbb\x82N H\xc3\x80NG H\xc3\x93A THU\xc3\x8a NGO\xc3\x80I'}


icsc_thanhtoan_vanchuyen()

class icsc_thanhtoan_vanchuyen_chitiet(osv.osv):
    _name = 'icsc.thanhtoan.vanchuyen.chitiet'
    _order = 'id desc'
    _columns = {'category_id': fields.many2one('product.category', 'Lo\xe1\xba\xa1i s\xe1\xba\xa3n ph\xe1\xba\xa9m', ondelete='cascade'),
     'so_phieu_ps': fields.integer('Phi\xe1\xba\xbfu ph\xc3\xa1t sinh'),
     'so_phieu_tt': fields.integer('Phi\xe1\xba\xbfu thanh to\xc3\xa1n'),
     'so_phieu_ton': fields.integer('Phi\xe1\xba\xbfu t\xe1\xbb\x93n'),
     'phieu_id': fields.many2one('icsc.thanhtoan.vanchuyen', 'Thanh to\xc3\xa1n', ondelete='cascade')}


icsc_thanhtoan_vanchuyen()

class icsc_tongtien_thanhtoan_vanchuyen(osv.osv):
    _name = 'icsc.tongtien.thanhtoan.vanchuyen'
    _order = 'id desc'
    _columns = {'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_tongtien_thanhtoan_vanchuyen()

class icsc_baocao_guihang_duongsat(osv.osv):
    _name = 'icsc.baocao.guihang.duongsat'
    _columns = {'donvi_vc': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)]),
     'donvi_nh': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b nh\xe1\xba\xadn h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'ngay_bd_phieu': fields.date('Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', help='T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt_phieu': fields.date('Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', help='\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'ngay_bd_phieu': fields.date.context_today,
     'ngay_kt_phieu': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_guihang_duongsat()

class icsc_baocao_kehoach_vanchuyen(osv.osv):
    _name = 'icsc.baocao.kehoach.vanchuyen'
    _order = 'id desc'
    _columns = {'ngay_bd_kh': fields.date('Ng\xc3\xa0y v\xe1\xba\xadn chuy\xe1\xbb\x83n', help='Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', required=True),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'ngay_bd_kh': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_kehoach_vanchuyen()

class icsc_baocao_uyquyen_gioithieu(osv.osv):
    _name = 'icsc.baocao.uyquyen.gioithieu'
    _order = 'id desc'
    _columns = {'nam': fields.char('N\xc4\x83m', required=True),
     'donvi_vc': fields.many2one('res.partner', 'Cty v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)], required=True),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'nam': datetime.date.today().year,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_uyquyen_gioithieu()

class icsc_baocao_tonghop_kho(osv.osv):
    _name = 'icsc.baocao.tonghop.kho'
    _order = 'id desc'
    _columns = {'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'loai_kho': fields.selection([('kho_daily', 'Kho \xc4\x91\xe1\xba\xa1i l\xc3\xbd'),
                  ('kho_congty', 'Kho c\xc3\xb4ng ty'),
                  ('kho_taptrung', 'Kho t\xe1\xba\xadp trung'),
                  ('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3')], 'Lo\xe1\xba\xa1i kho', required=True),
     'vi_tri': fields.many2one('stock.location', '\xc4\x90\xe1\xbb\x8ba di\xe1\xbb\x83m kh\xc3\xa1ch h\xc3\xa0ng', domain=[('active', '=', True)]),
     'partner_id': fields.many2one('res.partner', 'Kh\xc3\xa1ch h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'categ_id': fields.many2one('product.category', 'Lo\xe1\xba\xa1i s\xe1\xba\xa3n ph\xe1\xba\xa9m', required=True),
     'state_id': fields.many2one('res.country.state', 'T\xe1\xbb\x89nh')}
    _defaults = {'loai_kho': 'all',
     'categ_id': 1,
     'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today}


icsc_baocao_tonghop_kho()

class icsc_baocao_tonghop_phatsinh(osv.osv):
    _name = 'icsc.baocao.tonghop.phatsinh'
    _order = 'id desc'
    _columns = {'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True),
     'loai_kho': fields.selection([('kho_daily', 'Kho \xc4\x91\xe1\xba\xa1i l\xc3\xbd'),
                  ('kho_congty', 'Kho c\xc3\xb4ng ty'),
                  ('kho_taptrung', 'Kho t\xe1\xba\xadp trung'),
                  ('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3')], 'Lo\xe1\xba\xa1i kho', required=True),
     'partner_id': fields.many2one('res.partner', 'Kh\xc3\xa1ch h\xc3\xa0ng', domain=[('customer', '=', True)])}
    _defaults = {'loai_kho': 'all',
     'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today}


icsc_baocao_tonghop_phatsinh()

class icsc_baocao_xuatkho(osv.osv):
    _name = 'icsc.baocao.xuatkho'
    _order = 'id desc'
    _columns = {'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', required=True)}
    _defaults = {'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today}


icsc_baocao_xuatkho()

class icsc_baocao_xuatkho2(osv.osv):
    _name = 'icsc.baocao.xuatkho2'
    _order = 'id desc'
    _columns = {'nam': fields.char('N\xc4\x83m xu\xe1\xba\xa5t'),
     'thang': fields.many2one('icsc.month', 'Th\xc3\xa1ng xu\xe1\xba\xa5t'),
     'loai_kho': fields.selection([('kho_daily', 'Kho \xc4\x91\xe1\xba\xa1i l\xc3\xbd'),
                  ('kho_congty', 'Kho c\xc3\xb4ng ty'),
                  ('kho_taptrung', 'Kho t\xe1\xba\xadp trung'),
                  ('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3')], 'Lo\xe1\xba\xa1i kho', required=True)}
    _defaults = {'loai_kho': 'all',
     'nam': datetime.date.today().year}


icsc_baocao_xuatkho2()

class icsc_baocao_phatsinh_hanggui(osv.osv):
    _name = 'icsc.baocao.phatsinh.hanggui'
    _order = 'id desc'
    _columns = {'kho_xuat': fields.many2one('stock.location', 'Kho xu\xe1\xba\xa5t', required=True),
     'kho_nhap': fields.many2one('stock.location', 'Kho nh\xe1\xba\xadp', required=True, domain=[('location_id', '=', False)]),
     'khach_hang': fields.many2one('res.partner', 'Kh\xc3\xa1ch h\xc3\xa0ng', domain=[('customer', '=', True)], required=True),
     'nam': fields.char('N\xc4\x83m', required=True)}
    _defaults = {'nam': datetime.date.today().year}


icsc_baocao_phatsinh_hanggui()

class icsc_baocao_bienban_kiemke(osv.osv):
    _name = 'icsc.baocao.bienban.kiemke'
    _order = 'id desc'
    _columns = {'thang': fields.many2one('icsc.month', 'Th\xc3\xa1ng b\xc3\xa1o c\xc3\xa1o', required=True),
     'nam': fields.char('N\xc4\x83m', required=True),
     'vi_tri': fields.many2one('stock.location', 'Kho'),
     'partner_id': fields.many2one('res.partner', 'Kh\xc3\xa1ch h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'loai_kho': fields.selection([('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3'),
                  ('kho_daily', 'Kho \xc4\x91\xe1\xba\xa1i l\xc3\xbd'),
                  ('kho_congty', 'Kho c\xc3\xb4ng ty'),
                  ('kho_taptrung', 'Kho t\xe1\xba\xadp trung')], 'Lo\xe1\xba\xa1i kho')}
    _defaults = {'loai_kho': 'all',
     'nam': datetime.date.today().year}


icsc_baocao_bienban_kiemke()

class icsc_baocao_phieuthu_tienthu(osv.osv):
    _name = 'icsc.baocao.phieuthu.tienthu'
    _columns = {'ngay_batdau': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', help='Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', required=True),
     'ngay_kethuc': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', help='Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', required=True),
     'ngan_hang': fields.many2one('account.journal', 'Ng\xc3\xa2n h\xc3\xa0ng', required=True),
     'bo_phan': fields.selection([('ban_hang', 'B\xc3\xa1n h\xc3\xa0ng'), ('ke_toan', 'K\xe1\xba\xbf to\xc3\xa1n')], 'B\xe1\xbb\x99 ph\xe1\xba\xadn', required=True)}
    _defaults = {'ngay_batdau': fields.date.context_today,
     'ngay_batdau': fields.date.context_today}


icsc_baocao_phieuthu_tienthu()

class icsc_baocao_bangke_phieu(osv.osv):
    _name = 'icsc.baocao.bangke.phieu'
    _order = 'id desc'
    _columns = {'ngay_bd': fields.date('T\xe1\xbb\xab ng\xc3\xa0y', help='Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', required=True),
     'ngay_kt': fields.date('\xc4\x90\xe1\xba\xbfn ng\xc3\xa0y', help='Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', required=True),
     'dv_thuchien': fields.many2one('sale.shop', '\xc4\x90V th\xe1\xbb\xb1c hi\xe1\xbb\x87n'),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'ngay_bd': fields.date.context_today,
     'ngay_kt': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_phieuthu_tienthu()

class icsc_baocao_thongke_khoiluong(osv.osv):
    _name = 'icsc.baocao.thongke.khioiluong'
    _order = 'id desc'
    _columns = {'loai_khvc': fields.selection([('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3'),
                   ('vat', 'VAT'),
                   ('gui_ban', 'G\xe1\xbb\xadi h\xc3\xa0ng c\xc3\xb3 \xc4\x91\xe1\xba\xa3m b\xe1\xba\xa3o'),
                   ('kho_tap_trung', 'G\xe1\xbb\xadi kho t\xe1\xba\xadp trung trung'),
                   ('kho_dai_ly', 'H\xc3\xa0ng nguy\xc3\xaan li\xe1\xbb\x87u gia c\xc3\xb4ng')], 'Lo\xe1\xba\xa1i KHVC', required=True),
     'ngay_bd_phieu': fields.date('Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', help='Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', required=False),
     'ngay_kt_phieu': fields.date('Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', help='Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', required=False),
     'donvi_vc': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True)]),
     'donvi_nh': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b nh\xe1\xba\xadn h\xc3\xa0ng', domain=[('customer', '=', True)]),
     'dv_thuchien': fields.many2one('sale.shop', '\xc4\x90V th\xe1\xbb\xb1c hi\xe1\xbb\x87n'),
     'state_id': fields.many2one('res.country.state', 'Khu v\xe1\xbb\xb1c nh\xe1\xba\xadp'),
     'diachi_giao': fields.many2one('res.partner', '\xc4\x90\xe1\xbb\x8ba ch\xe1\xbb\x89 giao', domain=[('is_diadiem', '=', True), ('active', '=', True)]),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'loai_khvc': 'all',
     'ngay_bd_phieu': fields.date.context_today,
     'ngay_kt_phieu': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_thongke_khoiluong()

class icsc_baocao_kl_kvkn(osv.osv):
    _name = 'icsc.baocao.kl.kvkn'
    _order = 'id desc'
    _columns = {'loai_khvc': fields.selection([('all', 'T\xe1\xba\xa5t c\xe1\xba\xa3'),
                   ('vat', 'VAT'),
                   ('gui_ban', 'G\xe1\xbb\xadi h\xc3\xa0ng c\xc3\xb3 \xc4\x91\xe1\xba\xa3m b\xe1\xba\xa3o'),
                   ('kho_tap_trung', 'G\xe1\xbb\xadi kho t\xe1\xba\xadp trung'),
                   ('kho_dai_ly', 'H\xc3\xa0ng nguy\xc3\xaan li\xe1\xbb\x87u gia c\xc3\xb4ng')], 'Loo\xe1\xba\xa1i KHVC', required=True),
     'ngay_bd_phieu': fields.date('Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', help='Ng\xc3\xa0y b\xe1\xba\xaft \xc4\x91\xe1\xba\xa7u', required=False),
     'ngay_kt_phieu': fields.date('Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', help='Ng\xc3\xa0y k\xe1\xba\xbft th\xc3\xbac', required=False),
     'donvi_vc': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b v\xe1\xba\xadn chuy\xe1\xbb\x83n', domain=[('supplier', '=', True), ('active', '=', True)]),
     'donvi_nh': fields.many2one('res.partner', '\xc4\x90\xc6\xa1n v\xe1\xbb\x8b nh\xe1\xba\xadn h\xc3\xa0ng', domain=[('customer', '=', True), ('active', '=', True)]),
     'dv_thuchien': fields.many2one('sale.shop', '\xc4\x90V th\xe1\xbb\xb1c hi\xe1\xbb\x87n'),
     'state_id': fields.many2one('res.country.state', 'Khu v\xe1\xbb\xb1c nh\xe1\xba\xadp'),
     'diachi_giao': fields.many2one('res.partner', '\xc4\x90\xe1\xbb\x8ba ch\xe1\xbb\x89 giao', domain=[('is_diadiem', '=', True), ('active', '=', True)]),
     'tramkiemsoat': fields.many2one('res.country.tramkiemsoat', 'Tr\xe1\xba\xa1m ki\xe1\xbb\x83m so\xc3\xa1t'),
     'gio_bc': fields.datetime('Th\xe1\xbb\x9di gian xem b\xc3\xa1o c\xc3\xa1o', required=True, readonly=True)}
    _defaults = {'loai_khvc': 'all',
     'ngay_bd_phieu': fields.date.context_today,
     'ngay_kt_phieu': fields.date.context_today,
     'gio_bc': lambda self, cr, uid, context = {}: context.get('gio_bc', time.strftime('%Y-%m-%d %H:%M:%S'))}


icsc_baocao_kl_kvkn()