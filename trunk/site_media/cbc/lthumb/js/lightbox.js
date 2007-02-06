var Prototype = { Version: '1.4.0', ScriptFragment: '(?:<script.*?>)((\n|\r|.)*?)(?:<\/script>)', emptyFunction: function() {}, K: function(x) {return x} }
var Class = { create: function() { return function() { this.initialize.apply(this, arguments); } } }
var Abstract = new Object();
Object.extend = function(destination, source) { for (property in source) { destination[property] = source[property]; } return destination; }
Object.inspect = function(object) { try { if (object == undefined) return 'undefined'; if (object == null) return 'null'; return object.inspect ? object.inspect() : object.toString(); } catch (e) { if (e instanceof RangeError) return '...'; throw e; } }
Function.prototype.bind = function() { var __method = this, args = $A(arguments), object = args.shift(); return function() { return __method.apply(object, args.concat($A(arguments))); } }
Function.prototype.bindAsEventListener = function(object) { var __method = this; return function(event) { return __method.call(object, event || window.event); } }
Object.extend(Number.prototype, { toColorPart: function() { var digits = this.toString(16); if (this < 16) return '0' + digits; return digits; },
  succ: function() { return this + 1; },
  times: function(iterator) { $R(0, this, true).each(iterator); return this; } });
var Try = { these: function() { var returnValue; for (var i = 0; i < arguments.length; i++) { var lambda = arguments[i]; try { returnValue = lambda(); break; } catch (e) {} } return returnValue; } }
var PeriodicalExecuter = Class.create(); PeriodicalExecuter.prototype = { initialize: function(callback, frequency) { this.callback = callback; this.frequency = frequency; this.currentlyExecuting = false; this.registerCallback(); },
  registerCallback: function() { setInterval(this.onTimerEvent.bind(this), this.frequency * 1000); }, onTimerEvent: function() { if (!this.currentlyExecuting) { try { this.currentlyExecuting = true; this.callback(); } finally { this.currentlyExecuting = false; } } } }
function $() { var elements = new Array(); for (var i = 0; i < arguments.length; i++) { var element = arguments[i]; if (typeof element == 'string') element = document.getElementById(element); if (arguments.length == 1) return element; elements.push(element); } return elements; }
Object.extend(String.prototype, { stripTags: function() { return this.replace(/<\/?[^>]+>/gi, ''); },
  stripScripts: function() { return this.replace(new RegExp(Prototype.ScriptFragment, 'img'), ''); },
  extractScripts: function() { var matchAll = new RegExp(Prototype.ScriptFragment, 'img'); var matchOne = new RegExp(Prototype.ScriptFragment, 'im'); return (this.match(matchAll) || []).map(function(scriptTag) { return (scriptTag.match(matchOne) || ['', ''])[1]; }); },
  evalScripts: function() { return this.extractScripts().map(eval); },
  escapeHTML: function() { var div = document.createElement('div'); var text = document.createTextNode(this); div.appendChild(text); return div.innerHTML; },
  unescapeHTML: function() { var div = document.createElement('div'); div.innerHTML = this.stripTags(); return div.childNodes[0] ? div.childNodes[0].nodeValue : ''; },
  toQueryParams: function() { var pairs = this.match(/^\??(.*)$/)[1].split('&'); return pairs.inject({}, function(params, pairString) { var pair = pairString.split('='); params[pair[0]] = pair[1]; return params; }); },
  toArray: function() { return this.split(''); },
  camelize: function() { var oStringList = this.split('-'); if (oStringList.length == 1) return oStringList[0]; var camelizedString = this.indexOf('-') == 0 ? oStringList[0].charAt(0).toUpperCase() + oStringList[0].substring(1) : oStringList[0]; for (var i = 1, len = oStringList.length; i < len; i++) { var s = oStringList[i]; camelizedString += s.charAt(0).toUpperCase() + s.substring(1); } return camelizedString; },
  inspect: function() { return "'" + this.replace('\\', '\\\\').replace("'", '\\\'') + "'"; } });
String.prototype.parseQuery = String.prototype.toQueryParams;
var $break    = new Object();
var $continue = new Object();
var Enumerable = { each: function(iterator) { var index = 0; try { this._each(function(value) { try { iterator(value, index++); } catch (e) { if (e != $continue) throw e; } }); } catch (e) { if (e != $break) throw e; } },
  all: function(iterator) { var result = true; this.each(function(value, index) { result = result && !!(iterator || Prototype.K)(value, index); if (!result) throw $break; }); return result; },
  any: function(iterator) { var result = true; this.each(function(value, index) { if (result = !!(iterator || Prototype.K)(value, index)) throw $break; }); return result; },
  collect: function(iterator) { var results = []; this.each(function(value, index) { results.push(iterator(value, index)); }); return results; },
  detect: function (iterator) { var result; this.each(function(value, index) { if (iterator(value, index)) { result = value; throw $break; } }); return result; },
  findAll: function(iterator) { var results = []; this.each(function(value, index) { if (iterator(value, index)) results.push(value); }); return results; },
  grep: function(pattern, iterator) {
    var results = [];
    this.each(function(value, index) {
      var stringValue = value.toString();
      if (stringValue.match(pattern))
        results.push((iterator || Prototype.K)(value, index));
    })
    return results;
  },
  include: function(object) { var found = false; this.each(function(value) { if (value == object) { found = true; throw $break; } }); return found; },
  inject: function(memo, iterator) { this.each(function(value, index) { memo = iterator(memo, value, index); }); return memo; },
  invoke: function(method) { var args = $A(arguments).slice(1); return this.collect(function(value) { return value[method].apply(value, args); }); },
  max: function(iterator) { var result; this.each(function(value, index) { value = (iterator || Prototype.K)(value, index); if (value >= (result || value)) result = value; }); return result; },
  min: function(iterator) { var result; this.each(function(value, index) { value = (iterator || Prototype.K)(value, index); if (value <= (result || value)) result = value; }); return result; },
  partition: function(iterator) { var trues = [], falses = []; this.each(function(value, index) { ((iterator || Prototype.K)(value, index) ? trues : falses).push(value); }); return [trues, falses]; },
  pluck: function(property) { var results = []; this.each(function(value, index) { results.push(value[property]); }); return results; },
  reject: function(iterator) { var results = []; this.each(function(value, index) { if (!iterator(value, index)) results.push(value); }); return results; },
  sortBy: function(iterator) { return this.collect(function(value, index) { return {value: value, criteria: iterator(value, index)}; }).sort(function(left, right) { var a = left.criteria, b = right.criteria; return a < b ? -1 : a > b ? 1 : 0; }).pluck('value'); },
  toArray: function() { return this.collect(Prototype.K); },
  zip: function() { var iterator = Prototype.K, args = $A(arguments); if (typeof args.last() == 'function') iterator = args.pop(); var collections = [this].concat(args).map($A); return this.map(function(value, index) { iterator(value = collections.pluck(index)); return value; }); },
inspect: function() { return '#<Enumerable:' + this.toArray().inspect() + '>'; } }
Object.extend(Enumerable, { map:     Enumerable.collect, find:    Enumerable.detect, select:  Enumerable.findAll, member:  Enumerable.include, entries: Enumerable.toArray }); var $A = Array.from = function(iterable) { if (!iterable) return []; if (iterable.toArray) { return iterable.toArray(); } else { var results = []; for (var i = 0; i < iterable.length; i++) results.push(iterable[i]); return results; } }
Object.extend(Array.prototype, Enumerable);
Array.prototype._reverse = Array.prototype.reverse;
Object.extend(Array.prototype, { _each: function(iterator) { for (var i = 0; i < this.length; i++) iterator(this[i]); }, clear: function() { this.length = 0; return this; }, first: function() { return this[0]; }, last: function() { return this[this.length - 1]; }, compact: function() { return this.select(function(value) { return value != undefined || value != null; }); }, flatten: function() { return this.inject([], function(array, value) { return array.concat(value.constructor == Array ? value.flatten() : [value]); }); }, without: function() { var values = $A(arguments); return this.select(function(value) { return !values.include(value); }); }, indexOf: function(object) { for (var i = 0; i < this.length; i++) if (this[i] == object) return i; return -1; }, reverse: function(inline) { return (inline !== false ? this : this.toArray())._reverse(); }, shift: function() { var result = this[0]; for (var i = 0; i < this.length - 1; i++) this[i] = this[i + 1]; this.length--; return result; }, inspect: function() { return '[' + this.map(Object.inspect).join(', ') + ']'; } });
var Hash = { _each: function(iterator) { for (key in this) { var value = this[key]; if (typeof value == 'function') continue; var pair = [key, value]; pair.key = key; pair.value = value; iterator(pair); } },
  keys: function() { return this.pluck('key'); },
  values: function() { return this.pluck('value'); },
  merge: function(hash) { return $H(hash).inject($H(this), function(mergedHash, pair) { mergedHash[pair.key] = pair.value; return mergedHash; }); },
toQueryString: function() { return this.map(function(pair) { return pair.map(encodeURIComponent).join('='); }).join('&'); },
  inspect: function() { return '#<Hash:{' + this.map(function(pair) { return pair.map(Object.inspect).join(': '); }).join(', ') + '}>'; } }
function $H(object) { var hash = Object.extend({}, object || {}); Object.extend(hash, Enumerable); Object.extend(hash, Hash); return hash; }
ObjectRange = Class.create();
Object.extend(ObjectRange.prototype, Enumerable);
Object.extend(ObjectRange.prototype, { initialize: function(start, end, exclusive) { this.start = start; this.end = end; this.exclusive = exclusive; },
  _each: function(iterator) { var value = this.start; do { iterator(value); value = value.succ(); } while (this.include(value)); },
  include: function(value) { if (value < this.start) return false; if (this.exclusive) return value < this.end; return value <= this.end; } });
