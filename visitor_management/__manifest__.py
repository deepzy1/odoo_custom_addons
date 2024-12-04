{
    'name': 'Visitor Management',
    'version': '1.1',
    'summary': 'Manage visitor registrations and station kiosks in your company.',
    'sequence': 10,
    'description': """
        This module enables managing visitor registrations at various stations (entry gates) in a company.
        Features include:
        - Station creation and management
        - Kiosk URLs and QR codes for visitor check-ins
        - Visitor registration via kiosks or manual entries by security
        - Frontend interface for visitor check-in
    """,
    'author': 'Deepak R ,,',
    'website': '',
    'category': 'Operations',
    'depends': ['base', 'web', 'mail', 'website','hr'],
    'data': [
        'security/security_host_admin.xml',
        'views/minimal_layout.xml',
        'security/ir.model.access.csv',
        'views/visitor_registration.xml',
        'views/station2.xml',
        'views/visitor.xml',
        'views/today.xml',
        'views/menus.xml',
        'views/asset.xml',

        'views/visitor_templates.xml',
       # Include visitor templates
        # 'views/website_templates.xml',

    ],

    'assets': {
        # 'web.assets_backend': [
        #     'visitor_management/static/src/scss/styles.scss',
        #     'visitor_management/static/src/js/custom_backend.js',
        # ],
        'web.assets_frontend': [
            # 'visitor_management/static/src/js/custom_frontend.js',
            'visitor_management/static/src/css/style.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
