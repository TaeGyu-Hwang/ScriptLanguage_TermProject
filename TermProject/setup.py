from setuptools import setup, Extension

module = Extension('cLink',
                   sources=[r'C:\Users\user\OneDrive\taegyu\GitHub\ScriptLanguage_TermProject\TermProject\cLink\cLink\cLinkModule.c'],  # 절대 경로로 파일 지정
                   include_dirs=[r'C:\Users\user\AppData\Local\Programs\Python\Python39\include'],  # Python 헤더 파일 경로
                   library_dirs=[r'C:\Users\user\AppData\Local\Programs\Python\Python39\libs'],  # Python 라이브러리 경로
                   libraries=['python39'])

setup(name='cLink',
      version='1.0',
      description='This is a distance calculation package',
      ext_modules=[module])
