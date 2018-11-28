# lab for using pathlib to handle file system
In [1]: from pathlib import Path

In [2]: # webotron sync kitten_web www.go-fun.com

In [3]: ls
Pipfile       Pipfile.lock  index.html    kitten_web/   webotron/

In [4]: pathname = "kitten_web"

In [5]: path = Path(pathname)

In [6]: path
Out[6]: PosixPath('kitten_web')

In [7]: path.resolve()
Out[7]: PosixPath('/Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web')

In [8]: list(path.iterdir())
Out[8]:
[PosixPath('kitten_web/css'),
 PosixPath('kitten_web/images'),
 PosixPath('kitten_web/index.html')]

In [9]: ls kitten_web/
css/        images/     index.html

In [10]: path.is_dir()
Out[10]: True

In [11]: path.is_file()
Out[11]: False

In [12]: def handle_directory(target)
  File "<ipython-input-12-42e8b618be81>", line 1
    def handle_directory(target)
                                ^
SyntaxError: invalid syntax


In [13]: def handle_directory(target):
    ...:     for p in target.iterdir():
    ...:         if p.is_dir(): handle_directory(p)
    ...:         if p.is_file(): print(p.as_posix())
    ...:

In [14]: path
Out[14]: PosixPath('kitten_web')

In [15]: handle_directory(path)
kitten_web/css/main.css
kitten_web/images/Balinese-kitten1.jpg
kitten_web/images/Maine_coon_kitten_roarie.jpg
kitten_web/images/SFSPCA_Kitten.jpg
kitten_web/index.html

In [16]: # p.as_posix() convert windows system \ to /

In [17]: pathname = "/Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web/"

In [18]: path = Path(pathname)

In [19]: path
Out[19]: PosixPath('/Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web')

In [20]: pathname = "~/code/automating-aws-with-python/01-webotron/kitten_web/"

In [21]: path = Path(pathname)

In [22]: path
Out[22]: PosixPath('~/code/automating-aws-with-python/01-webotron/kitten_web')

In [23]: path.expanduser()
Out[23]: PosixPath('/Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web')

In [24]: # path.expanduser convert ~/ to full pathname

In [25]: handle_directory(path.expanduser())
/Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web/css/main.css
/Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web/images/Balinese-kitten1.jpg
/Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web/images/Maine_coon_kitten_roarie.jpg
/Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web/images/SFSPCA_Kitten.jpg
/Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web/index.html

In [26]: # to storage file in s3 format, we need to know the path relative to the root

In [41]: pathname = "/Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web/"

In [42]: path = Path(pathname)

In [43]: path.expanduser()
Out[43]: PosixPath('/Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web')

In [44]: root = pathname

In [45]: path.relative_to(root)
Out[45]: PosixPath('.')

# current path relative to root
In [46]: path = Path('/Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web/css/main.css')

In [47]: path.relative_to(root)
Out[47]: PosixPath('css/main.css')

In [50]: def handle_directory(target):
    ...:     for p in target.iterdir():
    ...:         if p.is_dir(): handle_directory(p)
    ...:         if p.is_file(): print("Path: {}\n Key: {}".format(p,p.relative_to(root)))
    ...:
    ...:

In [51]: handle_directory(Path(root))                                                                                                   
Path: /Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web/css/main.css
 Key: css/main.css
Path: /Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web/images/Balinese-kitten1.jpg
 Key: images/Balinese-kitten1.jpg
Path: /Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web/images/Maine_coon_kitten_roarie.jpg
 Key: images/Maine_coon_kitten_roarie.jpg
Path: /Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web/images/SFSPCA_Kitten.jpg
 Key: images/SFSPCA_Kitten.jpg
Path: /Users/erilam/code/automating-aws-with-python/01-webotron/kitten_web/index.html
 Key: index.html
