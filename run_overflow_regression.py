import json,pathlib,sys
from marionette_driver.marionette import Marionette
m=Marionette(bin='/workspace/work/zen/zen',headless=True,prefs={'zen.welcome-screen.seen':True,'zen.urlbar.open-on-startup':False,'zen.testing.enabled':True,'zen.urlbar.replace-newtab':False})
source=pathlib.Path('/workspace/work/zen-16482/src/zen/tests/spaces/browser_double_click_newtab.js').read_text(); source=source[source.index('add_task(async function test_double_click_overflow'):]
shim='''
const done=arguments[arguments.length-1];
const tasks=[], checks=[], saved=[];
const add_task=f=>tasks.push(f);
const Assert={ok(v,msg){checks.push({pass:!!v,message:msg});if(!v)throw Error(msg);},equal(a,b,msg){this.ok(a===b,msg);}};
const TestUtils={async waitForCondition(f,msg){for(let i=0;i<150;i++){if(f())return;await new Promise(r=>setTimeout(r,100));}throw Error(msg);}};
const SpecialPowers={async pushPrefEnv({set}){for(const [key,val] of set){const had=Services.prefs.prefHasUserValue(key);const type=Services.prefs.getPrefType(key);let old=type===128?Services.prefs.getBoolPref(key):type===64?Services.prefs.getIntPref(key):type===32?Services.prefs.getStringPref(key):null;saved.push([key,had,old]);typeof val==='boolean'?Services.prefs.setBoolPref(key,val):Services.prefs.setStringPref(key,val);}},async popPrefEnv(){for(const [key,had,val] of saved.reverse()){if(!had)Services.prefs.clearUserPref(key);else if(typeof val==='boolean')Services.prefs.setBoolPref(key,val);else if(typeof val==='number')Services.prefs.setIntPref(key,val);else Services.prefs.setStringPref(key,val);}}};
const EventUtils={synthesizeMouseAtPoint(x,y,opts,win){win.synthesizeMouseEvent('mousedown',x,y,{button:0,clickCount:opts.clickCount},{});win.synthesizeMouseEvent('mouseup',x,y,{button:0,clickCount:opts.clickCount},{});}};
const BrowserTestUtils={addTab(g,url,opts){return g.addTrustedTab(url,opts);},removeTab(t){gBrowser.removeTab(t,{animate:false});},waitForEvent(el,name){return new Promise(r=>el.addEventListener(name,r,{once:true}));},async withNewTab(url,fn){const t=gBrowser.addTrustedTab(url);gBrowser.selectedTab=t;try{await TestUtils.waitForCondition(()=>t.linkedBrowser.currentURI.spec===url&&!t.linkedBrowser.webProgress.isLoadingDocument,'Test page loads');await fn();}finally{gBrowser.removeTab(t,{animate:false});}}};
'''
try:
 m.start_session();m.set_context('chrome');m.timeout.script=45
 m.execute_async_script('const done=arguments[arguments.length-1];gZenWorkspaces.promiseInitialized.then(()=>done(true));')
 result=m.execute_async_script(shim+'\n'+source+'\n(async()=>{try{for(const task of tasks)await task();done({pass:true,checks});}catch(e){done({pass:false,error:String(e),checks});}})();')
 print(json.dumps(result,indent=2))
 pathlib.Path('/workspace/work/evidence-16482/regression-'+sys.argv[1]+'.json').write_text(json.dumps(result,indent=2))
finally:
 m.quit();m.cleanup()
