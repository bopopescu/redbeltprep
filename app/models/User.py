from system.core.model import Model
from flask import session
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def get_all_users(self):
        print self.db.query_db("SELECT * FROM users")

    def get_user_id(self):
        query = "SELECT id FROM users ORDER BY id DESC LIMIT 1"
        return self.db.query_db(query)

    def creation_validation(self, info):
        print "creation validation method"
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\.-]+\.[a-za-z]*$')
        errors = []
        password = info['password']
        if not info['name']:
            errors.append('Name cannot be blank')
        elif len(info['name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['confirm_pw']:
            errors.append('Password and confirmation must match!')
        if errors:
            return {"status": False, "errors": errors}
        else:
            return{"status": True}

    def register_user(self, info):
        print "registering user"
        pw_hash = self.bcrypt.generate_password_hash(info['password'])
        register_info = [info['name'], info['alias'], info['email'], pw_hash]
        register_query = "INSERT INTO users (name, alias, email, pw_hash, created_at) VALUES (%s, %s, %s, %s, NOW())"
        user = self.db.query_db(register_query, register_info)
        return user


    def validate_login(self, info):
        print "validating user info"
        email = info['email']
        errors = []
        try:
            verify_hash_query = "SELECT id, email, pw_hash FROM users WHERE email = %s"
            verify_hash_data = [email]
            query_return = self.db.query_db(verify_hash_query, verify_hash_data)
            password = info['password']
            if email == query_return[0]['email']:
                print "emails match"
                if self.bcrypt.check_password_hash(query_return[0]['pw_hash'], password):
                    print "passed pw validation"
                    session['id'] = query_return[0]['id']
                    return {"status" : True}
                else:
                    print "failed pw validation"
                    errors.append('incorrect password.')
                    return {"status": False, "errors" : errors}
        except:
            print "bad email."
            errors.append('bad email address.')
            return {"status": False, "errors": errors}

    def get_user_info(self, info):
        get_query = "SELECT * FROM users WHERE id = %s"
        get_data = [info]
        get_return = self.db.query_db(get_query, get_data)
        print "get return", get_return
        return get_return
