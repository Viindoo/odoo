# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from decimal import Decimal
import time
import re
from dateutil import parser
import datetime
from datetime import date
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.report import report_sxw

class picking(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(picking, self).__init__(cr,  uid, name, context=context)
        self.localcontext.update({'time': time,
         'get_pxk': self.get_pxk,
         'get_nguoilp': self.get_nguoilp,         
         'get_product_desc': self.get_product_desc,
         'get_product_uom': self.get_product_uom,
         'get_product_soluong': self.get_product_soluong,
         'get_product_ngay': self.get_product_ngay,
         'get_product_thang': self.get_product_thang,		 
         'get_product_nam': self.get_product_nam,
         'get_npp_mavung': self.get_npp_mavung,
         'get_loai_xuatkho': self.get_loai_xuatkho,
         'get_version': self.get_version, 
         'get_ma_dvtt': self.get_ma_dvtt,
         'get_in_mvtt': self.get_in_mvtt,
         'get_in_ten': self.get_in_ten,
         'get_in_tieude': self.get_in_tieude,
         'get_in_donvi1': self.get_in_donvi1,
         'get_in_donvitt': self.get_in_donvitt,
         'get_ten_donvitt': self.get_ten_donvitt,         
         'get_product_loaivc': self.get_product_loaivc,
         'get_product_fax': self.get_product_fax,            
         'get_ma_kho': self.get_ma_kho,		 		 
         'get_ten_kho': self.get_ten_kho,		 		          
         'get_product_ma2': self.get_product_ma2,
         'get_product_ma3': self.get_product_ma3,
         'get_product_ma4': self.get_product_ma4,         
         'get_product_ma5': self.get_product_ma5,         
         'get_product_ma6': self.get_product_ma6,     
         'get_product_ma1': self.get_product_ma1,
         'get_product_ma7': self.get_product_ma7,
         'get_product_ma8': self.get_product_ma8,
         'get_product_ma9': self.get_product_ma9 
         })        

    def get_product_desc(self, move_line):
        a = move_line.product_id.name
        desc=''
        
        if move_line.product_id.default_code and  move_line.product_id.state !='cancel' :
            desc = '[' + move_line.product_id.default_code + ']' + ' ' + a
            
        return desc
    def get_product_ma(self, move_line) :
        a1 = ''
        desc1 = []		
        desc2=''		
        if move_line.product_id.default_code and  move_line.product_id.state !='cancel':
			a1 = move_line.product_id.default_code
			desc2 = desc1.append(a1)		
        return desc2
    def get_product_uom(self, move_line):
        uom = move_line.product_uom.name
        if move_line.product_uom.name and move_line.product_id.state !='cancel':
            uom = move_line.product_uom.name[:1]
            
        return uom
    def get_pxk(self,  pick):
        pxk = pick.name
        if pick.name:
            pxk = pick.name
            
        return pxk 
    def get_nguoilp(self,  pick):
        nguoilp = pick.nguoi_lap_phieu.name
        if pick.nguoi_lap_phieu.name:
            nguoilp = pick.nguoi_lap_phieu.name
            
        return nguoilp         
    def get_product_soluong(self, move_line):
        soluong = 0
        test= Decimal(float(move_line.product_qty)) % 1 == 0
        if test == True:
            soluong = int(move_line.product_qty)
        else:
            soluong = round(move_line.product_qty,3)
        return soluong
    def get_product_ngay(self, pick):
        ids = pick.id
        ngsy=''	
        stmt= "select to_char(date_done + INTERVAL '7 hours','dd') from stock_picking where id = %s and state = 'done' and mistake_delivery != True"%(ids)       
        self.cr.execute(stmt)
        code = self.cr.fetchone()
        ngay = str(code[0])
	
        return ngay
    def get_product_thang(self, pick):
        ids = pick.id
        thang=''	
        stmt= "select to_char(date_done + INTERVAL '7 hours','mm') from stock_picking where id = %s and state = 'done' and mistake_delivery != True"%(ids)       
        self.cr.execute(stmt)
        code = self.cr.fetchone()
        thang = str(code[0])
        return thang
    def get_product_nam(self, pick):
        ids = pick.id
        nam=''	
        stmt= "select to_char(date_done + INTERVAL '7 hours','yyyy') from stock_picking where id = %s and state = 'done' and mistake_delivery != True"%(ids)       
        self.cr.execute(stmt)
        code = self.cr.fetchone()
        nam = str(code[0])		
        return nam
    def get_npp_mavung(self, pick):
        npp_vung = str(pick.npp_mavung)
        if npp_vung !='':
            npp_mavung = '|'+str(pick.npp_mavung)
        if npp_vung=='':
            npp_mavung = ''
        return npp_mavung
    def get_loai_xuatkho(self, pick):
        test = pick.is_npp     
        pxk_cha = str(pick.backorder_id.name)
        if test != True:
            loai_xuatkho = '|'+pick.loai_xuatkho+'|'
        if test == True:
            loai_xuatkho = '|'+'khotc'+'|'        
        return loai_xuatkho 
    def get_ma_dvtt(self, pick):
        pxk_cha = pick.backorder_id.name        
        test = pick.is_npp     
        if test != True:
            ma_dvtt = ''
        if test == True and pxk_cha !='':
            ma_dvtt = '|'+pick.npp_id.client_code
        if test == True and pxk_cha =='':
            ma_dvtt = pick.npp_id.client_code            
        return ma_dvtt
    def get_in_mvtt(self, pick):
        test = pick.is_npp
        mavungtt = ''
        if test != True:
            mavungtt = ''            
        if test == True:
            mavungtt = str(pick.npp_mavung)          
        return mavungtt
    def get_in_ten(self, pick):
        test = pick.is_npp
        tenvtt = ''
        if test != True:
            tenvtt = ''            
        if test == True:
            tenvtt = 'Mã vùng tiêu thụ:'+''
        return tenvtt 
    def get_in_tieude(self, pick):
        test = pick.is_npp
        tenmavt = ''
        if test != True:
            tenmavt = 'Mã vùng:'+''            
        if test == True:
            tenmavt = 'Mã vùng vận tải:'+''
        return tenmavt
    def get_in_donvi1(self, pick):
        test = pick.is_npp
        donvi1 = ''
        if test != True:
            donvi1 = 'Đơn vị nhận hàng:'+' '            
        if test == True:
            donvi1 = 'Đơn vị vận tải:'+' '
        return donvi1
    def get_in_donvitt(self, pick):
        test = pick.is_npp
        donvitt = ''
        if test != True:
            donvitt = ''            
        if test == True:
            donvitt = pick.npp_id.name
        return donvitt 
    def get_ten_donvitt(self, pick):
        test = pick.is_npp
        ten_donvitt = ''
        if test != True:
            ten_donvitt = ''            
        if test == True:
            ten_donvitt = 'Đơn vị tiêu thụ:'+' '
        return ten_donvitt         
    def get_version(self, pick):
        test = pick.is_npp     
        if test != True:
            version = ''
        if test == True:
            version = 'V2'+'|'
        return version          
    def get_product_loaivc(self, pick):
        loai = pick.loai_vanchuyen 
        nam = ''		
        if loai=='oto':
            loaivc = 'Ô tô (Đường sắt - Ô tô; Đường thủy - Ô tô; Kho - Ô tô)'
        if loai=='nhan_tai_ga':
            loaivc = 'Nhận tại ga (Cảng; Kho ngoài)'				
        return loaivc
    def get_product_fax(self, pick):
        loai = pick.loai_vanchuyen 
        if loai=='oto':
            fax = ''
        if loai=='nhan_tai_ga':
            fax = 'Bán hàng qua fax'				
        return fax        
    def get_ma_kho(self, pick):
       ids = pick.id
       desc=''	
       ma1=''	
       ma2=''	       
       stmt= "select st.code from stock_picking sp left join stock_move mv on mv.picking_id = sp.id left join stock_location st on mv.location_id = st.id where sp.id= %s and sp.type = 'out' and mv.state!='cancel' and sp.state = 'done' and sp.mistake_delivery != True"%(ids)       
       self.cr.execute(stmt)
       code = self.cr.fetchone()
       desc = str(code[0])
       return desc
    def get_ten_kho(self, pick):
       ids = pick.id
       desc=''	
       ma1=''	
       ma2=''	       
       stmt= "select st.code from stock_picking sp left join stock_move mv on mv.picking_id = sp.id left join stock_location st on mv.location_id = st.id where sp.id= %s and sp.type = 'out' and sp.state = 'done' and mv.state!='cancel' and sp.mistake_delivery != True"%(ids)       
       self.cr.execute(stmt)
       code = self.cr.fetchone()
       code1 = str(code[0])
       if code1=='119001':
            desc = 'Kho Supe lân 1'
       if code1=='119002':
            desc = 'Kho Supe lân 2'            
       if code1=='119003':
            desc = 'Kho NPK 1'
       if code1=='119004':
            desc = 'Kho NPK 2'
       if code1=='119005':
            desc = 'Kho NPK 3'            
       if code1=='119006':
            desc = 'Kho Lân nung chảy'
       if code1=='119007':
            desc = 'Kho Axit 1'
       if code1=='119008':
            desc = 'Kho Axit 2'
       if code1=='119009':
            desc = 'Kho sản phẩm khác'
       if code1=='11900B':
            desc = 'Kho thí nghiệm'
       if code1=='119010':
            desc = 'Kho Trừ Sâu 1'
       if code1=='119011':
            desc = 'Kho Trừ Sâu 2'
       if code1=='119013':
            desc = 'Kho sản phẩm phụ'        
       if code1=='11905b':
            desc = 'Kho NPK 4'
       if code1=='119099':
            desc = 'Kho cước'                
       if code1=='1290':
            desc = 'Kho gia công Hà Anh'                
       if code1=='1340':
            desc = 'Kho XN NPK Hải Dương'        
       if code1=='119000-A':
            desc = 'Kho NPK 4 (Đổi trả)'        
       if code1=='119001-A':
            desc = 'Kho Supe lân 1 (Đổi trả)'        
       if code1=='119002-A':
            desc = 'Kho Supe lân 2 (Đổi trả)'        
       if code1=='119003-A':
            desc = 'Kho NPK 1 (Đổi trả)'        
       if code1=='119004-A':
            desc = 'Kho NPK 2 (Đổi trả)'        
       if code1=='119005-A':
            desc = 'Kho NPK 3 (Đổi trả)'        
       if code1=='119007-A':
            desc = 'Kho Axit 1 (Đổi trả)'        
       if code1=='119008-A':
            desc = 'Kho Axit 2 (Đổi trả)'        
       if code1=='119006-A':
            desc = 'Kho Lân nung chảy (Đổi trả)'        
       if code1=='1290-A':
            desc = 'Kho gia công Hà Anh (Đổi trả)'        
       if code1=='1340-A':
            desc = 'Kho XN NPK Hải Dương (Đổi trả)'        
       return desc	     
    def get_product_ma1(self, pick):
       ids = pick.id
       desc=''	      
       stmt1= "SELECT left(string_agg(pr.default_code,''),6) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
       self.cr.execute(stmt1)
       code1 = self.cr.fetchone()[0]
       if pick.product_id.default_code:
           desc = code1
       return desc
    def get_product_ma2(self, pick):	
       ids = pick.id
       desc=''	          
       stmt2= "SELECT left(string_agg('','|'),1),left(string_agg(sm.product_qty::varchar,'|'),6) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
       self.cr.execute(stmt2)
       code2 = self.cr.fetchone()[0]
       
       if pick.product_id.default_code:
           desc = '|T'+code2
       return desc       
    def get_product_ma3(self, pick):
       ids = pick.id
       desc=''					
       dem2= "SELECT count(sm.id) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)
       self.cr.execute(dem2)
       dem = self.cr.fetchone()[0]
       dai= "SELECT length(string_agg(round(sm.product_qty,2)::varchar,'|')) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)                     
       self.cr.execute(dai)   
       dai2 = self.cr.fetchone()[0]
       if dem==1:
		   ma = pick.product_id.default_code[-1:]
		   if pick.product_id.default_code[-1:]=="A":
			   m=1
			   stmt3= "SELECT sm.product_qty from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
			   self.cr.execute(stmt3)
			   code3 = self.cr.fetchone()[0]       
			   desc = '|'+ str(code3*0.025)			   
		   if pick.product_id.default_code[-1:]=="B":
			   m=2
			   stmt3= "SELECT sm.product_qty from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
			   self.cr.execute(stmt3)
			   code3 = self.cr.fetchone()[0]       
			   desc = '|'+ str(code3*0.05)			   
		   if pick.product_id.default_code[-1:]!="B" and pick.product_id.default_code[-1:]!="A":
			   stmt3= "SELECT sm.product_qty from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
			   self.cr.execute(stmt3)
			   code3 = self.cr.fetchone()[0]       
			   desc = '|'+str(code3)		   
       if dem>1:
		   ma = pick.product_id.default_code[-1:]
		   if pick.product_id.default_code[-1:]=="A":
			   m=1
			   stmt3= "SELECT sm.product_qty from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
			   self.cr.execute(stmt3)
			   code3 = self.cr.fetchone()[0]       
			   desc = '|'+ str(code3*0.025)			   
		   if pick.product_id.default_code[-1:]=="B":
			   stmt3= "SELECT sm.product_qty from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
			   self.cr.execute(stmt3)
			   code3 = self.cr.fetchone()[0]       
			   desc = str(code3*0.025)			   
		   if pick.product_id.default_code[-1:]!="B" and pick.product_id.default_code[-1:]!="A":
			   stmt3= "SELECT sm.product_qty from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
			   self.cr.execute(stmt3)
			   code3 = self.cr.fetchone()[0]       
			   desc = str(code3)		   
       return desc   
    def get_product_ma4(self, pick):
       ids = pick.id
       desc=''	
       stmt1= "SELECT count(sm.id) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
       self.cr.execute(stmt1)
       ma2= self.cr.fetchall()[0][0]            
       if ma2>1:              
           stmt= "SELECT right(string_agg(pr.default_code,''),6) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)              
           self.cr.execute(stmt)
           code = self.cr.fetchone()[0]
           desc = code +'|' 
       return desc
    def get_product_ma5(self, pick):
       ids = pick.id
       desc=''	
       stmt1= "SELECT count(sm.id) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)              
       self.cr.execute(stmt1)
       ma2= self.cr.fetchall()[0][0]           
       if ma2>1:            
           stmt= "SELECT left(string_agg('T','|'),1),left(string_agg(sm.product_qty::varchar,'|'),6) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
           self.cr.execute(stmt)
           code = self.cr.fetchone()[0]
           desc = code+'|'
       return desc        
    def get_product_ma6(self, pick):
       ids = pick.id
       desc=''
       desc1=0	   
       ma1=0       
       stmt1= "SELECT count(sm.id) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
       self.cr.execute(stmt1)
       ma1= self.cr.fetchall()[0][0]
       ma2=ma1           
       if ma2==2:
		   desc=''
		   des1=0	           
		   if pick.product_id.default_code[-1:]=="A":	   
			   stmt= "SELECT (string_agg(sm.product_qty::varchar,'|')) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)              
			   self.cr.execute(stmt)
			   code = self.cr.fetchone()[0]
			   desc =  code.split('|')[1]
			   desc1 =  float(desc)*0.025
		   if pick.product_id.default_code[-1:]=="B":	   
			   stmt= "SELECT (string_agg(sm.product_qty::varchar,'|')) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)              
			   self.cr.execute(stmt)
			   code = self.cr.fetchone()[0]
			   desc =  code.split('|')[1]
			   desc1 =  float(desc)*0.05
		   if pick.product_id.default_code[-1:]!="B" and pick.product_id.default_code[-1:]!="A":
			   stmt= "SELECT (string_agg(sm.product_qty::varchar,'|')) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)              
			   self.cr.execute(stmt)
			   code = self.cr.fetchone()[0]
			   desc =  code.split('|')[1]
			   desc1 =  float(desc)
       return desc1              
       if ma2==3:
		   desc=''
		   desc1=0	        
		   if pick.product_id.default_code[-1:]=="A":	   
			   stmt= "SELECT (string_agg(sm.product_qty::varchar,'|')) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)              
			   self.cr.execute(stmt)
			   code = self.cr.fetchone()[0]
			   desc =  code.split('|')[2]
			   desc1 =  float(desc)*0.025
		   if pick.product_id.default_code[-1:]=="B":	   
			   stmt= "SELECT (string_agg(sm.product_qty::varchar,'|')) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)              
			   self.cr.execute(stmt)
			   code = self.cr.fetchone()[0]
			   desc =  code.split('|')[2]
			   desc1 =  float(desc)*0.05
		   if pick.product_id.default_code[-1:]!="B" and pick.product_id.default_code[-1:]!="A":
			   stmt= "SELECT (string_agg(sm.product_qty::varchar,'|')) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)              
			   self.cr.execute(stmt)
			   code = self.cr.fetchone()[0]
			   desc =  code.split('|')[2]
			   desc1 =  float(desc)   
       return desc1
# lấy 3 dòng sản phẩm
    def get_product_ma7(self, pick):
       ids = pick.id
       desc=''	
       ma1=0
       stmt1= "SELECT count(sm.id) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
       self.cr.execute(stmt1)
       ma3= self.cr.fetchall()[0][0]     
       if ma3>=3:              
           stmt= "SELECT left(right(string_agg(pr.default_code,''),10),6) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)              
           self.cr.execute(stmt)
           code = self.cr.fetchone()[0]
           desc = code +'|'
       return desc
    def get_product_ma8(self, pick):
       ids = pick.id
       desc=''	
       ma1=0
       stmt1= "SELECT count(sm.id) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)              
       self.cr.execute(stmt1)
       ma3= self.cr.fetchall()[0][0]            
       if ma3>=3:              
           stmt= "SELECT left(string_agg('T','|'),1),left(string_agg(sm.product_qty::varchar,'|'),13) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
           self.cr.execute(stmt)
           code = self.cr.fetchone()[0]
           desc = code +'|'
       return desc        
    def get_product_ma9(self, pick):
       ids = pick.id
       desc=''	
       ma1=0       
       stmt1= "SELECT count(sm.id) from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)       
       self.cr.execute(stmt1)
       ma3= self.cr.fetchall()[0][0]          
       if ma3>=3:
           stmt= "SELECT string_agg(sm.product_qty::varchar,'|') from stock_move sm left join product_product pr on pr.id =sm.product_id left join product_template pt on pr.product_tmpl_id = pt.id left join product_uom pu on pt.uom_id = pu.id left join stock_picking sp on sm.picking_id = sp.id where sp.id=%s and sm.state!='cancel'"%(ids)              
           self.cr.execute(stmt)
           code = self.cr.fetchone()[0]
           desc = code.split('|')[1]
       return desc   
# hết       

# hết       
for suffix in ['', '.in', '.out']:
    report_sxw.report_sxw('report.stock.picking.list' + suffix, 'stock.picking' + suffix, 'addons/stock/report/picking.rml', parser=picking)