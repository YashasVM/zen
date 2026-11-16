import json,pathlib,sys,time
from marionette_driver.marionette import Marionette
out=pathlib.Path('/workspace/work/evidence-16482');out.mkdir(exist_ok=True)
label=sys.argv[1]
m=Marionette(bin='/workspace/work/zen/zen',headless=True,prefs={'zen.welcome-screen.seen':True,'zen.urlbar.replace-newtab':True,'zen.urlbar.open-on-startup':False})
try:
 m.start_session();m.set_context('chrome');m.timeout.script=30
 m.execute_async_script('const done=arguments[arguments.length-1];gZenWorkspaces.promiseInitialized.then(()=>done(true));')
 m.execute_script('window.resizeTo(1100,700); for(let i=0;i<30;i++)gBrowser.addTrustedTab("about:blank"); gBrowser.selectedTab=gBrowser.tabs.at(-1);')
 time.sleep(1)
 pos=m.execute_script('const s=gZenWorkspaces.activeScrollbox; s.scrollbox.scrollTop=s.scrollbox.scrollHeight; const r=s.scrollbox.getBoundingClientRect(); const x=r.x+r.width/2,y=r.bottom-30; return {x,y,overflowing:s.overflowing,scrollHeight:s.scrollbox.scrollHeight,clientHeight:s.scrollbox.clientHeight,target:s.shadowRoot.elementFromPoint(x,y)?.localName};')
 time.sleep(.3)
 m.execute_script('window.doubleClickLog=[]; gBrowser.tabContainer.addEventListener("dblclick",e=>window.doubleClickLog.push({target:e.target.localName,original:e.originalTarget.localName,shadowScrollbox:e.originalTarget===gZenWorkspaces.activeScrollbox.scrollbox}),{capture:true});')
 actions=[{'type':'pointerMove','duration':0,'origin':'viewport','x':round(pos['x']),'y':round(pos['y'])}]
 for i in range(2):actions += [{'type':'pointerDown','button':0},{'type':'pointerUp','button':0},{'type':'pause','duration':50}]
 m._send_message('WebDriver:PerformActions',{'actions':[{'type':'pointer','id':'mouse','parameters':{'pointerType':'mouse'},'actions':actions}]})
 time.sleep(.5)
 result=m.execute_script('return {newtab:gURLBar.hasAttribute("zen-newtab"),events:window.doubleClickLog};')
 result['geometry']=pos
 (out/(label+'.png')).write_bytes(m.screenshot(format='binary'))
 (out/(label+'.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
finally:m.quit();m.cleanup()
