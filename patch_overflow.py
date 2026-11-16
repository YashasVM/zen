import pathlib,zipfile
root=pathlib.Path('/workspace/work/browser-omni')
p=root/'chrome/browser/content/browser/tabbrowser/tabs.mjs'
s=p.read_text();old='!event.target.classList.contains("zen-workspace-empty-space") ||';new='(!event.target.classList.contains("zen-workspace-empty-space") &&\n          event.originalTarget !== gZenWorkspaces.activeScrollbox?.scrollbox) ||'
assert s.count(old)==1
patch=pathlib.Path('/workspace/work/zen-16482/src/browser/components/tabbrowser/content/tabs-mjs.patch').read_text()
assert '+        '+new.replace('\n','\n+') in patch
p.write_text(s.replace(old,new))
# Start from the original release styles; issue 16482 is independent of 16616.
css=root/'chrome/browser/content/browser/zen-styles/zen-omnibox.css'
s=css.read_text();s=s[:s.index('\n/* The new-tab dialog still uses')];css.write_text(s)
with zipfile.ZipFile('/workspace/work/zen/browser/omni.ja','w',zipfile.ZIP_DEFLATED) as z:
 for f in root.rglob('*'):
  if f.is_file():z.write(f,str(f.relative_to(root)))
print('Applied exact changed condition from source patch')
