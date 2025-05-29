{
    'name': 'Sale Auto Workflow',
    'summary': '''Sale Auto Workflow ''',
    'description': '''Sale Auto Workflow ''',
    'author': 'Adhichand AP',
    'company': 'Adhichand',
    'maintainer': 'Adhichand',
    'website': 'https://www.linkedin.com/in/adhichand-in/',
    'category': 'sale',
    'depends': ['base','sale','account','stock'],
    'version': '17.0.0.0',
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        # 'data/data.xml',
        'views/res_config_settings.xml',
        'views/sale_order.xml'
    ],
    'images': [],
    'license': 'OPL-1',
    'installable': True,
    'application': False,
}
