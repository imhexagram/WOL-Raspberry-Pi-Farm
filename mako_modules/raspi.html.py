# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1623224787.6187084
_enable_loop = True
_template_filename = 'modeles/raspi.html'
_template_uri = 'raspi.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        image_list = context.get('image_list', UNDEFINED)
        variable = context.get('variable', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('<!DOCTYPE html>\r\n<html>\r\n    <head>\r\n        <meta name="viewport" content="width=device-width, initial-scale=1.0" charset="utf-8" />\r\n        <title>Wake On Lan - IUT de Valence</title>\r\n\t\t<link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.6.0/css/bootstrap.min.css" rel="stylesheet">\r\n\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>\r\n\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.6.0/js/bootstrap.min.js"></script>\r\n\t</head>\r\n    <body>\r\n\t\t<div class="jumbotron text-center" style="margin-bottom: 0;">\r\n\t\t\t<h2>Wake On Lan -IUT de Valence</h2>\r\n\t\t\t<p>Appli web du projet WOL</p>\r\n\t\t</div>\r\n\r\n\t\t<nav class="navbar navbar-expand-sm bg-light">\r\n\t\t\t<ul class="navbar-nav">\r\n\t\t\t  <li class="nav-item">\r\n\t\t\t\t<a class="nav-link" href="/index">Accueil</a>\r\n\t\t\t  </li>\r\n\t\t\t  <li class="nav-item">\r\n\t\t\t\t<a class="nav-link" href="/static/Auth.html">Authentification</a>\r\n\t\t\t  </li>\r\n\t\t\t  <li class="nav-item">\r\n\t\t\t\t<a class="nav-link" href="../Renouveler?salle=1&ordre=0&textRe=">Machine</a>\r\n\t\t\t  </li>\r\n\t\t\t</ul>\r\n\t\t</nav>\r\n\r\n\t\t<p1>Bonjour, bienvenu dans notre site! Ici vous pouvez superviser les raspberry pi.</p1>\r\n\t\t<button type="button" class="btn btn-info btn-sm" onclick="help()">help</button><br/><hr/>\r\n\t\t<script>\r\n\t\t\tfunction help(){\r\n\t\t\t\talert("Le bouton \'Réveiller\' fonctionne seulement pour Status=Off et PoE Mode=Shutdown. \\nLe bouton \'Arrêter\' éteint le Raspi et mettre PoE Mode=Shutdown. \\nLe bouton \'Stop\' met PoE Mode=Shutdown, si le status Raspi est \'On\', arrêt violent.")\r\n\t\t\t}\r\n\t\t</script>\r\n\t\t<script type="text/javascript">\r\n\t\t\tvar isCheckAll=false;\r\n\t\t\tfunction swapCheck(){\r\n\t\t\t\tif(isCheckAll){\r\n\t\t\t\t\t$("input[type=\'checkbox\'").each(function(){\r\n\t\t\t\t\t\tthis.checked=false;\r\n\t\t\t\t\t});\r\n\t\t\t\t\tisCheckAll=false;\r\n\t\t\t\t}else{\r\n\t\t\t\t\t$("input[type=\'checkbox\'").each(function(){\r\n\t\t\t\t\t\tthis.checked=true;\r\n\t\t\t\t\t});\r\n\t\t\t\t\tisCheckAll=true;\r\n\t\t\t\t}\r\n\t\t\t}\r\n\t\t</script>\r\n\t\t<br>\r\n\t\t\r\n\t\t<form method="get" action="../Renouveler_Raspi">\r\n            <p2>Liste des Raspberry Pi : </p2>\r\n\t\t\t<button type="submit" class="btn btn-sm btn-primary">Renouveler</button></br>\r\n\t\t\t<label>Switch : </label>  \r\n\t\t\t<select name="switch">\r\n\t\t\t\t<option value="172.25" selected="selected">All</option>\r\n\t\t\t\t<option value="172.25.206.99">Switch1</option>\r\n\t\t\t\t<option value="172.25.206.98">Switch2</option>\r\n\t\t\t</select>\r\n\t\t\t<hr/>\r\n\t\t</form>\r\n\t\t<form method="get" action="../Action_Raspi">\r\n\t\t\t<select name="choix">\r\n\t\t\t\t<option value="" selected="selected"></option>\r\n\t\t\t\t<option value="reveiller">Réveiller</option>\r\n\t\t\t\t<option value="arreter">Arrêter</option>\r\n\t\t\t\t<option value="stop">Stop PoE</option>\r\n\t\t\t\t<option value="changer">Changer Image</option>\r\n\t\t\t\t<option value="recharger">Recharger Image</option>\r\n\t\t\t</select>\r\n\t\t\t<select name="image">\r\n\t\t\t\t<option value="" selected="selected"></option>\r\n')
        for a in image_list :
            __M_writer('\t\t\t\t\t<option value=')
            __M_writer(str(a))
            __M_writer('>')
            __M_writer(str(a))
            __M_writer('</option>\r\n')
        __M_writer('\t\t\t</select>\r\n\t\t\t<button type="submit" class="btn btn-sm btn-primary">Valider</button>\r\n\t\t\r\n\t\t\t<div class="table-responsive">\r\n\t\t\t\t<table class="table table-hover table-bordered thead-light">\r\n\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t<th><input type="checkbox" onclick="swapCheck()"></th>\r\n\t\t\t\t\t\t<th>ID</th>\r\n\t\t\t\t\t\t<th>Hostname</th>\r\n\t\t\t\t\t\t<th>Switch</th>\r\n\t\t\t\t\t\t<th>Port</th>\r\n\t\t\t\t\t\t<th>Image</th>\r\n\t\t\t\t\t\t<th>Recharge</th>\r\n\t\t\t\t\t\t<th>Status</th>\r\n\t\t\t\t\t\t<th>PoE Mode</th>\r\n\t\t\t\t\t\t<th>Boutton</th>\r\n\t\t\t\t\t</tr>\r\n')
        for a,b,c,d,e,f,g,h in variable :
            __M_writer('\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t<td><input type="checkbox" name="hostnames" value=')
            __M_writer(str(b))
            __M_writer('></td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(a))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(b))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(c))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(d))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(e))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(f))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(g))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(h))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>\r\n\t\t\t\t\t\t\t\t<table>\r\n\t\t\t\t\t\t\t\t<tr>\r\n\r\n\t\t\t\t\t\t\t\t<form method="get" action="../Reveiller_Raspi">\r\n\t\t\t\t\t\t\t\t<button type="submit" class="btn btn-light" name="hostname" value=')
            __M_writer(str(b))
            __M_writer('>Réveiller</button>\r\n\t\t\t\t\t\t\t\t</form>\r\n\t\t\t\t\t\t\t\t<form method="get" action="../Arreter_Raspi">\r\n\t\t\t\t\t\t\t\t\t<button type="submit" class="btn btn-light" name="hostname" value=')
            __M_writer(str(b))
            __M_writer('>Arrêter</button>\r\n\t\t\t\t\t\t\t\t</form>\r\n\t\t\t\t\t\t\t\t<form method="get" action="../Stop_Raspi">\r\n\t\t\t\t\t\t\t\t\t<button type="submit" class="btn btn-danger" name="hostname" value=')
            __M_writer(str(b))
            __M_writer(' onclick="return window.confirm(\'Etes-vous sûr?\');">Stop PoE</button>\r\n\t\t\t\t\t\t\t\t</form>\r\n\r\n\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t</table>\r\n\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t</tr>\r\n')
        __M_writer('\t\t\t\t</table></br>\r\n\t\t\t</div>\r\n\t\t</form>\r\n\t\t<hr/>\r\n\t\t<div class="jumbotron text-center" style="margin-bottom: 0;">\r\n\t\t\t<h4>Bien travailler </h4>\r\n\t\t<p id="auteur">@2021 R&T Projet WOL - Ziyi LIU</p>\r\n\t\t</div>\r\n    </body>\r\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "modeles/raspi.html", "uri": "raspi.html", "source_encoding": "utf-8", "line_map": {"16": 0, "23": 1, "24": 77, "25": 78, "26": 78, "27": 78, "28": 78, "29": 78, "30": 80, "31": 97, "32": 98, "33": 99, "34": 99, "35": 100, "36": 100, "37": 101, "38": 101, "39": 102, "40": 102, "41": 103, "42": 103, "43": 104, "44": 104, "45": 105, "46": 105, "47": 106, "48": 106, "49": 107, "50": 107, "51": 113, "52": 113, "53": 116, "54": 116, "55": 119, "56": 119, "57": 127, "63": 57}}
__M_END_METADATA
"""
