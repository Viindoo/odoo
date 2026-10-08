/** @odoo-module **/

import { registry } from "@web/core/registry";
import wsTourUtils from '@website_sale/js/tours/tour_utils';
import wTourUtils from '@website/js/tours/tour_utils';

registry.category("web_tour.tours").add('website_sale_reorder_from_portal', {
        test: true,
        url: '/my/orders',
        steps: () => [
        // Initial reorder, nothing in cart
        {
            content: 'Select first order',
            trigger: '.o_portal_my_doc_table a:first',
        },
        wTourUtils.clickOnElement('Reorder Again', '.o_wsale_reorder_button'),
        wTourUtils.clickOnElement('Confirm', '.o_wsale_reorder_confirm'),
        wsTourUtils.assertCartContains({productName: 'Reorder Product 1'}),
        wsTourUtils.assertCartContains({productName: 'Reorder Product 2'}),
        {
            content: "Check that quantity is 1",
            trigger: ".js_quantity[value='1']",
        },
        // Second reorder, add reorder to cart
        {
            content: "Go back to my orders",
            trigger: "body",
            run: () => {
                window.location = "/my/orders";
            }
        },
        {
            content: 'Select first order',
            trigger: '.o_portal_my_doc_table a:first',
        },
        wTourUtils.clickOnElement('Reorder Again', '.o_wsale_reorder_button'),
        wTourUtils.clickOnElement('Confirm', '.o_wsale_reorder_confirm'),
        wTourUtils.clickOnElement('No', 'button:contains(No)'),
        wsTourUtils.assertCartContains({productName: 'Reorder Product 1'}),
        wsTourUtils.assertCartContains({productName: 'Reorder Product 2'}),
        {
            content: "Check that quantity is 2",
            trigger: ".js_quantity[value='2']",
        },
        // Third reorder, clear cart and reorder
        {
            content: "Go back to my orders",
            trigger: "body",
            run: () => {
                window.location = "/my/orders";
            }
        },
        {
            content: 'Select first order',
            trigger: '.o_portal_my_doc_table a:first',
        },
        wTourUtils.clickOnElement('Reorder Again', '.o_wsale_reorder_button'),
        wTourUtils.clickOnElement('Confirm', '.o_wsale_reorder_confirm'),
        wTourUtils.clickOnElement('Yes', 'button:contains(Yes)'),
        wsTourUtils.assertCartContains({productName: 'Reorder Product 1'}),
        wsTourUtils.assertCartContains({productName: 'Reorder Product 2'}),
        {
            content: "Check that quantity is 1",
            trigger: ".js_quantity[value='1']",
        },
        // Fourth reorder making sure confirmation dialog doesn't pop up unnecessary
        {
            content: "Deleting All products from cart",
            trigger: 'div.js_cart_lines',
            run: async () => {
                // The quantity change is debounced (500ms) then sent by RPC, and the
                // input ignores changes until the answer comes back: a click sent after
                // a fixed delay may hit the line still being removed and be lost, which
                // leaves a line in the cart. Wait for the cart lines to be re-rendered
                // (the clicked link is detached) before removing the next one. Removing
                // the last line reloads the page, which ends this step.
                let deleteLink;
                while ((deleteLink = document.querySelector("a.js_delete_product"))) {
                    deleteLink.click();
                    while (deleteLink.isConnected) {
                        await new Promise((r) => setTimeout(r, 50));
                    }
                }
            }
        },
        {
            content: "Go to my orders",
            trigger: 'body',
            run: () => {
                window.location = '/my/orders';
            }
        },
        {
            content: "Select first order",
            trigger: '.o_portal_my_doc_table a:first',
        },
        wTourUtils.clickOnElement('Reorder Again', '.o_wsale_reorder_button'),
        wTourUtils.clickOnElement('Confirm', '.o_wsale_reorder_confirm'),
        wsTourUtils.assertCartContains({productName: 'Reorder Product 1'}),
        {
            content: "Check that quantity is 1",
            trigger: ".js_quantity[value='1']",
            isCheck: true,
        },
    ]
});
