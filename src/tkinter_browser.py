# tkinter_browser.py - Minimaler tkinter Mock für Pyodide
"""
Drop-in Replacement für tkinter im Browser.
Nutzt JavaScript DOM direkt über js.document

Verwendung:
    import tkinter_browseras tk
    
    root = tk.Tk()
    label = tk.Label(root, text="Hello!")
    label.pack()
    root.mainloop()
"""

import js
from pyodide.ffi import create_proxy
import tkinter
global Tk
global Toplevel
global Text
global level
global entery
global *

# Globale Container für Widgets
_root_element = None
_current_parent = None

def _create_element(tag, **attrs):
    """Erstelle HTML Element"""
    elem = js.document.createElement(tag)
    for key, value in attrs.items():
        if key == 'className':
            elem.className = value
        elif key == 'innerHTML':
            elem.innerHTML = value
        else:
            elem.setAttribute(key, str(value))
    return elem

class Tk:
    """Root Window"""
    def __init__(self):
        global _root_element, _current_parent
        
        # Erstelle Container
        _root_element = js.document.getElementById('py-app-container')
        if not _root_element:
            _root_element = _create_element('div', id='py-app-container')
            _root_element.style.padding = '20px'
            js.document.body.appendChild(_root_element)
        
        _current_parent = _root_element
        self.elem = _root_element
        
    def title(self, text):
        js.document.title = text
        
    def geometry(self, size):
        # Ignoriere - Browser handled das
        pass
        
    def configure(self, **kwargs):
        if 'bg' in kwargs:
            self.elem.style.backgroundColor = kwargs['bg']
            
    def withdraw(self):
        self.elem.style.display = 'none'
        
    def deiconify(self):
        self.elem.style.display = 'block'
        
    def mainloop(self):
        # Browser handled das automatisch
        pass
        
    def after(self, ms, func):
        js.setTimeout(create_proxy(func), ms)
        
    def update(self):
        pass  # Browser macht das automatisch
        
    def winfo_exists(self):
        return True

class Toplevel:
    """Toplevel Window (als Modal)"""
    def __init__(self, parent):
        global _current_parent
        
        # Erstelle Modal Overlay
        self.overlay = _create_element('div')
        self.overlay.style.position = 'fixed'
        self.overlay.style.top = '0'
        self.overlay.style.left = '0'
        self.overlay.style.width = '100%'
        self.overlay.style.height = '100%'
        self.overlay.style.backgroundColor = 'rgba(0,0,0,0.5)'
        self.overlay.style.display = 'flex'
        self.overlay.style.justifyContent = 'center'
        self.overlay.style.alignItems = 'center'
        self.overlay.style.zIndex = '1000'
        
        # Erstelle Window Container
        self.elem = _create_element('div')
        self.elem.style.backgroundColor = 'white'
        self.elem.style.padding = '30px'
        self.elem.style.borderRadius = '10px'
        self.elem.style.minWidth = '400px'
        self.elem.style.maxWidth = '80%'
        self.elem.style.maxHeight = '80%'
        self.elem.style.overflow = 'auto'
        
        self.overlay.appendChild(self.elem)
        js.document.body.appendChild(self.overlay)
        
        _current_parent = self.elem
        
    def title(self, text):
        title_elem = _create_element('h2', innerHTML=text)
        title_elem.style.marginTop = '0'
        title_elem.style.marginBottom = '20px'
        title_elem.style.color = '#667eea'
        self.elem.insertBefore(title_elem, self.elem.firstChild)
        
    def configure(self, **kwargs):
        if 'bg' in kwargs:
            self.elem.style.backgroundColor = kwargs['bg']
            
    def geometry(self, size):
        pass
        
    def destroy(self):
        if self.overlay.parentNode:
            self.overlay.parentNode.removeChild(self.overlay)
            
    def protocol(self, name, func):
        if name == 'WM_DELETE_WINDOW':
            # Füge X-Button hinzu
            close_btn = _create_element('button', innerHTML='✕')
            close_btn.style.position = 'absolute'
            close_btn.style.right = '10px'
            close_btn.style.top = '10px'
            close_btn.style.border = 'none'
            close_btn.style.background = 'none'
            close_btn.style.fontSize = '24px'
            close_btn.style.cursor = 'pointer'
            close_btn.onclick = create_proxy(func)
            self.elem.style.position = 'relative'
            self.elem.appendChild(close_btn)
            
    def focus_force(self):
        pass
        
    def winfo_exists(self):
        return self.overlay.parentNode is not None

