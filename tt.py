from git import Repo

repo = Repo('C:\\Users\\practic\Desktop\\gg')
origin = repo.remote(name='test')
origin.push()
