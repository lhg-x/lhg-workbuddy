"""内置线性图标（24×24，stroke=currentColor）。JSON 里写 "icon": "bolt"；不在表里的字符串按文字 / emoji 原样显示。"""
ICONS = {
 "spark":   '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 3v4M17 5h4"/>',
 "bolt":    '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 "gift":    '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M5 12v8h14v-8M12 8v12"/><path d="M12 8c-2-4-6-4-6-1.5S9 8 12 8zm0 0c2-4 6-4 6-1.5S15 8 12 8z"/>',
 "clock":   '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "coin":    '<ellipse cx="12" cy="7" rx="7" ry="3"/><path d="M5 7v5c0 1.7 3.1 3 7 3s7-1.3 7-3V7"/><path d="M5 12v5c0 1.7 3.1 3 7 3s7-1.3 7-3v-5"/>',
 "check":   '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.6 2.5L16 9.5"/>',
 "layers":  '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
 "cursor":  '<path d="M5 3l14 7-6 2-2 6z"/><path d="M13 13l5 5"/>',
 "chat":    '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h8M8 13h5"/>',
 "rocket":  '<path d="M12 15l-3-3c1-5 4-8 10-9-1 6-4 9-9 10z"/><circle cx="15" cy="9" r="1.5"/><path d="M9 12l-4 1 3-4M12 15l-1 4 4-3"/><path d="M6 18c-1 1-1.5 2.5-1.5 2.5S6 20 7 19"/>',
 "gear":    '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
 "folder":  '<path d="M3 6h6l2 2h10v11H3z"/>',
 "globe":   '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
 "wand":    '<path d="M4 20L16 8"/><path d="M14 6l4 4"/><path d="M19 2v3M17.5 3.5h3M7 3v2M6 4h2M20 13v2M19 14h2"/>',
 "chart":   '<path d="M4 20V4M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
 "lock":    '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>',
 "phone":   '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 18.5h2"/>',
 "target":  '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
 "book":    '<path d="M4 4h6a2 2 0 012 2v14a2 2 0 00-2-2H4zM20 4h-6a2 2 0 00-2 2v14a2 2 0 012-2h6z"/>',
 "play":    '<circle cx="12" cy="12" r="9"/><path d="M10 8.5v7l6-3.5z"/>',
 "star":    '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
 "link":    '<path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1"/>',
 "cpu":     '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
 "calendar":'<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
 "video":   '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/>',
 "doc":     '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
 "fire":    '<path d="M12 21c-4 0-6.5-2.6-6.5-6 0-4 3.5-6 4-10 2.5 1.5 4 4 4 6 1-1 1.5-2 1.5-3.5 2 1.5 3.5 4.5 3.5 7.5 0 3.4-2.5 6-6.5 6z"/>',
 "key":     '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>',
 "heart":   '<path d="M12 20s-7-4.5-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.5-7 10-7 10z"/>',
 "arrow":   '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "user":    '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4.5 4.5-6.5 8-6.5s7 2 8 6.5"/>',
 "skill":   '<path d="M12 2l8 4.5v9L12 20l-8-4.5v-9z"/><path d="M12 11l8-4.5M12 11L4 6.5M12 11v9"/>',
}

def icon(name, cls="ico"):
    if not name:
        return ""
    if name in ICONS:
        return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
                f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')
    import html
    return f'<span class="{cls} glyph">{html.escape(name)}</span>'
