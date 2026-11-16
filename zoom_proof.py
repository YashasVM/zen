import json,time,pathlib,sys
from marionette_driver.marionette import Marionette
out=pathlib.Path('/workspace/work/evidence');out.mkdir(parents=True,exist_ok=True)
label=sys.argv[1] if len(sys.argv)>1 else 'before'
m=Marionette(bin='/workspace/work/zen/zen',headless=True,prefs={'zen.welcome-screen.seen':True,'zen.urlbar.replace-newtab':True,'zen.urlbar.open-on-startup':False,'zen.view.use-single-toolbar':False,'browser.shell.checkDefaultBrowser':False})
try:
 m.start_session();m.set_context('chrome')
 m.execute_async_script('const done=arguments[arguments.length-1]; gZenWorkspaces.promiseInitialized.then(()=>done(true));')
 m.execute_script('window.resizeTo(1100,800); const tab=gBrowser.addTrustedTab("about:robots"); gBrowser.selectedTab=tab;')
 time.sleep(2)
 m.execute_script('FullZoom.setZoom(1.5);')
 time.sleep(1)
 def state(): return m.execute_script('const b=document.getElementById("urlbar-zoom-button");return {newtab:gURLBar.hasAttribute("zen-newtab"),zoom:ZoomManager.zoom,hidden:b.hidden,display:getComputedStyle(b).display,visible:!!b.getClientRects().length,label:b.getAttribute("label"),tab:gBrowser.selectedBrowser.currentURI.spec};')
 results={'normal':state()}
 m.execute_script('BrowserCommands.openTab();');time.sleep(1)
 results['newtab']=state()
 (out/(label+'.png')).write_bytes(m.screenshot(format='binary'))
 m.execute_script('gURLBar._zenHandleUrlbarClose?.(false);gURLBar.blur();');time.sleep(1)
 results['closed']=state()
 (out/(label+'.json')).write_text(json.dumps(results,indent=2))
 print(json.dumps(results),flush=True)
finally:m.quit()