var $R = function(start, end, exclusive) { return new ObjectRange(start, end, exclusive); }
var Ajax = { getTransport: function() { return Try.these( function() {return new ActiveXObject('Msxml2.XMLHTTP')}, function() {return new ActiveXObject('Microsoft.XMLHTTP')}, function() {return new XMLHttpRequest()} ) || false; }, activeRequestCount: 0 }
Ajax.Responders = { responders: [], _each: function(iterator) { this.responders._each(iterator); }, register: function(responderToAdd) { if (!this.include(responderToAdd)) this.responders.push(responderToAdd); }, unregister: function(responderToRemove) { this.responders = this.responders.without(responderToRemove); }, dispatch: function(callback, request, transport, json) { this.each(function(responder) { if (responder[callback] && typeof responder[callback] == 'function') { try { responder[callback].apply(responder, [request, transport, json]); } catch (e) {} } }); } };
Object.extend(Ajax.Responders, Enumerable);
Ajax.Responders.register({ onCreate: function() { Ajax.activeRequestCount++; },
  onComplete: function() { Ajax.activeRequestCount--; } });
Ajax.Base = function() {};
Ajax.Base.prototype = {
  setOptions: function(options) {
    this.options = {
      method:       'post',
      asynchronous: true,
      parameters:   ''
    }
    Object.extend(this.options, options || {});
  },
  responseIsSuccess: function() {
    return this.transport.status == undefined
        || this.transport.status == 0
        || (this.transport.status >= 200 && this.transport.status < 300);
  },
  responseIsFailure: function() {
    return !this.responseIsSuccess();
  }
}
Ajax.Request = Class.create();
Ajax.Request.Events =
  ['Uninitialized', 'Loading', 'Loaded', 'Interactive', 'Complete'];
Ajax.Request.prototype = Object.extend(new Ajax.Base(), {
  initialize: function(url, options) {
    this.transport = Ajax.getTransport();
    this.setOptions(options);
    this.request(url);
  },
  request: function(url) { var parameters = this.options.parameters || ''; if (parameters.length > 0) parameters += '&_='; try { this.url = url; if (this.options.method == 'get' && parameters.length > 0) this.url += (this.url.match(/\?/) ? '&' : '?') + parameters; Ajax.Responders.dispatch('onCreate', this, this.transport); this.transport.open(this.options.method, this.url, this.options.asynchronous); if (this.options.asynchronous) { this.transport.onreadystatechange = this.onStateChange.bind(this); setTimeout((function() {this.respondToReadyState(1)}).bind(this), 10); } this.setRequestHeaders(); var body = this.options.postBody ? this.options.postBody : parameters; this.transport.send(this.options.method == 'post' ? body : null); } catch (e) { this.dispatchException(e); } }, setRequestHeaders: function() { var requestHeaders = ['X-Requested-With', 'XMLHttpRequest', 'X-Prototype-Version', Prototype.Version]; if (this.options.method == 'post') { requestHeaders.push('Content-type', 'application/x-www-form-urlencoded'); if (this.transport.overrideMimeType) requestHeaders.push('Connection', 'close'); } if (this.options.requestHeaders) requestHeaders.push.apply(requestHeaders, this.options.requestHeaders); for (var i = 0; i < requestHeaders.length; i += 2) this.transport.setRequestHeader(requestHeaders[i], requestHeaders[i+1]); }, onStateChange: function() { var readyState = this.transport.readyState; if (readyState != 1) this.respondToReadyState(this.transport.readyState); }, header: function(name) { try { return this.transport.getResponseHeader(name); } catch (e) {} }, evalJSON: function() { try { return eval(this.header('X-JSON')); } catch (e) {} }, evalResponse: function() { try { return eval(this.transport.responseText); } catch (e) { this.dispatchException(e); } }, respondToReadyState: function(readyState) { var event = Ajax.Request.Events[readyState]; var transport = this.transport, json = this.evalJSON(); if (event == 'Complete') { try { (this.options['on' + this.transport.status] || this.options['on' + (this.responseIsSuccess() ? 'Success' : 'Failure')] || Prototype.emptyFunction)(transport, json); } catch (e) { this.dispatchException(e); } if ((this.header('Content-type') || '').match(/^text\/javascript/i)) this.evalResponse(); } try { (this.options['on' + event] || Prototype.emptyFunction)(transport, json); Ajax.Responders.dispatch('on' + event, this, transport, json); } catch (e) { this.dispatchException(e); } /* Avoid memory leak in MSIE: clean up the oncomplete event handler */ if (event == 'Complete') this.transport.onreadystatechange = Prototype.emptyFunction; }, dispatchException: function(exception) { (this.options.onException || Prototype.emptyFunction)(this, exception); Ajax.Responders.dispatch('onException', this, exception); } });
Ajax.Updater = Class.create();
Object.extend(Object.extend(Ajax.Updater.prototype, Ajax.Request.prototype), {
  initialize: function(container, url, options) {
    this.containers = {
      success: container.success ? $(container.success) : $(container),
      failure: container.failure ? $(container.failure) :
        (container.success ? null : $(container))
    }
    this.transport = Ajax.getTransport();
    this.setOptions(options);
    var onComplete = this.options.onComplete || Prototype.emptyFunction;
    this.options.onComplete = (function(transport, object) {
      this.updateContent();
      onComplete(transport, object);
    }).bind(this);
    this.request(url);
  },
  updateContent: function() { var receiver = this.responseIsSuccess() ? this.containers.success : this.containers.failure; var response = this.transport.responseText; if (!this.options.evalScripts) response = response.stripScripts(); if (receiver) { if (this.options.insertion) { new this.options.insertion(receiver, response); } else { Element.update(receiver, response); } } if (this.responseIsSuccess()) { if (this.onComplete) setTimeout(this.onComplete.bind(this), 10); } }
});
Ajax.PeriodicalUpdater = Class.create();
Ajax.PeriodicalUpdater.prototype = Object.extend(new Ajax.Base(), { initialize: function(container, url, options) { this.setOptions(options); this.onComplete = this.options.onComplete; this.frequency = (this.options.frequency || 2); this.decay = (this.options.decay || 1); this.updater = {}; this.container = container; this.url = url; this.start(); }, start: function() { this.options.onComplete = this.updateComplete.bind(this); this.onTimerEvent(); }, stop: function() { this.updater.onComplete = undefined; clearTimeout(this.timer); (this.onComplete || Prototype.emptyFunction).apply(this, arguments); }, updateComplete: function(request) { if (this.options.decay) { this.decay = (request.responseText == this.lastText ? this.decay * this.options.decay : 1); this.lastText = request.responseText; } this.timer = setTimeout(this.onTimerEvent.bind(this), this.decay * this.frequency * 1000); }, onTimerEvent: function() { this.updater = new Ajax.Updater(this.container, this.url, this.options); } });
document.getElementsByClassName = function(className, parentElement) { var children = ($(parentElement) || document.body).getElementsByTagName('*'); return $A(children).inject([], function(elements, child) { if (child.className.match(new RegExp("(^|\\s)" + className + "(\\s|$)"))) elements.push(child); return elements; }); }

