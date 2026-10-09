import {
    contains,
    mailModels,
    openFormView,
    openKanbanView,
    start,
    startServer,
} from "@mail/../tests/mail_test_helpers";
import { ResPartner } from "@mail/../tests/mock_server/mock_models/res_partner";
import { beforeEach, describe, test } from "@odoo/hoot";
import { defineModels, defineParams, fields, models } from "@web/../tests/web_test_helpers";

describe.current.tags("desktop");

class Stage extends models.Model {
    _name = "stage";
    name = fields.Char();
}

let partnerId;

beforeEach(async () => {
    ResPartner._fields.stage_id = fields.Many2one({ relation: "stage" });
    ResPartner._fields.duration_tracking = fields.Json();
    ResPartner._fields.is_rotting = fields.Boolean();
    ResPartner._fields.rotting_days = fields.Integer();
    defineModels({ ...mailModels, ResPartner, Stage });
    // A language that writes the unit as a word after a space.
    defineParams({ translations: { "%(numberOfDays)sd": "%(numberOfDays)s ngày" } });
    const pyEnv = await startServer();
    const [stageId] = pyEnv["stage"].create([{ name: "New" }]);
    partnerId = pyEnv["res.partner"].create({
        name: "John Doe",
        stage_id: stageId,
        is_rotting: true,
        rotting_days: 5,
    });
});

test("rotting badge of the form status bar shows the day count in the user's language", async () => {
    await start();
    await openFormView("res.partner", partnerId, {
        arch: `
            <form>
                <field name="is_rotting" invisible="1"/>
                <field name="rotting_days" invisible="1"/>
                <field name="stage_id" widget="rotting_statusbar_duration"/>
            </form>`,
    });
    await contains(".o_statusbar_status .o_mail_resource_rotting_bg", { text: "5 ngày" });
});

test("rotting badge of a kanban card shows the day count in the user's language", async () => {
    await start();
    await openKanbanView("res.partner", {
        arch: `
            <kanban>
                <templates>
                    <t t-name="card">
                        <field name="name"/>
                        <field name="is_rotting" invisible="1"/>
                        <field name="rotting_days" widget="rotting"/>
                    </t>
                </templates>
            </kanban>`,
    });
    await contains(".o_kanban_record .o_mail_resource_rotting_bg", { text: "5 ngày" });
});
