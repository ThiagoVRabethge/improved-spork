users = ["Thiago", "José"]

def get_user():
  return users

def get_user_by_id(user_id):
  return users[user_id]

def post_user(user):
  users.append(user.name)

  return users