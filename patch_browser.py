import zipfile,pathlib,shutil
root=pathlib.Path('/workspace/work/browser-omni')
p=root/'chrome/browser/content/browser/zen-styles/zen-omnibox.css'
s=p.read_text(); rule='''/* The new-tab dialog still uses the selected browser's URL bar, but its zoom
   level only applies to that existing page. */
#urlbar[zen-newtab] #urlbar-zoom-button {
  display: none !important;
}
'''
assert rule in pathlib.Path('/workspace/zen-browser/src/zen/common/styles/zen-omnibox.css').read_text()
assert '#urlbar[zen-newtab] #urlbar-zoom-button' not in s
p.write_text(s+'\n'+rule)
shutil.copy2('/workspace/work/zen/browser/omni.ja','/workspace/work/omni-before.ja')
with zipfile.ZipFile('/workspace/work/zen/browser/omni.ja','w',zipfile.ZIP_DEFLATED) as z:
 for f in root.rglob('*'):
  if f.is_file():z.write(f,str(f.relative_to(root)))
print('Applied the exact source CSS rule to Zen 1.24.2b for runtime validation')