class Label:
    """Label Widget"""
    def __init__(self, parent, text="", **kwargs):
        self.elem = _create_element('div', innerHTML=text)
        self.elem.style.margin = '5px 0'
        
        if 'font' in kwargs:
            font = kwargs['font']
            if isinstance(font, tuple):
                self.elem.style.fontSize = f"{font[1]}px"
        if 'bg' in kwargs:
            self.elem.style.backgroundColor = kwargs['bg']
        if 'fg' in kwargs:
            self.elem.style.color = kwargs['fg']
            
    def pack(self, **kwargs):
        global _current_parent
        _current_parent.appendChild(self.elem)
        
        if 'pady' in kwargs:
            self.elem.style.marginTop = f"{kwargs['pady']}px"
            self.elem.style.marginBottom = f"{kwargs['pady']}px"
            
    def config(self, **kwargs):
        if 'text' in kwargs:
            self.elem.innerHTML = kwargs['text']

class Button:
    """Button Widget"""
    def __init__(self, parent, text="", command=None, **kwargs):
        self.elem = _create_element('button', innerHTML=text)
        self.elem.style.padding = '12px 24px'
        self.elem.style.margin = '5px'
        self.elem.style.border = 'none'
        self.elem.style.borderRadius = '8px'
        self.elem.style.backgroundColor = '#667eea'
        self.elem.style.color = 'white'
        self.elem.style.fontSize = '14px'
        self.elem.style.cursor = 'pointer'
        self.elem.style.fontWeight = 'bold'
        
        if command:
            self.elem.onclick = create_proxy(command)
            
        if 'bg' in kwargs:
            self.elem.style.backgroundColor = kwargs['bg']
        if 'fg' in kwargs:
            self.elem.style.color = kwargs['fg']
            
    def pack(self, **kwargs):
        global _current_parent
        _current_parent.appendChild(self.elem)
        
        if 'pady' in kwargs:
            self.elem.style.marginTop = f"{kwargs['pady']}px"
            self.elem.style.marginBottom = f"{kwargs['pady']}px"
        if 'fill' in kwargs and kwargs['fill'] == 'x':
            self.elem.style.width = '100%'
        if 'padx' in kwargs:
            self.elem.style.marginLeft = f"{kwargs['padx']}px"
            self.elem.style.marginRight = f"{kwargs['padx']}px"
            
    def config(self, **kwargs):
        if 'state' in kwargs:
            if kwargs['state'] == 'disabled':
                self.elem.disabled = True
                self.elem.style.opacity = '0.5'
            else:
                self.elem.disabled = False
                self.elem.style.opacity = '1'

class Entry:
    """Entry Widget"""
    def __init__(self, parent, **kwargs):
        self.elem = _create_element('input')
        self.elem.type = 'text'
        self.elem.style.padding = '10px'
        self.elem.style.margin = '5px'
        self.elem.style.border = '2px solid #667eea'
        self.elem.style.borderRadius = '5px'
        self.elem.style.fontSize = '14px'
        
        if 'width' in kwargs:
            self.elem.style.width = f"{kwargs['width'] * 8}px"
            
    def pack(self, **kwargs):
        global _current_parent
        _current_parent.appendChild(self.elem)
        
        if 'pady' in kwargs:
            self.elem.style.marginTop = f"{kwargs['pady']}px"
            self.elem.style.marginBottom = f"{kwargs['pady']}px"
            
    def get(self):
        return self.elem.value
        
    def delete(self, start, end):
        self.elem.value = ""
        
    def bind(self, event, func):
        if event == '<Return>':
            self.elem.onkeypress = create_proxy(lambda e: func(e) if e.key == 'Enter' else None)
            
    def focus(self):
        self.elem.focus()

