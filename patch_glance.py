import pathlib,zipfile
root=pathlib.Path('/workspace/work/browser-omni')
p=root/'chrome/browser/content/browser/zen-components/ZenGlanceManager.mjs'
s=p.read_text();old='    currentTab.setAttribute("glance-id", glanceId);';new=old+'\n\n    // TabOpen counted this tab before it moved out of the normal tab list.\n    gZenWorkspaces.updateTabsContainers();'
assert s.count(old)==1 and 'TabOpen counted this tab' not in s
assert new in pathlib.Path('/workspace/work/zen-16611/src/zen/glance/ZenGlanceManager.mjs').read_text()
p.write_text(s.replace(old,new))
p=root/'chrome/browser/content/browser/tabbrowser/tabs.mjs';s=p.read_text();s=s.replace('(!event.target.classList.contains("zen-workspace-empty-space") &&\n          event.originalTarget !== gZenWorkspaces.activeScrollbox?.scrollbox) ||','!event.target.classList.contains("zen-workspace-empty-space") ||');p.write_text(s)
with zipfile.ZipFile('/workspace/work/zen/browser/omni.ja','w',zipfile.ZIP_DEFLATED) as z:
 for f in root.rglob('*'):
  if f.is_file():z.write(f,str(f.relative_to(root)))
print('Applied exact Glance fix, isolated from earlier changes')
