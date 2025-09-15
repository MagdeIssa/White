import re
import os
import sys
import glob
from pathlib import Path

class StyleManager:
    """إدارة الأنماط والألوان"""
    def __init__(self):
        self.theme_colors = {
            'primary': '#3498db',
            'secondary': '#2980b9', 
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#2c3e50',
            'white': '#ffffff',
            'black': '#000000',
            'gray': '#6c757d',
            'blue': '#007bff',
            'green': '#28a745',
            'red': '#dc3545',
            'yellow': '#ffc107',
            'purple': '#6f42c1',
            'pink': '#e83e8c',
            'orange': '#fd7e14'
        }
        self.custom_styles = {}
        self.class_counter = 0

    def parse_style_attributes(self, content: str):
        """تحليل خصائص الأنماط من النص"""
        style_attrs = {}
        text_content = content
        
        patterns = {
            'color': r'color:([^;\s]+)',
            'size': r'size:([^;\s]+)', 
            'bg': r'bg:([^;\s]+)',
            'width': r'width:([^;\s]+)',
            'height': r'height:([^;\s]+)',
            'margin': r'margin:([^;\s]+)',
            'padding': r'padding:([^;\s]+)',
            'border': r'border:([^;\s]+)',
            'font': r'font:([^;\s]+)',
            'align': r'align:([^;\s]+)',
            'radius': r'radius:([^;\s]+)',
            'weight': r'weight:([^;\s]+)',
            'shadow': r'shadow:([^;\s]+)',
            'opacity': r'opacity:([^;\s]+)'
        }
        
        for attr, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                value = match.group(1).strip()
                if value:
                    style_attrs[attr] = value
                    # إزالة النمط من النص
                    text_content = re.sub(pattern, '', text_content)
        
        text_content = ' '.join(text_content.split())
        return text_content, style_attrs

    def generate_css_class(self, style_attrs: dict) -> str:
        """إنشاء CSS class"""
        if not style_attrs:
            return ""
        
        # إنشاء class جديد
        self.class_counter += 1
        class_name = f"ws{self.class_counter}"
        
        # تحويل الأنماط إلى CSS
        css_rules = []
        for attr, value in style_attrs.items():
            css_rule = self._convert_to_css(attr, value)
            if css_rule:
                css_rules.append(css_rule)
        
        if css_rules:
            self.custom_styles[f".{class_name}"] = "; ".join(css_rules)
            return f' class="{class_name}"'
        
        return ""

    def _convert_to_css(self, attr: str, value: str) -> str:
        """تحويل خصائص White إلى CSS مع دعم جميع الألوان"""
        if not value:
            return ""
        
        if attr == 'color':
            # First check if it's a theme color
            if value in self.theme_colors:
                value = self.theme_colors[value]
            # Otherwise use the color as-is (supports hex, rgb, hsl, named colors)
            return f"color: {value}"
        elif attr == 'size':
            if value.isdigit():
                value = f"{value}px"
            return f"font-size: {value}"
        elif attr == 'bg':
            # Same flexible approach for background colors
            if value in self.theme_colors:
                value = self.theme_colors[value]
            return f"background-color: {value}"
        elif attr == 'width':
            if value.isdigit():
                value = f"{value}px"
            return f"width: {value}"
        elif attr == 'height':
            if value.isdigit():
                value = f"{value}px"
            return f"height: {value}"
        elif attr == 'margin':
            if value.isdigit():
                value = f"{value}px"
            elif value == 'auto':
                return "margin: 0 auto"
            elif value == 'center':
                return "margin: 0 auto; display: block"
            return f"margin: {value}"
        elif attr == 'padding':
            if value.isdigit():
                value = f"{value}px"
            return f"padding: {value}"
        elif attr == 'border':
            # Support border colors too
            if value in self.theme_colors:
                value = self.theme_colors[value]
            return f"border: 1px solid {value}"
        elif attr == 'font':
            return f"font-family: {value}"
        elif attr == 'align':
            return f"text-align: {value}"
        elif attr == 'radius':
            if value.isdigit():
                value = f"{value}px"
            return f"border-radius: {value}"
        elif attr == 'weight':
            return f"font-weight: {value}"
        elif attr == 'shadow':
            return f"box-shadow: 0 2px 10px rgba(0,0,0,{value})"
        elif attr == 'opacity':
            return f"opacity: {value}"
        
        return ""


