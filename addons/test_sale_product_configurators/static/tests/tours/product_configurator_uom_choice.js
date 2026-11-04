import { rpcBus } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { stepUtils } from "@web_tour/tour_utils";
import configuratorTourUtils from "@sale/js/tours/product_configurator_tour_utils";
import * as tourUtils from "@sale/js/tours/tour_utils";

/**
 * Run the click of the step and wait for the price updates it requests.
 *
 * The configurator sets the quantity at once and the price when its request
 * answers, so a quantity step whose price stays the same is satisfied before
 * that answer and the next step can send a second request, e.g. a UoM change.
 * When the first request answers last, its unit price replaces the price of
 * the new UoM.
 */
function clickAndWaitForPrice(step) {
    return {
        ...step,
        async run(helpers) {
            const pending = new Set();
            let settle;
            const onRequest = ({ detail }) => {
                if (detail.url === "/sale/product_configurator/update_combination") {
                    pending.add(detail.data.id);
                }
            };
            const onResponse = ({ detail }) => {
                if (pending.delete(detail.data.id) && !pending.size) {
                    settle?.();
                }
            };
            rpcBus.addEventListener("RPC:REQUEST", onRequest);
            rpcBus.addEventListener("RPC:RESPONSE", onResponse);
            try {
                await helpers.click();
                if (pending.size) {
                    await new Promise((resolve) => (settle = resolve));
                }
            } finally {
                rpcBus.removeEventListener("RPC:REQUEST", onRequest);
                rpcBus.removeEventListener("RPC:RESPONSE", onResponse);
            }
        },
    };
}

registry.category("web_tour.tours").add("sale_product_configurator_uom_tour", {
    steps: () => [
        ...stepUtils.goToAppSteps("sale.sale_menu_root", "Go to the Sales App"),
        ...tourUtils.createNewSalesOrder(),
        ...tourUtils.selectCustomer("Tajine Saucisse"),
        ...tourUtils.selectPricelist("Custom pricelist (TEST)"),
        ...tourUtils.addProduct("Customizable Desk (TEST)"),
        configuratorTourUtils.assertProductPrice("Customizable Desk (TEST)", "750.00"),
        configuratorTourUtils.increaseProductQuantity("Customizable Desk (TEST)"),
        configuratorTourUtils.assertProductPrice("Customizable Desk (TEST)", "600.00"),
        configuratorTourUtils.decreaseProductQuantity("Customizable Desk (TEST)"),
        configuratorTourUtils.assertProductPrice("Customizable Desk (TEST)", "750.00"),
        configuratorTourUtils.setProductUoM("Customizable Desk (TEST)", "Dozens"),
        configuratorTourUtils.assertProductPrice("Customizable Desk (TEST)", "7,200.00"),
        configuratorTourUtils.addOptionalProduct("Conference Chair"),
        configuratorTourUtils.assertProductPrice("Conference Chair", "16.50"),
        clickAndWaitForPrice(configuratorTourUtils.increaseProductQuantity("Conference Chair")),
        configuratorTourUtils.assertProductPrice("Conference Chair", "16.50"),
        configuratorTourUtils.setProductUoM("Conference Chair", "Dozens"),
        configuratorTourUtils.assertProductPrice("Conference Chair", "198.00"),
        configuratorTourUtils.addOptionalProduct("Chair floor protection"),
        configuratorTourUtils.assertProductPrice("Chair floor protection", "12.00"),
        configuratorTourUtils.increaseProductQuantity("Chair floor protection"),
        configuratorTourUtils.assertPriceTotal("7,620.00"),
        ...configuratorTourUtils.saveConfigurator(),
        {
            content: "verify SO final price excluded",
            trigger: 'span[name="Untaxed Amount"]:contains("7,620.00")',
            run: "click",
        },
        {
            content: "verify SO final price included",
            trigger: 'span[name="amount_total"]:contains("8,700.00")',
            run: "click",
        },
        ...stepUtils.saveForm(),
    ],
});
