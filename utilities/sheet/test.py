from sheet import BubbleSheet

sheet = BubbleSheet(mc_num = 100,
                    tf_num = 10,
                    idtf_num = 10,
                    header_name = "Examination 1: Sample Exam")
sheet.save_template_as_img("template.png")
sheet.save_template_as_html('template.html')
