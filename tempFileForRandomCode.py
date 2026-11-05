import sqlite3
#
# def searchFilter(Query: str, Filters: list):
#     with sqlite3.connect('users.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute(f"SELECT * FROM users WHERE username = '{Query}' AND " + " AND ".join([f"tags LIKE '%{i}%'" for i in Filters]))
#         return cursor.fetchall()
#
# def AddElement(content):
#     element = ttk.Frame(elementsFrame)
#     structureFrame = ttk.Frame(element)
#     structureFrame.grid(row=0, column=0, sticky='NSEW')
#
#     fields = {}
#
#     if content:
#         for k, v in content.items():
#             fields[k] = {}
#             fields[k]['label'] = elements['structure']['labels'][k]
#             fields[k]['value'] = v
#             fields[k]['elementType'] = elements['structure']['elementTypes'][k]
#     else:
#         for k, v in elements['structure'].items():
#             fields[k] = {}
#             fields[k]['label'] = v['labels'][k]
#             fields[k]['value'] = ''
#             fields[k]['elementType'] = v['elementTypes'][k]
#
#     getter = LabelledListMaker(structureFrame, fields, 'core')
#     getters.append(getter)
#     structureFrame.grid_remove()
#
#     collapsedFrame = ttk.Frame(element)
#     collapsedFrame.grid(row=0, column=0, sticky='NSEW')
#     dropdownText = StringVar()
#     ttk.Label(collapsedFrame,
#               textvariable=dropdownText,
#               style='Body.TLabel',
#               justify='left').grid(row=0, column=0, sticky='W')
#     dropdownText.set('⏵ ' + ' - '.join(content.values()))
#
#     ttk.Button(
#         element,
#         text='Remove',
#         style='Buttons.TButton',
#         command=lambda frame=element, getter=getter:
#         DeleteElement(frame, getter)
#     ).grid(column=1, row=0, sticky='E', padx=2)
#
#     element.pack(anchor='w', pady=5)
#
#
# for i in elements['values']:
#     AddElement(i)