if (!window.Element) { var Element = new Object(); }
Object.extend(Element, { visible: function(element) { return $(element).style.display != 'none'; }, toggle: function() { for (var i = 0; i < arguments.length; i++) { var element = $(arguments[i]); Element[Element.visible(element) ? 'hide' : 'show'](element); } }, hide: function() { for (var i = 0; i < arguments.length; i++) { var element = $(arguments[i]); element.style.display = 'none'; } }, show: function() { for (var i = 0; i < arguments.length; i++) { var element = $(arguments[i]); element.style.display = ''; } }, remove: function(element) { element = $(element); element.parentNode.removeChild(element); }, update: function(element, html) { $(element).innerHTML = html.stripScripts(); setTimeout(function() {html.evalScripts()}, 10); }, getHeight: function(element) { element = $(element); return element.offsetHeight; }, classNames: function(element) { return new Element.ClassNames(element); }, hasClassName: function(element, className) { if (!(element = $(element))) return; return Element.classNames(element).include(className); }, addClassName: function(element, className) { if (!(element = $(element))) return; return Element.classNames(element).add(className); }, removeClassName: function(element, className) { if (!(element = $(element))) return; return Element.classNames(element).remove(className); }, cleanWhitespace: function(element) { element = $(element); for (var i = 0; i < element.childNodes.length; i++) { var node = element.childNodes[i]; if (node.nodeType == 3 && !/\S/.test(node.nodeValue)) Element.remove(node); } }, empty: function(element) { return $(element).innerHTML.match(/^\s*$/); }, scrollTo: function(element) { element = $(element); var x = element.x ? element.x : element.offsetLeft, y = element.y ? element.y : element.offsetTop; window.scrollTo(x, y); }, getStyle: function(element, style) { element = $(element); var value = element.style[style.camelize()]; if (!value) { if (document.defaultView && document.defaultView.getComputedStyle) { var css = document.defaultView.getComputedStyle(element, null); value = css ? css.getPropertyValue(style) : null; } else if (element.currentStyle) { value = element.currentStyle[style.camelize()]; } } if (window.opera && ['left', 'top', 'right', 'bottom'].include(style)) if (Element.getStyle(element, 'position') == 'static') value = 'auto'; return value == 'auto' ? null : value; }, setStyle: function(element, style) { element = $(element); for (name in style) element.style[name.camelize()] = style[name]; }, getDimensions: function(element) { element = $(element); if (Element.getStyle(element, 'display') != 'none') return {width: element.offsetWidth, height: element.offsetHeight}; var els = element.style; var originalVisibility = els.visibility; var originalPosition = els.position; els.visibility = 'hidden'; els.position = 'absolute'; els.display = ''; var originalWidth = element.clientWidth; var originalHeight = element.clientHeight; els.display = 'none'; els.position = originalPosition; els.visibility = originalVisibility; return {width: originalWidth, height: originalHeight}; }, makePositioned: function(element) { element = $(element); var pos = Element.getStyle(element, 'position'); if (pos == 'static' || !pos) { element._madePositioned = true; element.style.position = 'relative'; if (window.opera) { element.style.top = 0; element.style.left = 0; } } }, undoPositioned: function(element) { element = $(element); if (element._madePositioned) { element._madePositioned = undefined; element.style.position = element.style.top = element.style.left = element.style.bottom = element.style.right = ''; } }, makeClipping: function(element) { element = $(element); if (element._overflow) return; element._overflow = element.style.overflow; if ((Element.getStyle(element, 'overflow') || 'visible') != 'hidden') element.style.overflow = 'hidden'; }, undoClipping: function(element) { element = $(element); if (element._overflow) return; element.style.overflow = element._overflow; element._overflow = undefined; } });
var Toggle = new Object();
Toggle.display = Element.toggle;
Abstract.Insertion = function(adjacency) { this.adjacency = adjacency; }
Abstract.Insertion.prototype = { initialize: function(element, content) { this.element = $(element); this.content = content.stripScripts(); if (this.adjacency && this.element.insertAdjacentHTML) { try { this.element.insertAdjacentHTML(this.adjacency, this.content); } catch (e) { if (this.element.tagName.toLowerCase() == 'tbody') { this.insertContent(this.contentFromAnonymousTable()); } else { throw e; } } } else { this.range = this.element.ownerDocument.createRange(); if (this.initializeRange) this.initializeRange(); this.insertContent([this.range.createContextualFragment(this.content)]); } setTimeout(function() {content.evalScripts()}, 10); }, contentFromAnonymousTable: function() { var div = document.createElement('div'); div.innerHTML = '<table><tbody>' + this.content + '</tbody></table>'; return $A(div.childNodes[0].childNodes[0].childNodes); } }
var Insertion = new Object();
Insertion.Before = Class.create();
Insertion.Before.prototype = Object.extend(new Abstract.Insertion('beforeBegin'), { initializeRange: function() { this.range.setStartBefore(this.element); }, insertContent: function(fragments) { fragments.each((function(fragment) { this.element.parentNode.insertBefore(fragment, this.element); }).bind(this)); } });
Insertion.Top = Class.create();
Insertion.Top.prototype = Object.extend(new Abstract.Insertion('afterBegin'), { initializeRange: function() { this.range.selectNodeContents(this.element); this.range.collapse(true); }, insertContent: function(fragments) { fragments.reverse(false).each((function(fragment) { this.element.insertBefore(fragment, this.element.firstChild); }).bind(this)); } });
Insertion.Bottom = Class.create();
Insertion.Bottom.prototype = Object.extend(new Abstract.Insertion('beforeEnd'), { initializeRange: function() { this.range.selectNodeContents(this.element); this.range.collapse(this.element); }, insertContent: function(fragments) { fragments.each((function(fragment) { this.element.appendChild(fragment); }).bind(this)); } });
Insertion.After = Class.create();
Insertion.After.prototype = Object.extend(new Abstract.Insertion('afterEnd'), { initializeRange: function() { this.range.setStartAfter(this.element); }, insertContent: function(fragments) { fragments.each((function(fragment) { this.element.parentNode.insertBefore(fragment, this.element.nextSibling); }).bind(this)); } });
Element.ClassNames = Class.create();
Element.ClassNames.prototype = { initialize: function(element) { this.element = $(element); }, _each: function(iterator) { this.element.className.split(/\s+/).select(function(name) { return name.length > 0; })._each(iterator); }, set: function(className) { this.element.className = className; }, add: function(classNameToAdd) { if (this.include(classNameToAdd)) return; this.set(this.toArray().concat(classNameToAdd).join(' ')); }, remove: function(classNameToRemove) { if (!this.include(classNameToRemove)) return; this.set(this.select(function(className) { return className != classNameToRemove; }).join(' ')); }, toString: function() { return this.toArray().join(' '); } }
Object.extend(Element.ClassNames.prototype, Enumerable);
var Field = { clear: function() { for (var i = 0; i < arguments.length; i++) $(arguments[i]).value = ''; }, focus: function(element) { $(element).focus(); }, present: function() { for (var i = 0; i < arguments.length; i++) if ($(arguments[i]).value == '') return false; return true; }, select: function(element) { $(element).select(); }, activate: function(element) { element = $(element); element.focus(); if (element.select) element.select(); } }

var Form = { serialize: function(form) { var elements = Form.getElements($(form)); var queryComponents = new Array(); for (var i = 0; i < elements.length; i++) { var queryComponent = Form.Element.serialize(elements[i]); if (queryComponent) queryComponents.push(queryComponent); } return queryComponents.join('&'); }, getElements: function(form) { form = $(form); var elements = new Array(); for (tagName in Form.Element.Serializers) { var tagElements = form.getElementsByTagName(tagName); for (var j = 0; j < tagElements.length; j++) elements.push(tagElements[j]); } return elements; }, getInputs: function(form, typeName, name) { form = $(form); var inputs = form.getElementsByTagName('input'); if (!typeName && !name) return inputs; var matchingInputs = new Array(); for (var i = 0; i < inputs.length; i++) { var input = inputs[i]; if ((typeName && input.type != typeName) || (name && input.name != name)) continue; matchingInputs.push(input); } return matchingInputs; }, disable: function(form) { var elements = Form.getElements(form); for (var i = 0; i < elements.length; i++) { var element = elements[i]; element.blur(); element.disabled = 'true'; } }, enable: function(form) { var elements = Form.getElements(form); for (var i = 0; i < elements.length; i++) { var element = elements[i]; element.disabled = ''; } }, findFirstElement: function(form) { return Form.getElements(form).find(function(element) { return element.type != 'hidden' && !element.disabled && ['input', 'select', 'textarea'].include(element.tagName.toLowerCase()); }); }, focusFirstElement: function(form) { Field.activate(Form.findFirstElement(form)); }, reset: function(form) { $(form).reset(); } }
Form.Element = { serialize: function(element) { element = $(element); var method = element.tagName.toLowerCase(); var parameter = Form.Element.Serializers[method](element); if (parameter) { var key = encodeURIComponent(parameter[0]); if (key.length == 0) return; if (parameter[1].constructor != Array) parameter[1] = [parameter[1]]; return parameter[1].map(function(value) { return key + '=' + encodeURIComponent(value); }).join('&'); } }, getValue: function(element) { element = $(element); var method = element.tagName.toLowerCase(); var parameter = Form.Element.Serializers[method](element); if (parameter) return parameter[1]; } }
Form.Element.Serializers = { input: function(element) { switch (element.type.toLowerCase()) { case 'submit': case 'hidden': case 'password': case 'text': return Form.Element.Serializers.textarea(element); case 'checkbox': case 'radio': return Form.Element.Serializers.inputSelector(element); } return false; }, inputSelector: function(element) { if (element.checked) return [element.name, element.value]; }, textarea: function(element) { return [element.name, element.value]; }, select: function(element) { return Form.Element.Serializers[element.type == 'select-one' ? 'selectOne' : 'selectMany'](element); }, selectOne: function(element) { var value = '', opt, index = element.selectedIndex; if (index >= 0) { opt = element.options[index]; value = opt.value; if (!value && !('value' in opt)) value = opt.text; } return [element.name, value]; }, selectMany: function(element) { var value = new Array(); for (var i = 0; i < element.length; i++) { var opt = element.options[i]; if (opt.selected) { var optValue = opt.value; if (!optValue && !('value' in opt)) optValue = opt.text; value.push(optValue); } } return [element.name, value]; } }
var $F = Form.Element.getValue;
Abstract.TimedObserver = function() {}
Abstract.TimedObserver.prototype = { initialize: function(element, frequency, callback) { this.frequency = frequency; this.element   = $(element); this.callback  = callback; this.lastValue = this.getValue(); this.registerCallback(); }, registerCallback: function() { setInterval(this.onTimerEvent.bind(this), this.frequency * 1000); }, onTimerEvent: function() { var value = this.getValue(); if (this.lastValue != value) { this.callback(this.element, value); this.lastValue = value; } } }
Form.Element.Observer = Class.create();
Form.Element.Observer.prototype = Object.extend(new Abstract.TimedObserver(), { getValue: function() { return Form.Element.getValue(this.element); } });
Form.Observer = Class.create();
Form.Observer.prototype = Object.extend(new Abstract.TimedObserver(), { getValue: function() { return Form.serialize(this.element); } });

