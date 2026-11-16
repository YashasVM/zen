/* Any copyright is dedicated to the Public Domain.
   https://creativecommons.org/publicdomain/zero/1.0/ */

"use strict";

add_setup(async function () {
  await SpecialPowers.pushPrefEnv({
    set: [["zen.urlbar.replace-newtab", false]],
  });

  registerCleanupFunction(async () => {
    await SpecialPowers.popPrefEnv();
  });
});

add_task(async function test_Check_Creation() {
  const placeToDoubleClick =
    gZenWorkspaces.activeWorkspaceElement.querySelector(
      ".zen-workspace-empty-space",
    );
  ok(placeToDoubleClick, "We should have found the place to double click.");
  EventUtils.sendMouseEvent({ type: "dblclick" }, placeToDoubleClick, window);
  await TestUtils.waitForCondition(
    () => gBrowser.tabs.length === 3,
    "New tab should be opened.",
  );
  ok(true, "New tab should be opened.");
  await BrowserTestUtils.removeTab(gBrowser.tabs[1]);
  Assert.strictEqual(gBrowser.tabs.length, 2, "There should be one tab.");
});

add_task(async function test_double_click_overflow_padding_opens_tab() {
  await gZenWorkspaces.promiseInitialized;
  const originalTabs = new Set(gBrowser.tabs);
  const selectedTab = gBrowser.selectedTab;
  const scrollbox = gZenWorkspaces.activeScrollbox;
  try {
    for (let i = 0; i < 40; i++) {
      BrowserTestUtils.addTab(gBrowser, "about:blank", {
        skipAnimation: true,
      });
    }
    await TestUtils.waitForCondition(
      () => scrollbox.overflowing,
      "The tab list overflows",
    );
    const inner = scrollbox.scrollbox;
    inner.scrollTop = inner.scrollHeight;
    await TestUtils.waitForCondition(
      () => inner.scrollTop + inner.clientHeight >= inner.scrollHeight - 1,
      "The empty padding at the bottom is visible",
    );
    const count = gBrowser.tabs.length;
    const rect = inner.getBoundingClientRect();
    const clicked = BrowserTestUtils.waitForEvent(scrollbox, "dblclick");
    EventUtils.synthesizeMouseAtPoint(
      rect.x + rect.width / 2,
      rect.bottom - 30,
      { clickCount: 2 },
      window,
    );
    const event = await clicked;
    Assert.equal(
      event.originalTarget,
      inner,
      "The double-click hit the scrollbox padding, not a tab or control",
    );
    await TestUtils.waitForCondition(
      () => gBrowser.tabs.length === count + 1,
      "Double-clicking the overflow padding opens a new tab",
    );
  } finally {
    gBrowser.selectedTab = selectedTab;
    for (const tab of [...gBrowser.tabs]) {
      if (!originalTabs.has(tab)) {
        BrowserTestUtils.removeTab(tab);
      }
    }
  }
});