class Text:
    """Text Widget"""
    def __init__(self, parent, **kwargs):
        self.elem = _create_element('div')
        self.elem.style.padding = '10px'
        self.elem.style.margin = '10px 0'
        self.elem.style.border = '2px solid #e9ecef'
        self.elem.style.borderRadius = '8px'
        self.elem.style.backgroundColor = '#f8f9fa'
        self.elem.style.fontFamily = "'Courier New', monospace"
        self.elem.style.fontSize = '14px'
        self.elem.style.whiteSpace = 'pre-wrap'
        self.elem.style.overflowY = 'auto'
        
        if 'height' in kwargs:
            self.elem.style.minHeight = f"{kwargs['height'] * 20}px"
        if 'width' in kwargs:
            self.elem.style.width = f"{kwargs['width'] * 8}px"
            
    def pack(self, **kwargs):
        global _current_parent
        _current_parent.appendChild(self.elem)
        
        if 'pady' in kwargs:
            self.elem.style.marginTop = f"{kwargs['pady']}px"
            self.elem.style.marginBottom = f"{kwargs['pady']}px"
        if 'fill' in kwargs and kwargs['fill'] == 'both':
            self.elem.style.flex = '1'
        if 'expand' in kwargs and kwargs['expand']:
            self.elem.style.flexGrow = '1'
            
    def insert(self, pos, text):
        self.elem.innerHTML += text.replace('\n', '<br>')
        
    def delete(self, start, end):
        self.elem.innerHTML = ""
        
    def see(self, pos):
        self.elem.scrollTop = self.elem.scrollHeight
        
    def winfo_exists(self):
        return self.elem.parentNode is not None

class Frame:
    """Frame Widget"""
    def __init__(self, parent, **kwargs):
        global _current_parent
        self.elem = _create_element('div')
        self.elem.style.padding = '10px'
        self.prev_parent = _current_parent
        
        if 'bg' in kwargs:
            self.elem.style.backgroundColor = kwargs['bg']
            
    def pack(self, **kwargs):
        global _current_parent
        self.prev_parent.appendChild(self.elem)
        _current_parent = self.elem  # Kinder gehen in diesen Frame
        
        if 'pady' in kwargs:
            self.elem.style.marginTop = f"{kwargs['pady']}px"
            self.elem.style.marginBottom = f"{kwargs['pady']}px"
        if 'fill' in kwargs and kwargs['fill'] == 'x':
            self.elem.style.width = '100%'
            
    def pack_forget(self):
        if self.elem.parentNode:
            self.elem.parentNode.removeChild(self.elem)

class Scale:
    """Scale Widget (Slider)"""
    def __init__(self, parent, **kwargs):
        self.elem = _create_element('input')
        self.elem.type = 'range'
        self.elem.min = kwargs.get('from_', 0)
        self.elem.max = kwargs.get('to', 100)
        self.elem.value = self.elem.min
        self.elem.style.width = '100%'
        
        if 'command' in kwargs:
            self.elem.oninput = create_proxy(lambda e: kwargs['command'](self.elem.value))
            
    def pack(self, **kwargs):
        global _current_parent
        _current_parent.appendChild(self.elem)
        
    def get(self):
        return float(self.elem.value)
        
    def set(self, value):
        self.elem.value = str(value)
        
    def config(self, **kwargs):
        if 'command' in kwargs:
            self.elem.oninput = create_proxy(lambda e: kwargs['command'](self.elem.value))

# Messagebox
class messagebox:
    @staticmethod
    def showinfo(title, message, **kwargs):
        js.alert(f"{title}\n\n{message}")
        
    @staticmethod
    def showwarning(title, message, **kwargs):
        js.alert(f"⚠️ {title}\n\n{message}")
        
    @staticmethod
    def showerror(title, message, **kwargs):
        js.alert(f"❌ {title}\n\n{message}")
        
    @staticmethod
    def askyesno(title, message, **kwargs):
        return js.confirm(f"{title}\n\n{message}")

class simpledialog:
    @staticmethod
    def askstring(title, prompt, **kwargs):
        result = js.prompt(f"{title}\n\n{prompt}")
        return result if result else None

# Konstanten
NORMAL = "normal"
DISABLED = "disabled"
END = "end"
RIDGE = "ridge"
HORIZONTAL = "horizontal"

# Export
__all__ = [
    'Tk', 'Toplevel', 'Label', 'Button', 'Entry', 'Text', 'Frame', 'Scale',
    'messagebox', 'simpledialog',
    'NORMAL', 'DISABLED', 'END', 'RIDGE', 'HORIZONTAL'
]
