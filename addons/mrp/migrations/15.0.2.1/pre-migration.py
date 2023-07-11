def migrate(cr, version):
    cr.execute(
        """
        WITH production_info AS (
            SELECT mp.id,
                   MIN(wo.date_start) AS date_start
              FROM mrp_production mp
              JOIN mrp_workorder wo
                ON wo.production_id = mp.id
             WHERE mp.state != 'draft'
               AND mp.date_start IS NULL
             GROUP BY mp.id
        )
        UPDATE mrp_production mp
           SET date_start = info.date_start
         FROM production_info info
         WHERE mp.id = info.id
        """
    )