Abstract.EventObserver = function() {}
Abstract.EventObserver.prototype = { initialize: function(element, callback) { this.element  = $(element); this.callback = callback; this.lastValue = this.getValue(); if (this.element.tagName.toLowerCase() == 'form') this.registerFormCallbacks(); else this.registerCallback(this.element); }, onElementEvent: function() { var value = this.getValue(); if (this.lastValue != value) { this.callback(this.element, value); this.lastValue = value; } }, registerFormCallbacks: function() { var elements = Form.getElements(this.element); for (var i = 0; i < elements.length; i++) this.registerCallback(elements[i]); }, registerCallback: function(element) { if (element.type) { switch (element.type.toLowerCase()) { case 'checkbox': case 'radio': Event.observe(element, 'click', this.onElementEvent.bind(this)); break; case 'password': case 'text': case 'textarea': case 'select-one': case 'select-multiple': Event.observe(element, 'change', this.onElementEvent.bind(this)); break; } } } }
Form.Element.EventObserver = Class.create();
Form.Element.EventObserver.prototype = Object.extend(new Abstract.EventObserver(), { getValue: function() { return Form.Element.getValue(this.element); } });
Form.EventObserver = Class.create();
Form.EventObserver.prototype = Object.extend(new Abstract.EventObserver(), { getValue: function() { return Form.serialize(this.element); } });
if (!window.Event) { var Event = new Object(); }
Object.extend(Event, { KEY_BACKSPACE: 8, KEY_TAB:       9, KEY_RETURN:   13, KEY_ESC:      27, KEY_LEFT:     37, KEY_UP:       38, KEY_RIGHT:    39, KEY_DOWN:     40, KEY_DELETE:   46, element: function(event) { return event.target || event.srcElement; }, isLeftClick: function(event) { return (((event.which) && (event.which == 1)) || ((event.button) && (event.button == 1))); }, pointerX: function(event) { return event.pageX || (event.clientX + (document.documentElement.scrollLeft || document.body.scrollLeft)); }, pointerY: function(event) { return event.pageY || (event.clientY + (document.documentElement.scrollTop || document.body.scrollTop)); }, stop: function(event) { if (event.preventDefault) { event.preventDefault(); event.stopPropagation(); } else { event.returnValue = false; event.cancelBubble = true; } }, findElement: function(event, tagName) { var element = Event.element(event); while (element.parentNode && (!element.tagName || (element.tagName.toUpperCase() != tagName.toUpperCase()))) element = element.parentNode; return element; }, observers: false, _observeAndCache: function(element, name, observer, useCapture) { if (!this.observers) this.observers = []; if (element.addEventListener) { this.observers.push([element, name, observer, useCapture]); element.addEventListener(name, observer, useCapture); } else if (element.attachEvent) { this.observers.push([element, name, observer, useCapture]); element.attachEvent('on' + name, observer); } }, unloadCache: function() { if (!Event.observers) return; for (var i = 0; i < Event.observers.length; i++) { Event.stopObserving.apply(this, Event.observers[i]); Event.observers[i][0] = null; } Event.observers = false; }, observe: function(element, name, observer, useCapture) { var element = $(element); useCapture = useCapture || false; if (name == 'keypress' && (navigator.appVersion.match(/Konqueror|Safari|KHTML/) || element.attachEvent)) name = 'keydown'; this._observeAndCache(element, name, observer, useCapture); }, stopObserving: function(element, name, observer, useCapture) { var element = $(element); useCapture = useCapture || false; if (name == 'keypress' && (navigator.appVersion.match(/Konqueror|Safari|KHTML/) || element.detachEvent)) name = 'keydown'; if (element.removeEventListener) { element.removeEventListener(name, observer, useCapture); } else if (element.detachEvent) { element.detachEvent('on' + name, observer); } } });
Event.observe(window, 'unload', Event.unloadCache, false);
var Position = {
  includeScrollOffsets: false,
  prepare: function() { this.deltaX =  window.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft || 0; this.deltaY =  window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0; },
  realOffset: function(element) { var valueT = 0, valueL = 0; do { valueT += element.scrollTop  || 0; valueL += element.scrollLeft || 0; element = element.parentNode; } while (element); return [valueL, valueT]; },
  cumulativeOffset: function(element) { var valueT = 0, valueL = 0; do { valueT += element.offsetTop  || 0; valueL += element.offsetLeft || 0; element = element.offsetParent; } while (element); return [valueL, valueT]; },
  positionedOffset: function(element) { var valueT = 0, valueL = 0; do { valueT += element.offsetTop  || 0; valueL += element.offsetLeft || 0; element = element.offsetParent; if (element) { p = Element.getStyle(element, 'position'); if (p == 'relative' || p == 'absolute') break; } } while (element); return [valueL, valueT]; },
  offsetParent: function(element) { if (element.offsetParent) return element.offsetParent; if (element == document.body) return element; while ((element = element.parentNode) && element != document.body) if (Element.getStyle(element, 'position') != 'static') return element; return document.body; },
  within: function(element, x, y) { if (this.includeScrollOffsets) return this.withinIncludingScrolloffsets(element, x, y); this.xcomp = x; this.ycomp = y; this.offset = this.cumulativeOffset(element); return (y >= this.offset[1] && y <  this.offset[1] + element.offsetHeight && x >= this.offset[0] && x <  this.offset[0] + element.offsetWidth); },
  withinIncludingScrolloffsets: function(element, x, y) { var offsetcache = this.realOffset(element); this.xcomp = x + offsetcache[0] - this.deltaX; this.ycomp = y + offsetcache[1] - this.deltaY; this.offset = this.cumulativeOffset(element); return (this.ycomp >= this.offset[1] && this.ycomp <  this.offset[1] + element.offsetHeight && this.xcomp >= this.offset[0] && this.xcomp <  this.offset[0] + element.offsetWidth); },
  overlap: function(mode, element) { if (!mode) return 0; if (mode == 'vertical') return ((this.offset[1] + element.offsetHeight) - this.ycomp) / element.offsetHeight; if (mode == 'horizontal') return ((this.offset[0] + element.offsetWidth) - this.xcomp) / element.offsetWidth; },
  clone: function(source, target) { source = $(source); target = $(target); target.style.position = 'absolute'; var offsets = this.cumulativeOffset(source); target.style.top    = offsets[1] + 'px'; target.style.left   = offsets[0] + 'px'; target.style.width  = source.offsetWidth + 'px'; target.style.height = source.offsetHeight + 'px'; },
  page: function(forElement) { var valueT = 0, valueL = 0; var element = forElement; do { valueT += element.offsetTop  || 0; valueL += element.offsetLeft || 0; if (element.offsetParent==document.body) if (Element.getStyle(element,'position')=='absolute') break; } while (element = element.offsetParent); element = forElement; do { valueT -= element.scrollTop  || 0; valueL -= element.scrollLeft || 0; } while (element = element.parentNode); return [valueL, valueT]; },
  clone: function(source, target) {
    var options = Object.extend({ setLeft:    true, setTop:     true, setWidth:   true, setHeight:  true, offsetTop:  0, offsetLeft: 0 }, arguments[2] || {})
    source = $(source);
    var p = Position.page(source);
    target = $(target);
    var delta = [0, 0];
    var parent = null;
    if (Element.getStyle(target,'position') == 'absolute') { parent = Position.offsetParent(target); delta = Position.page(parent); }
    if (parent == document.body) { delta[0] -= document.body.offsetLeft; delta[1] -= document.body.offsetTop; }
    if(options.setLeft)   target.style.left  = (p[0] - delta[0] + options.offsetLeft) + 'px';
    if(options.setTop)    target.style.top   = (p[1] - delta[1] + options.offsetTop) + 'px';
    if(options.setWidth)  target.style.width = source.offsetWidth + 'px';
    if(options.setHeight) target.style.height = source.offsetHeight + 'px';
  },
  absolutize: function(element) { element = $(element); if (element.style.position == 'absolute') return; Position.prepare(); var offsets = Position.positionedOffset(element); var top     = offsets[1]; var left    = offsets[0]; var width   = element.clientWidth; var height  = element.clientHeight; element._originalLeft   = left - parseFloat(element.style.left  || 0); element._originalTop    = top  - parseFloat(element.style.top || 0); element._originalWidth  = element.style.width; element._originalHeight = element.style.height; element.style.position = 'absolute'; element.style.top    = top + 'px';; element.style.left   = left + 'px';; element.style.width  = width + 'px';; element.style.height = height + 'px';; },
  relativize: function(element) { element = $(element); if (element.style.position == 'relative') return; Position.prepare(); element.style.position = 'relative'; var top  = parseFloat(element.style.top  || 0) - (element._originalTop || 0); var left = parseFloat(element.style.left || 0) - (element._originalLeft || 0); element.style.top    = top + 'px'; element.style.left   = left + 'px'; element.style.height = element._originalHeight; element.style.width  = element._originalWidth; }
}
if (/Konqueror|Safari|KHTML/.test(navigator.userAgent)) { Position.cumulativeOffset = function(element) { var valueT = 0, valueL = 0; do { valueT += element.offsetTop  || 0; valueL += element.offsetLeft || 0; if (element.offsetParent == document.body) if (Element.getStyle(element, 'position') == 'absolute') break; element = element.offsetParent; } while (element); return [valueL, valueT]; } }
var Scriptaculous = {
  Version: '1.5.1',
  require: function(libraryName) {
    document.write('<script type="text/javascript" src="'+libraryName+'"></script>');
  },
  load: function() { if((typeof Prototype=='undefined') || parseFloat(Prototype.Version.split(".")[0] + "." + Prototype.Version.split(".")[1]) < 1.4) throw("script.aculo.us requires the Prototype JavaScript framework >= 1.4.0"); $A(document.getElementsByTagName("script")).findAll( function(s) { return (s.src && s.src.match(/scriptaculous\.js(\?.*)?$/)) }).each( function(s) { var path = s.src.replace(/scriptaculous\.js(\?.*)?$/,''); var includes = s.src.match(/\?.*load=([a-z,]*)/); (includes ? includes[1] : 'builder,effects,dragdrop,controls,slider').split(',').each( function(include) { Scriptaculous.require(path+include+'.js') }); }); }
}
Scriptaculous.load();
String.prototype.parseColor = function() {  var color = '#';  if(this.slice(0,4) == 'rgb(') {  var cols = this.slice(4,this.length-1).split(',');  var i=0; do { color += parseInt(cols[i]).toColorPart() } while (++i<3);  } else {  if(this.slice(0,1) == '#') {  if(this.length==4) for(var i=1;i<4;i++) color += (this.charAt(i) + this.charAt(i)).toLowerCase();  if(this.length==7) color = this.toLowerCase();  }  }  return(color.length==7 ? color : (arguments[0] || this));  }
Element.collectTextNodes = function(element) {  return $A($(element).childNodes).collect( function(node) { return (node.nodeType==3 ? node.nodeValue : (node.hasChildNodes() ? Element.collectTextNodes(node) : '')); }).flatten().join(''); }
Element.collectTextNodesIgnoreClass = function(element, className) {  return $A($(element).childNodes).collect( function(node) { return (node.nodeType==3 ? node.nodeValue : ((node.hasChildNodes() && !Element.hasClassName(node,className)) ? Element.collectTextNodes(node) : '')); }).flatten().join(''); }
Element.setStyle = function(element, style) {
  element = $(element);
  for(k in style) element.style[k.camelize()] = style[k];
}
Element.setContentZoom = function(element, percent) {  
  Element.setStyle(element, {fontSize: (percent/100) + 'em'});   
  if(navigator.appVersion.indexOf('AppleWebKit')>0) window.scrollBy(0,0);  
}
Element.getOpacity = function(element){  var opacity; if (opacity = Element.getStyle(element, 'opacity'))  return parseFloat(opacity);  if (opacity = (Element.getStyle(element, 'filter') || '').match(/alpha\(opacity=(.*)\)/))  if(opacity[1]) return parseFloat(opacity[1]) / 100;  return 1.0;  }
Element.setOpacity = function(element, value){  element= $(element);  if (value == 1){ Element.setStyle(element, { opacity: (/Gecko/.test(navigator.userAgent) && !/Konqueror|Safari|KHTML/.test(navigator.userAgent)) ? 0.999999 : null }); if(/MSIE/.test(navigator.userAgent))  Element.setStyle(element, {filter: Element.getStyle(element,'filter').replace(/alpha\([^\)]*\)/gi,'')});  } else {  if(value < 0.00001) value = 0;  Element.setStyle(element, {opacity: value}); if(/MSIE/.test(navigator.userAgent))  Element.setStyle(element, { filter: Element.getStyle(element,'filter').replace(/alpha\([^\)]*\)/gi,'') + 'alpha(opacity='+value*100+')' });  }   }  
Element.getInlineOpacity = function(element){  
  return $(element).style.opacity || '';
}  
Element.childrenWithClassName = function(element, className) {  
  return $A($(element).getElementsByTagName('*')).select(
    function(c) { return Element.hasClassName(c, className) });
}
Array.prototype.call = function() {
  var args = arguments;
  this.each(function(f){ f.apply(this, args) });
}
var Effect = {
  tagifyText: function(element) { var tagifyStyle = 'position:relative'; if(/MSIE/.test(navigator.userAgent)) tagifyStyle += ';zoom:1'; element = $(element); $A(element.childNodes).each( function(child) { if(child.nodeType==3) { child.nodeValue.toArray().each( function(character) { element.insertBefore( Builder.node('span',{style: tagifyStyle}, character == ' ' ? String.fromCharCode(160) : character), child); }); Element.remove(child); } }); },
  multiple: function(element, effect) {
    var elements;
    if(((typeof element == 'object') || 
        (typeof element == 'function')) && 
       (element.length))
      elements = element;
    else
      elements = $(element).childNodes;
      
    var options = Object.extend({
      speed: 0.1,
      delay: 0.0
    }, arguments[2] || {});
    var masterDelay = options.delay;
    $A(elements).each( function(element, index) {
      new effect(element, Object.extend(options, { delay: index * options.speed + masterDelay }));
    });
  },
  PAIRS: {
    'slide':  ['SlideDown','SlideUp'],
    'blind':  ['BlindDown','BlindUp'],
    'appear': ['Appear','Fade']
  },
  toggle: function(element, effect) { element = $(element); effect = (effect || 'appear').toLowerCase(); var options = Object.extend({ queue: { position:'end', scope:(element.id || 'global') } }, arguments[2] || {}); Effect[Element.visible(element) ? Effect.PAIRS[effect][1] : Effect.PAIRS[effect][0]](element, options); }
};
var Effect2 = Effect;
Effect.Transitions = {}
Effect.Transitions.linear = function(pos) {
  return pos;
}
Effect.Transitions.sinoidal = function(pos) {
  return (-Math.cos(pos*Math.PI)/2) + 0.5;
}
Effect.Transitions.reverse  = function(pos) {
  return 1-pos;
}
Effect.Transitions.flicker = function(pos) {
  return ((-Math.cos(pos*Math.PI)/4) + 0.75) + Math.random()/4;
}
Effect.Transitions.wobble = function(pos) {
  return (-Math.cos(pos*Math.PI*(9*pos))/2) + 0.5;
}
Effect.Transitions.pulse = function(pos) {
  return (Math.floor(pos*10) % 2 == 0 ? 
    (pos*10-Math.floor(pos*10)) : 1-(pos*10-Math.floor(pos*10)));
}
Effect.Transitions.none = function(pos) {
  return 0;
}
Effect.Transitions.full = function(pos) {
  return 1;
}
Effect.ScopedQueue = Class.create();
Object.extend(Object.extend(Effect.ScopedQueue.prototype, Enumerable), { initialize: function() { this.effects  = []; this.interval = null; }, _each: function(iterator) { this.effects._each(iterator); }, add: function(effect) { var timestamp = new Date().getTime(); var position = (typeof effect.options.queue == 'string') ? effect.options.queue : effect.options.queue.position; switch(position) { case 'front': this.effects.findAll(function(e){ return e.state=='idle' }).each( function(e) { e.startOn  += effect.finishOn; e.finishOn += effect.finishOn; }); break; case 'end': timestamp = this.effects.pluck('finishOn').max() || timestamp; break; } effect.startOn  += timestamp; effect.finishOn += timestamp; this.effects.push(effect); if(!this.interval) this.interval = setInterval(this.loop.bind(this), 40); },
  remove: function(effect) { this.effects = this.effects.reject(function(e) { return e==effect }); if(this.effects.length == 0) { clearInterval(this.interval); this.interval = null; } }, loop: function() { var timePos = new Date().getTime(); this.effects.invoke('loop', timePos); } });
