#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
程序启动入口
"""
from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

#自动导入数据库模型
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role,
                )

# 程序启动
if __name__ == '__main__':
    app.run()