class TableManager:
    """إدارة الجداول"""
    def __init__(self):
        self.current_table = None
        self.table_counter = 0

    def start_table(self, headers: list = None, style_attrs: dict = None):
        """بدء جدول جديد"""
        self.table_counter += 1
        table_id = f"table_{self.table_counter}"
        
        self.current_table = {
            'id': table_id,
            'headers': headers or [],
            'rows': [],
            'style_attrs': style_attrs or {}
        }

    def add_table_row(self, cells: list):
        """إضافة صف للجدول"""
        if self.current_table:
            self.current_table['rows'].append(cells)

    def end_table(self, style_manager) -> str:
        """إنهاء الجدول وإرجاع HTML"""
        if not self.current_table:
            return ""
        
        class_attr = style_manager.generate_css_class(self.current_table['style_attrs'])
        if class_attr:
            m = re.search(r'class="([^"]+)"', class_attr)
            if m:
                existing = m.group(1)
                combined = f' class="{existing} white-table"'
            else:
                combined = ' class="white-table"'
        else:
            combined = ' class="white-table"'
        
        table_html = []
        table_html.append(f'<table{combined}>')
        
        # Headers
        if self.current_table['headers']:
            table_html.append('    <thead>')
            table_html.append('        <tr>')
            for header in self.current_table['headers']:
                clean_header = header.strip().strip('"').strip("'")
                table_html.append(f'            <th>{clean_header}</th>')
            table_html.append('        </tr>')
            table_html.append('    </thead>')
        
        # Body
        if self.current_table['rows']:
            table_html.append('    <tbody>')
            for row in self.current_table['rows']:
                table_html.append('        <tr>')
                for cell in row:
                    clean_cell = cell.strip().strip('"').strip("'")
                    table_html.append(f'            <td>{clean_cell}</td>')
                table_html.append('        </tr>')
            table_html.append('    </tbody>')
        
        table_html.append('</table>')
        
        result = '\n'.join(table_html)
        self.current_table = None
        return result

class FormManager:
    """إدارة النماذج"""
    def __init__(self):
        self.current_form = None
        self.form_elements = []
        self.form_counter = 0

    def start_form(self, action: str = "", method: str = "POST", name: str = "", style_attrs: dict = None):
        """بدء نموذج جديد"""
        self.form_counter += 1
        form_id = f"form_{self.form_counter}"
        
        if not name:
            name = form_id
        
        self.current_form = {
            'id': form_id,
            'name': name,
            'action': action,
            'method': method,
            'elements': [],
            'style_attrs': style_attrs or {}
        }
        return form_id

    def add_form_element(self, element_html: str):
        """إضافة عنصر للنموذج الحالي"""
        if self.current_form:
            self.current_form['elements'].append(element_html)

    def end_form(self, style_manager) -> str:
        """إنهاء النموذج وإرجاع HTML"""
        if not self.current_form:
            return ""
        
        class_attr = ''
        if self.current_form.get('style_attrs'):
            raw = style_manager.generate_css_class(self.current_form['style_attrs'])
            if raw:
                m = re.search(r'class="([^"]+)"', raw)
                if m:
                    class_attr = f' class="{m.group(1)} white-form"'
                else:
                    class_attr = ' class="white-form"'
        else:
            class_attr = ' class="white-form"'
        
        form_html = []
        action = f' action="{self.current_form["action"]}"' if self.current_form["action"] else ''
        method = f' method="{self.current_form["method"]}"'
        form_id = f' id="{self.current_form["id"]}"'
        
        form_html.append(f'<form{form_id}{action}{method}{class_attr}>')
        
        for element in self.current_form['elements']:
            form_html.append(f'    {element}')
        
        form_html.append('</form>')
        
        result = '\n'.join(form_html)
        self.current_form = None
        return result

class VariableManager:
    """إدارة المتغيرات"""
    def __init__(self):
        self.variables = {}
    
    def set_variable(self, name: str, value):
        """تعيين متغير"""
        self.variables[name] = str(value)
    
    def get_variable(self, name: str):
        """الحصول على قيمة متغير"""
        return self.variables.get(name, f"{{{name}}}")
    
    def replace_variables(self, text: str) -> str:
        """استبدال المتغيرات في النص"""
        pattern = r'\{(\w+)\}'
        
        def replacer(match):
            var_name = match.group(1)
            return str(self.get_variable(var_name))
        
        return re.sub(pattern, replacer, text)

