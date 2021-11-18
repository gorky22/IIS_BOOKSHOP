#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from website import create_app, db_connection

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    db_connection.close()