from odoo import fields
from collections import defaultdict

_original_read = fields.Many2many.read


def patched_read(self, records):
    if (
        self.name in ('move_orig_ids', 'move_dest_ids')
        and records._name == 'stock.move'
    ):
        context = {'active_test': False}
        context.update(self.context)
        comodel = records.env[self.comodel_name].with_context(**context)
        domain = self.get_domain_list(records)
        comodel._flush_search(domain)
        wquery = comodel._where_calc(domain)
        comodel._apply_ir_rules(wquery, 'read')
        from_c, where_c, where_params = wquery.get_sql()
        group = defaultdict(list)
        # Join smaller CTEs to reduce the complexity of the full-table join
        records._cr.execute(f"""
            WITH allowed_move_ids AS (
                SELECT {comodel._table}.id FROM {from_c} WHERE {where_c or '1=1'}
            ),
            {self.relation}_tmp AS (
                SELECT {self.column1}, {self.column2}
                FROM {self.relation}
                WHERE {self.column1} = ANY(%s)
            )
            SELECT {self.relation}_tmp.{self.column1}, ARRAY_AGG(DISTINCT {self.relation}_tmp.{self.column2}) AS result_ids
            FROM allowed_move_ids
            JOIN {self.relation}_tmp ON {self.relation}_tmp.{self.column2} = allowed_move_ids.id
            GROUP BY {self.relation}_tmp.{self.column1}
            """,
            (*where_params, records.ids)
        )
        for row in records._cr.fetchall():
            group[row[0]] = row[1]
        values = [tuple(group[id_]) for id_ in records.ids]
        records.env.cache.insert_missing(records, self, values)
        return
    return _original_read(self, records)


fields.Many2many.read = patched_read
