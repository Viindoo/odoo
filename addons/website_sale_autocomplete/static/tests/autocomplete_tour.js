/** @odoo-module */

import { registry } from "@web/core/registry";
import tourUtils from '@website_sale/js/tours/tour_utils';


registry.category("web_tour.tours").add('autocomplete_tour', {
    test: true,
    url: '/shop', // /shop/address is redirected if no sales order
    steps: () => [
    ...tourUtils.addToCart({productName: "A test product"}),
    tourUtils.goToCart(),
    tourUtils.goToCheckout(),
{ // Actual test
    content: 'Input in Street & Number field',
    trigger: 'input[name="street"]',
    run: 'text This is a test'
}, {
    content: 'Check if results have appeared',
    trigger: '.js_autocomplete_result',
    run: function () {}
}, {
    content: 'Input again in street field',
    trigger: 'input[name="street"]',
    run: 'text add more'
}, {
    content: 'Click on the first result',
    trigger: '.js_autocomplete_result'
},
// The click empties the dropdown at once, but the fields are only filled when
// /autocomplete/address_full answers, and the debounced search of "add more" may
// still render a fresh dropdown afterwards: neither "the box disappeared" nor an
// immediate read of the fields is reliable, so wait for the expected values.
{ // Verify test data has been input
    content: 'Check Street & number have been set',
    trigger: 'input[name="street"]:propValue(42 A fictional Street)',
    run: function () {}
}, {
    content: 'Check City is not empty anymore',
    trigger: 'input[name="city"]:propValue(A Fictional City)',
    run: function () {}
}, {
    content: 'Check Zip code is not empty anymore',
    trigger: 'input[name="zip"]:propValue(12345)',
    run: function () {}
}]});
