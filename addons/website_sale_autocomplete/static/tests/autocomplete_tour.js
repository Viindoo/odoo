/** @odoo-module */

import { registry } from "@web/core/registry";
import { TourError } from "@web_tour/tour_service/tour_utils";
import tourUtils from '@website_sale/js/tours/tour_utils';


function fail (errorMessage) {
    throw new TourError(errorMessage);
}

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
    // After re-typing, wait for the results list to be present before clicking.
    // Without this guard the click can land on a stale element that is being replaced
    // by the new debounced request, causing _perform_complete_place_search to never fire.
    content: 'Wait for results after second input',
    trigger: '.js_autocomplete_result',
    run: function () {}
}, {
    content: 'Click on the first result',
    trigger: '.js_autocomplete_result'
}, {
    content: 'Verify the autocomplete box disappeared',
    trigger: 'body:not(:has(.js_autocomplete_result))'
}, { // Verify test data has been input
    content: 'Check Street & number have been set',
    trigger: 'input[name="street"]',
    run: function () {
        if (this.$anchor.val() !== '42 A fictional Street') {
            fail('Street value is not correct : ' + this.$anchor.val())
        }
    }
}, {
    content: 'Check City is not empty anymore',
    trigger: 'input[name="city"]',
    run: function () {
        if (this.$anchor.val() !== 'A Fictional City') {
            fail('Street value is not correct : ' + this.$anchor.val())
        }
    }
}, {
    content: 'Check Zip code is not empty anymore',
    trigger: 'input[name="zip"]',
    run: function () {
        if (this.$anchor.val() !== '12345') {
            fail('Street value is not correct : ' + this.$anchor.val())
        }
    }
}]});
