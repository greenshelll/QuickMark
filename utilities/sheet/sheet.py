from html2image import Html2Image
import math


class BubbleSheet:
    mc_col_weight = 1
    tf_col_weight = 0.6
    idtf_col_weight = 2.1
    def __init__(self, mc_num, tf_num, idtf_num, header_name):
        self.mc_num = mc_num
        self.tf_num = tf_num
        self.idtf_num = idtf_num
        self.header_name = header_name
        self.html = None
        

    def ok_layout(self,mc, tf, idtf):
        # checks if layout is going to be okay given number of items per category
        a = self.mc_col_weight*math.ceil(mc/25)
        b = self.tf_col_weight*math.ceil(tf/25)
        c = self.idtf_col_weight*math.ceil(idtf/10)
        total = a+b+c
        
        # allow fit to be lower/better when a category is absent
        
        if a==0:
            total -= 0.4
        if c == 0:
            total -= 0.4
        if b==0:
            total -= 0.4
        print(total)

        print("Layout Fit:",total/7*100,'%')
        if total > 7:
            return False
        else: 
            return True
        
    def html_to_png(self,mc_num, tf_num, idtf_num, png_file, width_inches, height_inches, dpi):
        # Calculate width and height in pixels
        width_pixels = int(width_inches * dpi)
        height_pixels = int(height_inches * dpi)
        

        def mc_instance(times):
            columns = []
            template = ''
            counter = 0
            for instance in range(1,times+1):
                counter+=1
                
                x_formatted = '{:03d}'.format(instance)
                template += f"""<div class="instance">
                                {x_formatted}
                                <div class="circle"></div>
                                <div class="circle"></div>
                                <div class="circle"></div>
                                <div class="circle"></div>
                            </div>"""
                if counter == 25:
                    template = '<div class="column-inner">'+template+'</div>'
                    columns.append(template)
                    template = ''
                    counter = 0
                if instance == times:
                    template = '<div class="column-inner">'+template+'</div>'
                    columns.append(template)
        
            columns = '<div class="column-group">'+''.join(columns)+'</div>'
            return columns
        
        def tf_instance(times):
            columns = []
            template = ''
            counter = 0
            for instance in range(1,times+1):
                counter+=1
                
                x_formatted = '{:03d}'.format(instance)
                template += f"""<div class="instance">
                                {x_formatted}
                                <div class="circle"></div>
                                <div class="circle"></div>
                            </div>"""
                if counter == 25:
                    template = '<div class="column-inner">'+template+'</div>'
                    columns.append(template)
                    template = ''
                    counter = 0
                if instance == times:
                    template = '<div class="column-inner">'+template+'</div>'
                    columns.append(template)
            columns = '<div class="column-group">'+''.join(columns)+'</div>'
            return columns
        
        
        def idtf_instance(times):
            columns = []
            template = ''
            counter = 0
            for instance in range(1,times+1):
                counter+=1
                x_formatted = '{:03d}'.format(instance)
                box = '<div class="box"></div>'*15
                template += f"""<div class="id-instance">{x_formatted}
                        <div class="box-instance">{box}</div></div>"""
                if counter == 10:
                    template = '<div class="column-inner">'+template+'</div>'
                    columns.append(template)
                    template = ''
                    counter = 0
                if instance == times:
                    template = '<div class="column-inner">'+template+'</div>'
                    columns.append(template)
            columns = '<div class="column-group">'+''.join(columns)+'</div>'
            return columns
        
        mc = mc_instance(mc_num)
        tf = tf_instance(tf_num)
        id = idtf_instance(idtf_num)
        type_counter = 0
        roman_num = ['I', 'II', 'III']
        def increment_type():
            nonlocal type_counter
            type_counter += 1
            return int(type_counter - 1)
        mcf = f'<div class="column"><b class="type-test"><div class="start"></div>{roman_num[increment_type()]}. Multiple Choice</b>{mc}</div>' if mc != '<div class="column-group">'+'</div>' else ''
        tff = f'<div class="column"><b class="type-test"><div class="start"></div>{roman_num[increment_type()]}. True or False</b>{tf}</div>' if tf !='<div class="column-group">'+'</div>'  else ''
        idf =  f'<div class="column"><b class="type-test"><div class="start"></div>{roman_num[increment_type()]}. Identification</b>{id}</div>' if id !='<div class="column-group">'+'</div>'  else ''
        
        html_string_with_size  = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Two Main Divs with Three Columns</title>
        <style>
            html{{
                height: 8in;
                width: 14in;
                background-color: white;
            }}
            
            body {{
                font-family: Arial, sans-serif;
                
                margin-left: 25px;
                
            }}
            
            
            .container {{
                display: flex;
                flex-direction: column;
                height: 80vh; /* Height of the viewport */
            }}
            
            .top {{
                background-color: white;
                padding-left: 10px;
                padding-right: 10px;
                padding-top: 5px;
                padding-bottom: 1px;
                display: flex;
                flex-direction: row;
            }}
            
            .bottom {{
                flex: 1; /* Fill remaining vertical space */
                display: flex;
                color: rgba(150,150,150);
                justify-content: space-between;
                background-color: white;
            }}
            
            .column {{
                flex: 1; /* Equal width */
                margin: 0 5px; /* Adjust space between columns */
                border-width: 5px;
                border-style: solid;
                display: flex;
                border-color: black;
                flex-direction: column;
                

            }}
            
            .column-inner {{
                background-color: white;
                padding: 5px;
                
            }}
            h2 {{
                text-align: center;
            }}
            .circle {{
                margin-left: 10px;
                display: flex;
                width: 15px;
                height: 15px;
                border-radius: 0%; /* Make it a circle */
                background-color: white; /* Blue background color */
                color: black; /* White text color */
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 10px; /* Adjust font size as needed */
                font-weight: bold;
                border-width: 4px;
                border-color: black;
                border-style: solid;
            }}
            .instance{{
                display: flex;
                flex-direction: row;
                margin-bottom:3px;
            }}
            .column-instance{{
                display: flex;
                flex-direction: row;
                border-width: 3px;
                border-style: solid;
                
            }}
            .box{{
                width: 30px;
                height: 40px;
                
                
                border-style: solid;
                border-width: 3;
                border-color: black;
            }}
            .box-instance{{
                display: flex;
                flex-direction: row;
                margin-left: 10px;
                border: 3px;
                border-style: solid;
                border-color: black;
            }}
            .id-instance{{
                display: flex;
                flex-direction: row;
                margin-right: 10px;
                margin-bottom: 10px;
            }}
            .column-group{{
                display: flex;

            }}
            .type-test{{
                margin-left: 5px;
                margin-top: 5px;
                display: flex;
                flex-direction: row;
            }}
            .start{{
                width: 0px;
                height: 0px;
                background-color: black;
                margin-right: 10px;
                
            }}
            .i {{
                margin-right: 20px;
                width: 500px;
                

            }}
        </style>
        </head>
        <body>
        <div class="container">
            <div class="top">
                <p><div class="i">{self.header_name}</div><b>Name: </b>______________________________ <b>Year and Section: </b>_____________ <b>Date: </b>________________</p> 
            </div>
            <div class="bottom">
                {mcf}

                {tff}

                {idf}
            </div>
            <script>
                window.onload = function() {{
                    var elements = document.querySelectorAll('.container');
                    var infoDiv = document.getElementById('info');
            
                    elements.forEach(function(element) {{
                        var rect = element.getBoundingClientRect();
                        var info = document.createElement('div');
                        info.innerHTML = "Element: " + element.id + "<br>" +
                                         "Width: " + rect.width + "<br>" +
                                         "Height: " + rect.height + "<br>" +
                                         "X: " + rect.x + "<br>" +
                                         "Y: " + rect.y + "<br>-----------------<br>";
                        infoDiv.appendChild(info);
                    }});
                }};
            </script>
        </div>
        </body>
        </html>

        """
        self.html = html_string_with_size
        # Create PNG image with specified size
        hti = Html2Image()
        hti.screenshot(html_str=html_string_with_size, save_as=png_file, size=(width_pixels, height_pixels))
    
    def save_template_as_html(self, filepath):
        # testing// extracting as html file
        with open(filepath, 'w') as w:
            w.write(self.html)
        print('Template saved as html in', filepath)
    def save_template_as_img(self, filepath):
        png_file = filepath
        width_inches = 14  # example width in inches
        height_inches = 8.5  # example height in inches
        dpi = 96  # example DPI (dots per inch)
        #___________________________________
        # number of items per category
        #best fits examples
        # 175 multiple choice
        # or 50 multiple choice, 100 true or false, 20 identification
        multiple_choice_num = self.mc_num
        true_false_num = self.tf_num
        identif_num = self.idtf_num
        is_ok = self.ok_layout(multiple_choice_num, true_false_num, identif_num)# checks if layout is going to be okay given number of items per category
        if is_ok:
            self.html_to_png(multiple_choice_num, true_false_num, identif_num, png_file, width_inches, height_inches, dpi)
        else:
            print("WARNING !!!! ITEMS SELECTED EXCEEDS LAYOUT LIMIT!!!!") 
            self.html_to_png(multiple_choice_num, true_false_num, identif_num, png_file, width_inches, height_inches, dpi)

