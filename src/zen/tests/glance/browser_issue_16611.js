/* Any copyright is dedicated to the Public Domain.
   https://creativecommons.org/publicdomain/zero/1.0/ */

"use strict";

add_task(async function test_glance_keeps_empty_tab_area() {
  await SpecialPowers.pushPrefEnv({
    set: [
      ["zen.window-sync.enabled", false],
      ["zen.testing.enabled", false],
      ["zen.urlbar.open-on-startup", false],
    ],
  });
  const win = await BrowserTestUtils.openNewBrowserWindow();
  try {
    await win.gZenWorkspaces.promiseInitialized;
    await win.gZenStartup.promiseInitialized;
    // Exercise the TabOpen layout updates and animations used outside tests.
    win.gZenUIManager.testingEnabled = false;
    const browser = win.gBrowser;
    const parent = BrowserTestUtils.addTab(browser, "about:robots", {
      skipAnimation: true,
    });
    await TestUtils.waitForCondition(
      () =>
        parent.linkedBrowser.currentURI.spec === "about:robots" &&
        !parent.linkedBrowser.webProgress.isLoadingDocument,
      "The pinned page has loaded",
    );
    browser.pinTab(parent);
    browser.selectedTab = parent;
    for (const tab of [...browser.tabs]) {
      if (tab !== parent && !tab.hasAttribute("zen-empty-tab")) {
        await BrowserTestUtils.removeTab(tab);
      }
    }
    const pins = win.gZenWorkspaces.activeWorkspaceElement.pinnedTabsContainer;
    await TestUtils.waitForCondition(
      () => pins.hasAttribute("hide-separator"),
      "The separator is hidden without unpinned tabs",
    );
    // Drain delayed startup and tab-close layout updates; an incidental refresh
    // after opening the Glance would mask the stale-container regression.
    await new Promise((resolve) => {
      // eslint-disable-next-line mozilla/no-arbitrary-setTimeout
      win.setTimeout(resolve, 1000);
    });

    await win.gZenGlanceManager.openGlance({
      url: "about:robots",
      clientX: 0,
      clientY: 0,
      width: 0,
      height: 0,
      triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal(),
    });
    Assert.ok(
      browser.selectedTab.hasAttribute("zen-glance-tab"),
      "A Glance opened from the pinned tab",
    );
    await TestUtils.waitForCondition(
      () => !browser.selectedBrowser.webProgress.isLoadingDocument,
      "The Glance page has loaded",
    );
    // Let the queued container update run before checking the final layout.
    await new Promise((resolve) => {
      win.requestAnimationFrame(() => win.requestAnimationFrame(resolve));
    });
    Assert.ok(
      pins.hasAttribute("hide-separator"),
      "A Glance alone keeps the normal tab area empty",
    );

    const normalTab = BrowserTestUtils.addTab(browser, "about:blank");
    await TestUtils.waitForCondition(
      () => !pins.hasAttribute("hide-separator"),
      "A real unpinned tab still shows the separator",
    );
    await BrowserTestUtils.removeTab(normalTab);
    await TestUtils.waitForCondition(
      () => pins.hasAttribute("hide-separator"),
      "Closing the real tab hides the separator while the Glance remains",
    );
  } finally {
    await BrowserTestUtils.closeWindow(win);
    await SpecialPowers.popPrefEnv();
  }
});