Effect.Queues = {
  instances: $H(),
  get: function(queueName) {
    if(typeof queueName != 'string') return queueName;
    
    if(!this.instances[queueName])
      this.instances[queueName] = new Effect.ScopedQueue();
      
    return this.instances[queueName];
  }
}
Effect.Queue = Effect.Queues.get('global');
Effect.DefaultOptions = {
  transition: Effect.Transitions.sinoidal,
  duration:   1.0,
  fps:        25.0,
  sync:       false,
  from:       0.0,
  to:         1.0,
  delay:      0.0,
  queue:      'parallel'
}
Effect.Base = function() {};
Effect.Base.prototype = {
  position: null,
  start: function(options) { this.options      = Object.extend(Object.extend({},Effect.DefaultOptions), options || {}); this.currentFrame = 0; this.state        = 'idle'; this.startOn      = this.options.delay*1000; this.finishOn     = this.startOn + (this.options.duration*1000); this.event('beforeStart'); if(!this.options.sync) Effect.Queues.get(typeof this.options.queue == 'string' ? 'global' : this.options.queue.scope).add(this); },
  loop: function(timePos) { if(timePos >= this.startOn) { if(timePos >= this.finishOn) { this.render(1.0); this.cancel(); this.event('beforeFinish'); if(this.finish) this.finish(); this.event('afterFinish'); return;  } var pos   = (timePos - this.startOn) / (this.finishOn - this.startOn); var frame = Math.round(pos * this.options.fps * this.options.duration); if(frame > this.currentFrame) { this.render(pos); this.currentFrame = frame; } } },
  render: function(pos) { if(this.state == 'idle') { this.state = 'running'; this.event('beforeSetup'); if(this.setup) this.setup(); this.event('afterSetup'); } if(this.state == 'running') { if(this.options.transition) pos = this.options.transition(pos); pos *= (this.options.to-this.options.from); pos += this.options.from; this.position = pos; this.event('beforeUpdate'); if(this.update) this.update(pos); this.event('afterUpdate'); } },
  cancel: function() { if(!this.options.sync) Effect.Queues.get(typeof this.options.queue == 'string' ? 'global' : this.options.queue.scope).remove(this); this.state = 'finished'; },
  event: function(eventName) { if(this.options[eventName + 'Internal']) this.options[eventName + 'Internal'](this); if(this.options[eventName]) this.options[eventName](this); },
  inspect: function() { return '#<Effect:' + $H(this).inspect() + ',options:' + $H(this.options).inspect() + '>'; }
}
Effect.Parallel = Class.create();
Object.extend(Object.extend(Effect.Parallel.prototype, Effect.Base.prototype), { initialize: function(effects) { this.effects = effects || []; this.start(arguments[1]); }, update: function(position) { this.effects.invoke('render', position); }, finish: function(position) { this.effects.each( function(effect) { effect.render(1.0); effect.cancel(); effect.event('beforeFinish'); if(effect.finish) effect.finish(position); effect.event('afterFinish'); }); } });
Effect.Opacity = Class.create();
Object.extend(Object.extend(Effect.Opacity.prototype, Effect.Base.prototype), { initialize: function(element) { this.element = $(element); if(/MSIE/.test(navigator.userAgent) && (!this.element.hasLayout)) Element.setStyle(this.element, {zoom: 1}); var options = Object.extend({ from: Element.getOpacity(this.element) || 0.0, to:   1.0 }, arguments[1] || {}); this.start(options); }, update: function(position) { Element.setOpacity(this.element, position); } });
Effect.Move = Class.create();
Object.extend(Object.extend(Effect.Move.prototype, Effect.Base.prototype), { initialize: function(element) { this.element = $(element); var options = Object.extend({ x:    0, y:    0, mode: 'relative' }, arguments[1] || {}); this.start(options); }, setup: function() { Element.makePositioned(this.element); this.originalLeft = parseFloat(Element.getStyle(this.element,'left') || '0'); this.originalTop  = parseFloat(Element.getStyle(this.element,'top')  || '0'); if(this.options.mode == 'absolute') { this.options.x = this.options.x - this.originalLeft; this.options.y = this.options.y - this.originalTop; } }, update: function(position) { Element.setStyle(this.element, { left: this.options.x  * position + this.originalLeft + 'px', top:  this.options.y  * position + this.originalTop  + 'px' }); } });
Effect.MoveBy = function(element, toTop, toLeft) {
  return new Effect.Move(element, 
    Object.extend({ x: toLeft, y: toTop }, arguments[3] || {}));
};
Effect.Scale = Class.create();
Object.extend(Object.extend(Effect.Scale.prototype, Effect.Base.prototype), {
  initialize: function(element, percent) {
    this.element = $(element)
    var options = Object.extend({
      scaleX: true,
      scaleY: true,
      scaleContent: true,
      scaleFromCenter: false,
      scaleMode: 'box',
      scaleFrom: 100.0,
      scaleTo:   percent
    }, arguments[2] || {});
    this.start(options);
  },
  setup: function() {
    this.restoreAfterFinish = this.options.restoreAfterFinish || false;
    this.elementPositioning = Element.getStyle(this.element,'position');
    
    this.originalStyle = {};
    ['top','left','width','height','fontSize'].each( function(k) {
      this.originalStyle[k] = this.element.style[k];
    }.bind(this));
      
    this.originalTop  = this.element.offsetTop;
    this.originalLeft = this.element.offsetLeft;
    
    var fontSize = Element.getStyle(this.element,'font-size') || '100%';
    ['em','px','%'].each( function(fontSizeType) {
      if(fontSize.indexOf(fontSizeType)>0) {
        this.fontSize     = parseFloat(fontSize);
        this.fontSizeType = fontSizeType;
      }
    }.bind(this));
    
    this.factor = (this.options.scaleTo - this.options.scaleFrom)/100;
    
    this.dims = null;
    if(this.options.scaleMode=='box')
      this.dims = [this.element.offsetHeight, this.element.offsetWidth];
    if(/^content/.test(this.options.scaleMode))
      this.dims = [this.element.scrollHeight, this.element.scrollWidth];
    if(!this.dims)
      this.dims = [this.options.scaleMode.originalHeight,
                   this.options.scaleMode.originalWidth];
  },
  update: function(position) {
    var currentScale = (this.options.scaleFrom/100.0) + (this.factor * position);
    if(this.options.scaleContent && this.fontSize)
      Element.setStyle(this.element, {fontSize: this.fontSize * currentScale + this.fontSizeType });
    this.setDimensions(this.dims[0] * currentScale, this.dims[1] * currentScale);
  },
  finish: function(position) {
    if (this.restoreAfterFinish) Element.setStyle(this.element, this.originalStyle);
  },
  setDimensions: function(height, width) {
    var d = {};
    if(this.options.scaleX) d.width = width + 'px';
    if(this.options.scaleY) d.height = height + 'px';
    if(this.options.scaleFromCenter) {
      var topd  = (height - this.dims[0])/2;
      var leftd = (width  - this.dims[1])/2;
      if(this.elementPositioning == 'absolute') {
        if(this.options.scaleY) d.top = this.originalTop-topd + 'px';
        if(this.options.scaleX) d.left = this.originalLeft-leftd + 'px';
      } else {
        if(this.options.scaleY) d.top = -topd + 'px';
        if(this.options.scaleX) d.left = -leftd + 'px';
      }
    }
    Element.setStyle(this.element, d);
  }
});
Effect.Highlight = Class.create();
Object.extend(Object.extend(Effect.Highlight.prototype, Effect.Base.prototype), {
  initialize: function(element) {
    this.element = $(element);
    var options = Object.extend({ startcolor: '#ffff99' }, arguments[1] || {});
    this.start(options);
  },
  setup: function() {
    if(Element.getStyle(this.element, 'display')=='none') { this.cancel(); return; }
    this.oldStyle = {
      backgroundImage: Element.getStyle(this.element, 'background-image') };
    Element.setStyle(this.element, {backgroundImage: 'none'});
    if(!this.options.endcolor)
      this.options.endcolor = Element.getStyle(this.element, 'background-color').parseColor('#ffffff');
    if(!this.options.restorecolor)
      this.options.restorecolor = Element.getStyle(this.element, 'background-color');
    this._base  = $R(0,2).map(function(i){ return parseInt(this.options.startcolor.slice(i*2+1,i*2+3),16) }.bind(this));
    this._delta = $R(0,2).map(function(i){ return parseInt(this.options.endcolor.slice(i*2+1,i*2+3),16)-this._base[i] }.bind(this));
  },
  update: function(position) {
    Element.setStyle(this.element,{backgroundColor: $R(0,2).inject('#',function(m,v,i){
      return m+(Math.round(this._base[i]+(this._delta[i]*position)).toColorPart()); }.bind(this)) });
  },
  finish: function() {
    Element.setStyle(this.element, Object.extend(this.oldStyle, {
      backgroundColor: this.options.restorecolor
    }));
  }
});
Effect.ScrollTo = Class.create();
Object.extend(Object.extend(Effect.ScrollTo.prototype, Effect.Base.prototype), {
  initialize: function(element) {
    this.element = $(element);
    this.start(arguments[1] || {});
  },
  setup: function() {
    Position.prepare();
    var offsets = Position.cumulativeOffset(this.element);
    if(this.options.offset) offsets[1] += this.options.offset;
    var max = window.innerHeight ? 
      window.height - window.innerHeight :
      document.body.scrollHeight - 
        (document.documentElement.clientHeight ? 
          document.documentElement.clientHeight : document.body.clientHeight);
    this.scrollStart = Position.deltaY;
    this.delta = (offsets[1] > max ? max : offsets[1]) - this.scrollStart;
  },
  update: function(position) {
    Position.prepare();
    window.scrollTo(Position.deltaX, 
      this.scrollStart + (position*this.delta));
  }
});
Effect.Fade = function(element) { var oldOpacity = Element.getInlineOpacity(element); var options = Object.extend({ from: Element.getOpacity(element) || 1.0, to:   0.0, afterFinishInternal: function(effect) { with(Element) { if(effect.options.to!=0) return; hide(effect.element); setStyle(effect.element, {opacity: oldOpacity}); }} }, arguments[1] || {}); return new Effect.Opacity(element,options); }
Effect.Appear = function(element) { var options = Object.extend({ from: (Element.getStyle(element, 'display') == 'none' ? 0.0 : Element.getOpacity(element) || 0.0), to:   1.0, beforeSetup: function(effect) { with(Element) { setOpacity(effect.element, effect.options.from); show(effect.element); }} }, arguments[1] || {}); return new Effect.Opacity(element,options); }
Effect.Puff = function(element) { element = $(element); var oldStyle = { opacity: Element.getInlineOpacity(element), position: Element.getStyle(element, 'position') }; return new Effect.Parallel( [ new Effect.Scale(element, 200, { sync: true, scaleFromCenter: true, scaleContent: true, restoreAfterFinish: true }), new Effect.Opacity(element, { sync: true, to: 0.0 } ) ], Object.extend({ duration: 1.0, beforeSetupInternal: function(effect) { with(Element) { setStyle(effect.effects[0].element, {position: 'absolute'}); }}, afterFinishInternal: function(effect) { with(Element) { hide(effect.effects[0].element); setStyle(effect.effects[0].element, oldStyle); }} }, arguments[1] || {}) ); }
Effect.BlindUp = function(element) { element = $(element); Element.makeClipping(element); return new Effect.Scale(element, 0, Object.extend({ scaleContent: false, scaleX: false, restoreAfterFinish: true, afterFinishInternal: function(effect) { with(Element) { [hide, undoClipping].call(effect.element); }} }, arguments[1] || {}) ); }
Effect.BlindDown = function(element) { element = $(element); var oldHeight = Element.getStyle(element, 'height'); var elementDimensions = Element.getDimensions(element); return new Effect.Scale(element, 100, Object.extend({ scaleContent: false, scaleX: false, scaleFrom: 0, scaleMode: {originalHeight: elementDimensions.height, originalWidth: elementDimensions.width}, restoreAfterFinish: true, afterSetup: function(effect) { with(Element) { makeClipping(effect.element); setStyle(effect.element, {height: '0px'}); show(effect.element); }},  afterFinishInternal: function(effect) { with(Element) { undoClipping(effect.element); setStyle(effect.element, {height: oldHeight}); }} }, arguments[1] || {}) ); }
Effect.SwitchOff = function(element) { element = $(element); var oldOpacity = Element.getInlineOpacity(element); return new Effect.Appear(element, { duration: 0.4, from: 0, transition: Effect.Transitions.flicker, afterFinishInternal: function(effect) { new Effect.Scale(effect.element, 1, { duration: 0.3, scaleFromCenter: true, scaleX: false, scaleContent: false, restoreAfterFinish: true, beforeSetup: function(effect) { with(Element) { [makePositioned,makeClipping].call(effect.element); }}, afterFinishInternal: function(effect) { with(Element) { [hide,undoClipping,undoPositioned].call(effect.element); setStyle(effect.element, {opacity: oldOpacity}); }} }) } }); }
Effect.DropOut = function(element) { element = $(element); var oldStyle = { top: Element.getStyle(element, 'top'), left: Element.getStyle(element, 'left'), opacity: Element.getInlineOpacity(element) }; return new Effect.Parallel( [ new Effect.Move(element, {x: 0, y: 100, sync: true }), new Effect.Opacity(element, { sync: true, to: 0.0 }) ], Object.extend( { duration: 0.5, beforeSetup: function(effect) { with(Element) { makePositioned(effect.effects[0].element); }}, afterFinishInternal: function(effect) { with(Element) { [hide, undoPositioned].call(effect.effects[0].element); setStyle(effect.effects[0].element, oldStyle); }} }, arguments[1] || {})); }
Effect.Shake = function(element) { element = $(element); var oldStyle = { top: Element.getStyle(element, 'top'), left: Element.getStyle(element, 'left') }; return new Effect.Move(element, { x:  20, y: 0, duration: 0.05, afterFinishInternal: function(effect) { new Effect.Move(effect.element, { x: -40, y: 0, duration: 0.1,  afterFinishInternal: function(effect) { new Effect.Move(effect.element, { x:  40, y: 0, duration: 0.1,  afterFinishInternal: function(effect) { new Effect.Move(effect.element, { x: -40, y: 0, duration: 0.1,  afterFinishInternal: function(effect) { new Effect.Move(effect.element, { x:  40, y: 0, duration: 0.1,  afterFinishInternal: function(effect) { new Effect.Move(effect.element, { x: -20, y: 0, duration: 0.05, afterFinishInternal: function(effect) { with(Element) { undoPositioned(effect.element); setStyle(effect.element, oldStyle); }}}) }}) }}) }}) }}) }}); }
Effect.SlideDown = function(element) { element = $(element); Element.cleanWhitespace(element); var oldInnerBottom = Element.getStyle(element.firstChild, 'bottom'); var elementDimensions = Element.getDimensions(element); return new Effect.Scale(element, 100, Object.extend({ scaleContent: false, scaleX: false, scaleFrom: 0, scaleMode: {originalHeight: elementDimensions.height, originalWidth: elementDimensions.width}, restoreAfterFinish: true, afterSetup: function(effect) { with(Element) { makePositioned(effect.element); makePositioned(effect.element.firstChild); if(window.opera) setStyle(effect.element, {top: ''}); makeClipping(effect.element); setStyle(effect.element, {height: '0px'}); show(element); }}, afterUpdateInternal: function(effect) { with(Element) { setStyle(effect.element.firstChild, {bottom: (effect.dims[0] - effect.element.clientHeight) + 'px' }); }}, afterFinishInternal: function(effect) { with(Element) { undoClipping(effect.element); undoPositioned(effect.element.firstChild); undoPositioned(effect.element); setStyle(effect.element.firstChild, {bottom: oldInnerBottom}); }} }, arguments[1] || {}) ); }
  
