#!/usr/bin/env python
# # -*- coding: utf-8 -*-

'''
the script is used to generate vod datamodel html view, base on the vod
datamodel definition in datamodel.xml file, and the related db_gen tool
the db_gen tool has already parse out the datamodel.xml file, and this
script just use the parse result to convert it to a table format in
HTML file, the HTML file use the bootstrap as the basic css style.
'''

''' author: denny wang (wangliang8@hisense.com) '''

import os
import re
import sys
import shutil
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

cwp = os.path.dirname(os.path.realpath(__file__))
kernel_path = os.path.join(cwp, "../kernel")
datamodel_path = cwp
file_menu = {}
kernel_re = re.compile(r"kernel_(.+).full.tar")
VERSION = "0.0.0.0"
KERNEL_NAME = ""


html_template = '''
<!DOCTYPE html>
<html>
   <head>
   <title>聚好看数据模型 <{{version}}></title>
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <!-- 引入 Bootstrap -->
   <link href="http://apps.bdimg.com/libs/bootstrap/3.3.0/css/bootstrap.min.css" rel="stylesheet">
   
   <!-- HTML5 Shim 和 Respond.js 用于让 IE8 支持 HTML5元素和媒体查询 -->
   <!-- 注意： 如果通过 file://  引入 Respond.js 文件，则该文件无法起效果 -->
   <!--[if lt IE 9]>
   <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
   <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
   <![endif]-->
   </head>
   <body>
   <div class="container">
   <h3>聚好看数据模型对照 版本{{version}}</h3>
   <table class="table table-condensed table-hover table-striped table-bordered">
     <caption><h3>每一个表都会拥有的公用字段</h3>（每个表的描述中不会再做涉及）</caption>
     <thead>
       <tr>
         <th class="col-md-2">字段</th>
         <th class="col-md-1">类型</th>
         <th class="col-md-1">关键字</th>
         <th class="col-md-1">索引</th>
         <th class="col-md-7">描述</th>
       </tr>
     </thead>
     <tbody>
       <tr>
         <td>id</td>
         <td>BigInteger</td>
         <td>True</td>
         <td>True</td>
         <td>整个表的中记录的唯一标识</td>
       </tr>
       <tr>
         <td>customer_id</td>
         <td>BigInteger</td>
         <td>False</td>
         <td>True</td>
         <td>customer_id</td>
       </tr>
       <tr>
         <td>created_time</td>
         <td>Integer</td>
         <td>False</td>
         <td>False</td>
         <td>记录的创建时间，手动用sql语句创建的话，这个字段需要特殊考虑</td>
       </tr>
       <tr>
         <td>modified_time</td>
         <td>Integer</td>
         <td>False</td>
         <td>False</td>
         <td>记录的修改时间，包括任何字段的修改，手动用sql语句创建的话，这个字段需要特俗考虑</td>
       </tr>
       <tr>
         <td>deleted</td>
         <td>SmallInteger</td>
         <td>False</td>
         <td>False</td>
         <td>记录删除标识，标识本记录在业务系统中属于删除状态，程序需要总是判断此字段来获取有效的数据</td>
       </tr>
     </tbody>
   </table>
   {% for table in tables %}
     <table class="table table-condensed table-hover table-striped table-bordered">
       <caption><h3>表：{{table.table_name}}</h3></caption>
       <thead>
         <tr>
           <th class="col-md-2">字段</th>
           <th class="col-md-1">类型</th>
           <th class="col-md-1">关键字</th>
           <th class="col-md-1">索引</th>
           <th>描述</th>
         </tr>
       </thead>
       <tbody>
       {% for field in table.fields %}
         <tr>
           <td>{{field.name}}</td>
           <td>{{field.full_type}}</td>
           <td>False</td>
           <td>{{field.isIndex}}</td>
           <td>{{field.desc}}</td>
         </tr>
       {% endfor %}
       </tbody>
     </table>
   {% endfor %}

   
   </div>
   <!-- jQuery (Bootstrap 的 JavaScript 插件需要引入 jQuery) -->
   <script src="https://code.jquery.com/jquery.js"></script>
   <!-- 包括所有已编译的插件 -->
   <script src="js/bootstrap.min.js"></script>
   </body>
</html>
'''

