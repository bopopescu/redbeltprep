"""
    Routes Configuration File

    Put Routing rules here
"""
from system.core.router import routes


routes['default_controller'] = 'Users'
routes['GET']['/'] = 'Users#index'
routes['POST']['/register'] = 'Users#register'
routes['POST']['/login'] = 'Users#login'
routes['GET']['/logout'] = 'Users#logout'
routes['GET']['/books'] = 'Books#books'
routes['GET']['/books/add'] = 'Books#add'
routes['POST']['/books/create'] = 'Books#create'
routes['GET']['/books/<int:id>'] = 'Books#book_page'
routes['POST']['/books/create/<int:id>'] = 'Books#new_review'
routes['GET']['/users/<int:id>'] = 'Users#user_page'



"""
    routes['GET']['/users'] = 'users#index'
    routes['GET']['/users/new'] = 'users#new'
    routes['POST']['/users'] = 'users#create'
    routes['GET']['/users/<int:id>'] = 'users#show'
    routes['GET']['/users/<int:id>/edit' = 'users#edit'
    routes['PATCH']['/users/<int:id>'] = 'users#update'
    routes['DELETE']['/users/<int:id>'] = 'users#destroy'
"""
