from system.core.model import Model
from flask import session

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def get_all_users(self):
        print self.db.query_db("SELECT * FROM users")

    def register_user(self, info):
        print "registering user"
        pw_hash = self.bcrypt.generate_password_hash(info['password'])
        register_info = [info['name'], info['alias'], info['email'], pw_hash]
        register_query = "INSERT INTO users (name, alias, email, pw_hash, created_at) VALUES (%s, %s, %s, %s, NOW())"
        return self.db.query_db(register_query, register_info)


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
