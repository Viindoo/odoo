import { registry } from "@web/core/registry";

registry.category("web_tour.tours").add('test_repair_without_product_in_parts', {

    steps: () => [
    {
        content: "Click product_id field",
        trigger: "div[name='move_ids'] .o_data_row td.o_data_cell[name=product_id]",
        run: "click",
    },
    {
        content: "Unset the product",
        trigger: "div[name=move_ids] div[name=product_id] input",
        run: "edit",
    },
    {
        content: "Click partner field",
        trigger: ".o_field_widget[name=partner_id] input",
        // Type the partner name: the customer search mode of the field orders
        // the dropdown by customer_rank, so on a database with enough ranked
        // customers a bare click would not show "A Partner" (rank 0) in the
        // first page at all.
        run: "edit A Partner",
    },
    // Note: Selecting the partner is only to trigger the compute;
    // this could be done by modifying any other field.
    {
        content: "Select partner",
        trigger: ".ui-menu-item > a:contains('A Partner')",
        run: "click",
    },
    {
        content: "Click the product field",
        trigger: "div[name=move_ids] .o_field_widget[name=product_id] input",
        run: "edit [1234] A Product",
    },
    {
        content: "Select a product",
        trigger:".ui-menu-item > a:contains('[1234] A Product')",
        run: "click",
    },
    {
        content: "Save the repair order",
        trigger: ".o_form_button_save",
        run: "click",
    },
    {
        content: "wait for save completion",
        trigger: ".o_form_saved",
    },
]});
