import json,pathlib,sys
from marionette_driver.marionette import Marionette
m=Marionette(bin='/workspace/work/zen/zen',headless=True,prefs={'zen.welcome-screen.seen':True,'zen.urlbar.open-on-startup':False,'zen.testing.enabled':True})
source=pathlib.Path('/workspace/zen-browser/src/zen/tests/urlbar/browser_issue_16616.js').read_text()
shim='''
const done=arguments[arguments.length-1];
const tasks=[], checks=[], saved=[];
const add_task=f=>tasks.push(f);
const Assert={ok(v,msg){checks.push({pass:!!v,message:msg});if(!v)throw Error(msg);},equal(a,b,msg){this.ok(a===b,msg);}};
const TestUtils={async waitForCondition(f,msg){for(let i=0;i<150;i++){if(f())return;await new Promise(r=>setTimeout(r,100));}throw Error(msg);}};
const SpecialPowers={async pushPrefEnv({set}){for(const [key,val] of set){const had=Services.prefs.prefHasUserValue(key);const type=Services.prefs.getPrefType(key);let old=type===128?Services.prefs.getBoolPref(key):type===64?Services.prefs.getIntPref(key):type===32?Services.prefs.getStringPref(key):null;saved.push([key,had,old]);typeof val==='boolean'?Services.prefs.setBoolPref(key,val):Services.prefs.setStringPref(key,val);}},async popPrefEnv(){for(const [key,had,val] of saved.reverse()){if(!had)Services.prefs.clearUserPref(key);else if(typeof val==='boolean')Services.prefs.setBoolPref(key,val);else if(typeof val==='number')Services.prefs.setIntPref(key,val);else Services.prefs.setStringPref(key,val);}}};
const BrowserTestUtils={async withNewTab(url,fn){const t=gBrowser.addTrustedTab(url);gBrowser.selectedTab=t;try{await TestUtils.waitForCondition(()=>t.linkedBrowser.currentURI.spec===url&&!t.linkedBrowser.webProgress.isLoadingDocument,'Test page loads');await fn();}finally{gBrowser.removeTab(t,{animate:false});}}};
'''
try:
 m.start_session();m.set_context('chrome');m.timeout.script=45
 m.execute_async_script('const done=arguments[arguments.length-1];gZenWorkspaces.promiseInitialized.then(()=>done(true));')
 result=m.execute_async_script(shim+'\n'+source+'\n(async()=>{try{for(const task of tasks)await task();done({pass:true,checks});}catch(e){done({pass:false,error:String(e),checks});}})();')
 print(json.dumps(result,indent=2))
 pathlib.Path('/workspace/work/evidence/regression-'+sys.argv[1]+'.json').write_text(json.dumps(result,indent=2))
finally:
 m.quit();m.cleanup()
