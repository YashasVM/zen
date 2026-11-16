import pathlib,json,sys
from marionette_driver.marionette import Marionette
source=pathlib.Path('/workspace/work/zen-16611/src/zen/tests/glance/browser_issue_16611.js').read_text()
m=Marionette(bin='/workspace/work/zen/zen',headless=True,prefs={'zen.welcome-screen.seen':True,'zen.urlbar.open-on-startup':False,'zen.testing.enabled':False})
shim='''
const done=arguments[arguments.length-1], tasks=[],checks=[],saved=[];
const add_task=f=>tasks.push(f);
const Assert={ok(v,msg){checks.push({pass:!!v,message:msg});if(!v)throw Error(msg);}};
const TestUtils={async waitForCondition(f,msg){for(let i=0;i<150;i++){if(f())return;await new Promise(r=>setTimeout(r,100));}throw Error(msg);}};
const SpecialPowers={async pushPrefEnv({set}){for(const [key,val]of set){const had=Services.prefs.prefHasUserValue(key),old=Services.prefs.getBoolPref(key,false);saved.push([key,had,old]);Services.prefs.setBoolPref(key,val);}},async popPrefEnv(){for(const[key,had,val]of saved.reverse())had?Services.prefs.setBoolPref(key,val):Services.prefs.clearUserPref(key);}};
const BrowserTestUtils={async openNewBrowserWindow(){const w=window.OpenBrowserWindow();await TestUtils.waitForCondition(()=>w.gBrowserInit?.delayedStartupFinished,'New window ready');return w;},async closeWindow(w){w.close();await TestUtils.waitForCondition(()=>w.closed,'Window closes');},addTab(g,url,opts){return g.addTrustedTab(url,opts);},removeTab(t){t.ownerDocument.defaultView.gBrowser.removeTab(t,{animate:false});}};
'''
try:
 m.start_session();m.set_context('chrome');m.timeout.script=45
 m.execute_async_script('const done=arguments[arguments.length-1];gZenWorkspaces.promiseInitialized.then(()=>done(true));')
 result=m.execute_async_script(shim+'\n'+source+'\n(async()=>{try{for(const task of tasks)await task();done({pass:true,checks});}catch(e){done({pass:false,error:String(e),checks});}})();')
 print(json.dumps(result,indent=2),flush=True)
 pathlib.Path('/workspace/work/evidence-16611/regression-'+sys.argv[1]+'.json').write_text(json.dumps(result,indent=2))
finally:m.quit();m.cleanup()
