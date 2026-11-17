PS C:\Users\Admin\Documents\caseloop> Get-ChildItem -Recurse -Filter "*.ts*" | Select-String "fetch"

frontend\node_modules\@types\react\experimental.d.ts:48:         * In 
other words, the tree is CPU bound and not I/O bound (e.g. due to 
fetching data).
frontend\node_modules\@types\react\experimental.d.ts:100:     * When 
multiple components need to fetch data, this data may arrive in an 
unpredictable order.
frontend\node_modules\@types\react\index.d.ts:2109:     * based on user 
input and something that needs to wait for a data fetch.
frontend\node_modules\@types\react\index.d.ts:2122:     * data fetching 
updates until subsequent renders so that more crucial updates can be
frontend\node_modules\@types\react\index.d.ts:3274:        
fetchPriority?: "high" | "low" | "auto" | undefined;
frontend\node_modules\@types\react\index.d.ts:3439:        
fetchPriority?: "high" | "low" | "auto" | undefined;
frontend\node_modules\@types\react\ts5.0\experimental.d.ts:48:         
* In other words, the tree is CPU bound and not I/O bound (e.g. due to 
fetching data).
frontend\node_modules\@types\react\ts5.0\experimental.d.ts:100:     * 
When multiple components need to fetch data, this data may arrive in an 
unpredictable order.
frontend\node_modules\@types\react\ts5.0\index.d.ts:2110:     * based 
on user input and something that needs to wait for a data fetch.
frontend\node_modules\@types\react\ts5.0\index.d.ts:2123:     * data 
fetching updates until subsequent renders so that more crucial updates 
can be
frontend\node_modules\@types\react\ts5.0\index.d.ts:3275:        
fetchPriority?: "high" | "low" | "auto" | undefined;
frontend\node_modules\@types\react\ts5.0\index.d.ts:3440:        
fetchPriority?: "high" | "low" | "auto" | undefined;
frontend\node_modules\@types\react-dom\canary.d.ts:37:    function 
prefetchDNS(href: string): void;
frontend\node_modules\@types\react-dom\canary.d.ts:44:        // since 
the spec has a notion of a dedicated type: https://html.spec.whatwg.org/
multipage/urls-and-fetching.html#cors-settings-attribute
frontend\node_modules\@types\react-dom\canary.d.ts:53:        | "fetch"
frontend\node_modules\@types\react-dom\canary.d.ts:65:        
fetchPriority?: "high" | "low" | "auto" | undefined;
frontend\node_modules\@types\react-dom\canary.d.ts:94:        
fetchPriority?: "high" | "low" | "auto" | undefined;
frontend\node_modules\csstype\index.d.ts:19842:  | "[fetchpriority]"
frontend\node_modules\csstype\index.d.ts:20023:  | "[fetchpriority]"
frontend\node_modules\typescript\lib\lib.dom.d.ts:2048:    /** A 
cryptographic hash of the resource to be fetched by request. Sets 
request's integrity. */
frontend\node_modules\typescript\lib\lib.dom.d.ts:2742: * The 
**`AbortSignal`** interface represents a signal object that allows you 
to communicate with an asynchronous operation (such as a fetch request) 
and abort it if required via an AbortController object.
frontend\node_modules\typescript\lib\lib.dom.d.ts:7498:     * The 
**`put()`** method of the Often, you will just want to Window/fetch one 
or more requests, then add the result straight to your cache.
frontend\node_modules\typescript\lib\lib.dom.d.ts:12215: * The 
**`FormData`** interface provides a way to construct a set of key/value 
pairs representing form fields and their values, which can be sent 
using the Window/fetch, XMLHttpRequest.send() or navigator.sendBeacon() 
methods.
frontend\node_modules\typescript\lib\lib.dom.d.ts:14567:     * The 
**`fetchPriority`** property of the HTMLImageElement interface 
represents a hint to the browser indicating how it should prioritize 
fetching a particular image relative to other images.
frontend\node_modules\typescript\lib\lib.dom.d.ts:14569:     * [MDN Refe
rence](https://developer.mozilla.org/docs/Web/API/HTMLImageElement/fetch
Priority)
frontend\node_modules\typescript\lib\lib.dom.d.ts:14571:    
fetchPriority: "high" | "low" | "auto";
frontend\node_modules\typescript\lib\lib.dom.d.ts:15147:     * The 
**`blocking`** property of the HTMLLinkElement interface is a string 
indicating that certain operations should be blocked on the fetching of 
an external resource.
frontend\node_modules\typescript\lib\lib.dom.d.ts:15168:     * The 
**`fetchPriority`** property of the HTMLLinkElement interface 
represents a hint to the browser indicating how it should prioritize 
fetching a particular resource relative to other resources of the same 
type.
frontend\node_modules\typescript\lib\lib.dom.d.ts:15170:     * [MDN Refe
rence](https://developer.mozilla.org/docs/Web/API/HTMLLinkElement/fetchP
riority)
frontend\node_modules\typescript\lib\lib.dom.d.ts:15172:    
fetchPriority: "high" | "low" | "auto";
frontend\node_modules\typescript\lib\lib.dom.d.ts:15198:     * The 
**`integrity`** property of the HTMLLinkElement interface is a string 
containing inline metadata that a browser can use to verify that a 
fetched resource has been delivered without unexpected manipulation.
frontend\node_modules\typescript\lib\lib.dom.d.ts:15433:     * The 
**`HTMLMediaElement.networkState`** property indicates the current 
state of the fetching of media over the network.
frontend\node_modules\typescript\lib\lib.dom.d.ts:16333:     * The 
**`blocking`** property of the HTMLScriptElement interface is a string 
indicating that certain operations should be blocked on the fetching of 
the script.
frontend\node_modules\typescript\lib\lib.dom.d.ts:16356:     * The 
**`fetchPriority`** property of the HTMLScriptElement interface 
represents a hint to the browser indicating how it should prioritize 
fetching an external script relative to other external scripts.
frontend\node_modules\typescript\lib\lib.dom.d.ts:16358:     * [MDN Refe
rence](https://developer.mozilla.org/docs/Web/API/HTMLScriptElement/fetc
hPriority)
frontend\node_modules\typescript\lib\lib.dom.d.ts:16360:    
fetchPriority: "high" | "low" | "auto";
frontend\node_modules\typescript\lib\lib.dom.d.ts:16364:     * The 
**`integrity`** property of the HTMLScriptElement interface is a string 
that contains inline metadata that a browser can use to verify that a 
fetched resource has been delivered without unexpected manipulation.
frontend\node_modules\typescript\lib\lib.dom.d.ts:16376:     * The 
**`referrerPolicy`** property of the `referrerpolicy` of the script 
element, which defines how the referrer is set when fetching the script 
and any scripts it imports.
frontend\node_modules\typescript\lib\lib.dom.d.ts:16709:     * The 
**`blocking`** property of the HTMLStyleElement interface is a string 
indicating that certain operations should be blocked on the fetching of 
critical subresources.
frontend\node_modules\typescript\lib\lib.dom.d.ts:17757: * The 
**`Headers`** interface of the Fetch API allows you to perform various 
actions on HTTP request and response headers.
frontend\node_modules\typescript\lib\lib.dom.d.ts:21352:     * The 
**`setHeaderValue()`** method of the NavigationPreloadManager interface 
sets the value of the Service-Worker-Navigation-Preload header that 
will be sent with requests resulting from a Window/fetch operation made 
during service worker navigation preloading.
frontend\node_modules\typescript\lib\lib.dom.d.ts:23069:     * The 
legacy **`Performance.navigation`** read-only property returns a 
PerformanceNavigation object representing the type of navigation that 
occurs in the given browsing context, such as the number of 
redirections needed to fetch the resource.
frontend\node_modules\typescript\lib\lib.dom.d.ts:23514:     * The 
**`decodedBodySize`** read-only property returns the size (in octets) 
received from the fetch (HTTP or cache) of the message body after 
removing any applied content encoding (like gzip or Brotli).
frontend\node_modules\typescript\lib\lib.dom.d.ts:23532:     * The 
**`encodedBodySize`** read-only property represents the size (in 
octets) received from the fetch (HTTP or cache) of the payload body 
before removing any applied content encodings (like gzip or Brotli).
frontend\node_modules\typescript\lib\lib.dom.d.ts:23538:     * The 
**`fetchStart`** read-only property represents a DOMHighResTimeStamp 
immediately before the browser starts to fetch the resource.
frontend\node_modules\typescript\lib\lib.dom.d.ts:23540:     * [MDN Refe
rence](https://developer.mozilla.org/docs/Web/API/PerformanceResourceTim
ing/fetchStart)
frontend\node_modules\typescript\lib\lib.dom.d.ts:23542:    readonly 
fetchStart: DOMHighResTimeStamp;
frontend\node_modules\typescript\lib\lib.dom.d.ts:23550:     * The 
**`nextHopProtocol`** read-only property is a string representing the 
network protocol used to fetch the resource, as identified by the ALPN 
Protocol ID (RFC7301).
frontend\node_modules\typescript\lib\lib.dom.d.ts:23562:     * The 
**`redirectStart`** read-only property returns a DOMHighResTimeStamp 
representing the start time of the fetch which that initiates the 
redirect.
frontend\node_modules\typescript\lib\lib.dom.d.ts:23586:     * The 
**`responseStatus`** read-only property represents the HTTP response 
status code returned when fetching the resource.
frontend\node_modules\typescript\lib\lib.dom.d.ts:23604:     * The 
**`transferSize`** read-only property represents the size (in octets) 
of the fetched resource.
frontend\node_modules\typescript\lib\lib.dom.d.ts:23736:     * The 
legacy **`PerformanceTiming.fetchStart`** read-only property returns an 
`unsigned long long` representing the moment, in milliseconds since the 
UNIX epoch, the browser is ready to fetch the document using an HTTP 
request.
frontend\node_modules\typescript\lib\lib.dom.d.ts:23739:     * [MDN Refe
rence](https://developer.mozilla.org/docs/Web/API/PerformanceTiming/fetc
hStart)
frontend\node_modules\typescript\lib\lib.dom.d.ts:23741:    readonly 
fetchStart: number;
frontend\node_modules\typescript\lib\lib.dom.d.ts:24249:     * The 
**`response`** read-only property of the object which is sent from the 
authenticator to the user agent for the creation/fetching of 
credentials.
frontend\node_modules\typescript\lib\lib.dom.d.ts:25949: * The 
**`ReadableStreamDefaultReader`** interface of the Streams API 
represents a default reader that can be used to read stream data 
supplied from a network (such as a fetch request).
frontend\node_modules\typescript\lib\lib.dom.d.ts:26116: * The 
**`Request`** interface of the Fetch API represents a resource request.
frontend\node_modules\typescript\lib\lib.dom.d.ts:26312: * The 
**`Response`** interface of the Fetch API represents the response to a 
request.
frontend\node_modules\typescript\lib\lib.dom.d.ts:36916:    /** [MDN 
Reference](https://developer.mozilla.org/docs/Web/API/Window/fetch) */
frontend\node_modules\typescript\lib\lib.dom.d.ts:36917:    
fetch(input: RequestInfo | URL, init?: RequestInit): Promise<Response>;
frontend\node_modules\typescript\lib\lib.dom.d.ts:39141:/** [MDN 
Reference](https://developer.mozilla.org/docs/Web/API/Window/fetch) */
frontend\node_modules\typescript\lib\lib.dom.d.ts:39142:declare 
function fetch(input: RequestInfo | URL, init?: RequestInit): 
Promise<Response>;
frontend\node_modules\typescript\lib\lib.es2020.bigint.d.ts:730:     * 
no alignment constraint; multi-byte values may be fetched from any 
offset.
frontend\node_modules\typescript\lib\lib.es2020.bigint.d.ts:738:     * 
no alignment constraint; multi-byte values may be fetched from any 
offset.
frontend\node_modules\typescript\lib\lib.es5.d.ts:1752:     * no 
alignment constraint; multi-byte values may be fetched from any offset.
frontend\node_modules\typescript\lib\lib.es5.d.ts:1760:     * no 
alignment constraint; multi-byte values may be fetched from any offset.
frontend\node_modules\typescript\lib\lib.es5.d.ts:1768:     * no 
alignment constraint; multi-byte values may be fetched from any offset.
frontend\node_modules\typescript\lib\lib.es5.d.ts:1775:     * no 
alignment constraint; multi-byte values may be fetched from any offset.
frontend\node_modules\typescript\lib\lib.es5.d.ts:1782:     * no 
alignment constraint; multi-byte values may be fetched from any offset.
frontend\node_modules\typescript\lib\lib.es5.d.ts:1790:     * no 
alignment constraint; multi-byte values may be fetched from any offset.
frontend\node_modules\typescript\lib\lib.es5.d.ts:1797:     * no 
alignment constraint; multi-byte values may be fetched from any offset.
frontend\node_modules\typescript\lib\lib.es5.d.ts:1805:     * no 
alignment constraint; multi-byte values may be fetched from any offset.
frontend\node_modules\typescript\lib\lib.esnext.float16.d.ts:432:     * 
no alignment constraint; multi-byte values may be fetched from any 
offset.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:325:interface 
FetchEventInit extends ExtendableEventInit {
frontend\node_modules\typescript\lib\lib.webworker.d.ts:749:    /** A 
cryptographic hash of the resource to be fetched by request. Sets 
request's integrity. */
frontend\node_modules\typescript\lib\lib.webworker.d.ts:1126: * The 
**`AbortSignal`** interface represents a signal object that allows you 
to communicate with an asynchronous operation (such as a fetch request) 
and abort it if required via an AbortController object.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:2215:     * The 
**`put()`** method of the Often, you will just want to Window/fetch one 
or more requests, then add the result straight to your cache.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4121: * This is 
the event type for `fetch` events dispatched on the 
ServiceWorkerGlobalScope.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4123: * [MDN 
Reference](https://developer.mozilla.org/docs/Web/API/FetchEvent)
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4125:interface 
FetchEvent extends ExtendableEvent {
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4129:     * 
[MDN Reference](https://developer.mozilla.org/docs/Web/API/FetchEvent/cl
ientId)
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4133:     * The 
**`handled`** property of the FetchEvent interface returns a promise 
indicating if the event has been handled by the fetch algorithm or not.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4135:     * 
[MDN Reference](https://developer.mozilla.org/docs/Web/API/FetchEvent/ha
ndled)
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4139:     * The 
**`preloadResponse`** read-only property of the FetchEvent interface 
returns a Promise that resolves to the navigation preload Response if 
navigation preload was triggered, or `undefined` otherwise.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4141:     * 
[MDN Reference](https://developer.mozilla.org/docs/Web/API/FetchEvent/pr
eloadResponse)
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4147:     * 
[MDN Reference](https://developer.mozilla.org/docs/Web/API/FetchEvent/re
quest)
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4153:     * 
[MDN Reference](https://developer.mozilla.org/docs/Web/API/FetchEvent/re
sultingClientId)
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4159:     * 
[MDN Reference](https://developer.mozilla.org/docs/Web/API/FetchEvent/re
spondWith)
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4164:declare 
var FetchEvent: {
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4165:    
prototype: FetchEvent;
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4166:    
new(type: string, eventInitDict: FetchEventInit): FetchEvent;
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4713: * The 
**`FormData`** interface provides a way to construct a set of key/value 
pairs representing form fields and their values, which can be sent 
using the Window/fetch, XMLHttpRequest.send() or navigator.sendBeacon() 
methods.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:4789: * The 
**`Headers`** interface of the Fetch API allows you to perform various 
actions on HTTP request and response headers.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:6004:     * The 
**`setHeaderValue()`** method of the NavigationPreloadManager interface 
sets the value of the Service-Worker-Navigation-Preload header that 
will be sent with requests resulting from a Window/fetch operation made 
during service worker navigation preloading.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:6733:     * The 
**`decodedBodySize`** read-only property returns the size (in octets) 
received from the fetch (HTTP or cache) of the message body after 
removing any applied content encoding (like gzip or Brotli).
frontend\node_modules\typescript\lib\lib.webworker.d.ts:6751:     * The 
**`encodedBodySize`** read-only property represents the size (in 
octets) received from the fetch (HTTP or cache) of the payload body 
before removing any applied content encodings (like gzip or Brotli).
frontend\node_modules\typescript\lib\lib.webworker.d.ts:6757:     * The 
**`fetchStart`** read-only property represents a DOMHighResTimeStamp 
immediately before the browser starts to fetch the resource.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:6759:     * 
[MDN Reference](https://developer.mozilla.org/docs/Web/API/PerformanceRe
sourceTiming/fetchStart)
frontend\node_modules\typescript\lib\lib.webworker.d.ts:6761:    
readonly fetchStart: DOMHighResTimeStamp;
frontend\node_modules\typescript\lib\lib.webworker.d.ts:6769:     * The 
**`nextHopProtocol`** read-only property is a string representing the 
network protocol used to fetch the resource, as identified by the ALPN 
Protocol ID (RFC7301).
frontend\node_modules\typescript\lib\lib.webworker.d.ts:6781:     * The 
**`redirectStart`** read-only property returns a DOMHighResTimeStamp 
representing the start time of the fetch which that initiates the 
redirect.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:6805:     * The 
**`responseStatus`** read-only property represents the HTTP response 
status code returned when fetching the resource.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:6823:     * The 
**`transferSize`** read-only property represents the size (in octets) 
of the fetched resource.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:7615: * The 
**`ReadableStreamDefaultReader`** interface of the Streams API 
represents a default reader that can be used to read stream data 
supplied from a network (such as a fetch request).
frontend\node_modules\typescript\lib\lib.webworker.d.ts:7729: * The 
**`Request`** interface of the Fetch API represents a resource request.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:7826: * The 
**`Response`** interface of the Fetch API represents the response to a 
request.
frontend\node_modules\typescript\lib\lib.webworker.d.ts:8101:    
"fetch": FetchEvent;
frontend\node_modules\typescript\lib\lib.webworker.d.ts:8134:    /** 
[MDN Reference](https://developer.mozilla.org/docs/Web/API/ServiceWorker
GlobalScope/fetch_event) */
frontend\node_modules\typescript\lib\lib.webworker.d.ts:8135:    
onfetch: ((this: ServiceWorkerGlobalScope, ev: FetchEvent) => any) | 
null;
frontend\node_modules\typescript\lib\lib.webworker.d.ts:12002:    /** 
[MDN 
Reference](https://developer.mozilla.org/docs/Web/API/Window/fetch) */
frontend\node_modules\typescript\lib\lib.webworker.d.ts:12003:    
fetch(input: RequestInfo | URL, init?: RequestInit): Promise<Response>;
frontend\node_modules\typescript\lib\lib.webworker.d.ts:12988:/** [MDN 
Reference](https://developer.mozilla.org/docs/Web/API/Window/fetch) */
frontend\node_modules\typescript\lib\lib.webworker.d.ts:12989:declare 
function fetch(input: RequestInfo | URL, init?: RequestInit): 
Promise<Response>;
frontend\node_modules\typescript\lib\typescript.d.ts:9537:     * @param 
file File to fetch the resolution mode within
frontend\node_modules\vite\dist\node\index.d.ts:18:import { F as 
FetchResult, H as HMRLogger } from './types.d-aGj9QkWt.js';
frontend\node_modules\vite\dist\node\index.d.ts:19:export { a as 
FetchFunction } from './types.d-aGj9QkWt.js';
frontend\node_modules\vite\dist\node\index.d.ts:1795:     * Fetch 
information about the module for Vite SSR runtime.
frontend\node_modules\vite\dist\node\index.d.ts:1798:    
ssrFetchModule(id: string, importer?: string): Promise<FetchResult>;
frontend\node_modules\vite\dist\node\index.d.ts:3509:interface 
FetchModuleOptions {
frontend\node_modules\vite\dist\node\index.d.ts:3514: * Fetch module 
information for Vite runtime.
frontend\node_modules\vite\dist\node\index.d.ts:3517:declare function 
fetchModule(server: ViteDevServer, url: string, importer?: string, 
options?: FetchModuleOptions): Promise<FetchResult>;
frontend\node_modules\vite\dist\node\index.d.ts:3594:interface 
MainThreadRuntimeOptions extends Omit<ViteRuntimeOptions, 'root' | 
'fetchModule' | 'hmr'> {
frontend\node_modules\vite\dist\node\index.d.ts:3627:export { type 
Alias, type AliasOptions, type AnymatchFn, type AnymatchPattern, type 
AppType, type AwaitWriteFinishOptions, type BindCLIShortcutsOptions, 
type BuildOptions, type CLIShortcut, type CSSModulesOptions, type 
CSSOptions, type CommonServerOptions, type ConfigEnv, Connect, type 
CorsOptions, type CorsOrigin, type DepOptimizationConfig, type 
DepOptimizationMetadata, type DepOptimizationOptions, type 
ESBuildOptions, type ESBuildTransformResult, type ExperimentalOptions, 
type ExportsData, FSWatcher, type FetchModuleOptions, type 
FileSystemServeOptions, type FilterPattern, type HMRBroadcaster, type 
HMRBroadcasterClient, type HMRChannel, type HTMLOptions, type 
HmrContext, type HmrOptions, type HookHandler, type HtmlTagDescriptor, 
HttpProxy, type HttpServer, type IndexHtmlTransform, type 
IndexHtmlTransformContext, type IndexHtmlTransformHook, type 
IndexHtmlTransformResult, type InlineConfig, type 
InternalResolveOptions, type JsonOptions, type LegacyOptions, type 
LibraryFormats, type LibraryOptions, type LightningCSSOptions, type 
LogErrorOptions, type LogLevel, type LogOptions, type LogType, type 
Logger, type LoggerOptions, type MainThreadRuntimeOptions, type 
Manifest, type ManifestChunk, type MapToFunction, type AnymatchMatcher 
as Matcher, ModuleGraph, ModuleNode, type ModulePreloadOptions, type 
OptimizedDepInfo, type Plugin, PluginContainer, type PluginHookUtils, 
type PluginOption, type PreprocessCSSResult, type PreviewOptions, type 
PreviewServer, type PreviewServerHook, type ProxyOptions, type 
RenderBuiltAssetUrl, type ResolveFn, type 
ResolveModulePreloadDependenciesFn, type ResolveOptions, type 
ResolvedBuildOptions, type ResolvedCSSOptions, type ResolvedConfig, 
type ResolvedModulePreloadOptions, type ResolvedPreviewOptions, type 
ResolvedSSROptions, type ResolvedServerOptions, type 
ResolvedServerUrls, type ResolvedUrl, type ResolvedWorkerOptions, type 
ResolverFunction, type ResolverObject, type RollupCommonJSOptions, type 
RollupDynamicImportVarsOptions, type SSROptions, type SSRTarget, type 
SendOptions, type ServerHMRChannel, ServerHMRConnector, type 
ServerHook, type ServerOptions, SplitVendorChunkCache, type 
SsrDepOptimizationOptions, Terser, type TerserOptions, type 
TransformOptions, type TransformResult, type UserConfig, type 
UserConfigExport, type UserConfigFn, type UserConfigFnObject, type 
UserConfigFnPromise, type ViteDevServer, type WatchOptions, WebSocket, 
WebSocketAlias, type WebSocketClient, type WebSocketCustomListener, 
WebSocketServer, build, buildErrorMessage, createFilter, createLogger, 
createServer, createViteRuntime, defineConfig, fetchModule, 
formatPostcssSourceMap, isCSSRequest, isFileLoadingAllowed, 
isFileServingAllowed, loadConfigFromFile, loadEnv, mergeAlias, 
mergeConfig, normalizePath, optimizeDeps, preprocessCSS, preview, 
resolveConfig, resolveEnvPrefix, rollupVersion, searchForWorkspaceRoot, 
send, sortUserPlugins, splitVendorChunk, splitVendorChunkPlugin, 
transformWithEsbuild, VERSION as version };
frontend\node_modules\vite\dist\node\runtime.d.ts:2:export { a as 
FetchFunction, F as FetchResult, e as HMRConnection, H as HMRLogger, g 
as HMRRuntimeConnection, f as ModuleCache, S as SSRImportMetadata, h as 
ViteRuntimeImportMeta, s as ssrDynamicImportKey, i as ssrExportAllKey, 
j as ssrImportKey, k as ssrImportMetaKey, l as ssrModuleExportsKey } 
from './types.d-aGj9QkWt.js';
frontend\node_modules\vite\dist\node\runtime.d.ts:55:    protected 
directRequest(id: string, fetchResult: ResolvedResult, _callstack: 
string[]): Promise<any>;
frontend\node_modules\vite\dist\node\types.d-aGj9QkWt.d.ts:58:    
private fetchUpdate;
frontend\node_modules\vite\dist\node\types.d-aGj9QkWt.d.ts:179:     * 
@param id ID that was used to fetch the module
frontend\node_modules\vite\dist\node\types.d-aGj9QkWt.d.ts:193:    
meta?: FetchResult;
frontend\node_modules\vite\dist\node\types.d-aGj9QkWt.d.ts:200:type 
FetchResult = ExternalFetchResult | ViteFetchResult;
frontend\node_modules\vite\dist\node\types.d-aGj9QkWt.d.ts:201:interface
 ExternalFetchResult {
frontend\node_modules\vite\dist\node\types.d-aGj9QkWt.d.ts:214:interface
 ViteFetchResult {
frontend\node_modules\vite\dist\node\types.d-aGj9QkWt.d.ts:226:type 
ResolvedResult = (ExternalFetchResult | ViteFetchResult) & {
frontend\node_modules\vite\dist\node\types.d-aGj9QkWt.d.ts:232:type 
FetchFunction = (id: string, importer?: string) => Promise<FetchResult>;
frontend\node_modules\vite\dist\node\types.d-aGj9QkWt.d.ts:240:     * 
For SSR, Vite exposes `server.ssrFetchModule` function that you can use 
here.
frontend\node_modules\vite\dist\node\types.d-aGj9QkWt.d.ts:241:     * 
For other runtime use cases, Vite also exposes `fetchModule` from its 
main entry point.
frontend\node_modules\vite\dist\node\types.d-aGj9QkWt.d.ts:243:    
fetchModule: FetchFunction;
frontend\node_modules\vite\dist\node\types.d-aGj9QkWt.d.ts:281:export { 
type FetchResult as F, type HMRLogger as H, ModuleCacheMap as M, type 
ResolvedResult as R, type SSRImportMetadata as S, type 
ViteRuntimeOptions as V, type FetchFunction as a, type ViteModuleRunner 
as b, HMRClient as c, type ViteRuntimeModuleContext as d, type 
HMRConnection as e, type ModuleCache as f, type HMRRuntimeConnection as 
g, type ViteRuntimeImportMeta as h, ssrExportAllKey as i, ssrImportKey 
as j, ssrImportMetaKey as k, ssrModuleExportsKey as l, 
ssrDynamicImportKey as s };
frontend\src\App.tsx:2:import { fetchResponses, createResponse, 
checkBackendHealth, ResponseItem } from './services/api';
frontend\src\App.tsx:28:      const data = await fetchResponses();
frontend\src\services\api.ts:26:export async function fetchResponses(): 
Promise<ResponseItem[]> {
frontend\src\services\api.ts:27:  const res = await 
fetch(`${API_BASE_URL}/responses/`);
frontend\src\services\api.ts:28:  if (!res.ok) throw new Error("Failed 
to fetch responses from local backend.");
frontend\src\services\api.ts:33:  const res = await 
fetch(`${API_BASE_URL}/responses/?coordinator_id=1`, {
frontend\src\services\api.ts:46:  const res = await 
fetch("http://127.0.0.1:8000/");