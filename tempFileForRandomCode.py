# welcomeNotification.set(f'Welcome {username.get()}!')
#             loginButton.grid_remove()
#             switchAccountButton.grid(row=0, column=0, sticky='E', padx=(0,4))
#             logOutButton.grid(row=0, column=1, sticky='E')
#             if GetValueFromUser(username.get(), 'designation') == 'admin':
#                 adminFrame.grid(row=0, column=1, sticky='E', padx=(0, 4))
#                 headerFrame.columnconfigure(1, weight=1)
#                 generalFrame.grid_remove()
#             else:
#                 generalFrame.grid(row=0, column=1, sticky='E', padx=(0, 4))
#                 headerFrame.columnconfigure(1, weight=1)
#                 adminFrame.grid_remove()