Effect.SlideUp = function(element) { element = $(element); Element.cleanWhitespace(element); var oldInnerBottom = Element.getStyle(element.firstChild, 'bottom'); return new Effect.Scale(element, 0, Object.extend({ scaleContent: false, scaleX: false, scaleMode: 'box', scaleFrom: 100, restoreAfterFinish: true, beforeStartInternal: function(effect) { with(Element) { makePositioned(effect.element); makePositioned(effect.element.firstChild); if(window.opera) setStyle(effect.element, {top: ''}); makeClipping(effect.element); show(element); }},  afterUpdateInternal: function(effect) { with(Element) { setStyle(effect.element.firstChild, {bottom: (effect.dims[0] - effect.element.clientHeight) + 'px' }); }}, afterFinishInternal: function(effect) { with(Element) { [hide, undoClipping].call(effect.element); undoPositioned(effect.element.firstChild); undoPositioned(effect.element); setStyle(effect.element.firstChild, {bottom: oldInnerBottom}); }} }, arguments[1] || {}) ); }
Effect.Squish = function(element) { return new Effect.Scale(element, window.opera ? 1 : 0, { restoreAfterFinish: true, beforeSetup: function(effect) { with(Element) { makeClipping(effect.element); }},  afterFinishInternal: function(effect) { with(Element) { hide(effect.element); undoClipping(effect.element); }} }); }
Effect.Grow = function(element) {
  element = $(element); var options = Object.extend({ direction: 'center', moveTransistion: Effect.Transitions.sinoidal, scaleTransition: Effect.Transitions.sinoidal, opacityTransition: Effect.Transitions.full }, arguments[1] || {}); var oldStyle = { top: element.style.top, left: element.style.left, height: element.style.height, width: element.style.width, opacity: Element.getInlineOpacity(element) }; var dims = Element.getDimensions(element);    var initialMoveX, initialMoveY; var moveX, moveY;
  
  switch (options.direction) {
    case 'top-left': initialMoveX = initialMoveY = moveX = moveY = 0; break; case 'top-right': initialMoveX = dims.width; initialMoveY = moveY = 0; moveX = -dims.width; break; case 'bottom-left': initialMoveX = moveX = 0; initialMoveY = dims.height; moveY = -dims.height; break; case 'bottom-right': initialMoveX = dims.width; initialMoveY = dims.height; moveX = -dims.width; moveY = -dims.height; break; case 'center': initialMoveX = dims.width / 2; initialMoveY = dims.height / 2; moveX = -dims.width / 2; moveY = -dims.height / 2; break;
  }
  
  return new Effect.Move(element, { x: initialMoveX, y: initialMoveY, duration: 0.01, beforeSetup: function(effect) { with(Element) { hide(effect.element); makeClipping(effect.element); makePositioned(effect.element); }}, afterFinishInternal: function(effect) { new Effect.Parallel( [ new Effect.Opacity(effect.element, { sync: true, to: 1.0, from: 0.0, transition: options.opacityTransition }), new Effect.Move(effect.element, { x: moveX, y: moveY, sync: true, transition: options.moveTransition }), new Effect.Scale(effect.element, 100, { scaleMode: { originalHeight: dims.height, originalWidth: dims.width }, sync: true, scaleFrom: window.opera ? 1 : 0, transition: options.scaleTransition, restoreAfterFinish: true}) ], Object.extend({ beforeSetup: function(effect) { with(Element) { setStyle(effect.effects[0].element, {height: '0px'}); show(effect.effects[0].element); }}, afterFinishInternal: function(effect) { with(Element) { [undoClipping, undoPositioned].call(effect.effects[0].element); setStyle(effect.effects[0].element, oldStyle); }} }, options) ) } });
}
Effect.Shrink = function(element) { element = $(element); var options = Object.extend({ direction: 'center', moveTransistion: Effect.Transitions.sinoidal, scaleTransition: Effect.Transitions.sinoidal, opacityTransition: Effect.Transitions.none }, arguments[1] || {}); var oldStyle = { top: element.style.top, left: element.style.left, height: element.style.height, width: element.style.width, opacity: Element.getInlineOpacity(element) }; var dims = Element.getDimensions(element); var moveX, moveY; switch (options.direction) { case 'top-left': moveX = moveY = 0; break; case 'top-right': moveX = dims.width; moveY = 0; break; case 'bottom-left': moveX = 0; moveY = dims.height; break; case 'bottom-right': moveX = dims.width; moveY = dims.height; break; case 'center':  moveX = dims.width / 2; moveY = dims.height / 2; break; }
  
  return new Effect.Parallel( [ new Effect.Opacity(element, { sync: true, to: 0.0, from: 1.0, transition: options.opacityTransition }), new Effect.Scale(element, window.opera ? 1 : 0, { sync: true, transition: options.scaleTransition, restoreAfterFinish: true}), new Effect.Move(element, { x: moveX, y: moveY, sync: true, transition: options.moveTransition }) ], Object.extend({            beforeStartInternal: function(effect) { with(Element) { [makePositioned, makeClipping].call(effect.effects[0].element) }}, afterFinishInternal: function(effect) { with(Element) { [hide, undoClipping, undoPositioned].call(effect.effects[0].element); setStyle(effect.effects[0].element, oldStyle); }} }, options) ); }