class WhiteCompiler:
    def __init__(self, theme_config=None):
        self.style_manager = StyleManager()
        self.variable_manager = VariableManager()
        self.form_manager = FormManager()
        self.table_manager = TableManager()
        self.html_output = []
        self.metadata = {'title': 'White Language Output'}
        self.theme_config = {
        'minimal_css': False,
        'enable_gradients': True,
        'enable_shadows': True,
        'container_centered': True,}
        if theme_config:
            self.theme_config.update(theme_config)
        
        
    def find_white_files(self, path: str = "."):
        """البحث عن جميع ملفات .white"""
        white_files = []
        
        if os.path.isfile(path) and path.endswith('.white'):
            return [path]
        
        if os.path.isdir(path):
            pattern = os.path.join(path, "*.white")
            white_files = glob.glob(pattern)
        
        return white_files
    
    def parse_file(self, filename: str) -> str:
        """تحليل ملف White"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            
            print(f"parsing {filename}")
            return self.compile_to_html(content)
            
        except FileNotFoundError:
            error_msg = f"not found {filename}"
            print(error_msg)
            return self.generate_error_html(error_msg)
        except Exception as e:
            error_msg = f"couldn't read {str(e)}"
            print(error_msg)
            return self.generate_error_html(error_msg)
    
    def generate_error_html(self, error_message: str) -> str:
        """إنشاء HTML لعرض الأخطاء"""
        return f"""<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>خطأ - White Compiler</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f8f9fa; }}
        .error {{ background: #f8d7da; color: #721c24; padding: 20px; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="error">
        <h2>حدث خطأ</h2>
        <p>{error_message}</p>
    </div>
</body>
</html>"""

    def handle_table(self, line: str) -> str:
        """معالجة أمر الجدول"""
        match = re.search(r'headers:\[(.+)\]', line)
        if match:
            headers_str = match.group(1)
            headers = []
            current_header = ""
            in_quotes = False
            quote_char = None
            
            for char in headers_str:
                if char in ['"', "'"] and not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char and in_quotes:
                    in_quotes = False
                    quote_char = None
                elif char == ',' and not in_quotes:
                    if current_header.strip():
                        headers.append(current_header.strip())
                    current_header = ""
                    continue
                
                if char != quote_char or in_quotes:
                    current_header += char
            
            if current_header.strip():
                headers.append(current_header.strip())
            
            self.table_manager.start_table(headers)
        
        return ""

    def handle_tablerow(self, line: str) -> str:
        """معالجة صف الجدول"""
        content = line[8:].strip()
        
        cells = []
        current_cell = ""
        in_quotes = False
        quote_char = None
        
        for char in content:
            if char in ['"', "'"] and not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
            elif char == ',' and not in_quotes:
                if current_cell.strip():
                    cells.append(current_cell.strip())
                current_cell = ""
                continue
            
            if char != quote_char or in_quotes:
                current_cell += char
        
        if current_cell.strip():
            cells.append(current_cell.strip())
        
        self.table_manager.add_table_row(cells)
        return ""

    def handle_endtable(self) -> str:
        """إنهاء الجدول"""
        return self.table_manager.end_table(self.style_manager)

    def handle_form(self, line: str) -> str:
        """معالجة بدء النموذج"""
        content = line[4:].strip()
        content, style_attrs = self.style_manager.parse_style_attributes(content)
        
        action = ""
        method = "POST"
        name = ""
        
        action_match = re.search(r'action:"?([^"\s]+)"?', content)
        if action_match:
            action = action_match.group(1)
        
        method_match = re.search(r'method:"?([^"\s]+)"?', content)
        if method_match:
            method = method_match.group(1)
        
        name_match = re.search(r'name:"?([^"\s]+)"?', content)
        if name_match:
            name = name_match.group(1)
        
        self.form_manager.start_form(action, method, name, style_attrs)
        return ""

    def handle_input(self, line: str) -> str:
        """معالجة حقل الإدخال"""
        content = line[5:].strip()
        
        label = ""
        if content.startswith('"'):
            end_quote = content.find('"', 1)
            if end_quote != -1:
                label = content[1:end_quote]
                content = content[end_quote + 1:].strip()
        
        input_type = "text"
        name = ""
        required = False
        
        type_match = re.search(r'type:([^\s]+)', content)
        if type_match:
            input_type = type_match.group(1)
        
        name_match = re.search(r'name:([^\s]+)', content)
        if name_match:
            name = name_match.group(1)
        
        if 'required' in content:
            required = True
        
        required_attr = ' required' if required else ''
        input_html = f'<div class="form-group"><label for="{name}">{label}</label><input type="{input_type}" id="{name}" name="{name}"{required_attr} class="form-control"></div>'
        
        self.form_manager.add_form_element(input_html)
        return ""

    def handle_select(self, line: str) -> str:
        """معالجة قائمة الاختيار"""
        content = line[6:].strip()
        
        label = ""
        if content.startswith('"'):
            end_quote = content.find('"', 1)
            if end_quote != -1:
                label = content[1:end_quote]
                content = content[end_quote + 1:].strip()
        
        name = ""
        options = []
        required = False
        
        name_match = re.search(r'name:([^\s]+)', content)
        if name_match:
            name = name_match.group(1)
        
        options_match = re.search(r'options:\[(.+)\]', content)
        if options_match:
            options_str = options_match.group(1)
            current_option = ""
            in_quotes = False
            quote_char = None
            
            for char in options_str:
                if char in ['"', "'"] and not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char and in_quotes:
                    in_quotes = False
                    quote_char = None
                elif char == ',' and not in_quotes:
                    if current_option.strip():
                        options.append(current_option.strip().strip('"').strip("'"))
                    current_option = ""
                    continue
                
                if char != quote_char or in_quotes:
                    current_option += char
            
            if current_option.strip():
                options.append(current_option.strip().strip('"').strip("'"))
        
        if 'required' in content:
            required = True
        
        required_attr = ' required' if required else ''
        
        select_html = [f'<div class="form-group"><label for="{name}">{label}</label>']
        select_html.append(f'<select id="{name}" name="{name}"{required_attr} class="form-control">')
        select_html.append('<option value="">اختر...</option>')
        
        for option in options:
            select_html.append(f'<option value="{option}">{option}</option>')
        
        select_html.append('</select></div>')
        
        self.form_manager.add_form_element('\n'.join(select_html))
        return ""

    def handle_textarea(self, line: str) -> str:
        """معالجة منطقة النص"""
        content = line[8:].strip()
        
        label = ""
        if content.startswith('"'):
            end_quote = content.find('"', 1)
            if end_quote != -1:
                label = content[1:end_quote]
                content = content[end_quote + 1:].strip()
        
        name = ""
        rows = "4"
        
        name_match = re.search(r'name:([^\s]+)', content)
        if name_match:
            name = name_match.group(1)
        
        rows_match = re.search(r'rows:([^\s]+)', content)
        if rows_match:
            rows = rows_match.group(1)
        
        textarea_html = f'<div class="form-group"><label for="{name}">{label}</label><textarea id="{name}" name="{name}" rows="{rows}" class="form-control"></textarea></div>'
        
        self.form_manager.add_form_element(textarea_html)
        return ""

    def handle_endform(self) -> str:
        """إنهاء النموذج"""
        return self.form_manager.end_form(self.style_manager)

    def handle_span_concatenation(self, line: str) -> str:
        """معالجة دمج النصوص مع span"""
        parts = []
        current_part = ""
        i = 0
        
        while i < len(line):
            if line[i:i+5] == 'span ':
                if current_part.strip():
                    parts.append(('text', current_part.strip().strip('"').strip("'")))
                    current_part = ""
                
                span_start = i + 5
                span_content = ""
                quote_char = None
                
                j = span_start
                while j < len(line) and line[j] in [' ', '"', "'"]:
                    if line[j] in ['"', "'"]:
                        quote_char = line[j]
                        j += 1
                        break
                    j += 1
                
                if quote_char:
                    while j < len(line) and line[j] != quote_char:
                        span_content += line[j]
                        j += 1
                    j += 1
                
                span_attrs = {}
                remaining = line[j:].strip()
                if remaining.startswith(' '):
                    remaining = remaining[1:]
                
                color_match = re.search(r'color:([^\s+]+)', remaining)
                if color_match:
                    span_attrs['color'] = color_match.group(1)
                
                weight_match = re.search(r'weight:([^\s+]+)', remaining)
                if weight_match:
                    span_attrs['weight'] = weight_match.group(1)
                
                parts.append(('span', span_content, span_attrs))
                
                next_plus = remaining.find('+')
                if next_plus != -1:
                    i = j + next_plus + 1
                else:
                    break
                    
            elif line[i] == '+':
                if current_part.strip():
                    parts.append(('text', current_part.strip().strip('"').strip("'")))
                    current_part = ""
                i += 1
            else:
                current_part += line[i]
                i += 1
        
        if current_part.strip():
            parts.append(('text', current_part.strip().strip('"').strip("'")))
        
        html_parts = []
        for part in parts:
            if part[0] == 'text':
                text = self.variable_manager.replace_variables(part[1])
                html_parts.append(text)
            elif part[0] == 'span':
                content = self.variable_manager.replace_variables(part[1])
                attrs = part[2] if len(part) > 2 else {}
                
                style = ""
                if 'color' in attrs:
                    color = attrs['color']
                    if color in self.style_manager.theme_colors:
                        color = self.style_manager.theme_colors[color]
                    style += f"color: {color}; "
                
                if 'weight' in attrs:
                    style += f"font-weight: {attrs['weight']}; "
                
                style_attr = f' style="{style.strip()}"' if style else ''
                html_parts.append(f'<span{style_attr}>{content}</span>')
        
        return ''.join(html_parts)

    def parse_line(self, line: str) -> str:
        """تحليل سطر واحد والعودة بـ HTML"""
        line = line.strip()
        if not line or line.startswith("//") or line.startswith('#'):
            return ""
        
        if line.startswith("table "):
            return self.handle_table(line)
        elif line.startswith("tablerow "):
            return self.handle_tablerow(line)
        elif line == "endtable":
            return self.handle_endtable()
        elif line.startswith("form "):
            return self.handle_form(line)
        elif line.startswith("input "):
            return self.handle_input(line)
        elif line.startswith("select "):
            return self.handle_select(line)
        elif line.startswith("textarea "):
            return self.handle_textarea(line)
        elif line == "endform":
            return self.handle_endform()
        elif 'span ' in line and ('+' in line or 'span "' in line):
            return f"<p>{self.handle_span_concatenation(line)}</p>"
        elif line.startswith("image "):
            return self._handle_image(line)
        elif line.startswith("span "):
            return self._handle_span(line)
        elif line.startswith("title "):
            return self._handle_title(line)
        elif line.startswith("button "):
            return self._handle_button(line)
        elif line.startswith("print "):
            return self._handle_print(line)
        elif line.startswith("header "):
            return self._handle_header(line)
        elif line.startswith("paragraph "):
            return self._handle_paragraph(line)
        elif line.startswith("link "):
            return self._handle_link(line)
        elif line.startswith("list "):
            return self._handle_list(line)
        elif line.startswith("var"):
            args = line.split()
            var_name = args[1]
            value = " ".join(args[3:]).strip("\"'")
            self.variable_manager.set_variable(var_name, value)
            return ""
        elif line.startswith("code "):
            return self._handle_code(line)
        elif line.startswith("div "):
            return self._handle_div(line)
        elif line == "br":
            return "<br>"
        elif line == "hr":
            return "<hr>"
        else:
            content = self.variable_manager.replace_variables(line)
            return f"<p>{content}</p>"
        
        return f"<p>{line}</p>"

    def _handle_image(self, line: str) -> str:
        """معالجة الصور"""
        match = re.search(r'image\s+"([^"]+)"', line)
        src = match.group(1) if match else ""
        
        match_alt = re.search(r'alt:"([^"]+)"', line)
        alt = match_alt.group(1) if match_alt else ""
        
        match_w = re.search(r'width:(\d+)', line)
        width = match_w.group(1) if match_w else ""
        
        match_r = re.search(r'radius:(\d+)', line)
        radius = match_r.group(1) if match_r else ""
        
        style = ""
        if radius:
            style += f"border-radius:{radius}px;"
        
        width_attr = f' width="{width}"' if width else ""
        style_attr = f' style="{style}"' if style else ""
        
        return f'<img src="{src}" alt="{alt}"{width_attr}{style_attr}>'

    def _handle_span(self, line: str) -> str:
        """معالجة span"""
        match = re.search(r'span\s+"([^"]+)"', line)
        text = match.group(1) if match else ""
        
        match_c = re.search(r'class:([^\s]+)', line)
        cls = match_c.group(1) if match_c else ""
        
        match_color = re.search(r'color:([^\s]+)', line)
        color = match_color.group(1) if match_color else ""
        
        if color in self.style_manager.theme_colors:
            color = self.style_manager.theme_colors[color]
        
        style = f' style="color:{color};"' if color else ""
        class_attr = f' class="{cls}"' if cls else ""
        
        return f'<span{class_attr}{style}>{text}</span>'
    
    def compile_to_html(self, source_code: str) -> str:
        """تحويل كود White إلى HTML"""
        self.html_output = []
        
        lines = source_code.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('meta '):
                self._handle_meta(line)
        
        self._generate_html_head()
        
        for line_num, line in enumerate(lines, 1):
            try:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('meta '):
                    html_output = self.parse_line(line)
                    if html_output:
                        self.html_output.append(html_output)
            except Exception as e:
                error_html = f'<div style="background: #f8d7da; color: #721c24; padding: 10px; margin: 5px 0; border-radius: 5px;">خطأ في السطر {line_num}: {str(e)}</div>'
                self.html_output.append(error_html)
                print(f"⚠️ خطأ في السطر {line_num}: {str(e)}")
        
        # إنهاء أي جدول أو نموذج مفتوح
        if self.table_manager.current_table:
            self.html_output.append(self.table_manager.end_table(self.style_manager))
        if self.form_manager.current_form:
            self.html_output.append(self.form_manager.end_form(self.style_manager))
        
        self._generate_html_footer()
        return '\n'.join(self.html_output)
    
    def _generate_html_head(self):
        """إنشاء رأس HTML"""
        title = self.metadata.get('title', 'White Language Output')
        description = self.metadata.get('description', '')
        
        self.html_output.extend([
            '<!DOCTYPE html>',
            '<html lang="ar">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'    <title>{title}</title>'
        ])
        
        if description:
            self.html_output.append(f'    <meta name="description" content="{description}">')
        
        self.html_output.append('    <style>')
        self.html_output.append(self._generate_base_css())
        
        # إضافة الأنماط المخصصة
        for selector, rules in self.style_manager.custom_styles.items():
            self.html_output.append(f'        {selector} {{ {rules}; }}')
        
        self.html_output.extend([
            '    </style>',
            '</head>',
            '<body>',
            '    <div class="container">'
        ])
    
    def _generate_base_css(self) -> str:
        if self.theme_config.get('minimal_css', False):
            return self._generate_minimal_css()
        else:
            return self._generate_full_css()
    def _generate_minimal_css(self) -> str:
        """Generate minimal base CSS - NO default colors, maximum user flexibility"""
        return '''        * { 
                box-sizing: border-box; 
            }
            
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                margin: 0;
                padding: 20px;
                direction: rtl;
                /* NO default background or colors - let user define */
            }
            
            .container {
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 40px;
                /* NO default background or colors - let user define */
            }
            
            h1, h2, h3, h4, h5, h6 {
                margin: 20px 0;
                /* NO default color - user has full control */
            }
            
            p {
                margin: 15px 0;
                line-height: 1.8;
                /* NO default color or alignment - user decides */
            }
            
            button { 
                padding: 10px 20px; 
                border: none; 
                border-radius: 4px; 
                cursor: pointer; 
                /* NO default colors - user styles everything */
            }
            
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 20px auto;
            }
            
            th, td {
                padding: 10px;
                border: 1px solid #ddd;
                text-align: center;
            }
            
            .white-form {
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
            }
            
            .form-group {
                margin-bottom: 15px;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: 600;
            }
            
            .form-control {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            
            img {
                max-width: 100%;
                height: auto;
                display: block;
            }
            
            ul {
                margin: 20px auto;
                padding: 20px;
            }
            
            a {
                text-decoration: none;
                /* NO default color - user defines */
            }
            
            a:hover {
                text-decoration: underline;
            }
            
            pre {
                padding: 15px;
                border-radius: 4px;
                overflow-x: auto;
                /* NO default background - user defines */
            }
            
            code {
                font-family: 'Courier New', Consolas, monospace;
            }
            
            hr {
                border: none;
                height: 1px;
                margin: 20px 0;
                /* NO default color - user defines */
            }
            
            /* Essential utility classes */
            .text-center { text-align: center; }
            .text-left { text-align: left; }
            .text-right { text-align: right; }
            .block { display: block; }
            .inline { display: inline; }
            .inline-block { display: inline-block; }
            
            @media (max-width: 768px) {
                .container {
                    padding: 15px;
                }
                
                .white-form {
                    padding: 15px;
                }
            }'''

    def _generate_full_css(self) -> str:
        """Generate full-featured CSS with some default styling but still flexible colors"""
        # Keep theme colors as defaults but don't force them
        primary = self.style_manager.theme_colors.get('primary', '#3498db')
        secondary = self.style_manager.theme_colors.get('secondary', '#2980b9')
        light = self.style_manager.theme_colors.get('light', '#f8f9fa')
        dark = self.style_manager.theme_colors.get('dark', '#2c3e50')
        success = self.style_manager.theme_colors.get('success', '#27ae60')
        warning = self.style_manager.theme_colors.get('warning', '#f39c12')
        info = self.style_manager.theme_colors.get('info', '#17a2b8')

        return f'''        * {{
                box-sizing: border-box;
            }}
            
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                margin: 0;
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                direction: rtl;
            }}
            
            .container {{
                max-width: 1200px; 
                margin: 0 auto; 
                background: rgba(255, 255, 255, 0.95); 
                padding: 40px; 
                border-radius: 20px; 
                box-shadow: 0 15px 35px rgba(0,0,0,0.2);
                backdrop-filter: blur(10px);
            }}
            
            h1, h2, h3, h4, h5, h6 {{
                text-align: center;
                margin: 20px 0;
                /* User can override with color: attribute */
            }}
            
            h1 {{ font-size: 2.5em; margin-bottom: 30px; }}
            h2 {{ font-size: 2em; margin: 25px 0 20px 0; }}
            
            p {{
                text-align: center;
                margin: 15px 0;
                line-height: 1.8;
                /* User can override alignment and color */
            }}
            
            button {{ 
                padding: 12px 24px; 
                margin: 8px; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
                transition: all 0.3s ease;
                font-weight: 600;
                font-size: 16px;
                /* Default button style, but user can override all colors */
                background: {primary};
                color: white;
            }}
            
            button:hover {{ 
                transform: translateY(-2px); 
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                background: {secondary};
            }}
            
            .white-table, table {{
                width: 100%;
                max-width: 800px;
                border-collapse: collapse;
                margin: 30px auto;
                background: white;
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                border-radius: 12px;
                overflow: hidden;
            }}
            
            .white-table th, table th {{
                background: {primary};
                color: white;
                padding: 18px 15px;
                text-align: center;
                font-weight: 600;
                font-size: 16px;
            }}
            
            .white-table td, table td {{
                padding: 15px;
                border-bottom: 1px solid #eee;
                text-align: center;
                font-size: 14px;
            }}
            
            .white-table tbody tr:hover, table tbody tr:hover {{
                background: {light};
                transition: background 0.3s ease;
            }}
            
            .white-table tbody tr:nth-child(even), table tbody tr:nth-child(even) {{
                background: #fdfdfd;
            }}
            
            .white-form {{
                background: {light};
                padding: 30px;
                border-radius: 15px;
                margin: 30px auto;
                max-width: 600px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            }}
            
            .form-group {{
                margin-bottom: 20px;
            }}
            
            .form-group label {{
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: {dark};
                font-size: 15px;
            }}
            
            .form-control {{
                width: 100%;
                padding: 12px 15px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 15px;
                transition: all 0.3s ease;
                font-family: inherit;
            }}
            
            .form-control:focus {{
                outline: none;
                border-color: {primary};
                box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
                transform: translateY(-1px);
            }}
            
            img {{
                max-width: 100%;
                height: auto;
                margin: 20px auto;
                display: block;
                border-radius: 8px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}
            
            ul {{
                max-width: 600px;
                margin: 20px auto;
                padding: 25px 30px;
                background: rgba(52, 152, 219, 0.1);
                border-radius: 12px;
                border-right: 4px solid {primary};
            }}
            
            li {{
                margin-bottom: 12px;
                font-size: 16px;
                line-height: 1.6;
            }}
            
            a {{
                color: {primary};
                text-decoration: none;
                font-weight: 500;
                transition: color 0.3s ease;
            }}
            
            a:hover {{
                color: {secondary};
                text-decoration: underline;
            }}
            
            pre {{
                background: {dark};
                color: #ecf0f1;
                padding: 25px;
                border-radius: 12px;
                overflow-x: auto;
                margin: 25px auto;
                max-width: 90%;
                font-size: 14px;
                line-height: 1.5;
            }}
            
            code {{
                font-family: 'Courier New', Consolas, monospace;
            }}
            
            hr {{
                border: none;
                height: 2px;
                background: linear-gradient(to right, transparent, {primary}, transparent);
                margin: 40px 0;
            }}
            
            /* Color utility classes - users can still override these */
            .text-primary {{ color: {primary}; }}
            .text-secondary {{ color: {secondary}; }}
            .text-success {{ color: {success}; }}
            .text-warning {{ color: {warning}; }}
            .text-info {{ color: {info}; }}
            .text-light {{ color: {light}; }}
            .text-dark {{ color: {dark}; }}
            .text-white {{ color: white; }}
            .text-black {{ color: black; }}
            
            .bg-primary {{ background-color: {primary}; }}
            .bg-secondary {{ background-color: {secondary}; }}
            .bg-success {{ background-color: {success}; }}
            .bg-warning {{ background-color: {warning}; }}
            .bg-info {{ background-color: {info}; }}
            .bg-light {{ background-color: {light}; }}
            .bg-dark {{ background-color: {dark}; }}
            .bg-white {{ background-color: white; }}
            .bg-black {{ background-color: black; }}
            
            @media (max-width: 768px) {{
                .container {{
                    padding: 20px;
                    margin: 10px;
                }}
                
                h1 {{ font-size: 2em; }}
                h2 {{ font-size: 1.5em; }}
                
                .white-table, table {{
                    font-size: 12px;
                }}
                
                .white-form {{
                    padding: 20px;
                }}
            }}'''

    # Also update the __init__ method of WhiteCompiler class:
    def __init__(self, theme_config=None):
        self.style_manager = StyleManager()
        self.variable_manager = VariableManager()
        self.form_manager = FormManager()
        self.table_manager = TableManager()
        self.html_output = []
        self.metadata = {'title': 'White Language Output'}
        
        # Add theme configuration support
        self.theme_config = {
            'minimal_css': False,  # Set to True for minimal CSS
            'enable_gradients': True,
            'enable_shadows': True,
            'container_centered': True,
        }
        if theme_config:
            self.theme_config.update(theme_config)
        
    
    def _generate_html_footer(self):
        self.html_output.extend([
            '    </div>',
            '    <footer style="text-align: center; margin-top: 50px; color: rgba(255,255,255,0.9); font-size: 14px;">',
            '        <p>مُولد بواسطة White Language Compiler</p>',
            '    </footer>',
            '</body>',
            '</html>'
        ])

    def _extract_content(self, line: str, command: str) -> str:
        """استخراج المحتوى من السطر"""
        content = line[len(command):].strip()
        
        if content.startswith('"') and content.count('"') >= 2:
            end_quote = content.find('"', 1)
            if end_quote != -1:
                quoted_part = content[1:end_quote]
                remaining = content[end_quote + 1:].strip()
                content = quoted_part + (' ' + remaining if remaining else '')
        elif content.startswith("'") and content.count("'") >= 2:
            end_quote = content.find("'", 1)
            if end_quote != -1:
                quoted_part = content[1:end_quote]
                remaining = content[end_quote + 1:].strip()
                content = quoted_part + (' ' + remaining if remaining else '')
        
        return content

    # معالجات الأوامر الأساسية
    def _handle_print(self, line: str) -> str:
        content = self._extract_content(line, 'print')
        content = self.variable_manager.replace_variables(content)
        content, style_attrs = self.style_manager.parse_style_attributes(content)
        class_attr = self.style_manager.generate_css_class(style_attrs)
        return f'<p{class_attr}>{content}</p>'
    
    def _handle_title(self, line: str) -> str:
        content = self._extract_content(line, 'title')
        content = self.variable_manager.replace_variables(content)
        content, style_attrs = self.style_manager.parse_style_attributes(content)
        class_attr = self.style_manager.generate_css_class(style_attrs)
        return f'<h1{class_attr}>{content}</h1>'
    
    # In handle_form method, check if button is inside form context
    def _handle_button(self, line: str) -> str:
        content = self._extract_content(line, 'button')
        content = self.variable_manager.replace_variables(content)
        content, style_attrs = self.style_manager.parse_style_attributes(content)
        
        button_type = "button"
        if 'type:submit' in line:
            button_type = "submit"
        elif 'type:reset' in line:
            button_type = "reset"

        class_attr = self.style_manager.generate_css_class(style_attrs)
        button_html = f'<button type="{button_type}"{class_attr}>{content}</button>'
        
        # If we're inside a form, add to form elements instead of returning directly
        if self.form_manager.current_form:
            self.form_manager.add_form_element(button_html)
            return ""
        
        return button_html
    
    def _handle_header(self, line: str) -> str:
        content = self._extract_content(line, 'header')
        content = self.variable_manager.replace_variables(content)
        content, style_attrs = self.style_manager.parse_style_attributes(content)
        class_attr = self.style_manager.generate_css_class(style_attrs)
        return f'<h2{class_attr}>{content}</h2>'
    
    def _handle_paragraph(self, line: str) -> str:
        content = self._extract_content(line, 'paragraph')
        content = self.variable_manager.replace_variables(content)
        content, style_attrs = self.style_manager.parse_style_attributes(content)
        class_attr = self.style_manager.generate_css_class(style_attrs)
        return f'<p{class_attr}>{content}</p>'
    
    def _handle_link(self, line: str) -> str:
        content = self._extract_content(line, 'link')
        content = self.variable_manager.replace_variables(content)
        content, style_attrs = self.style_manager.parse_style_attributes(content)
        
        if ' to ' in content:
            parts = content.split(' to ', 1)
            text = parts[0].strip().strip('"').strip("'")
            url = parts[1].strip().strip('"').strip("'")
            
            class_attr = self.style_manager.generate_css_class(style_attrs)
            return f'<a href="{url}"{class_attr}>{text}</a>'
        return ""
    
    def _handle_list(self, line: str) -> str:
        content = self._extract_content(line, 'list')
        content = self.variable_manager.replace_variables(content)
        content, style_attrs = self.style_manager.parse_style_attributes(content)
        
        items = [item.strip().strip('"').strip("'") for item in content.split(',')]
        class_attr = self.style_manager.generate_css_class(style_attrs)
        
        list_html = [f'<ul{class_attr}>']
        for item in items:
            if item:
                list_html.append(f'    <li>{item}</li>')
        list_html.append('</ul>')
        
        return '\n'.join(list_html)
    
    def _handle_code(self, line: str) -> str:
        content = self._extract_content(line, 'code')
        content, style_attrs = self.style_manager.parse_style_attributes(content)
        
        content = content.replace('\\n', '\n')
        
        class_attr = self.style_manager.generate_css_class(style_attrs)
        return f'<pre{class_attr}><code>{content}</code></pre>'
    
    def _handle_div(self, line: str) -> str:
        content = self._extract_content(line, 'div')
        content = self.variable_manager.replace_variables(content)
        content, style_attrs = self.style_manager.parse_style_attributes(content)
        class_attr = self.style_manager.generate_css_class(style_attrs)
        return f'<div{class_attr}>{content}</div>'
    
    def _handle_meta(self, line: str):
        """معالجة metadata"""
        content = self._extract_content(line, 'meta')
        if '=' in content:
            key, value = content.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            self.metadata[key] = value

def main():
    """الدالة الرئيسية"""
    print("White Language Compiler")
    
    search_path = "."
    if len(sys.argv) > 1:
        search_path = sys.argv[1]
    
    compiler = WhiteCompiler()
    
    white_files = compiler.find_white_files(search_path)
    
    if not white_files:
        print(f"couldn't find files")
        return
    
    print(f"a file is found {len(white_files)} :")
    for i, file in enumerate(white_files, 1):
        print(f"   {i}. {file}")
    print()
    
    for white_file in white_files:
        try:
            print(f"processing: {white_file}")
            
            html_output = compiler.parse_file(white_file)
            
            output_file = white_file.replace('.white', '.html')
            
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(html_output)
            
            print(f"created {output_file}")
                        
        except Exception as e:
            print(f"error{str(e)}")
        
        print()

if __name__ == "__main__":
    main()
