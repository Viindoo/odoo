# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import HttpCase, tagged
from odoo.tests.common import ChromeBrowser

# Shared by both tests: anchored at the fixture's top-left corner, the same
# spot a stray cursor near the origin sits over; the trusted count is read
# after two animation frames, once Blink settles any hover recomputation.
TRUSTED_HOVER_PROBE_EXPR = """(() => new Promise((resolve) => {
    const probe = document.createElement('button');
    probe.textContent = 'trusted-hover-probe';
    probe.style.position = 'fixed';
    probe.style.top = '0';
    probe.style.left = '0';
    document.body.appendChild(probe);
    let trustedHoverCount = 0;
    const countIfTrusted = (event) => { if (event.isTrusted) { trustedHoverCount += 1; } };
    probe.addEventListener('pointerover', countIfTrusted, true);
    probe.addEventListener('mouseover', countIfTrusted, true);
    probe.focus();
    probe.style.height = '48px';
    probe.scrollIntoView();
    requestAnimationFrame(() => requestAnimationFrame(() => {
        probe.remove();
        resolve(trustedHoverCount);
    }));
}))()"""


@tagged('post_install', '-at_install')
class BrowserHarnessCursorHygieneTests(HttpCase):
    """A browser-driven test page must never receive a TRUSTED pointer/mouse hover
    event (pointerover, mouseover, and their -enter siblings) that originates from
    the test harness's own environment rather than from a simulated user action.
    Injecting a mouse cursor inside the viewport reproduces this: the next focus,
    scroll, or layout change makes Blink dispatch a genuine (isTrusted) hover event
    to whatever element ends up under that point, corrupting any hover-driven
    assertion the page makes about its own, deliberately-triggered events. (Only
    this in-page mechanism, and the fix, are proven - the runbot's own OS-level
    cursor position at test start was never directly observed.)
    """

    def test_probe_detects_a_trusted_hover_event_from_a_stray_cursor(self):
        # Sensitivity guarantee, kept permanently: proves the probe below CAN
        # observe the phantom-hover condition on this machine/Chrome build, so
        # a green result on the harness test never gets mistaken for "the
        # condition cannot occur here" instead of "the harness prevents it".
        browser = ChromeBrowser(self)
        self.addCleanup(browser.stop)
        self.authenticate(None, None, browser=browser)
        self.cr.flush()
        self.cr.clear()
        browser.navigate_to(self.base_url() + '/web/login')
        browser._wait_ready()

        # Park the OS-level cursor inside the viewport, over the corner the
        # probe's element is anchored to, before any DOM mutation happens -
        # this is the hostile condition the harness must neutralise.
        browser._websocket_request('Input.dispatchMouseEvent', params={
            'type': 'mouseMoved', 'x': 1, 'y': 1,
        })
        result = browser._websocket_request('Runtime.evaluate', params={
            'expression': TRUSTED_HOVER_PROBE_EXPR,
            'awaitPromise': True,
        })['result']

        trusted_hover_count = result['value']
        self.assertGreaterEqual(
            trusted_hover_count, 1,
            "the hostile-cursor probe must be able to observe at least one "
            "trusted hover event on this machine/Chrome build, otherwise it "
            "cannot guard the harness behaviour asserted below",
        )

    def test_browser_harness_parks_cursor_before_test_code_runs(self):
        # Simulate "the browser is still sitting over a stray cursor position
        # right as the harness hands control to the page's own test code" by
        # injecting the hostile position at the exact boundary a harness fix
        # belongs at - once the harness itself considers the page ready and
        # right before test code starts running - regardless of where in a
        # real environment that stray position actually originates from.
        original_wait_ready = ChromeBrowser._wait_ready

        def _wait_ready_over_a_stray_cursor(browser, ready_code=None, timeout=60):
            is_ready = original_wait_ready(browser, ready_code, timeout=timeout)
            if is_ready:
                browser._websocket_request('Input.dispatchMouseEvent', params={
                    'type': 'mouseMoved', 'x': 1, 'y': 1,
                })
            return is_ready

        self.patch(ChromeBrowser, '_wait_ready', _wait_ready_over_a_stray_cursor)

        code = TRUSTED_HOVER_PROBE_EXPR + """.then((trustedHoverCount) => {
            if (trustedHoverCount === 0) {
                console.log('test successful');
            } else {
                console.error(
                    'phantom trusted hover event(s) reached the probe: '
                    + trustedHoverCount
                );
            }
        })"""
        self.browser_js('/web/login', code)
