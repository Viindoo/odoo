def migrate(cr, version):
    cr.execute(
        """
        UPDATE mrp_production as mp
        SET date_start = (SELECT MIN(date_start) FROM mrp_workorder WHERE production_id = mp.id) 
        WHERE mp.state != 'draft' AND mp.date_start IS NULL
        """
    )
