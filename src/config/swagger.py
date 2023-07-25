template = {
    "swagger": "2.0",
    "info": {
        "title": "Rick And Morty Backend Api",
        "description": "API for Rick and Morty Full Stack Project",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "GKP",
            "email": "",
            "url": "https://github.com/GKPavesi",
        },
        "termsOfService": "",
        "version": "1.0"
    },
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ]
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}