/**
 * Created by Administrator on 2018/12/28.
 */
/*! jQuery v1.9.0 | (c) 2005, 2012 jQuery Foundation, Inc. | jquery.org/license */
var window = {};

(function (e, t) {
    "use strict";
    function n(e) {
        var t = e.length, n = st.type(e);
        return st.isWindow(e) ? !1 : 1 === e.nodeType && t ? !0 : "array" === n || "function" !== n && (0 === t || "number" == typeof t && t > 0 && t - 1 in e)
    }

    function r(e) {
        var t = Tt[e] = {};
        return st.each(e.match(lt) || [], function (e, n) {
            t[n] = !0
        }), t
    }

    function i(e, n, r, i) {
        if (st.acceptData(e)) {
            var o, a, s = st.expando, u = "string" == typeof n, l = e.nodeType,
                c = l ? st.cache : e, f = l ? e[s] : e[s] && s;
            if (f && c[f] && (i || c[f].data) || !u || r !== t)return f || (l ? e[s] = f = K.pop() || st.guid++ : f = s), c[f] || (c[f] = {}, l || (c[f].toJSON = st.noop)), ("object" == typeof n || "function" == typeof n) && (i ? c[f] = st.extend(c[f], n) : c[f].data = st.extend(c[f].data, n)), o = c[f], i || (o.data || (o.data = {}), o = o.data), r !== t && (o[st.camelCase(n)] = r), u ? (a = o[n], null == a && (a = o[st.camelCase(n)])) : a = o, a
        }
    }

    function o(e, t, n) {
        if (st.acceptData(e)) {
            var r, i, o, a = e.nodeType, u = a ? st.cache : e,
                l = a ? e[st.expando] : st.expando;
            if (u[l]) {
                if (t && (r = n ? u[l] : u[l].data)) {
                    st.isArray(t) ? t = t.concat(st.map(t, st.camelCase)) : t in r ? t = [t] : (t = st.camelCase(t), t = t in r ? [t] : t.split(" "));
                    for (i = 0, o = t.length; o > i; i++)delete r[t[i]];
                    if (!(n ? s : st.isEmptyObject)(r))return
                }
                (n || (delete u[l].data, s(u[l]))) && (a ? st.cleanData([e], !0) : st.support.deleteExpando || u != u.window ? delete u[l] : u[l] = null)
            }
        }
    }

    function a(e, n, r) {
        if (r === t && 1 === e.nodeType) {
            var i = "data-" + n.replace(Nt, "-$1").toLowerCase();
            if (r = e.getAttribute(i), "string" == typeof r) {
                try {
                    r = "true" === r ? !0 : "false" === r ? !1 : "null" === r ? null : +r + "" === r ? +r : wt.test(r) ? st.parseJSON(r) : r
                } catch (o) {
                }
                st.data(e, n, r)
            } else r = t
        }
        return r
    }

    function s(e) {
        var t;
        for (t in e)if (("data" !== t || !st.isEmptyObject(e[t])) && "toJSON" !== t)return !1;
        return !0
    }

    function u() {
        return !0
    }

    function l() {
        return !1
    }

    function c(e, t) {
        do e = e[t]; while (e && 1 !== e.nodeType);
        return e
    }

    function f(e, t, n) {
        if (t = t || 0, st.isFunction(t))return st.grep(e, function (e, r) {
            var i = !!t.call(e, r, e);
            return i === n
        });
        if (t.nodeType)return st.grep(e, function (e) {
            return e === t === n
        });
        if ("string" == typeof t) {
            var r = st.grep(e, function (e) {
                return 1 === e.nodeType
            });
            if (Wt.test(t))return st.filter(t, r, !n);
            t = st.filter(t, r)
        }
        return st.grep(e, function (e) {
            return st.inArray(e, t) >= 0 === n
        })
    }

    function p(e) {
        var t = zt.split("|"), n = e.createDocumentFragment();
        if (n.createElement)for (; t.length;)n.createElement(t.pop());
        return n
    }

    function d(e, t) {
        return e.getElementsByTagName(t)[0] || e.appendChild(e.ownerDocument.createElement(t))
    }

    function h(e) {
        var t = e.getAttributeNode("type");
        return e.type = (t && t.specified) + "/" + e.type, e
    }

    function g(e) {
        var t = nn.exec(e.type);
        return t ? e.type = t[1] : e.removeAttribute("type"), e
    }

    function m(e, t) {
        for (var n,
                 r = 0; null != (n = e[r]); r++)st._data(n, "globalEval", !t || st._data(t[r], "globalEval"))
    }

    function y(e, t) {
        if (1 === t.nodeType && st.hasData(e)) {
            var n, r, i, o = st._data(e), a = st._data(t, o), s = o.events;
            if (s) {
                delete a.handle, a.events = {};
                for (n in s)for (r = 0, i = s[n].length; i > r; r++)st.event.add(t, n, s[n][r])
            }
            a.data && (a.data = st.extend({}, a.data))
        }
    }

    function v(e, t) {
        var n, r, i;
        if (1 === t.nodeType) {
            if (n = t.nodeName.toLowerCase(), !st.support.noCloneEvent && t[st.expando]) {
                r = st._data(t);
                for (i in r.events)st.removeEvent(t, i, r.handle);
                t.removeAttribute(st.expando)
            }
            "script" === n && t.text !== e.text ? (h(t).text = e.text, g(t)) : "object" === n ? (t.parentNode && (t.outerHTML = e.outerHTML), st.support.html5Clone && e.innerHTML && !st.trim(t.innerHTML) && (t.innerHTML = e.innerHTML)) : "input" === n && Zt.test(e.type) ? (t.defaultChecked = t.checked = e.checked, t.value !== e.value && (t.value = e.value)) : "option" === n ? t.defaultSelected = t.selected = e.defaultSelected : ("input" === n || "textarea" === n) && (t.defaultValue = e.defaultValue)
        }
    }

    function b(e, n) {
        var r, i, o = 0,
            a = e.getElementsByTagName !== t ? e.getElementsByTagName(n || "*") : e.querySelectorAll !== t ? e.querySelectorAll(n || "*") : t;
        if (!a)for (a = [], r = e.childNodes || e; null != (i = r[o]); o++)!n || st.nodeName(i, n) ? a.push(i) : st.merge(a, b(i, n));
        return n === t || n && st.nodeName(e, n) ? st.merge([e], a) : a
    }

    function x(e) {
        Zt.test(e.type) && (e.defaultChecked = e.checked)
    }

    function T(e, t) {
        if (t in e)return t;
        for (var n = t.charAt(0).toUpperCase() + t.slice(1), r = t,
                 i = Nn.length; i--;)if (t = Nn[i] + n, t in e)return t;
        return r
    }

    function w(e, t) {
        return e = t || e, "none" === st.css(e, "display") || !st.contains(e.ownerDocument, e)
    }

    function N(e, t) {
        for (var n, r = [], i = 0,
                 o = e.length; o > i; i++)n = e[i], n.style && (r[i] = st._data(n, "olddisplay"), t ? (r[i] || "none" !== n.style.display || (n.style.display = ""), "" === n.style.display && w(n) && (r[i] = st._data(n, "olddisplay", S(n.nodeName)))) : r[i] || w(n) || st._data(n, "olddisplay", st.css(n, "display")));
        for (i = 0; o > i; i++)n = e[i], n.style && (t && "none" !== n.style.display && "" !== n.style.display || (n.style.display = t ? r[i] || "" : "none"));
        return e
    }

    function C(e, t, n) {
        var r = mn.exec(t);
        return r ? Math.max(0, r[1] - (n || 0)) + (r[2] || "px") : t
    }

    function k(e, t, n, r, i) {
        for (var o = n === (r ? "border" : "content") ? 4 : "width" === t ? 1 : 0,
                 a = 0; 4 > o; o += 2)"margin" === n && (a += st.css(e, n + wn[o], !0, i)), r ? ("content" === n && (a -= st.css(e, "padding" + wn[o], !0, i)), "margin" !== n && (a -= st.css(e, "border" + wn[o] + "Width", !0, i))) : (a += st.css(e, "padding" + wn[o], !0, i), "padding" !== n && (a += st.css(e, "border" + wn[o] + "Width", !0, i)));
        return a
    }

    function E(e, t, n) {
        var r = !0, i = "width" === t ? e.offsetWidth : e.offsetHeight,
            o = ln(e),
            a = st.support.boxSizing && "border-box" === st.css(e, "boxSizing", !1, o);
        if (0 >= i || null == i) {
            if (i = un(e, t, o), (0 > i || null == i) && (i = e.style[t]), yn.test(i))return i;
            r = a && (st.support.boxSizingReliable || i === e.style[t]), i = parseFloat(i) || 0
        }
        return i + k(e, t, n || (a ? "border" : "content"), r, o) + "px"
    }

    function S(e) {
        var t = V, n = bn[e];
        return n || (n = A(e, t), "none" !== n && n || (cn = (cn || st("<iframe frameborder='0' width='0' height='0'/>").css("cssText", "display:block !important")).appendTo(t.documentElement), t = (cn[0].contentWindow || cn[0].contentDocument).document, t.write("<!doctype html><html><body>"), t.close(), n = A(e, t), cn.detach()), bn[e] = n), n
    }

    function A(e, t) {
        var n = st(t.createElement(e)).appendTo(t.body),
            r = st.css(n[0], "display");
        return n.remove(), r
    }

    function j(e, t, n, r) {
        var i;
        if (st.isArray(t)) st.each(t, function (t, i) {
            n || kn.test(e) ? r(e, i) : j(e + "[" + ("object" == typeof i ? t : "") + "]", i, n, r)
        }); else if (n || "object" !== st.type(t)) r(e, t); else for (i in t)j(e + "[" + i + "]", t[i], n, r)
    }

    function D(e) {
        return function (t, n) {
            "string" != typeof t && (n = t, t = "*");
            var r, i = 0, o = t.toLowerCase().match(lt) || [];
            if (st.isFunction(n))for (; r = o[i++];)"+" === r[0] ? (r = r.slice(1) || "*", (e[r] = e[r] || []).unshift(n)) : (e[r] = e[r] || []).push(n)
        }
    }

    function L(e, n, r, i) {
        function o(u) {
            var l;
            return a[u] = !0, st.each(e[u] || [], function (e, u) {
                var c = u(n, r, i);
                return "string" != typeof c || s || a[c] ? s ? !(l = c) : t : (n.dataTypes.unshift(c), o(c), !1)
            }), l
        }

        var a = {}, s = e === $n;
        return o(n.dataTypes[0]) || !a["*"] && o("*")
    }

    function H(e, n) {
        var r, i, o = st.ajaxSettings.flatOptions || {};
        for (r in n)n[r] !== t && ((o[r] ? e : i || (i = {}))[r] = n[r]);
        return i && st.extend(!0, e, i), e
    }

    function M(e, n, r) {
        var i, o, a, s, u = e.contents, l = e.dataTypes, c = e.responseFields;
        for (o in c)o in r && (n[c[o]] = r[o]);
        for (; "*" === l[0];)l.shift(), i === t && (i = e.mimeType || n.getResponseHeader("Content-Type"));
        if (i)for (o in u)if (u[o] && u[o].test(i)) {
            l.unshift(o);
            break
        }
        if (l[0] in r) a = l[0]; else {
            for (o in r) {
                if (!l[0] || e.converters[o + " " + l[0]]) {
                    a = o;
                    break
                }
                s || (s = o)
            }
            a = a || s
        }
        return a ? (a !== l[0] && l.unshift(a), r[a]) : t
    }

    function q(e, t) {
        var n, r, i, o, a = {}, s = 0, u = e.dataTypes.slice(), l = u[0];
        if (e.dataFilter && (t = e.dataFilter(t, e.dataType)), u[1])for (n in e.converters)a[n.toLowerCase()] = e.converters[n];
        for (; i = u[++s];)if ("*" !== i) {
            if ("*" !== l && l !== i) {
                if (n = a[l + " " + i] || a["* " + i], !n)for (r in a)if (o = r.split(" "), o[1] === i && (n = a[l + " " + o[0]] || a["* " + o[0]])) {
                    n === !0 ? n = a[r] : a[r] !== !0 && (i = o[0], u.splice(s--, 0, i));
                    break
                }
                if (n !== !0)if (n && e["throws"]) t = n(t); else try {
                    t = n(t)
                } catch (c) {
                    return {
                        state: "parsererror",
                        error: n ? c : "No conversion from " + l + " to " + i
                    }
                }
            }
            l = i
        }
        return {state: "success", data: t}
    }

    function _() {
        try {
            return new e.XMLHttpRequest
        } catch (t) {
        }
    }

    function F() {
        try {
            return new e.ActiveXObject("Microsoft.XMLHTTP")
        } catch (t) {
        }
    }

    function O() {
        return setTimeout(function () {
            Qn = t
        }), Qn = st.now()
    }

    function B(e, t) {
        st.each(t, function (t, n) {
            for (var r = (rr[t] || []).concat(rr["*"]), i = 0,
                     o = r.length; o > i; i++)if (r[i].call(e, t, n))return
        })
    }

    function P(e, t, n) {
        var r, i, o = 0, a = nr.length, s = st.Deferred().always(function () {
            delete u.elem
        }), u = function () {
            if (i)return !1;
            for (var t = Qn || O(),
                     n = Math.max(0, l.startTime + l.duration - t),
                     r = n / l.duration || 0, o = 1 - r, a = 0,
                     u = l.tweens.length; u > a; a++)l.tweens[a].run(o);
            return s.notifyWith(e, [l, o, n]), 1 > o && u ? n : (s.resolveWith(e, [l]), !1)
        }, l = s.promise({
            elem: e,
            props: st.extend({}, t),
            opts: st.extend(!0, {specialEasing: {}}, n),
            originalProperties: t,
            originalOptions: n,
            startTime: Qn || O(),
            duration: n.duration,
            tweens: [],
            createTween: function (t, n) {
                var r = st.Tween(e, l.opts, t, n, l.opts.specialEasing[t] || l.opts.easing);
                return l.tweens.push(r), r
            },
            stop: function (t) {
                var n = 0, r = t ? l.tweens.length : 0;
                if (i)return this;
                for (i = !0; r > n; n++)l.tweens[n].run(1);
                return t ? s.resolveWith(e, [l, t]) : s.rejectWith(e, [l, t]), this
            }
        }), c = l.props;
        for (R(c, l.opts.specialEasing); a > o; o++)if (r = nr[o].call(l, e, c, l.opts))return r;
        return B(l, c), st.isFunction(l.opts.start) && l.opts.start.call(e, l), st.fx.timer(st.extend(u, {
            elem: e,
            anim: l,
            queue: l.opts.queue
        })), l.progress(l.opts.progress).done(l.opts.done, l.opts.complete).fail(l.opts.fail).always(l.opts.always)
    }

    function R(e, t) {
        var n, r, i, o, a;
        for (n in e)if (r = st.camelCase(n), i = t[r], o = e[n], st.isArray(o) && (i = o[1], o = e[n] = o[0]), n !== r && (e[r] = o, delete e[n]), a = st.cssHooks[r], a && "expand" in a) {
            o = a.expand(o), delete e[r];
            for (n in o)n in e || (e[n] = o[n], t[n] = i)
        } else t[r] = i
    }

    function W(e, t, n) {
        var r, i, o, a, s, u, l, c, f, p = this, d = e.style, h = {}, g = [],
            m = e.nodeType && w(e);
        n.queue || (c = st._queueHooks(e, "fx"), null == c.unqueued && (c.unqueued = 0, f = c.empty.fire, c.empty.fire = function () {
            c.unqueued || f()
        }), c.unqueued++, p.always(function () {
            p.always(function () {
                c.unqueued--, st.queue(e, "fx").length || c.empty.fire()
            })
        })), 1 === e.nodeType && ("height" in t || "width" in t) && (n.overflow = [d.overflow, d.overflowX, d.overflowY], "inline" === st.css(e, "display") && "none" === st.css(e, "float") && (st.support.inlineBlockNeedsLayout && "inline" !== S(e.nodeName) ? d.zoom = 1 : d.display = "inline-block")), n.overflow && (d.overflow = "hidden", st.support.shrinkWrapBlocks || p.done(function () {
            d.overflow = n.overflow[0], d.overflowX = n.overflow[1], d.overflowY = n.overflow[2]
        }));
        for (r in t)if (o = t[r], Zn.exec(o)) {
            if (delete t[r], u = u || "toggle" === o, o === (m ? "hide" : "show"))continue;
            g.push(r)
        }
        if (a = g.length) {
            s = st._data(e, "fxshow") || st._data(e, "fxshow", {}), "hidden" in s && (m = s.hidden), u && (s.hidden = !m), m ? st(e).show() : p.done(function () {
                st(e).hide()
            }), p.done(function () {
                var t;
                st._removeData(e, "fxshow");
                for (t in h)st.style(e, t, h[t])
            });
            for (r = 0; a > r; r++)i = g[r], l = p.createTween(i, m ? s[i] : 0), h[i] = s[i] || st.style(e, i), i in s || (s[i] = l.start, m && (l.end = l.start, l.start = "width" === i || "height" === i ? 1 : 0))
        }
    }

    function $(e, t, n, r, i) {
        return new $.prototype.init(e, t, n, r, i)
    }

    function I(e, t) {
        var n, r = {height: e}, i = 0;
        for (t = t ? 1 : 0; 4 > i; i += 2 - t)n = wn[i], r["margin" + n] = r["padding" + n] = e;
        return t && (r.opacity = r.width = e), r
    }

    function z(e) {
        return st.isWindow(e) ? e : 9 === e.nodeType ? e.defaultView || e.parentWindow : !1
    }

    var X, U, V = e.document, Y = e.location, J = e.jQuery, G = e.$, Q = {},
        K = [], Z = "1.9.0", et = K.concat, tt = K.push, nt = K.slice,
        rt = K.indexOf, it = Q.toString, ot = Q.hasOwnProperty, at = Z.trim,
        st = function (e, t) {
            return new st.fn.init(e, t, X)
        }, ut = /[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/.source, lt = /\S+/g,
        ct = /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,
        ft = /^(?:(<[\w\W]+>)[^>]*|#([\w-]*))$/,
        pt = /^<(\w+)\s*\/?>(?:<\/\1>|)$/, dt = /^[\],:{}\s]*$/,
        ht = /(?:^|:|,)(?:\s*\[)+/g, gt = /\\(?:["\\\/bfnrt]|u[\da-fA-F]{4})/g,
        mt = /"[^"\\\r\n]*"|true|false|null|-?(?:\d+\.|)\d+(?:[eE][+-]?\d+|)/g,
        yt = /^-ms-/, vt = /-([\da-z])/gi, bt = function (e, t) {
            return t.toUpperCase()
        }, xt = function () {
            V.addEventListener ? (V.removeEventListener("DOMContentLoaded", xt, !1), st.ready()) : "complete" === V.readyState && (V.detachEvent("onreadystatechange", xt), st.ready())
        };
    st.fn = st.prototype = {
        jquery: Z,
        constructor: st,
        init: function (e, n, r) {
            var i, o;
            if (!e)return this;
            if ("string" == typeof e) {
                if (i = "<" === e.charAt(0) && ">" === e.charAt(e.length - 1) && e.length >= 3 ? [null, e, null] : ft.exec(e), !i || !i[1] && n)return !n || n.jquery ? (n || r).find(e) : this.constructor(n).find(e);
                if (i[1]) {
                    if (n = n instanceof st ? n[0] : n, st.merge(this, st.parseHTML(i[1], n && n.nodeType ? n.ownerDocument || n : V, !0)), pt.test(i[1]) && st.isPlainObject(n))for (i in n)st.isFunction(this[i]) ? this[i](n[i]) : this.attr(i, n[i]);
                    return this
                }
                if (o = V.getElementById(i[2]), o && o.parentNode) {
                    if (o.id !== i[2])return r.find(e);
                    this.length = 1, this[0] = o
                }
                return this.context = V, this.selector = e, this
            }
            return e.nodeType ? (this.context = this[0] = e, this.length = 1, this) : st.isFunction(e) ? r.ready(e) : (e.selector !== t && (this.selector = e.selector, this.context = e.context), st.makeArray(e, this))
        },
        selector: "",
        length: 0,
        size: function () {
            return this.length
        },
        toArray: function () {
            return nt.call(this)
        },
        get: function (e) {
            return null == e ? this.toArray() : 0 > e ? this[this.length + e] : this[e]
        },
        pushStack: function (e) {
            var t = st.merge(this.constructor(), e);
            return t.prevObject = this, t.context = this.context, t
        },
        each: function (e, t) {
            return st.each(this, e, t)
        },
        ready: function (e) {
            return st.ready.promise().done(e), this
        },
        slice: function () {
            return this.pushStack(nt.apply(this, arguments))
        },
        first: function () {
            return this.eq(0)
        },
        last: function () {
            return this.eq(-1)
        },
        eq: function (e) {
            var t = this.length, n = +e + (0 > e ? t : 0);
            return this.pushStack(n >= 0 && t > n ? [this[n]] : [])
        },
        map: function (e) {
            return this.pushStack(st.map(this, function (t, n) {
                return e.call(t, n, t)
            }))
        },
        end: function () {
            return this.prevObject || this.constructor(null)
        },
        push: tt,
        sort: [].sort,
        splice: [].splice
    }, st.fn.init.prototype = st.fn, st.extend = st.fn.extend = function () {
        var e, n, r, i, o, a, s = arguments[0] || {}, u = 1,
            l = arguments.length, c = !1;
        for ("boolean" == typeof s && (c = s, s = arguments[1] || {}, u = 2), "object" == typeof s || st.isFunction(s) || (s = {}), l === u && (s = this, --u); l > u; u++)if (null != (e = arguments[u]))for (n in e)r = s[n], i = e[n], s !== i && (c && i && (st.isPlainObject(i) || (o = st.isArray(i))) ? (o ? (o = !1, a = r && st.isArray(r) ? r : []) : a = r && st.isPlainObject(r) ? r : {}, s[n] = st.extend(c, a, i)) : i !== t && (s[n] = i));
        return s
    }, st.extend({
        noConflict: function (t) {
            return e.$ === st && (e.$ = G), t && e.jQuery === st && (e.jQuery = J), st
        }, isReady: !1, readyWait: 1, holdReady: function (e) {
            e ? st.readyWait++ : st.ready(!0)
        }, ready: function (e) {
            if (e === !0 ? !--st.readyWait : !st.isReady) {
                if (!V.body)return setTimeout(st.ready);
                st.isReady = !0, e !== !0 && --st.readyWait > 0 || (U.resolveWith(V, [st]), st.fn.trigger && st(V).trigger("ready").off("ready"))
            }
        }, isFunction: function (e) {
            return "function" === st.type(e)
        }, isArray: Array.isArray || function (e) {
            return "array" === st.type(e)
        }, isWindow: function (e) {
            return null != e && e == e.window
        }, isNumeric: function (e) {
            return !isNaN(parseFloat(e)) && isFinite(e)
        }, type: function (e) {
            return null == e ? e + "" : "object" == typeof e || "function" == typeof e ? Q[it.call(e)] || "object" : typeof e
        }, isPlainObject: function (e) {
            if (!e || "object" !== st.type(e) || e.nodeType || st.isWindow(e))return !1;
            try {
                if (e.constructor && !ot.call(e, "constructor") && !ot.call(e.constructor.prototype, "isPrototypeOf"))return !1
            } catch (n) {
                return !1
            }
            var r;
            for (r in e);
            return r === t || ot.call(e, r)
        }, isEmptyObject: function (e) {
            var t;
            for (t in e)return !1;
            return !0
        }, error: function (e) {
            throw Error(e)
        }, parseHTML: function (e, t, n) {
            if (!e || "string" != typeof e)return null;
            "boolean" == typeof t && (n = t, t = !1), t = t || V;
            var r = pt.exec(e), i = !n && [];
            return r ? [t.createElement(r[1])] : (r = st.buildFragment([e], t, i), i && st(i).remove(), st.merge([], r.childNodes))
        }, parseJSON: function (n) {
            return e.JSON && e.JSON.parse ? e.JSON.parse(n) : null === n ? n : "string" == typeof n && (n = st.trim(n), n && dt.test(n.replace(gt, "@").replace(mt, "]").replace(ht, ""))) ? Function("return " + n)() : (st.error("Invalid JSON: " + n), t)
        }, parseXML: function (n) {
            var r, i;
            if (!n || "string" != typeof n)return null;
            try {
                e.DOMParser ? (i = new DOMParser, r = i.parseFromString(n, "text/xml")) : (r = new ActiveXObject("Microsoft.XMLDOM"), r.async = "false", r.loadXML(n))
            } catch (o) {
                r = t
            }
            return r && r.documentElement && !r.getElementsByTagName("parsererror").length || st.error("Invalid XML: " + n), r
        }, noop: function () {
        }, globalEval: function (t) {
            t && st.trim(t) && (e.execScript || function (t) {
                e.eval.call(e, t)
            })(t)
        }, camelCase: function (e) {
            return e.replace(yt, "ms-").replace(vt, bt)
        }, nodeName: function (e, t) {
            return e.nodeName && e.nodeName.toLowerCase() === t.toLowerCase()
        }, each: function (e, t, r) {
            var i, o = 0, a = e.length, s = n(e);
            if (r) {
                if (s)for (; a > o && (i = t.apply(e[o], r), i !== !1); o++); else for (o in e)if (i = t.apply(e[o], r), i === !1)break
            } else if (s)for (; a > o && (i = t.call(e[o], o, e[o]), i !== !1); o++); else for (o in e)if (i = t.call(e[o], o, e[o]), i === !1)break;
            return e
        }, trim: at && !at.call("\ufeff\u00a0") ? function (e) {
            return null == e ? "" : at.call(e)
        } : function (e) {
            return null == e ? "" : (e + "").replace(ct, "")
        }, makeArray: function (e, t) {
            var r = t || [];
            return null != e && (n(Object(e)) ? st.merge(r, "string" == typeof e ? [e] : e) : tt.call(r, e)), r
        }, inArray: function (e, t, n) {
            var r;
            if (t) {
                if (rt)return rt.call(t, e, n);
                for (r = t.length, n = n ? 0 > n ? Math.max(0, r + n) : n : 0; r > n; n++)if (n in t && t[n] === e)return n
            }
            return -1
        }, merge: function (e, n) {
            var r = n.length, i = e.length, o = 0;
            if ("number" == typeof r)for (; r > o; o++)e[i++] = n[o]; else for (; n[o] !== t;)e[i++] = n[o++];
            return e.length = i, e
        }, grep: function (e, t, n) {
            var r, i = [], o = 0, a = e.length;
            for (n = !!n; a > o; o++)r = !!t(e[o], o), n !== r && i.push(e[o]);
            return i
        }, map: function (e, t, r) {
            var i, o = 0, a = e.length, s = n(e), u = [];
            if (s)for (; a > o; o++)i = t(e[o], o, r), null != i && (u[u.length] = i); else for (o in e)i = t(e[o], o, r), null != i && (u[u.length] = i);
            return et.apply([], u)
        }, guid: 1, proxy: function (e, n) {
            var r, i, o;
            return "string" == typeof n && (r = e[n], n = e, e = r), st.isFunction(e) ? (i = nt.call(arguments, 2), o = function () {
                return e.apply(n || this, i.concat(nt.call(arguments)))
            }, o.guid = e.guid = e.guid || st.guid++, o) : t
        }, access: function (e, n, r, i, o, a, s) {
            var u = 0, l = e.length, c = null == r;
            if ("object" === st.type(r)) {
                o = !0;
                for (u in r)st.access(e, n, u, r[u], !0, a, s)
            } else if (i !== t && (o = !0, st.isFunction(i) || (s = !0), c && (s ? (n.call(e, i), n = null) : (c = n, n = function (e, t, n) {
                    return c.call(st(e), n)
                })), n))for (; l > u; u++)n(e[u], r, s ? i : i.call(e[u], u, n(e[u], r)));
            return o ? e : c ? n.call(e) : l ? n(e[0], r) : a
        }, now: function () {
            return (new Date).getTime()
        }
    }), st.ready.promise = function (t) {
        if (!U)if (U = st.Deferred(), "complete" === V.readyState) setTimeout(st.ready); else if (V.addEventListener) V.addEventListener("DOMContentLoaded", xt, !1), e.addEventListener("load", st.ready, !1); else {
            V.attachEvent("onreadystatechange", xt), e.attachEvent("onload", st.ready);
            var n = !1;
            try {
                n = null == e.frameElement && V.documentElement
            } catch (r) {
            }
            n && n.doScroll && function i() {
                if (!st.isReady) {
                    try {
                        n.doScroll("left")
                    } catch (e) {
                        return setTimeout(i, 50)
                    }
                    st.ready()
                }
            }()
        }
        return U.promise(t)
    }, st.each("Boolean Number String Function Array Date RegExp Object Error".split(" "), function (e, t) {
        Q["[object " + t + "]"] = t.toLowerCase()
    }), X = st(V);
    var Tt = {};
    st.Callbacks = function (e) {
        e = "string" == typeof e ? Tt[e] || r(e) : st.extend({}, e);
        var n, i, o, a, s, u, l = [], c = !e.once && [], f = function (t) {
            for (n = e.memory && t, i = !0, u = a || 0, a = 0, s = l.length, o = !0; l && s > u; u++)if (l[u].apply(t[0], t[1]) === !1 && e.stopOnFalse) {
                n = !1;
                break
            }
            o = !1, l && (c ? c.length && f(c.shift()) : n ? l = [] : p.disable())
        }, p = {
            add: function () {
                if (l) {
                    var t = l.length;
                    (function r(t) {
                        st.each(t, function (t, n) {
                            var i = st.type(n);
                            "function" === i ? e.unique && p.has(n) || l.push(n) : n && n.length && "string" !== i && r(n)
                        })
                    })(arguments), o ? s = l.length : n && (a = t, f(n))
                }
                return this
            }, remove: function () {
                return l && st.each(arguments, function (e, t) {
                    for (var n; (n = st.inArray(t, l, n)) > -1;)l.splice(n, 1), o && (s >= n && s--, u >= n && u--)
                }), this
            }, has: function (e) {
                return st.inArray(e, l) > -1
            }, empty: function () {
                return l = [], this
            }, disable: function () {
                return l = c = n = t, this
            }, disabled: function () {
                return !l
            }, lock: function () {
                return c = t, n || p.disable(), this
            }, locked: function () {
                return !c
            }, fireWith: function (e, t) {
                return t = t || [], t = [e, t.slice ? t.slice() : t], !l || i && !c || (o ? c.push(t) : f(t)), this
            }, fire: function () {
                return p.fireWith(this, arguments), this
            }, fired: function () {
                return !!i
            }
        };
        return p
    }, st.extend({
        Deferred: function (e) {
            var t = [["resolve", "done", st.Callbacks("once memory"), "resolved"], ["reject", "fail", st.Callbacks("once memory"), "rejected"], ["notify", "progress", st.Callbacks("memory")]],
                n = "pending", r = {
                    state: function () {
                        return n
                    }, always: function () {
                        return i.done(arguments).fail(arguments), this
                    }, then: function () {
                        var e = arguments;
                        return st.Deferred(function (n) {
                            st.each(t, function (t, o) {
                                var a = o[0], s = st.isFunction(e[t]) && e[t];
                                i[o[1]](function () {
                                    var e = s && s.apply(this, arguments);
                                    e && st.isFunction(e.promise) ? e.promise().done(n.resolve).fail(n.reject).progress(n.notify) : n[a + "With"](this === r ? n.promise() : this, s ? [e] : arguments)
                                })
                            }), e = null
                        }).promise()
                    }, promise: function (e) {
                        return null != e ? st.extend(e, r) : r
                    }
                }, i = {};
            return r.pipe = r.then, st.each(t, function (e, o) {
                var a = o[2], s = o[3];
                r[o[1]] = a.add, s && a.add(function () {
                    n = s
                }, t[1 ^ e][2].disable, t[2][2].lock), i[o[0]] = function () {
                    return i[o[0] + "With"](this === i ? r : this, arguments), this
                }, i[o[0] + "With"] = a.fireWith
            }), r.promise(i), e && e.call(i, i), i
        }, when: function (e) {
            var t, n, r, i = 0, o = nt.call(arguments), a = o.length,
                s = 1 !== a || e && st.isFunction(e.promise) ? a : 0,
                u = 1 === s ? e : st.Deferred(), l = function (e, n, r) {
                    return function (i) {
                        n[e] = this, r[e] = arguments.length > 1 ? nt.call(arguments) : i, r === t ? u.notifyWith(n, r) : --s || u.resolveWith(n, r)
                    }
                };
            if (a > 1)for (t = Array(a), n = Array(a), r = Array(a); a > i; i++)o[i] && st.isFunction(o[i].promise) ? o[i].promise().done(l(i, r, o)).fail(u.reject).progress(l(i, n, t)) : --s;
            return s || u.resolveWith(r, o), u.promise()
        }
    }), st.support = function () {
        var n, r, i, o, a, s, u, l, c, f, p = V.createElement("div");
        if (p.setAttribute("className", "t"), p.innerHTML = "  <link/><table></table><a href='/a'>a</a><input type='checkbox'/>", r = p.getElementsByTagName("*"), i = p.getElementsByTagName("a")[0], !r || !i || !r.length)return {};
        o = V.createElement("select"), a = o.appendChild(V.createElement("option")), s = p.getElementsByTagName("input")[0], i.style.cssText = "top:1px;float:left;opacity:.5", n = {
            getSetAttribute: "t" !== p.className,
            leadingWhitespace: 3 === p.firstChild.nodeType,
            tbody: !p.getElementsByTagName("tbody").length,
            htmlSerialize: !!p.getElementsByTagName("link").length,
            style: /top/.test(i.getAttribute("style")),
            hrefNormalized: "/a" === i.getAttribute("href"),
            opacity: /^0.5/.test(i.style.opacity),
            cssFloat: !!i.style.cssFloat,
            checkOn: !!s.value,
            optSelected: a.selected,
            enctype: !!V.createElement("form").enctype,
            html5Clone: "<:nav></:nav>" !== V.createElement("nav").cloneNode(!0).outerHTML,
            boxModel: "CSS1Compat" === V.compatMode,
            deleteExpando: !0,
            noCloneEvent: !0,
            inlineBlockNeedsLayout: !1,
            shrinkWrapBlocks: !1,
            reliableMarginRight: !0,
            boxSizingReliable: !0,
            pixelPosition: !1
        }, s.checked = !0, n.noCloneChecked = s.cloneNode(!0).checked, o.disabled = !0, n.optDisabled = !a.disabled;
        try {
            delete p.test
        } catch (d) {
            n.deleteExpando = !1
        }
        s = V.createElement("input"), s.setAttribute("value", ""), n.input = "" === s.getAttribute("value"), s.value = "t", s.setAttribute("type", "radio"), n.radioValue = "t" === s.value, s.setAttribute("checked", "t"), s.setAttribute("name", "t"), u = V.createDocumentFragment(), u.appendChild(s), n.appendChecked = s.checked, n.checkClone = u.cloneNode(!0).cloneNode(!0).lastChild.checked, p.attachEvent && (p.attachEvent("onclick", function () {
            n.noCloneEvent = !1
        }), p.cloneNode(!0).click());
        for (f in{
            submit: !0,
            change: !0,
            focusin: !0
        })p.setAttribute(l = "on" + f, "t"), n[f + "Bubbles"] = l in e || p.attributes[l].expando === !1;
        return p.style.backgroundClip = "content-box", p.cloneNode(!0).style.backgroundClip = "", n.clearCloneStyle = "content-box" === p.style.backgroundClip, st(function () {
            var r, i, o,
                a = "padding:0;margin:0;border:0;display:block;box-sizing:content-box;-moz-box-sizing:content-box;-webkit-box-sizing:content-box;",
                s = V.getElementsByTagName("body")[0];
            s && (r = V.createElement("div"), r.style.cssText = "border:0;width:0;height:0;position:absolute;top:0;left:-9999px;margin-top:1px", s.appendChild(r).appendChild(p), p.innerHTML = "<table><tr><td></td><td>t</td></tr></table>", o = p.getElementsByTagName("td"), o[0].style.cssText = "padding:0;margin:0;border:0;display:none", c = 0 === o[0].offsetHeight, o[0].style.display = "", o[1].style.display = "none", n.reliableHiddenOffsets = c && 0 === o[0].offsetHeight, p.innerHTML = "", p.style.cssText = "box-sizing:border-box;-moz-box-sizing:border-box;-webkit-box-sizing:border-box;padding:1px;border:1px;display:block;width:4px;margin-top:1%;position:absolute;top:1%;", n.boxSizing = 4 === p.offsetWidth, n.doesNotIncludeMarginInBodyOffset = 1 !== s.offsetTop, e.getComputedStyle && (n.pixelPosition = "1%" !== (e.getComputedStyle(p, null) || {}).top, n.boxSizingReliable = "4px" === (e.getComputedStyle(p, null) || {width: "4px"}).width, i = p.appendChild(V.createElement("div")), i.style.cssText = p.style.cssText = a, i.style.marginRight = i.style.width = "0", p.style.width = "1px", n.reliableMarginRight = !parseFloat((e.getComputedStyle(i, null) || {}).marginRight)), p.style.zoom !== t && (p.innerHTML = "", p.style.cssText = a + "width:1px;padding:1px;display:inline;zoom:1", n.inlineBlockNeedsLayout = 3 === p.offsetWidth, p.style.display = "block", p.innerHTML = "<div></div>", p.firstChild.style.width = "5px", n.shrinkWrapBlocks = 3 !== p.offsetWidth, s.style.zoom = 1), s.removeChild(r), r = p = o = i = null)
        }), r = o = u = a = i = s = null, n
    }();
    var wt = /(?:\{[\s\S]*\}|\[[\s\S]*\])$/, Nt = /([A-Z])/g;
    st.extend({
        cache: {},
        expando: "jQuery" + (Z + Math.random()).replace(/\D/g, ""),
        noData: {
            embed: !0,
            object: "clsid:D27CDB6E-AE6D-11cf-96B8-444553540000",
            applet: !0
        },
        hasData: function (e) {
            return e = e.nodeType ? st.cache[e[st.expando]] : e[st.expando], !!e && !s(e)
        },
        data: function (e, t, n) {
            return i(e, t, n, !1)
        },
        removeData: function (e, t) {
            return o(e, t, !1)
        },
        _data: function (e, t, n) {
            return i(e, t, n, !0)
        },
        _removeData: function (e, t) {
            return o(e, t, !0)
        },
        acceptData: function (e) {
            var t = e.nodeName && st.noData[e.nodeName.toLowerCase()];
            return !t || t !== !0 && e.getAttribute("classid") === t
        }
    }), st.fn.extend({
        data: function (e, n) {
            var r, i, o = this[0], s = 0, u = null;
            if (e === t) {
                if (this.length && (u = st.data(o), 1 === o.nodeType && !st._data(o, "parsedAttrs"))) {
                    for (r = o.attributes; r.length > s; s++)i = r[s].name, i.indexOf("data-") || (i = st.camelCase(i.substring(5)), a(o, i, u[i]));
                    st._data(o, "parsedAttrs", !0)
                }
                return u
            }
            return "object" == typeof e ? this.each(function () {
                st.data(this, e)
            }) : st.access(this, function (n) {
                return n === t ? o ? a(o, e, st.data(o, e)) : null : (this.each(function () {
                    st.data(this, e, n)
                }), t)
            }, null, n, arguments.length > 1, null, !0)
        }, removeData: function (e) {
            return this.each(function () {
                st.removeData(this, e)
            })
        }
    }), st.extend({
        queue: function (e, n, r) {
            var i;
            return e ? (n = (n || "fx") + "queue", i = st._data(e, n), r && (!i || st.isArray(r) ? i = st._data(e, n, st.makeArray(r)) : i.push(r)), i || []) : t
        }, dequeue: function (e, t) {
            t = t || "fx";
            var n = st.queue(e, t), r = n.length, i = n.shift(),
                o = st._queueHooks(e, t), a = function () {
                    st.dequeue(e, t)
                };
            "inprogress" === i && (i = n.shift(), r--), o.cur = i, i && ("fx" === t && n.unshift("inprogress"), delete o.stop, i.call(e, a, o)), !r && o && o.empty.fire()
        }, _queueHooks: function (e, t) {
            var n = t + "queueHooks";
            return st._data(e, n) || st._data(e, n, {
                    empty: st.Callbacks("once memory").add(function () {
                        st._removeData(e, t + "queue"), st._removeData(e, n)
                    })
                })
        }
    }), st.fn.extend({
        queue: function (e, n) {
            var r = 2;
            return "string" != typeof e && (n = e, e = "fx", r--), r > arguments.length ? st.queue(this[0], e) : n === t ? this : this.each(function () {
                var t = st.queue(this, e, n);
                st._queueHooks(this, e), "fx" === e && "inprogress" !== t[0] && st.dequeue(this, e)
            })
        }, dequeue: function (e) {
            return this.each(function () {
                st.dequeue(this, e)
            })
        }, delay: function (e, t) {
            return e = st.fx ? st.fx.speeds[e] || e : e, t = t || "fx", this.queue(t, function (t, n) {
                var r = setTimeout(t, e);
                n.stop = function () {
                    clearTimeout(r)
                }
            })
        }, clearQueue: function (e) {
            return this.queue(e || "fx", [])
        }, promise: function (e, n) {
            var r, i = 1, o = st.Deferred(), a = this, s = this.length,
                u = function () {
                    --i || o.resolveWith(a, [a])
                };
            for ("string" != typeof e && (n = e, e = t), e = e || "fx"; s--;)r = st._data(a[s], e + "queueHooks"), r && r.empty && (i++, r.empty.add(u));
            return u(), o.promise(n)
        }
    });
    var Ct, kt, Et = /[\t\r\n]/g, St = /\r/g,
        At = /^(?:input|select|textarea|button|object)$/i, jt = /^(?:a|area)$/i,
        Dt = /^(?:checked|selected|autofocus|autoplay|async|controls|defer|disabled|hidden|loop|multiple|open|readonly|required|scoped)$/i,
        Lt = /^(?:checked|selected)$/i, Ht = st.support.getSetAttribute,
        Mt = st.support.input;
    st.fn.extend({
        attr: function (e, t) {
            return st.access(this, st.attr, e, t, arguments.length > 1)
        }, removeAttr: function (e) {
            return this.each(function () {
                st.removeAttr(this, e)
            })
        }, prop: function (e, t) {
            return st.access(this, st.prop, e, t, arguments.length > 1)
        }, removeProp: function (e) {
            return e = st.propFix[e] || e, this.each(function () {
                try {
                    this[e] = t, delete this[e]
                } catch (n) {
                }
            })
        }, addClass: function (e) {
            var t, n, r, i, o, a = 0, s = this.length,
                u = "string" == typeof e && e;
            if (st.isFunction(e))return this.each(function (t) {
                st(this).addClass(e.call(this, t, this.className))
            });
            if (u)for (t = (e || "").match(lt) || []; s > a; a++)if (n = this[a], r = 1 === n.nodeType && (n.className ? (" " + n.className + " ").replace(Et, " ") : " ")) {
                for (o = 0; i = t[o++];)0 > r.indexOf(" " + i + " ") && (r += i + " ");
                n.className = st.trim(r)
            }
            return this
        }, removeClass: function (e) {
            var t, n, r, i, o, a = 0, s = this.length,
                u = 0 === arguments.length || "string" == typeof e && e;
            if (st.isFunction(e))return this.each(function (t) {
                st(this).removeClass(e.call(this, t, this.className))
            });
            if (u)for (t = (e || "").match(lt) || []; s > a; a++)if (n = this[a], r = 1 === n.nodeType && (n.className ? (" " + n.className + " ").replace(Et, " ") : "")) {
                for (o = 0; i = t[o++];)for (; r.indexOf(" " + i + " ") >= 0;)r = r.replace(" " + i + " ", " ");
                n.className = e ? st.trim(r) : ""
            }
            return this
        }, toggleClass: function (e, t) {
            var n = typeof e, r = "boolean" == typeof t;
            return st.isFunction(e) ? this.each(function (n) {
                st(this).toggleClass(e.call(this, n, this.className, t), t)
            }) : this.each(function () {
                if ("string" === n)for (var i, o = 0, a = st(this), s = t,
                                            u = e.match(lt) || []; i = u[o++];)s = r ? s : !a.hasClass(i), a[s ? "addClass" : "removeClass"](i); else("undefined" === n || "boolean" === n) && (this.className && st._data(this, "__className__", this.className), this.className = this.className || e === !1 ? "" : st._data(this, "__className__") || "")
            })
        }, hasClass: function (e) {
            for (var t = " " + e + " ", n = 0,
                     r = this.length; r > n; n++)if (1 === this[n].nodeType && (" " + this[n].className + " ").replace(Et, " ").indexOf(t) >= 0)return !0;
            return !1
        }, val: function (e) {
            var n, r, i, o = this[0];
            {
                if (arguments.length)return i = st.isFunction(e), this.each(function (r) {
                    var o, a = st(this);
                    1 === this.nodeType && (o = i ? e.call(this, r, a.val()) : e, null == o ? o = "" : "number" == typeof o ? o += "" : st.isArray(o) && (o = st.map(o, function (e) {
                            return null == e ? "" : e + ""
                        })), n = st.valHooks[this.type] || st.valHooks[this.nodeName.toLowerCase()], n && "set" in n && n.set(this, o, "value") !== t || (this.value = o))
                });
                if (o)return n = st.valHooks[o.type] || st.valHooks[o.nodeName.toLowerCase()], n && "get" in n && (r = n.get(o, "value")) !== t ? r : (r = o.value, "string" == typeof r ? r.replace(St, "") : null == r ? "" : r)
            }
        }
    }), st.extend({
        valHooks: {
            option: {
                get: function (e) {
                    var t = e.attributes.value;
                    return !t || t.specified ? e.value : e.text
                }
            }, select: {
                get: function (e) {
                    for (var t, n, r = e.options, i = e.selectedIndex,
                             o = "select-one" === e.type || 0 > i,
                             a = o ? null : [], s = o ? i + 1 : r.length,
                             u = 0 > i ? s : o ? i : 0; s > u; u++)if (n = r[u], !(!n.selected && u !== i || (st.support.optDisabled ? n.disabled : null !== n.getAttribute("disabled")) || n.parentNode.disabled && st.nodeName(n.parentNode, "optgroup"))) {
                        if (t = st(n).val(), o)return t;
                        a.push(t)
                    }
                    return a
                }, set: function (e, t) {
                    var n = st.makeArray(t);
                    return st(e).find("option").each(function () {
                        this.selected = st.inArray(st(this).val(), n) >= 0
                    }), n.length || (e.selectedIndex = -1), n
                }
            }
        },
        attr: function (e, n, r) {
            var i, o, a, s = e.nodeType;
            if (e && 3 !== s && 8 !== s && 2 !== s)return e.getAttribute === t ? st.prop(e, n, r) : (a = 1 !== s || !st.isXMLDoc(e), a && (n = n.toLowerCase(), o = st.attrHooks[n] || (Dt.test(n) ? kt : Ct)), r === t ? o && a && "get" in o && null !== (i = o.get(e, n)) ? i : (e.getAttribute !== t && (i = e.getAttribute(n)), null == i ? t : i) : null !== r ? o && a && "set" in o && (i = o.set(e, r, n)) !== t ? i : (e.setAttribute(n, r + ""), r) : (st.removeAttr(e, n), t))
        },
        removeAttr: function (e, t) {
            var n, r, i = 0, o = t && t.match(lt);
            if (o && 1 === e.nodeType)for (; n = o[i++];)r = st.propFix[n] || n, Dt.test(n) ? !Ht && Lt.test(n) ? e[st.camelCase("default-" + n)] = e[r] = !1 : e[r] = !1 : st.attr(e, n, ""), e.removeAttribute(Ht ? n : r)
        },
        attrHooks: {
            type: {
                set: function (e, t) {
                    if (!st.support.radioValue && "radio" === t && st.nodeName(e, "input")) {
                        var n = e.value;
                        return e.setAttribute("type", t), n && (e.value = n), t
                    }
                }
            }
        },
        propFix: {
            tabindex: "tabIndex",
            readonly: "readOnly",
            "for": "htmlFor",
            "class": "className",
            maxlength: "maxLength",
            cellspacing: "cellSpacing",
            cellpadding: "cellPadding",
            rowspan: "rowSpan",
            colspan: "colSpan",
            usemap: "useMap",
            frameborder: "frameBorder",
            contenteditable: "contentEditable"
        },
        prop: function (e, n, r) {
            var i, o, a, s = e.nodeType;
            if (e && 3 !== s && 8 !== s && 2 !== s)return a = 1 !== s || !st.isXMLDoc(e), a && (n = st.propFix[n] || n, o = st.propHooks[n]), r !== t ? o && "set" in o && (i = o.set(e, r, n)) !== t ? i : e[n] = r : o && "get" in o && null !== (i = o.get(e, n)) ? i : e[n]
        },
        propHooks: {
            tabIndex: {
                get: function (e) {
                    var n = e.getAttributeNode("tabindex");
                    return n && n.specified ? parseInt(n.value, 10) : At.test(e.nodeName) || jt.test(e.nodeName) && e.href ? 0 : t
                }
            }
        }
    }), kt = {
        get: function (e, n) {
            var r = st.prop(e, n),
                i = "boolean" == typeof r && e.getAttribute(n),
                o = "boolean" == typeof r ? Mt && Ht ? null != i : Lt.test(n) ? e[st.camelCase("default-" + n)] : !!i : e.getAttributeNode(n);
            return o && o.value !== !1 ? n.toLowerCase() : t
        }, set: function (e, t, n) {
            return t === !1 ? st.removeAttr(e, n) : Mt && Ht || !Lt.test(n) ? e.setAttribute(!Ht && st.propFix[n] || n, n) : e[st.camelCase("default-" + n)] = e[n] = !0, n
        }
    }, Mt && Ht || (st.attrHooks.value = {
        get: function (e, n) {
            var r = e.getAttributeNode(n);
            return st.nodeName(e, "input") ? e.defaultValue : r && r.specified ? r.value : t
        }, set: function (e, n, r) {
            return st.nodeName(e, "input") ? (e.defaultValue = n, t) : Ct && Ct.set(e, n, r)
        }
    }), Ht || (Ct = st.valHooks.button = {
        get: function (e, n) {
            var r = e.getAttributeNode(n);
            return r && ("id" === n || "name" === n || "coords" === n ? "" !== r.value : r.specified) ? r.value : t
        }, set: function (e, n, r) {
            var i = e.getAttributeNode(r);
            return i || e.setAttributeNode(i = e.ownerDocument.createAttribute(r)), i.value = n += "", "value" === r || n === e.getAttribute(r) ? n : t
        }
    }, st.attrHooks.contenteditable = {
        get: Ct.get, set: function (e, t, n) {
            Ct.set(e, "" === t ? !1 : t, n)
        }
    }, st.each(["width", "height"], function (e, n) {
        st.attrHooks[n] = st.extend(st.attrHooks[n], {
            set: function (e, r) {
                return "" === r ? (e.setAttribute(n, "auto"), r) : t
            }
        })
    })), st.support.hrefNormalized || (st.each(["href", "src", "width", "height"], function (e, n) {
        st.attrHooks[n] = st.extend(st.attrHooks[n], {
            get: function (e) {
                var r = e.getAttribute(n, 2);
                return null == r ? t : r
            }
        })
    }), st.each(["href", "src"], function (e, t) {
        st.propHooks[t] = {
            get: function (e) {
                return e.getAttribute(t, 4)
            }
        }
    })), st.support.style || (st.attrHooks.style = {
        get: function (e) {
            return e.style.cssText || t
        }, set: function (e, t) {
            return e.style.cssText = t + ""
        }
    }), st.support.optSelected || (st.propHooks.selected = st.extend(st.propHooks.selected, {
        get: function (e) {
            var t = e.parentNode;
            return t && (t.selectedIndex, t.parentNode && t.parentNode.selectedIndex), null
        }
    })), st.support.enctype || (st.propFix.enctype = "encoding"), st.support.checkOn || st.each(["radio", "checkbox"], function () {
        st.valHooks[this] = {
            get: function (e) {
                return null === e.getAttribute("value") ? "on" : e.value
            }
        }
    }), st.each(["radio", "checkbox"], function () {
        st.valHooks[this] = st.extend(st.valHooks[this], {
            set: function (e, n) {
                return st.isArray(n) ? e.checked = st.inArray(st(e).val(), n) >= 0 : t
            }
        })
    });
    var qt = /^(?:input|select|textarea)$/i, _t = /^key/,
        Ft = /^(?:mouse|contextmenu)|click/,
        Ot = /^(?:focusinfocus|focusoutblur)$/, Bt = /^([^.]*)(?:\.(.+)|)$/;
    st.event = {
        global: {},
        add: function (e, n, r, i, o) {
            var a, s, u, l, c, f, p, d, h, g, m,
                y = 3 !== e.nodeType && 8 !== e.nodeType && st._data(e);
            if (y) {
                for (r.handler && (a = r, r = a.handler, o = a.selector), r.guid || (r.guid = st.guid++), (l = y.events) || (l = y.events = {}), (s = y.handle) || (s = y.handle = function (e) {
                    return st === t || e && st.event.triggered === e.type ? t : st.event.dispatch.apply(s.elem, arguments)
                }, s.elem = e), n = (n || "").match(lt) || [""], c = n.length; c--;)u = Bt.exec(n[c]) || [], h = m = u[1], g = (u[2] || "").split(".").sort(), p = st.event.special[h] || {}, h = (o ? p.delegateType : p.bindType) || h, p = st.event.special[h] || {}, f = st.extend({
                    type: h,
                    origType: m,
                    data: i,
                    handler: r,
                    guid: r.guid,
                    selector: o,
                    needsContext: o && st.expr.match.needsContext.test(o),
                    namespace: g.join(".")
                }, a), (d = l[h]) || (d = l[h] = [], d.delegateCount = 0, p.setup && p.setup.call(e, i, g, s) !== !1 || (e.addEventListener ? e.addEventListener(h, s, !1) : e.attachEvent && e.attachEvent("on" + h, s))), p.add && (p.add.call(e, f), f.handler.guid || (f.handler.guid = r.guid)), o ? d.splice(d.delegateCount++, 0, f) : d.push(f), st.event.global[h] = !0;
                e = null
            }
        },
        remove: function (e, t, n, r, i) {
            var o, a, s, u, l, c, f, p, d, h, g,
                m = st.hasData(e) && st._data(e);
            if (m && (u = m.events)) {
                for (t = (t || "").match(lt) || [""], l = t.length; l--;)if (s = Bt.exec(t[l]) || [], d = g = s[1], h = (s[2] || "").split(".").sort(), d) {
                    for (f = st.event.special[d] || {}, d = (r ? f.delegateType : f.bindType) || d, p = u[d] || [], s = s[2] && RegExp("(^|\\.)" + h.join("\\.(?:.*\\.|)") + "(\\.|$)"), a = o = p.length; o--;)c = p[o], !i && g !== c.origType || n && n.guid !== c.guid || s && !s.test(c.namespace) || r && r !== c.selector && ("**" !== r || !c.selector) || (p.splice(o, 1), c.selector && p.delegateCount--, f.remove && f.remove.call(e, c));
                    a && !p.length && (f.teardown && f.teardown.call(e, h, m.handle) !== !1 || st.removeEvent(e, d, m.handle), delete u[d])
                } else for (d in u)st.event.remove(e, d + t[l], n, r, !0);
                st.isEmptyObject(u) && (delete m.handle, st._removeData(e, "events"))
            }
        },
        trigger: function (n, r, i, o) {
            var a, s, u, l, c, f, p, d = [i || V], h = n.type || n,
                g = n.namespace ? n.namespace.split(".") : [];
            if (s = u = i = i || V, 3 !== i.nodeType && 8 !== i.nodeType && !Ot.test(h + st.event.triggered) && (h.indexOf(".") >= 0 && (g = h.split("."), h = g.shift(), g.sort()), c = 0 > h.indexOf(":") && "on" + h, n = n[st.expando] ? n : new st.Event(h, "object" == typeof n && n), n.isTrigger = !0, n.namespace = g.join("."), n.namespace_re = n.namespace ? RegExp("(^|\\.)" + g.join("\\.(?:.*\\.|)") + "(\\.|$)") : null, n.result = t, n.target || (n.target = i), r = null == r ? [n] : st.makeArray(r, [n]), p = st.event.special[h] || {}, o || !p.trigger || p.trigger.apply(i, r) !== !1)) {
                if (!o && !p.noBubble && !st.isWindow(i)) {
                    for (l = p.delegateType || h, Ot.test(l + h) || (s = s.parentNode); s; s = s.parentNode)d.push(s), u = s;
                    u === (i.ownerDocument || V) && d.push(u.defaultView || u.parentWindow || e)
                }
                for (a = 0; (s = d[a++]) && !n.isPropagationStopped();)n.type = a > 1 ? l : p.bindType || h, f = (st._data(s, "events") || {})[n.type] && st._data(s, "handle"), f && f.apply(s, r), f = c && s[c], f && st.acceptData(s) && f.apply && f.apply(s, r) === !1 && n.preventDefault();
                if (n.type = h, !(o || n.isDefaultPrevented() || p._default && p._default.apply(i.ownerDocument, r) !== !1 || "click" === h && st.nodeName(i, "a") || !st.acceptData(i) || !c || !i[h] || st.isWindow(i))) {
                    u = i[c], u && (i[c] = null), st.event.triggered = h;
                    try {
                        i[h]()
                    } catch (m) {
                    }
                    st.event.triggered = t, u && (i[c] = u)
                }
                return n.result
            }
        },
        dispatch: function (e) {
            e = st.event.fix(e);
            var n, r, i, o, a, s = [], u = nt.call(arguments),
                l = (st._data(this, "events") || {})[e.type] || [],
                c = st.event.special[e.type] || {};
            if (u[0] = e, e.delegateTarget = this, !c.preDispatch || c.preDispatch.call(this, e) !== !1) {
                for (s = st.event.handlers.call(this, e, l), n = 0; (o = s[n++]) && !e.isPropagationStopped();)for (e.currentTarget = o.elem, r = 0; (a = o.handlers[r++]) && !e.isImmediatePropagationStopped();)(!e.namespace_re || e.namespace_re.test(a.namespace)) && (e.handleObj = a, e.data = a.data, i = ((st.event.special[a.origType] || {}).handle || a.handler).apply(o.elem, u), i !== t && (e.result = i) === !1 && (e.preventDefault(), e.stopPropagation()));
                return c.postDispatch && c.postDispatch.call(this, e), e.result
            }
        },
        handlers: function (e, n) {
            var r, i, o, a, s = [], u = n.delegateCount, l = e.target;
            if (u && l.nodeType && (!e.button || "click" !== e.type))for (; l != this; l = l.parentNode || this)if (l.disabled !== !0 || "click" !== e.type) {
                for (i = [], r = 0; u > r; r++)a = n[r], o = a.selector + " ", i[o] === t && (i[o] = a.needsContext ? st(o, this).index(l) >= 0 : st.find(o, this, null, [l]).length), i[o] && i.push(a);
                i.length && s.push({elem: l, handlers: i})
            }
            return n.length > u && s.push({elem: this, handlers: n.slice(u)}), s
        },
        fix: function (e) {
            if (e[st.expando])return e;
            var t, n, r = e, i = st.event.fixHooks[e.type] || {},
                o = i.props ? this.props.concat(i.props) : this.props;
            for (e = new st.Event(r), t = o.length; t--;)n = o[t], e[n] = r[n];
            return e.target || (e.target = r.srcElement || V), 3 === e.target.nodeType && (e.target = e.target.parentNode), e.metaKey = !!e.metaKey, i.filter ? i.filter(e, r) : e
        },
        props: "altKey bubbles cancelable ctrlKey currentTarget eventPhase metaKey relatedTarget shiftKey target timeStamp view which".split(" "),
        fixHooks: {},
        keyHooks: {
            props: "char charCode key keyCode".split(" "),
            filter: function (e, t) {
                return null == e.which && (e.which = null != t.charCode ? t.charCode : t.keyCode), e
            }
        },
        mouseHooks: {
            props: "button buttons clientX clientY fromElement offsetX offsetY pageX pageY screenX screenY toElement".split(" "),
            filter: function (e, n) {
                var r, i, o, a = n.button, s = n.fromElement;
                return null == e.pageX && null != n.clientX && (r = e.target.ownerDocument || V, i = r.documentElement, o = r.body, e.pageX = n.clientX + (i && i.scrollLeft || o && o.scrollLeft || 0) - (i && i.clientLeft || o && o.clientLeft || 0), e.pageY = n.clientY + (i && i.scrollTop || o && o.scrollTop || 0) - (i && i.clientTop || o && o.clientTop || 0)), !e.relatedTarget && s && (e.relatedTarget = s === e.target ? n.toElement : s), e.which || a === t || (e.which = 1 & a ? 1 : 2 & a ? 3 : 4 & a ? 2 : 0), e
            }
        },
        special: {
            load: {noBubble: !0}, click: {
                trigger: function () {
                    return st.nodeName(this, "input") && "checkbox" === this.type && this.click ? (this.click(), !1) : t
                }
            }, focus: {
                trigger: function () {
                    if (this !== V.activeElement && this.focus)try {
                        return this.focus(), !1
                    } catch (e) {
                    }
                }, delegateType: "focusin"
            }, blur: {
                trigger: function () {
                    return this === V.activeElement && this.blur ? (this.blur(), !1) : t
                }, delegateType: "focusout"
            }, beforeunload: {
                postDispatch: function (e) {
                    e.result !== t && (e.originalEvent.returnValue = e.result)
                }
            }
        },
        simulate: function (e, t, n, r) {
            var i = st.extend(new st.Event, n, {
                type: e,
                isSimulated: !0,
                originalEvent: {}
            });
            r ? st.event.trigger(i, null, t) : st.event.dispatch.call(t, i), i.isDefaultPrevented() && n.preventDefault()
        }
    }, st.removeEvent = V.removeEventListener ? function (e, t, n) {
        e.removeEventListener && e.removeEventListener(t, n, !1)
    } : function (e, n, r) {
        var i = "on" + n;
        e.detachEvent && (e[i] === t && (e[i] = null), e.detachEvent(i, r))
    }, st.Event = function (e, n) {
        return this instanceof st.Event ? (e && e.type ? (this.originalEvent = e, this.type = e.type, this.isDefaultPrevented = e.defaultPrevented || e.returnValue === !1 || e.getPreventDefault && e.getPreventDefault() ? u : l) : this.type = e, n && st.extend(this, n), this.timeStamp = e && e.timeStamp || st.now(), this[st.expando] = !0, t) : new st.Event(e, n)
    }, st.Event.prototype = {
        isDefaultPrevented: l,
        isPropagationStopped: l,
        isImmediatePropagationStopped: l,
        preventDefault: function () {
            var e = this.originalEvent;
            this.isDefaultPrevented = u, e && (e.preventDefault ? e.preventDefault() : e.returnValue = !1)
        },
        stopPropagation: function () {
            var e = this.originalEvent;
            this.isPropagationStopped = u, e && (e.stopPropagation && e.stopPropagation(), e.cancelBubble = !0)
        },
        stopImmediatePropagation: function () {
            this.isImmediatePropagationStopped = u, this.stopPropagation()
        }
    }, st.each({
        mouseenter: "mouseover",
        mouseleave: "mouseout"
    }, function (e, t) {
        st.event.special[e] = {
            delegateType: t,
            bindType: t,
            handle: function (e) {
                var n, r = this, i = e.relatedTarget, o = e.handleObj;
                return (!i || i !== r && !st.contains(r, i)) && (e.type = o.origType, n = o.handler.apply(this, arguments), e.type = t), n
            }
        }
    }), st.support.submitBubbles || (st.event.special.submit = {
        setup: function () {
            return st.nodeName(this, "form") ? !1 : (st.event.add(this, "click._submit keypress._submit", function (e) {
                var n = e.target,
                    r = st.nodeName(n, "input") || st.nodeName(n, "button") ? n.form : t;
                r && !st._data(r, "submitBubbles") && (st.event.add(r, "submit._submit", function (e) {
                    e._submit_bubble = !0
                }), st._data(r, "submitBubbles", !0))
            }), t)
        }, postDispatch: function (e) {
            e._submit_bubble && (delete e._submit_bubble, this.parentNode && !e.isTrigger && st.event.simulate("submit", this.parentNode, e, !0))
        }, teardown: function () {
            return st.nodeName(this, "form") ? !1 : (st.event.remove(this, "._submit"), t)
        }
    }), st.support.changeBubbles || (st.event.special.change = {
        setup: function () {
            return qt.test(this.nodeName) ? (("checkbox" === this.type || "radio" === this.type) && (st.event.add(this, "propertychange._change", function (e) {
                "checked" === e.originalEvent.propertyName && (this._just_changed = !0)
            }), st.event.add(this, "click._change", function (e) {
                this._just_changed && !e.isTrigger && (this._just_changed = !1), st.event.simulate("change", this, e, !0)
            })), !1) : (st.event.add(this, "beforeactivate._change", function (e) {
                var t = e.target;
                qt.test(t.nodeName) && !st._data(t, "changeBubbles") && (st.event.add(t, "change._change", function (e) {
                    !this.parentNode || e.isSimulated || e.isTrigger || st.event.simulate("change", this.parentNode, e, !0)
                }), st._data(t, "changeBubbles", !0))
            }), t)
        }, handle: function (e) {
            var n = e.target;
            return this !== n || e.isSimulated || e.isTrigger || "radio" !== n.type && "checkbox" !== n.type ? e.handleObj.handler.apply(this, arguments) : t
        }, teardown: function () {
            return st.event.remove(this, "._change"), !qt.test(this.nodeName)
        }
    }), st.support.focusinBubbles || st.each({
        focus: "focusin",
        blur: "focusout"
    }, function (e, t) {
        var n = 0, r = function (e) {
            st.event.simulate(t, e.target, st.event.fix(e), !0)
        };
        st.event.special[t] = {
            setup: function () {
                0 === n++ && V.addEventListener(e, r, !0)
            }, teardown: function () {
                0 === --n && V.removeEventListener(e, r, !0)
            }
        }
    }), st.fn.extend({
        on: function (e, n, r, i, o) {
            var a, s;
            if ("object" == typeof e) {
                "string" != typeof n && (r = r || n, n = t);
                for (s in e)this.on(s, n, r, e[s], o);
                return this
            }
            if (null == r && null == i ? (i = n, r = n = t) : null == i && ("string" == typeof n ? (i = r, r = t) : (i = r, r = n, n = t)), i === !1) i = l; else if (!i)return this;
            return 1 === o && (a = i, i = function (e) {
                return st().off(e), a.apply(this, arguments)
            }, i.guid = a.guid || (a.guid = st.guid++)), this.each(function () {
                st.event.add(this, e, i, r, n)
            })
        }, one: function (e, t, n, r) {
            return this.on(e, t, n, r, 1)
        }, off: function (e, n, r) {
            var i, o;
            if (e && e.preventDefault && e.handleObj)return i = e.handleObj, st(e.delegateTarget).off(i.namespace ? i.origType + "." + i.namespace : i.origType, i.selector, i.handler), this;
            if ("object" == typeof e) {
                for (o in e)this.off(o, n, e[o]);
                return this
            }
            return (n === !1 || "function" == typeof n) && (r = n, n = t), r === !1 && (r = l), this.each(function () {
                st.event.remove(this, e, r, n)
            })
        }, bind: function (e, t, n) {
            return this.on(e, null, t, n)
        }, unbind: function (e, t) {
            return this.off(e, null, t)
        }, delegate: function (e, t, n, r) {
            return this.on(t, e, n, r)
        }, undelegate: function (e, t, n) {
            return 1 === arguments.length ? this.off(e, "**") : this.off(t, e || "**", n)
        }, trigger: function (e, t) {
            return this.each(function () {
                st.event.trigger(e, t, this)
            })
        }, triggerHandler: function (e, n) {
            var r = this[0];
            return r ? st.event.trigger(e, n, r, !0) : t
        }, hover: function (e, t) {
            return this.mouseenter(e).mouseleave(t || e)
        }
    }), st.each("blur focus focusin focusout load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup error contextmenu".split(" "), function (e, t) {
        st.fn[t] = function (e, n) {
            return arguments.length > 0 ? this.on(t, null, e, n) : this.trigger(t)
        }, _t.test(t) && (st.event.fixHooks[t] = st.event.keyHooks), Ft.test(t) && (st.event.fixHooks[t] = st.event.mouseHooks)
    }), function (e, t) {
        function n(e) {
            return ht.test(e + "")
        }

        function r() {
            var e, t = [];
            return e = function (n, r) {
                return t.push(n += " ") > C.cacheLength && delete e[t.shift()], e[n] = r
            }
        }

        function i(e) {
            return e[P] = !0, e
        }

        function o(e) {
            var t = L.createElement("div");
            try {
                return e(t)
            } catch (n) {
                return !1
            } finally {
                t = null
            }
        }

        function a(e, t, n, r) {
            var i, o, a, s, u, l, c, d, h, g;
            if ((t ? t.ownerDocument || t : R) !== L && D(t), t = t || L, n = n || [], !e || "string" != typeof e)return n;
            if (1 !== (s = t.nodeType) && 9 !== s)return [];
            if (!M && !r) {
                if (i = gt.exec(e))if (a = i[1]) {
                    if (9 === s) {
                        if (o = t.getElementById(a), !o || !o.parentNode)return n;
                        if (o.id === a)return n.push(o), n
                    } else if (t.ownerDocument && (o = t.ownerDocument.getElementById(a)) && O(t, o) && o.id === a)return n.push(o), n
                } else {
                    if (i[2])return Q.apply(n, K.call(t.getElementsByTagName(e), 0)), n;
                    if ((a = i[3]) && W.getByClassName && t.getElementsByClassName)return Q.apply(n, K.call(t.getElementsByClassName(a), 0)), n
                }
                if (W.qsa && !q.test(e)) {
                    if (c = !0, d = P, h = t, g = 9 === s && e, 1 === s && "object" !== t.nodeName.toLowerCase()) {
                        for (l = f(e), (c = t.getAttribute("id")) ? d = c.replace(vt, "\\$&") : t.setAttribute("id", d), d = "[id='" + d + "'] ", u = l.length; u--;)l[u] = d + p(l[u]);
                        h = dt.test(e) && t.parentNode || t, g = l.join(",")
                    }
                    if (g)try {
                        return Q.apply(n, K.call(h.querySelectorAll(g), 0)), n
                    } catch (m) {
                    } finally {
                        c || t.removeAttribute("id")
                    }
                }
            }
            return x(e.replace(at, "$1"), t, n, r)
        }

        function s(e, t) {
            for (var n = e && t && e.nextSibling; n; n = n.nextSibling)if (n === t)return -1;
            return e ? 1 : -1
        }

        function u(e) {
            return function (t) {
                var n = t.nodeName.toLowerCase();
                return "input" === n && t.type === e
            }
        }

        function l(e) {
            return function (t) {
                var n = t.nodeName.toLowerCase();
                return ("input" === n || "button" === n) && t.type === e
            }
        }

        function c(e) {
            return i(function (t) {
                return t = +t, i(function (n, r) {
                    for (var i, o = e([], n.length, t),
                             a = o.length; a--;)n[i = o[a]] && (n[i] = !(r[i] = n[i]))
                })
            })
        }

        function f(e, t) {
            var n, r, i, o, s, u, l, c = X[e + " "];
            if (c)return t ? 0 : c.slice(0);
            for (s = e, u = [], l = C.preFilter; s;) {
                (!n || (r = ut.exec(s))) && (r && (s = s.slice(r[0].length) || s), u.push(i = [])), n = !1, (r = lt.exec(s)) && (n = r.shift(), i.push({
                    value: n,
                    type: r[0].replace(at, " ")
                }), s = s.slice(n.length));
                for (o in C.filter)!(r = pt[o].exec(s)) || l[o] && !(r = l[o](r)) || (n = r.shift(), i.push({
                    value: n,
                    type: o,
                    matches: r
                }), s = s.slice(n.length));
                if (!n)break
            }
            return t ? s.length : s ? a.error(e) : X(e, u).slice(0)
        }

        function p(e) {
            for (var t = 0, n = e.length, r = ""; n > t; t++)r += e[t].value;
            return r
        }

        function d(e, t, n) {
            var r = t.dir, i = n && "parentNode" === t.dir, o = I++;
            return t.first ? function (t, n, o) {
                for (; t = t[r];)if (1 === t.nodeType || i)return e(t, n, o)
            } : function (t, n, a) {
                var s, u, l, c = $ + " " + o;
                if (a) {
                    for (; t = t[r];)if ((1 === t.nodeType || i) && e(t, n, a))return !0
                } else for (; t = t[r];)if (1 === t.nodeType || i)if (l = t[P] || (t[P] = {}), (u = l[r]) && u[0] === c) {
                    if ((s = u[1]) === !0 || s === N)return s === !0
                } else if (u = l[r] = [c], u[1] = e(t, n, a) || N, u[1] === !0)return !0
            }
        }

        function h(e) {
            return e.length > 1 ? function (t, n, r) {
                for (var i = e.length; i--;)if (!e[i](t, n, r))return !1;
                return !0
            } : e[0]
        }

        function g(e, t, n, r, i) {
            for (var o, a = [], s = 0, u = e.length,
                     l = null != t; u > s; s++)(o = e[s]) && (!n || n(o, r, i)) && (a.push(o), l && t.push(s));
            return a
        }

        function m(e, t, n, r, o, a) {
            return r && !r[P] && (r = m(r)), o && !o[P] && (o = m(o, a)), i(function (i, a, s, u) {
                var l, c, f, p = [], d = [], h = a.length,
                    m = i || b(t || "*", s.nodeType ? [s] : s, []),
                    y = !e || !i && t ? m : g(m, p, e, s, u),
                    v = n ? o || (i ? e : h || r) ? [] : a : y;
                if (n && n(y, v, s, u), r)for (l = g(v, d), r(l, [], s, u), c = l.length; c--;)(f = l[c]) && (v[d[c]] = !(y[d[c]] = f));
                if (i) {
                    if (o || e) {
                        if (o) {
                            for (l = [], c = v.length; c--;)(f = v[c]) && l.push(y[c] = f);
                            o(null, v = [], l, u)
                        }
                        for (c = v.length; c--;)(f = v[c]) && (l = o ? Z.call(i, f) : p[c]) > -1 && (i[l] = !(a[l] = f))
                    }
                } else v = g(v === a ? v.splice(h, v.length) : v), o ? o(null, a, v, u) : Q.apply(a, v)
            })
        }

        function y(e) {
            for (var t, n, r, i = e.length, o = C.relative[e[0].type],
                     a = o || C.relative[" "], s = o ? 1 : 0,
                     u = d(function (e) {
                         return e === t
                     }, a, !0), l = d(function (e) {
                    return Z.call(t, e) > -1
                }, a, !0), c = [function (e, n, r) {
                    return !o && (r || n !== j) || ((t = n).nodeType ? u(e, n, r) : l(e, n, r))
                }]; i > s; s++)if (n = C.relative[e[s].type]) c = [d(h(c), n)]; else {
                if (n = C.filter[e[s].type].apply(null, e[s].matches), n[P]) {
                    for (r = ++s; i > r && !C.relative[e[r].type]; r++);
                    return m(s > 1 && h(c), s > 1 && p(e.slice(0, s - 1)).replace(at, "$1"), n, r > s && y(e.slice(s, r)), i > r && y(e = e.slice(r)), i > r && p(e))
                }
                c.push(n)
            }
            return h(c)
        }

        function v(e, t) {
            var n = 0, r = t.length > 0, o = e.length > 0,
                s = function (i, s, u, l, c) {
                    var f, p, d, h = [], m = 0, y = "0", v = i && [],
                        b = null != c, x = j,
                        T = i || o && C.find.TAG("*", c && s.parentNode || s),
                        w = $ += null == x ? 1 : Math.E;
                    for (b && (j = s !== L && s, N = n); null != (f = T[y]); y++) {
                        if (o && f) {
                            for (p = 0; d = e[p]; p++)if (d(f, s, u)) {
                                l.push(f);
                                break
                            }
                            b && ($ = w, N = ++n)
                        }
                        r && ((f = !d && f) && m--, i && v.push(f))
                    }
                    if (m += y, r && y !== m) {
                        for (p = 0; d = t[p]; p++)d(v, h, s, u);
                        if (i) {
                            if (m > 0)for (; y--;)v[y] || h[y] || (h[y] = G.call(l));
                            h = g(h)
                        }
                        Q.apply(l, h), b && !i && h.length > 0 && m + t.length > 1 && a.uniqueSort(l)
                    }
                    return b && ($ = w, j = x), v
                };
            return r ? i(s) : s
        }

        function b(e, t, n) {
            for (var r = 0, i = t.length; i > r; r++)a(e, t[r], n);
            return n
        }

        function x(e, t, n, r) {
            var i, o, a, s, u, l = f(e);
            if (!r && 1 === l.length) {
                if (o = l[0] = l[0].slice(0), o.length > 2 && "ID" === (a = o[0]).type && 9 === t.nodeType && !M && C.relative[o[1].type]) {
                    if (t = C.find.ID(a.matches[0].replace(xt, Tt), t)[0], !t)return n;
                    e = e.slice(o.shift().value.length)
                }
                for (i = pt.needsContext.test(e) ? -1 : o.length - 1; i >= 0 && (a = o[i], !C.relative[s = a.type]); i--)if ((u = C.find[s]) && (r = u(a.matches[0].replace(xt, Tt), dt.test(o[0].type) && t.parentNode || t))) {
                    if (o.splice(i, 1), e = r.length && p(o), !e)return Q.apply(n, K.call(r, 0)), n;
                    break
                }
            }
            return S(e, l)(r, t, M, n, dt.test(e)), n
        }

        function T() {
        }

        var w, N, C, k, E, S, A, j, D, L, H, M, q, _, F, O, B,
            P = "sizzle" + -new Date, R = e.document, W = {}, $ = 0, I = 0,
            z = r(), X = r(), U = r(), V = typeof t, Y = 1 << 31, J = [],
            G = J.pop, Q = J.push, K = J.slice, Z = J.indexOf || function (e) {
                    for (var t = 0,
                             n = this.length; n > t; t++)if (this[t] === e)return t;
                    return -1
                }, et = "[\\x20\\t\\r\\n\\f]",
            tt = "(?:\\\\.|[\\w-]|[^\\x00-\\xa0])+", nt = tt.replace("w", "w#"),
            rt = "([*^$|!~]?=)",
            it = "\\[" + et + "*(" + tt + ")" + et + "*(?:" + rt + et + "*(?:(['\"])((?:\\\\.|[^\\\\])*?)\\3|(" + nt + ")|)|)" + et + "*\\]",
            ot = ":(" + tt + ")(?:\\(((['\"])((?:\\\\.|[^\\\\])*?)\\3|((?:\\\\.|[^\\\\()[\\]]|" + it.replace(3, 8) + ")*)|.*)\\)|)",
            at = RegExp("^" + et + "+|((?:^|[^\\\\])(?:\\\\.)*)" + et + "+$", "g"),
            ut = RegExp("^" + et + "*," + et + "*"),
            lt = RegExp("^" + et + "*([\\x20\\t\\r\\n\\f>+~])" + et + "*"),
            ct = RegExp(ot), ft = RegExp("^" + nt + "$"), pt = {
                ID: RegExp("^#(" + tt + ")"),
                CLASS: RegExp("^\\.(" + tt + ")"),
                NAME: RegExp("^\\[name=['\"]?(" + tt + ")['\"]?\\]"),
                TAG: RegExp("^(" + tt.replace("w", "w*") + ")"),
                ATTR: RegExp("^" + it),
                PSEUDO: RegExp("^" + ot),
                CHILD: RegExp("^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\(" + et + "*(even|odd|(([+-]|)(\\d*)n|)" + et + "*(?:([+-]|)" + et + "*(\\d+)|))" + et + "*\\)|)", "i"),
                needsContext: RegExp("^" + et + "*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\(" + et + "*((?:-\\d)?\\d*)" + et + "*\\)|)(?=[^-]|$)", "i")
            }, dt = /[\x20\t\r\n\f]*[+~]/, ht = /\{\s*\[native code\]\s*\}/,
            gt = /^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/,
            mt = /^(?:input|select|textarea|button)$/i, yt = /^h\d$/i,
            vt = /'|\\/g, bt = /\=[\x20\t\r\n\f]*([^'"\]]*)[\x20\t\r\n\f]*\]/g,
            xt = /\\([\da-fA-F]{1,6}[\x20\t\r\n\f]?|.)/g, Tt = function (e, t) {
                var n = "0x" + t - 65536;
                return n !== n ? t : 0 > n ? String.fromCharCode(n + 65536) : String.fromCharCode(55296 | n >> 10, 56320 | 1023 & n)
            };
        try {
            K.call(H.childNodes, 0)[0].nodeType
        } catch (wt) {
            K = function (e) {
                for (var t, n = []; t = this[e]; e++)n.push(t);
                return n
            }
        }
        E = a.isXML = function (e) {
            var t = e && (e.ownerDocument || e).documentElement;
            return t ? "HTML" !== t.nodeName : !1
        }, D = a.setDocument = function (e) {
            var r = e ? e.ownerDocument || e : R;
            return r !== L && 9 === r.nodeType && r.documentElement ? (L = r, H = r.documentElement, M = E(r), W.tagNameNoComments = o(function (e) {
                return e.appendChild(r.createComment("")), !e.getElementsByTagName("*").length
            }), W.attributes = o(function (e) {
                e.innerHTML = "<select></select>";
                var t = typeof e.lastChild.getAttribute("multiple");
                return "boolean" !== t && "string" !== t
            }), W.getByClassName = o(function (e) {
                return e.innerHTML = "<div class='hidden e'></div><div class='hidden'></div>", e.getElementsByClassName && e.getElementsByClassName("e").length ? (e.lastChild.className = "e", 2 === e.getElementsByClassName("e").length) : !1
            }), W.getByName = o(function (e) {
                e.id = P + 0, e.innerHTML = "<a name='" + P + "'></a><div name='" + P + "'></div>", H.insertBefore(e, H.firstChild);
                var t = r.getElementsByName && r.getElementsByName(P).length === 2 + r.getElementsByName(P + 0).length;
                return W.getIdNotName = !r.getElementById(P), H.removeChild(e), t
            }), C.attrHandle = o(function (e) {
                return e.innerHTML = "<a href='#'></a>", e.firstChild && typeof e.firstChild.getAttribute !== V && "#" === e.firstChild.getAttribute("href")
            }) ? {} : {
                href: function (e) {
                    return e.getAttribute("href", 2)
                }, type: function (e) {
                    return e.getAttribute("type")
                }
            }, W.getIdNotName ? (C.find.ID = function (e, t) {
                if (typeof t.getElementById !== V && !M) {
                    var n = t.getElementById(e);
                    return n && n.parentNode ? [n] : []
                }
            }, C.filter.ID = function (e) {
                var t = e.replace(xt, Tt);
                return function (e) {
                    return e.getAttribute("id") === t
                }
            }) : (C.find.ID = function (e, n) {
                if (typeof n.getElementById !== V && !M) {
                    var r = n.getElementById(e);
                    return r ? r.id === e || typeof r.getAttributeNode !== V && r.getAttributeNode("id").value === e ? [r] : t : []
                }
            }, C.filter.ID = function (e) {
                var t = e.replace(xt, Tt);
                return function (e) {
                    var n = typeof e.getAttributeNode !== V && e.getAttributeNode("id");
                    return n && n.value === t
                }
            }), C.find.TAG = W.tagNameNoComments ? function (e, n) {
                return typeof n.getElementsByTagName !== V ? n.getElementsByTagName(e) : t
            } : function (e, t) {
                var n, r = [], i = 0, o = t.getElementsByTagName(e);
                if ("*" === e) {
                    for (; n = o[i]; i++)1 === n.nodeType && r.push(n);
                    return r
                }
                return o
            }, C.find.NAME = W.getByName && function (e, n) {
                    return typeof n.getElementsByName !== V ? n.getElementsByName(name) : t
                }, C.find.CLASS = W.getByClassName && function (e, n) {
                    return typeof n.getElementsByClassName === V || M ? t : n.getElementsByClassName(e)
                }, _ = [], q = [":focus"], (W.qsa = n(r.querySelectorAll)) && (o(function (e) {
                e.innerHTML = "<select><option selected=''></option></select>", e.querySelectorAll("[selected]").length || q.push("\\[" + et + "*(?:checked|disabled|ismap|multiple|readonly|selected|value)"), e.querySelectorAll(":checked").length || q.push(":checked")
            }), o(function (e) {
                e.innerHTML = "<input type='hidden' i=''/>", e.querySelectorAll("[i^='']").length && q.push("[*^$]=" + et + "*(?:\"\"|'')"), e.querySelectorAll(":enabled").length || q.push(":enabled", ":disabled"), e.querySelectorAll("*,:x"), q.push(",.*:")
            })), (W.matchesSelector = n(F = H.matchesSelector || H.mozMatchesSelector || H.webkitMatchesSelector || H.oMatchesSelector || H.msMatchesSelector)) && o(function (e) {
                W.disconnectedMatch = F.call(e, "div"), F.call(e, "[s!='']:x"), _.push("!=", ot)
            }), q = RegExp(q.join("|")), _ = RegExp(_.join("|")), O = n(H.contains) || H.compareDocumentPosition ? function (e, t) {
                var n = 9 === e.nodeType ? e.documentElement : e,
                    r = t && t.parentNode;
                return e === r || !(!r || 1 !== r.nodeType || !(n.contains ? n.contains(r) : e.compareDocumentPosition && 16 & e.compareDocumentPosition(r)))
            } : function (e, t) {
                if (t)for (; t = t.parentNode;)if (t === e)return !0;
                return !1
            }, B = H.compareDocumentPosition ? function (e, t) {
                var n;
                return e === t ? (A = !0, 0) : (n = t.compareDocumentPosition && e.compareDocumentPosition && e.compareDocumentPosition(t)) ? 1 & n || e.parentNode && 11 === e.parentNode.nodeType ? e === r || O(R, e) ? -1 : t === r || O(R, t) ? 1 : 0 : 4 & n ? -1 : 1 : e.compareDocumentPosition ? -1 : 1
            } : function (e, t) {
                var n, i = 0, o = e.parentNode, a = t.parentNode, u = [e],
                    l = [t];
                if (e === t)return A = !0, 0;
                if (e.sourceIndex && t.sourceIndex)return (~t.sourceIndex || Y) - (O(R, e) && ~e.sourceIndex || Y);
                if (!o || !a)return e === r ? -1 : t === r ? 1 : o ? -1 : a ? 1 : 0;
                if (o === a)return s(e, t);
                for (n = e; n = n.parentNode;)u.unshift(n);
                for (n = t; n = n.parentNode;)l.unshift(n);
                for (; u[i] === l[i];)i++;
                return i ? s(u[i], l[i]) : u[i] === R ? -1 : l[i] === R ? 1 : 0
            }, A = !1, [0, 0].sort(B), W.detectDuplicates = A, L) : L
        }, a.matches = function (e, t) {
            return a(e, null, null, t)
        }, a.matchesSelector = function (e, t) {
            if ((e.ownerDocument || e) !== L && D(e), t = t.replace(bt, "='$1']"), !(!W.matchesSelector || M || _ && _.test(t) || q.test(t)))try {
                var n = F.call(e, t);
                if (n || W.disconnectedMatch || e.document && 11 !== e.document.nodeType)return n
            } catch (r) {
            }
            return a(t, L, null, [e]).length > 0
        }, a.contains = function (e, t) {
            return (e.ownerDocument || e) !== L && D(e), O(e, t)
        }, a.attr = function (e, t) {
            var n;
            return (e.ownerDocument || e) !== L && D(e), M || (t = t.toLowerCase()), (n = C.attrHandle[t]) ? n(e) : M || W.attributes ? e.getAttribute(t) : ((n = e.getAttributeNode(t)) || e.getAttribute(t)) && e[t] === !0 ? t : n && n.specified ? n.value : null
        }, a.error = function (e) {
            throw Error("Syntax error, unrecognized expression: " + e)
        }, a.uniqueSort = function (e) {
            var t, n = [], r = 1, i = 0;
            if (A = !W.detectDuplicates, e.sort(B), A) {
                for (; t = e[r]; r++)t === e[r - 1] && (i = n.push(r));
                for (; i--;)e.splice(n[i], 1)
            }
            return e
        }, k = a.getText = function (e) {
            var t, n = "", r = 0, i = e.nodeType;
            if (i) {
                if (1 === i || 9 === i || 11 === i) {
                    if ("string" == typeof e.textContent)return e.textContent;
                    for (e = e.firstChild; e; e = e.nextSibling)n += k(e)
                } else if (3 === i || 4 === i)return e.nodeValue
            } else for (; t = e[r]; r++)n += k(t);
            return n
        }, C = a.selectors = {
            cacheLength: 50,
            createPseudo: i,
            match: pt,
            find: {},
            relative: {
                ">": {dir: "parentNode", first: !0},
                " ": {dir: "parentNode"},
                "+": {dir: "previousSibling", first: !0},
                "~": {dir: "previousSibling"}
            },
            preFilter: {
                ATTR: function (e) {
                    return e[1] = e[1].replace(xt, Tt), e[3] = (e[4] || e[5] || "").replace(xt, Tt), "~=" === e[2] && (e[3] = " " + e[3] + " "), e.slice(0, 4)
                }, CHILD: function (e) {
                    return e[1] = e[1].toLowerCase(), "nth" === e[1].slice(0, 3) ? (e[3] || a.error(e[0]), e[4] = +(e[4] ? e[5] + (e[6] || 1) : 2 * ("even" === e[3] || "odd" === e[3])), e[5] = +(e[7] + e[8] || "odd" === e[3])) : e[3] && a.error(e[0]), e
                }, PSEUDO: function (e) {
                    var t, n = !e[5] && e[2];
                    return pt.CHILD.test(e[0]) ? null : (e[4] ? e[2] = e[4] : n && ct.test(n) && (t = f(n, !0)) && (t = n.indexOf(")", n.length - t) - n.length) && (e[0] = e[0].slice(0, t), e[2] = n.slice(0, t)), e.slice(0, 3))
                }
            },
            filter: {
                TAG: function (e) {
                    return "*" === e ? function () {
                        return !0
                    } : (e = e.replace(xt, Tt).toLowerCase(), function (t) {
                        return t.nodeName && t.nodeName.toLowerCase() === e
                    })
                }, CLASS: function (e) {
                    var t = z[e + " "];
                    return t || (t = RegExp("(^|" + et + ")" + e + "(" + et + "|$)")) && z(e, function (e) {
                            return t.test(e.className || typeof e.getAttribute !== V && e.getAttribute("class") || "")
                        })
                }, ATTR: function (e, t, n) {
                    return function (r) {
                        var i = a.attr(r, e);
                        return null == i ? "!=" === t : t ? (i += "", "=" === t ? i === n : "!=" === t ? i !== n : "^=" === t ? n && 0 === i.indexOf(n) : "*=" === t ? n && i.indexOf(n) > -1 : "$=" === t ? n && i.substr(i.length - n.length) === n : "~=" === t ? (" " + i + " ").indexOf(n) > -1 : "|=" === t ? i === n || i.substr(0, n.length + 1) === n + "-" : !1) : !0
                    }
                }, CHILD: function (e, t, n, r, i) {
                    var o = "nth" !== e.slice(0, 3), a = "last" !== e.slice(-4),
                        s = "of-type" === t;
                    return 1 === r && 0 === i ? function (e) {
                        return !!e.parentNode
                    } : function (t, n, u) {
                        var l, c, f, p, d, h,
                            g = o !== a ? "nextSibling" : "previousSibling",
                            m = t.parentNode, y = s && t.nodeName.toLowerCase(),
                            v = !u && !s;
                        if (m) {
                            if (o) {
                                for (; g;) {
                                    for (f = t; f = f[g];)if (s ? f.nodeName.toLowerCase() === y : 1 === f.nodeType)return !1;
                                    h = g = "only" === e && !h && "nextSibling"
                                }
                                return !0
                            }
                            if (h = [a ? m.firstChild : m.lastChild], a && v) {
                                for (c = m[P] || (m[P] = {}), l = c[e] || [], d = l[0] === $ && l[1], p = l[0] === $ && l[2], f = d && m.childNodes[d]; f = ++d && f && f[g] || (p = d = 0) || h.pop();)if (1 === f.nodeType && ++p && f === t) {
                                    c[e] = [$, d, p];
                                    break
                                }
                            } else if (v && (l = (t[P] || (t[P] = {}))[e]) && l[0] === $) p = l[1]; else for (; (f = ++d && f && f[g] || (p = d = 0) || h.pop()) && ((s ? f.nodeName.toLowerCase() !== y : 1 !== f.nodeType) || !++p || (v && ((f[P] || (f[P] = {}))[e] = [$, p]), f !== t)););
                            return p -= i, p === r || 0 === p % r && p / r >= 0
                        }
                    }
                }, PSEUDO: function (e, t) {
                    var n,
                        r = C.pseudos[e] || C.setFilters[e.toLowerCase()] || a.error("unsupported pseudo: " + e);
                    return r[P] ? r(t) : r.length > 1 ? (n = [e, e, "", t], C.setFilters.hasOwnProperty(e.toLowerCase()) ? i(function (e, n) {
                        for (var i, o = r(e, t),
                                 a = o.length; a--;)i = Z.call(e, o[a]), e[i] = !(n[i] = o[a])
                    }) : function (e) {
                        return r(e, 0, n)
                    }) : r
                }
            },
            pseudos: {
                not: i(function (e) {
                    var t = [], n = [], r = S(e.replace(at, "$1"));
                    return r[P] ? i(function (e, t, n, i) {
                        for (var o, a = r(e, null, i, []),
                                 s = e.length; s--;)(o = a[s]) && (e[s] = !(t[s] = o))
                    }) : function (e, i, o) {
                        return t[0] = e, r(t, null, o, n), !n.pop()
                    }
                }), has: i(function (e) {
                    return function (t) {
                        return a(e, t).length > 0
                    }
                }), contains: i(function (e) {
                    return function (t) {
                        return (t.textContent || t.innerText || k(t)).indexOf(e) > -1
                    }
                }), lang: i(function (e) {
                    return ft.test(e || "") || a.error("unsupported lang: " + e), e = e.replace(xt, Tt).toLowerCase(), function (t) {
                        var n;
                        do if (n = M ? t.getAttribute("xml:lang") || t.getAttribute("lang") : t.lang)return n = n.toLowerCase(), n === e || 0 === n.indexOf(e + "-"); while ((t = t.parentNode) && 1 === t.nodeType);
                        return !1
                    }
                }), target: function (t) {
                    var n = e.location && e.location.hash;
                    return n && n.slice(1) === t.id
                }, root: function (e) {
                    return e === H
                }, focus: function (e) {
                    return e === L.activeElement && (!L.hasFocus || L.hasFocus()) && !!(e.type || e.href || ~e.tabIndex)
                }, enabled: function (e) {
                    return e.disabled === !1
                }, disabled: function (e) {
                    return e.disabled === !0
                }, checked: function (e) {
                    var t = e.nodeName.toLowerCase();
                    return "input" === t && !!e.checked || "option" === t && !!e.selected
                }, selected: function (e) {
                    return e.parentNode && e.parentNode.selectedIndex, e.selected === !0
                }, empty: function (e) {
                    for (e = e.firstChild; e; e = e.nextSibling)if (e.nodeName > "@" || 3 === e.nodeType || 4 === e.nodeType)return !1;
                    return !0
                }, parent: function (e) {
                    return !C.pseudos.empty(e)
                }, header: function (e) {
                    return yt.test(e.nodeName)
                }, input: function (e) {
                    return mt.test(e.nodeName)
                }, button: function (e) {
                    var t = e.nodeName.toLowerCase();
                    return "input" === t && "button" === e.type || "button" === t
                }, text: function (e) {
                    var t;
                    return "input" === e.nodeName.toLowerCase() && "text" === e.type && (null == (t = e.getAttribute("type")) || t.toLowerCase() === e.type)
                }, first: c(function () {
                    return [0]
                }), last: c(function (e, t) {
                    return [t - 1]
                }), eq: c(function (e, t, n) {
                    return [0 > n ? n + t : n]
                }), even: c(function (e, t) {
                    for (var n = 0; t > n; n += 2)e.push(n);
                    return e
                }), odd: c(function (e, t) {
                    for (var n = 1; t > n; n += 2)e.push(n);
                    return e
                }), lt: c(function (e, t, n) {
                    for (var r = 0 > n ? n + t : n; --r >= 0;)e.push(r);
                    return e
                }), gt: c(function (e, t, n) {
                    for (var r = 0 > n ? n + t : n; t > ++r;)e.push(r);
                    return e
                })
            }
        };
        for (w in{
            radio: !0,
            checkbox: !0,
            file: !0,
            password: !0,
            image: !0
        })C.pseudos[w] = u(w);
        for (w in{submit: !0, reset: !0})C.pseudos[w] = l(w);
        S = a.compile = function (e, t) {
            var n, r = [], i = [], o = U[e + " "];
            if (!o) {
                for (t || (t = f(e)), n = t.length; n--;)o = y(t[n]), o[P] ? r.push(o) : i.push(o);
                o = U(e, v(i, r))
            }
            return o
        }, C.pseudos.nth = C.pseudos.eq, C.filters = T.prototype = C.pseudos, C.setFilters = new T, D(), a.attr = st.attr, st.find = a, st.expr = a.selectors, st.expr[":"] = st.expr.pseudos, st.unique = a.uniqueSort, st.text = a.getText, st.isXMLDoc = a.isXML, st.contains = a.contains
    }(e);
    var Pt = /Until$/, Rt = /^(?:parents|prev(?:Until|All))/,
        Wt = /^.[^:#\[\.,]*$/, $t = st.expr.match.needsContext,
        It = {children: !0, contents: !0, next: !0, prev: !0};
    st.fn.extend({
        find: function (e) {
            var t, n, r;
            if ("string" != typeof e)return r = this, this.pushStack(st(e).filter(function () {
                for (t = 0; r.length > t; t++)if (st.contains(r[t], this))return !0
            }));
            for (n = [], t = 0; this.length > t; t++)st.find(e, this[t], n);
            return n = this.pushStack(st.unique(n)), n.selector = (this.selector ? this.selector + " " : "") + e, n
        }, has: function (e) {
            var t, n = st(e, this), r = n.length;
            return this.filter(function () {
                for (t = 0; r > t; t++)if (st.contains(this, n[t]))return !0
            })
        }, not: function (e) {
            return this.pushStack(f(this, e, !1))
        }, filter: function (e) {
            return this.pushStack(f(this, e, !0))
        }, is: function (e) {
            return !!e && ("string" == typeof e ? $t.test(e) ? st(e, this.context).index(this[0]) >= 0 : st.filter(e, this).length > 0 : this.filter(e).length > 0)
        }, closest: function (e, t) {
            for (var n, r = 0, i = this.length, o = [],
                     a = $t.test(e) || "string" != typeof e ? st(e, t || this.context) : 0; i > r; r++)for (n = this[r]; n && n.ownerDocument && n !== t && 11 !== n.nodeType;) {
                if (a ? a.index(n) > -1 : st.find.matchesSelector(n, e)) {
                    o.push(n);
                    break
                }
                n = n.parentNode
            }
            return this.pushStack(o.length > 1 ? st.unique(o) : o)
        }, index: function (e) {
            return e ? "string" == typeof e ? st.inArray(this[0], st(e)) : st.inArray(e.jquery ? e[0] : e, this) : this[0] && this[0].parentNode ? this.first().prevAll().length : -1
        }, add: function (e, t) {
            var n = "string" == typeof e ? st(e, t) : st.makeArray(e && e.nodeType ? [e] : e),
                r = st.merge(this.get(), n);
            return this.pushStack(st.unique(r))
        }, addBack: function (e) {
            return this.add(null == e ? this.prevObject : this.prevObject.filter(e))
        }
    }), st.fn.andSelf = st.fn.addBack, st.each({
        parent: function (e) {
            var t = e.parentNode;
            return t && 11 !== t.nodeType ? t : null
        }, parents: function (e) {
            return st.dir(e, "parentNode")
        }, parentsUntil: function (e, t, n) {
            return st.dir(e, "parentNode", n)
        }, next: function (e) {
            return c(e, "nextSibling")
        }, prev: function (e) {
            return c(e, "previousSibling")
        }, nextAll: function (e) {
            return st.dir(e, "nextSibling")
        }, prevAll: function (e) {
            return st.dir(e, "previousSibling")
        }, nextUntil: function (e, t, n) {
            return st.dir(e, "nextSibling", n)
        }, prevUntil: function (e, t, n) {
            return st.dir(e, "previousSibling", n)
        }, siblings: function (e) {
            return st.sibling((e.parentNode || {}).firstChild, e)
        }, children: function (e) {
            return st.sibling(e.firstChild)
        }, contents: function (e) {
            return st.nodeName(e, "iframe") ? e.contentDocument || e.contentWindow.document : st.merge([], e.childNodes)
        }
    }, function (e, t) {
        st.fn[e] = function (n, r) {
            var i = st.map(this, t, n);
            return Pt.test(e) || (r = n), r && "string" == typeof r && (i = st.filter(r, i)), i = this.length > 1 && !It[e] ? st.unique(i) : i, this.length > 1 && Rt.test(e) && (i = i.reverse()), this.pushStack(i)
        }
    }), st.extend({
        filter: function (e, t, n) {
            return n && (e = ":not(" + e + ")"), 1 === t.length ? st.find.matchesSelector(t[0], e) ? [t[0]] : [] : st.find.matches(e, t)
        }, dir: function (e, n, r) {
            for (var i = [],
                     o = e[n]; o && 9 !== o.nodeType && (r === t || 1 !== o.nodeType || !st(o).is(r));)1 === o.nodeType && i.push(o), o = o[n];
            return i
        }, sibling: function (e, t) {
            for (var n = []; e; e = e.nextSibling)1 === e.nodeType && e !== t && n.push(e);
            return n
        }
    });
    var zt = "abbr|article|aside|audio|bdi|canvas|data|datalist|details|figcaption|figure|footer|header|hgroup|mark|meter|nav|output|progress|section|summary|time|video",
        Xt = / jQuery\d+="(?:null|\d+)"/g,
        Ut = RegExp("<(?:" + zt + ")[\\s/>]", "i"), Vt = /^\s+/,
        Yt = /<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/gi,
        Jt = /<([\w:]+)/, Gt = /<tbody/i, Qt = /<|&#?\w+;/,
        Kt = /<(?:script|style|link)/i, Zt = /^(?:checkbox|radio)$/i,
        en = /checked\s*(?:[^=]|=\s*.checked.)/i,
        tn = /^$|\/(?:java|ecma)script/i, nn = /^true\/(.*)/,
        rn = /^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g, on = {
            option: [1, "<select multiple='multiple'>", "</select>"],
            legend: [1, "<fieldset>", "</fieldset>"],
            area: [1, "<map>", "</map>"],
            param: [1, "<object>", "</object>"],
            thead: [1, "<table>", "</table>"],
            tr: [2, "<table><tbody>", "</tbody></table>"],
            col: [2, "<table><tbody></tbody><colgroup>", "</colgroup></table>"],
            td: [3, "<table><tbody><tr>", "</tr></tbody></table>"],
            _default: st.support.htmlSerialize ? [0, "", ""] : [1, "X<div>", "</div>"]
        }, an = p(V), sn = an.appendChild(V.createElement("div"));
    on.optgroup = on.option, on.tbody = on.tfoot = on.colgroup = on.caption = on.thead, on.th = on.td, st.fn.extend({
        text: function (e) {
            return st.access(this, function (e) {
                return e === t ? st.text(this) : this.empty().append((this[0] && this[0].ownerDocument || V).createTextNode(e))
            }, null, e, arguments.length)
        }, wrapAll: function (e) {
            if (st.isFunction(e))return this.each(function (t) {
                st(this).wrapAll(e.call(this, t))
            });
            if (this[0]) {
                var t = st(e, this[0].ownerDocument).eq(0).clone(!0);
                this[0].parentNode && t.insertBefore(this[0]), t.map(function () {
                    for (var e = this; e.firstChild && 1 === e.firstChild.nodeType;)e = e.firstChild;
                    return e
                }).append(this)
            }
            return this
        }, wrapInner: function (e) {
            return st.isFunction(e) ? this.each(function (t) {
                st(this).wrapInner(e.call(this, t))
            }) : this.each(function () {
                var t = st(this), n = t.contents();
                n.length ? n.wrapAll(e) : t.append(e)
            })
        }, wrap: function (e) {
            var t = st.isFunction(e);
            return this.each(function (n) {
                st(this).wrapAll(t ? e.call(this, n) : e)
            })
        }, unwrap: function () {
            return this.parent().each(function () {
                st.nodeName(this, "body") || st(this).replaceWith(this.childNodes)
            }).end()
        }, append: function () {
            return this.domManip(arguments, !0, function (e) {
                (1 === this.nodeType || 11 === this.nodeType || 9 === this.nodeType) && this.appendChild(e)
            })
        }, prepend: function () {
            return this.domManip(arguments, !0, function (e) {
                (1 === this.nodeType || 11 === this.nodeType || 9 === this.nodeType) && this.insertBefore(e, this.firstChild)
            })
        }, before: function () {
            return this.domManip(arguments, !1, function (e) {
                this.parentNode && this.parentNode.insertBefore(e, this)
            })
        }, after: function () {
            return this.domManip(arguments, !1, function (e) {
                this.parentNode && this.parentNode.insertBefore(e, this.nextSibling)
            })
        }, remove: function (e, t) {
            for (var n,
                     r = 0; null != (n = this[r]); r++)(!e || st.filter(e, [n]).length > 0) && (t || 1 !== n.nodeType || st.cleanData(b(n)), n.parentNode && (t && st.contains(n.ownerDocument, n) && m(b(n, "script")), n.parentNode.removeChild(n)));
            return this
        }, empty: function () {
            for (var e, t = 0; null != (e = this[t]); t++) {
                for (1 === e.nodeType && st.cleanData(b(e, !1)); e.firstChild;)e.removeChild(e.firstChild);
                e.options && st.nodeName(e, "select") && (e.options.length = 0)
            }
            return this
        }, clone: function (e, t) {
            return e = null == e ? !1 : e, t = null == t ? e : t, this.map(function () {
                return st.clone(this, e, t)
            })
        }, html: function (e) {
            return st.access(this, function (e) {
                var n = this[0] || {}, r = 0, i = this.length;
                if (e === t)return 1 === n.nodeType ? n.innerHTML.replace(Xt, "") : t;
                if (!("string" != typeof e || Kt.test(e) || !st.support.htmlSerialize && Ut.test(e) || !st.support.leadingWhitespace && Vt.test(e) || on[(Jt.exec(e) || ["", ""])[1].toLowerCase()])) {
                    e = e.replace(Yt, "<$1></$2>");
                    try {
                        for (; i > r; r++)n = this[r] || {}, 1 === n.nodeType && (st.cleanData(b(n, !1)), n.innerHTML = e);
                        n = 0
                    } catch (o) {
                    }
                }
                n && this.empty().append(e)
            }, null, e, arguments.length)
        }, replaceWith: function (e) {
            var t = st.isFunction(e);
            return t || "string" == typeof e || (e = st(e).not(this).detach()), this.domManip([e], !0, function (e) {
                var t = this.nextSibling, n = this.parentNode;
                (n && 1 === this.nodeType || 11 === this.nodeType) && (st(this).remove(), t ? t.parentNode.insertBefore(e, t) : n.appendChild(e))
            })
        }, detach: function (e) {
            return this.remove(e, !0)
        }, domManip: function (e, n, r) {
            e = et.apply([], e);
            var i, o, a, s, u, l, c = 0, f = this.length, p = this, m = f - 1,
                y = e[0], v = st.isFunction(y);
            if (v || !(1 >= f || "string" != typeof y || st.support.checkClone) && en.test(y))return this.each(function (i) {
                var o = p.eq(i);
                v && (e[0] = y.call(this, i, n ? o.html() : t)), o.domManip(e, n, r)
            });
            if (f && (i = st.buildFragment(e, this[0].ownerDocument, !1, this), o = i.firstChild, 1 === i.childNodes.length && (i = o), o)) {
                for (n = n && st.nodeName(o, "tr"), a = st.map(b(i, "script"), h), s = a.length; f > c; c++)u = i, c !== m && (u = st.clone(u, !0, !0), s && st.merge(a, b(u, "script"))), r.call(n && st.nodeName(this[c], "table") ? d(this[c], "tbody") : this[c], u, c);
                if (s)for (l = a[a.length - 1].ownerDocument, st.map(a, g), c = 0; s > c; c++)u = a[c], tn.test(u.type || "") && !st._data(u, "globalEval") && st.contains(l, u) && (u.src ? st.ajax({
                    url: u.src,
                    type: "GET",
                    dataType: "script",
                    async: !1,
                    global: !1,
                    "throws": !0
                }) : st.globalEval((u.text || u.textContent || u.innerHTML || "").replace(rn, "")));
                i = o = null
            }
            return this
        }
    }), st.each({
        appendTo: "append",
        prependTo: "prepend",
        insertBefore: "before",
        insertAfter: "after",
        replaceAll: "replaceWith"
    }, function (e, t) {
        st.fn[e] = function (e) {
            for (var n, r = 0, i = [], o = st(e),
                     a = o.length - 1; a >= r; r++)n = r === a ? this : this.clone(!0), st(o[r])[t](n), tt.apply(i, n.get());
            return this.pushStack(i)
        }
    }), st.extend({
        clone: function (e, t, n) {
            var r, i, o, a, s, u = st.contains(e.ownerDocument, e);
            if (st.support.html5Clone || st.isXMLDoc(e) || !Ut.test("<" + e.nodeName + ">") ? s = e.cloneNode(!0) : (sn.innerHTML = e.outerHTML, sn.removeChild(s = sn.firstChild)), !(st.support.noCloneEvent && st.support.noCloneChecked || 1 !== e.nodeType && 11 !== e.nodeType || st.isXMLDoc(e)))for (r = b(s), i = b(e), a = 0; null != (o = i[a]); ++a)r[a] && v(o, r[a]);
            if (t)if (n)for (i = i || b(e), r = r || b(s), a = 0; null != (o = i[a]); a++)y(o, r[a]); else y(e, s);
            return r = b(s, "script"), r.length > 0 && m(r, !u && b(e, "script")), r = i = o = null, s
        }, buildFragment: function (e, t, n, r) {
            for (var i, o, a, s, u, l, c, f = e.length, d = p(t), h = [],
                     g = 0; f > g; g++)if (o = e[g], o || 0 === o)if ("object" === st.type(o)) st.merge(h, o.nodeType ? [o] : o); else if (Qt.test(o)) {
                for (s = s || d.appendChild(t.createElement("div")), a = (Jt.exec(o) || ["", ""])[1].toLowerCase(), u = on[a] || on._default, s.innerHTML = u[1] + o.replace(Yt, "<$1></$2>") + u[2], c = u[0]; c--;)s = s.lastChild;
                if (!st.support.leadingWhitespace && Vt.test(o) && h.push(t.createTextNode(Vt.exec(o)[0])), !st.support.tbody)for (o = "table" !== a || Gt.test(o) ? "<table>" !== u[1] || Gt.test(o) ? 0 : s : s.firstChild, c = o && o.childNodes.length; c--;)st.nodeName(l = o.childNodes[c], "tbody") && !l.childNodes.length && o.removeChild(l);
                for (st.merge(h, s.childNodes), s.textContent = ""; s.firstChild;)s.removeChild(s.firstChild);
                s = d.lastChild
            } else h.push(t.createTextNode(o));
            for (s && d.removeChild(s), st.support.appendChecked || st.grep(b(h, "input"), x), g = 0; o = h[g++];)if ((!r || -1 === st.inArray(o, r)) && (i = st.contains(o.ownerDocument, o), s = b(d.appendChild(o), "script"), i && m(s), n))for (c = 0; o = s[c++];)tn.test(o.type || "") && n.push(o);
            return s = null, d
        }, cleanData: function (e, n) {
            for (var r, i, o, a, s = 0, u = st.expando, l = st.cache,
                     c = st.support.deleteExpando,
                     f = st.event.special; null != (o = e[s]); s++)if ((n || st.acceptData(o)) && (i = o[u], r = i && l[i])) {
                if (r.events)for (a in r.events)f[a] ? st.event.remove(o, a) : st.removeEvent(o, a, r.handle);
                l[i] && (delete l[i], c ? delete o[u] : o.removeAttribute !== t ? o.removeAttribute(u) : o[u] = null, K.push(i))
            }
        }
    });
    var un, ln, cn, fn = /alpha\([^)]*\)/i, pn = /opacity\s*=\s*([^)]*)/,
        dn = /^(top|right|bottom|left)$/, hn = /^(none|table(?!-c[ea]).+)/,
        gn = /^margin/, mn = RegExp("^(" + ut + ")(.*)$", "i"),
        yn = RegExp("^(" + ut + ")(?!px)[a-z%]+$", "i"),
        vn = RegExp("^([+-])=(" + ut + ")", "i"), bn = {BODY: "block"},
        xn = {position: "absolute", visibility: "hidden", display: "block"},
        Tn = {letterSpacing: 0, fontWeight: 400},
        wn = ["Top", "Right", "Bottom", "Left"],
        Nn = ["Webkit", "O", "Moz", "ms"];
    st.fn.extend({
        css: function (e, n) {
            return st.access(this, function (e, n, r) {
                var i, o, a = {}, s = 0;
                if (st.isArray(n)) {
                    for (i = ln(e), o = n.length; o > s; s++)a[n[s]] = st.css(e, n[s], !1, i);
                    return a
                }
                return r !== t ? st.style(e, n, r) : st.css(e, n)
            }, e, n, arguments.length > 1)
        }, show: function () {
            return N(this, !0)
        }, hide: function () {
            return N(this)
        }, toggle: function (e) {
            var t = "boolean" == typeof e;
            return this.each(function () {
                (t ? e : w(this)) ? st(this).show() : st(this).hide()
            })
        }
    }), st.extend({
        cssHooks: {
            opacity: {
                get: function (e, t) {
                    if (t) {
                        var n = un(e, "opacity");
                        return "" === n ? "1" : n
                    }
                }
            }
        },
        cssNumber: {
            columnCount: !0,
            fillOpacity: !0,
            fontWeight: !0,
            lineHeight: !0,
            opacity: !0,
            orphans: !0,
            widows: !0,
            zIndex: !0,
            zoom: !0
        },
        cssProps: {"float": st.support.cssFloat ? "cssFloat" : "styleFloat"},
        style: function (e, n, r, i) {
            if (e && 3 !== e.nodeType && 8 !== e.nodeType && e.style) {
                var o, a, s, u = st.camelCase(n), l = e.style;
                if (n = st.cssProps[u] || (st.cssProps[u] = T(l, u)), s = st.cssHooks[n] || st.cssHooks[u], r === t)return s && "get" in s && (o = s.get(e, !1, i)) !== t ? o : l[n];
                if (a = typeof r, "string" === a && (o = vn.exec(r)) && (r = (o[1] + 1) * o[2] + parseFloat(st.css(e, n)), a = "number"), !(null == r || "number" === a && isNaN(r) || ("number" !== a || st.cssNumber[u] || (r += "px"), st.support.clearCloneStyle || "" !== r || 0 !== n.indexOf("background") || (l[n] = "inherit"), s && "set" in s && (r = s.set(e, r, i)) === t)))try {
                    l[n] = r
                } catch (c) {
                }
            }
        },
        css: function (e, n, r, i) {
            var o, a, s, u = st.camelCase(n);
            return n = st.cssProps[u] || (st.cssProps[u] = T(e.style, u)), s = st.cssHooks[n] || st.cssHooks[u], s && "get" in s && (o = s.get(e, !0, r)), o === t && (o = un(e, n, i)), "normal" === o && n in Tn && (o = Tn[n]), r ? (a = parseFloat(o), r === !0 || st.isNumeric(a) ? a || 0 : o) : o
        },
        swap: function (e, t, n, r) {
            var i, o, a = {};
            for (o in t)a[o] = e.style[o], e.style[o] = t[o];
            i = n.apply(e, r || []);
            for (o in t)e.style[o] = a[o];
            return i
        }
    }), e.getComputedStyle ? (ln = function (t) {
        return e.getComputedStyle(t, null)
    }, un = function (e, n, r) {
        var i, o, a, s = r || ln(e), u = s ? s.getPropertyValue(n) || s[n] : t,
            l = e.style;
        return s && ("" !== u || st.contains(e.ownerDocument, e) || (u = st.style(e, n)), yn.test(u) && gn.test(n) && (i = l.width, o = l.minWidth, a = l.maxWidth, l.minWidth = l.maxWidth = l.width = u, u = s.width, l.width = i, l.minWidth = o, l.maxWidth = a)), u
    }) : V.documentElement.currentStyle && (ln = function (e) {
            return e.currentStyle
        }, un = function (e, n, r) {
            var i, o, a, s = r || ln(e), u = s ? s[n] : t, l = e.style;
            return null == u && l && l[n] && (u = l[n]), yn.test(u) && !dn.test(n) && (i = l.left, o = e.runtimeStyle, a = o && o.left, a && (o.left = e.currentStyle.left), l.left = "fontSize" === n ? "1em" : u, u = l.pixelLeft + "px", l.left = i, a && (o.left = a)), "" === u ? "auto" : u
        }), st.each(["height", "width"], function (e, n) {
        st.cssHooks[n] = {
            get: function (e, r, i) {
                return r ? 0 === e.offsetWidth && hn.test(st.css(e, "display")) ? st.swap(e, xn, function () {
                    return E(e, n, i)
                }) : E(e, n, i) : t
            }, set: function (e, t, r) {
                var i = r && ln(e);
                return C(e, t, r ? k(e, n, r, st.support.boxSizing && "border-box" === st.css(e, "boxSizing", !1, i), i) : 0)
            }
        }
    }), st.support.opacity || (st.cssHooks.opacity = {
        get: function (e, t) {
            return pn.test((t && e.currentStyle ? e.currentStyle.filter : e.style.filter) || "") ? .01 * parseFloat(RegExp.$1) + "" : t ? "1" : ""
        }, set: function (e, t) {
            var n = e.style, r = e.currentStyle,
                i = st.isNumeric(t) ? "alpha(opacity=" + 100 * t + ")" : "",
                o = r && r.filter || n.filter || "";
            n.zoom = 1, (t >= 1 || "" === t) && "" === st.trim(o.replace(fn, "")) && n.removeAttribute && (n.removeAttribute("filter"), "" === t || r && !r.filter) || (n.filter = fn.test(o) ? o.replace(fn, i) : o + " " + i)
        }
    }), st(function () {
        st.support.reliableMarginRight || (st.cssHooks.marginRight = {
            get: function (e, n) {
                return n ? st.swap(e, {display: "inline-block"}, un, [e, "marginRight"]) : t
            }
        }), !st.support.pixelPosition && st.fn.position && st.each(["top", "left"], function (e, n) {
            st.cssHooks[n] = {
                get: function (e, r) {
                    return r ? (r = un(e, n), yn.test(r) ? st(e).position()[n] + "px" : r) : t
                }
            }
        })
    }), st.expr && st.expr.filters && (st.expr.filters.hidden = function (e) {
        return 0 === e.offsetWidth && 0 === e.offsetHeight || !st.support.reliableHiddenOffsets && "none" === (e.style && e.style.display || st.css(e, "display"))
    }, st.expr.filters.visible = function (e) {
        return !st.expr.filters.hidden(e)
    }), st.each({margin: "", padding: "", border: "Width"}, function (e, t) {
        st.cssHooks[e + t] = {
            expand: function (n) {
                for (var r = 0, i = {},
                         o = "string" == typeof n ? n.split(" ") : [n]; 4 > r; r++)i[e + wn[r] + t] = o[r] || o[r - 2] || o[0];
                return i
            }
        }, gn.test(e) || (st.cssHooks[e + t].set = C)
    });
    var Cn = /%20/g, kn = /\[\]$/, En = /\r?\n/g,
        Sn = /^(?:submit|button|image|reset)$/i,
        An = /^(?:input|select|textarea|keygen)/i;
    st.fn.extend({
        serialize: function () {
            return st.param(this.serializeArray())
        }, serializeArray: function () {
            return this.map(function () {
                var e = st.prop(this, "elements");
                return e ? st.makeArray(e) : this
            }).filter(function () {
                var e = this.type;
                return this.name && !st(this).is(":disabled") && An.test(this.nodeName) && !Sn.test(e) && (this.checked || !Zt.test(e))
            }).map(function (e, t) {
                var n = st(this).val();
                return null == n ? null : st.isArray(n) ? st.map(n, function (e) {
                    return {name: t.name, value: e.replace(En, "\r\n")}
                }) : {name: t.name, value: n.replace(En, "\r\n")}
            }).get()
        }
    }), st.param = function (e, n) {
        var r, i = [], o = function (e, t) {
            t = st.isFunction(t) ? t() : null == t ? "" : t, i[i.length] = encodeURIComponent(e) + "=" + encodeURIComponent(t)
        };
        if (n === t && (n = st.ajaxSettings && st.ajaxSettings.traditional), st.isArray(e) || e.jquery && !st.isPlainObject(e)) st.each(e, function () {
            o(this.name, this.value)
        }); else for (r in e)j(r, e[r], n, o);
        return i.join("&").replace(Cn, "+")
    };
    var jn, Dn, Ln = st.now(), Hn = /\?/, Mn = /#.*$/, qn = /([?&])_=[^&]*/,
        _n = /^(.*?):[ \t]*([^\r\n]*)\r?$/gm,
        Fn = /^(?:about|app|app-storage|.+-extension|file|res|widget):$/,
        On = /^(?:GET|HEAD)$/, Bn = /^\/\//,
        Pn = /^([\w.+-]+:)(?:\/\/([^\/?#:]*)(?::(\d+)|)|)/, Rn = st.fn.load,
        Wn = {}, $n = {}, In = "*/".concat("*");
    try {
        Dn = Y.href
    } catch (zn) {
        Dn = V.createElement("a"), Dn.href = "", Dn = Dn.href
    }
    jn = Pn.exec(Dn.toLowerCase()) || [], st.fn.load = function (e, n, r) {
        if ("string" != typeof e && Rn)return Rn.apply(this, arguments);
        var i, o, a, s = this, u = e.indexOf(" ");
        return u >= 0 && (i = e.slice(u, e.length), e = e.slice(0, u)), st.isFunction(n) ? (r = n, n = t) : n && "object" == typeof n && (o = "POST"), s.length > 0 && st.ajax({
            url: e,
            type: o,
            dataType: "html",
            data: n
        }).done(function (e) {
            a = arguments, s.html(i ? st("<div>").append(st.parseHTML(e)).find(i) : e)
        }).complete(r && function (e, t) {
                s.each(r, a || [e.responseText, t, e])
            }), this
    }, st.each(["ajaxStart", "ajaxStop", "ajaxComplete", "ajaxError", "ajaxSuccess", "ajaxSend"], function (e, t) {
        st.fn[t] = function (e) {
            return this.on(t, e)
        }
    }), st.each(["get", "post"], function (e, n) {
        st[n] = function (e, r, i, o) {
            return st.isFunction(r) && (o = o || i, i = r, r = t), st.ajax({
                url: e,
                type: n,
                dataType: o,
                data: r,
                success: i
            })
        }
    }), st.extend({
        active: 0,
        lastModified: {},
        etag: {},
        ajaxSettings: {
            url: Dn,
            type: "GET",
            isLocal: Fn.test(jn[1]),
            global: !0,
            processData: !0,
            async: !0,
            contentType: "application/x-www-form-urlencoded; charset=UTF-8",
            accepts: {
                "*": In,
                text: "text/plain",
                html: "text/html",
                xml: "application/xml, text/xml",
                json: "application/json, text/javascript"
            },
            contents: {xml: /xml/, html: /html/, json: /json/},
            responseFields: {xml: "responseXML", text: "responseText"},
            converters: {
                "* text": e.String,
                "text html": !0,
                "text json": st.parseJSON,
                "text xml": st.parseXML
            },
            flatOptions: {url: !0, context: !0}
        },
        ajaxSetup: function (e, t) {
            return t ? H(H(e, st.ajaxSettings), t) : H(st.ajaxSettings, e)
        },
        ajaxPrefilter: D(Wn),
        ajaxTransport: D($n),
        ajax: function (e, n) {
            function r(e, n, r, s) {
                var l, f, v, b, T, N = n;
                2 !== x && (x = 2, u && clearTimeout(u), i = t, a = s || "", w.readyState = e > 0 ? 4 : 0, r && (b = M(p, w, r)), e >= 200 && 300 > e || 304 === e ? (p.ifModified && (T = w.getResponseHeader("Last-Modified"), T && (st.lastModified[o] = T), T = w.getResponseHeader("etag"), T && (st.etag[o] = T)), 304 === e ? (l = !0, N = "notmodified") : (l = q(p, b), N = l.state, f = l.data, v = l.error, l = !v)) : (v = N, (e || !N) && (N = "error", 0 > e && (e = 0))), w.status = e, w.statusText = (n || N) + "", l ? g.resolveWith(d, [f, N, w]) : g.rejectWith(d, [w, N, v]), w.statusCode(y), y = t, c && h.trigger(l ? "ajaxSuccess" : "ajaxError", [w, p, l ? f : v]), m.fireWith(d, [w, N]), c && (h.trigger("ajaxComplete", [w, p]), --st.active || st.event.trigger("ajaxStop")))
            }

            "object" == typeof e && (n = e, e = t), n = n || {};
            var i, o, a, s, u, l, c, f, p = st.ajaxSetup({}, n),
                d = p.context || p,
                h = p.context && (d.nodeType || d.jquery) ? st(d) : st.event,
                g = st.Deferred(), m = st.Callbacks("once memory"),
                y = p.statusCode || {}, v = {}, b = {}, x = 0, T = "canceled",
                w = {
                    readyState: 0, getResponseHeader: function (e) {
                        var t;
                        if (2 === x) {
                            if (!s)for (s = {}; t = _n.exec(a);)s[t[1].toLowerCase()] = t[2];
                            t = s[e.toLowerCase()]
                        }
                        return null == t ? null : t
                    }, getAllResponseHeaders: function () {
                        return 2 === x ? a : null
                    }, setRequestHeader: function (e, t) {
                        var n = e.toLowerCase();
                        return x || (e = b[n] = b[n] || e, v[e] = t), this
                    }, overrideMimeType: function (e) {
                        return x || (p.mimeType = e), this
                    }, statusCode: function (e) {
                        var t;
                        if (e)if (2 > x)for (t in e)y[t] = [y[t], e[t]]; else w.always(e[w.status]);
                        return this
                    }, abort: function (e) {
                        var t = e || T;
                        return i && i.abort(t), r(0, t), this
                    }
                };
            if (g.promise(w).complete = m.add, w.success = w.done, w.error = w.fail, p.url = ((e || p.url || Dn) + "").replace(Mn, "").replace(Bn, jn[1] + "//"), p.type = n.method || n.type || p.method || p.type, p.dataTypes = st.trim(p.dataType || "*").toLowerCase().match(lt) || [""], null == p.crossDomain && (l = Pn.exec(p.url.toLowerCase()), p.crossDomain = !(!l || l[1] === jn[1] && l[2] === jn[2] && (l[3] || ("http:" === l[1] ? 80 : 443)) == (jn[3] || ("http:" === jn[1] ? 80 : 443)))), p.data && p.processData && "string" != typeof p.data && (p.data = st.param(p.data, p.traditional)), L(Wn, p, n, w), 2 === x)return w;
            c = p.global, c && 0 === st.active++ && st.event.trigger("ajaxStart"), p.type = p.type.toUpperCase(), p.hasContent = !On.test(p.type), o = p.url, p.hasContent || (p.data && (o = p.url += (Hn.test(o) ? "&" : "?") + p.data, delete p.data), p.cache === !1 && (p.url = qn.test(o) ? o.replace(qn, "$1_=" + Ln++) : o + (Hn.test(o) ? "&" : "?") + "_=" + Ln++)), p.ifModified && (st.lastModified[o] && w.setRequestHeader("If-Modified-Since", st.lastModified[o]), st.etag[o] && w.setRequestHeader("If-None-Match", st.etag[o])), (p.data && p.hasContent && p.contentType !== !1 || n.contentType) && w.setRequestHeader("Content-Type", p.contentType), w.setRequestHeader("Accept", p.dataTypes[0] && p.accepts[p.dataTypes[0]] ? p.accepts[p.dataTypes[0]] + ("*" !== p.dataTypes[0] ? ", " + In + "; q=0.01" : "") : p.accepts["*"]);
            for (f in p.headers)w.setRequestHeader(f, p.headers[f]);
            if (p.beforeSend && (p.beforeSend.call(d, w, p) === !1 || 2 === x))return w.abort();
            T = "abort";
            for (f in{success: 1, error: 1, complete: 1})w[f](p[f]);
            if (i = L($n, p, n, w)) {
                w.readyState = 1, c && h.trigger("ajaxSend", [w, p]), p.async && p.timeout > 0 && (u = setTimeout(function () {
                    w.abort("timeout")
                }, p.timeout));
                try {
                    x = 1, i.send(v, r)
                } catch (N) {
                    if (!(2 > x))throw N;
                    r(-1, N)
                }
            } else r(-1, "No Transport");
            return w
        },
        getScript: function (e, n) {
            return st.get(e, t, n, "script")
        },
        getJSON: function (e, t, n) {
            return st.get(e, t, n, "json")
        }
    }), st.ajaxSetup({
        accepts: {script: "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"},
        contents: {script: /(?:java|ecma)script/},
        converters: {
            "text script": function (e) {
                return st.globalEval(e), e
            }
        }
    }), st.ajaxPrefilter("script", function (e) {
        e.cache === t && (e.cache = !1), e.crossDomain && (e.type = "GET", e.global = !1)
    }), st.ajaxTransport("script", function (e) {
        if (e.crossDomain) {
            var n, r = V.head || st("head")[0] || V.documentElement;
            return {
                send: function (t, i) {
                    n = V.createElement("script"), n.async = !0, e.scriptCharset && (n.charset = e.scriptCharset), n.src = e.url, n.onload = n.onreadystatechange = function (e, t) {
                        (t || !n.readyState || /loaded|complete/.test(n.readyState)) && (n.onload = n.onreadystatechange = null, n.parentNode && n.parentNode.removeChild(n), n = null, t || i(200, "success"))
                    }, r.insertBefore(n, r.firstChild)
                }, abort: function () {
                    n && n.onload(t, !0)
                }
            }
        }
    });
    var Xn = [], Un = /(=)\?(?=&|$)|\?\?/;
    st.ajaxSetup({
        jsonp: "callback", jsonpCallback: function () {
            var e = Xn.pop() || st.expando + "_" + Ln++;
            return this[e] = !0, e
        }
    }), st.ajaxPrefilter("json jsonp", function (n, r, i) {
        var o, a, s,
            u = n.jsonp !== !1 && (Un.test(n.url) ? "url" : "string" == typeof n.data && !(n.contentType || "").indexOf("application/x-www-form-urlencoded") && Un.test(n.data) && "data");
        return u || "jsonp" === n.dataTypes[0] ? (o = n.jsonpCallback = st.isFunction(n.jsonpCallback) ? n.jsonpCallback() : n.jsonpCallback, u ? n[u] = n[u].replace(Un, "$1" + o) : n.jsonp !== !1 && (n.url += (Hn.test(n.url) ? "&" : "?") + n.jsonp + "=" + o), n.converters["script json"] = function () {
            return s || st.error(o + " was not called"), s[0]
        }, n.dataTypes[0] = "json", a = e[o], e[o] = function () {
            s = arguments
        }, i.always(function () {
            e[o] = a, n[o] && (n.jsonpCallback = r.jsonpCallback, Xn.push(o)), s && st.isFunction(a) && a(s[0]), s = a = t
        }), "script") : t
    });
    var Vn, Yn, Jn = 0, Gn = e.ActiveXObject && function () {
            var e;
            for (e in Vn)Vn[e](t, !0)
        };
    st.ajaxSettings.xhr = e.ActiveXObject ? function () {
        return !this.isLocal && _() || F()
    } : _, Yn = st.ajaxSettings.xhr(), st.support.cors = !!Yn && "withCredentials" in Yn, Yn = st.support.ajax = !!Yn, Yn && st.ajaxTransport(function (n) {
        if (!n.crossDomain || st.support.cors) {
            var r;
            return {
                send: function (i, o) {
                    var a, s, u = n.xhr();
                    if (n.username ? u.open(n.type, n.url, n.async, n.username, n.password) : u.open(n.type, n.url, n.async), n.xhrFields)for (s in n.xhrFields)u[s] = n.xhrFields[s];
                    n.mimeType && u.overrideMimeType && u.overrideMimeType(n.mimeType), n.crossDomain || i["X-Requested-With"] || (i["X-Requested-With"] = "XMLHttpRequest");
                    try {
                        for (s in i)u.setRequestHeader(s, i[s])
                    } catch (l) {
                    }
                    u.send(n.hasContent && n.data || null), r = function (e, i) {
                        var s, l, c, f, p;
                        try {
                            if (r && (i || 4 === u.readyState))if (r = t, a && (u.onreadystatechange = st.noop, Gn && delete Vn[a]), i) 4 !== u.readyState && u.abort(); else {
                                f = {}, s = u.status, p = u.responseXML, c = u.getAllResponseHeaders(), p && p.documentElement && (f.xml = p), "string" == typeof u.responseText && (f.text = u.responseText);
                                try {
                                    l = u.statusText
                                } catch (d) {
                                    l = ""
                                }
                                s || !n.isLocal || n.crossDomain ? 1223 === s && (s = 204) : s = f.text ? 200 : 404
                            }
                        } catch (h) {
                            i || o(-1, h)
                        }
                        f && o(s, l, f, c)
                    }, n.async ? 4 === u.readyState ? setTimeout(r) : (a = ++Jn, Gn && (Vn || (Vn = {}, st(e).unload(Gn)), Vn[a] = r), u.onreadystatechange = r) : r()
                }, abort: function () {
                    r && r(t, !0)
                }
            }
        }
    });
    var Qn, Kn, Zn = /^(?:toggle|show|hide)$/,
        er = RegExp("^(?:([+-])=|)(" + ut + ")([a-z%]*)$", "i"),
        tr = /queueHooks$/, nr = [W], rr = {
            "*": [function (e, t) {
                var n, r, i = this.createTween(e, t), o = er.exec(t), a = i.cur(),
                    s = +a || 0, u = 1, l = 20;
                if (o) {
                    if (n = +o[2], r = o[3] || (st.cssNumber[e] ? "" : "px"), "px" !== r && s) {
                        s = st.css(i.elem, e, !0) || n || 1;
                        do u = u || ".5", s /= u, st.style(i.elem, e, s + r); while (u !== (u = i.cur() / a) && 1 !== u && --l)
                    }
                    i.unit = r, i.start = s, i.end = o[1] ? s + (o[1] + 1) * n : n
                }
                return i
            }]
        };
    st.Animation = st.extend(P, {
        tweener: function (e, t) {
            st.isFunction(e) ? (t = e, e = ["*"]) : e = e.split(" ");
            for (var n, r = 0,
                     i = e.length; i > r; r++)n = e[r], rr[n] = rr[n] || [], rr[n].unshift(t)
        }, prefilter: function (e, t) {
            t ? nr.unshift(e) : nr.push(e)
        }
    }), st.Tween = $, $.prototype = {
        constructor: $,
        init: function (e, t, n, r, i, o) {
            this.elem = e, this.prop = n, this.easing = i || "swing", this.options = t, this.start = this.now = this.cur(), this.end = r, this.unit = o || (st.cssNumber[n] ? "" : "px")
        },
        cur: function () {
            var e = $.propHooks[this.prop];
            return e && e.get ? e.get(this) : $.propHooks._default.get(this)
        },
        run: function (e) {
            var t, n = $.propHooks[this.prop];
            return this.pos = t = this.options.duration ? st.easing[this.easing](e, this.options.duration * e, 0, 1, this.options.duration) : e, this.now = (this.end - this.start) * t + this.start, this.options.step && this.options.step.call(this.elem, this.now, this), n && n.set ? n.set(this) : $.propHooks._default.set(this), this
        }
    }, $.prototype.init.prototype = $.prototype, $.propHooks = {
        _default: {
            get: function (e) {
                var t;
                return null == e.elem[e.prop] || e.elem.style && null != e.elem.style[e.prop] ? (t = st.css(e.elem, e.prop, "auto"), t && "auto" !== t ? t : 0) : e.elem[e.prop]
            }, set: function (e) {
                st.fx.step[e.prop] ? st.fx.step[e.prop](e) : e.elem.style && (null != e.elem.style[st.cssProps[e.prop]] || st.cssHooks[e.prop]) ? st.style(e.elem, e.prop, e.now + e.unit) : e.elem[e.prop] = e.now
            }
        }
    }, $.propHooks.scrollTop = $.propHooks.scrollLeft = {
        set: function (e) {
            e.elem.nodeType && e.elem.parentNode && (e.elem[e.prop] = e.now)
        }
    }, st.each(["toggle", "show", "hide"], function (e, t) {
        var n = st.fn[t];
        st.fn[t] = function (e, r, i) {
            return null == e || "boolean" == typeof e ? n.apply(this, arguments) : this.animate(I(t, !0), e, r, i)
        }
    }), st.fn.extend({
        fadeTo: function (e, t, n, r) {
            return this.filter(w).css("opacity", 0).show().end().animate({opacity: t}, e, n, r)
        }, animate: function (e, t, n, r) {
            var i = st.isEmptyObject(e), o = st.speed(t, n, r),
                a = function () {
                    var t = P(this, st.extend({}, e), o);
                    a.finish = function () {
                        t.stop(!0)
                    }, (i || st._data(this, "finish")) && t.stop(!0)
                };
            return a.finish = a, i || o.queue === !1 ? this.each(a) : this.queue(o.queue, a)
        }, stop: function (e, n, r) {
            var i = function (e) {
                var t = e.stop;
                delete e.stop, t(r)
            };
            return "string" != typeof e && (r = n, n = e, e = t), n && e !== !1 && this.queue(e || "fx", []), this.each(function () {
                var t = !0, n = null != e && e + "queueHooks", o = st.timers,
                    a = st._data(this);
                if (n) a[n] && a[n].stop && i(a[n]); else for (n in a)a[n] && a[n].stop && tr.test(n) && i(a[n]);
                for (n = o.length; n--;)o[n].elem !== this || null != e && o[n].queue !== e || (o[n].anim.stop(r), t = !1, o.splice(n, 1));
                (t || !r) && st.dequeue(this, e)
            })
        }, finish: function (e) {
            return e !== !1 && (e = e || "fx"), this.each(function () {
                var t, n = st._data(this), r = n[e + "queue"],
                    i = n[e + "queueHooks"], o = st.timers,
                    a = r ? r.length : 0;
                for (n.finish = !0, st.queue(this, e, []), i && i.cur && i.cur.finish && i.cur.finish.call(this), t = o.length; t--;)o[t].elem === this && o[t].queue === e && (o[t].anim.stop(!0), o.splice(t, 1));
                for (t = 0; a > t; t++)r[t] && r[t].finish && r[t].finish.call(this);
                delete n.finish
            })
        }
    }), st.each({
        slideDown: I("show"),
        slideUp: I("hide"),
        slideToggle: I("toggle"),
        fadeIn: {opacity: "show"},
        fadeOut: {opacity: "hide"},
        fadeToggle: {opacity: "toggle"}
    }, function (e, t) {
        st.fn[e] = function (e, n, r) {
            return this.animate(t, e, n, r)
        }
    }), st.speed = function (e, t, n) {
        var r = e && "object" == typeof e ? st.extend({}, e) : {
            complete: n || !n && t || st.isFunction(e) && e,
            duration: e,
            easing: n && t || t && !st.isFunction(t) && t
        };
        return r.duration = st.fx.off ? 0 : "number" == typeof r.duration ? r.duration : r.duration in st.fx.speeds ? st.fx.speeds[r.duration] : st.fx.speeds._default, (null == r.queue || r.queue === !0) && (r.queue = "fx"), r.old = r.complete, r.complete = function () {
            st.isFunction(r.old) && r.old.call(this), r.queue && st.dequeue(this, r.queue)
        }, r
    }, st.easing = {
        linear: function (e) {
            return e
        }, swing: function (e) {
            return .5 - Math.cos(e * Math.PI) / 2
        }
    }, st.timers = [], st.fx = $.prototype.init, st.fx.tick = function () {
        var e, n = st.timers, r = 0;
        for (Qn = st.now(); n.length > r; r++)e = n[r], e() || n[r] !== e || n.splice(r--, 1);
        n.length || st.fx.stop(), Qn = t
    }, st.fx.timer = function (e) {
        e() && st.timers.push(e) && st.fx.start()
    }, st.fx.interval = 13, st.fx.start = function () {
        Kn || (Kn = setInterval(st.fx.tick, st.fx.interval))
    }, st.fx.stop = function () {
        clearInterval(Kn), Kn = null
    }, st.fx.speeds = {
        slow: 600,
        fast: 200,
        _default: 400
    }, st.fx.step = {}, st.expr && st.expr.filters && (st.expr.filters.animated = function (e) {
        return st.grep(st.timers, function (t) {
            return e === t.elem
        }).length
    }), st.fn.offset = function (e) {
        if (arguments.length)return e === t ? this : this.each(function (t) {
            st.offset.setOffset(this, e, t)
        });
        var n, r, i = {top: 0, left: 0}, o = this[0], a = o && o.ownerDocument;
        if (a)return n = a.documentElement, st.contains(n, o) ? (o.getBoundingClientRect !== t && (i = o.getBoundingClientRect()), r = z(a), {
            top: i.top + (r.pageYOffset || n.scrollTop) - (n.clientTop || 0),
            left: i.left + (r.pageXOffset || n.scrollLeft) - (n.clientLeft || 0)
        }) : i
    }, st.offset = {
        setOffset: function (e, t, n) {
            var r = st.css(e, "position");
            "static" === r && (e.style.position = "relative");
            var i, o, a = st(e), s = a.offset(), u = st.css(e, "top"),
                l = st.css(e, "left"),
                c = ("absolute" === r || "fixed" === r) && st.inArray("auto", [u, l]) > -1,
                f = {}, p = {};
            c ? (p = a.position(), i = p.top, o = p.left) : (i = parseFloat(u) || 0, o = parseFloat(l) || 0), st.isFunction(t) && (t = t.call(e, n, s)), null != t.top && (f.top = t.top - s.top + i), null != t.left && (f.left = t.left - s.left + o), "using" in t ? t.using.call(e, f) : a.css(f)
        }
    }, st.fn.extend({
        position: function () {
            if (this[0]) {
                var e, t, n = {top: 0, left: 0}, r = this[0];
                return "fixed" === st.css(r, "position") ? t = r.getBoundingClientRect() : (e = this.offsetParent(), t = this.offset(), st.nodeName(e[0], "html") || (n = e.offset()), n.top += st.css(e[0], "borderTopWidth", !0), n.left += st.css(e[0], "borderLeftWidth", !0)), {
                    top: t.top - n.top - st.css(r, "marginTop", !0),
                    left: t.left - n.left - st.css(r, "marginLeft", !0)
                }
            }
        }, offsetParent: function () {
            return this.map(function () {
                for (var e = this.offsetParent || V.documentElement; e && !st.nodeName(e, "html") && "static" === st.css(e, "position");)e = e.offsetParent;
                return e || V.documentElement
            })
        }
    }), st.each({
        scrollLeft: "pageXOffset",
        scrollTop: "pageYOffset"
    }, function (e, n) {
        var r = /Y/.test(n);
        st.fn[e] = function (i) {
            return st.access(this, function (e, i, o) {
                var a = z(e);
                return o === t ? a ? n in a ? a[n] : a.document.documentElement[i] : e[i] : (a ? a.scrollTo(r ? st(a).scrollLeft() : o, r ? o : st(a).scrollTop()) : e[i] = o, t)
            }, e, i, arguments.length, null)
        }
    }), st.each({Height: "height", Width: "width"}, function (e, n) {
        st.each({
            padding: "inner" + e,
            content: n,
            "": "outer" + e
        }, function (r, i) {
            st.fn[i] = function (i, o) {
                var a = arguments.length && (r || "boolean" != typeof i),
                    s = r || (i === !0 || o === !0 ? "margin" : "border");
                return st.access(this, function (n, r, i) {
                    var o;
                    return st.isWindow(n) ? n.document.documentElement["client" + e] : 9 === n.nodeType ? (o = n.documentElement, Math.max(n.body["scroll" + e], o["scroll" + e], n.body["offset" + e], o["offset" + e], o["client" + e])) : i === t ? st.css(n, r, s) : st.style(n, r, i, s)
                }, n, a ? i : t, a, null)
            }
        })
    }), e.jQuery = e.$ = st, "function" == typeof define && define.amd && define.amd.jQuery && define("jquery", [], function () {
        return st
    })
})(window);
//@ sourceMappingURL=jquery.min.map

function unzip(b64Data) {
    var strData;
    if (!window.atob) {
    } else {
    }
    var charData;
    if (!Array.prototype.map) {
    } else {
    }
    strData = Base64_Zip.btou(RawDeflate.inflate(Base64_Zip.fromBase64(b64Data)));
    return strData
}
var com = {};
com.str = {
    _KEY: "12345678900000001234567890000000",
    _IV: "abcd134556abcedf",
    Encrypt: function (str) {
        var key = CryptoJS.enc.Utf8.parse(this._KEY);
        var iv = CryptoJS.enc.Utf8.parse(this._IV);
        var encrypted = "";
        var srcs = CryptoJS.enc.Utf8.parse(str);
        encrypted = CryptoJS.AES.encrypt(srcs, key, {
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
        return encrypted.ciphertext.toString()
    },
    Decrypt: function (str) {
        var result = com.str.DecryptInner(str);
        try {
            var newstr = com.str.DecryptInner(result);
            if (newstr != "") {
                result = newstr
            }
        } catch (ex) {
            var msg = ex
        }
        return result
    },
    DecryptInner: function (str) {
        var key = CryptoJS.enc.Utf8.parse(this._KEY);
        var iv = CryptoJS.enc.Utf8.parse(this._IV);
        var encryptedHexStr = CryptoJS.enc.Hex.parse(str);
        var srcs = CryptoJS.enc.Base64.stringify(encryptedHexStr);
        var decrypt = CryptoJS.AES.decrypt(srcs, key, {
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
        var decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
        var result = decryptedStr.toString();
        try {
            result = Decrypt(result)
        } catch (ex) {
            var msg = ex
        }
        return result
    }
};
function iemap(myarray, callback, thisArg) {
    var T, A, k;
    if (myarray == null) {
        throw new TypeError(" this is null or not defined")
    }
    var O = Object(myarray);
    var len = O.length >>> 0;
    if (typeof callback !== "function") {
        throw new TypeError(callback + " is not a function")
    }
    if (thisArg) {
        T = thisArg
    }
    A = new Array(len);
    k = 0;
    while (k < len) {
        var kValue, mappedValue;
        if (k in O) {
            kValue = O[k];
            mappedValue = callback.call(T, kValue, k, O);
            A[k] = mappedValue
        }
        k++
    }
    return A
};

(function (ctx) {
    var zip_WSIZE = 32768;
    var zip_STORED_BLOCK = 0;
    var zip_STATIC_TREES = 1;
    var zip_DYN_TREES = 2;
    var zip_lbits = 9;
    var zip_dbits = 6;
    var zip_INBUFSIZ = 32768;
    var zip_INBUF_EXTRA = 64;
    var zip_slide;
    var zip_wp;
    var zip_fixed_tl = null;
    var zip_fixed_td;
    var zip_fixed_bl, zip_fixed_bd;
    var zip_bit_buf;
    var zip_bit_len;
    var zip_method;
    var zip_eof;
    var zip_copy_leng;
    var zip_copy_dist;
    var zip_tl, zip_td;
    var zip_bl, zip_bd;
    var zip_inflate_data;
    var zip_inflate_pos;
    var zip_MASK_BITS = new Array(0, 1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 65535);
    var zip_cplens = new Array(3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 23, 27, 31, 35, 43, 51, 59, 67, 83, 99, 115, 131, 163, 195, 227, 258, 0, 0);
    var zip_cplext = new Array(0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 0, 99, 99);
    var zip_cpdist = new Array(1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193, 257, 385, 513, 769, 1025, 1537, 2049, 3073, 4097, 6145, 8193, 12289, 16385, 24577);
    var zip_cpdext = new Array(0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13);
    var zip_border = new Array(16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15);
    var zip_HuftList = function () {
        this.next = null;
        this.list = null
    };
    var zip_HuftNode = function () {
        this.e = 0;
        this.b = 0;
        this.n = 0;
        this.t = null
    };
    var zip_HuftBuild = function (b, n, s, d, e, mm) {
        this.BMAX = 16;
        this.N_MAX = 288;
        this.status = 0;
        this.root = null;
        this.m = 0;
        var a;
        var c = new Array(this.BMAX + 1);
        var el;
        var f;
        var g;
        var h;
        var i;
        var j;
        var k;
        var lx = new Array(this.BMAX + 1);
        var p;
        var pidx;
        var q;
        var r = new zip_HuftNode();
        var u = new Array(this.BMAX);
        var v = new Array(this.N_MAX);
        var w;
        var x = new Array(this.BMAX + 1);
        var xp;
        var y;
        var z;
        var o;
        var tail;
        tail = this.root = null;
        for (i = 0; i < c.length; i++) {
            c[i] = 0
        }
        for (i = 0; i < lx.length; i++) {
            lx[i] = 0
        }
        for (i = 0; i < u.length; i++) {
            u[i] = null
        }
        for (i = 0; i < v.length; i++) {
            v[i] = 0
        }
        for (i = 0; i < x.length; i++) {
            x[i] = 0
        }
        el = n > 256 ? b[256] : this.BMAX;
        p = b;
        pidx = 0;
        i = n;
        do {
            c[p[pidx]]++;
            pidx++
        } while (--i > 0);
        if (c[0] == n) {
            this.root = null;
            this.m = 0;
            this.status = 0;
            return
        }
        for (j = 1; j <= this.BMAX; j++) {
            if (c[j] != 0) {
                break
            }
        }
        k = j;
        if (mm < j) {
            mm = j
        }
        for (i = this.BMAX; i != 0; i--) {
            if (c[i] != 0) {
                break
            }
        }
        g = i;
        if (mm > i) {
            mm = i
        }
        for (y = 1 << j; j < i; j++, y <<= 1) {
            if ((y -= c[j]) < 0) {
                this.status = 2;
                this.m = mm;
                return
            }
        }
        if ((y -= c[i]) < 0) {
            this.status = 2;
            this.m = mm;
            return
        }
        c[i] += y;
        x[1] = j = 0;
        p = c;
        pidx = 1;
        xp = 2;
        while (--i > 0) {
            x[xp++] = (j += p[pidx++])
        }
        p = b;
        pidx = 0;
        i = 0;
        do {
            if ((j = p[pidx++]) != 0) {
                v[x[j]++] = i
            }
        } while (++i < n);
        n = x[g];
        x[0] = i = 0;
        p = v;
        pidx = 0;
        h = -1;
        w = lx[0] = 0;
        q = null;
        z = 0;
        for (; k <= g; k++) {
            a = c[k];
            while (a-- > 0) {
                while (k > w + lx[1 + h]) {
                    w += lx[1 + h];
                    h++;
                    z = (z = g - w) > mm ? mm : z;
                    if ((f = 1 << (j = k - w)) > a + 1) {
                        f -= a + 1;
                        xp = k;
                        while (++j < z) {
                            if ((f <<= 1) <= c[++xp]) {
                                break
                            }
                            f -= c[xp]
                        }
                    }
                    if (w + j > el && w < el) {
                        j = el - w
                    }
                    z = 1 << j;
                    lx[1 + h] = j;
                    q = new Array(z);
                    for (o = 0; o < z; o++) {
                        q[o] = new zip_HuftNode()
                    }
                    if (tail == null) {
                        tail = this.root = new zip_HuftList()
                    } else {
                        tail = tail.next = new zip_HuftList()
                    }
                    tail.next = null;
                    tail.list = q;
                    u[h] = q;
                    if (h > 0) {
                        x[h] = i;
                        r.b = lx[h];
                        r.e = 16 + j;
                        r.t = q;
                        j = (i & ((1 << w) - 1)) >> (w - lx[h]);
                        u[h - 1][j].e = r.e;
                        u[h - 1][j].b = r.b;
                        u[h - 1][j].n = r.n;
                        u[h - 1][j].t = r.t
                    }
                }
                r.b = k - w;
                if (pidx >= n) {
                    r.e = 99
                } else {
                    if (p[pidx] < s) {
                        r.e = (p[pidx] < 256 ? 16 : 15);
                        r.n = p[pidx++]
                    } else {
                        r.e = e[p[pidx] - s];
                        r.n = d[p[pidx++] - s]
                    }
                }
                f = 1 << (k - w);
                for (j = i >> w; j < z; j += f) {
                    q[j].e = r.e;
                    q[j].b = r.b;
                    q[j].n = r.n;
                    q[j].t = r.t
                }
                for (j = 1 << (k - 1); (i & j) != 0; j >>= 1) {
                    i ^= j
                }
                i ^= j;
                while ((i & ((1 << w) - 1)) != x[h]) {
                    w -= lx[h];
                    h--
                }
            }
        }
        this.m = lx[1];
        this.status = ((y != 0 && g != 1) ? 1 : 0)
    };
    var zip_GET_BYTE = function () {
        if (zip_inflate_data.length == zip_inflate_pos) {
            return -1
        }
        var charcode = zip_inflate_data.charCodeAt(zip_inflate_pos++);
        return charcode & 255
    };
    var zip_NEEDBITS = function (n) {
        while (zip_bit_len < n) {
            zip_bit_buf |= zip_GET_BYTE() << zip_bit_len;
            zip_bit_len += 8
        }
    };
    var zip_GETBITS = function (n) {
        return zip_bit_buf & zip_MASK_BITS[n]
    };
    var zip_DUMPBITS = function (n) {
        zip_bit_buf >>= n;
        zip_bit_len -= n
    };
    var zip_inflate_codes = function (buff, off, size) {
        var e;
        var t;
        var n;
        if (size == 0) {
            return 0
        }
        n = 0;
        for (; ;) {
            zip_NEEDBITS(zip_bl);
            t = zip_tl.list[zip_GETBITS(zip_bl)];
            e = t.e;
            while (e > 16) {
                if (e == 99) {
                    return -1
                }
                zip_DUMPBITS(t.b);
                e -= 16;
                zip_NEEDBITS(e);
                t = t.t[zip_GETBITS(e)];
                e = t.e
            }
            zip_DUMPBITS(t.b);
            if (e == 16) {
                zip_wp &= zip_WSIZE - 1;
                buff[off + n++] = zip_slide[zip_wp++] = t.n;
                if (n == size) {
                    return size
                }
                continue
            }
            if (e == 15) {
                break
            }
            zip_NEEDBITS(e);
            zip_copy_leng = t.n + zip_GETBITS(e);
            zip_DUMPBITS(e);
            zip_NEEDBITS(zip_bd);
            t = zip_td.list[zip_GETBITS(zip_bd)];
            e = t.e;
            while (e > 16) {
                if (e == 99) {
                    return -1
                }
                zip_DUMPBITS(t.b);
                e -= 16;
                zip_NEEDBITS(e);
                t = t.t[zip_GETBITS(e)];
                e = t.e
            }
            zip_DUMPBITS(t.b);
            zip_NEEDBITS(e);
            zip_copy_dist = zip_wp - t.n - zip_GETBITS(e);
            zip_DUMPBITS(e);
            while (zip_copy_leng > 0 && n < size) {
                zip_copy_leng--;
                zip_copy_dist &= zip_WSIZE - 1;
                zip_wp &= zip_WSIZE - 1;
                buff[off + n++] = zip_slide[zip_wp++] = zip_slide[zip_copy_dist++]
            }
            if (n == size) {
                return size
            }
        }
        zip_method = -1;
        return n
    };
    var zip_inflate_stored = function (buff, off, size) {
        var n;
        n = zip_bit_len & 7;
        zip_DUMPBITS(n);
        zip_NEEDBITS(16);
        n = zip_GETBITS(16);
        zip_DUMPBITS(16);
        zip_NEEDBITS(16);
        if (n != ((~zip_bit_buf) & 65535)) {
            return -1
        }
        zip_DUMPBITS(16);
        zip_copy_leng = n;
        n = 0;
        while (zip_copy_leng > 0 && n < size) {
            zip_copy_leng--;
            zip_wp &= zip_WSIZE - 1;
            zip_NEEDBITS(8);
            buff[off + n++] = zip_slide[zip_wp++] = zip_GETBITS(8);
            zip_DUMPBITS(8)
        }
        if (zip_copy_leng == 0) {
            zip_method = -1
        }
        return n
    };
    var zip_inflate_fixed = function (buff, off, size) {
        if (zip_fixed_tl == null) {
            var i;
            var l = new Array(288);
            var h;
            for (i = 0; i < 144; i++) {
                l[i] = 8
            }
            for (; i < 256; i++) {
                l[i] = 9
            }
            for (; i < 280; i++) {
                l[i] = 7
            }
            for (; i < 288; i++) {
                l[i] = 8
            }
            zip_fixed_bl = 7;
            h = new zip_HuftBuild(l, 288, 257, zip_cplens, zip_cplext, zip_fixed_bl);
            if (h.status != 0) {
                alert("HufBuild error: " + h.status);
                return -1
            }
            zip_fixed_tl = h.root;
            zip_fixed_bl = h.m;
            for (i = 0; i < 30; i++) {
                l[i] = 5
            }
            zip_fixed_bd = 5;
            h = new zip_HuftBuild(l, 30, 0, zip_cpdist, zip_cpdext, zip_fixed_bd);
            if (h.status > 1) {
                zip_fixed_tl = null;
                alert("HufBuild error: " + h.status);
                return -1
            }
            zip_fixed_td = h.root;
            zip_fixed_bd = h.m
        }
        zip_tl = zip_fixed_tl;
        zip_td = zip_fixed_td;
        zip_bl = zip_fixed_bl;
        zip_bd = zip_fixed_bd;
        return zip_inflate_codes(buff, off, size)
    };
    var zip_inflate_dynamic = function (buff, off, size) {
        var i;
        var j;
        var l;
        var n;
        var t;
        var nb;
        var nl;
        var nd;
        var ll = new Array(286 + 30);
        var h;
        for (i = 0; i < ll.length; i++) {
            ll[i] = 0
        }
        zip_NEEDBITS(5);
        nl = 257 + zip_GETBITS(5);
        zip_DUMPBITS(5);
        zip_NEEDBITS(5);
        nd = 1 + zip_GETBITS(5);
        zip_DUMPBITS(5);
        zip_NEEDBITS(4);
        nb = 4 + zip_GETBITS(4);
        zip_DUMPBITS(4);
        if (nl > 286 || nd > 30) {
            return -1
        }
        for (j = 0; j < nb; j++) {
            zip_NEEDBITS(3);
            ll[zip_border[j]] = zip_GETBITS(3);
            zip_DUMPBITS(3)
        }
        for (; j < 19; j++) {
            ll[zip_border[j]] = 0
        }
        zip_bl = 7;
        h = new zip_HuftBuild(ll, 19, 19, null, null, zip_bl);
        if (h.status != 0) {
            return -1
        }
        zip_tl = h.root;
        zip_bl = h.m;
        n = nl + nd;
        i = l = 0;
        while (i < n) {
            zip_NEEDBITS(zip_bl);
            t = zip_tl.list[zip_GETBITS(zip_bl)];
            j = t.b;
            zip_DUMPBITS(j);
            j = t.n;
            if (j < 16) {
                ll[i++] = l = j
            } else {
                if (j == 16) {
                    zip_NEEDBITS(2);
                    j = 3 + zip_GETBITS(2);
                    zip_DUMPBITS(2);
                    if (i + j > n) {
                        return -1
                    }
                    while (j-- > 0) {
                        ll[i++] = l
                    }
                } else {
                    if (j == 17) {
                        zip_NEEDBITS(3);
                        j = 3 + zip_GETBITS(3);
                        zip_DUMPBITS(3);
                        if (i + j > n) {
                            return -1
                        }
                        while (j-- > 0) {
                            ll[i++] = 0
                        }
                        l = 0
                    } else {
                        zip_NEEDBITS(7);
                        j = 11 + zip_GETBITS(7);
                        zip_DUMPBITS(7);
                        if (i + j > n) {
                            return -1
                        }
                        while (j-- > 0) {
                            ll[i++] = 0
                        }
                        l = 0
                    }
                }
            }
        }
        zip_bl = zip_lbits;
        h = new zip_HuftBuild(ll, nl, 257, zip_cplens, zip_cplext, zip_bl);
        if (zip_bl == 0) {
            h.status = 1
        }
        if (h.status != 0) {
            if (h.status == 1) {
            }
            return -1
        }
        zip_tl = h.root;
        zip_bl = h.m;
        for (i = 0; i < nd; i++) {
            ll[i] = ll[i + nl]
        }
        zip_bd = zip_dbits;
        h = new zip_HuftBuild(ll, nd, 0, zip_cpdist, zip_cpdext, zip_bd);
        zip_td = h.root;
        zip_bd = h.m;
        if (zip_bd == 0 && nl > 257) {
            return -1
        }
        if (h.status == 1) {
        }
        if (h.status != 0) {
            return -1
        }
        return zip_inflate_codes(buff, off, size)
    };
    var zip_inflate_start = function () {
        var i;
        if (zip_slide == null) {
            zip_slide = new Array(2 * zip_WSIZE)
        }
        zip_wp = 0;
        zip_bit_buf = 0;
        zip_bit_len = 0;
        zip_method = -1;
        zip_eof = false;
        zip_copy_leng = zip_copy_dist = 0;
        zip_tl = null
    };
    var zip_inflate_internal = function (buff, off, size) {
        var n, i;
        n = 0;
        while (n < size) {
            if (zip_eof && zip_method == -1) {
                return n
            }
            if (zip_copy_leng > 0) {
                if (zip_method != zip_STORED_BLOCK) {
                    while (zip_copy_leng > 0 && n < size) {
                        zip_copy_leng--;
                        zip_copy_dist &= zip_WSIZE - 1;
                        zip_wp &= zip_WSIZE - 1;
                        buff[off + n++] = zip_slide[zip_wp++] = zip_slide[zip_copy_dist++]
                    }
                } else {
                    while (zip_copy_leng > 0 && n < size) {
                        zip_copy_leng--;
                        zip_wp &= zip_WSIZE - 1;
                        zip_NEEDBITS(8);
                        buff[off + n++] = zip_slide[zip_wp++] = zip_GETBITS(8);
                        zip_DUMPBITS(8)
                    }
                    if (zip_copy_leng == 0) {
                        zip_method = -1
                    }
                }
                if (n == size) {
                    return n
                }
            }
            if (zip_method == -1) {
                if (zip_eof) {
                    break
                }
                zip_NEEDBITS(1);
                if (zip_GETBITS(1) != 0) {
                    zip_eof = true
                }
                zip_DUMPBITS(1);
                zip_NEEDBITS(2);
                zip_method = zip_GETBITS(2);
                zip_DUMPBITS(2);
                zip_tl = null;
                zip_copy_leng = 0
            }
            switch (zip_method) {
                case 0:
                    i = zip_inflate_stored(buff, off + n, size - n);
                    break;
                case 1:
                    if (zip_tl != null) {
                        i = zip_inflate_codes(buff, off + n, size - n)
                    } else {
                        i = zip_inflate_fixed(buff, off + n, size - n)
                    }
                    break;
                case 2:
                    if (zip_tl != null) {
                        i = zip_inflate_codes(buff, off + n, size - n)
                    } else {
                        i = zip_inflate_dynamic(buff, off + n, size - n)
                    }
                    break;
                default:
                    i = -1;
                    break
            }
            if (i == -1) {
                if (zip_eof) {
                    return 0
                }
                return -1
            }
            n += i
        }
        return n
    };
    var zip_inflate = function (str) {
        var i, j;
        zip_inflate_start();
        zip_inflate_data = str;
        zip_inflate_pos = 0;
        var buff = new Array(1024);
        var aout = [];
        while ((i = zip_inflate_internal(buff, 0, buff.length)) > 0) {
            var cbuf = new Array(i);
            for (j = 0; j < i; j++) {
                cbuf[j] = String.fromCharCode(buff[j])
            }
            aout[aout.length] = cbuf.join("")
        }
        zip_inflate_data = null;
        return aout.join("")
    };
    if (!ctx.RawDeflate) {
        ctx.RawDeflate = {}
    }
    ctx.RawDeflate.inflate = zip_inflate
})(this);

/*
 CryptoJS v3.1.2
 code.google.com/p/crypto-js
 (c) 2009-2013 by Jeff Mott. All rights reserved.
 code.google.com/p/crypto-js/wiki/License
 */
var CryptoJS = CryptoJS || function (u, p) {
        var d = {}, l = d.lib = {}, s = function () {
            }, t = l.Base = {
                extend: function (a) {
                    s.prototype = this;
                    var c = new s;
                    a && c.mixIn(a);
                    c.hasOwnProperty("init") || (c.init = function () {
                        c.$super.init.apply(this, arguments)
                    });
                    c.init.prototype = c;
                    c.$super = this;
                    return c
                }, create: function () {
                    var a = this.extend();
                    a.init.apply(a, arguments);
                    return a
                }, init: function () {
                }, mixIn: function (a) {
                    for (var c in a)a.hasOwnProperty(c) && (this[c] = a[c]);
                    a.hasOwnProperty("toString") && (this.toString = a.toString)
                }, clone: function () {
                    return this.init.prototype.extend(this)
                }
            },
            r = l.WordArray = t.extend({
                init: function (a, c) {
                    a = this.words = a || [];
                    this.sigBytes = c != p ? c : 4 * a.length
                }, toString: function (a) {
                    return (a || v).stringify(this)
                }, concat: function (a) {
                    var c = this.words, e = a.words, j = this.sigBytes;
                    a = a.sigBytes;
                    this.clamp();
                    if (j % 4)for (var k = 0; k < a; k++)c[j + k >>> 2] |= (e[k >>> 2] >>> 24 - 8 * (k % 4) & 255) << 24 - 8 * ((j + k) % 4); else if (65535 < e.length)for (k = 0; k < a; k += 4)c[j + k >>> 2] = e[k >>> 2]; else c.push.apply(c, e);
                    this.sigBytes += a;
                    return this
                }, clamp: function () {
                    var a = this.words, c = this.sigBytes;
                    a[c >>> 2] &= 4294967295 <<
                        32 - 8 * (c % 4);
                    a.length = u.ceil(c / 4)
                }, clone: function () {
                    var a = t.clone.call(this);
                    a.words = this.words.slice(0);
                    return a
                }, random: function (a) {
                    for (var c = [],
                             e = 0; e < a; e += 4)c.push(4294967296 * u.random() | 0);
                    return new r.init(c, a)
                }
            }), w = d.enc = {}, v = w.Hex = {
                stringify: function (a) {
                    var c = a.words;
                    a = a.sigBytes;
                    for (var e = [], j = 0; j < a; j++) {
                        var k = c[j >>> 2] >>> 24 - 8 * (j % 4) & 255;
                        e.push((k >>> 4).toString(16));
                        e.push((k & 15).toString(16))
                    }
                    return e.join("")
                }, parse: function (a) {
                    for (var c = a.length, e = [],
                             j = 0; j < c; j += 2)e[j >>> 3] |= parseInt(a.substr(j,
                            2), 16) << 24 - 4 * (j % 8);
                    return new r.init(e, c / 2)
                }
            }, b = w.Latin1 = {
                stringify: function (a) {
                    var c = a.words;
                    a = a.sigBytes;
                    for (var e = [],
                             j = 0; j < a; j++)e.push(String.fromCharCode(c[j >>> 2] >>> 24 - 8 * (j % 4) & 255));
                    return e.join("")
                }, parse: function (a) {
                    for (var c = a.length, e = [],
                             j = 0; j < c; j++)e[j >>> 2] |= (a.charCodeAt(j) & 255) << 24 - 8 * (j % 4);
                    return new r.init(e, c)
                }
            }, x = w.Utf8 = {
                stringify: function (a) {
                    try {
                        return decodeURIComponent(escape(b.stringify(a)))
                    } catch (c) {
                        throw Error("Malformed UTF-8 data");
                    }
                }, parse: function (a) {
                    return b.parse(unescape(encodeURIComponent(a)))
                }
            },
            q = l.BufferedBlockAlgorithm = t.extend({
                reset: function () {
                    this._data = new r.init;
                    this._nDataBytes = 0
                }, _append: function (a) {
                    "string" == typeof a && (a = x.parse(a));
                    this._data.concat(a);
                    this._nDataBytes += a.sigBytes
                }, _process: function (a) {
                    var c = this._data, e = c.words, j = c.sigBytes,
                        k = this.blockSize, b = j / (4 * k),
                        b = a ? u.ceil(b) : u.max((b | 0) - this._minBufferSize, 0);
                    a = b * k;
                    j = u.min(4 * a, j);
                    if (a) {
                        for (var q = 0; q < a; q += k)this._doProcessBlock(e, q);
                        q = e.splice(0, a);
                        c.sigBytes -= j
                    }
                    return new r.init(q, j)
                }, clone: function () {
                    var a = t.clone.call(this);
                    a._data = this._data.clone();
                    return a
                }, _minBufferSize: 0
            });
        l.Hasher = q.extend({
            cfg: t.extend(), init: function (a) {
                this.cfg = this.cfg.extend(a);
                this.reset()
            }, reset: function () {
                q.reset.call(this);
                this._doReset()
            }, update: function (a) {
                this._append(a);
                this._process();
                return this
            }, finalize: function (a) {
                a && this._append(a);
                return this._doFinalize()
            }, blockSize: 16, _createHelper: function (a) {
                return function (b, e) {
                    return (new a.init(e)).finalize(b)
                }
            }, _createHmacHelper: function (a) {
                return function (b, e) {
                    return (new n.HMAC.init(a,
                        e)).finalize(b)
                }
            }
        });
        var n = d.algo = {};
        return d
    }(Math);
(function () {
    var u = CryptoJS, p = u.lib.WordArray;
    u.enc.Base64 = {
        stringify: function (d) {
            var l = d.words, p = d.sigBytes, t = this._map;
            d.clamp();
            d = [];
            for (var r = 0; r < p; r += 3)for (var w = (l[r >>> 2] >>> 24 - 8 * (r % 4) & 255) << 16 | (l[r + 1 >>> 2] >>> 24 - 8 * ((r + 1) % 4) & 255) << 8 | l[r + 2 >>> 2] >>> 24 - 8 * ((r + 2) % 4) & 255,
                                                   v = 0; 4 > v && r + 0.75 * v < p; v++)d.push(t.charAt(w >>> 6 * (3 - v) & 63));
            if (l = t.charAt(64))for (; d.length % 4;)d.push(l);
            return d.join("")
        },
        parse: function (d) {
            var l = d.length, s = this._map, t = s.charAt(64);
            t && (t = d.indexOf(t), -1 != t && (l = t));
            for (var t = [], r = 0, w = 0; w <
            l; w++)if (w % 4) {
                var v = s.indexOf(d.charAt(w - 1)) << 2 * (w % 4),
                    b = s.indexOf(d.charAt(w)) >>> 6 - 2 * (w % 4);
                t[r >>> 2] |= (v | b) << 24 - 8 * (r % 4);
                r++
            }
            return p.create(t, r)
        },
        _map: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    }
})();
(function (u) {
    function p(b, n, a, c, e, j, k) {
        b = b + (n & a | ~n & c) + e + k;
        return (b << j | b >>> 32 - j) + n
    }

    function d(b, n, a, c, e, j, k) {
        b = b + (n & c | a & ~c) + e + k;
        return (b << j | b >>> 32 - j) + n
    }

    function l(b, n, a, c, e, j, k) {
        b = b + (n ^ a ^ c) + e + k;
        return (b << j | b >>> 32 - j) + n
    }

    function s(b, n, a, c, e, j, k) {
        b = b + (a ^ (n | ~c)) + e + k;
        return (b << j | b >>> 32 - j) + n
    }

    for (var t = CryptoJS, r = t.lib, w = r.WordArray, v = r.Hasher, r = t.algo,
             b = [],
             x = 0; 64 > x; x++)b[x] = 4294967296 * u.abs(u.sin(x + 1)) | 0;
    r = r.MD5 = v.extend({
        _doReset: function () {
            this._hash = new w.init([1732584193, 4023233417, 2562383102, 271733878])
        },
        _doProcessBlock: function (q, n) {
            for (var a = 0; 16 > a; a++) {
                var c = n + a, e = q[c];
                q[c] = (e << 8 | e >>> 24) & 16711935 | (e << 24 | e >>> 8) & 4278255360
            }
            var a = this._hash.words, c = q[n + 0], e = q[n + 1], j = q[n + 2],
                k = q[n + 3], z = q[n + 4], r = q[n + 5], t = q[n + 6],
                w = q[n + 7], v = q[n + 8], A = q[n + 9], B = q[n + 10],
                C = q[n + 11], u = q[n + 12], D = q[n + 13], E = q[n + 14],
                x = q[n + 15], f = a[0], m = a[1], g = a[2], h = a[3],
                f = p(f, m, g, h, c, 7, b[0]), h = p(h, f, m, g, e, 12, b[1]),
                g = p(g, h, f, m, j, 17, b[2]), m = p(m, g, h, f, k, 22, b[3]),
                f = p(f, m, g, h, z, 7, b[4]), h = p(h, f, m, g, r, 12, b[5]),
                g = p(g, h, f, m, t, 17, b[6]), m = p(m, g, h, f, w, 22, b[7]),
                f = p(f, m, g, h, v, 7, b[8]), h = p(h, f, m, g, A, 12, b[9]),
                g = p(g, h, f, m, B, 17, b[10]),
                m = p(m, g, h, f, C, 22, b[11]), f = p(f, m, g, h, u, 7, b[12]),
                h = p(h, f, m, g, D, 12, b[13]),
                g = p(g, h, f, m, E, 17, b[14]),
                m = p(m, g, h, f, x, 22, b[15]), f = d(f, m, g, h, e, 5, b[16]),
                h = d(h, f, m, g, t, 9, b[17]), g = d(g, h, f, m, C, 14, b[18]),
                m = d(m, g, h, f, c, 20, b[19]), f = d(f, m, g, h, r, 5, b[20]),
                h = d(h, f, m, g, B, 9, b[21]), g = d(g, h, f, m, x, 14, b[22]),
                m = d(m, g, h, f, z, 20, b[23]), f = d(f, m, g, h, A, 5, b[24]),
                h = d(h, f, m, g, E, 9, b[25]), g = d(g, h, f, m, k, 14, b[26]),
                m = d(m, g, h, f, v, 20, b[27]), f = d(f, m, g, h, D, 5, b[28]),
                h = d(h, f,
                    m, g, j, 9, b[29]), g = d(g, h, f, m, w, 14, b[30]),
                m = d(m, g, h, f, u, 20, b[31]), f = l(f, m, g, h, r, 4, b[32]),
                h = l(h, f, m, g, v, 11, b[33]),
                g = l(g, h, f, m, C, 16, b[34]),
                m = l(m, g, h, f, E, 23, b[35]), f = l(f, m, g, h, e, 4, b[36]),
                h = l(h, f, m, g, z, 11, b[37]),
                g = l(g, h, f, m, w, 16, b[38]),
                m = l(m, g, h, f, B, 23, b[39]), f = l(f, m, g, h, D, 4, b[40]),
                h = l(h, f, m, g, c, 11, b[41]),
                g = l(g, h, f, m, k, 16, b[42]),
                m = l(m, g, h, f, t, 23, b[43]), f = l(f, m, g, h, A, 4, b[44]),
                h = l(h, f, m, g, u, 11, b[45]),
                g = l(g, h, f, m, x, 16, b[46]),
                m = l(m, g, h, f, j, 23, b[47]), f = s(f, m, g, h, c, 6, b[48]),
                h = s(h, f, m, g, w, 10, b[49]), g = s(g, h, f, m,
                E, 15, b[50]), m = s(m, g, h, f, r, 21, b[51]),
                f = s(f, m, g, h, u, 6, b[52]), h = s(h, f, m, g, k, 10, b[53]),
                g = s(g, h, f, m, B, 15, b[54]),
                m = s(m, g, h, f, e, 21, b[55]), f = s(f, m, g, h, v, 6, b[56]),
                h = s(h, f, m, g, x, 10, b[57]),
                g = s(g, h, f, m, t, 15, b[58]),
                m = s(m, g, h, f, D, 21, b[59]), f = s(f, m, g, h, z, 6, b[60]),
                h = s(h, f, m, g, C, 10, b[61]),
                g = s(g, h, f, m, j, 15, b[62]),
                m = s(m, g, h, f, A, 21, b[63]);
            a[0] = a[0] + f | 0;
            a[1] = a[1] + m | 0;
            a[2] = a[2] + g | 0;
            a[3] = a[3] + h | 0
        }, _doFinalize: function () {
            var b = this._data, n = b.words, a = 8 * this._nDataBytes,
                c = 8 * b.sigBytes;
            n[c >>> 5] |= 128 << 24 - c % 32;
            var e = u.floor(a /
                4294967296);
            n[(c + 64 >>> 9 << 4) + 15] = (e << 8 | e >>> 24) & 16711935 | (e << 24 | e >>> 8) & 4278255360;
            n[(c + 64 >>> 9 << 4) + 14] = (a << 8 | a >>> 24) & 16711935 | (a << 24 | a >>> 8) & 4278255360;
            b.sigBytes = 4 * (n.length + 1);
            this._process();
            b = this._hash;
            n = b.words;
            for (a = 0; 4 > a; a++)c = n[a], n[a] = (c << 8 | c >>> 24) & 16711935 | (c << 24 | c >>> 8) & 4278255360;
            return b
        }, clone: function () {
            var b = v.clone.call(this);
            b._hash = this._hash.clone();
            return b
        }
    });
    t.MD5 = v._createHelper(r);
    t.HmacMD5 = v._createHmacHelper(r)
})(Math);
(function () {
    var u = CryptoJS, p = u.lib, d = p.Base, l = p.WordArray, p = u.algo,
        s = p.EvpKDF = d.extend({
            cfg: d.extend({
                keySize: 4,
                hasher: p.MD5,
                iterations: 1
            }), init: function (d) {
                this.cfg = this.cfg.extend(d)
            }, compute: function (d, r) {
                for (var p = this.cfg, s = p.hasher.create(), b = l.create(),
                         u = b.words, q = p.keySize,
                         p = p.iterations; u.length < q;) {
                    n && s.update(n);
                    var n = s.update(d).finalize(r);
                    s.reset();
                    for (var a = 1; a < p; a++)n = s.finalize(n), s.reset();
                    b.concat(n)
                }
                b.sigBytes = 4 * q;
                return b
            }
        });
    u.EvpKDF = function (d, l, p) {
        return s.create(p).compute(d,
            l)
    }
})();
CryptoJS.lib.Cipher || function (u) {
    var p = CryptoJS, d = p.lib, l = d.Base, s = d.WordArray,
        t = d.BufferedBlockAlgorithm, r = p.enc.Base64, w = p.algo.EvpKDF,
        v = d.Cipher = t.extend({
            cfg: l.extend(),
            createEncryptor: function (e, a) {
                return this.create(this._ENC_XFORM_MODE, e, a)
            },
            createDecryptor: function (e, a) {
                return this.create(this._DEC_XFORM_MODE, e, a)
            },
            init: function (e, a, b) {
                this.cfg = this.cfg.extend(b);
                this._xformMode = e;
                this._key = a;
                this.reset()
            },
            reset: function () {
                t.reset.call(this);
                this._doReset()
            },
            process: function (e) {
                this._append(e);
                return this._process()
            },
            finalize: function (e) {
                e && this._append(e);
                return this._doFinalize()
            },
            keySize: 4,
            ivSize: 4,
            _ENC_XFORM_MODE: 1,
            _DEC_XFORM_MODE: 2,
            _createHelper: function (e) {
                return {
                    encrypt: function (b, k, d) {
                        return ("string" == typeof k ? c : a).encrypt(e, b, k, d)
                    }, decrypt: function (b, k, d) {
                        return ("string" == typeof k ? c : a).decrypt(e, b, k, d)
                    }
                }
            }
        });
    d.StreamCipher = v.extend({
        _doFinalize: function () {
            return this._process(!0)
        }, blockSize: 1
    });
    var b = p.mode = {}, x = function (e, a, b) {
        var c = this._iv;
        c ? this._iv = u : c = this._prevBlock;
        for (var d = 0; d < b; d++)e[a + d] ^=
            c[d]
    }, q = (d.BlockCipherMode = l.extend({
        createEncryptor: function (e, a) {
            return this.Encryptor.create(e, a)
        }, createDecryptor: function (e, a) {
            return this.Decryptor.create(e, a)
        }, init: function (e, a) {
            this._cipher = e;
            this._iv = a
        }
    })).extend();
    q.Encryptor = q.extend({
        processBlock: function (e, a) {
            var b = this._cipher, c = b.blockSize;
            x.call(this, e, a, c);
            b.encryptBlock(e, a);
            this._prevBlock = e.slice(a, a + c)
        }
    });
    q.Decryptor = q.extend({
        processBlock: function (e, a) {
            var b = this._cipher, c = b.blockSize, d = e.slice(a, a + c);
            b.decryptBlock(e, a);
            x.call(this,
                e, a, c);
            this._prevBlock = d
        }
    });
    b = b.CBC = q;
    q = (p.pad = {}).Pkcs7 = {
        pad: function (a, b) {
            for (var c = 4 * b, c = c - a.sigBytes % c,
                     d = c << 24 | c << 16 | c << 8 | c, l = [],
                     n = 0; n < c; n += 4)l.push(d);
            c = s.create(l, c);
            a.concat(c)
        }, unpad: function (a) {
            a.sigBytes -= a.words[a.sigBytes - 1 >>> 2] & 255
        }
    };
    d.BlockCipher = v.extend({
        cfg: v.cfg.extend({mode: b, padding: q}), reset: function () {
            v.reset.call(this);
            var a = this.cfg, b = a.iv, a = a.mode;
            if (this._xformMode == this._ENC_XFORM_MODE)var c = a.createEncryptor; else c = a.createDecryptor, this._minBufferSize = 1;
            this._mode = c.call(a,
                this, b && b.words)
        }, _doProcessBlock: function (a, b) {
            this._mode.processBlock(a, b)
        }, _doFinalize: function () {
            var a = this.cfg.padding;
            if (this._xformMode == this._ENC_XFORM_MODE) {
                a.pad(this._data, this.blockSize);
                var b = this._process(!0)
            } else b = this._process(!0), a.unpad(b);
            return b
        }, blockSize: 4
    });
    var n = d.CipherParams = l.extend({
        init: function (a) {
            this.mixIn(a)
        }, toString: function (a) {
            return (a || this.formatter).stringify(this)
        }
    }), b = (p.format = {}).OpenSSL = {
        stringify: function (a) {
            var b = a.ciphertext;
            a = a.salt;
            return (a ? s.create([1398893684,
                1701076831]).concat(a).concat(b) : b).toString(r)
        }, parse: function (a) {
            a = r.parse(a);
            var b = a.words;
            if (1398893684 == b[0] && 1701076831 == b[1]) {
                var c = s.create(b.slice(2, 4));
                b.splice(0, 4);
                a.sigBytes -= 16
            }
            return n.create({ciphertext: a, salt: c})
        }
    }, a = d.SerializableCipher = l.extend({
        cfg: l.extend({format: b}), encrypt: function (a, b, c, d) {
            d = this.cfg.extend(d);
            var l = a.createEncryptor(c, d);
            b = l.finalize(b);
            l = l.cfg;
            return n.create({
                ciphertext: b,
                key: c,
                iv: l.iv,
                algorithm: a,
                mode: l.mode,
                padding: l.padding,
                blockSize: a.blockSize,
                formatter: d.format
            })
        },
        decrypt: function (a, b, c, d) {
            d = this.cfg.extend(d);
            b = this._parse(b, d.format);
            return a.createDecryptor(c, d).finalize(b.ciphertext)
        }, _parse: function (a, b) {
            return "string" == typeof a ? b.parse(a, this) : a
        }
    }), p = (p.kdf = {}).OpenSSL = {
        execute: function (a, b, c, d) {
            d || (d = s.random(8));
            a = w.create({keySize: b + c}).compute(a, d);
            c = s.create(a.words.slice(b), 4 * c);
            a.sigBytes = 4 * b;
            return n.create({key: a, iv: c, salt: d})
        }
    }, c = d.PasswordBasedCipher = a.extend({
        cfg: a.cfg.extend({kdf: p}), encrypt: function (b, c, d, l) {
            l = this.cfg.extend(l);
            d = l.kdf.execute(d,
                b.keySize, b.ivSize);
            l.iv = d.iv;
            b = a.encrypt.call(this, b, c, d.key, l);
            b.mixIn(d);
            return b
        }, decrypt: function (b, c, d, l) {
            l = this.cfg.extend(l);
            c = this._parse(c, l.format);
            d = l.kdf.execute(d, b.keySize, b.ivSize, c.salt);
            l.iv = d.iv;
            return a.decrypt.call(this, b, c, d.key, l)
        }
    })
}();
(function () {
    for (var u = CryptoJS, p = u.lib.BlockCipher, d = u.algo, l = [], s = [],
             t = [], r = [], w = [], v = [], b = [], x = [], q = [], n = [],
             a = [], c = 0; 256 > c; c++)a[c] = 128 > c ? c << 1 : c << 1 ^ 283;
    for (var e = 0, j = 0, c = 0; 256 > c; c++) {
        var k = j ^ j << 1 ^ j << 2 ^ j << 3 ^ j << 4,
            k = k >>> 8 ^ k & 255 ^ 99;
        l[e] = k;
        s[k] = e;
        var z = a[e], F = a[z], G = a[F], y = 257 * a[k] ^ 16843008 * k;
        t[e] = y << 24 | y >>> 8;
        r[e] = y << 16 | y >>> 16;
        w[e] = y << 8 | y >>> 24;
        v[e] = y;
        y = 16843009 * G ^ 65537 * F ^ 257 * z ^ 16843008 * e;
        b[k] = y << 24 | y >>> 8;
        x[k] = y << 16 | y >>> 16;
        q[k] = y << 8 | y >>> 24;
        n[k] = y;
        e ? (e = z ^ a[a[a[G ^ z]]], j ^= a[a[j]]) : e = j = 1
    }
    var H = [0, 1, 2, 4, 8,
        16, 32, 64, 128, 27, 54], d = d.AES = p.extend({
        _doReset: function () {
            for (var a = this._key, c = a.words, d = a.sigBytes / 4,
                     a = 4 * ((this._nRounds = d + 6) + 1),
                     e = this._keySchedule = [],
                     j = 0; j < a; j++)if (j < d) e[j] = c[j]; else {
                var k = e[j - 1];
                j % d ? 6 < d && 4 == j % d && (k = l[k >>> 24] << 24 | l[k >>> 16 & 255] << 16 | l[k >>> 8 & 255] << 8 | l[k & 255]) : (k = k << 8 | k >>> 24, k = l[k >>> 24] << 24 | l[k >>> 16 & 255] << 16 | l[k >>> 8 & 255] << 8 | l[k & 255], k ^= H[j / d | 0] << 24);
                e[j] = e[j - d] ^ k
            }
            c = this._invKeySchedule = [];
            for (d = 0; d < a; d++)j = a - d, k = d % 4 ? e[j] : e[j - 4], c[d] = 4 > d || 4 >= j ? k : b[l[k >>> 24]] ^ x[l[k >>> 16 & 255]] ^ q[l[k >>>
                8 & 255]] ^ n[l[k & 255]]
        }, encryptBlock: function (a, b) {
            this._doCryptBlock(a, b, this._keySchedule, t, r, w, v, l)
        }, decryptBlock: function (a, c) {
            var d = a[c + 1];
            a[c + 1] = a[c + 3];
            a[c + 3] = d;
            this._doCryptBlock(a, c, this._invKeySchedule, b, x, q, n, s);
            d = a[c + 1];
            a[c + 1] = a[c + 3];
            a[c + 3] = d
        }, _doCryptBlock: function (a, b, c, d, e, j, l, f) {
            for (var m = this._nRounds, g = a[b] ^ c[0], h = a[b + 1] ^ c[1],
                     k = a[b + 2] ^ c[2], n = a[b + 3] ^ c[3], p = 4,
                     r = 1; r < m; r++)var q = d[g >>> 24] ^ e[h >>> 16 & 255] ^ j[k >>> 8 & 255] ^ l[n & 255] ^ c[p++],
                     s = d[h >>> 24] ^ e[k >>> 16 & 255] ^ j[n >>> 8 & 255] ^ l[g & 255] ^ c[p++],
                     t =
                         d[k >>> 24] ^ e[n >>> 16 & 255] ^ j[g >>> 8 & 255] ^ l[h & 255] ^ c[p++],
                     n = d[n >>> 24] ^ e[g >>> 16 & 255] ^ j[h >>> 8 & 255] ^ l[k & 255] ^ c[p++],
                     g = q, h = s, k = t;
            q = (f[g >>> 24] << 24 | f[h >>> 16 & 255] << 16 | f[k >>> 8 & 255] << 8 | f[n & 255]) ^ c[p++];
            s = (f[h >>> 24] << 24 | f[k >>> 16 & 255] << 16 | f[n >>> 8 & 255] << 8 | f[g & 255]) ^ c[p++];
            t = (f[k >>> 24] << 24 | f[n >>> 16 & 255] << 16 | f[g >>> 8 & 255] << 8 | f[h & 255]) ^ c[p++];
            n = (f[n >>> 24] << 24 | f[g >>> 16 & 255] << 16 | f[h >>> 8 & 255] << 8 | f[k & 255]) ^ c[p++];
            a[b] = q;
            a[b + 1] = s;
            a[b + 2] = t;
            a[b + 3] = n
        }, keySize: 8
    });
    u.AES = p._createHelper(d)
})();


/*
 CryptoJS v3.1.2
 code.google.com/p/crypto-js
 (c) 2009-2013 by Jeff Mott. All rights reserved.
 code.google.com/p/crypto-js/wiki/License
 */
var CryptoJS = CryptoJS || function (h, r) {
        var k = {}, l = k.lib = {}, n = function () {
            }, f = l.Base = {
                extend: function (a) {
                    n.prototype = this;
                    var b = new n;
                    a && b.mixIn(a);
                    b.hasOwnProperty("init") || (b.init = function () {
                        b.$super.init.apply(this, arguments)
                    });
                    b.init.prototype = b;
                    b.$super = this;
                    return b
                }, create: function () {
                    var a = this.extend();
                    a.init.apply(a, arguments);
                    return a
                }, init: function () {
                }, mixIn: function (a) {
                    for (var b in a)a.hasOwnProperty(b) && (this[b] = a[b]);
                    a.hasOwnProperty("toString") && (this.toString = a.toString)
                }, clone: function () {
                    return this.init.prototype.extend(this)
                }
            },
            j = l.WordArray = f.extend({
                init: function (a, b) {
                    a = this.words = a || [];
                    this.sigBytes = b != r ? b : 4 * a.length
                }, toString: function (a) {
                    return (a || s).stringify(this)
                }, concat: function (a) {
                    var b = this.words, d = a.words, c = this.sigBytes;
                    a = a.sigBytes;
                    this.clamp();
                    if (c % 4)for (var e = 0; e < a; e++)b[c + e >>> 2] |= (d[e >>> 2] >>> 24 - 8 * (e % 4) & 255) << 24 - 8 * ((c + e) % 4); else if (65535 < d.length)for (e = 0; e < a; e += 4)b[c + e >>> 2] = d[e >>> 2]; else b.push.apply(b, d);
                    this.sigBytes += a;
                    return this
                }, clamp: function () {
                    var a = this.words, b = this.sigBytes;
                    a[b >>> 2] &= 4294967295 <<
                        32 - 8 * (b % 4);
                    a.length = h.ceil(b / 4)
                }, clone: function () {
                    var a = f.clone.call(this);
                    a.words = this.words.slice(0);
                    return a
                }, random: function (a) {
                    for (var b = [],
                             d = 0; d < a; d += 4)b.push(4294967296 * h.random() | 0);
                    return new j.init(b, a)
                }
            }), m = k.enc = {}, s = m.Hex = {
                stringify: function (a) {
                    var b = a.words;
                    a = a.sigBytes;
                    for (var d = [], c = 0; c < a; c++) {
                        var e = b[c >>> 2] >>> 24 - 8 * (c % 4) & 255;
                        d.push((e >>> 4).toString(16));
                        d.push((e & 15).toString(16))
                    }
                    return d.join("")
                }, parse: function (a) {
                    for (var b = a.length, d = [],
                             c = 0; c < b; c += 2)d[c >>> 3] |= parseInt(a.substr(c,
                            2), 16) << 24 - 4 * (c % 8);
                    return new j.init(d, b / 2)
                }
            }, p = m.Latin1 = {
                stringify: function (a) {
                    var b = a.words;
                    a = a.sigBytes;
                    for (var d = [],
                             c = 0; c < a; c++)d.push(String.fromCharCode(b[c >>> 2] >>> 24 - 8 * (c % 4) & 255));
                    return d.join("")
                }, parse: function (a) {
                    for (var b = a.length, d = [],
                             c = 0; c < b; c++)d[c >>> 2] |= (a.charCodeAt(c) & 255) << 24 - 8 * (c % 4);
                    return new j.init(d, b)
                }
            }, t = m.Utf8 = {
                stringify: function (a) {
                    try {
                        return decodeURIComponent(escape(p.stringify(a)))
                    } catch (b) {
                        throw Error("Malformed UTF-8 data");
                    }
                }, parse: function (a) {
                    return p.parse(unescape(encodeURIComponent(a)))
                }
            },
            q = l.BufferedBlockAlgorithm = f.extend({
                reset: function () {
                    this._data = new j.init;
                    this._nDataBytes = 0
                }, _append: function (a) {
                    "string" == typeof a && (a = t.parse(a));
                    this._data.concat(a);
                    this._nDataBytes += a.sigBytes
                }, _process: function (a) {
                    var b = this._data, d = b.words, c = b.sigBytes,
                        e = this.blockSize, f = c / (4 * e),
                        f = a ? h.ceil(f) : h.max((f | 0) - this._minBufferSize, 0);
                    a = f * e;
                    c = h.min(4 * a, c);
                    if (a) {
                        for (var g = 0; g < a; g += e)this._doProcessBlock(d, g);
                        g = d.splice(0, a);
                        b.sigBytes -= c
                    }
                    return new j.init(g, c)
                }, clone: function () {
                    var a = f.clone.call(this);
                    a._data = this._data.clone();
                    return a
                }, _minBufferSize: 0
            });
        l.Hasher = q.extend({
            cfg: f.extend(), init: function (a) {
                this.cfg = this.cfg.extend(a);
                this.reset()
            }, reset: function () {
                q.reset.call(this);
                this._doReset()
            }, update: function (a) {
                this._append(a);
                this._process();
                return this
            }, finalize: function (a) {
                a && this._append(a);
                return this._doFinalize()
            }, blockSize: 16, _createHelper: function (a) {
                return function (b, d) {
                    return (new a.init(d)).finalize(b)
                }
            }, _createHmacHelper: function (a) {
                return function (b, d) {
                    return (new u.HMAC.init(a,
                        d)).finalize(b)
                }
            }
        });
        var u = k.algo = {};
        return k
    }(Math);

(function (global) {
    if (global.Base64_Zip) {
    }
    var version = "2.1.1";
    var buffer;
    if (typeof module !== "undefined" && module.exports) {
        buffer = require("buffer").Buffer
    }
    var b64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    var b64tab = function (bin) {
        var t = {};
        for (var i = 0, l = bin.length; i < l; i++) {
            t[bin.charAt(i)] = i
        }
        return t
    }(b64chars);
    var fromCharCode = String.fromCharCode;
    var cb_utob = function (c) {
        if (c.length < 2) {
            var cc = c.charCodeAt(0);
            return cc < 128 ? c : cc < 2048 ? (fromCharCode(192 | (cc >>> 6)) + fromCharCode(128 | (cc & 63))) : (fromCharCode(224 | ((cc >>> 12) & 15)) + fromCharCode(128 | ((cc >>> 6) & 63)) + fromCharCode(128 | (cc & 63)))
        } else {
            var cc = 65536 + (c.charCodeAt(0) - 55296) * 1024 + (c.charCodeAt(1) - 56320);
            return (fromCharCode(240 | ((cc >>> 18) & 7)) + fromCharCode(128 | ((cc >>> 12) & 63)) + fromCharCode(128 | ((cc >>> 6) & 63)) + fromCharCode(128 | (cc & 63)))
        }
    };
    var re_utob = /[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g;
    var utob = function (u) {
        return u.replace(re_utob, cb_utob)
    };
    var cb_encode = function (ccc) {
        var padlen = [0, 2, 1][ccc.length % 3],
            ord = ccc.charCodeAt(0) << 16 | ((ccc.length > 1 ? ccc.charCodeAt(1) : 0) << 8) | ((ccc.length > 2 ? ccc.charCodeAt(2) : 0)),
            chars = [b64chars.charAt(ord >>> 18), b64chars.charAt((ord >>> 12) & 63), padlen >= 2 ? "=" : b64chars.charAt((ord >>> 6) & 63), padlen >= 1 ? "=" : b64chars.charAt(ord & 63)];
        return chars.join("")
    };
    var Base64_btoa = function (b) {
        return b.replace(/[\s\S]{1,3}/g, cb_encode)
    };
    var _encode = buffer ? function (u) {
        return (new buffer(u)).toString("base64")
    } : function (u) {
        return Base64_btoa(utob(u))
    };
    var encode = function (u, urisafe) {
        return !urisafe ? _encode(u) : _encode(u).replace(/[+\/]/g, function (m0) {
            return m0 == "+" ? "-" : "_"
        }).replace(/=/g, "")
    };
    var encodeURI = function (u) {
        return encode(u, true)
    };
    var re_btou = new RegExp(["[\xC0-\xDF][\x80-\xBF]", "[\xE0-\xEF][\x80-\xBF]{2}", "[\xF0-\xF7][\x80-\xBF]{3}"].join("|"), "g");
    var cb_btou = function (cccc) {
        switch (cccc.length) {
            case 4:
                var cp = ((7 & cccc.charCodeAt(0)) << 18) | ((63 & cccc.charCodeAt(1)) << 12) | ((63 & cccc.charCodeAt(2)) << 6) | (63 & cccc.charCodeAt(3)),
                    offset = cp - 65536;
                return (fromCharCode((offset >>> 10) + 55296) + fromCharCode((offset & 1023) + 56320));
            case 3:
                return fromCharCode(((15 & cccc.charCodeAt(0)) << 12) | ((63 & cccc.charCodeAt(1)) << 6) | (63 & cccc.charCodeAt(2)));
            default:
                return fromCharCode(((31 & cccc.charCodeAt(0)) << 6) | (63 & cccc.charCodeAt(1)))
        }
    };
    var btou = function (b) {
        return b.replace(re_btou, cb_btou)
    };
    var cb_decode = function (cccc) {
        var len = cccc.length, padlen = len % 4,
            n = (len > 0 ? b64tab[cccc.charAt(0)] << 18 : 0) | (len > 1 ? b64tab[cccc.charAt(1)] << 12 : 0) | (len > 2 ? b64tab[cccc.charAt(2)] << 6 : 0) | (len > 3 ? b64tab[cccc.charAt(3)] : 0),
            chars = [fromCharCode(n >>> 16), fromCharCode((n >>> 8) & 255), fromCharCode(n & 255)];
        chars.length -= [0, 0, 2, 1][padlen];
        return chars.join("")
    };
    var Base64_atob = function (a) {
        return a.replace(/[\s\S]{1,4}/g, cb_decode)
    };
    var _decode = buffer ? function (a) {
        return (new buffer(a, "base64")).toString()
    } : function (a) {
        return btou(Base64_atob(a))
    };
    var decode = function (a) {
        return _decode(a.replace(/[-_]/g, function (m0) {
            return m0 == "-" ? "+" : "/"
        }).replace(/[^A-Za-z0-9\+\/]/g, ""))
    };
    global.Base64_Zip = {
        VERSION: version,
        atob: Base64_atob,
        btoa: Base64_btoa,
        fromBase64: decode,
        toBase64: encode,
        utob: utob,
        encode: encode,
        encodeURI: encodeURI,
        btou: btou,
        decode: decode
    };
    if (typeof Object.defineProperty === "function") {
        var noEnum = function (v) {
            return {
                value: v,
                enumerable: false,
                writable: true,
                configurable: true
            }
        };
        global.Base64_Zip.extendString = function () {
            Object.defineProperty(String.prototype, "fromBase64", noEnum(function () {
                return decode(this)
            }));
            Object.defineProperty(String.prototype, "toBase64", noEnum(function (urisafe) {
                return encode(this, urisafe)
            }));
            Object.defineProperty(String.prototype, "toBase64URI", noEnum(function () {
                return encode(this, true)
            }))
        }
    }
})(this);

(function ($) {
    var GetList = function (element, option) {
        this.element = element;
        this.setting = {width: 600, height: 35};
        this.setting = $.extend({}, this.setting, option)
    };
    var guidCreate = function (type, index, pagesize) {
        $("#diverror").html("");
        $("#txtValidateCode").val("");
        $("#txthidtype").val(type);
        $("#txthidpage").val(index);
        $("#txthidpagesize").val(pagesize);
        var guid = createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid();
        $("#txthidGuid").val(guid);
        $("#divYzmImg").html("<img alt='点击刷新验证码！' name='validateCode' id='ImgYzm' onclick='ref()'  title='点击切换验证码' src='/ValiCode/CreateCode/?guid=" + guid + "' style='cursor: pointer;'  />")
    };
    var createGuid = function () {
        return (((1 + Math.random()) * 65536) | 0).toString(16).substring(1)
    };
    GetList.prototype = {
        Init: function () {
            $("#hidOrder").attr("order", "法院层级");
            $("#hidOrder").attr("direction", "asc")
        }, SortObj: null, SortCase: function (yzm, guid) {
            if (this.SortObj != null) {
                this.SortObj.BuildList(this.SortObj, 1, 5, 1, yzm, guid);
                $("#dialog").hide();
                $("#txtValidateCode").val("");
                this.SortObj = null
            }
        }, BuildHead: function () {
            var s = this;
            var $this = $(this.element);
            var param = $(this.setting.param);
            var datalist = "";
            var list_top = $("#sort");
            list_top.html("");
            var $list_operate = $("#operate");
            $list_operate.html("");
            var orderlist = [{key: "法院层级", value: "法院层级"}, {
                key: "裁判日期",
                value: "裁判日期"
            }, {key: "审判程序", value: "审判程序"}];
            for (var i = 0; i < orderlist.length; i++) {
                var key = orderlist[i].key;
                var value = orderlist[i].value;
                var $divSort;
                if (i == 0) {
                    $divSort = $("<div class=\"buttonclick\" key='desc'>" + value + '<div class="descico"></div></div>')
                } else {
                    $divSort = $("<div class=\"button\" key='desc'>" + value + '<div class="descico"></div></div>')
                }
                var _this = this;
                $divSort.click(function () {
                    var direction = "asc";
                    if ($(this).text() == "法院层级") {
                        if ($(this).attr("key") == "asc") {
                            $(this).find("div:first").attr("class", "descico");
                            $(this).attr("key", "desc");
                            direction = "asc"
                        } else {
                            $(this).find("div:first").attr("class", "ascico");
                            $(this).attr("key", "asc");
                            direction = "desc"
                        }
                    } else {
                        if ($(this).attr("key") == "asc") {
                            $(this).find("div:first").attr("class", "descico");
                            $(this).attr("key", "desc")
                        } else {
                            $(this).find("div:first").attr("class", "ascico");
                            $(this).attr("key", "asc")
                        }
                        direction = $(this).attr("key")
                    }
                    $(this).parent().find("div[class='buttonclick']").attr("class", "button");
                    $(this).attr("class", "buttonclick");
                    $(this).siblings().find(".ascico").attr("class", "descico");
                    $(this).siblings().attr("key", "desc");
                    var order = $(this).text();
                    $("#hidOrder").attr("order", order);
                    $("#hidOrder").attr("direction", direction);
                    _this.SortObj = s;
                    guidCreate(7);
                    var valiguid = $("#txthidGuid").val();
                    $.ajax({
                        url: "/ValiCode/GetCode",
                        type: "POST",
                        async: true,
                        data: {"guid": valiguid},
                        success: function (data) {
                            s.BuildList(s, 1, 5, 1, data, valiguid)
                        }
                    })
                });
                list_top.append($divSort)
            }
            var $divListDownLoad = $("<div class='list-operate'><span>批量下载</span></div>");
            $divListDownLoad.click(function () {
                downDocList()
            });
            var $divListCollect = $("<div class='list-operate' id='listplsc'><span>批量收藏</span></div>");
            $divListCollect.click(function () {
                collectDocList()
            });
            var $ckList = $("<input class='listck' type='checkbox' id='ckall' name='ckall'/>");
            $ckList.click(function () {
                var ckState = $("#ckall").prop("checked");
                $("input[name='ckList']").prop("checked", ckState)
            });
            $list_operate.append($ckList);
            $list_operate.append($divListCollect);
            $list_operate.append($divListDownLoad);
            var $divListDataCount = $("<div class=\"list_datacount\">共找到<span id='span_datacount' style='color:red;'>0</span>个结果，显示前200条。<div class=\"downloadico\"></div></div>");
            list_top.append($divListDataCount)
        }, DateTimeFormat: function (fmt, addDay, addMonth, addYear) {
            today = new Date();
            var o = {
                "M+": today.getMonth() + 1 + addMonth,
                "d+": today.getDate() + addDay,
                "h+": today.getHours(),
                "m+": today.getMinutes(),
                "s+": today.getSeconds(),
                "q+": Math.floor((today.getMonth() + 3) / 3),
                "S": today.getMilliseconds()
            };
            if (/(y+)/.test(fmt)) {
                fmt = fmt.replace(RegExp.$1, (today.getFullYear() + addYear + "").substr(4 - RegExp.$1.length))
            }
            for (var k in o) {
                if (new RegExp("(" + k + ")").test(fmt)) {
                    fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)))
                }
            }
            return fmt
        }, BuildList: function (obj, index, page, type, yzm, guid) {
            var url = window.location.href;
            var nyzm = url.indexOf("&number");
            var subyzm = url.substring(nyzm + 1);
            var n1yzm = subyzm.indexOf("&");
            var yzm1 = subyzm.substr(7, 4);
            var nyzm = url.indexOf("&guid");
            var subguid = url.substring(nyzm + 1);
            var n1guid = subguid.indexOf("&");
            var guid1 = subguid.substr(5, 35);
            if (yzm != undefined && yzm != "undefined") {
                yzm1 = yzm
            }
            if (guid != undefined && guid != "undefined") {
                guid1 = guid
            }
            var s = this;
            var $this = $(this.element);
            var param = $(this.setting.param);
            var datalist = "";
            var list_center = $("#resultList");
            list_center.html("<div style='height:25px;line-height:25px;vertical-align:middle;'><img src='/Assets/js/libs/icons/loading.gif'/><span>正在加载，请稍候...</span></div>");
            var listparam = "";
            for (var i = 0; i < param.length; i++) {
                var parsplit = param[i].condition;
                listparam += parsplit + ","
            }
            listparam = listparam.substring(0, listparam.length - 1);
            var order = $("#hidOrder").attr("order");
            if (order == "审判程序") {
                order = "审判程序代码"
            }
            var direction = $("#hidOrder").attr("direction");
            var dataCount = 0;
            if (index > 25) {
                Lawyee.Tools.ShowMessage("返回的结果过多，推荐您精确检索条件后再次查询!");
                list_center.css("height", "500px");
                list_center.css("font-size", "18px");
                list_center.html("无符合条件的数据...");
                return false
            }
            var guid1 = createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid();
            var yzm1;
            $.ajax({
                url: "/List/ListContent",
                type: "POST",
                async: true,
                data: {
                    "Param": listparam,
                    "Index": index,
                    "Page": page,
                    "Order": order,
                    "Direction": direction,
                    "vl5x": getKey(),
                    "number": yzm1,
                    "guid": guid1
                },
                success: function (data) {
                    if (data == "remind") {
                        window.location.href = "/Html_Pages/VisitRemind20180914.html"
                    }
                    datalist = eval("(" + data + ")");
                    var currentDocId = "";
                    list_center.html("");
                    if (datalist != undefined && datalist != null) {
                        if (datalist.length > 1) {
                            dataCount = (datalist[0].Count != undefined ? datalist[0].Count : 0);
                            if (datalist[0].RunEval != undefined) {
                                eval(unzip(datalist[0].RunEval))
                            }
                            $("#span_datacount").text(dataCount);
                            var keyWordArr = new Array();
                            if (listparam != "") {
                                var paramArr = listparam.split(",");
                                for (var i = 0; i < paramArr.length; i++) {
                                    var keyWord = "";
                                    var paramKey = paramArr[i].split(":")[0];
                                    if (paramKey != undefined && ("关键词,全文检索,首部,事实,理由,判决结果,尾部".indexOf(paramKey) >= 0)) {
                                        keyWord = paramArr[i].split(":")[1];
                                        var reg = /\s+/g;
                                        keyWord = keyWord.replace(reg, " ");
                                        var kwarr = keyWord.split(" ");
                                        for (var m = 0; m < kwarr.length; m++) {
                                            keyWordArr.push(kwarr[m])
                                        }
                                    }
                                }
                            }
                            var caseTypeStr = "", relateFiles = "";
                            for (var i = 1; i < datalist.length; i++) {
                                var key = datalist[i].文书ID != undefined ? datalist[i].文书ID : "";
                                var caseCourt = datalist[i].法院名称 != undefined ? datalist[i].法院名称 : "";
                                var caseNumber = datalist[i].案号 != undefined ? datalist[i].案号 : "";
                                var caseTypeInt = datalist[i].案件类型 != undefined ? datalist[i].案件类型 : "";
                                caseTypeStr = caseTypeStr + caseTypeInt + ",";
                                relateFiles = (relateFiles == "" ? relateFiles : (relateFiles + "~")) + key + "|" + caseCourt + "|" + caseNumber + "|" + caseTypeInt
                            }
                            caseTypeStr = obj.GetDicValue("AJLX", caseTypeStr);
                            var caseTypeArray = caseTypeStr.split(",");
                            for (var i = 1; i < datalist.length; i++) {
                                var key = datalist[i].文书ID != undefined ? datalist[i].文书ID : "";
                                var caseNameTitle = datalist[i].案件名称 != undefined ? datalist[i].案件名称.replace(",", "，") : "";
                                currentDocId += key + ",";
                                title = caseNameTitle;
                                if (title == "") {
                                    continue
                                }
                                titleOri = caseNameTitle;
                                var caseTypeInt = datalist[i].案件类型 != undefined ? datalist[i].案件类型 : "";
                                var caseType = (caseTypeArray[i - 1] != undefined ? caseTypeArray[i - 1] : "");
                                var trialRound = datalist[i].审判程序 != undefined ? datalist[i].审判程序 : "";
                                var style = "";
                                if (trialRound == "再审审查与审判监督") {
                                    trialRound = "审监"
                                }
                                if (trialRound == "非诉执行审查") {
                                    trialRound = "非诉"
                                }
                                if (trialRound == "刑罚变更") {
                                    caseType = "";
                                    style = "width:48px;"
                                }
                                if (trialRound == "其他") {
                                    trialRound = ""
                                }
                                if (trialRound == "执行" && caseType == "执行") {
                                    trialRound = ""
                                }
                                var caseCourt = datalist[i].法院名称 != undefined ? datalist[i].法院名称 : "";
                                var caseNumber = datalist[i].案号 != undefined ? datalist[i].案号 : "";
                                var caseContent = datalist[i].DocContent != undefined ? datalist[i].DocContent : "";
                                var judgeDate = datalist[i].裁判日期 != undefined ? datalist[i].裁判日期 : "";
                                var notpublic = datalist[i].不公开理由;
                                judgeDate == "0001-01-01" ? "" : judgeDate;
                                var today = new Date();
                                var dateNow = obj.DateTimeFormat("yyyy-MM-dd", 0, 0, 0);
                                if (obj.DataCompare(judgeDate, dateNow) > 0) {
                                    judgeDate = ""
                                }
                                var titleInfo = "【裁判理由】";
                                var linkA = "/content/content?DocID=" + key;
                                var keyWords = "";
                                if (keyWordArr.length > 0) {
                                    keyWords = keyWordArr.join("|");
                                    linkA = "/content/content?DocID=" + key + "&KeyWord=" + keyWords;
                                    titleInfo = "【命中结果】";
                                    keyWord = keyWordArr[0];
                                    caseContent = obj.ToCDB(caseContent);
                                    caseContent = caseContent.replace(/&amp;#xA;/g, "");
                                    caseContent = caseContent.replace(/&amp;nbsp;/g, "");
                                    caseContent = caseContent.replace(/&amp;gt;/g, "");
                                    caseContent = caseContent.replace(/&amp;lt;/g, "");
                                    if (caseContent.indexOf(keyWord) >= 0) {
                                        var keyWordIndex = caseContent.indexOf(keyWord);
                                        var startIndex = keyWordIndex - 60;
                                        var markRedCon = "";
                                        if (startIndex <= 0) {
                                            markRedCon = markRedCon + caseContent.substr(0, keyWordIndex) + keyWord;
                                            markRedCon = markRedCon + caseContent.substr(keyWordIndex + keyWord.length, 130 - keyWordIndex)
                                        } else {
                                            markRedCon = markRedCon + caseContent.substr(keyWordIndex - 60, 60) + keyWord;
                                            markRedCon = markRedCon + caseContent.substr(keyWordIndex + keyWord.length, 60)
                                        }
                                        caseContent = "..." + markRedCon + "..."
                                    } else {
                                        caseContent = caseContent.substr(0, 130)
                                    }
                                    title = obj.KeyWordsMarkRed(title, keyWordArr);
                                    caseContent = obj.KeyWordsMarkRed(caseContent, keyWordArr)
                                } else {
                                    if (notpublic == "" || notpublic == undefined) {
                                        var cpyz = datalist[i].裁判要旨段原文 != undefined ? datalist[i].裁判要旨段原文 : "";
                                        caseContent = cpyz;
                                        caseContent = obj.ToCDB(caseContent);
                                        caseContent = caseContent.substr(0, 130) + "..."
                                    } else {
                                        titleInfo = "【不公开理由】";
                                        caseContent = datalist[i].不公开理由
                                    }
                                }
                                var listitemid = "dataItem" + i;
                                if (caseContent == "" || caseContent == "...") {
                                    titleInfo = "";
                                    caseContent = ""
                                }
                                var li = $('<div class="dataItem" id="' + listitemid + '" key="' + key + '" title="' + titleOri + '" caseCourt="' + caseCourt + '" caseNumber="' + caseNumber + '" judgeDate="' + judgeDate + '">' + '<div class="label">' + (caseType != "" ? ('<div class="ajlx_lable">' + caseType + "</div>") : "") + (trialRound != "" ? ('<div class="ajlx_lable" style="' + style + '">' + trialRound + "</div>") : "") + "</div>" + "<table>" + "<tr>" + "<td colspan='2'>" + '<div class="wstitle">' + '<input type="hidden" class="DocIds" value="' + key + "|" + titleOri + "|" + judgeDate + '" >' + "<input class='listck' type='checkbox' name='ckList' downloadValue=\"" + key + "|" + titleOri + "|" + judgeDate + '"  value="' + key + "^" + title + "^" + caseCourt + "^" + caseNumber + "^" + judgeDate + '"/>&nbsp;' + "<a href='javascript:void(0)' onclick='javascript:Navi(\"" + key + '","' + keyWords + "\")' target='_self' style='color:Black; text-decoration:none'>" + title + "</a>" + "</div>" + "</td>" + "</tr>" + "<tr>" + "<td colspan='2'>" + '<div class="fymc">' + caseCourt + (caseNumber == "无" ? "" : ("&nbsp;&nbsp;&nbsp;&nbsp;" + caseNumber)) + "&nbsp;&nbsp;&nbsp;&nbsp;" + judgeDate + "</div>" + "</td>" + "</tr>" + "<tr>" + "<td colspan='2'>" + '<div class="mzjg">' + titleInfo + "</div>" + "</td>" + "</tr>" + "<tr>" + "<td class=\"wszy\" colspan='2'>" + caseContent + "</td>" + "</tr>" + "<tr>" + "<td class=\"\" colspan='2'>" + "<div id='ListItem" + (i - 1) + "'></div>" + "</td>" + "</tr>" + "</table>" + '<div class="scxz">' + '<div class="download">' + "<img style=\"cursor:pointer; margin-bottom:5px;\" title='通过中国司法案例网身份认证的会员（主要包括法官、律师、法律学者、法律院校学生）才能推荐裁判文书到中国司法案例网，经全体会员众筹投票，符合条件可收入最高人民法院司法案例库' onclick=\"Casefx('" + key + '\');" src="/Assets/img/list/wytal-hove.png" alt="通过中国司法案例网身份认证的会员（主要包括法官、律师、法律学者、法律院校学生）才能推荐裁判文书到中国司法案例网，经全体会员众筹投票，符合条件可收入最高人民法院司法案例库"/>' + "</div>" + '<div class="download">' + "<img style=\"cursor:pointer;\" title='下载' onclick=\"DownLoadCaseNew('" + listitemid + '\');" src="/Assets/img/list/list_download.png" alt="下载"/>' + "</div>" + '<div class="collect">' + "<img style=\"cursor:pointer;\" title='收藏'  onclick=\"CollectCaseNew('" + listitemid + '\');" src="/Assets/img/list/list_collect.png"  alt="收藏"/>' + "</div>" + "</div>" + "</div>");
                                list_center.append(li)
                            }
                        } else {
                            list_center.css("height", "500px");
                            list_center.css("font-size", "18px");
                            list_center.html("无符合条件的数据...")
                        }
                        list_center.render();
                        try {
                            var getGs = $("#hidConditions").val();
                            toGridsum.SearchList(getGs)
                        } catch (e) {
                        }
                        if (currentDocId != "") {
                            currentDocId = currentDocId.substring(0, currentDocId.lastIndexOf(","))
                        }
                        rfDataList = obj.GetRelateFiles(obj, relateFiles, currentDocId)
                    } else {
                        list_center.css("height", "500px");
                        list_center.css("font-size", "18px");
                        list_center.html("无符合条件的数据...")
                    }
                    if (type == 1) {
                        obj.BuildBottom(obj, dataCount)
                    }
                }
            })
        }, PageObj: null, BuildBottom: function (obj, dataCount) {
            var list_bottom = $("#docbottom");
            list_bottom.html("");
            var $pager = $('<div style="margin-top:20px;" id="pageNumber" class="pageNumber" total="' + dataCount + '"  pageSize="10" showSelect="false" selectDirection="bottom" centerPageNum="10" edgePageNum="0" page="0"  prevText="上一页" nextText="下一页" selectData=\'{"list":[{"key":5,"value":5},{"key":10,"value":10},{"key":15,"value":15},{"key":20,"value":20}]}\'></div>');
            $pager.attr("total", dataCount);
            list_bottom.append($pager);
            $pager.render();
            var _this = this;
            $pager.bind("pageChange", function (e, index) {
                var pageSize = $(this).attr("pageSize");
                _this.PageObj = {pageSize: pageSize, obj: obj, index: index};
                guidCreate(3, index, pageSize);
                var valiguid = $("#txthidGuid").val();
                $.ajax({
                    url: "/ValiCode/GetCode",
                    type: "POST",
                    async: true,
                    data: {"guid": valiguid},
                    success: function (data) {
                        var type = $("#txthidtype").val();
                        $("#txtValidateCode").val(data);
                        if (type == 3) {
                            var index = $("#txthidpage").val();
                            var pagesize = $("#txthidpagesize").val();
                            var url = window.location.href;
                            listObj.PageChange()
                        } else {
                            if (type == 4) {
                                var tree = $("#txthidtree").val();
                                var treekey = $("#txthidtreekey").val();
                                var url = window.location.href;
                                url = decodeURI(url);
                                var params = new Array();
                                var parameter = {
                                    type: "searchWord",
                                    value: treekey,
                                    sign: "",
                                    pid: "",
                                    condition: tree + ":" + treekey
                                };
                                params.push(parameter);
                                Param("treesearch", params, $("#txtValidateCode").val(), valiguid)
                            } else {
                                if (type == 5) {
                                    listUIKey.CheckSearch($("#txtValidateCode").val(), valiguid)
                                } else {
                                    if (type == 6) {
                                        listUIKey.removeContent($("#txtValidateCode").val(), valiguid)
                                    } else {
                                        if (type == 7) {
                                            listObj.SortCase($("#txtValidateCode").val(), valiguid)
                                        } else {
                                            s.Search(type, $("#txtValidateCode").val(), valiguid)
                                        }
                                    }
                                }
                            }
                        }
                    }
                })
            });
            $pager.bind("sizeChange", function (e, num) {
                _this.PageObj = {pageSize: num, obj: obj, index: 1};
                guidCreate(3, 1, num);
                var valiguid = $("#txthidGuid").val();
                $.ajax({
                    url: "/ValiCode/GetCode",
                    type: "POST",
                    async: true,
                    data: {"guid": valiguid},
                    success: function (data) {
                        obj.BuildList(obj, 1, num, 0, data, valiguid)
                    }
                })
            })
        }, PageChange: function (data) {
            if (this.PageObj != null) {
                var guid = $("#txthidGuid").val();
                var yzm = $("#txtValidateCode").val();
                this.PageObj.obj.BuildList(this.PageObj.obj, this.PageObj.index + 1, this.PageObj.pageSize, 0, yzm, guid);
                $("#dialog").hide();
                $("#txtValidateCode").val("");
                this.PageObj = null;
                $("html,body").animate({scrollTop: 0}, "fast")
            }
        }, GetRelateFiles: function (obj, caseInfoAll, currentDocId) {
            var dataList;
            var htmlStr = "";
            $.ajax({
                url: "/List/GetAllRelateFiles",
                type: "POST",
                async: true,
                data: {"caseInfoAll": caseInfoAll},
                success: function (data) {
                    try {
                        dataList = $.parseJSON(data)
                    } catch (error) {
                        dataList = ""
                    }
                    var relateFilesArray = obj.BuildRFHtml(obj, dataList, currentDocId);
                    for (var rfi = 0; rfi < relateFilesArray.length; rfi++) {
                        $("#ListItem" + rfi).html(relateFilesArray[rfi]);
                        if (htmlStr != "" && relateFilesArray[rfi] != "<table></table>") {
                            $("#ListItem" + rfi).prepend(htmlStr)
                        }
                    }
                }
            })
        }, BuildRFHtml: function (obj, dataList, currentDocId) {
            var relateFilesArray = [];
            var arry_arrentId = currentDocId.split(",");
            if (dataList != undefined && dataList.RelateFiles != undefined && dataList.RelateFiles.length > 0) {
                for (var i = 0; i < dataList.RelateFiles.length; i++) {
                    var html = "<table>";
                    var relateFile = dataList.RelateFiles[i].RelateFile;
                    if ($.isArray(relateFile)) {
                        if (relateFile.length > 0) {
                            var fileType = "0";
                            var img = "";
                            var relateId = "";
                            for (var ii = 0; ii < relateFile.length; ii++) {
                                var fileTypeii = relateFile[ii].Type;
                                var judgeTime = relateFile[ii].裁判日期 == "0001-01-01" ? "" : relateFile[ii].裁判日期;
                                var title = "【关联文书】";
                                if (arry_arrentId[i] == relateFile[ii].文书ID) {
                                    if (ii == 0) {
                                        img += '<img src="/Assets/img/list/bp_18.png" style="padding-left:2px;"/><img style="padding-bottom: 5px;" src="/Assets/img/list/dot_10.png"/>'
                                    } else {
                                        if (ii == relateFile.length - 1 && relateFile.length == 2) {
                                            img += '<img style="padding-left:2px;" src="/Assets/img/list/bp_18.png"/><img style="margin-bottom: 10px;margin-right: 5px;" src="/Assets/img/list/dot_04.png"/>'
                                        } else {
                                            if (ii < relateFile.length - 1) {
                                                img += '<img style="margin-bottom:10px;" src="/Assets/img/list/bp_18.png"/><img src="/Assets/img/list/dotLine_03.png"/>'
                                            } else {
                                                img += '<img src="/Assets/img/list/bp_18.png" style="padding-left:2px;" /><img style="padding-right: 4px;padding-bottom: 11px;" src="/Assets/img/list/dot_07.png"/>'
                                            }
                                        }
                                    }
                                } else {
                                    if (ii == 0) {
                                        img += '<img style="padding-bottom: 5px;margin-left:10px;margin-top: 10px;" src="/Assets/img/list/dot_10.png"/>'
                                    } else {
                                        if (ii < relateFile.length - 1) {
                                            img += '<img style="margin-left:45px" src="/Assets/img/list/dotLine_03.png"/>'
                                        } else {
                                            if (ii == relateFile.length - 1 && relateFile.length == 2) {
                                                img += '<img style="margin-left:48px;margin-right: 5px;" src="/Assets/img/list/dot_04.png"/>'
                                            } else {
                                                img += '<img style="padding-right: 4px;padding-top: 8px;" src="/Assets/img/list/dot_07.png"/>'
                                            }
                                        }
                                    }
                                }
                            }
                            for (var ii = 0; ii < relateFile.length; ii++) {
                                var fileTypeii = relateFile[ii].Type;
                                var judgeTime = relateFile[ii].裁判日期 == "0001-01-01" ? "" : relateFile[ii].裁判日期;
                                var title = "【关联文书】";
                                if (ii > 0) {
                                    title = ""
                                }
                                var colStr = 0;
                                if (relateFile.length == 2) {
                                    colStr = relateFile.length + 1
                                } else {
                                    colStr = relateFile.length * 2
                                }
                                html += "<tr>";
                                html += "<td class='list-glws-title' colspan=\"2\">";
                                html += '<lable title="关联文书仅以本网收录的裁判文书为依据，如果对此结果有疑义，请联系作出裁判文书的人民法院。">' + title + "</lable>";
                                html += "</td>";
                                html += "</tr>";
                                html += "<tr>";
                                if (ii == 0) {
                                    html += "<td  rowspan=" + colStr + ' style="text-align: right;width: 70px;"><div style="width: 70px;float: right; margin-bottom: 10px;">' + img + "</div></td>"
                                }
                                if (arry_arrentId[i] == relateFile[ii].文书ID) {
                                    html += "<td class='list-glws'>";
                                    html += "&nbsp;" + relateFile[ii].Mark + "";
                                    html += "&nbsp;" + relateFile[ii].审理法院 + "";
                                    html += "&nbsp;<a  title='本篇文书' target='_blank' >" + relateFile[ii].案号 + "</a>";
                                    html += "&nbsp;" + judgeTime + "";
                                    html += "&nbsp;" + relateFile[ii].结案方式 + "";
                                    html += "</td>"
                                } else {
                                    html += "<td class='list-glws'>";
                                    html += "&nbsp;" + relateFile[ii].Mark + "";
                                    html += "&nbsp;" + relateFile[ii].审理法院 + "";
                                    html += "&nbsp;<a style='text-decoration:underline;' title='点击查看全文' target='_blank' href=\"/Content/Content?DocID=" + relateFile[ii].文书ID + '">' + relateFile[ii].案号 + "</a>";
                                    html += "&nbsp;" + judgeTime + "";
                                    html += "&nbsp;" + relateFile[ii].结案方式 + "";
                                    html += "</td>"
                                }
                                html += "</tr>";
                                if (ii == 0) {
                                    if (relateFile[ii + 1] != undefined) {
                                        var fileTypeNext = relateFile[ii + 1].Type;
                                        if (fileTypeNext !== fileTypeii) {
                                        }
                                    }
                                }
                                if (ii == relateFile.length - 1 && fileTypeii != fileType) {
                                    html += "<tr>";
                                    html += '<td class="list-glws_dot"></td>';
                                    html += "<td class='list-glws'>";
                                    html += "<div style='margin-left:7px;height:1px;border-bottom:1px dashed #666666;'></div>";
                                    html += "</td>";
                                    html += "</tr>";
                                    fileType = fileTypeii
                                }
                            }
                        }
                    }
                    html += "</table>";
                    relateFilesArray.push(html)
                }
            }
            return relateFilesArray
        }, ToCDB: function (str) {
            var tmp = "";
            for (var i = 0; i < str.length; i++) {
                if (str.charCodeAt(i) > 65248 && str.charCodeAt(i) < 65375) {
                    tmp += String.fromCharCode(str.charCodeAt(i) - 65248)
                } else {
                    tmp += String.fromCharCode(str.charCodeAt(i))
                }
            }
            return tmp
        }, DataCompare: function (a, b) {
            var arr = a.split("-");
            var starttime = new Date(arr[0], arr[1], arr[2]);
            var starttimes = starttime.getTime();
            var arrs = b.split("-");
            var lktime = new Date(arrs[0], arrs[1], arrs[2]);
            var lktimes = lktime.getTime();
            if (starttimes >= lktimes) {
                return 1
            } else {
                return 0
            }
        }, GetDicValue: function (dicId, dicKey) {
            var dicValue = "";
            $.ajax({
                url: "/List/GetDicValue",
                type: "POST",
                async: false,
                data: {"dicId": dicId, "dicKey": dicKey},
                success: function (data) {
                    dicValue = data
                }
            });
            return dicValue
        }, KeyWordsMarkRed: function (content, keyWordArr) {
            for (var keyi = 0; keyi < keyWordArr.length; keyi++) {
                if (content.indexOf(keyWordArr[keyi]) >= 0) {
                    eval("content = content.replace(/" + keyWordArr[keyi] + "/g, \"<span style='color:red'>" + keyWordArr[keyi] + '</span>")')
                }
            }
            return content
        }
    };
    $.fn.UIList = function (option) {
        var List = new GetList(this, option);
        List.Init();
        List.BuildHead();
        List.BuildList(List, 1, 10, 1);
        return List
    }
})(jQuery);
function collectDocList() {
    var getListDocIds = $("input[name='ckList']:checked");
    if (getListDocIds.length > 0) {
        var DocIds = new Array();
        var realid = "";
        getListDocIds.each(function () {
            var $dataitem = $(this).parents(".dataItem");
            var id = $dataitem.attr("key");
            var unzipid = unzip(id);
            try {
                realid = com.str.Decrypt(unzipid);
                if (realid == "") {
                    setTimeout("collectDocList()", 1000);
                    return
                } else {
                    DocIds.push(realid + "^" + $dataitem.attr("title") + "^" + $dataitem.attr("caseCourt") + "^" + $dataitem.attr("caseNumber") + "^" + $dataitem.attr("judgeDate"))
                }
            } catch (ex) {
                setTimeout("collectDocList()", 1000);
                return
            }
        })
    } else {
        Lawyee.Tools.ShowMessage("请选择需要收藏的文书!")
    }
    if (DocIds.length == 0) {
        return
    }
    $.ajax({
        url: "/Content/CheckLogin",
        type: "POST",
        async: false,
        data: {},
        success: function (res) {
            if (res == "0") {
                SaveUrl();
                window.location = "/User/RegisterAndLogin?Operate=1"
            } else {
                var ckChecked = $("input[name='ckList']:checked");
                var caseInfo = "";
                if (DocIds.length > 0) {
                    caseInfo = DocIds.join("&");
                    $("#hidCaseInfo").val(caseInfo);
                    top.Dialog.confirm("是否收藏到新的案例包中？|提示|是否", function () {
                        var $conditions = $(".removeCondtion");
                        var conditions = "";
                        $conditions.each(function () {
                            conditions += $(this).attr("val") + "&"
                        });
                        conditions = conditions.substr(0, conditions.length - 1);
                        if (conditions.split("&").length >= 2) {
                            var conArry = conditions.split("&");
                            conditions = conArry[0] + conArry[1]
                        }
                        conditions = conditions.replace(/:/g, "为").replace(/&/g, "且");
                        var dates = new Date();
                        var _years = dates.getFullYear();
                        var _months = dates.getMonth() + 1;
                        var _days = dates.getDay();
                        var _hours = dates.getHours();
                        var _minutes = dates.getMinutes();
                        var _seconds = dates.getSeconds();
                        var _mill = dates.getMilliseconds();
                        var nowTimes = _years + "" + _months + "" + _days + "" + _hours + "" + _minutes + "" + _seconds + "" + _mill;
                        AddPackage(conditions + nowTimes)
                    }, function () {
                        List.Package.BindPackageList();
                        $("#divCasePackage").show()
                    })
                }
            }
        }
    })
}
function downDocList() {
    var getListDocIds = $("input[name='ckList']:checked");
    if (getListDocIds.length > 0) {
        var DownloadDocIds = new Array();
        var realid = "";
        getListDocIds.each(function () {
            var $dataitem = $(this).parents(".dataItem");
            var id = $dataitem.attr("key");
            var unzipid = unzip(id);
            try {
                realid = com.str.Decrypt(unzipid);
                if (realid == "") {
                    setTimeout("downDocList()", 1000);
                    return
                } else {
                    DownloadDocIds.push(realid + "|" + $dataitem.attr("title") + "|" + $dataitem.attr("judgeDate"))
                }
            } catch (ex) {
                setTimeout("downDocList()", 1000);
                return
            }
        })
    } else {
        Lawyee.Tools.ShowMessage("请选择需要下载的文书!")
    }
    if (DownloadDocIds.length == 0) {
        return
    }
    if (getListDocIds.length > 0) {
        var thebody = document.body;
        var formid = "DownloadForm";
        var url = "/CreateContentJS/CreateListDocZip.aspx?action=1";
        var theform = document.createElement("form");
        theform.id = formid;
        theform.action = url;
        theform.method = "POST";
        var $conditions = $(".removeCondtion");
        var conditions = "";
        $conditions.each(function () {
            conditions += $(this).attr("val") + "&"
        });
        conditions = conditions.substr(0, conditions.length - 1);
        conditions = conditions.replace(/:/g, "为").replace(/&/g, "且");
        var theInput = document.createElement("input");
        theInput.type = "hidden";
        theInput.id = "conditions";
        theInput.name = "conditions";
        theInput.value = encodeURI(conditions);
        theform.appendChild(theInput);
        var theInput = document.createElement("input");
        theInput.type = "hidden";
        theInput.id = "docIds";
        theInput.name = "docIds";
        theInput.value = DownloadDocIds.toString();
        theform.appendChild(theInput);
        var theInput = document.createElement("input");
        theInput.type = "hidden";
        theInput.id = "keyCode";
        theInput.name = "keyCode";
        theInput.value = "";
        theform.appendChild(theInput);
        thebody.appendChild(theform);
        theform.submit()
    }
}
function Navi(id, keyword) {
    var eval_s = unzip('w61ZQW7CgzAQfAtRDsK2wqjDugHClFPCnsOQw6PDikIRSRsODcKVQ09Rw75eIMKIwoLCocKYFMK8wqVhJMK0EcO2end2Zm1hZX3CjMO3wodzwqTDo8KPdMOzwpLDqsO4w7TDtsO8wqrCk8O3w61xwqfCt8OJw74gfMOPJwUza8OzBBJgwpbDkSHCj1DDiELCtitOJWgLA8Oew4EsDMOUA2MQF8OswqBqw5ABEsOACcOqBzFgAjzCoTgUwozCksKgAAwaYcK+RgZBwrhZRcOJw6nCnMOqw48oTcO0KggpVMOZI8KEf8K5w6Zuw5VzwrlKwrrCrcKkw4wow6ULwq/CmMKQw5TCjMKZT8OYZ8KKw5fDtcO3X8O0JMOyw6HDjMKDwrx8woYUZT9Gw4LCpsK7Vy7DuDnCmcKBwrvDk8K3F1M9WsO3eMKVwqpAw53CpsKoBcKhwrPChsKew5gVw4hhwozDll7CrcKwB3rDnMOjdsK3w6/DrxbCjFg1dmnCu8K3JsKLasOdPRPChDfDm8Kpwr97DcKvw7IkwrjDrUwHwrjDrMOHwod9wpvCucKCZUEwfS5nRXBFd8OUHGxdw6hOacO2NsO6w7fCusKzw6Z5bHlYw4R3QyDClwDDtmTCrEjDuGTDoy4KacK5w5LDvnnDrhLCgDDCrifCgy5fc2PCqcOjwprDlcKqwosawp8pw53Co8O1woA0w6LCojgPw54WDUVJIcKDLw==')
    //alert(eval_s)
    eval(eval_s)
    var unzipid = unzip(id);
    //alert(unzipid)
    //var realid = com.str.Decrypt(unzipid);
    //return realid
    try {
        var realid = com.str.Decrypt(unzipid);
        //var realid = '8252121f-8260-4241-b707-018d52d151ca'
        //alert('end')
        //alert(realid)
        if (realid == "") {
            setTimeout("Navi('" + id + "','" + keyword + "')", 1000)
        } else {
            var url = "/content/content?DocID=" + realid + "&KeyWord=" + encodeURI(keyword);
            openWin(url)
        }
    } catch (ex) {
        setTimeout("Navi('" + id + "','" + keyword + "')", 1000)
    }
}
function openWin(url) {
    $("body").append($('<a href="' + url + '" target="_blank" id="openWin"></a>'));
    document.getElementById("openWin").click();
    $("#openWin").remove()
}