def get_kernel_version(fname):
    m = kernel_re.match(fname)
    if m:
        return m.groups()[0]
    return None

def setup_kernel_files():
    global file_menu
    tmp = []
    for f in os.listdir(kernel_path):
        m = kernel_re.match(f)
        if m:
            tmp.append(f)
    tmp = sorted(tmp)
    i = 0
    for f in tmp:
        file_menu[i] = f
        i += 1

def enter_input():
    while True:
        show_files()
        inp = raw_input("input the kernel build index: ")
        if inp.lower() == "q":
            exit(0)
        if not inp.isdigit():
            continue
        index = int(inp)
        if index not in file_menu:
            continue
        return index
    return None

def show_files():
    for index, fname in file_menu.items():
        print "\t%3d %s"%(index, fname)

def copy_kernel_tar_file(fname):
    ''' return the target file path '''
    source = os.path.join(kernel_path, fname)
    target = os.path.join(datamodel_path, fname)
    shutil.copyfile(source, target)
    return target

def extract_tar_file(fpath):
    ''' extract the file for input argument is a full path of file '''
    dirname, fname = os.path.split(fpath)
    os.system("cd %s;tar xvf %s > /dev/null"%(dirname, fname))

def gen_datamodel_file(path):
    ''' input path is the kernel path which was extracted earlier '''
    sys.path.append(path)
    # since the db_gen has no .py suffix, cannot import, so just rename it
    # by adding a .py suffix
    # the following code was copied from db_gen.py file
    # actually, we only take use of the Table Field definition
    os.system("cd {0}/df/datamodel/; mv db_gen db_gen.py".format(path))
    from xml.dom import minidom
    from xml.dom.minidom import getDOMImplementation, Node
    from db_gen import Table, getFields

    doc = minidom.parse(os.path.join(path, "df/datamodel/datamodel.xml"))
    tables = []
    # ******* Table definition SETUP ********
    dict_tables = doc.getElementsByTagName("table")
    for dict_table in dict_tables:
        table = Table(dict_table.getAttribute("name"))
        for field in getFields(dict_table):
            table.appendField(field)
            if field.isIndex:
                table.indexs.append(field)
        tables.append(table)
    export_html(tables)

def export_html(tables):
    # should call the Field object for getattr function with 'type'
    # to get the more detail version of field type, add a full_tyoe
    # field to every field
    for table in tables:
        for field in table.fields:
            field.full_type = field.type

    from jinja2 import Template
    t = Template(html_template)
    s = t.render(tables=tables, version=VERSION)
    dm_fname = "datamodel_%s.html"%VERSION
    print "%s file generated"%dm_fname
    fd = open(dm_fname, 'w')
    fd.write(s)
    fd.close()
    return s

def clean_files():
    extract_kernel_path = os.path.join(datamodel_path, "kernel")
    if os.path.exists(extract_kernel_path):
        print "clear temp folder", extract_kernel_path
        shutil.rmtree(extract_kernel_path)
    kernel_tar_file = os.path.join(datamodel_path, KERNEL_NAME)
    if os.path.exists(kernel_tar_file):
        print "clear temp tarball", kernel_tar_file
        os.remove(kernel_tar_file)
        
def handle_file(fname):
    global VERSION, KERNEL_NAME
    VERSION = get_kernel_version(fname)
    KERNEL_NAME = fname
    print "you have select the kernel file: ", fname
    # normally the kernel tar ball extract as a kernel folder
    p = copy_kernel_tar_file(fname)
    # need to delete the kernel folder first
    extracted_kernel_path = os.path.join(os.path.dirname(p), 'kernel')
    if os.path.exists(extracted_kernel_path):
        shutil.rmtree(extracted_kernel_path)
    extract_tar_file(p)
    gen_datamodel_file(extracted_kernel_path)
    
def call_gen():
    setup_kernel_files()
    index = enter_input()
    handle_file(file_menu[index])
    
if __name__ == "__main__":
    call_gen()
    clean_files()

