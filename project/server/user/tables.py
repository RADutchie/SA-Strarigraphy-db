# project/server/user.py


from flask_table import Table, Col, LinkCol

class IndexTable(Table):
    classes = ['table', 'table-striped']
    id = Col('Id', show=False)
    unit_name = Col("Unit Name")
    strat_no = Col("SA strat unit number")
    map_symbol = Col("Map symbol")
    view = LinkCol('View record', 'user.view', url_kwargs=dict(id='id'))
    edit = LinkCol('Edit record', 'user.edit', url_kwargs=dict(id='id'))