Effect.Pulsate = function(element) { element = $(element); var options    = arguments[1] || {}; var oldOpacity = Element.getInlineOpacity(element); var transition = options.transition || Effect.Transitions.sinoidal; var reverser   = function(pos){ return transition(1-Effect.Transitions.pulse(pos)) }; reverser.bind(transition); return new Effect.Opacity(element, Object.extend(Object.extend({  duration: 3.0, from: 0, afterFinishInternal: function(effect) { Element.setStyle(effect.element, {opacity: oldOpacity}); } }, options), {transition: reverser})); }
Effect.Fold = function(element) { element = $(element); var oldStyle = { top: element.style.top, left: element.style.left, width: element.style.width, height: element.style.height }; Element.makeClipping(element); return new Effect.Scale(element, 5, Object.extend({   scaleContent: false, scaleX: false, afterFinishInternal: function(effect) { new Effect.Scale(element, 1, { scaleContent: false, scaleY: false, afterFinishInternal: function(effect) { with(Element) { [hide, undoClipping].call(effect.element); setStyle(effect.element, oldStyle); }} }); }}, arguments[1] || {})); }
var fileLoadingImage = "/site_media/cbc/lthumb/images/loading.gif";		var fileBottomNavCloseImage = "/site_media/cbc/lthumb/images/closelabel.gif"; var resizeSpeed = 7; var borderSize = 10; var imageArray = new Array; var activeImage; if(resizeSpeed > 10){ resizeSpeed = 10;} if(resizeSpeed < 1){ resizeSpeed = 1;} resizeDuration = (11 - resizeSpeed) * 0.15; Object.extend(Element, { getWidth: function(element) { element = $(element); return element.offsetWidth; }, setWidth: function(element,w) { element = $(element); element.style.width = w +"px"; }, setHeight: function(element,h) { element = $(element); element.style.height = h +"px"; }, setTop: function(element,t) { element = $(element); element.style.top = t +"px"; }, setSrc: function(element,src) { element = $(element); element.src = src; }, setHref: function(element,href) { element = $(element); element.href = href; }, setInnerHTML: function(element,content) { element = $(element); element.innerHTML = content; } });
Array.prototype.removeDuplicates = function () {
	for(i = 1; i < this.length; i++){
		if(this[i][0] == this[i-1][0]){
			this.splice(i,1);
		}
	}
}
Array.prototype.empty = function () {
	for(i = 0; i <= this.length; i++){
		this.shift();
	}
}
var Lightbox = Class.create();
Lightbox.prototype = {
	initialize: function() {	
		if (!document.getElementsByTagName){ return; }
		var anchors = document.getElementsByTagName('a');
		for (var i=0; i<anchors.length; i++){ var anchor = anchors[i]; var relAttribute = String(anchor.getAttribute('rel')); if (anchor.getAttribute('href') && (relAttribute.toLowerCase().match('lightbox'))){ anchor.onclick = function () {myLightbox.start(this); return false;} } }
		var objBody = document.getElementsByTagName("body").item(0);
		
		var objOverlay = document.createElement("div");
		objOverlay.setAttribute('id','overlay');
		objOverlay.style.display = 'none';
		objOverlay.onclick = function() { myLightbox.end(); return false; }
		objBody.appendChild(objOverlay);
		
		var objLightbox = document.createElement("div");
		objLightbox.setAttribute('id','lightbox');
		objLightbox.style.display = 'none';
		objBody.appendChild(objLightbox);
	
		var objOuterImageContainer = document.createElement("div");
		objOuterImageContainer.setAttribute('id','outerImageContainer');
		objLightbox.appendChild(objOuterImageContainer);
		var objImageContainer = document.createElement("div");
		objImageContainer.setAttribute('id','imageContainer');
		objOuterImageContainer.appendChild(objImageContainer);
	
		var objLightboxImage = document.createElement("img");
		objLightboxImage.setAttribute('id','lightboxImage');
		objImageContainer.appendChild(objLightboxImage);
	
		var objHoverNav = document.createElement("div");
		objHoverNav.setAttribute('id','hoverNav');
		objImageContainer.appendChild(objHoverNav);
	
		var objPrevLink = document.createElement("a");
		objPrevLink.setAttribute('id','prevLink');
		objPrevLink.setAttribute('href','#');
		objHoverNav.appendChild(objPrevLink);
		
		var objNextLink = document.createElement("a");
		objNextLink.setAttribute('id','nextLink');
		objNextLink.setAttribute('href','#');
		objHoverNav.appendChild(objNextLink);
	
		var objLoading = document.createElement("div");
		objLoading.setAttribute('id','loading');
		objImageContainer.appendChild(objLoading);
	
		var objLoadingLink = document.createElement("a");
		objLoadingLink.setAttribute('id','loadingLink');
		objLoadingLink.setAttribute('href','#');
		objLoadingLink.onclick = function() { myLightbox.end(); return false; }
		objLoading.appendChild(objLoadingLink);
	
		var objLoadingImage = document.createElement("img");
		objLoadingImage.setAttribute('src', fileLoadingImage);
		objLoadingLink.appendChild(objLoadingImage);
		var objImageDataContainer = document.createElement("div");
		objImageDataContainer.setAttribute('id','imageDataContainer');
		objImageDataContainer.className = 'clearfix';
		objLightbox.appendChild(objImageDataContainer);
		var objImageData = document.createElement("div");
		objImageData.setAttribute('id','imageData');
		objImageDataContainer.appendChild(objImageData);
	
		var objImageDetails = document.createElement("div");
		objImageDetails.setAttribute('id','imageDetails');
		objImageData.appendChild(objImageDetails);
	
		var objCaption = document.createElement("span");
		objCaption.setAttribute('id','caption');
		objImageDetails.appendChild(objCaption);
	
		var objNumberDisplay = document.createElement("span");
		objNumberDisplay.setAttribute('id','numberDisplay');
		objImageDetails.appendChild(objNumberDisplay);
		
		var objBottomNav = document.createElement("div");
		objBottomNav.setAttribute('id','bottomNav');
		objImageData.appendChild(objBottomNav);
	
		var objBottomNavCloseLink = document.createElement("a");
		objBottomNavCloseLink.setAttribute('id','bottomNavClose');
		objBottomNavCloseLink.setAttribute('href','#');
		objBottomNavCloseLink.onclick = function() { myLightbox.end(); return false; }
		objBottomNav.appendChild(objBottomNavCloseLink);
	
		var objBottomNavCloseImage = document.createElement("img");
		objBottomNavCloseImage.setAttribute('src', fileBottomNavCloseImage);
		objBottomNavCloseLink.appendChild(objBottomNavCloseImage);
	},
	start: function(imageLink) {	hideSelectBoxes(); var arrayPageSize = getPageSize(); Element.setHeight('overlay', arrayPageSize[1]); new Effect.Appear('overlay', { duration: 0.2, from: 0.0, to: 0.8 }); imageArray = []; imageNum = 0;		if (!document.getElementsByTagName){ return; } var anchors = document.getElementsByTagName('a'); if((imageLink.getAttribute('rel') == 'lightbox')){ imageArray.push(new Array(imageLink.getAttribute('href'), imageLink.getAttribute('title')));			} else { for (var i=0; i<anchors.length; i++){ var anchor = anchors[i]; if (anchor.getAttribute('href') && (anchor.getAttribute('rel') == imageLink.getAttribute('rel'))){ imageArray.push(new Array(anchor.getAttribute('href'), anchor.getAttribute('title'))); } } imageArray.removeDuplicates(); while(imageArray[imageNum][0] != imageLink.getAttribute('href')) { imageNum++;} } var arrayPageSize = getPageSize(); var arrayPageScroll = getPageScroll(); var lightboxTop = arrayPageScroll[1] + (arrayPageSize[3] / 15); Element.setTop('lightbox', lightboxTop); Element.show('lightbox'); this.changeImage(imageNum); },
	changeImage: function(imageNum) {	
		
		activeImage = imageNum;
		Element.show('loading');
		Element.hide('lightboxImage');
		Element.hide('hoverNav');
		Element.hide('prevLink');
		Element.hide('nextLink');
		Element.hide('imageDataContainer');
		Element.hide('numberDisplay');		
		
		imgPreloader = new Image();
		
		imgPreloader.onload=function(){
			Element.setSrc('lightboxImage', imageArray[activeImage][0]);
			myLightbox.resizeImageContainer(imgPreloader.width, imgPreloader.height);
		}
		imgPreloader.src = imageArray[activeImage][0];
	},
	resizeImageContainer: function( imgWidth, imgHeight) { this.wCur = Element.getWidth('outerImageContainer'); this.hCur = Element.getHeight('outerImageContainer'); this.xScale = ((imgWidth  + (borderSize * 2)) / this.wCur) * 100; this.yScale = ((imgHeight  + (borderSize * 2)) / this.hCur) * 100; wDiff = (this.wCur - borderSize * 2) - imgWidth; hDiff = (this.hCur - borderSize * 2) - imgHeight; if(!( hDiff == 0)){ new Effect.Scale('outerImageContainer', this.yScale, {scaleX: false, duration: resizeDuration, queue: 'front'}); } if(!( wDiff == 0)){ new Effect.Scale('outerImageContainer', this.xScale, {scaleY: false, delay: resizeDuration, duration: resizeDuration}); } if((hDiff == 0) && (wDiff == 0)){ if (navigator.appVersion.indexOf("MSIE")!=-1){ pause(250); } else { pause(100);} } Element.setHeight('prevLink', imgHeight); Element.setHeight('nextLink', imgHeight); Element.setWidth( 'imageDataContainer', imgWidth + (borderSize * 2)); this.showImage(); },
	showImage: function(){
		Element.hide('loading');
		new Effect.Appear('lightboxImage', { duration: 0.5, queue: 'end', afterFinish: function(){	myLightbox.updateDetails(); } });
		this.preloadNeighborImages();
	},
	updateDetails: function() { Element.show('caption'); Element.setInnerHTML( 'caption', imageArray[activeImage][1]); if(imageArray.length > 1){ Element.show('numberDisplay'); Element.setInnerHTML( 'numberDisplay', "Image " + eval(activeImage + 1) + " of " + imageArray.length); } new Effect.Parallel( [ new Effect.SlideDown( 'imageDataContainer', { sync: true, duration: resizeDuration + 0.25, from: 0.0, to: 1.0 }), new Effect.Appear('imageDataContainer', { sync: true, duration: 1.0 }) ], { duration: 0.65, afterFinish: function() { myLightbox.updateNav();} } ); },
	updateNav: function() { Element.show('hoverNav'); if(activeImage != 0){ Element.show('prevLink'); document.getElementById('prevLink').onclick = function() { myLightbox.changeImage(activeImage - 1); return false; } } if(activeImage != (imageArray.length - 1)){ Element.show('nextLink'); document.getElementById('nextLink').onclick = function() { myLightbox.changeImage(activeImage + 1); return false; } } this.enableKeyboardNav(); },
	enableKeyboardNav: function() { document.onkeydown = this.keyboardAction; },
	disableKeyboardNav: function() { document.onkeydown = ''; },
	keyboardAction: function(e) {
		if (e == null) { keycode = event.keyCode; } else { keycode = e.which; } key = String.fromCharCode(keycode).toLowerCase(); if((key == 'x') || (key == 'o') || (key == 'c')){ myLightbox.end(); } else if(key == 'p'){ if(activeImage != 0){ myLightbox.disableKeyboardNav(); myLightbox.changeImage(activeImage - 1); } } else if(key == 'n'){ if(activeImage != (imageArray.length - 1)){ myLightbox.disableKeyboardNav(); myLightbox.changeImage(activeImage + 1); } } },
	preloadNeighborImages: function(){ if((imageArray.length - 1) > activeImage){ preloadNextImage = new Image(); preloadNextImage.src = imageArray[activeImage + 1][0]; } if(activeImage > 0){ preloadPrevImage = new Image(); preloadPrevImage.src = imageArray[activeImage - 1][0]; } },
	end: function() { this.disableKeyboardNav(); Element.hide('lightbox'); new Effect.Fade('overlay', { duration: 0.2}); showSelectBoxes(); }
}
function getPageScroll(){
	var yScroll;
	if (self.pageYOffset) {
		yScroll = self.pageYOffset;
	} else if (document.documentElement && document.documentElement.scrollTop){
		yScroll = document.documentElement.scrollTop;
	} else if (document.body) {
		yScroll = document.body.scrollTop;
	}
	arrayPageScroll = new Array('',yScroll) 
	return arrayPageScroll;
}
function getPageSize(){
	var xScroll, yScroll;
	if (window.innerHeight && window.scrollMaxY) {	xScroll = document.body.scrollWidth; yScroll = window.innerHeight + window.scrollMaxY; } else if (document.body.scrollHeight > document.body.offsetHeight){ xScroll = document.body.scrollWidth; yScroll = document.body.scrollHeight; } else { xScroll = document.body.offsetWidth; yScroll = document.body.offsetHeight; }
	
	var windowWidth, windowHeight;
	if (self.innerHeight) { windowWidth = self.innerWidth; windowHeight = self.innerHeight; } else if (document.documentElement && document.documentElement.clientHeight) { windowWidth = document.documentElement.clientWidth; windowHeight = document.documentElement.clientHeight; } else if (document.body) { windowWidth = document.body.clientWidth; windowHeight = document.body.clientHeight; }	
	
	if(yScroll < windowHeight){ pageHeight = windowHeight; } else { pageHeight = yScroll; }
	if(xScroll < windowWidth){	pageWidth = windowWidth; } else { pageWidth = xScroll; }
	arrayPageSize = new Array(pageWidth,pageHeight,windowWidth,windowHeight) 
	return arrayPageSize;
}
function getKey(e){ if (e == null) { keycode = event.keyCode; } else { keycode = e.which; } key = String.fromCharCode(keycode).toLowerCase(); if(key == 'x'){ } }
function listenKey () {	document.onkeypress = getKey; }
function showSelectBoxes(){ selects = document.getElementsByTagName("select"); for (i = 0; i != selects.length; i++) { selects[i].style.visibility = "visible"; } }
function hideSelectBoxes(){
	selects = document.getElementsByTagName("select");
	for (i = 0; i != selects.length; i++) {
		selects[i].style.visibility = "hidden";
	}
}
function pause(numberMillis) { var now = new Date(); var exitTime = now.getTime() + numberMillis; while (true) { now = new Date(); if (now.getTime() > exitTime) return; } }
function initLightbox() { myLightbox = new Lightbox(); }
Event.observe(window, 'load', initLightbox, false);



