import { defineCalendarModels } from "@calendar/../tests/calendar_test_helpers";
import { expect, test } from "@odoo/hoot";
import { queryAllTexts } from "@odoo/hoot-dom";
import {
    defineModels,
    defineParams,
    fields,
    models,
    mountView,
    serverState,
} from "@web/../tests/web_test_helpers";

class EventEn extends models.Model {
    _name = "event.en";

    mon = fields.Boolean({ string: "Mon" });
    tue = fields.Boolean({ string: "Tue" });
    wed = fields.Boolean({ string: "Wed" });
    thu = fields.Boolean({ string: "Thu" });
    fri = fields.Boolean({ string: "Fri" });
    sat = fields.Boolean({ string: "Sat" });
    sun = fields.Boolean({ string: "Sun" });

    _records = [{ id: 1 }];
}

class EventVi extends models.Model {
    _name = "event.vi";

    // The labels a Vietnamese user receives: all but Sunday's start with "T".
    mon = fields.Boolean({ string: "T2" });
    tue = fields.Boolean({ string: "T3" });
    wed = fields.Boolean({ string: "T4" });
    thu = fields.Boolean({ string: "T5" });
    fri = fields.Boolean({ string: "T6" });
    sat = fields.Boolean({ string: "T7" });
    sun = fields.Boolean({ string: "CN" });

    _records = [{ id: 1 }];
}

defineCalendarModels();
defineModels([EventEn, EventVi]);

async function mountWeekDays(resModel) {
    await mountView({
        type: "form",
        resModel,
        resId: 1,
        arch: `<form><widget name="calendar_week_days"/></form>`,
    });
    return queryAllTexts(".o_calendar_week_days_rounded");
}

test("weekday buttons can be told apart in Vietnamese", async () => {
    serverState.lang = "vi_VN";
    defineParams({ lang_parameters: { week_start: 1 } });

    expect(await mountWeekDays("event.vi")).toEqual(["T2", "T3", "T4", "T5", "T6", "T7", "CN"]);
});

test("weekday buttons keep their one-letter look in English", async () => {
    serverState.lang = "en_US";
    defineParams({ lang_parameters: { week_start: 7 } });

    expect(await mountWeekDays("event.en")).toEqual(["S", "M", "T", "W", "T", "F", "S"]);
});

test("weekday buttons render for a language whose code carries a script modifier", async () => {
    serverState.lang = "sr@latin";
    defineParams({ lang_parameters: { week_start: 1 } });

    expect(await mountWeekDays("event.en")).toEqual(["p", "u", "s", "č", "p", "s", "n"]);
});
