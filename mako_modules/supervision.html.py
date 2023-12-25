# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1623399337.0117345
_enable_loop = True
_template_filename = 'modeles/supervision.html'
_template_uri = 'supervision.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        variable = context.get('variable', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('<!DOCTYPE html>\r\n<html>\r\n    <head>\r\n        <meta name="viewport" content="width=device-width, initial-scale=1.0" charset="utf-8" />\r\n        <title>Wake On Lan - IUT de Valence</title>\r\n\t\t<link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.6.0/css/bootstrap.min.css" rel="stylesheet">\r\n\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>\r\n\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.6.0/js/bootstrap.min.js"></script>\r\n\t</head>\r\n    <body>\r\n\t\t<div class="jumbotron text-center" style="margin-bottom: 0;">\r\n\t\t\t<h2>Wake On Lan -IUT de Valence</h2>\r\n\t\t\t<p>Appli web du projet WOL</p>\r\n\t\t</div>\r\n\r\n\t\t<nav class="navbar navbar-expand-sm bg-light">\r\n\t\t\t<ul class="navbar-nav">\r\n\t\t\t  <li class="nav-item">\r\n\t\t\t\t<a class="nav-link" href="/index">Accueil</a>\r\n\t\t\t  </li>\r\n\t\t\t  <li class="nav-item">\r\n\t\t\t\t<a class="nav-link" href="/static/Auth.html">Authentification</a>\r\n\t\t\t  </li>\r\n\t\t\t  <li class="nav-item">\r\n\t\t\t\t<a class="nav-link" href="../Raspi">Raspi</a>\r\n\t\t\t  </li>\r\n\t\t\t</ul>\r\n\t\t</nav>\r\n\r\n\t\t<p1>Bonjour, bienvenu dans notre site! Ici vous pouvez superviser les machines.</p1>\r\n\t\t<button type="button" class="btn btn-info btn-sm" onclick="help()">help</button><br/><hr/>\r\n\t\t<script>\r\n\t\t\tfunction help(){\r\n\t\t\t\talert("Lorsque la machine est éteinte, l\'heure de démarrage est nulle. \\nIl faut du temps pour \'Renouveler\' et \'Réveiller\'. \\nVeuillez \'Renouveler\' manuellement environ une minute après le \'Réveiller\', si la machine ne toujour pas en ligne, le rack a peut-être été emporté.")\r\n\t\t\t}\r\n\t\t</script>\r\n\t\t<br>\r\n\t\t\r\n\t\t<form method="get" action="../Renouveler">\r\n            <p2>Liste des PC de la salle : </p2>\r\n\t\t\t<button type="submit" class="btn btn-sm btn-primary">Renouveler</button></br>\r\n\t\t\t<label>Salle : </label>  \r\n\t\t\t<select name="salle">\r\n\t\t\t\t<option value="" selected="selected">All</option>\r\n\t\t\t\t<option value="172.21">C113</option>\r\n\t\t\t\t<option value="172.25">D102</option>\r\n\t\t\t\t<option value="172.23">D103</option>\r\n\t\t\t\t<option value="172.24">D106</option>\r\n\t\t\t</select>\r\n\t\t\t<label>Ordre : </label>  \r\n\t\t\t<select name="ordre">\r\n\t\t\t\t<option value="0" selected="selected">ID</option>\r\n\t\t\t\t<option value="1">Hostname</option>\r\n\t\t\t\t<option value="5">Nom étudiant</option>\r\n\t\t\t\t<option value="6">Group</option>\r\n\t\t\t\t<option value="2">IP</option>\r\n\t\t\t\t<option value="7">Temps de démarrage</option>\r\n\t\t\t</select>\r\n\t\t\t<label>Recherche : </label>\r\n\t\t\t<input type="text" value="" name="textRe" />\r\n\t\t\t<hr/>\r\n\t\t</form>\r\n\t\t\t<div class="table-responsive">\r\n\t\t\t\t<table class="table table-hover table-bordered thead-light">\r\n\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t<th>ID</th>\r\n\t\t\t\t\t\t<th>Hostname</th>\r\n\t\t\t\t\t\t<th>Nom étudiant</th>\r\n\t\t\t\t\t\t<th>Group</th>\r\n\t\t\t\t\t\t<th>Addr_IP</th>\r\n\t\t\t\t\t\t<th>Addr_MAC</th>\r\n\t\t\t\t\t\t<th>Heure de démarrage</th>\r\n\t\t\t\t\t\t<th>Temps de démarrage</th>\r\n\t\t\t\t\t\t<th>Boutton</th>\r\n\t\t\t\t\t</tr>\r\n')
        for a,b,c,d,e,f,g,h in variable :
            __M_writer('\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(a))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(b))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(f))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(g))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(c))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(d))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(e))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>')
            __M_writer(str(h))
            __M_writer('</td>\r\n\t\t\t\t\t\t\t<td>\r\n\t\t\t\t\t\t\t\t<form method="get" action="../Reveiller">\r\n\t\t\t\t\t\t\t\t<button type="submit" class="btn btn-light" name="hostname" value=')
            __M_writer(str(b))
            __M_writer('>Réveiller</button>\r\n\t\t\t\t\t\t\t\t</form>\r\n\t\t\t\t\t\t\t\t<form method="get" action="../Supprimer">\r\n\t\t\t\t\t\t\t\t<button type="submit" class="btn btn-danger" name="pc" value=')
            __M_writer(str(a))
            __M_writer(' onclick="return window.confirm(\'Etes-vous sûr?\');">Supprimer</button>\r\n\t\t\t\t\t\t\t\t</form>\r\n\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t</tr>\r\n')
        __M_writer('\t\t\t\t</table></br>\r\n\t\t\t</div>\r\n\t\t<hr/>\r\n\t\t<div class="jumbotron text-center" style="margin-bottom: 0;">\r\n\t\t\t<h4>Bien travailler </h4>\r\n\t\t<p id="auteur">@2021 R&T Projet WOL - Ziyi LIU</p>\r\n\t\t</div>\r\n    </body>\r\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "modeles/supervision.html", "uri": "supervision.html", "source_encoding": "utf-8", "line_map": {"16": 0, "22": 1, "23": 76, "24": 77, "25": 78, "26": 78, "27": 79, "28": 79, "29": 80, "30": 80, "31": 81, "32": 81, "33": 82, "34": 82, "35": 83, "36": 83, "37": 84, "38": 84, "39": 85, "40": 85, "41": 88, "42": 88, "43": 91, "44": 91, "45": 96, "51": 45}}
__M_END_METADATA
"""
