from distutils.core import setup
setup(
  name = 'KutanSpeech',
  packages = ['KutanSpeech'],
  version = '1.02',
  license = 'MIT',
  description = 'Word by word Speech Recognition Library.',
  author = 'Mustafa Kaan Kutan',
  author_email = 'mkkwin10@gmail.com',
  url = 'https://github.com/kaankutan/kutanspeech',
  download_url = 'https://github.com/kaankutan/KutanSpeech/archive/1.20.tar.gz',
  keywords = ['Wordbyword', 'Speech', 'Recognition', 'Library'],
  install_requires=[
          'SpeechRecognition',
          'PyAudio',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
