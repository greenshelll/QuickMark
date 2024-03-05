from sheet import BubbleSheet

sheet = BubbleSheet(mc_num = 100,
                    tf_num =25,
                    idtf_num = 10,
                    header_name = "Examination 1: Sample Exam")
sheet.save_template_as_img("template.png")
sheet.save_template_as_html('template.html')

"""
Max:
    MC: 175
    True or False: 300
    idtf: 30


"""