import json,pathlib,time,sys
from marionette_driver.marionette import Marionette
out=pathlib.Path('/workspace/work/evidence-16611');out.mkdir(exist_ok=True)
m=Marionette(bin='/workspace/work/zen/zen',headless=True,prefs={'zen.welcome-screen.seen':True,'zen.urlbar.open-on-startup':False,'zen.window-sync.enabled':False,'zen.glance.enabled':True})
try:
 m.start_session();m.set_context('chrome');m.timeout.script=30
 m.execute_async_script('const done=arguments[arguments.length-1];gZenWorkspaces.promiseInitialized.then(()=>done(true));')
 m.execute_script('window.resizeTo(1100,800);window.testPin=gBrowser.addTrustedTab("about:robots");gBrowser.pinTab(testPin);gBrowser.selectedTab=testPin;for(const t of [...gBrowser.tabs])if(t!==testPin&&!t.hasAttribute("zen-empty-tab"))gBrowser.removeTab(t,{animate:false});')
 time.sleep(1)
 state='''const w=gZenWorkspaces.activeWorkspaceElement;return {separatorHidden:w.pinnedTabsContainer.hasAttribute("hide-separator"),children:[...w.tabsContainer.children].map(t=>({tag:t.localName,empty:t.hasAttribute("zen-empty-tab"),glance:t.hasAttribute("zen-glance-tab"),hidden:t.hidden,closing:t.closing,id:t.id})),tabs:gBrowser.tabs.map(t=>({pinned:t.pinned,glance:t.hasAttribute("zen-glance-tab"),parent:t.parentNode.localName}))};'''
 results={'initial':m.execute_script(state)}
 m.execute_async_script('const done=arguments[arguments.length-1];gZenGlanceManager.openGlance({url:"about:robots",clientX:0,clientY:0,width:0,height:0,triggeringPrincipal:Services.scriptSecurityManager.getSystemPrincipal()}).then(()=>done(true));')
 time.sleep(1)
 results['glance']=m.execute_script(state)
 label=sys.argv[1];(out/(label+'.png')).write_bytes(m.screenshot(format='binary'));(out/(label+'.json')).write_text(json.dumps(results,indent=2));print(json.dumps(results),flush=True)
finally:m.quit();m.cleanup()
