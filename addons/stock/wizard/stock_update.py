# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from pytz import timezone
from dateutil.relativedelta import relativedelta
from openerp.osv import fields, osv
from openerp.osv.orm import browse_record, browse_null
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP

class stock_update(osv.osv):
    _name = 'stock.update'
    _description = 'Update'
    _order = 'id desc'
    _columns = {
         'phieu_id': fields.many2one('stock.picking', 'PXK'),
         'bang_kiem_soat': fields.text('Bảng kiểm soát/số toa', required=True),
         'line_ids': fields.one2many('stock.move.update', 'parent_id', 'Sản phẩm'),
         'ngay_capnhat': fields.date('Ngày cập nhật'),
         'user_id': fields.many2one('res.users', 'Người cập nhật'),
         'date_done': fields.date('Ngày giao hàng',required=True),
         'partner_id': fields.many2one('res.partner', 'Khách hàng'),
         'daidien_muahang': fields.many2one('res.partner', 'Người đại diện mua hàng', domain="[('check','=',True),('parent_id','=',partner_id)]"),
         'loai_vanchuyen': fields.selection([('diennuoc', ''),('oto', 'Ô tô (Đường sắt – ô tô; đường thủy – ô tô, kho – ô tô)'), ('nhan_tai_ga', 'Nhận tại ga (cảng, kho ngoài)')], 'Hình thức vận chuyển')
         }

    def default_get(self, cr, uid, fields, context = None):
        """ To get default values for the object.
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param fields: List of fields for which we want default values
         @param context: A standard dictionary
         @return: A dictionary which of fields with values.
        """
        if context is None:
            context = {}
        picking_pool = self.pool.get('stock.picking')
        vals = []
        picking_obj = picking_pool.browse(cr, uid, context.get('active_id', False))
        res = super(stock_update, self).default_get(cr, uid, fields, context=context)
        if picking_obj.id:
            picking_id = picking_obj.id
            bang_kiem_soat = picking_obj.bang_kiem_soat
            ngaygiao = picking_obj.date_done
            for line in picking_obj.move_lines:
                vals.append({'product_id': line.product_id.id,
                 'no': line.no,
                 'chitiet_kh': line.id,
                 'product_qty': line.product_qty,
                 'product_uom': line.product_uom.id,
                 'location_id': line.location_id.id,
                 'location_dest_id': line.location_dest_id.id})

            if 'phieu_id' in fields:
                res.update({'phieu_id': picking_id})
            if 'bang_kiem_soat' in fields:
                res.update({'bang_kiem_soat': bang_kiem_soat})
            if 'line_ids' in fields:
                res.update({'line_ids': vals})
            if 'ngay_capnhat' in fields:
				datehd = datetime.now(timezone('UTC'))
				ngay_capnhat = datehd.astimezone(timezone('Asia/Ho_Chi_Minh'))
				res.update({'ngay_capnhat': ngay_capnhat.strftime("%Y-%m-%d")})
            if 'partner_id' in fields:
                res.update({'partner_id': picking_obj.partner_id.id})
            if 'daidien_muahang' in fields:
                res.update({'daidien_muahang': picking_obj.daidien_muahang.id})
            if 'date_done' in fields:
				ngay=str(ngaygiao)
				ngay2= datetime.strptime(ngay, "%Y-%m-%d %H:%M:%S")
				time1= ngay_capnhat.hour
				time2= ngay2.hour				
				if (time1>=7 and time2>=10 and time2<17): date_done1 = ngay2	
				else:date_done1 = ngay2 + timedelta(days=0, hours=7)				
				date_done3=str(date_done1)
				ngaychuan=date_done3[0:10]				
				date_done2=datetime.strptime(ngaychuan, "%Y-%m-%d")
				res.update({'date_done': date_done2.strftime("%Y-%m-%d")})
            if 'user_id' in fields:
                res.update({'user_id': uid})
            if 'loai_vanchuyen' in fields:
                res.update({'loai_vanchuyen': picking_obj.loai_vanchuyen})
        return res

    def action_correct_delivery(self, cr, uid, ids, context = None):
        picking_pool = self.pool.get('stock.picking')
        move_pool = self.pool.get('stock.move')
        update_pool = self.pool.get('stock.update')	
        for data in self.browse(cr, uid, ids, context):
            bang_kiem_soat = data.bang_kiem_soat
            daidien_muahang = data.daidien_muahang.id
            phieu_id = data.phieu_id.id
            date_done = data.date_done
            picking_pool.write(cr, uid, phieu_id, {'loai_vanchuyen': data.loai_vanchuyen,
             'nguoi_lap_phieu': data.user_id.id,
             'date_done': date_done,
             'date': date_done,
             'daidien_muahang': daidien_muahang,
             'bang_kiem_soat': bang_kiem_soat}, context=context)
            for line in data.line_ids:
                move_id = line.chitiet_kh.id
                move_pool.write(cr, uid, move_id, {'location_id': line.location_id.id,
                 'date': date_done}, context=context)

        return {'type': 'ir.actions.act_window_close'}


stock_update()

class stock_move_update(osv.osv):
    _name = 'stock.move.update'
    _description = 'Stock Move'
    _order = 'id desc'
    _columns = {
         'parent_id': fields.many2one('stock.update', 'Cập nhật'),
         'chitiet_kh': fields.many2one('stock.move', 'Chi tiết'),
         'no': fields.integer('STT'),
         'product_id': fields.many2one('product.product', 'Sản phẩm'),
         'product_qty': fields.float('Số lượng'),
         'product_uom': fields.many2one('product.uom', 'Đơn vị'),
         'location_id': fields.many2one('stock.location', 'Địa điểm nguồn'),
         'location_dest_id': fields.many2one('stock.location', 'Địa điểm đích')
         }


stock_move_update()