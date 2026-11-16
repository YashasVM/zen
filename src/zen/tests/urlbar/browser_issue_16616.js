/* Any copyright is dedicated to the Public Domain.
   https://creativecommons.org/publicdomain/zero/1.0/ */

"use strict";

add_task(async function test_newtab_hides_current_page_zoom() {
  await SpecialPowers.pushPrefEnv({
    set: [
      ["zen.urlbar.replace-newtab", true],
      ["zen.view.use-single-toolbar", false],
    ],
  });
  try {
    await BrowserTestUtils.withNewTab("https://example.com/", async () => {
      const button = document.getElementById("urlbar-zoom-button");
      const visible = () => !!button.getClientRects().length;
      try {
        FullZoom.setZoom(1.5);
        await TestUtils.waitForCondition(
          () => ZoomManager.zoom === 1.5 && visible(),
          "The current page's zoom indicator is visible",
        );

        Assert.ok(
          gZenUIManager.handleNewTab(false, false, "tab", true),
          "The new-tab dialog opens",
        );
        await TestUtils.waitForCondition(
          () => gURLBar.hasAttribute("zen-newtab"),
          "The URL bar is in new-tab mode",
        );
        Assert.ok(!visible(), "The new-tab dialog hides the old page's zoom");
        Assert.equal(
          ZoomManager.zoom,
          1.5,
          "Opening the dialog keeps page zoom",
        );

        gURLBar._zenHandleUrlbarClose(false);
        gURLBar.blur();
        await TestUtils.waitForCondition(
          () => !gURLBar.hasAttribute("zen-newtab") && visible(),
          "Closing the dialog restores the current page's zoom indicator",
        );
        Assert.equal(
          ZoomManager.zoom,
          1.5,
          "Closing the dialog keeps page zoom",
        );
      } finally {
        gURLBar._zenHandleUrlbarClose?.(false);
        gURLBar.blur();
        await FullZoom.reset();
      }
    });
  } finally {
    await SpecialPowers.popPrefEnv();
  }
});
